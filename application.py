from flask import Flask, render_template
from controls import *


application = Flask(__name__)


departure_date, return_date= get_data_travel()

@application.route('/', methods=['GET', 'POST'])
@application.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('index.html', data_departure=departure_date, data_return=return_date)

@application.route('/about')
def about():
    return render_template('about.html')

@application.route('/contact')
def contact():
    return render_template('/contact.html')

if __name__ == '__main__':
    application.run(port=5002, debug=True)

