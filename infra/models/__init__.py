"""Agrega os modelos do pacote infra.models para facilitar os imports.

Importar este módulo garante que todas as classes mapeadas (Base,
Patient) sejam registradas no metadata do SQLAlchemy
antes da criação das tabelas.
"""

from infra.models.base import Base
from infra.models.patient import Patient
