from flask import Flask, render_template, request
from controls import *


application = Flask(__name__)


departure_date, return_date= get_data_travel()

conversion_rates = Currency()

# get current data rates
data = conversion_rates.currency_convector().get("date")
# list comprehension of keys rates
currencies = [key for key in conversion_rates.currency_convector().get("rates")]

@application.route('/', methods=['GET', 'POST'])
@application.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('index.html', data_departure=departure_date, data_return=return_date)

@application.route('/search')
def search():
    return render_template('search.html')

@application.route('/currency', methods=['GET', 'POST'])
def currency():
    if request.method == 'POST':

        amount = float(request.form['amount'])
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']
        # get conversion rate
        conversion_rate = conversion_rates.currency_convector().get("rates")[to_currency] / \
                          conversion_rates.currency_convector().get("rates")[from_currency]
        converted_amount = round(amount * conversion_rate, 2)
        # return template rates
        return render_template('currency.html', data=data, amount=amount, from_currency=from_currency + " =",
                               converted_amount=converted_amount, to_currency=to_currency, currencies=currencies)
    else:
        return render_template('currency.html', data=data, currencies=currencies)


if __name__ == '__main__':
    application.run(port=5002, debug=True)

