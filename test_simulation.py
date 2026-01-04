import datetime
import pytz
from unittest.mock import patch
from mobell import core, logger

log = logger.setup_logging()

def run_simulation():
    log.info("--- 🔔 Starting Market Open Simulation 🔔 ---")

    # 1. Pick a specific valid trading time
    # Wednesday, Jan 7, 2026 at 9:30 AM ET (Standard Trading Day)
    # We use a future date to ensure it doesn't conflict with past holiday data quirks
    mock_ny_time = datetime.datetime(
        2026, 1, 7, 9, 30, 0, tzinfo=pytz.timezone("America/New_York")
    )

    log.info(f"Injecting Fake Time: {mock_ny_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # 2. Monkeypatch datetime.datetime inside the mobell.core module
    # We replace 'datetime.datetime' with a Mock object, but we tell it
    # that when .now() is called, it should return our mock_ny_time.
    with patch("mobell.core.datetime.datetime") as mock_dt:
        mock_dt.now.return_value = mock_ny_time

        # We also need to pass through other attributes if necessary,
        # but since core.py mainly uses .now(), this usually suffices.
        # Note: The side_effect ensures that if the code creates a datetime
        # (like datetime.datetime(year...)), it calls the real datetime class.
        mock_dt.side_effect = lambda *args, **kwargs: datetime.datetime(*args, **kwargs)

        # 3. Run the actual application logic
        try:
            core.run_market_check()
            log.info("Simulation Complete ✅. Did you hear the bell?")
        except Exception as e:
            log.info(f"Simulation Failed ❌ with error: {e}")


if __name__ == "__main__":
    run_simulation()
