from unittest.mock import patch, MagicMock

import pytest

from src.exception.validacoes_exception import ClienteNaoEncontradoError
from src.model.cliente import ClienteModel
from src.repository.cliente_repository import ClientRepository


class TestClientRepository:

    @patch("src.repository.cliente_repository.GerenciadorDB")
    def test_buscar_por_cpf_sucesso(self, mock_db):
        mock_session = MagicMock()
        mock_db.session_scope.return_value.__enter__.return_value = mock_session

        cliente_esperado = ClienteModel(id=1, cpf="12345678900", nome="João", ativo=True)

        (mock_session.query.return_value
         .filter.return_value
         .first.return_value) = cliente_esperado

        resultado = ClientRepository.buscar_por_cpf("12345678900")

        assert resultado == cliente_esperado
        assert resultado.nome == "João"

    @patch("src.repository.cliente_repository.GerenciadorDB")
    def test_buscar_por_cpf_nao_encontrado(self, mock_db):
        mock_session = MagicMock()
        mock_db.session_scope.return_value.__enter__.return_value = mock_session

        (mock_session.query.return_value
         .filter.return_value
         .first.return_value) = None

        with pytest.raises(ClienteNaoEncontradoError):
            ClientRepository.buscar_por_cpf("99999999999")
