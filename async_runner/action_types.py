from enum import Enum

class Actions(Enum):
    enqueued = 'enqueued'
    picked_up = 'picked_up'
    completed = 'completed'
    error = 'error'
