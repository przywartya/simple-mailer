import os

USE_REDIS = os.environ.get("USE_REDIS", False)
DEBUG = os.environ.get("DEBUG", False)

SUCCESS_CODES = [200, 202]

MAILGUN_URL = os.environ.get("MAILGUN_URL", "")
MAILGUN_KEY = os.environ.get("MAILGUN_KEY", "")

SENDGRID_KEY = os.environ.get("SENDGRID_KEY", "")
