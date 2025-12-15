import json
from contextlib import contextmanager
from typing import Generator, Any

import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

Base = declarative_base()


class GerenciadorDB:
    _engine = None
    _SessionLocal = None

    @staticmethod
    def _carregar_credenciais(secret_name: str, region: str):
        cliente = boto3.client("secretsmanager", region_name=region)
        resposta = cliente.get_secret_value(SecretId=secret_name)
        return json.loads(resposta["SecretString"])

    @classmethod
    def inicializar(cls, secret_name: str, region: str):

        if cls._engine is not None:
            return

        creds = cls._carregar_credenciais(secret_name, region)
        db_url = cls.montar_db_url(creds)

        cls._engine = create_engine(
            db_url,
            pool_size=1,
            max_overflow=0,
            pool_recycle=3600,
            pool_pre_ping=True,
            echo=False
        )

        cls._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._engine)

    @classmethod
    def get_session(cls) -> Session:

        if cls._SessionLocal is None:
            raise RuntimeError("Database não inicializado. Chame inicializar() primeiro.")

        return cls._SessionLocal()

    @classmethod
    @contextmanager
    def session_scope(cls) -> Generator[Session, Any, None]:

        session = cls.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def montar_db_url(creds: dict) -> str:
        return (
            f"postgresql+psycopg2://{creds['username']}:"
            f"{creds['password']}@"
            f"{creds['host']}:"
            f"{creds.get('port', 5432)}/"
            f"{creds['dbname']}"
        )