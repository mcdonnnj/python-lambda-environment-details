#!/usr/bin/env python3

"""get_installed_packages: Get information about packages installed with pip."""

# Standard Python Libraries
import argparse
import json
import logging
from subprocess import CalledProcessError, check_output  # nosec

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
    command = "pip list --format json"

    try:
        result = check_output(command.split(" "), shell=False)  # nosec
    except CalledProcessError as err:
        logging.error("Problem running command '%s'", err.cmd)
        logging.error("Process returned code '%d'", err.returncode)
        logging.error(err.output)
        return None

    return json.loads(result)


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
