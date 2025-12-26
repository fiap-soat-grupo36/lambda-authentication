import json
from unittest.mock import patch, MagicMock

import pytest

from src.service.token_service import GeradorTokenJWT


class TestGeradorTokenJWT:
    
    @patch.dict('os.environ', {'JWT_SECRET_KEY': 'test-secret-key'})
    def test_gerar_token_sucesso(self):
        # Executa
        token = GeradorTokenJWT.gerar_token(
            cpf='12345678901',
            cliente_id='1',
            nome='Teste',
            ativo=True,
        )

        assert isinstance(token, str)
        assert len(token) > 0

    @patch.dict('os.environ', {'JWT_SECRET_KEY': 'test-secret-key'})
    def test_gerar_e_validar_token(self):
        # Gera um token
        token = GeradorTokenJWT.gerar_token(
            cpf='12345678901',
            cliente_id='1',
            nome='Teste',
            ativo=True,
        )

        # Valida o token
        payload = GeradorTokenJWT.validar_token(token)
        
        assert payload['cpf'] == '12345678901'
        assert payload['cliente_id'] == '1'
        assert payload['nome'] == 'Teste'
        assert payload['ativo'] is True
        assert 'iat' in payload
        assert 'exp' in payload

    def test_erro_sem_secret_key(self):
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(RuntimeError, match="JWT_SECRET_KEY"):
                GeradorTokenJWT.gerar_token(
                    cpf='12345678901',
                    cliente_id='1',
                    nome='Teste',
                    ativo=True,
                )
