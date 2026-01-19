from unittest.mock import patch, MagicMock
import pytest
from src.utils.conexao_db import GerenciadorDB

def test_inicializa_engine_e_sessao_quando_nao_inicializado():
    GerenciadorDB._engine = None
    GerenciadorDB._session_factory = None
    with patch('src.utils.conexao_db.create_engine') as mock_create_engine:
        mock_create_engine.return_value = MagicMock()
        engine = GerenciadorDB._get_engine()
        assert engine is not None
        assert GerenciadorDB._engine is not None
        assert GerenciadorDB._session_factory is not None

def test_retorna_engine_existente_quando_ja_inicializado():
    with patch('src.utils.conexao_db.create_engine') as mock_create_engine:
        GerenciadorDB._engine = MagicMock()
        GerenciadorDB._session_factory = MagicMock()
        engine = GerenciadorDB._get_engine()
        mock_create_engine.assert_not_called()
        assert engine == GerenciadorDB._engine

def test_session_scope_gera_sessao_e_fecha_ao_finalizar():
    with patch('src.utils.conexao_db.create_engine') as mock_create_engine:
        mock_engine = MagicMock()
        mock_session = MagicMock()
        mock_create_engine.return_value = mock_engine
        GerenciadorDB._engine = mock_engine
        GerenciadorDB._session_factory = MagicMock(return_value=mock_session)
        with GerenciadorDB.session_scope() as session:
            assert session == mock_session
            session.commit.assert_not_called()
        session.commit.assert_called_once()
        session.close.assert_called_once()

def test_session_scope_rollback_em_caso_de_erro():
    with patch('src.utils.conexao_db.create_engine') as mock_create_engine:
        mock_engine = MagicMock()
        mock_session = MagicMock()
        mock_create_engine.return_value = mock_engine
        GerenciadorDB._engine = mock_engine
        GerenciadorDB._session_factory = MagicMock(return_value=mock_session)
        with pytest.raises(Exception):
            with GerenciadorDB.session_scope() as session:
                assert session == mock_session
                raise Exception("Erro simulado")
        session.rollback.assert_called_once()
        session.close.assert_called_once()

def test_dispose_engine_descarta_engine_e_sessao():
    mock_engine = MagicMock()
    GerenciadorDB._engine = mock_engine
    GerenciadorDB._session_factory = MagicMock()
    GerenciadorDB.dispose_engine()
    mock_engine.dispose.assert_called_once()
    assert GerenciadorDB._engine is None
    assert GerenciadorDB._session_factory is None
