import datetime
from dateutil.relativedelta import relativedelta

def clean_handler(ledger):
    """
    Clean ledgers.

    Parameters
    ----------
    ledger : list
        List of transactions.

    Returns
    -------
    ledger : list
        List of transactions.
    """
    ledger = clean_datetimes(ledger)
    ledger = clean_floats(ledger)
    return ledger

def clean_datetimes(ledger):
    """
    Convert datetime objects to strings if they are strings.

    Parameters
    ----------
    ledger : list
        List of transactions.

    Returns
    -------
    ledger : list
        List of transactions.
    """
    cleaned_ledger = []
    for record in ledger:
        record["date"] = str(record["date"])
        cleaned_ledger.append(record)
    return cleaned_ledger


def clean_floats(ledger):
    """
    Shorten strings, convert to thousands values.

    Parameters
    ----------
    ledger : list
        List of transactions.
    
    Returns
    -------
    ledger : list
        List of transactions.
    """
    cleaned_ledger = []
    for record in ledger:
        record["amount"] = format(record["amount"], ",.2f")
        cleaned_ledger.append(record)
    return cleaned_ledger


def validate_datetime(time_object):
    """
    Make sure the time object is a datetime object.
    Parameters
    ----------
    time_object : datetime.datetime or datetime.date or string
        Time object.
    Returns
    -------
    time_object : datetime.datetime
        Time object.
    """
    if isinstance(time_object, str):
        time_object = datetime.datetime.strptime(time_object, "%Y-%m-%d")
    return time_object


import datetime


def time_strings_to_int(string):
    """
    Convert time strings to ints, 
    where the int is how many times they occur in a year.
    Parameters
    ----------
    string : string
        String to convert.
    Returns
    -------
    float
        timedelta representation of the string.
    """
    if string == "daily":
        return 365
    elif string == "weekly":
        return 52
    if string == "monthly":
        return 12
    elif string == "quarterly":
        return 4
    elif string == "annually":
        return 1
    else:
        return 1


def time_strings_to_timedelta(string):
    """
    Convert some natural language times to timedeltas.
    Parameters
    ----------
    string : string
        String to convert.
    Returns
    -------
    timedelta
        timedelta representation of the string.
    """
    if string == "daily":
        return datetime.timedelta(days=1)
    elif string == "weekly":
        return datetime.timedelta(weeks=1)
    if string == "monthly":
        # Approximately 1 month, an average value
        return datetime.timedelta(days=30.44)
    elif string == "quarterly":
        # Approximately 3 months, an average value
        return datetime.timedelta(days=91.31)
    elif string == "annually":
        # Approximately 1 year, an average value
        return datetime.timedelta(days=365.25)
    else:
        return datetime.timedelta(days=365.25)


def calculate_dates(first_date, period, end_date):
    """
    Return a list of dates.

    Parameters
    ----------
    first_date : datetime.date
        First date.
    period : string
        Period of time.
    end_date : datetime.date
        End date.
    """
    delta = time_strings_to_timedelta(period)

    dates = []  # Empty list to hold the dates

    current_date = first_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += delta

    return dates


if __name__ == "__main__":
    print(calculate_dates(datetime.date(2020, 1, 1), "monthly", datetime.date(2020, 12, 31)))
