from sqlalchemy import select, func
from datetime import datetime, timedelta
from core.db import SessionLocal
from core.models import Booking, Slot


class Analytics:
    def __init__(self):
        self.db = SessionLocal()

    # ---------------------------------------------
    # 1) Fill Rate: (confirmed bookings / total capacity)
    # ---------------------------------------------
    def daily_fill_rate(self, center_id, day):
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        # total slot capacity
        slots = self.db.execute(
            select(Slot).where(
                Slot.center_id == center_id,
                Slot.start >= day_start,
                Slot.end <= day_end
            )
        ).scalars().all()

        total_capacity = sum(s.capacity for s in slots)

        # confirmed bookings
        confirmed = self.db.execute(
            select(func.count())
            .select_from(Booking)
            .where(
                Booking.center_id == center_id,
                Booking.status == "CONFIRMED",
                Booking.created_at >= day_start,
                Booking.created_at <= day_end
            )
        ).scalar_one()

        if total_capacity == 0:
            return 0.0

        return round((confirmed / total_capacity) * 100, 2)

    # ---------------------------------------------
    # 2) No-show rate
    # ---------------------------------------------
    def no_show_rate(self, center_id, day):
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        # total bookings
        total = self.db.execute(
            select(func.count())
            .select_from(Booking)
            .where(
                Booking.center_id == center_id,
                Booking.created_at >= day_start,
                Booking.created_at <= day_end
            )
        ).scalar_one()

        # no-shows
        no_shows = self.db.execute(
            select(func.count())
            .select_from(Booking)
            .where(
                Booking.center_id == center_id,
                Booking.status == "NO_SHOW",
                Booking.created_at >= day_start,
                Booking.created_at <= day_end
            )
        ).scalar_one()

        if total == 0:
            return 0.0

        return round((no_shows / total) * 100, 2)

    # ---------------------------------------------
    # 3) Peak hours (most booked time blocks)
    # ---------------------------------------------
    def peak_hours(self, center_id, day):
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        results = self.db.execute(
            select(
                Slot.start,
                func.count(Booking.id).label("usage")
            )
            .join(Booking, Booking.slot_id == Slot.id, isouter=True)
            .where(
                Slot.center_id == center_id,
                Slot.start >= day_start,
                Slot.end <= day_end
            )
            .group_by(Slot.start)
            .order_by(func.count(Booking.id).desc())
        ).all()

        # return top 3 peak slots
        return [
            {"start": row[0], "bookings": row[1]}
            for row in results[:3]
        ]

    # ---------------------------------------------
    # 4) Avg Lead Time (booking time → slot start)
    # ---------------------------------------------
    def avg_lead_time(self, center_id, day):
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        results = self.db.execute(
            select(
                Slot.start,
                Booking.created_at
            )
            .join(Slot, Slot.id == Booking.slot_id)
            .where(
                Booking.center_id == center_id,
                Booking.status == "CONFIRMED",
                Slot.start >= day_start,
                Slot.start <= day_end
            )
        ).all()

        if not results:
            return 0.0

        diffs = [
            (slot_start - created).total_seconds() / 3600
            for slot_start, created in results
        ]

        return round(sum(diffs) / len(diffs), 2)  # hours

    # ---------------------------------------------
    # 5) Service type distribution
    # ---------------------------------------------
    def service_type_stats(self, center_id, day):
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        results = self.db.execute(
            select(
                Booking.service_type,
                func.count().label("count")
            )
            .where(
                Booking.center_id == center_id,
                Booking.created_at >= day_start,
                Booking.created_at <= day_end
            )
            .group_by(Booking.service_type)
            .order_by(func.count().desc())
        ).all()

        return [{"service_type": r[0], "count": r[1]} for r in results]

    # ---------------------------------------------
    # 6) Combined analytics snapshot
    # ---------------------------------------------
    def daily_report(self, center_id, day):
        return {
            "date": day.strftime("%d-%m-%Y"),
            "fill_rate": self.daily_fill_rate(center_id, day),
            "no_show_rate": self.no_show_rate(center_id, day),
            "peak_hours": self.peak_hours(center_id, day),
            "avg_lead_time_hours": self.avg_lead_time(center_id, day),
            "service_type_distribution": self.service_type_stats(center_id, day),
        }
