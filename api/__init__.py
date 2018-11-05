from api.v1.demo import *
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from instance.config import application_configuration

app = Flask(__name__)


def environment_name(environment):
    app.config.from_object(application_configuration[environment])


environment_name('DevelopmentEnvironment')
databases = SQLAlchemy(app)
