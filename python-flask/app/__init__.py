import os
from flask import Flask
from app.extensions.db import db


def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://loc_user:loc_pass@192.168.137.64/location_app"
    #app.config['SQLALCHEMY_DATABASE_URI'] = \
    #    'sqlite:///' + os.path.join(basedir, 'database.db')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app
