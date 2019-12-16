import os

USE_REDIS = os.environ.get("USE_REDIS", False)
DEBUG = os.environ.get("DEBUG", False)

SUCCESS_CODES = [200, 202]

MAILGUN_URL = os.environ.get("MAILGUN_URL", "")
MAILGUN_KEY = os.environ.get("MAILGUN_KEY", "")

SENDGRID_KEY = os.environ.get("SENDGRID_KEY", "")


PROVIDER_RETRIES_BACKOFF_FACTOR = 0.3
PROVIDER_RETRIES_BACKOFF_MAX = 60  # one minute
