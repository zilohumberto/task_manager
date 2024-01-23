from enum import Enum


class TaskStatus(Enum):
    """
        CREATE -> (initial state)
                RUNNING ->
                    CANCELLED (end state)
                    ERROR (end state)
                    DONE (end state)


    """
    CREATED = 1
    RUNNING = 2
    CANCELLED = 3
    FAILED = 4  # TBD: unused, how to handle errors?
    DONE = 5
