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