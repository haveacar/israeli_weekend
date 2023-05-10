import datetime
import os

import requests as requests
from flask import json

# api key and request url
API_KEY = "c66xOBOerxjgjCqRfbT3MzvIIqMoDm6e"
REQUEST_URL = "https://api.apilayer.com/fixer/latest?base=USD"

# path
CURRENT_PATH = os.path.dirname(__file__)
CURRENT_PATCH_JASON = os.path.join(CURRENT_PATH, "static")

def get_data_travel(number_weeks=3) -> tuple:
    """
    func to generate departing date and return with Israel preferences
    :return: tuple of strings
    """

    current_date = datetime.date.today()

    # Add two weeks to the current date
    two_weeks = datetime.timedelta(weeks=number_weeks)
    future_date = current_date + two_weeks

    # Loop until we find a Thursday day
    while future_date.weekday() != 3:
        future_date += datetime.timedelta(days=1)

    # create departure string
    data_departure = f"{future_date}_{future_date + datetime.timedelta(days=1)}"

    # create return string
    sunday_return = future_date + datetime.timedelta(days=3)
    data_return = f"{sunday_return}_{sunday_return + datetime.timedelta(days=3)}"

    return data_departure, data_return

class Currency:
    '''Currency convertor'''

    def __init__(self):
        pass

    def currency_convector(self):

        def receive_data():
            """
            Receive_data func check
            :return:  dict(collected_rates) or False
            """
            try:
                # receive data
                response_data = requests.get(REQUEST_URL, headers={"UserAgent": "XY", "apikey": API_KEY})
                collected_rates = json.loads(response_data.text)
                if collected_rates.get("success") == True: return collected_rates

            except:
                return False

        def reload_rates() -> dict:
            """
            Func Reload_data checks date from file
            if date!= date.now try upload
            :return: dict (rates), str(date)
            """
            time_now = datetime.datetime.now().strftime("%Y-%m-%d")
            # open rates from file
            with open(os.path.join(CURRENT_PATCH_JASON, "data_rates.json")) as f:
                rates_from_file = json.load(f)
            rates = rates_from_file

            # check from file current date
            if rates_from_file.get("date") != time_now:
                print("Uploading Data")
                rates = receive_data()

                # cannot receive data
                if rates == False:
                    print("Cannot update")
                    rates = rates_from_file
                else:
                    print("Uploading successful")
                    # create file
                    with open(os.path.join(CURRENT_PATCH_JASON, "data_rates.json"), "w") as f:
                        json.dump(rates, f, indent=4)
                        pass
            return rates

        all_rates = reload_rates()

        return all_rates




