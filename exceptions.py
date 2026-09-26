
class NotFoundError(Exception):
    """Recurso não encontrado."""
    pass


class ConflictError(Exception):
    """Conflito de dados únicos (ex: CPF/e-mail duplicado)."""
    pass