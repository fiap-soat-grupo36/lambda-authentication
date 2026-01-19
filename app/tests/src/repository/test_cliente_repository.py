from unittest.mock import patch, MagicMock

import pytest

from src.exception.validacoes_exception import ClienteNaoEncontradoError
from src.model.cliente import ClienteModel
from src.repository.cliente_repository import ClientRepository


class TestClientRepository:
    @patch('src.repository.cliente_repository.GerenciadorDB')
    def test_buscar_por_cpf_sucesso(self, mock_db):
        mock_session = MagicMock()
        mock_db.session_scope.return_value.__enter__.return_value = (
            mock_session
        )

        # Mock do objeto ClienteModel com método to_dict
        mock_cliente = MagicMock()
        mock_cliente.to_dict.return_value = {
            'id': 1,
            'cpf': '12345678900',
            'nome': 'João',
            'ativo': True,
            'cnpj': None,
            'data_cadastro': None,
            'data_nascimento': None,
            'email': None,
            'bairro': None,
            'cep': None,
            'cidade': None,
            'complemento': None,
            'estado': None,
            'logradouro': None,
            'numero': None,
            'observacao': None,
            'telefone': None,
        }

        (
            mock_session.query.return_value.filter.return_value.first.return_value
        ) = mock_cliente

        resultado = ClientRepository.buscar_por_cpf('12345678900')

        assert resultado['id'] == 1
        assert resultado['cpf'] == '12345678900'
        assert resultado['nome'] == 'João'
        assert resultado['ativo'] is True

    @patch('src.repository.cliente_repository.GerenciadorDB')
    def test_buscar_por_cpf_nao_encontrado(self, mock_db):
        mock_session = MagicMock()
        mock_db.session_scope.return_value.__enter__.return_value = (
            mock_session
        )

        (
            mock_session.query.return_value.filter.return_value.first.return_value
        ) = None

        with pytest.raises(ClienteNaoEncontradoError):
            ClientRepository.buscar_por_cpf('99999999999')
