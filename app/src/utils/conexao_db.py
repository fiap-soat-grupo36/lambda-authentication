# src/database/gerenciador_db.py
import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import logging
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

logger = logging.getLogger(__name__)

class GerenciadorDB:
    _engine = None
    _session_factory = None

    @classmethod
    def _get_engine(cls):
        if cls._engine is None:
            database_url = os.getenv('DATABASE_URL')

            # NullPool é recomendado para Lambda - não mantém conexões persistentes
            cls._engine = create_engine(
                database_url,
                poolclass=NullPool,  # Desabilita pool - cada conexão é fechada após uso
                echo=False,
                connect_args={
                    'connect_timeout': 10,
                    'options': '-c statement_timeout=30000'
                }
            )
            cls._session_factory = sessionmaker(bind=cls._engine)
        return cls._engine

    @classmethod
    @contextmanager
    def session_scope(cls):
        """Gerenciador de contexto que garante fechamento da sessão e conexão."""
        cls._get_engine()
        session = cls._session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Erro na sessão do banco: {str(e)}")
            raise
        finally:
            session.close()
            # Força fechamento da conexão subjacente
            if hasattr(session, 'get_bind'):
                try:
                    session.get_bind().dispose()
                except Exception:
                    pass

    @classmethod
    def dispose_engine(cls):
        """Descarta o engine e todas as conexões."""
        if cls._engine is not None:
            cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None
