from datetime import datetime


def overlaps(a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime) -> bool:
    """True if the time range a overlaps the time range b."""
    return a_start <= b_end and b_start <= a_end
