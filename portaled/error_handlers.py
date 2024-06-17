from fastapi import Request
from fastapi.responses import JSONResponse
from portaled.utils.errors import AlreadyExistError, UnauthorizedError, NotFoundError, InvalidToken
from fastapi.exceptions import ValidationException


async def assertion_error_handler(request: Request, exc: AssertionError):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )


async def not_found_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc)}
    )


async def validation_exception_error_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )


async def unauthorized_error_handler(request: Request, exc: UnauthorizedError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.msg}
    )


async def already_exist_error_handler(request: Request, exc: AlreadyExistError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc)}
    )


async def invalid_token_error_handler(request: Request, exc: InvalidToken):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.msg}
    )
