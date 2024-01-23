from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("settings.default")
db = SQLAlchemy(app)

from application.views.task_manager import *
