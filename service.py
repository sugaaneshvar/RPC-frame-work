from rpc_framework.models import StudentProfile


class GradeService:
    def calculate_grade_average(self, profile: StudentProfile) -> float:
        if not profile.grades:
            return 0.0
        return float(sum(profile.grades) / len(profile.grades))
