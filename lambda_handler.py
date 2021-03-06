"""This module contains the lamdba_handler code."""

# Standard Python Libraries
import logging
import os

# cisagov Libraries
from pled import get_installed_packages as gip

# This Lambda function expects the following environment variables to be
# defined:
# 1. messaget - The message for the lambda to print
# 2. log_level - If provided it should be one of the following: "debug", "info",
#                "warning", "error", and "critical"

# In the case of AWS Lambda, the root logger is used BEFORE our Lambda handler
# runs, and this creates a default handler that goes to the console.  Once
# logging has been configured, calling logging.basicConfig() has no effect.  We
# can get around this by removing any root handlers (if present) before calling
# logging.basicConfig().  This unconfigures logging and allows --debug to
# affect the logging level that appears in the CloudWatch logs.
#
# See
# https://stackoverflow.com/questions/1943747/python-logging-before-you-run-logging-basicconfig
# and
# https://stackoverflow.com/questions/37703609/using-python-logging-with-aws-lambda
# for more details.
logging_root = logging.getLogger()
if logging_root.handlers:
    for logging_handler in logging_root.handlers:
        logging_root.removeHandler(logging_handler)


def handler(event, context):
    """Handle all Lambda events."""
    gip.setup_logging(os.environ.get("log_level", "info"))

    logging.debug(f"AWS Event was: {event}")

    if not os.environ.get("s3_key", None):
        result = gip.get_information(s3_bucket=os.environ.get("s3_bucket", None))
    else:
        result = gip.get_information(
            s3_bucket=os.environ.get("s3_bucket", None), s3_key=os.environ["s3_key"]
        )

    return result
