import json
from unittest.mock import patch, MagicMock

import pytest

import handler
from src.exception.validacoes_exception import (
    CPFInvalidoError,
    ClienteNaoEncontradoError,
    ClienteInativoError,
)


class TestLambdaHandler:
    @pytest.fixture
    def evento_base(self):
        return {'body': json.dumps({'cpf': '12345678900'})}

    @pytest.fixture
    def mock_config(self):
        """Mock para AppConfig com configurações fake"""
        mock = MagicMock()
        mock.db_secret_name = 'test-secret'
        mock.aws_region = 'us-east-1'
        mock.db_host = 'localhost'
        mock.db_port = '5432'
        mock.db_name = 'testdb'
        return mock

    @patch('handler.GerenciadorDB')
    @patch('handler.AppConfig')
    @patch('handler.AuthService')
    def test_handler_sucesso(self, mock_auth_service, mock_app_config, mock_db, evento_base, mock_config):
        mock_app_config.return_value = mock_config
    @patch('handler.GerenciadorDB')
    @patch('handler.AppConfig')
    @patch('handler.AuthService')
    def test_handler_sucesso(self, mock_auth_service, mock_app_config, mock_db, evento_base, mock_config):
        mock_app_config.return_value = mock_config
        retorno_esperado = {
            'access_token': 'token.jwt.fake',
            'token_type': 'Bearer',
        }
        mock_auth_service.autenticar_cliente.return_value = retorno_esperado

        resposta = handler.lambda_handler(evento_base, None)

        assert resposta['statusCode'] == 200
        body = json.loads(resposta['body'])
        assert body == retorno_esperado

        mock_auth_service.autenticar_cliente.assert_called_once()
        mock_db.inicializar.assert_called_once()
        mock_db.dispose_engine.assert_called_once()

    @patch('handler.GerenciadorDB')
    @patch('handler.AppConfig')
    def test_handler_erro_cpf_obrigatorio(self, mock_app_config, mock_db, mock_config):
    @patch('handler.GerenciadorDB')
    @patch('handler.AppConfig')
    def test_handler_erro_cpf_obrigatorio(self, mock_app_config, mock_db, mock_config):
        mock_app_config.return_value = mock_config
        evento = {'body': json.dumps({'outra_coisa': 'valor'})}

        resposta = handler.lambda_handler(evento, None)

        assert resposta['statusCode'] == 400

        body_dict = json.loads(resposta['body'])

        assert 'CPF é obrigatório' in body_dict['erro']
        mock_db.dispose_engine.assert_called_once()

    @patch('handler.GerenciadorDB')
    @patch('handler.AppConfig')
    @patch('handler.AuthService')
    def test_handler_erro_cpf_invalido(self, mock_auth_service, mock_app_config, mock_db, evento_base, mock_config):
        mock_app_config.return_value = mock_config
    @patch('handler.GerenciadorDB')
    @patch('handler.AppConfig')
    @patch('handler.AuthService')
    def test_handler_erro_cpf_invalido(self, mock_auth_service, mock_app_config, mock_db, evento_base, mock_config):
        mock_app_config.return_value = mock_config
        mock_auth_service.autenticar_cliente.side_effect = CPFInvalidoError(
            'CPF inválido.'
        )

        resposta = handler.lambda_handler(evento_base, None)

        assert resposta['statusCode'] == 400

        body = json.loads(resposta['body'])
        assert 'CPF inválido' in body['erro']
        mock_db.dispose_engine.assert_called_once()

    @patch('handler.GerenciadorDB')
    @patch('handler.AppConfig')
    @patch('handler.AuthService')
    def test_handler_erro_cliente_nao_encontrado(
        self, mock_auth_service, mock_app_config, mock_db, evento_base, mock_config
    ):
    @patch('handler.GerenciadorDB')
    @patch('handler.AppConfig')
    @patch('handler.AuthService')
    def test_handler_erro_cliente_nao_encontrado(
        self, mock_auth_service, mock_app_config, mock_db, evento_base, mock_config
    ):
        mock_app_config.return_value = mock_config
        mock_auth_service.autenticar_cliente.side_effect = (
            ClienteNaoEncontradoError('Não achei.')
        )

        resposta = handler.lambda_handler(evento_base, None)

        assert resposta['statusCode'] == 404

        body_dict = json.loads(resposta['body'])

        assert 'Não achei' in body_dict['erro']
        mock_db.dispose_engine.assert_called_once()

    @patch('handler.GerenciadorDB')
    @patch('handler.AppConfig')
    @patch('handler.AuthService')
    def test_handler_erro_cliente_inativo(
        self, mock_auth_service, mock_app_config, mock_db, evento_base, mock_config
    ):
    @patch('handler.GerenciadorDB')
    @patch('handler.AppConfig')
    @patch('handler.AuthService')
    def test_handler_erro_cliente_inativo(
        self, mock_auth_service, mock_app_config, mock_db, evento_base, mock_config
    ):
        mock_app_config.return_value = mock_config
        mock_auth_service.autenticar_cliente.side_effect = ClienteInativoError(
            'Inativo.'
        )

        resposta = handler.lambda_handler(evento_base, None)

        assert resposta['statusCode'] == 403
        assert 'Inativo' in resposta['body']
        mock_db.dispose_engine.assert_called_once()

    @patch('handler.GerenciadorDB')
    @patch('handler.AppConfig')
    @patch('handler.AuthService')
    def test_handler_erro_interno(self, mock_auth_service, mock_app_config, mock_db, evento_base, mock_config):
        mock_app_config.return_value = mock_config
        mock_auth_service.autenticar_cliente.side_effect = Exception(
            'Erro de conexão DB'
        )

        resposta = handler.lambda_handler(evento_base, None)

        assert resposta['statusCode'] == 500
        assert 'Erro interno no servidor' in resposta['body']
        mock_db.dispose_engine.assert_called_once()
