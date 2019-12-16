from unittest import mock

from api.src import mail_sender
from api.src.datatypes import Mail
from api.src.mail_providers import BaseEmailProvider


class MockProvider200(BaseEmailProvider):
    def post_message(self, mail: Mail):
        return mock.Mock(status_code=200)

    def __str__(self):
        return "MockProvider200"


class MockProvider202(BaseEmailProvider):
    def post_message(self, mail: Mail):
        return mock.Mock(status_code=200)

    def __str__(self):
        return "MockProvider202"


class MockProvider400(BaseEmailProvider):
    def post_message(self, mail: Mail):
        return mock.Mock(status_code=400)

    def __str__(self):
        return "MockProvider400"


class MockProvider500(BaseEmailProvider):
    def post_message(self, mail: Mail):
        return mock.Mock(status_code=500)

    def __str__(self):
        return "MockProvider500"


@mock.patch("api.src.mail_providers.BaseEmailProvider.connection_failed")
@mock.patch("api.src.mail_providers.BaseEmailProvider.check_and_wait")
@mock.patch("api.src.mail_sender.logging")
def test_it_iterates_over_providers_and_tries_to_post_message(
    logging_mock, check_and_wait_mock, connection_failed_mock
):
    mail_sender.PROVIDERS = [MockProvider400(), MockProvider200()]
    mail_sender.try_sending_to_email_service(
        mail=Mail(
            receiverEmail="a@a.com",
            senderEmail="b@b.com",
            emailSubject="hello!",
            message="",
        )
    )
    assert check_and_wait_mock.call_count == 2
    assert connection_failed_mock.call_count == 1

    logging_mock.warning.assert_has_calls(
        [
            mock.call(
                "(to: %s) sending from %s failed (response: %s)",
                "a@a.com",
                "MockProvider400",
                mock.ANY,
            ),
            mock.call("(to: %s) sent from %s", "a@a.com", "MockProvider200"),
        ]
    )

    mail_sender.PROVIDERS = [MockProvider500(), MockProvider202()]
    mail_sender.try_sending_to_email_service(
        mail=Mail(
            receiverEmail="a@a.com",
            senderEmail="b@b.com",
            emailSubject="hello!",
            message="",
        )
    )
    assert check_and_wait_mock.call_count == 4
    assert connection_failed_mock.call_count == 2

    logging_mock.warning.assert_has_calls(
        [
            mock.call(
                "(to: %s) sending from %s failed (response: %s)",
                "a@a.com",
                "MockProvider500",
                mock.ANY,
            ),
            mock.call("(to: %s) sent from %s", "a@a.com", "MockProvider202"),
        ]
    )
