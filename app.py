"""Ponto de entrada da aplicação Flask.

Cria a instância da API, registra as tags de documentação do
Swagger e inicializa as rotas de cada entidade.
"""

from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS

from api.routes.patient_routes import init_patient_routes

info = Info(title="API Gestão de Pacientes", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
patient_tag = Tag(name="Patient", description="Adição, visualização e remoção de pacientes à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


init_patient_routes(app, patient_tag)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )