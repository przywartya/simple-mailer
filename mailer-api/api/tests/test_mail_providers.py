from unittest import mock

from sendgrid import helpers

from api.src.const import MAILGUN_KEY, MAILGUN_URL
from api.src.datatypes import Mail
from api.src.mail_providers import Mailgun, Sendgrid


@mock.patch("api.src.mail_providers.requests.post")
def test_mailgun_post_message(requests_post_mock):
    Mailgun().post_message(
        mail=Mail(
            receiverEmail="a@a.com",
            senderEmail="b@b.com",
            emailSubject="hello!",
            message=None,
        )
    )
    requests_post_mock.assert_called_with(
        auth=("api", MAILGUN_KEY),
        data={
            "from": "b@b.com",
            "to": "a@a.com",
            "subject": "hello!",
            "text": None,
        },
        url=MAILGUN_URL,
    )


@mock.patch("api.src.mail_providers.Sendgrid._get_message")
@mock.patch("api.src.mail_providers.SendGridAPIClient.send")
def test_sendgrid_post_message(sendgrid_post_mock, _get_message_mock):
    sendgrid_mail_helper = helpers.mail.Mail(
        from_email="b@b.com",
        to_emails="a@a.com",
        subject="hello!",
        plain_text_content=None,
    )

    _get_message_mock.return_value = sendgrid_mail_helper

    Sendgrid().post_message(
        mail=Mail(
            receiverEmail="a@a.com",
            senderEmail="b@b.com",
            emailSubject="hello!",
            message=None,
        )
    )
    _get_message_mock.assert_called_with(
        mail=Mail(
            receiverEmail="a@a.com",
            senderEmail="b@b.com",
            emailSubject="hello!",
            message=None,
        )
    )
    sendgrid_post_mock.assert_called_with(message=sendgrid_mail_helper)
