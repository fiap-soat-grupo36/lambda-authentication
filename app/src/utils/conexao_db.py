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
    def inicializar(cls, secret_name: str, region: str, db_host: str = None, db_port: str = None, db_name: str = None):

        if cls._engine is not None:
            logger.debug(
                'Database já inicializado, reutilizando engine existente'
            )
            return

        logger.info('Inicializando conexão com o banco de dados')
        creds = cls._carregar_credenciais(secret_name, region)
        
        # Adiciona informações de host, port e database nas credenciais
        if db_host:
            creds['host'] = db_host
        if db_port:
            creds['port'] = int(db_port)
        if db_name:
            creds['dbname'] = db_name
            
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
        """
        Monta a URL de conexão do banco de dados.
        Suporta diferentes formatos de secrets do RDS/Secrets Manager.
        """
        # Aceita diferentes nomes de chaves
        host = creds.get('host') or creds.get('hostname') or creds.get('endpoint')
        port = creds.get('port', 5432)
        username = creds.get('username') or creds.get('user')
        password = creds.get('password')
        database = creds.get('dbname') or creds.get('database') or creds.get('db')
        
        # Validação
        if not all([host, username, password, database]):
            missing = []
            if not host: missing.append('host/hostname/endpoint')
            if not username: missing.append('username/user')
            if not password: missing.append('password')
            if not database: missing.append('dbname/database/db')
            
            logger.error(
                f'Secret do banco de dados está incompleto. Chaves faltando: {", ".join(missing)}',
                extra={'available_keys': list(creds.keys())}
            )
            raise ValueError(
                f'Secret do banco de dados inválido. Chaves disponíveis: {list(creds.keys())}'
            )
        
        return (
            f"postgresql+psycopg2://{username}:"
            f"{password}@"
            f"{host}:"
            f"{port}/"
            f"{database}"
        )
