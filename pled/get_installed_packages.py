#!/usr/bin/env python3

"""get_installed_packages: Get information about packages installed with pip."""

# Standard Python Libraries
import argparse
import json
import logging
import subprocess  # nosec

from ._version import __version__


def setup_logging(log_level):
    """Set up logging at the provided level."""
    try:
        logging.basicConfig(
            format="%(asctime)-15s %(levelname)s %(message)s", level=log_level.upper()
        )
    except ValueError:
        logging.critical('"%s" is not a valid logging level.', log_level)
        logging.critical(
            "Possible values are debug, info, warning, error, and critical."
        )
        return 1


def get_pip_packages():
    """Get the list of installed pip packages and return a dict of them."""
    command = ["pip", "list", "--format", "json"]
    result = subprocess.run(command, capture_output=True, shell=False)  # nosec

    if result.returncode:
        logging.error("Problem running pip command. Return code: %d", result.returncode)
        logging.error(result.stderr)
        return None

    return json.loads(result.stdout)


def main():
    """Display package information."""
    arg_parser = argparse.ArgumentParser(
        description="Get details about pip installed packages."
    )
    arg_parser.add_argument("--version", action="version", version=__version__)
    arg_parser.add_argument(
        "--log-level",
        choices=["debug", "info", "warning", "error", "critical"],
        default="warning",
        dest="log_level",
        help="Log level to use.",
        metavar="LEVEL",
        nargs="?",
        type=str,
    )

    args = arg_parser.parse_args()

    # Set up logging
    setup_logging(args.log_level)

    pip_list = get_pip_packages()

    if pip_list:
        print(json.dumps(pip_list, sort_keys=True, indent=4))

    # Stop logging and clean up
    logging.shutdown()

    return 0 if pip_list else -1


if __name__ == "__main__":
    main()
