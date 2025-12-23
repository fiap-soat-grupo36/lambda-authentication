import importlib
from unittest.mock import patch

import src.utils.config as config_module


class TestAppConfig:
    @patch.dict(
        'os.environ',
        {
            'DB_SECRET_NAME': 'test/db/secret',
            'JWT_SECRET_NAME': 'test/jwt/secret',
            'AWS_REGION': 'us-east-2',
        },
        clear=True,
    )
    def test_app_config_lendo_variaveis_ambiente(self):
        importlib.reload(config_module)

        # Acessamos a classe através do módulo recarregado
        assert config_module.AppConfig.DB_SECRET_NAME == 'test/db/secret'
        assert config_module.AppConfig.JWT_SECRET_NAME == 'test/jwt/secret'
        assert config_module.AppConfig.AWS_REGION == 'us-east-2'

    @patch.dict('os.environ', {'DB_SECRET_NAME': 'Apenas_DB'}, clear=True)
    def test_app_config_fallback_aws_region(self):
        importlib.reload(config_module)

        assert config_module.AppConfig.DB_SECRET_NAME == 'Apenas_DB'
        assert config_module.AppConfig.AWS_REGION == 'us-east-2'


@patch('src.utils.conexao_db.GerenciadorDB')
def test_inicializar_aplicacao_chama_db_inicializar(mock_gerenciador_db):
    env_vars = {
        'DB_SECRET_NAME': 'db_prod',
        'AWS_REGION': 'us-east-2',
        'AWS_ACCESS_KEY_ID': 'testing',  # Credencial Fake
        'AWS_SECRET_ACCESS_KEY': 'testing',  # Credencial Fake
        'AWS_SECURITY_TOKEN': 'testing',  # Credencial Fake
        'AWS_SESSION_TOKEN': 'testing',  # Credencial Fake
    }

    with patch.dict('os.environ', env_vars, clear=True):
        # Recarrega o módulo para pegar as variáveis de ambiente novas
        importlib.reload(config_module)

        # Executa a função
        config_module.inicializar_aplicacao()

        mock_gerenciador_db.inicializar.assert_called_once()

        # Verifica os parâmetros
        mock_gerenciador_db.inicializar.assert_called_with(
            secret_name='db_prod', region='us-east-2'
        )
