from flask import Flask, render_template, request
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import desc
from controls import *
from constants import *
from datetime import datetime
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

# create table
with application.app_context():
    db.create_all()


# emission calculate
fly_green = Carbon()

@application.route('/')
@application.route('/home')
def home():
    """index page"""
    # generate dates for search
    departure_date, return_date = get_dates()
    template_data = {
        'data_departure': departure_date,
        'data_return': return_date,
    }

    return render_template('index.html', **template_data)


@application.route('/currency', methods=['GET', 'POST'])
def currency():
    """currency convector page"""
    if request.method == 'POST':

        amount = float(request.form['amount'])
        from_currency = request.form['from_currency'][:3]
        to_currency = request.form['to_currency'][:3]

        # get data request
        currency_data = receive_data()
        if currency_data != False:
            # get current data rates
            data = currency_data.get("date")
            conversion_rate = currency_data.get("rates")[to_currency] / \
                              currency_data.get("rates")[from_currency]

            converted_amount = round(amount * conversion_rate, 2)  # round
            # return template rates
            return render_template('currency.html', data=f'Rates from Data: {data}', amount=amount,
                                   from_currency=from_currency + " =",
                                   converted_amount=converted_amount, to_currency=to_currency,
                                   currencies=CURRENCY_NAMES)

        else:
            return render_template('currency.html', data="Oops:( Something Wrong", currencies=CURRENCY_NAMES)
    else:
        return render_template('currency.html', currencies=CURRENCY_NAMES)


@application.route('/carbon', methods=['GET', 'POST'])
def carbon():
    """emission calculate"""
    if request.method == 'POST':
        # get from page
        from_city = request.form['input1']
        to_city = request.form['input2']
        passengers_n = request.form['input3']
        round_trip = request.form.get('checkbox')

        # output roundtrip
        trip = ""
        if round_trip: trip = "(Round Trip)"
        try:
            # get result from carbon api
            result = fly_green.carbon_request(from_city, to_city, round_trip, int(passengers_n))
            distance = result['data']['attributes']['distance_value']
            carbon_kg = result['data']['attributes']['carbon_kg']
        except:
            return render_template('carbon.html', error="Oops:( Something Wrong")

        else:
            return render_template('carbon.html', from_city=f' From : {from_city}', to_city=f'To: {to_city}{trip}',

                                   distance=f'Distance:{distance} km',
                                   carbon_kg=f'Calculated emissions: {carbon_kg} kg')
    else:
        return render_template('carbon.html')


@application.route('/contact')
def contact():
    """Contact Us page"""
    return render_template('contact.html')


@application.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@application.route('/airlines')
def airlines():
    """Airlines page"""
    return render_template('airlines.html')


@application.route('/login', methods=['GET', 'POST'])
def login():
    '''Login function'''
    return "Login"


if __name__ == '__main__':
    application.run(port=5005, debug=False)
