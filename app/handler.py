from ddtrace import tracer

@tracer.wrap("lambda_handler")
def lambda_handler(event, context):
    """Simple Lambda handler for authentication placeholder.

    Wrapped with Datadog Lambda wrapper so traces and logs can be forwarded to Datadog.
    """
    return {
        "statusCode": 200,
        "body": {
            "message": "Hello from fiap-auth-lambda (Python 3.12)!",
            "event": event,
        },
    }
