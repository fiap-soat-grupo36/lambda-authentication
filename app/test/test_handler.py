import pytest
from app.handler import lambda_handler

EXPECTED_MSG = "Hello from fiap-auth-lambda (Python 3.12)!"


def test_lambda_handler_basic_structure():
    result = lambda_handler({}, None)
    assert isinstance(result, dict)
    assert result.get("statusCode") == 200
    assert "body" in result and isinstance(result["body"], dict)


def test_lambda_handler_message_and_event_echo():
    event = {"user": "alice", "roles": ["admin"]}
    result = lambda_handler(event, object())
    body = result["body"]
    assert body["message"] == EXPECTED_MSG
    assert body["event"] == event


def test_lambda_handler_handles_various_event_types():
    test_events = [
        [],
        123,
        "a string event",
        None,
        {"nested": {"a": [1, 2, 3]}},
    ]
    for evt in test_events:
        res = lambda_handler(evt, None)
        assert res["statusCode"] == 200
        assert res["body"]["event"] == evt