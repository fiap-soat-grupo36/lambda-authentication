import json

from datadog import datadog_lambda_wrapper

from src.exception.validacoes_exception import (
    CPFInvalidoError,
    ClienteNaoEncontradoError,
    ClienteInativoError,
)
from src.service.auth_service import AuthService
from src.utils.conexao_db import GerenciadorDB
from src.utils.config import AppConfig, logger


@datadog_lambda_wrapper
def lambda_handler(event, context):
    try:
        # Inicializa a conexão com o banco de dados
        config = AppConfig()
        GerenciadorDB.inicializar(
            secret_name=config.db_secret_name,
            region=config.aws_region,
            db_host=config.db_host,
            db_port=config.db_port,
            db_name=config.db_name,
        )

        logger.info('Lambda invocada', extra={'event': event})

        body = json.loads(event.get('body', '{}'))
        cpf = body.get('cpf')

        if not cpf:
            logger.warning('CPF não fornecido na requisição')
            return _resposta(400, {'erro': 'CPF é obrigatório.'})

        logger.info(
            'Iniciando autenticação', extra={'cpf_masked': cpf[:3] + '***'}
        )

        resultado = AuthService.autenticar_cliente(cpf=cpf)

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
    finally:
        # Garante que todas as conexões sejam fechadas
        try:
            GerenciadorDB.dispose_engine()
            logger.debug('Conexões com banco de dados fechadas com sucesso')
        except Exception as e:
            logger.error(
                'Erro ao fechar conexões com banco', extra={'error': str(e)}
            )


def _resposta(status, body):
    return {
        'statusCode': status,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body),
    }
