from .definition.pi import get_pi
from .definition.send_emails import send_emails
from .definition.wait_5s import wait_5s
from .definition.wait_1m import wait_1m

TASK_MAP = {
    "get_pi": get_pi,
    "send_emails": send_emails,
    "wait_5s": wait_5s,
    "wait_1m": wait_1m,
}
