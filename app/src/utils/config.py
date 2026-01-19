import os

from src.utils.conexao_db import GerenciadorDB
from src.utils.log import DatadogLogConfig


class AppConfig:
    DB_SECRET_NAME = os.environ.get('DB_SECRET_NAME')
    DB_HOST = os.environ.get('DB_HOST')  # Endpoint do RDS
    DB_PORT = os.environ.get('DB_PORT', '5432')  # Porta do RDS
    DB_NAME = os.environ.get('DB_NAME')  # Nome do database
    JWT_SECRET_KEY = os.environ.get(
        'JWT_SECRET_KEY'
    )  # Secret do JWT direto da variável de ambiente
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-2')
    ENVIRONMENT = os.environ.get('DD_ENV', 'dev')
    SERVICE_NAME = os.environ.get(
        'DD_SERVICE', f'fiap-auth-lambda-{ENVIRONMENT}'
    )


_log_config = DatadogLogConfig(
    service_name=AppConfig.SERVICE_NAME, environment=AppConfig.ENVIRONMENT
)
logger = _log_config.get_logger()


def inicializar_aplicacao():
    GerenciadorDB.inicializar(
        secret_name=AppConfig.DB_SECRET_NAME,
        region=AppConfig.AWS_REGION,
        db_host=AppConfig.DB_HOST,
        db_port=AppConfig.DB_PORT,
        db_name=AppConfig.DB_NAME,
    )
