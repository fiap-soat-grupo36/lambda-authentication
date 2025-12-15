import json
from unittest.mock import patch

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

    @patch('handler.AuthService')
    def test_handler_sucesso(self, mock_auth_service, evento_base):
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

    def test_handler_erro_cpf_obrigatorio(self):
        evento = {'body': json.dumps({'outra_coisa': 'valor'})}

        resposta = handler.lambda_handler(evento, None)

        assert resposta['statusCode'] == 400

        body_dict = json.loads(resposta['body'])

        assert 'CPF é obrigatório' in body_dict['erro']

    @patch('handler.AuthService')
    def test_handler_erro_cpf_invalido(self, mock_auth_service, evento_base):
        mock_auth_service.autenticar_cliente.side_effect = CPFInvalidoError(
            'CPF inválido.'
        )

        resposta = handler.lambda_handler(evento_base, None)

        assert resposta['statusCode'] == 400

        body = json.loads(resposta['body'])
        assert 'CPF inválido' in body['erro']

    @patch('handler.AuthService')
    def test_handler_erro_cliente_nao_encontrado(
        self, mock_auth_service, evento_base
    ):
        mock_auth_service.autenticar_cliente.side_effect = (
            ClienteNaoEncontradoError('Não achei.')
        )

        resposta = handler.lambda_handler(evento_base, None)

        assert resposta['statusCode'] == 404

        body_dict = json.loads(resposta['body'])

        assert 'Não achei' in body_dict['erro']

    @patch('handler.AuthService')
    def test_handler_erro_cliente_inativo(
        self, mock_auth_service, evento_base
    ):
        mock_auth_service.autenticar_cliente.side_effect = ClienteInativoError(
            'Inativo.'
        )

        resposta = handler.lambda_handler(evento_base, None)

        assert resposta['statusCode'] == 403
        assert 'Inativo' in resposta['body']

    @patch('handler.AuthService')
    def test_handler_erro_interno(self, mock_auth_service, evento_base):
        mock_auth_service.autenticar_cliente.side_effect = Exception(
            'Erro de conexão DB'
        )

        resposta = handler.lambda_handler(evento_base, None)

        assert resposta['statusCode'] == 500
        assert 'Erro interno no servidor' in resposta['body']
