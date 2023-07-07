from flask import Flask, render_template, request, redirect
from sqlalchemy import desc
from controls import *
from constants import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os

# set up flask
application = Flask(__name__)
# database Path
DB_PATH = os.path.join(os.path.dirname(__file__), 'travel_test.db')

# database connect
application.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:////{DB_PATH}'

db = SQLAlchemy(application)

STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
# specify the directory where you want to save uploaded files
application.config['UPLOAD_FOLDER'] = os.path.join(STATIC_PATH, 'images_post')


# class DB review
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    country = db.Column(db.String(300), nullable=False)
    pos_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    img_name = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Review %r>' % self.id


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Client %r>' % self.email


# create table
with application.app_context():
    db.create_all()

# emission calculate
fly_green = Carbon()


def get_reviews() -> list:
    """Func to get data from Database"""
    review_list = []
    try:
        reviews = Review.query.order_by(desc(Review.date)).limit(6).all()
    except:
        print("Database error")
    else:
        for review in reviews:
            review_dict = {}
            review_dict['id'] = review.id
            review_dict['name'] = review.name
            review_dict['country'] = review.country
            review_dict['pos_text'] = review.pos_text
            review_dict['rating'] = review.rating
            review_dict['date'] = review.date.strftime('%Y-%m-%d %H:%M:%S')
            review_dict['img_name'] = review.img_name
            review_list.append(review_dict)
        return review_list


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


@application.route('/posts', methods=['GET', 'POST'])
def posts():
    """Posts page"""
    if request.method == "POST":

        title = request.form["title"].capitalize()
        country = request.form["country"].capitalize()
        text_positive = request.form["positive"].capitalize()
        rating = int(request.form["rating"])

        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                # Ensure the filename is safe to use
                filename = secure_filename(file.filename)
                # resized_img = resize_image(file)
                file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))

                # create an instance of the class database
                review = Review(name=title, country=country, pos_text=text_positive, rating=rating, img_name=filename)
                try:
                    # write to database
                    with db.session.begin():
                        db.session.add(review)

                    return redirect('/')
                except:
                    return render_template('post.html', rating=RATING, error_db="Oops(: Something Wrong!")
    else:
        return render_template('post.html', rating=RATING)


@application.route('/login', methods=['GET', 'POST'])
def login():
    '''Login function'''
    return "Login"


if __name__ == '__main__':
    application.run(port=5002, debug=False)
