from datetime import datetime, timedelta
from sqlalchemy import select, func
from core.db import SessionLocal
from core.models import Slot, Booking

HOLD_MINUTES = 5


class Scheduler:
    def __init__(self):
        self.db = SessionLocal()

    # --------------------------------------------------
    # ✅ Get available slots for a given day
    # --------------------------------------------------
    def list_available(self, center_id, day: datetime):
        start_day = day.replace(hour=0, minute=0, second=0, microsecond=0)
        end_day = start_day + timedelta(days=1)

        slots = (
            self.db.execute(
                select(Slot).where(
                    Slot.center_id == center_id,
                    Slot.start >= start_day,
                    Slot.end <= end_day
                )
            ).scalars().all()
        )

        now = datetime.utcnow()
        results = []

        for s in slots:
            # confirmed bookings
            used = (
                self.db.execute(
                    select(func.count())
                    .select_from(Booking)
                    .where(
                        Booking.slot_id == s.id,
                        Booking.status == "CONFIRMED"
                    )
                ).scalar_one()
            )

            # held bookings
            held = (
                self.db.execute(
                    select(func.count())
                    .select_from(Booking)
                    .where(
                        Booking.slot_id == s.id,
                        Booking.hold == True,
                        Booking.created_at >= now - timedelta(minutes=HOLD_MINUTES)
                    )
                ).scalar_one()
            )

            remaining = max(s.capacity - used - held, 0)

            results.append({
                "slot_id": s.id,
                "start": s.start,
                "end": s.end,
                "remaining": remaining
            })

        return results

    # --------------------------------------------------
    # ✅ Hold a slot temporarily
    # --------------------------------------------------
    def hold_slot(self, slot_id, customer_name, vehicle_reg, service_type):
        from datetime import datetime

        booking = Booking(
            slot_id=slot_id,
            center_id=None,
            customer_name=customer_name,
            vehicle_reg=vehicle_reg,
            service_type=service_type,
            status="CONFIRMED",
            hold=True,
            created_at=datetime.utcnow()
        )

        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)

        return booking.id

    # --------------------------------------------------
    # ✅ Convert held booking → permanent booking
    # --------------------------------------------------
    def confirm_booking(self, booking_id):
        booking = self.db.get(Booking, booking_id)

        if not booking:
            return False

        booking.hold = False
        self.db.commit()
        return True

    # --------------------------------------------------
    # ✅ Cancel booking
    # --------------------------------------------------
    def cancel_booking(self, booking_id):
        booking = self.db.get(Booking, booking_id)

        if not booking:
            return False

        booking.status = "CANCELLED"
        self.db.commit()
        return True
