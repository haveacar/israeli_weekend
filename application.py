from flask import Flask, render_template, request
from controls import *
import os
from models import db


# set up flask
application = Flask(__name__)
# database Path
DB_PATH = os.path.join(os.path.dirname(__file__), 'travel_test.db')

STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
# specify the directory where you want to save uploaded files
application.config['UPLOAD_FOLDER'] = os.path.join(STATIC_PATH, 'images_post')


# database PostgreSQL connect
application.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:////{DB_PATH}'
db.init_app(application)

# create table
with application.app_context():
    db.create_all()

# emission calculate
fly_green = Carbon()



if __name__ == '__main__':
    application.run(port=5003, debug=False)
