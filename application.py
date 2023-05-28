from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from controls import *
from constants import *

application = Flask(__name__)

application.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:Stason2407@datacolldb.curf1kkopmp5.eu-central-1.rds.amazonaws.com'
db = SQLAlchemy(application)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    country = db.Column(db.String(300), nullable=False)
    pos_text = db.Column(db.Text, nullable=False)
    neg_text = db.Column(db.Text, nullable=False)


    def __repr__(self):
        return '<Review %r>' % self.id

with application.app_context():
    db.create_all()


"""
    db.session.add(User(username="example"))
    db.session.commit()

    users = db.session.execute(db.select(User)).scalars()"""


# emission calculate
fly_green = Carbon()


@application.route('/')
@application.route('/home')
def home():
    """index page"""
    departure_date, return_date = get_dates()
    return render_template('index.html', data_departure=departure_date, data_return=return_date)



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
            return render_template('currency.html', data=f'Rates from Data: {data}', amount=amount, from_currency=from_currency + " =",
                                   converted_amount=converted_amount, to_currency=to_currency, currencies=CURRENCY_NAMES)

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

@application.route('/posts')
def posts():
    """Posts page"""
    return render_template('post.html')

if __name__ == '__main__':
    application.run(port=5001, debug=True)
