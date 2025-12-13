from typing import Dict

from exception.validacoes_exception import ClienteInativoError
from src.repository.cliente_repository import ClientRepository
from src.service.token_service import GeradorTokenJWT
from src.service.validador_cpf_service import ValidadorCPFService


class AuthService:
    @staticmethod
    def autenticar_cliente(
            cpf: str,
            secret_name_jwt: str,
            region: str,
            expira_em_minutos: int = 30
    ) -> Dict[str, str]:
        cpf_limpo = ValidadorCPFService.validar_cpf(cpf)

        cliente = ClientRepository.buscar_por_cpf(cpf_limpo)

        if not cliente.ativo:
            raise ClienteInativoError("Cliente está inativo.")

        token = GeradorTokenJWT.gerar_token(
            cpf=cliente.cpf,
            cliente_id=str(cliente.id),
            nome=cliente.nome,
            ativo=cliente.ativo,
            secret_name=secret_name_jwt,
            region=region,
            expira_em_minutos=expira_em_minutos
        )

        return {
            "access_token": token,
            "token_type": "Bearer"
        }
