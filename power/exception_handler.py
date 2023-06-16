from urllib.request import Request

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.responses import JSONResponse

ERROR_MSG_MISSING = "Field `{field}` is missing."
ERROR_MSG_TYPE_ERROR = "Field `{field}` is should be {type}."


def pydantic_validation_exception_handler(request: Request, exception: RequestValidationError) -> JSONResponse:
    try:
        field_errors = []

        for pydantic_error in exception.errors():
            loc, msg = (
                pydantic_error["loc"],
                pydantic_error["msg"],
            )
            filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
            field_string = ".".join(filtered_loc)  # nested fields with dot-notation
            error_type = pydantic_error.get("type")
            print(error_type)
            if error_type == "value_error.missing":
                msg = ERROR_MSG_MISSING.format(field=field_string)
            elif "type_error" in error_type and "enum" not in error_type:
                msg = ERROR_MSG_TYPE_ERROR.format(field=field_string, type=error_type.split(".")[-1])
            else:
                msg = f"Field `{field_string}`, {msg}"

            field_errors.append(msg)
        return JSONResponse({"status_code": 400, "message": field_errors})
    except TypeError:
        return JSONResponse({"status_code": 400, "message": "Invalid JSON"})


EXCEPTION_HANDLERS_DICT = {
    RequestValidationError: pydantic_validation_exception_handler,
    ValidationError: pydantic_validation_exception_handler,
}
