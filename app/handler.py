def lambda_handler(event, context):
    """Simple Lambda handler for authentication placeholder.

    Returns a JSON with a message and echoes the event for quick testing.
    """
    return {
        "statusCode": 200,
        "body": {
            "message": "Hello from fiap-auth-lambda (Python 3.12)!",
            "event": event,
        },
    }
