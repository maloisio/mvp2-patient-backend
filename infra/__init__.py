"""Ponto central de configuração do banco de dados.

Cria o diretório do banco (se necessário), a engine de conexão, a
fábrica de sessões (Session) e garante que todas as tabelas mapeadas
em infra.models existam no banco SQLite.
"""

from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from infra.models import Base, Patient

db_path = "infra/db/"

if not os.path.exists(db_path):
    os.makedirs(db_path)

db_url = 'sqlite:///%s/db.sqlite3' % db_path

engine = create_engine(db_url, echo=False)

Session = sessionmaker(bind=engine)

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)