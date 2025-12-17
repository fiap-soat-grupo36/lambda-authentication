import json
from unittest.mock import patch, MagicMock

import pytest

from src.service.token_service import GeradorTokenJWT


class TestGeradorTokenJWT:
    @pytest.fixture(autouse=True)
    def limpar_cache(self):
        # Reseta o cache antes de cada teste para garantir isolamento
        GeradorTokenJWT._segredo_cache = None

    @patch('src.service.token_service.boto3')
    def test_carregar_segredo_aws_sucesso(self, mock_boto3):
        # Configura o retorno do Secrets Manager
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client

        fake_secret = json.dumps({'jwt_secret': 'my-super-secret-key'})
        mock_client.get_secret_value.return_value = {
            'SecretString': fake_secret
        }

        # Executa
        token = GeradorTokenJWT.gerar_token(
            cpf='12345678901',
            cliente_id='1',
            nome='Teste',
            ativo=True,
            secret_name='prod/secret',
            region='us-east-1',
        )

        assert isinstance(token, str)
        assert len(token) > 0
        # Garante que chamou o serviço da AWS
        mock_client.get_secret_value.assert_called_once()

    @patch('src.service.token_service.boto3')
    def test_uso_de_cache_segredo(self, mock_boto3):
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        fake_secret = json.dumps({'jwt_secret': 'cached-key'})
        mock_client.get_secret_value.return_value = {
            'SecretString': fake_secret
        }

        GeradorTokenJWT.gerar_token('111', '1', 'A', True, 'sec', 'us')

        GeradorTokenJWT.gerar_token('222', '2', 'B', True, 'sec', 'us')

        assert mock_client.get_secret_value.call_count == 1

    @patch('src.service.token_service.boto3')
    def test_validar_token_sucesso(self, mock_boto3):
        # Setup do segredo
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        secret_key = 'segredo-teste'
        mock_client.get_secret_value.return_value = {
            'SecretString': json.dumps({'jwt_secret': secret_key})
        }

        # Gera um token real usando a mesma chave
        import jwt

        token_valido = jwt.encode(
            {'sub': '123'}, secret_key, algorithm='HS256'
        )

        payload = GeradorTokenJWT.validar_token(token_valido, 'sec', 'us')
        assert payload['sub'] == '123'
