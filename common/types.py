from typing import Any, TypeVar

from models.base import BaseModel

DataDict = dict[str, Any]
ClaimsDict = dict[str, Any]
APIResponseType: Any = [int, dict[str, Any]]
ModelType = TypeVar("ModelType", bound=BaseModel)
