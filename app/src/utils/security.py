import os
from typing import Dict, Any

from jwt import ExpiredSignatureError, InvalidTokenError

from src.service.token_service import GeradorTokenJWT


def obter_usuario_atual(token: str) -> Dict[str, Any]:
    secret_name = os.environ.get('JWT_SECRET_NAME')
    region = os.environ.get('AWS_REGION', 'sa-east-1')

    try:
        payload = GeradorTokenJWT.validar_token(
            token=token, secret_name=secret_name, region=region
        )
        return payload

    except ExpiredSignatureError:
        raise Exception('Token expirado.')

    except InvalidTokenError:
        raise Exception('Token inválido.')
