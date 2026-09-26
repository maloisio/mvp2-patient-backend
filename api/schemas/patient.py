"""Schemas Pydantic da entidade Patient.

Define os formatos de entrada (criação e atualização) e saída
(visualização, listagem, remoção) usados pelas rotas, além das
funções que convertem instâncias de Patient em dicionários prontos
para serialização JSON.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from infra.models.patient import Patient


def validar_formato_data(value: Optional[str]) -> Optional[str]:
    if value is None:
        return value
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ValueError("birth_date deve estar no formato 'YYYY-MM-DD' (ex: '1990-05-20')")
    return value


class PatientSchema(BaseModel):
    """Define como um novo paciente a ser inserido deve ser representado."""

    name: str = "Maria da Silva"
    birth_date: str = "1990-05-20"
    tax_id: str = "12345678900"
    phone: str = "41999999999"
    email: str = "maria.silva@email.com"

    cep: str = "80230-000"
    logradouro: str = "Rua das Flores"
    complemento: Optional[str] = "Apto 101"
    bairro: str = "Centro"
    localidade: str = "Curitiba"
    uf: str = "PR"

    profession: str = "Engenheira"

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, value):
        return validar_formato_data(value)


class PatientUpdateSchema(BaseModel):
    name: Optional[str] = "PrimeiroNomeAtualizado UltimoNomeAtualizado"
    birth_date: Optional[str] = "2026-05-20"
    tax_id: Optional[str] = "CpfAtualizado"
    phone: Optional[str] = "TelefoneAtualizado"
    email: Optional[str] = "email@atualizado"

    cep: Optional[str] = "80230-000"
    logradouro: Optional[str] = "Rua Atualizada"
    complemento: Optional[str] = "Apto 202"
    bairro: Optional[str] = "Centro"
    localidade: Optional[str] = "Curitiba"
    uf: Optional[str] = "PR"

    profession: Optional[str] = "ProfissaoAtualizada"

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, value):
        return validar_formato_data(value)


class PatientPathSchema(BaseModel):
    patient_id: int


class ListagemPatientsSchema(BaseModel):
    patients: List[PatientSchema]


class PatientViewSchema(BaseModel):
    id: int = 1
    name: str = "Maria da Silva"
    birth_date: str = "1990-05-20"
    tax_id: str = "12345678900"
    phone: str = "41999999999"
    email: str = "maria.silva@email.com"

    cep: str = "80230-000"
    logradouro: str = "Rua das Flores"
    complemento: Optional[str] = "Apto 101"
    bairro: str = "Centro"
    localidade: str = "Curitiba"
    uf: str = "PR"

    profession: str = "Engenheira"



class PatientDelSchema(BaseModel):
    mesage: str
    name: str


def apresenta_patient(patient: Patient):
    """ Retorna uma representação do paciente seguindo o schema definido em
        PatientViewSchema.
    """
    return {
        "patient_id": patient.patient_id,
        "name": patient.name,
        "birth_date": (
            patient.birth_date.isoformat()
            if patient.birth_date
            else None
        ),
        "tax_id": patient.tax_id,
        "phone": patient.phone,
        "email": patient.email,

        "cep": patient.cep,
        "logradouro": patient.logradouro,
        "complemento": patient.complemento,
        "bairro": patient.bairro,
        "localidade": patient.localidade,
        "uf": patient.uf,

        "profession": patient.profession,
    }


def apresenta_patients(patients: List[Patient]):
    """ Retorna uma representação dos pacientes seguindo o schema definido em
        PatientViewSchema, incluindo as consultas de cada um.
    """
    return {"patients": [apresenta_patient(p) for p in patients]}