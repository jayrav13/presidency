<<<<<<< HEAD
from debates import Debate, Debates
from executive_orders import Year, Order, Orders
=======
"""
__init__

Establish this Flask app.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_httpauth import HTTPBasicAuth
from flask_json import FlaskJSON
import logging
import os

app = Flask(__name__)
app.config.from_pyfile('../config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

auth = HTTPBasicAuth()

json = FlaskJSON(app)

from presidency import views, models
>>>>>>> 1e0368128bfeb26f485081a1ac90049118ff556a
