from sqlalchemy import Column, String, Boolean, Integer, DateTime, Date

from src.utils.conexao_db import Base


class ClienteModel(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    ativo = Column(Boolean, default=True)
    cnpj = Column(String, nullable=True)
    cpf = Column(String, unique=True, nullable=True)
    data_cadastro = Column(DateTime, nullable=True)
    data_nascimento = Column(Date, nullable=True)
    email = Column(String, nullable=True)

    # Campos de endereço
    bairro = Column(String, nullable=True)
    cep = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    complemento = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    logradouro = Column(String, nullable=True)
    numero = Column(String, nullable=True)

    nome = Column(String, nullable=False)
    observacao = Column(String, nullable=True)
    telefone = Column(String, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'ativo': self.ativo,
            'cnpj': self.cnpj,
            'cpf': self.cpf,
            'data_cadastro': self.data_cadastro.isoformat()
            if self.data_cadastro
            else None,
            'data_nascimento': self.data_nascimento.isoformat()
            if self.data_nascimento
            else None,
            'email': self.email,
            'bairro': self.bairro,
            'cep': self.cep,
            'cidade': self.cidade,
            'complemento': self.complemento,
            'estado': self.estado,
            'logradouro': self.logradouro,
            'numero': self.numero,
            'nome': self.nome,
            'observacao': self.observacao,
            'telefone': self.telefone,
        }
