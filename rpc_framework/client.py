from __future__ import annotations

import json
import socket
from contextlib import closing

from rpc_framework.marshalling import marshal_request
from rpc_framework.models import StudentProfile


class RPCClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 5000) -> None:
        self.host = host
        self.port = port

    def calculate_grade_average(self, profile: StudentProfile) -> float:
        request = marshal_request(
            "calculate_grade_average",
            {"name": profile.name, "id": profile.id, "grades": profile.grades},
        )
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.connect((self.host, self.port))
            sock.sendall(json.dumps(request).encode("utf-8"))
            response = json.loads(sock.recv(4096).decode("utf-8"))

        if "error" in response:
            raise TypeError(response["error"])
        return float(response["result"])
