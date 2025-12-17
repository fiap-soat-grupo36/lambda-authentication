import os

from src.utils.conexao_db import GerenciadorDB


class AppConfig:
    DB_SECRET_NAME = os.environ.get('DB_SECRET_NAME')
    JWT_SECRET_NAME = os.environ.get('JWT_SECRET_NAME')
    AWS_REGION = os.environ.get('AWS_REGION', 'sa-east-1')


def inicializar_aplicacao():
    GerenciadorDB.inicializar(
        secret_name=AppConfig.DB_SECRET_NAME, region=AppConfig.AWS_REGION
    )
