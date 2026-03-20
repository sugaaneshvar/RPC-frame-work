from rpc_framework.marshalling import validate_types
from rpc_framework.models import StudentProfile
from rpc_framework.server import RPCServer


def test_validate_types_accepts_valid_profile() -> None:
    validate_types({"name": "Alice", "id": 7, "grades": [80, 90, 100]}, StudentProfile)


def test_validate_types_rejects_string_for_int() -> None:
    try:
        validate_types({"name": "Bob", "id": "seven", "grades": [70, 80]}, StudentProfile)
    except TypeError as exc:
        assert "payload.id expected int" in str(exc)
    else:
        raise AssertionError("Expected TypeError for invalid StudentProfile.id")


def test_server_calculates_average() -> None:
    server = RPCServer()
    response = server.handle_request(
        {
            "method": "calculate_grade_average",
            "params": {
                "profile": {"name": "Cara", "id": 9, "grades": [75, 85, 95]},
            },
        }
    )
    assert response == {"result": 85.0}


def test_server_rejects_invalid_profile() -> None:
    server = RPCServer()
    response = server.handle_request(
        {
            "method": "calculate_grade_average",
            "params": {
                "profile": {"name": "Dana", "id": "nine", "grades": [75, 85, 95]},
            },
        }
    )
    assert "error" in response
    assert "payload.id expected int" in response["error"]


if __name__ == "__main__":
    test_validate_types_accepts_valid_profile()
    test_validate_types_rejects_string_for_int()
    test_server_calculates_average()
    test_server_rejects_invalid_profile()
    print("All tests passed.")
