from . import utils, ledger
from dateutil.relativedelta import relativedelta

def calculate_total_repayments(n, m):
    """
    Calculate the total repayments for a mortgage.

    Parameters
    ----------
    n : int
        Number of years.
    m : int
        Number of payments per year.

    Returns
    -------
    total : float
        Total repayments.
    """
    return n * m 


def calculate_beta(r, m):
    """
    Calculate the interest rate per period (beta).

    Parameters
    ----------
    r : float
        Annual interest rate.
    m : int
        Number of payments per year.

    Returns
    -------
    beta : float
        Interest rate per period.
    """
    return r / m


def calculate_repayments(p, beta, n):
    """
    Calculate the amortization repayment schedule for a repayment.

    Parameters
    ----------
    p : float
        Principal amount.
    beta : float
        Interest rate per period.
    n : int
        Total Number of payments.
        
    Returns
    -------
    schedule : list of tuple
        Amortization schedule.
    """
    a = (  # amortization calculation
        p
        * (
            (beta * (1 + beta) ** n)
            / ((1 + beta)**n - 1)
        )   
    )

    return a


def calculate_remaining_principal_at_t(p, a, beta, t):
    """
    Calculate remaining principal at time t.

    Parameters
    ----------
    p : float
        Principal amount.
    a : float
        Amortization schedule.
    beta : float
        Interest rate per period.
    t : int
        Time period.

    Returns
    -------
    a : float
        Repayment at time t.
    """
    return p * (1 + beta)**t - a * ((1 + beta)**t - 1) / beta


def calculate_stamp_duty(price, fhog=False, new=False):
    """
    Determine stamp duty in WA.

    Rules
    -----
    Stamp Duty Rates WA & other fees
    Purchase Price/Value	Stamp Duty Rate
    $0 – $80,000	$1.90 per $100 or part thereof
    $80,001 – $100,000	$1,520 + $2.85 per $100 or part thereof above $80,000
    $100,001 – $250,000	$2,090 + $3.80 per $100 or part thereof above $100,000
    $250,001 – $500,000	$7,790 + $4.75 per $100 or part thereof above $250,000
    $500,001 and upwards	$19,665 + $5.15 per $100 or part thereof above $500,000
    Other related fees
    Mortgage Registration Fee: $174.70
    Land Transfer Fee: $174.70 for land up to $85,000; $184.70 for land between $85,001 and $120,000; $204.70 for land between $120,001 and $200,000 and then $20 for every $100,000 or part thereof.   ...

    Parameters
    ----------
    price : float
        Purchase price of the property.
    fhog : bool, optional
        Whether the first home owner grant applies. The default is False.
    new : bool, optional
        Whether the property is new. The default is False.

    Returns
    -------
    duty : float
    """
    duty = 0
    if price <= 80_000:
        duty += price * 0.019
    elif price <= 100_000:
        duty += 1_520 + (price - 80_000) * 0.0285
    elif price <= 250_000:
        duty += 2_090 + (price - 100_000) * 0.038
    elif price <= 500_000:
        duty += 7_790 + (price - 250_000) * 0.0475
    else:
        duty += 19_665 + (price - 500_000) * 0.0515

    # mortgage registration fee
    duty += 174.70

    # land transfer fee
    if price <= 85_000:
        duty += 174.70
    elif price <= 120_000:
        duty += 184.70
    elif price <= 200_000:
        duty += 204.70
    else:
        duty += 20 + (price - 200_000) / 100_000 * 100

    return duty

def property_handler(config, start_date, end_date):
    records = []
    records.append(
        create_stamp_duty_record(
            purchase_price=config["purchase_price"], 
            purchase_date=utils.validate_datetime(config["purchase_date"])
            )
        )
    records.append(
        create_deposit_record(
            config["deposit"], 
            config["purchase_date"]
            )
        )
    records += create_mortgage_repayment_records(
        debt=config["purchase_price"] - config["deposit"],
        repayment_period=config["repayment_period"],
        interest_rate=config["interest_rate"],
        mortgage_term=config["mortgage_term"],
        purchase_date=utils.validate_datetime(config["purchase_date"])
    )

    return records

def create_stamp_duty_record(purchase_price, purchase_date):
    stamp_duty = calculate_stamp_duty(purchase_price)
    record = ledger.create_record(
            description=f"Stamp Duty",
            debit="expenses",
            credit="assets",
            amount=stamp_duty,
            date=purchase_date
        )
    return record

def create_deposit_record(deposit, purchase_date):
    record = ledger.create_record(
        description=f"Deposit for Property",
        debit="expenses",
        credit="assets",
        amount=deposit,
        date=purchase_date
    )
    return record

def create_mortgage_repayment_records(
        debt,
        repayment_period,
        interest_rate,
        mortgage_term,
        purchase_date
    ):
    repayment_int = utils.time_strings_to_int(repayment_period)
    repayments = calculate_repayments(
        debt, 
        calculate_beta(interest_rate, repayment_int),
        calculate_total_repayments(repayment_int, mortgage_term)
        )
    last_payment = relativedelta(years=mortgage_term) + purchase_date
    payment_schedule = utils.calculate_dates(purchase_date, repayment_period, last_payment)
    records = []
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