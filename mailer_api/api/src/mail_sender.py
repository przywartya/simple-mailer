import logging
import itertools

from .const import SUCCESS_CODES
from .datatypes import Mail
from .mail_providers import PROVIDERS


def try_sending_to_email_service(mail: Mail):
    logging.warning("(to: %s) attempting to send", mail.receiverEmail)
    for provider in itertools.cycle(PROVIDERS):
        response = None
        provider.check_and_wait()
        try:
            response = provider.post_message(mail=mail)
            if response and response.status_code in SUCCESS_CODES:
                logging.warning(
                    "(to: %s) sent from %s", mail.receiverEmail, str(provider)
                )
                return
        except Exception:
            provider.connection_failed()
            logging.error(
                "(to: %s) sending from %s failed",
                mail.receiverEmail,
                str(provider),
                exc_info=True,
            )
        else:
            provider.connection_failed()
            response_text = ""
            if response:
                response = response.text
            logging.warning(
                "(to: %s) sending from %s failed (response: %s)",
                mail.receiverEmail,
                str(provider),
                response_text,
            )
