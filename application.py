from flask import Flask, render_template, request
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
import views
from controls import *
import os
from models import db, Users


# set up flask
application = Flask(__name__)
# database Path
DB_PATH = os.path.join(os.path.dirname(__file__), 'travel_test.db')

STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
# specify the directory where you want to save uploaded files
application.config['UPLOAD_FOLDER'] = os.path.join(STATIC_PATH, 'images_post')
application.config['SECRET_KEY'] = SECRET_KEY
application.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# database PostgreSQL connect
application.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:////{DB_PATH}'
db.init_app(application)

admin = Admin(application, name='My App Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Users, db.session))

# initialization views
views.init(application)

# create table
with application.app_context():
    db.create_all()


if __name__ == '__main__':
    application.run(port=5000, debug=False)
