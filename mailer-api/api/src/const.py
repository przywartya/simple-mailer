import os

DEBUG = os.environ.get('DEBUG', False)

SUCCESS_CODES = [200, 202]

MAILGUN_URL = os.environ.get('MAILGUN_URL', None)
MAILGUN_KEY = os.environ.get('MAILGUN_KEY', None)
SENDGRID_KEY = os.environ.get('SENDGRID_KEY', None)

