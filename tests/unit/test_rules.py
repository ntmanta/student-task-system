from datetime import date

from src.domain.rules import completion_rate, compute_status


def test_submission_before_deadline_is_submitted():
    assert compute_status(date(2026, 12, 1), date(2026, 11, 30)) == "Submitted"


def test_submission_on_deadline_is_submitted():
    assert compute_status(date(2026, 12, 1), date(2026, 12, 1)) == "Submitted"


def test_submission_after_deadline_is_late():
    assert compute_status(date(2026, 12, 1), date(2026, 12, 2)) == "Late"


def test_completion_rate_half():
    assert completion_rate(5, 10) == 50.0


def test_completion_rate_with_zero_students_is_zero():
    assert completion_rate(0, 0) == 0.0


def test_completion_rate_is_rounded_to_two_decimals():
    assert completion_rate(1, 3) == 33.33