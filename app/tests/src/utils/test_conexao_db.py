import pytest
from unittest.mock import patch, MagicMock, call
from app.src.utils.conexao_db import GerenciadorDB

@pytest.fixture(autouse=True)
def reset_gerenciador():
    """Reset GerenciadorDB state before each test."""
    GerenciadorDB._engine = None
    GerenciadorDB._session_factory = None
    GerenciadorDB._database_url = None
    yield
    GerenciadorDB._engine = None
    GerenciadorDB._session_factory = None
    GerenciadorDB._database_url = None


@patch('app.src.utils.conexao_db.boto3.client')
@patch('app.src.utils.conexao_db.create_engine')
def test_inicializar_success(mock_create_engine, mock_boto_client):
    """Test successful database initialization."""
    mock_secrets_client = MagicMock()
    mock_boto_client.return_value = mock_secrets_client
    mock_secrets_client.get_secret_value.return_value = {
        'SecretString': '{"username":"user","password":"pass"}'
    }
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine

    GerenciadorDB.inicializar('secret', 'us-east-1', 'localhost', 5432, 'mydb')

    assert GerenciadorDB._engine is not None
    assert GerenciadorDB._session_factory is not None
    assert 'postgresql://user:pass@localhost:5432/mydb' == GerenciadorDB._database_url


@patch('app.src.utils.conexao_db.boto3.client')
@patch('app.src.utils.conexao_db.create_engine')
def test_inicializar_disposes_existing_engine(mock_create_engine, mock_boto_client):
    """Test that initialization disposes existing engine."""
    mock_secrets_client = MagicMock()
    mock_boto_client.return_value = mock_secrets_client
    mock_secrets_client.get_secret_value.return_value = {
        'SecretString': '{"username":"user","password":"pass"}'
    }
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine

    GerenciadorDB.inicializar('secret', 'us-east-1', 'localhost', 5432, 'mydb')
    first_engine = GerenciadorDB._engine

    GerenciadorDB.inicializar('secret', 'us-east-1', 'localhost', 5432, 'mydb')

    first_engine.dispose.assert_called_once()


def test_session_scope_not_initialized():
    """Test session_scope raises error when not initialized."""
    with pytest.raises(RuntimeError, match='Database não inicializado'):
        with GerenciadorDB.session_scope():
            pass


@patch('app.src.utils.conexao_db.boto3.client')
@patch('app.src.utils.conexao_db.create_engine')
def test_session_scope_commit(mock_create_engine, mock_boto_client):
    """Test session_scope commits on success."""
    mock_secrets_client = MagicMock()
    mock_boto_client.return_value = mock_secrets_client
    mock_secrets_client.get_secret_value.return_value = {
        'SecretString': '{"username":"user","password":"pass"}'
    }
    mock_engine = MagicMock()
    mock_session = MagicMock()
    mock_session_factory = MagicMock(return_value=mock_session)
    mock_create_engine.return_value = mock_engine

    GerenciadorDB.inicializar('secret', 'us-east-1', 'localhost', 5432, 'mydb')
    GerenciadorDB._session_factory = mock_session_factory

    with GerenciadorDB.session_scope() as session:
        assert session is mock_session

    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()


@patch('app.src.utils.conexao_db.boto3.client')
@patch('app.src.utils.conexao_db.create_engine')
def test_session_scope_rollback_on_error(mock_create_engine, mock_boto_client):
    """Test session_scope rollbacks on exception."""
    mock_secrets_client = MagicMock()
    mock_boto_client.return_value = mock_secrets_client
    mock_secrets_client.get_secret_value.return_value = {
        'SecretString': '{"username":"user","password":"pass"}'
    }
    mock_engine = MagicMock()
    mock_session = MagicMock()
    mock_session_factory = MagicMock(return_value=mock_session)
    mock_create_engine.return_value = mock_engine

    GerenciadorDB.inicializar('secret', 'us-east-1', 'localhost', 5432, 'mydb')
    GerenciadorDB._session_factory = mock_session_factory

    with pytest.raises(ValueError):
        with GerenciadorDB.session_scope():
            raise ValueError('Test error')

    mock_session.rollback.assert_called_once()
    mock_session.close.assert_called_once()


def test_dispose_engine_success():
    """Test dispose_engine disposes and resets engine."""
    mock_engine = MagicMock()
    GerenciadorDB._engine = mock_engine
    GerenciadorDB._session_factory = MagicMock()
    GerenciadorDB._database_url = 'test_url'

    GerenciadorDB.dispose_engine()

    mock_engine.dispose.assert_called_once()
    assert GerenciadorDB._engine is None
    assert GerenciadorDB._session_factory is None
    assert GerenciadorDB._database_url is None


def test_dispose_engine_when_none():
    """Test dispose_engine when engine is None."""
    GerenciadorDB._engine = None
    GerenciadorDB.dispose_engine()
    assert GerenciadorDB._engine is None