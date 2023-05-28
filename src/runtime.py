import datetime
from src.utils import validate_datetime
from . import streams, utils


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

    ledger = streams.ledger_handler(
        configuration,
        start_date,
        end_date
        )

    ledger = utils.clean_handler(ledger)

    return ledger


if __name__ == "__main__":
    start_date = "2021-01-01"
    end_date = "2023-12-31"
    config = {
        "runtime": {
            "start_date": start_date,
            "end_date": end_date,
        },
    }
    simulate(config)
