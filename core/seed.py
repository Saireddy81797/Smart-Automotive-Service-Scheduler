from core.db import init_db, SessionLocal
from core.models import ServiceCenter, Slot
from datetime import datetime, timedelta


def main():
    init_db()
    db = SessionLocal()

    # Clear old data (optional but recommended)
    db.query(Slot).delete()
    db.query(ServiceCenter).delete()
    db.commit()

    # Create 1 service center
    center = ServiceCenter(
        name="Noida Sector 62",
        tz="Asia/Kolkata",
        day_capacity=48
    )
    db.add(center)
    db.commit()
    db.refresh(center)

    # Create 7 days of slots (9 AM – 6 PM, every 30 mins)
    for day_offset in range(7):
        start_day = (
            datetime.now()
            .replace(hour=9, minute=0, second=0, microsecond=0)
            + timedelta(days=day_offset)
        )
        current = start_day
        while current.hour < 18:
            slot = Slot(
                center_id=center.id,
                start=current,
                end=current + timedelta(minutes=30),
                capacity=4,
            )
            db.add(slot)
            current += timedelta(minutes=30)

    db.commit()
    print("✅ DB Seed Complete — slots + center created.")


if __name__ == "__main__":
    main()
