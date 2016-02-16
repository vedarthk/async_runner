# -*- coding: utf-8 -*-
"""
    async_runner.async_runner
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Async task runner, wrapper over Celery.

"""

import types
import platform
import importlib

from django.conf import settings
from celery import task, execute
from celery.utils.log import get_task_logger

__all__ = ('send_task', 'schedule_run')

log = get_task_logger(__name__)


def send_task(task_fn, queue, args=None, kwargs=None, **options):
    """Execute background task with Celery.
    If task fails it will get enqueued in error queue and can be re-proccessed.
    Error queue can be specified in options.

    :param task_fn: function to execute as background task
    :param queue: `kombu.Queue` object
    :param args: positional arguments to task function
    :param kwargs: key word arguments to task function
    :returns: Query task state.
    :rtype: ``celery.result.AsyncResult``

    """
    options['queue'] = queue

    if not isinstance(task_fn, types.FunctionType):
        task_fn = _import(task_fn)

    return execute.send_task(
        'async_runner.async_runner.run',
        kwargs={
            'task_fn': task_fn,
            'args': args or tuple(),
            'kwargs': kwargs or {},
            'options': options.copy(),
        },
        **options
    )


@task
def run(task_fn, args, kwargs, options):
    """Celery task function which will execute function provided as `task_fn`.

    :param task_fn: function to be executed as task
    :param args: arguments to task function
    :param kwargs: key word arguments to task function
    :param options: options passed while `send_task` was called
    :returns:
    :rtype: ``NoneType``

    """

    func_signature = _func_signature(task_fn)
    log.info(u'Running {} [{}]'.format(
        func_signature, run.request.id))

    try:
        task_fn(*args, **kwargs)
    except Exception as e:
        if options.get('retry', False):
            return retry_run(
                task_fn=task_fn, args=args, kwargs=kwargs, options=options)

        _send_to_error_queue(task_fn, args, kwargs, options)

        _process_task_exception(data={
            'task': func_signature,
            'task_request_id': run.request.id,
            'task_args': args,
            'task_kwargs': kwargs,
            'task_options': options,
            'node': platform.node()
        }, exception=e)
        raise


@task
def schedule_run(task_fn, queue, args=None, kwargs=None, **options):
    """This can be used to schedule task (via Celery beat) with async runner.

    :param task_fn: function to execute as background task
    :param args: positional arguments to task function
    :param kwargs: key word arguments to task function
    :returns: Query task state.
    :rtype: ``celery.result.AsyncResult``

    """
    return send_task(task_fn, queue, args=args, kwargs=kwargs, **options)


def _send_to_error_queue(task_fn, args, kwargs, options):
    log.info(u'Moving to error queue {}'.format(_func_signature(task_fn)))
    error_options = options.copy()
    error_options['queue'] = '{}_error'.format(error_options['queue'])

    # remoce countdown on task when moving to error queue
    error_options.pop('countdown', None)

    run.apply_async(
        kwargs={
            'task_fn': task_fn,
            'args': args,
            'kwargs': kwargs,
            'options': options,
        }, **error_options
    )


def retry_run(task_fn, args, kwargs, options):
    """Retry celery task function which will execute function provided as `task_fn`.

    :param task_fn: function to be executed as task
    :param args: arguments to task function
    :param kwargs: key word arguments to task function
    :param options: options passed while `send_task` was called
    :returns:
    :rtype: ``NoneType``

    """

    assert 'retry_policy' in options,\
        'Specify `retry_policy` in `options` to retry task'

    log.info(u'Retrying {} with retry_policy={}'.format(
        _func_signature(task_fn), options['retry_policy']))

    retry_options = _update_options_for_retry(options)

    if not retry_options.get('retry', True):
        log.info(u'Maximum retries reached for {}'.format(
            _func_signature(task_fn)))

    run.apply_async(
        kwargs={
            'task_fn': task_fn,
            'args': args or tuple(),
            'kwargs': kwargs or {},
            'options': options.copy(),
        },
        **retry_options
    )


def _update_options_for_retry(options):
    retry_count = options['retry_count'] = options.get('retry_count', 0) + 1
    retry_policy = options['retry_policy']
    options['countdown'] = retry_policy['retry_interval']

    if retry_count == options['max_retries']:
        options['retry'] = False
    return options


def _func_signature(fn):
    """Create signature string for given function object.

    :param fn: function for which signature will be generated
    :returns: string with module path of function
    :rtype: ``unicode``

    """
    return u'{}.{}'.format(fn.__module__, fn.__name__)


def _process_task_exception(data, exception):
    """Process exception which occured while execution of the task.
    To process the exception, a function has to be given in settings
    file of Django.

    eg:
    ASYNC_RUNNER = {
        'EXCEPTION_PROCESSOR': 'module.path.function'
    }

    OR

    ASYNC_RUNNER = {
        'EXCEPTION_PROCESSOR': module.function
    }

    :param data: data containg task and node on which it was executing
    :param exception: exception object generated in the task
    :returns: ``None``
    :rtype: ``NoneType``

    """
    ASYNC_RUNNER = getattr(settings, 'ASYNC_RUNNER', None)
    if ASYNC_RUNNER and 'EXCEPTION_PROCESSOR' in ASYNC_RUNNER:
        exception_processor = ASYNC_RUNNER['EXCEPTION_PROCESSOR']
        if not isinstance(exception_processor, types.FunctionType):
            exception_processor = _import(exception_processor)

        exception_processor(data=data, exception=exception)


def _import(module_path):
    """Import module path as python object.

    :param module_path: module path of the python object
    :returns: python object

    """
    parts = module_path.split('.')
    module_name, name = '.'.join(parts[:-1]), parts[-1]

    return getattr(importlib.import_module(module_name), name)
