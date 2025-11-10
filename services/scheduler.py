from datetime import datetime, timedelta
from sqlalchemy import select, func
from core.db import SessionLocal
from core.models import Slot, Booking


HOLD_MINUTES = 5


class Scheduler:
def __init__(self):
self.db = SessionLocal()


def _slot_usage(self, slot_id):
q = select(func.count()).select_from(Booking).where(
Booking.slot_id==slot_id, Booking.status=="CONFIRMED"
)
return self.db.execute(q).scalar_one()


def list_available(self, center_id, day: datetime):
start_day = day.replace(hour=0, minute=0, second=0, microsecond=0)
end_day = start_day + timedelta(days=1)
slots = self.db.execute(select(Slot).where(
Slot.center_id==center_id, Slot.start>=start_day, Slot.end<=end_day
)).scalars().all()
out = []
now = datetime.utcnow()
for s in slots:
used = self._slot_usage(s.id)
# consider temp holds
held = self.db.execute(select(func.count()).select_from(Booking).where(
Booking.slot_id==s.id, Booking.hold==True, # noqa
Booking.created_at>= now - timedelta(minutes=HOLD_MINUTES)
)).scalar_one()
remaining = max(s.capacity - used - held, 0)
out.append({"slot_id": s.id, "start": s.start, "end": s.end, "remaining": remaining})
return out


def hold_slot(self, slot_id, customer_name, vehicle_reg, service_type):
b = Booking(slot_id=slot_id, center_id=None, customer_name=customer_name,
vehicle_reg=vehicle_reg, service_type=service_type, status="CONFIRMED")
from datetime import datetime
b.created_at = datetime.utcnow()
b.hold = True
self.db.add(b)
self.db.commit()
return b.id


def confirm_booking(self, booking_id):
b = self.db.get(Booking, booking_id)
if b:
b.hold = False
self.db.commit()
return True
return False


def cancel_booking(self, booking_id):
b = self.db.get(Booking, booking_id)
if b:
b.status = "CANCELLED"
self.db.commit()
return True
return False
