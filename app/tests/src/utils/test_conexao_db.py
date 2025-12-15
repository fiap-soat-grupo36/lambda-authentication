from unittest.mock import patch, MagicMock

import pytest

from src.utils.conexao_db import GerenciadorDB


class TestGerenciadorDB:

    @staticmethod
    def setup_method(self):
        GerenciadorDB._engine = None
        GerenciadorDB._SessionLocal = None

    @patch("src.utils.conexao_db.create_engine")
    @patch("src.utils.conexao_db.boto3")
    def test_inicializar_sucesso(self, mock_boto3, mock_create_engine):
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        mock_client.get_secret_value.return_value = {
            "SecretString": '{"username": "u", "password": "p", "host": "h", "dbname": "d"}'
        }
        GerenciadorDB.inicializar("secret", "region")

        mock_create_engine.assert_called_once()
        assert GerenciadorDB._engine is not None
        assert GerenciadorDB._SessionLocal is not None

    def test_get_session_erro_sem_inicializar(self):
        with pytest.raises(RuntimeError) as exc:
            GerenciadorDB.get_session()
        assert "Database não inicializado" in str(exc.value)
