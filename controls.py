import datetime
import os
import requests as requests
from flask import json
from keys_api import *

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


CURRENCY_NAMES = (
    'AED - United Arab Emirates Dirham',
    'AFN - Afghan Afghani',
    'ALL - Albanian Lek',
    'AMD - Armenian Dram',
    'ANG - Netherlands Antillean Guilder',
    'AOA - Angolan Kwanza',
    'ARS - Argentine Peso',
    'AUD - Australian Dollar',
    'AWG - Aruban Florin',
    'AZN - Azerbaijani Manat',
    'BAM - Bosnia-Herzegovina Convertible Mark',
    'BBD - Barbadian Dollar',
    'BDT - Bangladeshi Taka',
    'BGN - Bulgarian Lev',
    'BHD - Bahraini Dinar',
    'BIF - Burundian Franc',
    'BMD - Bermudan Dollar',
    'BND - Brunei Dollar',
    'BOB - Bolivian Boliviano',
    'BRL - Brazilian Real',
    'BSD - Bahamian Dollar',
    'BTC - Bitcoin',
    'BTN - Bhutanese Ngultrum',
    'BWP - Botswanan Pula',
    'BYN - Belarusian Ruble',
    'BZD - Belize Dollar',
    'CAD - Canadian Dollar',
    'CDF - Congolese Franc',
    'CHF - Swiss Franc',
    'CLF - Chilean Unit of Account (UF)',
    'CLP - Chilean Peso',
    'CNY - Chinese Yuan',
    'COP - Colombian Peso',
    'CRC - Costa Rican Colón',
    'CUC - Cuban Convertible Peso',
    'CUP - Cuban Peso',
    'CVE - Cape Verdean Escudo',
    'CZK - Czech Koruna',
    'DJF - Djiboutian Franc',
    'DKK - Danish Krone',
    'DOP - Dominican Peso',
    'DZD - Algerian Dinar',
    'EGP - Egyptian Pound',
    'ERN - Eritrean Nakfa',
    'ETB - Ethiopian Birr',
    'EUR - Euro',
    'FJD - Fijian Dollar',
    'FKP - Falkland Islands Pound',
    'GBP - British Pound',
    'GEL - Georgian Lari',
    'GGP - Guernsey Pound',
    'GHS - Ghanaian Cedi',
    'GIP - Gibraltar Pound',
    'GMD - Gambian Dalasi',
    'GNF - Guinean Franc',
    'GTQ - Guatemalan Quetzal',
    'GYD - Guyanaese Dollar',
    'HKD - Hong Kong Dollar',
    'HNL - Honduran Lempira',
    'HRK - Croatian Kuna',
    'HTG - Haitian Gourde',
    'HUF - Hungarian Forint',
    'IDR - Indonesian Rupiah',
    'ILS - Israeli New Shekel',
    'IMP - Isle of Man Pound',
    'INR - Indian Rupee',
    'IQD - Iraqi Dinar',
    'IRR - Iranian Rial',
    'ISK - Icelandic Króna',
    'JEP - Jersey Pound',
    'JMD - Jamaican Dollar',
    'JOD - Jordanian Dinar',
    'JPY - Japanese Yen',
    'KES - Kenyan Shilling',
    'KGS - Kyrgystani Som',
    'KHR - Cambodian Riel',
    'KMF - Comorian Franc',
    'KPW - North Korean Won'
    'KRW - South Korean Won',
    'KWD - Kuwaiti Dinar',
    'KYD - Cayman Islands Dollar',
    'KZT - Kazakhstani Tenge',
    'LAK - Lao Kip',
    'LBP - Lebanese Pound',
    'LKR - Sri Lankan Rupee',
    'LRD - Liberian Dollar',
    'LSL - Lesotho Loti',
    'LTL - Lithuanian Litas',
    'LVL - Latvian Lats',
    'LYD - Libyan Dinar',
    'MAD - Moroccan Dirham',
    'MDL - Moldovan Leu',
    'MGA - Malagasy Ariary',
    'MKD - Macedonian Denar',
    'MMK - Burmese Kyat',
    'MNT - Mongolian Tugrik',
    'MOP - Macanese Pataca',
    'MRO - Mauritanian Ouguiya',
    'MUR - Mauritian Rupee',
    'MVR - Maldivian Rufiyaa',
    'MWK - Malawian Kwacha',
    'MXN - Mexican Peso',
    'MYR - Malaysian Ringgit',
    'MZN - Mozambican Metical',
    'NAD - Namibian Dollar',
    'NGN - Nigerian Naira',
    'NIO - Nicaraguan Córdoba',
    'NOK - Norwegian Krone',
    'NPR - Nepalese Rupee',
    'NZD - New Zealand Dollar',
    'OMR - Omani Rial',
    'PAB - Panamanian Balboa',
    'PEN - Peruvian Sol',
    'PGK - Papua New Guinean Kina',
    'PHP - Philippine Peso',
    'PKR - Pakistani Rupee',
    'PLN - Polish Złoty',
    'PYG - Paraguayan Guarani',
    'QAR - Qatari Riyal',
    'RON - Romanian Leu',
    'RSD - Serbian Dinar',
    'RUB - Russian Ruble',
    'RWF - Rwandan Franc',
    'SAR - Saudi Riyal',
    'SBD - Solomon Islands Dollar',
    'SCR - Seychellois Rupee',
    'SDG - Sudanese Pound',
    'SEK - Swedish Krona',
    'SGD - Singapore Dollar',
    'SHP - Saint Helena Pound',
    'SLE - Sierra Leonean Leone',
    'SLL - Sierra Leonean Leone',
    'SOS - Somali Shilling',
    'SRD - Surinamese Dollar',
    'STD - São Tomé and Príncipe Dobra',
    'SVC - Salvadoran Colón',
    'SYP - Syrian Pound',
    'SZL - Eswatini Lilangeni',
    'THB - Thai Baht',
    'TJS - Tajikistani Somoni',
    'TMT - Turkmenistan Manat',
    'TND - Tunisian Dinar',
    'TOP - Tongan Paʻanga',
    'TRY - Turkish Lira',
    'TTD - Trinidad and Tobago Dollar',
    'TWD - New Taiwan Dollar',
    'TZS - Tanzanian Shilling',
    'UAH - Ukrainian Hryvnia',
    'UGX - Ugandan Shilling',
    'USD - United States Dollar',
    'UYU - Uruguayan Peso',
    'UZS - Uzbekistani Som',
    'VEF - Venezuelan Bolívar',
    'VES - Venezuelan Bolívar Soberano',
    'VND - Vietnamese Đồng',
    'VUV - Vanuatu Vatu',
    'WST - Samoan Tala',
    'XAF - Central African CFA Franc',
    'XAG - Silver Ounce',
    'XAU - Gold Ounce',
    'XCD - East Caribbean Dollar',
    'XDR - Special Drawing Rights',
    'XOF - West African CFA Franc',
    'XPF - CFP Franc',
    'YER - Yemeni Rial',
    'ZAR - South African Rand',
    'ZMK - Zambian Kwacha',
    'ZMW - Zambian Kwacha',
    'ZWL - Zimbabwean Dollar',
)


