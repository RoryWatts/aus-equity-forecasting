"""
Convert dictionary data about transactions, assets etc. 
into a stream of transactions at specified periods.
"""
from . import mortgage, utils, ledger
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
            records += property_handler(purchase, start_date, end_date)
    return records


def property_handler(property, start_date, end_date):
    records = []

    type = property["type"]
    purchase_price = property["purchase_price"]

    purchase_date = property["purchase_date"]
    purchase_date = utils.validate_datetime(purchase_date)

    stamp_duty = mortgage.calculate_stamp_duty(purchase_price)
    records.append(
        ledger.create_record(
            description=f"Stamp Duty for {type}",
            debit="expenses",
            credit="assets",
            amount=stamp_duty,
            date=purchase_date
        )
    )

    deposit = property["deposit"]
    records.append(
        ledger.create_record(
            description=f"Deposit for Property",
            debit="expenses",
            credit="assets",
            amount=deposit,
            date=purchase_date
        )
    )

    debt = purchase_price - deposit
    deposit = property["deposit"]
    interest_rate = property["interest_rate"]
    mortgage_term = property["mortgage_term"]
    repayment_period = property["repayment_period"]
    repayment_int = utils.time_strings_to_int(repayment_period)
    repayments = mortgage.calculate_repayments(
        debt, 
        mortgage.calculate_beta(interest_rate, repayment_int),
        mortgage.calculate_total_repayments(repayment_int, mortgage_term)
        )
    last_payment = relativedelta(years=mortgage_term) + purchase_date
    payment_schedule = utils.calculate_dates(purchase_date, repayment_period, last_payment)
    for date in payment_schedule:
        records.append(
            ledger.create_record(
                description=f"Repayment for Property",
                debit="expenses",
                credit="assets",
                amount=repayments,
                date=date
            )
        )

    return records


def assets_handler(assets):
    return {}


def expenses_handler(expenses):
    return {}


def liabilities_handler(liabilities):
    return {}


def revenues_handler(revenues):
    return {}