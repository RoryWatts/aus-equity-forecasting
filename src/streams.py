"""
Convert dictionary data about transactions, assets etc. 
into a stream of transactions at specified periods.
"""
from . import real_estate, utils, ledger
from dateutil.relativedelta import relativedelta


def ledger_handler(configuration, start_date, end_date):
    """
    Handle the streams from the configuration file.

    Parameters
    ----------
    configuration : dict
        Configuration dictionary.
    start_date : datetime.date
        Start date of the simulation.
    end_date : datetime.date
        End date of the simulation.

    Returns
    -------
    ledger : list
        List of transactions.
    """
    ledger = []
    purchases = configuration.get("purchases", {})
    ledger += purchases_handler(purchases, start_date, end_date)
    return ledger


def purchases_handler(purchases, start_date, end_date):
    records = []
    for purchase in purchases:
        purchase_type = purchase["type"]
        if purchase_type == "property":
            records += real_estate.property_handler(purchase, start_date, end_date)
    return records


def assets_handler(assets):
    return {}


def expenses_handler(expenses):
    return {}


def liabilities_handler(liabilities):
    return {}


def revenues_handler(revenues):
    return {}