from .pi import get_pi
from .send_emails import send_emails
from .wait_5s import wait_5s

TASK_MAP = {
    "get_pi": get_pi,
    "send_emails": send_emails,
    "wait_5s": wait_5s,
}
