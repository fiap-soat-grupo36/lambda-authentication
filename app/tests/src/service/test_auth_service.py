from unittest.mock import patch

import pytest

from src.exception.validacoes_exception import ClienteInativoError
from src.model.cliente import ClienteModel
from src.service.auth_service import AuthService


class TestAuthService:
    @patch('src.service.auth_service.GeradorTokenJWT')
    @patch('src.service.auth_service.ClientRepository')
    @patch('src.service.auth_service.ValidadorCPFService')
    def test_autenticar_cliente_fluxo_completo(
        self, mock_validador, mock_repo, mock_jwt
    ):
        # 1. Mock Validador
        cpf_input = '123'
        mock_validador.validar_cpf.return_value = '123_limpo'

        cliente_mock = ClienteModel(
            id=1, cpf='123_limpo', nome='Maria', ativo=True
        )
        mock_repo.buscar_por_cpf.return_value = cliente_mock

        # 3. Mock JWT
        token_fake = 'eyJ.token.fake'
        mock_jwt.gerar_token.return_value = token_fake

        # Execução
        resposta = AuthService.autenticar_cliente(cpf_input)

        # Asserções
        assert resposta['access_token'] == token_fake
        assert resposta['token_type'] == 'Bearer'

        mock_validador.validar_cpf.assert_called_with(cpf_input)
        mock_repo.buscar_por_cpf.assert_called_with('123_limpo')
        mock_jwt.gerar_token.assert_called_once()

    @patch('src.service.auth_service.ClientRepository')
    @patch('src.service.auth_service.ValidadorCPFService')
    def test_erro_cliente_inativo(self, mock_validador, mock_repo):
        mock_validador.validar_cpf.return_value = '123'

        cliente_inativo = ClienteModel(
            id=1, cpf='123', nome='Maria', ativo=False
        )
        mock_repo.buscar_por_cpf.return_value = cliente_inativo

        with pytest.raises(ClienteInativoError) as exc_info:
            AuthService.autenticar_cliente('123')

        assert 'Cliente está inativo' in str(exc_info.value)
