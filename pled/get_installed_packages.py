"""get_installed_packages: Get information about packages installed with pip."""

# Standard Python Libraries
import json
import logging
from subprocess import CalledProcessError, check_output  # nosec

# Third-Party Libraries
from boto3 import client as boto3_client
from botocore.exceptions import ClientError


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


def upload_to_s3_bucket(bucket, key, data):
    """Upload the provided data to a given S3 bucket as the given key."""
    s3_client = boto3_client("s3")
    try:
        s3_client.put_object(
            Body=json.dumps(data).encode("utf-8"), Bucket=bucket, Key=key
        )
    except ClientError as put_error:
        logging.error(
            "Unable to put object to S3 bucket '%s' with key '%s'", bucket, key
        )
        logging.error(put_error)


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


def get_information(s3_bucket=None, s3_key="pip_package_list.json"):
    """Provide a main entrypoint to the functionality of this module."""
    pip_list = get_pip_packages()

    if s3_bucket:
        upload_to_s3_bucket(s3_bucket, s3_key, pip_list)

    return pip_list
