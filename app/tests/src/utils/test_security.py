from unittest.mock import patch

import pytest
from jwt import ExpiredSignatureError, InvalidTokenError

from src.utils.security import obter_usuario_atual


class TestSecurity:

    @patch("src.utils.security.GeradorTokenJWT")
    @patch.dict('os.environ', {"JWT_SECRET_NAME": "my-secret", "AWS_REGION": "us-east-1"})
    def test_obter_usuario_atual_sucesso(self, mock_jwt_service):
        payload_esperado = {"sub": "123", "nome": "Teste"}
        mock_jwt_service.validar_token.return_value = payload_esperado

        token = "token_valido"
        resultado = obter_usuario_atual(token)

        assert resultado == payload_esperado

        mock_jwt_service.validar_token.assert_called_with(
            token=token,
            secret_name="my-secret",
            region="us-east-1"
        )

    @patch("src.utils.security.GeradorTokenJWT")
    @patch.dict('os.environ', {"JWT_SECRET_NAME": "s", "AWS_REGION": "r"})
    def test_erro_token_expirado(self, mock_jwt_service):
        mock_jwt_service.validar_token.side_effect = ExpiredSignatureError()

        with pytest.raises(Exception) as exc_info:
            obter_usuario_atual("token_expirado")

        assert str(exc_info.value) == "Token expirado."

    @patch("src.utils.security.GeradorTokenJWT")
    @patch.dict('os.environ', {"JWT_SECRET_NAME": "s", "AWS_REGION": "r"})
    def test_erro_token_invalido(self, mock_jwt_service):
        mock_jwt_service.validar_token.side_effect = InvalidTokenError()

        with pytest.raises(Exception) as exc_info:
            obter_usuario_atual("token_ruim")

        assert str(exc_info.value) == "Token inválido."
