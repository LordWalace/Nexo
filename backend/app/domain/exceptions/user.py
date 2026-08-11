from app.core.exceptions import AppException


class UserNotFoundException(AppException):
    def __init__(self) -> None:
        super().__init__(
            code="USER_NOT_FOUND", message="Usuário não encontrado.", status_code=404
        )


class DuplicateEmailException(AppException):
    def __init__(self) -> None:
        super().__init__(
            code="DUPLICATE_EMAIL",
            message="Este e-mail já está em uso.",
            status_code=409,
        )
