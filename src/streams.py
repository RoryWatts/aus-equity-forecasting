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
    ledger += assets_handler(
        configuration.get("assets", []),
        start_date
    )
    ledger += liabilities_handler(
        configuration.get("liabilities", []),
        start_date
    )
    ledger += purchases_handler(
        configuration.get("purchases", []),
        start_date, 
        end_date)
    ledger += expenses_handler(
        configuration.get("expenses", []),
        start_date,
        end_date
    )
    ledger += revenues_handler(
        configuration.get("revenues", []),
        start_date,
        end_date
    )
    return ledger


def purchases_handler(purchases, start_date, end_date):
    records = []
    for purchase in purchases:
        purchase_type = purchase["type"]
        if purchase_type == "property":
            records += real_estate.property_handler(purchase, start_date, end_date)
    return records


def assets_handler(assets, start_date):
    records = []
    for asset in assets:
        records.append(
            ledger.create_record(
                description=asset["description"],
                debit="assets",
                credit="revenues",
                amount=asset["amount"],
                date=start_date
            )
        )
    return records


def liabilities_handler(liabilities, start_date):
    records = []
    for liability in liabilities:
        records.append(
            ledger.create_record(
                description=liability["description"],
                debit="expenses",
                credit="liabilities",
                amount=liability["amount"],
                date=start_date
            )
        )
    return records


def expenses_handler(expenses, start_date, end_date):
    records = []
    for expense in expenses:
        if expense.get("ends", None):
            end_date = utils.validate_datetime(expense["ends"])
        dates = utils.calculate_dates(
            start_date,
            expense["period"],
            end_date
        )
        for date in dates:
            records.append(
                ledger.create_record(
                    description=expense["description"],
                    debit="expenses",
                    credit="assets",
                    amount=expense["amount"],
                    date=date
                    )
                )
    return records


def revenues_handler(revenues, start_date, end_date):
    records = []
    for revenue in revenues:
        if revenue.get("ends", None):
            end_date = utils.validate_datetime(revenue["ends"])
        dates = utils.calculate_dates(
            start_date,
            revenue["period"],
            end_date
        )
        for date in dates:
            records.append(
                ledger.create_record(
                    description=revenue["description"],
                    debit="assets",
                    credit="revenues",
                    amount=revenue["amount"],
                    date=date
                    )
                )
    return records