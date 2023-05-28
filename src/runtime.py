import datetime
from src.utils import validate_datetime
from . import streams, utils, ledger


def simulate(configuration):
    """
    Create a ledger from a configuration file by simulating transactions.

    Parameters
    ----------
    config : dict
        Configuration dictionary.

    Returns
    -------
    ledger : list
        List of transactions.
    """
    start_date = configuration["runtime"].get("start_date", datetime.date.today())
    start_date = validate_datetime(start_date)
    end_date = configuration["runtime"].get("end_date", datetime.date.today() + datetime.timedelta(days=365))
    end_date = validate_datetime(end_date)

    _ledger = streams.ledger_handler(
        configuration,
        start_date,
        end_date
        )

    _ledger = utils.clean_handler(_ledger)
    equity = ledger.calculate_equity(_ledger)

    return equity
