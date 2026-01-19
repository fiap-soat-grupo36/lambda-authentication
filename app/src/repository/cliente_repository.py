from src.exception.validacoes_exception import ClienteNaoEncontradoError
from src.model.cliente import ClienteModel
from src.utils.conexao_db import GerenciadorDB
from src.utils.config import logger


class ClientRepository:
    @staticmethod
    def buscar_por_cpf(cpf: str) -> ClienteModel:
        logger.debug('Buscando cliente por CPF no banco de dados')

        with GerenciadorDB.session_scope() as session:
            cliente = (
                session.query(ClienteModel)
                .filter(ClienteModel.cpf == cpf)
                .first()
            )

            if not cliente:
                logger.warning('Cliente não encontrado no banco de dados')
                raise ClienteNaoEncontradoError(
                    f'Cliente com CPF {cpf} não encontrado.'
                )

            logger.debug(
                'Cliente encontrado', extra={'cliente_id': str(cliente.id)}
            )
            return cliente.to_dict()
