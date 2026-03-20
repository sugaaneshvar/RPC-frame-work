from dataclasses import dataclass


@dataclass
class StudentProfile:
    name: str
    id: int
    grades: list[int]
