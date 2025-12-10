import contextlib
from types import SimpleNamespace
from unittest.mock import Mock


from app import handler


def test_lambda_handler_sets_tag_and_sends_metric(monkeypatch):
    span = SimpleNamespace(calls=[])
    def set_tag(key, value):
        span.calls.append((key, value))
    span.set_tag = set_tag
    monkeypatch.setattr(handler.tracer, "current_span", lambda: span)

    @contextlib.contextmanager
    def fake_trace(name):
        yield
    monkeypatch.setattr(handler.tracer, "trace", fake_trace)

    metric_mock = Mock()
    monkeypatch.setattr(handler, "lambda_metric", metric_mock)

    monkeypatch.setattr(handler, "get_message", lambda: "mensagem de teste")

    resp = handler.lambda_handler({}, None)

    assert ('customer.id', '123456') in span.calls

    metric_mock.assert_called_once_with(
        metric_name='coffee_house.order_value',
        value=12.45,
        tags=['product:latte', 'order:online']
    )

    assert resp["statusCode"] == 200
    assert resp["body"] == "mensagem de teste"


def test_get_message_returns_expected_string():
    assert handler.get_message() == "Hello from serverless!"
