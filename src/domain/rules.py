"""Pure business rules (no database, no web code)."""
from datetime import date


def compute_status(deadline: date, submitted_on: date) -> str:
    """A submission made on or before the deadline is 'Submitted', otherwise 'Late'."""
    return "Submitted" if submitted_on <= deadline else "Late"


def completion_rate(submitted_count: int, total_students: int) -> float:
    """Percentage of students who submitted, rounded to 2 decimals."""
    if total_students <= 0:
        return 0.0
    return round(submitted_count / total_students * 100, 2)