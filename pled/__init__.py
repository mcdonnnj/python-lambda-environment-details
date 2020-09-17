"""This package contains the python-lambda-environment-details code."""

from ._version import __version__  # noqa: F401
from .get_installed_packages import get_pip_packages

__all__ = ["get_pip_packages"]
