import logging
import itertools

from .const import SUCCESS_CODES
from .datatypes import Mail
from .mail_providers import PROVIDERS


def try_sending_to_email_service(mail: Mail):
    logging.info("(to: %s) attempting to send", mail.receiverEmail)
    for provider in itertools.cycle(PROVIDERS):
        response = None

        try:
            response = provider.post_message(mail=mail)
            if response:
                if response.status_code in SUCCESS_CODES:
                    logging.info(
                        "(to: %s) sent from %s",
                        mail.receiverEmail,
                        str(provider),
                    )
                    return
                else:
                    logging.warning(
                        "(to: %s) sending from %s failed (response: %s)",
                        mail.receiverEmail,
                        str(provider),
                        response.text,
                    )

            raise ValueError("empty response")
        except Exception:
            logging.error(
                "(to: %s) sending from %s failed",
                mail.receiverEmail,
                str(provider),
                exc_info=True,
            )
