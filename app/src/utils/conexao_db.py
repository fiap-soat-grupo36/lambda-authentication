import json
import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from contextlib import contextmanager

# Base para os modelos SQLAlchemy
Base = declarative_base()


class GerenciadorDB:
    _engine = None
    _session_factory = None
    _database_url = None

    @classmethod
    def inicializar(cls, secret_name, region, db_host, db_port, db_name):
        """Configura a URL do banco e cria o engine com NullPool."""
        if cls._engine is not None:
            cls.dispose_engine()

        client = boto3.client('secretsmanager', region_name=region)
        secret = client.get_secret_value(SecretId=secret_name)
        credentials = json.loads(secret['SecretString'])

        cls._database_url = (
            f"postgresql://{credentials['username']}:{credentials['password']}"
            f"@{db_host}:{db_port}/{db_name}"
        )

        cls._engine = create_engine(
            cls._database_url,
            poolclass=NullPool,  # Não mantém conexões abertas
            echo=False,
            connect_args={
                'connect_timeout': 10,
                'options': '-c statement_timeout=30000'
            }
        )
        cls._session_factory = sessionmaker(bind=cls._engine)

    @classmethod
    @contextmanager
    def session_scope(cls):
        """Gerencia sessão com commit/rollback automático."""
        if cls._session_factory is None:
            raise RuntimeError('Database não inicializado.')

        session = cls._session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            # Fecha a sessão e, com NullPool, fecha a conexão TCP também
            session.close()

    @classmethod
    def dispose_engine(cls):
        """Libera recursos do engine e fecha todas as conexões."""
        if cls._engine is not None:
            try:
                cls._engine.dispose()
            finally:
                cls._engine = None
                cls._session_factory = None
                cls._database_url = None
