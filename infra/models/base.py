"""Base declarativa compartilhada por todos os modelos SQLAlchemy.

Deve existir uma única instância de Base em todo o projeto, para que
todas as tabelas sejam registradas no mesmo metadata e possam ser
criadas juntas por Base.metadata.create_all().
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()