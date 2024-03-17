import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("settings.default")
db = SQLAlchemy(app)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s -> [%(filename)s:%(lineno)s-%(funcName)20s()]')

from application.views.task_manager import *
