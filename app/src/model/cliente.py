from sqlalchemy import Column, String, Boolean, Integer

from src.utils.conexao_db import Base


class ClienteModel(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    cpf = Column(String, unique=True, nullable=False)
    nome = Column(String, nullable=False)
    email = Column(String)
    ativo = Column(Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'cpf': self.cpf,
            'nome': self.nome,
            'email': self.email,
            'ativo': self.ativo,
        }
