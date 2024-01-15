import os
from dotenv import load_dotenv


load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")

# TASK MANAGER SETTINGS
KEEP_RUNNING_TASK_MANAGER: bool = True
MAX_TIMEOUT_SECONDS: int = 5 * 60  # 5 minutes = 300 seconds
