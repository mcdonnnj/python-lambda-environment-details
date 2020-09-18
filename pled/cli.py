#!/usr/bin/env python3

"""Provide a command line frontend to the functionality of this module."""

# Standard Python Libraries
import argparse
import json
import logging

from ._version import __version__
from .get_installed_packages import get_information, setup_logging


def main():
    """Provide a command line front-end."""
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

    pip_list = get_information()

    if pip_list:
        print(json.dumps(pip_list, sort_keys=True, indent=4))

    # Stop logging and clean up
    logging.shutdown()

    return 0 if pip_list else -1


if __name__ == "__main__":
    main()
