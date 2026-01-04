import argparse
import sys
import os
import textwrap
from mobell import core, logger as log_setup


def setup_cron():
    """
    Generates crontab lines.
    """
    python_exe = sys.executable
    script_path = os.path.abspath(__file__)

    cron_1 = f"30 21 * * 1-5 {python_exe} {script_path} run"
    cron_2 = f"30 22 * * 1-5 {python_exe} {script_path} run"

    print("\n--- Copy these lines into your crontab (run: crontab -e) ---")
    print(f"# Market Opening Bell (Generated for {python_exe})")
    print(cron_1)
    print(cron_2)
    print("----------------------------------------------------------")
    print("Note: This schedules checks for both 21:30 and 22:30 SGT.")
    print("The script logic handles the EST/EDT switch automatically.")


def main():
    # 1. Define the top-level parser with rich formatting
    parser = argparse.ArgumentParser(
        prog="python cli.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
            \033[1mNYSE Market Opening Bell Automator\033[0m
            ----------------------------------
            A python tool to play a bell sound exactly when the New York Stock
            Exchange opens (9:30 AM ET), accounting for:
              - Singapore Time (SGT) conversion
              - Daylight Saving Time (DST) switches
              - US Public Holidays (via 'holidays' library)
              - Weekends
        """),
        epilog=textwrap.dedent("""
            \033[1mConfiguration:\033[0m
              On first run, a 'config.toml' file is created in the app root.
              Use this file to customize the bell sound path and log directory.

            \033[1mExamples:\033[0m
              python cli.py setup-cron   # Get crontab lines to schedule the app
              python cli.py run          # Manual check (plays sound if market is open)
              python cli.py help         # Show this help message
        """),
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 2. Command: run
    run_parser = subparsers.add_parser(
        "run",
        help="Check current time and play bell if market is opening.",
        description="Checks if today is a trading day and if the current time matches 9:30 AM ET. If yes, plays the bell.",
    )

    # 3. Command: setup-cron
    cron_parser = subparsers.add_parser(
        "setup-cron",
        help="Generate the crontab lines required to automate this.",
        description="Outputs the specific crontab lines needed to run this script at 9:30 PM and 10:30 PM SGT.",
    )

    # 4. Command: help (Explicitly adding 'help' as a command)
    help_parser = subparsers.add_parser("help", help="Display this help message.")

    # If no arguments provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Handle the 'help' command manually
    if args.command == "help":
        parser.print_help()
        sys.exit(0)

    # Initialize logging for functional commands
    log_setup.setup_logging()

    if args.command == "run":
        core.run_market_check()
    elif args.command == "setup-cron":
        setup_cron()


if __name__ == "__main__":
    main()
