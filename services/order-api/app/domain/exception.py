class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


class DataSourceNotFound(NotFoundError):
    pass


class SessionNotFound(NotFoundError):
    pass


class InfrastructureError(Exception):
    pass


class IntegrityConstraintError(Exception):
    """Raised when a DB integrity constraint (FK, unique, check) is violated."""
    pass
