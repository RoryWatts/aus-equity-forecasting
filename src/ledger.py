from . import utils


def create_record(description, debit, credit, amount, date):
    """
    Create a record for a transaction.

    Parameters
    ----------
    label : string
        Label for the transaction.
    debit : string
        Debit account.
    credit : string
        Credit account.
    amount : float
        Amount.
    date : datetime.datetime | str
        Date of transaction.

    Returns
    -------
    record : dict
        Transaction record.
    """
    return {
        "description": description,
        "debit": debit,
        "credit": credit,
        "amount": amount,
        "date": utils.validate_datetime(date),
    }


def calculate_equity(ledger):
    assets = 0.0
    liabilities = 0.0

    for transaction in ledger:
        amount = float(transaction['amount'].replace(',', ''))
        if transaction['debit'] == 'assets':
            assets += amount
        elif transaction['debit'] == 'liabilities':
            liabilities -= amount
        if transaction['credit'] == 'assets':
            assets -= amount
        elif transaction['credit'] == 'liabilities':
            liabilities += amount
            
    return assets - liabilities
