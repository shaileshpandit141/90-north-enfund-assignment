from typing import Any, Dict, List, NotRequired, TypedDict

TypeData = Dict[str, Any] | List[Dict[str, Any]]


class TypeError(TypedDict):
    field: str
    code: str
    message: str
    details: NotRequired[Dict[str, Any]]


TypeErrors = List[TypeError]


class TypeResponsePayload(TypedDict):
    message: str
    data: NotRequired[TypeData]
    errors: NotRequired[TypeErrors]


class TypeSuccessPayload(TypedDict):
    message: str
    data: TypeData


class TypeErrorPayload(TypedDict):
    message: str
    errors: TypeErrors
