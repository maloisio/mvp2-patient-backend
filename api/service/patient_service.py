"""Camada de serviço (regras de negócio) da entidade Patient.

Orquestra as operações de cadastro, consulta, atualização e remoção
de pacientes, aplicando validações e traduzindo erros de banco em
exceções de domínio. Não conhece detalhes dos outros módulos,
ex SQLAlchemy nem de HTTP.
"""

from datetime import datetime, date
from sqlalchemy.exc import IntegrityError

from infra.repository import patient_repository
from infra.models import Patient
from exceptions import NotFoundError, ConflictError
from logger import logger
import time

from api.clients.scheduling_client import del_all_apointments

def _parse_date(value):
    """Converte string 'YYYY-MM-DD' em objeto date.
    Aceita None ou date direto.
    """
    if value is None:
        return None

    if isinstance(value, date):
        return value

    return datetime.strptime(value, "%Y-%m-%d").date()


def add_patient(
    name,
    birth_date,
    tax_id,
    phone,
    email,
    cep,
    logradouro,
    complemento,
    bairro,
    localidade,
    uf,
    profession
):
    """Adiciona um novo paciente à base de dados."""

    patient = Patient(
        name=name,
        birth_date=_parse_date(birth_date),
        tax_id=tax_id,
        phone=phone,
        email=email,
        cep=cep,
        logradouro=logradouro,
        complemento=complemento,
        bairro=bairro,
        localidade=localidade,
        uf=uf,
        profession=profession,
    )

    logger.debug(
        f"Adicionando paciente de nome: '{patient.name}'"
    )

    try:
        return patient_repository.create(patient)

    except IntegrityError as error:
        logger.exception(
            f"Erro de integridade ao adicionar paciente '{patient.name}'"
        )

        print("ERRO DE INTEGRIDADE:", error)
        print("CAUSA:", error.orig)

        raise ConflictError(
            f"Erro de integridade no banco: {error.orig}"
        )


def get_patients():
    """Retorna todos os pacientes cadastrados."""

    logger.debug("Buscando pacientes")

    patients = patient_repository.find_all()

    logger.debug(
        f"{len(patients)} pacientes encontrados"
    )

    return patients


def get_patient_by_id(patient_id):
    """Busca um paciente pelo ID.

    Lança NotFoundError se não existir.
    """

    start = time.perf_counter()

    patient = patient_repository.find_by_id(patient_id)

    elapsed = time.perf_counter() - start

    logger.debug(
        f"Busca do paciente #{patient_id} "
        f"levou {elapsed:.3f}s"
    )

    if not patient:
        error_msg = "Paciente não encontrado na base"

        logger.warning(
            f"Erro ao buscar paciente #{patient_id}, "
            f"{error_msg}"
        )

        raise NotFoundError(error_msg)

    logger.debug(
        f"Paciente encontrado: '{patient.name}'"
    )

    return patient


def update_patient(
    patient_id,
    name=None,
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
    """Atualiza os dados de um paciente já cadastrado.

    Só altera os campos que forem diferentes de None.
    """

    logger.debug(
        f"Atualizando dados do paciente #{patient_id}"
    )

    try:
        patient = patient_repository.update(
            patient_id,
            name=name,
            birth_date=(
                _parse_date(birth_date)
                if birth_date
                else None
            ),
            tax_id=tax_id,
            phone=phone,
            email=email,
            cep=cep,
            logradouro=logradouro,
            complemento=complemento,
            bairro=bairro,
            localidade=localidade,
            uf=uf,
            profession=profession,
        )

    except IntegrityError:
        error_msg = (
            "CPF ou e-mail já cadastrado "
            "por outro paciente"
        )

        logger.warning(
            f"Erro ao atualizar paciente "
            f"#{patient_id}, {error_msg}"
        )

        raise ConflictError(error_msg)

    if not patient:
        error_msg = "Paciente não encontrado na base"

        logger.warning(
            f"Erro ao atualizar paciente "
            f"#{patient_id}, {error_msg}"
        )

        raise NotFoundError(error_msg)

    logger.debug(
        f"Paciente #{patient_id} - "
        f"'{patient.name}' atualizado com sucesso"
    )

    return patient


def delete_patient_by_id(patient_id):
    """Remove um paciente pelo ID.

    Lança NotFoundError se não existir.
    Retorna o nome do paciente removido.
    """

    logger.debug(
        f"Deletando dados sobre paciente #{patient_id}"
    )

    patient_name = patient_repository.delete(patient_id)

    if not patient_name:
        error_msg = "Paciente não encontrado na base"

        logger.warning(
            f"Erro ao deletar paciente "
            f"#{patient_id}, {error_msg}"
        )

        raise NotFoundError(error_msg)

    logger.debug(
        f"Deletado paciente #{patient_id} "
        f"- '{patient_name}'"
    )

    response = del_all_apointments(patient_id)

    if not response:
        error_msg = "Paciente não possuí consultas"

        logger.debug(
            f"Erro ao deletar consultas "
            f"#{patient_id}, {error_msg}"
        )

    return patient_name