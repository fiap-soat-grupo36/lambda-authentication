import os

from src.utils.conexao_db import GerenciadorDB
from src.utils.log import DatadogLogConfig


class AppConfig:
    DB_SECRET_NAME = os.environ.get('DB_SECRET_NAME')
    JWT_SECRET_NAME = os.environ.get('JWT_SECRET_NAME')
    AWS_REGION = os.environ.get('AWS_REGION', 'sa-east-1')
    SERVICE_NAME = os.environ.get('DD_SERVICE', 'fiap-auth-lambda')
    ENVIRONMENT = os.environ.get('DD_ENV', 'dev')


_log_config = DatadogLogConfig(
    service_name=AppConfig.SERVICE_NAME, environment=AppConfig.ENVIRONMENT
)
logger = _log_config.get_logger()


def inicializar_aplicacao():
    GerenciadorDB.inicializar(
        secret_name=AppConfig.DB_SECRET_NAME, region=AppConfig.AWS_REGION
    )
