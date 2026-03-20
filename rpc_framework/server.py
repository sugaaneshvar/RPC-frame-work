from __future__ import annotations

import json
import socket
from contextlib import closing
from typing import Any

from rpc_framework.marshalling import unmarshal_student_profile
from rpc_framework.models import StudentProfile
from rpc_framework.service import GradeService


class RPCServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 5000) -> None:
        self.host = host
        self.port = port
        self.service = GradeService()

    def handle_request(self, request: dict[str, Any]) -> dict[str, Any]:
        method = request.get("method")
        if method != "calculate_grade_average":
            return {"error": f"Unknown method: {method}"}

        try:
            profile_payload = request["params"]["profile"]
            profile = unmarshal_student_profile(profile_payload, StudentProfile)
            result = self.service.calculate_grade_average(profile)
            return {"result": result}
        except (KeyError, TypeError) as exc:
            return {"error": str(exc)}

    def serve_forever(self) -> None:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, self.port))
            sock.listen()
            while True:
                conn, _ = sock.accept()
                with closing(conn):
                    raw_request = conn.recv(4096).decode("utf-8")
                    response = self.handle_request(json.loads(raw_request))
                    conn.sendall(json.dumps(response).encode("utf-8"))


if __name__ == "__main__":
    RPCServer().serve_forever()
