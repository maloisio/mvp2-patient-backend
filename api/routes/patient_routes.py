"""Rotas HTTP da entidade Patient.

Responsável por receber as requisições, delegar o processamento para
api.service.patient_service e formatar a resposta HTTP (status code
e corpo JSON). Não contém regra de negócio nem acesso a banco.
"""

from urllib.parse import unquote

from api.schemas.patient import (
    PatientSchema,
    PatientUpdateSchema,
    PatientPathSchema,
    ListagemPatientsSchema,
    PatientViewSchema,
    PatientDelSchema,
    apresenta_patient,
    apresenta_patients,
)
from api.schemas.error import ErrorSchema
from api.service import patient_service
from exceptions import NotFoundError, ConflictError
from logger import logger
import time

def init_patient_routes(app, patient_tag):
    """Registra as rotas de Paciente na aplicação.
    """

    @app.post('/patient', tags=[patient_tag],
            responses={"200": PatientViewSchema, "409": ErrorSchema, "400": ErrorSchema})
    def add_patient(body: PatientSchema):
        """Adiciona um novo Paciente à base de dados

        Retorna uma representação do paciente cadastrado.
        """
        try:
            patient = patient_service.add_patient(
                name=body.name,
                birth_date=body.birth_date,
                tax_id=body.tax_id,
                phone=body.phone,
                email=body.email,
                cep=body.cep,
                logradouro=body.logradouro,
                complemento=body.complemento,
                bairro=body.bairro,
                localidade=body.localidade,
                uf=body.uf,
                profession=body.profession,
            )
            return apresenta_patient(patient), 200

        except ConflictError as e:
            return {"message": str(e)}, 409

        except Exception as e:
            error_msg = "Não foi possível salvar novo paciente"
            logger.warning(f"Erro ao adicionar paciente '{body.name}': {e}")
            return {"message": error_msg}, 400

    @app.get('/patients', tags=[patient_tag],
             responses={"200": ListagemPatientsSchema, "404": ErrorSchema})
    def get_patients():
        """Faz a busca por todos os Pacientes cadastrados

        Retorna uma representação da listagem de pacientes.
        """
        patients = patient_service.get_patients()

        if not patients:
            return {"patients": []}, 200

        return apresenta_patients(patients), 200

    @app.get(
        '/patient/<int:patient_id>',
        tags=[patient_tag],
        responses={"200": PatientViewSchema, "404": ErrorSchema}
    )
    def get_patient(path: PatientPathSchema):
        """Faz a busca por um Paciente a partir do ID informado"""

        logger.debug(
            f"REST Patient: recebendo GET /patient/{path.patient_id}"
        )

        start = time.perf_counter()

        try:
            patient = patient_service.get_patient_by_id(path.patient_id)

            logger.debug(
                f"REST Patient: get_patient_by_id levou "
                f"{time.perf_counter() - start:.3f}s"
            )

            start = time.perf_counter()

            result = apresenta_patient(patient)

            logger.debug(
                f"REST Patient: apresenta_patient levou "
                f"{time.perf_counter() - start:.3f}s"
            )

            return result, 200

        except NotFoundError as e:
            logger.debug(
                f"REST Patient: paciente #{path.patient_id} não encontrado"
            )

            return {"message": str(e)}, 404

    @app.delete('/patient/<int:patient_id>', tags=[patient_tag],
                responses={"200": PatientDelSchema, "404": ErrorSchema})
    def del_patient(path: PatientPathSchema):
        """Deleta um Paciente a partir do ID informado
        """
        try:
            patient_name = patient_service.delete_patient_by_id(path.patient_id)
            return {"message": "Paciente removido", "name": patient_name}, 200
        except NotFoundError as e:
            return {"message": str(e)}, 404
        
    @app.put('/patient/<int:patient_id>', tags=[patient_tag],
        responses={"200": PatientViewSchema, "404": ErrorSchema, "409": ErrorSchema})
    def update_patient(path: PatientPathSchema, body: PatientUpdateSchema):
        """Atualiza os dados de um Paciente já cadastrado a partir do ID informado

        Apenas os campos enviados no corpo serão alterados (atualização parcial).
        Retorna uma representação do paciente atualizado.
        """
        try:
            patient = patient_service.update_patient(
                patient_id=path.patient_id,
                name=body.name,
                birth_date=body.birth_date,
                tax_id=body.tax_id,
                phone=body.phone,
                email=body.email,
                cep=body.cep,
                logradouro=body.logradouro,
                complemento=body.complemento,
                bairro=body.bairro,
                localidade=body.localidade,
                uf=body.uf,
                profession=body.profession,
            )
            return apresenta_patient(patient), 200

        except NotFoundError as e:
            return {"message": str(e)}, 404

        except ConflictError as e:
            return {"message": str(e)}, 409