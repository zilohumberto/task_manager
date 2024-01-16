import os
from dotenv import load_dotenv


load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")

PG_DBS = {
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "db": POSTGRES_DB,
    "host": POSTGRES_HOST,
    "port": POSTGRES_PORT,
}

SQLALCHEMY_DATABASE_URI = (
    "postgresql://{user}:{password}@{host}:{port}/{db}?client_encoding=utf-8".format(
        **PG_DBS
    )
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
STATEMENT_TIMEOUT = 105000

# TASK MANAGER SETTINGS
KEEP_RUNNING_TASK_MANAGER: bool = True
MAX_TIMEOUT_SECONDS: int = 5*60  # 5 minutes = 300 seconds
