"""Modelo de dados do Paciente.

Define a entidade Patient
mapeada via SQLAlchemy para a tabela 'patient'.
"""

from sqlalchemy import Column, Integer, String, Date
from infra.models.base import Base


class Patient(Base):
    __tablename__ = 'patient'
    __table_args__ = {
        "sqlite_autoincrement": True
    }

    patient_id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=False)
    tax_id = Column(String(14), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    cep = Column(String(9), nullable=False)
    logradouro = Column(String(200), nullable=False)
    complemento = Column(String(100), nullable=True)
    bairro = Column(String(100), nullable=False)
    localidade = Column(String(100), nullable=False)
    uf = Column(String(2), nullable=False)

    profession = Column(String(100), nullable=False)

    def __init__(
        self,
        name,
        birth_date=None,
        tax_id=None,
        phone=None,
        email=None,
        cep=None,
        logradouro=None,
        complemento=None,
        bairro=None,
        localidade=None,
        uf=None,
        profession=None
    ):
        self.name = name
        self.birth_date = birth_date
        self.tax_id = tax_id
        self.phone = phone
        self.email = email

        self.cep = cep
        self.logradouro = logradouro
        self.complemento = complemento
        self.bairro = bairro
        self.localidade = localidade
        self.uf = uf

        self.profession = profession