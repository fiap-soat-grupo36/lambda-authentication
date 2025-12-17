from src.exception.validacoes_exception import ClienteNaoEncontradoError
from src.model.cliente import ClienteModel
from src.utils.conexao_db import GerenciadorDB


class ClientRepository:
    @staticmethod
    def buscar_por_cpf(cpf: str) -> ClienteModel:
        with GerenciadorDB.session_scope() as session:
            cliente = (
                session.query(ClienteModel)
                .filter(ClienteModel.cpf == cpf)
                .first()
            )

            if not cliente:
                raise ClienteNaoEncontradoError(
                    f'Cliente com CPF {cpf} não encontrado.'
                )

            return cliente
