"""Repositório de acesso a dados da entidade Patient.

Contém apenas operações de banco de dados (CRUD). Não deve conter
regras de negócio.
"""

from sqlalchemy.orm import joinedload
from infra import Session
from infra.models import Patient


def create(patient: Patient) -> Patient:
    session = Session()
    try:
        session.add(patient)
        session.commit()
        return _get_by_id(session, patient.patient_id)
    finally:
        session.close()

def find_all():
    session = Session()
    try:
        return session.query(Patient).all()
    finally:
        session.close()

def find_by_id(patient_id: int):
    session = Session()
    try:
        return _get_by_id(session, patient_id)
    finally:
        session.close()


def update(patient_id: int, **fields):
    session = Session()
    try:
        patient = ( session.query(Patient) .filter(Patient.patient_id == patient_id) .first() )

        if not patient:
            return None

        for key, value in fields.items():
            if value is not None:
                setattr(patient, key, value)

        session.commit()
        return _get_by_id(session, patient_id)
    finally:
        session.close()


def delete(patient_id: int):
    session = Session()
    try:
        patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()
        if not patient:
            return None

        name = patient.name
        session.delete(patient)
        session.commit()
        return name
    finally:
        session.close()


def _get_by_id(session, patient_id):
    return (
        session.query(Patient)
        .filter(Patient.patient_id == patient_id)
        .first()
    )