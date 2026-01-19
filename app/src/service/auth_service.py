from typing import Dict

from src.exception.validacoes_exception import ClienteInativoError
from src.repository.cliente_repository import ClientRepository
from src.service.token_service import GeradorTokenJWT
from src.service.validador_cpf_service import ValidadorCPFService
from src.utils.config import logger


class AuthService:
    @staticmethod
    def autenticar_cliente(
        cpf: str,
        expira_em_minutos: int = 30,
    ) -> Dict[str, str]:
        logger.debug('Validando CPF')
        cpf_limpo = ValidadorCPFService.validar_cpf(cpf)

        logger.debug('Buscando cliente no banco de dados')
        cliente = ClientRepository.buscar_por_cpf(cpf_limpo)

        if not cliente['ativo']:
            logger.warning(
                f'Cliente inativo', extra={'cliente_id': str(cliente['id'])}
            )
            raise ClienteInativoError('Cliente está inativo.')

        logger.debug(
            'Gerando token JWT', extra={'cliente_id': str(cliente['id'])}
        )
        token = GeradorTokenJWT.gerar_token(
            cpf=cliente['cpf'],
            cliente_id=str(cliente['id']),
            nome=cliente['nome'],
            ativo=cliente['ativo'],
            expira_em_minutos=expira_em_minutos,
        )

        logger.info(
            'Token gerado com sucesso', extra={'cliente_id': str(cliente['id'])}
        )
        return {'access_token': token, 'token_type': 'Bearer'}
