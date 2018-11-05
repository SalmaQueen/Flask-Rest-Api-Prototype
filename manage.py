#!/usr/bin/env python3
import os

from flask_script import Manager
# https://flask-script.readthedocs.io/en/latest/

from flask_migrate import Migrate, MigrateCommand
# https://flask-migrate.readthedocs.io/en/latest/

from sqlalchemy_utils.functions import create_database, drop_database

from api.__init__ import app, databases

migrate = Migrate(app, databases)
manager = Manager(app)
manager.add_command('databases', MigrateCommand)


@manager.command
def createdb():
    try:
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])
    except:
        print("Could not create a database")


@manager.command
def dropdb():
    try:
        drop_database(app.config['SQLALCHEMY_DATABASE_URI'])
    except:
        print("Could not drop a database")


if __name__ == '__main__':
    manager.run()