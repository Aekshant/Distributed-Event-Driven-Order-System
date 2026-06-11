from __future__ import annotations

from http import HTTPStatus
from typing import Any, Generic, TypeVar
from uuid import UUID
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

T = TypeVar("T")
class ApiResponse(BaseModel, Generic[T]):
    status: int
    success: bool
    message: str
    data: T

    @classmethod
    def ok(cls, data: T, message: str = "Success", status_code: int = 200) -> "ApiResponse[T]":
        return cls(status=status_code, success=True, message=message, data=data)

    @classmethod
    def fail(cls, message: str, data: object | None = None, status_code: int = 400) -> "ApiResponse[object]":
        return cls(status=status_code, success=False, message=message, data=data if data is not None else {})




def parse_user_id(x_user_id: str | None) -> UUID | None:
    if not x_user_id:
        return None
    try:
        return UUID(x_user_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid X-User-Id header") from exc


def ok_response(
    data: Any,
    message: str = "Success",
    *,
    status_code: int | HTTPStatus = HTTPStatus.OK,
) -> JSONResponse:
    code = int(status_code)
    payload = ApiResponse.ok(data, message, status_code=code)
    return JSONResponse(
        status_code=code,
        content=jsonable_encoder(payload),
    )


def fail_response(
    message: str,
    data: Any | None = None,
    *,
    status_code: int | HTTPStatus = HTTPStatus.BAD_REQUEST,
) -> JSONResponse:
    code = int(status_code)
    payload = ApiResponse.fail(message, data, status_code=code)
    return JSONResponse(
        status_code=code,
        content=jsonable_encoder(payload),
    )
