import datetime
import os
import requests as requests
from flask import json
from keys_api import *

# path
CURRENT_PATH = os.path.dirname(__file__)
CURRENT_PATCH_JASON = os.path.join(CURRENT_PATH, "static")

MONTH = 6
current_date = datetime.date.today()

def generate_months()->list:
    """
    Func generate list months from current date
    :return: list months names
    """
    month_list = []


    # generate list months from current date
    for x in range(MONTH):
        next_month = current_date + datetime.timedelta(x *30)
        month_list.append(next_month.strftime('%B'))

    return month_list


def get_dates(month_i:str)-> tuple:
    """
    func to generate departing date and return with Israel preferences
    :return: tuple of strings
    """
    # get moths list
    month_list = generate_months()
    # get index choice month
    month_index = month_list.index(month_i)

    choice = datetime.timedelta(days=30 * month_index)
    future_date = current_date + choice

    # Loop until we find a Thursday day
    while future_date.weekday() != 3:
        future_date += datetime.timedelta(days=1)

    # create departure string
    data_departure = f"{future_date}_{future_date + datetime.timedelta(days=1)}"

    # create return string
    sunday_return = future_date + datetime.timedelta(days=3)
    data_return = f"{sunday_return}_{sunday_return + datetime.timedelta(days=3)}"

    return data_departure, data_return

print(get_dates('August'))

def get_data_travel(number_weeks=3) -> tuple:
    """
    func to generate departing date and return with Israel preferences
    :return: tuple of strings
    """

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
                response_data = requests.get(REQUEST_URL, headers={"UserAgent": "XY", "apikey": API_KEY_CUR}, timeout=5)
                print(response_data)
                collected_rates = json.loads(response_data.text)

                if collected_rates.get("success") == True: return collected_rates

            except requests.exceptions.Timeout:
                print("Connection timed out")
                return False

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


class Carbon:

    # This class is responsible for talking to the Flight Search API.
    def get_iata_code(self, city: str) -> str | None:
        """
        Func request to kivi for get Iata code
        :param city: city str
        :return: str|None
        """

        params = {
            "term": city.lower()
        }
        try:
            response = requests.get(url=KIWI_ENDPOINT, headers=HEADER, params=params, timeout=5)

        except requests.exceptions.Timeout:
            print("Connection timed out")
            return None
        except:
            print("Data collect error")
            return None

        else:
            response.raise_for_status()

            return response.json()['locations'][0]['code']

    def carbon_request(self, departure_city: str, destination_city: str, return_t= False, passenger: int = 1):
        """
        Func request to carbon for calculate co2
        :param departure_city: str
        :param destination_city: str
        :param passenger: int
        :return: dict
        """

        self.departure = self.get_iata_code(departure_city)
        self.destination = self.get_iata_code(destination_city)
        self.passenger = passenger

        headers = {
            "Authorization": f"Bearer {API_KEY_CARBON}",
            "Content-Type": "application/json"
        }
        if return_t:
            data = {
                "type": "flight",
                "passengers": self.passenger,
                "legs": [
                    {"departure_airport": f"{self.departure}", "destination_airport": f"{self.destination}"},
                    {"departure_airport": f"{self.destination}", "destination_airport": f"{self.departure}"}
                ]
            }

        else:
            data = {
                "type": "flight",
                "passengers": self.passenger,
                "legs": [
                    {"departure_airport": f"{self.departure}", "destination_airport": f"{self.destination}"},

                ]
            }
        try:
            response = requests.post(CARBON_URL, headers=headers, data=json.dumps(data), timeout=5)

        except requests.exceptions.Timeout:
            print("Connection timed out")
            return None
        except:
            print("Get carbon Api error")
            return None

        else:
            res = response.json()
            return res


