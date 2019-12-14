import json

from unittest import mock
from starlette.testclient import TestClient
from api.src.main import app

client = TestClient(app)


def test_send_mail_empty_fields():
    response = client.post("/mail", json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['body', 'mail', 'receiverEmail'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }, {
            'loc': ['body', 'mail', 'senderEmail'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }, {
            'loc': ['body', 'mail', 'emailSubject'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }]
    }

def test_send_mail_invalid_emails():
    response = client.post("/mail", json.dumps({
        'receiverEmail': 'aaaa'
    }))
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['body', 'mail', 'receiverEmail'],
            'msg': 'value is not a valid email address',
            'type': 'value_error.email'
        }, {
            'loc': ['body', 'mail', 'senderEmail'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }, {
            'loc': ['body', 'mail', 'emailSubject'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }]
    }

    response = client.post("/mail", json.dumps({
        'senderEmail': 'aaaa'
    }))
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['body', 'mail', 'receiverEmail'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }, {
            'loc': ['body', 'mail', 'senderEmail'],
            'msg': 'value is not a valid email address',
            'type': 'value_error.email'
        }, {
            'loc': ['body', 'mail', 'emailSubject'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }]
    }


def test_send_mail_valid_body():
    response = client.post("/mail", json.dumps({
        'receiverEmail': 'a@a.com',
        'senderEmail': 'b@b.com',
        'emailSubject': 'hello!'
    }))
    assert response.status_code == 200
    assert response.json() == {
        'emailSubject': 'hello!',
        'message': None,
        'receiverEmail': 'a@a.com',
        'senderEmail': 'b@b.com'
    }
