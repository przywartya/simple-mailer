from unittest import mock

from sendgrid import helpers

from api.src.const import MAILGUN_KEY, MAILGUN_URL
from api.src.datatypes import Mail
from api.src import mail_providers


@mock.patch("api.src.mail_providers.requests.post")
def test_mailgun_post_message(requests_post_mock):
    mail_providers.Mailgun().post_message(
        mail=Mail(
            receiverEmail="a@a.com",
            senderEmail="b@b.com",
            emailSubject="hello!",
            message="",
        )
    )
    requests_post_mock.assert_called_with(
        auth=("api", MAILGUN_KEY),
        data={
            "from": "b@b.com",
            "to": "a@a.com",
            "subject": "hello!",
            "text": "",
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
        plain_text_content="",
    )

    _get_message_mock.return_value = sendgrid_mail_helper

    mail_providers.Sendgrid().post_message(
        mail=Mail(
            receiverEmail="a@a.com",
            senderEmail="b@b.com",
            emailSubject="hello!",
            message="",
        )
    )
    _get_message_mock.assert_called_with(
        mail=Mail(
            receiverEmail="a@a.com",
            senderEmail="b@b.com",
            emailSubject="hello!",
            message="",
        )
    )
    sendgrid_post_mock.assert_called_with(message=sendgrid_mail_helper)


@mock.patch("api.src.mail_providers.time.sleep")
def test_mail_provider_connection_timer(sleep_mock):
    mail_providers.PROVIDER_RETRIES_BACKOFF_MAX = 3
    mail_providers.PROVIDER_RETRIES_BACKOFF_FACTOR = 0.3

    provider = mail_providers.BaseEmailProvider()

    for _, time_to_sleep in zip(range(5), [None, 0.3, 0.6, 1.2, 2.4]):
        provider.check_and_wait()
        provider.connection_failed()
        time_to_sleep and sleep_mock.assert_called_with(time_to_sleep)


@mock.patch("api.src.mail_providers.time.sleep")
def test_mail_provider_connection_backoff_max(sleep_mock):
    mail_providers.PROVIDER_RETRIES_BACKOFF_MAX = 1
    mail_providers.PROVIDER_RETRIES_BACKOFF_FACTOR = 0.3

    provider = mail_providers.BaseEmailProvider()

    for _, time_to_sleep in zip(range(6), [None, 0.3, 0.6, None, 0.3, 0.6]):
        provider.check_and_wait()
        provider.connection_failed()
        time_to_sleep and sleep_mock.assert_called_with(time_to_sleep)
