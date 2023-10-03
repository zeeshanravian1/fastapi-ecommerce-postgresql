"""
    Middlewares Module

    Description:
    - This module contains all middlewares used in project.

"""

# Importing Python Packages
import logging
import re
from jose import JWTError, ExpiredSignatureError
from sqlalchemy.exc import IntegrityError

# Importing FastAPI Packages
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, ResponseValidationError

# Importing Project Files
from .response_message import core_response_message


exception_logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------


async def exception_handling(request: Request, call_next):
    """
    Exception Handling Middleware

    Description:
    - This function is used to handle exceptions.

    Parameter:
    - **request** (Request): Request object. **(Required)**
    - **call_next** (Callable): Next function to be called. **(Required)**

    Return:
    - **response** (Response): Response object.

    """
    print("Calling exception_handling middleware")

    try:
        response: Response = await call_next(request)

    except ExpiredSignatureError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": core_response_message.TOKEN_EXPIRED},
        )

    except JWTError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": core_response_message.INVALID_TOKEN},
        )

    except IntegrityError as err:
        err_message: str = (
            str(err.orig)
            .split("DETAIL:")[1]
            .replace("Key", "")
            .replace("(", "")
            .replace(")", "")
            .strip()
        )
        err_message = re.sub(
            pattern=r"in table.*", repl="", string=err_message
        ).strip()

        if err.orig.pgcode == "23502":
            detail = core_response_message.NOT_NULL_VIOLATION + str(
                err_message
            )

        elif err.orig.pgcode == "23503":
            detail = core_response_message.FOREIGN_KEY_VIOLATION + str(
                err_message
            )

        elif err.orig.pgcode == "23505":
            detail = core_response_message.UNIQUE_VIOLATION + str(err_message)

        else:
            exception_logger.exception(msg=err)
            detail = core_response_message.INTEGRITY_ERROR

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": detail},
        )

    except ResponseValidationError as err:
        exception_logger.exception(msg=err)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": core_response_message.INVALID_RESPONSE_BODY},
        )

    except HTTPException as err:
        exception_logger.exception(msg=err)
        return JSONResponse(
            status_code=err.status_code, content={"message": err.detail}
        )

    except Exception as err:
        exception_logger.exception(msg=err)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": core_response_message.INTERNAL_SERVER_ERROR},
        )

    return response
