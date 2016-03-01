===============================
Async Runner
===============================

.. image:: https://img.shields.io/pypi/v/async_runner.svg
        :target: https://pypi.python.org/pypi/async_runner

.. image:: https://img.shields.io/travis/vedarthk/async_runner.svg
        :target: https://travis-ci.org/vedarthk/async_runner

.. image:: http://readthedocs.org/projects/async-runner/badge/?version=latest
        :target: http://async-runner.readthedocs.org/en/latest/?badge=latest
        :alt: Documentation Status


Async runner is a thin wrapper over Celery API. This will enable control over failed messages by moving them to separate queue (generally queue_name_error) and also allows to retry the task with the help of retry policy.


More can be found at documentation: https://async_runner.readthedocs.org


.. code-block:: python

    from async_runner import async_runner
    async_runner.send_task(
        task_fn=func,  # task function can be python module path
        queue='queue_name',  # name of the queue
        args=(arg1, arg2, arg3, ),  # tuple/list of positional arguments to task function
        kwargs={'name': 'parameter'},  # dictionary with key word arguments to task function
        options={
            'max_retries': 3,  # maximum number of times the task is retried
            'retry_policy': {
                'retry_interval': 12  # interval between retires (in seconds)
            }
        }
    )


**TODO:** Decouple from Django
