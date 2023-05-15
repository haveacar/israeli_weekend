from flask import Flask, render_template, request
from controls import *
from constants import *


application = Flask(__name__)

# get departure_date return_date
departure_date, return_date= get_data_travel()

# currency convector
conversion_rates = Currency()

date_obj = datetime.datetime.strptime(departure_date.split('_')[0], '%Y-%m-%d')

# extract the month name
month_name = date_obj.strftime('%B')

# get current data rates
data = conversion_rates.currency_convector().get("date")

# list comprehension of keys rates
currencies = [key for key in conversion_rates.currency_convector().get("rates")]

# emission calculate
fly_green = Carbon()





@application.route('/', methods=['GET', 'POST'])
@application.route('/home', methods=['GET', 'POST'])
def home():
    """index page"""
    return render_template('index.html', data_departure=departure_date, data_return=return_date, cheap_month=month_name )

@application.route('/search')
def search():
    """air tickets search page"""
    return render_template('search.html')

@application.route('/currency', methods=['GET', 'POST'])
def currency():
    """currency convector page"""
    if request.method == 'POST':

        amount = float(request.form['amount'])
        from_currency = request.form['from_currency'][:3]
        to_currency = request.form['to_currency'][:3]
        # get conversion rate
        conversion_rate = conversion_rates.currency_convector().get("rates")[to_currency] / \
                          conversion_rates.currency_convector().get("rates")[from_currency]

        converted_amount = round(amount * conversion_rate, 2) # round
        # return template rates
        return render_template('currency.html', data=data, amount=amount, from_currency=from_currency + " =",
                               converted_amount=converted_amount, to_currency=to_currency, currencies=CURRENCY_NAMES)
    else:
        return render_template('currency.html', data=data, currencies=CURRENCY_NAMES)

@application.route('/booking')
def booking():
    """booking.com search"""
    return render_template('booking.html')

@application.route('/carbon', methods=['GET', 'POST'])
def carbon():
    """emission calculate"""
    if request.method == 'POST':
        print(fly_green.carbon_request('Frankfurt', 'Tel Aviv', 1))
    else:
        return render_template('carbon.html')

if __name__ == '__main__':
    application.run(port=5002, debug=True)

