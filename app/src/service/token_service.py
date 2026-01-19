import os
from datetime import datetime, timedelta
from typing import Dict, Any

import jwt

from src.utils.config import logger


class GeradorTokenJWT:
    @staticmethod
    def _obter_segredo() -> str:
        """Obtém o secret do JWT da variável de ambiente."""
        segredo = os.environ.get('JWT_SECRET_KEY')

        if not segredo:
            logger.error('JWT_SECRET_KEY não configurada')
            raise RuntimeError(
                "Variável de ambiente 'JWT_SECRET_KEY' não configurada."
            )

        return segredo

    @staticmethod
    def gerar_token(
        cpf: str,
        cliente_id: str,
        nome: str,
        ativo: bool,
        expira_em_minutos: int = 30,
    ) -> str:
        """Gera um token JWT com as informações do cliente."""

        logger.debug('Obtendo secret para geração do token')
        segredo = GeradorTokenJWT._obter_segredo()

        agora = datetime.utcnow()
        expira = agora + timedelta(minutes=expira_em_minutos)

        payload = {
            'sub': cpf,
            'roles': ['CLIENTE'],
            'cpf': cpf,
            'cliente_id': cliente_id,
            'nome': nome,
            'ativo': ativo,
            'iat': int(agora.timestamp()),
            'exp': int(expira.timestamp()),
        }

        logger.debug('Codificando token JWT')
        token = jwt.encode(payload, segredo, algorithm='HS256')

        if isinstance(token, bytes):
            token = token.decode('utf-8')

        logger.debug('Token JWT gerado com sucesso')
        return token

    @staticmethod
    def validar_token(token: str, algoritmo: str = 'HS256') -> Dict[str, Any]:
        """Valida e decodifica um token JWT."""

        logger.debug('Validando token JWT')
        segredo = GeradorTokenJWT._obter_segredo()

        try:
            payload = jwt.decode(
                token,
                segredo,
                algorithms=[algoritmo],
                options={'verify_iat': False},
            )
            logger.debug('Token validado com sucesso')
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning('Token expirado')
            raise
        except jwt.InvalidTokenError as e:
            logger.warning('Token inválido', extra={'error': str(e)})
            raise
