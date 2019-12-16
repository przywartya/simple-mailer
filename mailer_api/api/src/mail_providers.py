import logging
import requests
import time

from sendgrid import SendGridAPIClient, helpers

from .const import (
    MAILGUN_KEY,
    MAILGUN_URL,
    SENDGRID_KEY,
    PROVIDER_RETRIES_BACKOFF_FACTOR,
    PROVIDER_RETRIES_BACKOFF_MAX,
)
from .datatypes import Mail


class BaseEmailProvider:
    def __init__(self):
        self.number_of_retries = 0

    def check_and_wait(self):
        if self.number_of_retries and self.number_of_retries > 0:
            time_to_sleep = PROVIDER_RETRIES_BACKOFF_FACTOR * (
                2 ** (self.number_of_retries - 1)
            )
            if time_to_sleep > PROVIDER_RETRIES_BACKOFF_MAX:
                self.reset_retries()
            else:
                logging.warning("sleeping for %s", time_to_sleep)
                time.sleep(time_to_sleep)

    def connection_failed(self):
        self.number_of_retries += 1

    def reset_retries(self):
        self.number_of_retries = 0

    def post_message(self, mail: Mail):
        raise NotImplementedError

    @property
    def api_key(self):
        raise NotImplementedError


class Mailgun(BaseEmailProvider):
    def post_message(self, mail: Mail) -> requests.Response:
        return requests.post(
            url=MAILGUN_URL,
            auth=("api", self.api_key),
            data={
                "from": mail.senderEmail,
                "to": mail.receiverEmail,
                "subject": mail.emailSubject,
                "text": mail.message,
            },
        )

    @property
    def api_key(self):
        return MAILGUN_KEY

    def __str__(self):
        return "Mailgun"


class Sendgrid(BaseEmailProvider):
    def __init__(self):
        super().__init__()
        self.api_client = SendGridAPIClient(api_key=self.api_key)

    def post_message(self, mail: Mail) -> requests.Response:
        return self.api_client.send(message=self._get_message(mail=mail))

    def _get_message(self, mail: Mail):
        return helpers.mail.Mail(
            from_email=mail.senderEmail,
            to_emails=mail.receiverEmail,
            subject=mail.emailSubject,
            plain_text_content=mail.message,
        )

    @property
    def api_key(self):
        return SENDGRID_KEY

    def __str__(self):
        return "Sendgrid"


PROVIDERS = [Sendgrid(), Mailgun()]
