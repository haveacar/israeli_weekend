import datetime

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
    one_day = datetime.timedelta(days=1)
    data_departure = f"{future_date}_{future_date + one_day}"

    # create return string
    sunday_return = future_date + datetime.timedelta(days=3)
    two_days = datetime.timedelta(days=2)
    data_return = f"{sunday_return}_{sunday_return + two_days}"

    return data_departure, data_return