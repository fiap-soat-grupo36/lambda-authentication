import json
from logging import Logger

from src.exception.validacoes_exception import CPFInvalidoError, ClienteNaoEncontradoError, ClienteInativoError
from src.service.auth_service import AuthService
from src.utils.conexao_db import GerenciadorDB
from src.utils.config import AppConfig

try:
    GerenciadorDB.inicializar(secret_name=AppConfig.DB_SECRET_NAME, region=AppConfig.AWS_REGION)
except Exception as e:
    print(f"Aviso: Falha na inicialização do DB no Cold Start: {e}")


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        cpf = body.get("cpf")

        if not cpf:
            return _resposta(400, {"erro": "CPF é obrigatório."})

        resultado = AuthService.autenticar_cliente(
            cpf=cpf,
            secret_name_jwt=AppConfig.JWT_SECRET_NAME,
            region=AppConfig.AWS_REGION
        )

        return _resposta(200, resultado)

    except CPFInvalidoError as e:
        return _resposta(400, {"erro": str(e)})

    except ClienteNaoEncontradoError as e:
        return _resposta(404, {"erro": str(e)})

    except ClienteInativoError as e:
        return _resposta(403, {"erro": str(e)})

    except Exception as e:
        Logger(f"Erro inesperado: {str(e)}")
        return _resposta(500, {"erro": "Erro interno no servidor."})


def _resposta(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }
