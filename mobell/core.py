import datetime
import pytz
import holidays
import logging
from . import utils

# Get logger (it will inherit config from setup_logging in cli.py)
logger = logging.getLogger(__name__)


def run_market_check():
    ny_tz = pytz.timezone("America/New_York")
    ny_now = datetime.datetime.now(ny_tz)

    logger.info(
        f"Checking status. NYSE Time: {ny_now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )

    # Weekend Check
    if ny_now.weekday() >= 5:
        logger.info("Status: Weekend. Market closed.")
        return

    # Holiday Check
    nyse_holidays = holidays.NYSE(years=ny_now.year)
    today_date = ny_now.date()

    if today_date in nyse_holidays:
        holiday_name = nyse_holidays.get(today_date)
        logger.info(f"Status: Holiday ({holiday_name}). Market closed.")
        return

    # Opening Time Check
    # Matches 09:30 AM ET
    if ny_now.hour == 9 and ny_now.minute == 30:
        logger.info("MARKET OPEN! Triggering bell.")
        utils.play_bell()
    else:
        logger.info("Status: Market not opening right now.")