class Carbon:

    # This class is responsible for talking to the Flight Search API.
    def _get_iata_code(self, city: str)->str|None:
        """
        Func request to kivi for get Iata code
        :param city: city str
        :return: str|None
        """

        params = {
            "term": city.lower()
        }
        try:
            response = requests.get(url=KIWI_ENDPOINT, headers=HEADER, params=params)
        except:
            print("Data collect error")
            return None

        else:
            response.raise_for_status()

            return response.json()['locations'][0]['code']

    def carbon_request(self, departure_city:str, destination_city:str, passenger:int):
        """
        Func request to carbon for calculate co2
        :param departure_city: str
        :param destination_city: str
        :param passenger: int
        :return: dict
        """

        self.departure = self._get_iata_code(departure_city)
        self.destination = self._get_iata_code(destination_city)
        self.passenger = passenger

        headers = {
            "Authorization": f"Bearer {API_KEY_CARBON}",
            "Content-Type": "application/json"
        }

        data = {
            "type": "flight",
            "passengers": self.passenger,
            "legs": [
                {"departure_airport": f"{self.departure}", "destination_airport": f"{self.destination}"},
                {"departure_airport": f"{self.departure}", "destination_airport": f"{self.destination}"}
            ]
        }
        try:
            response = requests.post(CARBON_URL, headers=headers, data=json.dumps(data))
        except:
            print("Get carbon Api error")
            return None

        else:
            return response.content


