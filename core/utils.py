from datetime import datetime, time


def combine_date_time(date_obj, hour, minute=0):
    """Utility to merge date with specific time."""
    return datetime.combine(date_obj, time(hour=hour, minute=minute))


def readable(dt: datetime):
    return dt.strftime("%d %b %Y, %I:%M %p")
