from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Any, get_args, get_origin, get_type_hints


def validate_types(value: Any, expected_type: Any, path: str = "payload") -> None:
    """Validate incoming values against the expected schema."""
    origin = get_origin(expected_type)

    if expected_type is Any:
        return

    if origin is list:
        if not isinstance(value, list):
            raise TypeError(f"{path} expected list, received {type(value).__name__}")
        (item_type,) = get_args(expected_type)
        for index, item in enumerate(value):
            validate_types(item, item_type, f"{path}[{index}]")
        return

    if is_dataclass(expected_type):
        if not isinstance(value, dict):
            raise TypeError(f"{path} expected object, received {type(value).__name__}")
        hints = get_type_hints(expected_type)
        for field in fields(expected_type):
            if field.name not in value:
                raise TypeError(f"{path}.{field.name} is required")
            validate_types(value[field.name], hints[field.name], f"{path}.{field.name}")
        return

    if not isinstance(value, expected_type):
        raise TypeError(
            f"{path} expected {expected_type.__name__}, received {type(value).__name__}"
        )


def marshal_request(method: str, profile_data: dict[str, Any]) -> dict[str, Any]:
    return {"method": method, "params": {"profile": profile_data}}


def unmarshal_student_profile(payload: dict[str, Any], profile_type: type) -> Any:
    validate_types(payload, profile_type)
    return profile_type(**payload)
