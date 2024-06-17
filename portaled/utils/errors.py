class NotFoundError(Exception):
    status_code = 404


class AlreadyExistError(Exception):
    status_code = 400


class UnauthorizedError(Exception):
    status_code = 401
    msg = "You're not authorized to perform this action."


class InvalidToken(Exception):
    status_code = 403
    msg = "Token is invalid or expired"
