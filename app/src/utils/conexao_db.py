import json
from contextlib import contextmanager
from typing import Generator, Any
import logging

import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

Base = declarative_base()

# Usar logging básico aqui para evitar import circular
logger = logging.getLogger(__name__)


class GerenciadorDB:
    _engine = None
    _SessionLocal = None

    @staticmethod
    def _carregar_credenciais(secret_name: str, region: str):
        logger.debug(
            'Carregando credenciais do Secrets Manager',
            extra={'secret_name': secret_name},
        )
        cliente = boto3.client('secretsmanager', region_name=region)
        resposta = cliente.get_secret_value(SecretId=secret_name)
        logger.debug('Credenciais carregadas com sucesso')
        return json.loads(resposta['SecretString'])

    @classmethod
    def inicializar(cls, secret_name: str, region: str):

        if cls._engine is not None:
            logger.debug(
                'Database já inicializado, reutilizando engine existente'
            )
            return

        logger.info('Inicializando conexão com o banco de dados')
        creds = cls._carregar_credenciais(secret_name, region)
        db_url = cls.montar_db_url(creds)

        logger.debug('Criando engine do SQLAlchemy')
        cls._engine = create_engine(
            db_url,
            pool_size=1,
            max_overflow=0,
            pool_recycle=3600,
            pool_pre_ping=True,
            echo=False,
        )

        cls._SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=cls._engine
        )
        logger.info('Conexão com banco de dados inicializada com sucesso')

    @classmethod
    def get_session(cls) -> Session:

        if cls._SessionLocal is None:
            logger.error(
                'Tentativa de obter sessão sem inicializar o database'
            )
            raise RuntimeError(
                'Database não inicializado. Chame inicializar() primeiro.'
            )

        logger.debug('Criando nova sessão do banco de dados')
        return cls._SessionLocal()

    @classmethod
    @contextmanager
    def session_scope(cls) -> Generator[Session, Any, None]:

        session = cls.get_session()
        try:
            yield session
            session.commit()
            logger.debug('Transação commitada com sucesso')
        except Exception as e:
            session.rollback()
            logger.error(
                'Erro na transação, fazendo rollback',
                exc_info=True,
                extra={'error': str(e)},
            )
            raise
        finally:
            session.close()
            logger.debug('Sessão do banco de dados fechada')

    def montar_db_url(creds: dict) -> str:
        return (
            f"postgresql+psycopg2://{creds['username']}:"
            f"{creds['password']}@"
            f"{creds['host']}:"
            f"{creds.get('port', 5432)}/"
            f"{creds['dbname']}"
        )
