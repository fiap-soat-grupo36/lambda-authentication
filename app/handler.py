import json

from src.exception.validacoes_exception import (
    CPFInvalidoError,
    ClienteNaoEncontradoError,
    ClienteInativoError,
)
from src.service.auth_service import AuthService
from src.utils.conexao_db import GerenciadorDB
from src.utils.config import AppConfig, logger
from datadog import datadog_lambda_wrapper

try:
    GerenciadorDB.inicializar(
        secret_name=AppConfig.DB_SECRET_NAME, region=AppConfig.AWS_REGION
    )
    logger.info('Database inicializado com sucesso no Cold Start')
except Exception as e:
    logger.error(
        f'Falha na inicialização do DB no Cold Start',
        exc_info=True,
        extra={'error': str(e)},
    )


@datadog_lambda_wrapper
def lambda_handler(event, context):
    try:
        logger.info('Lambda invocada', extra={'event': event})

        body = json.loads(event.get('body', '{}'))
        cpf = body.get('cpf')

        if not cpf:
            logger.warning('CPF não fornecido na requisição')
            return _resposta(400, {'erro': 'CPF é obrigatório.'})

        logger.info(
            'Iniciando autenticação', extra={'cpf_masked': cpf[:3] + '***'}
        )

        resultado = AuthService.autenticar_cliente(
            cpf=cpf,
            secret_name_jwt=AppConfig.JWT_SECRET_NAME,
            region=AppConfig.AWS_REGION,
        )

        logger.info('Autenticação bem-sucedida')
        return _resposta(200, resultado)

    except CPFInvalidoError as e:
        logger.warning('CPF inválido', extra={'error': str(e)})
        return _resposta(400, {'erro': str(e)})

    except ClienteNaoEncontradoError as e:
        logger.warning('Cliente não encontrado', extra={'error': str(e)})
        return _resposta(404, {'erro': str(e)})

    except ClienteInativoError as e:
        logger.warning('Cliente inativo', extra={'error': str(e)})
        return _resposta(403, {'erro': str(e)})

    except Exception as e:
        logger.error(
            'Erro inesperado na lambda', exc_info=True, extra={'error': str(e)}
        )
        return _resposta(500, {'erro': 'Erro interno no servidor.'})


def _resposta(status, body):
    return {
        'statusCode': status,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body),
    }
