from flask import Flask, render_template, request
from controls import *
from constants import *

application = Flask(__name__)

# get departure_date return_date
departure_date, return_date = get_data_travel()

months = generate_months()



# currency convector
conversion_rates = Currency()
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
    if request.method == 'POST':
        # get from form
        selected = request.form['from1']

        # get dates
        departure_d, return_d = get_dates(selected)

        return render_template('index.html', data_departure=f'{departure_d}', data_return=f'{return_d}',
                               cheap_month=selected, months=months)
    else:
        # current date timedelta 2 weeks
        search_date = current_date + datetime.timedelta(weeks=2)
        month_name = search_date.strftime('%B')
        # get dates
        departure_date, return_date = get_dates(month_name)

        return render_template('index.html', data_departure=departure_date, data_return=return_date,
                               cheap_month=month_name, months=months)


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

        converted_amount = round(amount * conversion_rate, 2)  # round
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


if __name__ == '__main__':
    application.run(port=5002, debug=True)
