from datetime import datetime

import pytest

from time_calculator import compute_date, compute_time, compute_difference


# ==========================================
#              compute_date
# ==========================================
class TestComputeDate:
    def test_leap_year_feb29_add_one_year(self):
        # 2024 is a leap year; adding 1 year clamps Feb 29 -> Feb 28
        result = compute_date("2024-02-29", 1, 0, 0, "Add")
        assert result == datetime(2025, 2, 28)

    def test_leap_year_feb29_add_four_years(self):
        # 2024 -> 2028 is also a leap year, so no clamping needed
        result = compute_date("2024-02-29", 4, 0, 0, "Add")
        assert result == datetime(2028, 2, 29)

    def test_month_end_clamping_jan31_minus_one_month(self):
        # Jan 31 - 1 month -> Dec 31 (Dec has 31 days, no clamping needed)
        result = compute_date("2026-01-31", 0, 1, 0, "Subtract")
        assert result == datetime(2025, 12, 31)

    def test_month_end_clamping_mar31_minus_one_month(self):
        # Mar 31 - 1 month -> Feb has only 28 days in 2026 (non-leap)
        result = compute_date("2026-03-31", 0, 1, 0, "Subtract")
        assert result == datetime(2026, 2, 28)

    def test_month_end_clamping_jan30_add_one_month_leap_year(self):
        # Jan 30 + 1 month -> Feb clamps to 29 in a leap year
        result = compute_date("2024-01-30", 0, 1, 0, "Add")
        assert result == datetime(2024, 2, 29)

    def test_year_boundary_crossing_add(self):
        result = compute_date("2025-12-15", 0, 1, 0, "Add")
        assert result == datetime(2026, 1, 15)

    def test_year_boundary_crossing_subtract(self):
        result = compute_date("2026-01-15", 0, 1, 0, "Subtract")
        assert result == datetime(2025, 12, 15)

    def test_subtract_does_not_double_negate(self):
        # Regression: a positive spinbox value combined with "Subtract"
        # must subtract once, not add (double negation of a negative sign).
        result = compute_date("2026-06-15", 0, 0, 5, "Subtract")
        assert result == datetime(2026, 6, 10)

    def test_add_is_positive(self):
        result = compute_date("2026-06-15", 0, 0, 5, "Add")
        assert result == datetime(2026, 6, 20)


# ==========================================
#              compute_time
# ==========================================
class TestComputeTime:
    def test_add_crosses_midnight(self):
        result = compute_time("11:59:59 PM", 0, 0, 2, "Add")
        assert result.strftime("%I:%M:%S %p") == "12:00:01 AM"

    def test_subtract_crosses_midnight_backwards(self):
        result = compute_time("12:00:00 AM", 0, 0, 1, "Subtract")
        assert result.strftime("%I:%M:%S %p") == "11:59:59 PM"

    def test_subtract_does_not_double_negate(self):
        result = compute_time("05:30:00 PM", 1, 0, 0, "Subtract")
        assert result.strftime("%I:%M:%S %p") == "04:30:00 PM"

    def test_add_is_positive(self):
        result = compute_time("05:30:00 PM", 1, 0, 0, "Add")
        assert result.strftime("%I:%M:%S %p") == "06:30:00 PM"


# ==========================================
#            compute_difference
# ==========================================
class TestComputeDifference:
    def test_normal_order_no_swap(self):
        delta, swapped = compute_difference("2026-01-01", "2026-05-01")
        assert not swapped
        assert (delta.years, delta.months, delta.days) == (0, 4, 0)

    def test_swap_when_end_before_start(self):
        # end date before start date must be swapped, and the caller
        # should be told so it can label the result accordingly
        delta, swapped = compute_difference("2026-05-01", "2026-01-01")
        assert swapped
        assert (delta.years, delta.months, delta.days) == (0, 4, 0)

    def test_leap_year_feb29_in_range(self):
        # Feb 29 2024 -> Feb 28 2025 is exactly 1 year (2025 is not a leap year)
        delta, swapped = compute_difference("2024-02-29", "2025-02-28")
        assert not swapped
        assert (delta.years, delta.months, delta.days) == (1, 0, 0)

    def test_year_boundary_crossing(self):
        delta, swapped = compute_difference("2025-11-15", "2026-02-15")
        assert not swapped
        assert (delta.years, delta.months, delta.days) == (0, 3, 0)

    def test_same_date_is_zero_difference(self):
        delta, swapped = compute_difference("2026-06-15", "2026-06-15")
        assert not swapped
        assert (delta.years, delta.months, delta.days) == (0, 0, 0)


# ==========================================
#           invalid input handling
# ==========================================
class TestInvalidInput:
    def test_compute_date_invalid_day_raises_value_error(self):
        with pytest.raises(ValueError):
            compute_date("2026-02-30", 0, 0, 1, "Add")

    def test_compute_difference_invalid_date_raises_value_error(self):
        with pytest.raises(ValueError):
            compute_difference("2026-13-01", "2026-01-01")
