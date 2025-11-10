from core.db import init_db, SessionLocal
from core.models import ServiceCenter, Slot
from datetime import datetime, timedelta


def main():
    init_db()
    db = SessionLocal()

    # Create a sample service center
    center = ServiceCenter(name="Noida Sector 62", day_capacity=48)
    db.add(center)
    db.commit()
    db.refresh(center)

    # Create 30-minute slots for 7 days, 9 AM – 6 PM
    for day_offset in range(7):
        day_start = (
            datetime.now()
            .replace(hour=9, minute=0, second=0, microsecond=0)
            + timedelta(days=day_offset)
        )
        current = day_start
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
    print("✅ Seed completed: Service center + slots created.")


if __name__ == "__main__":
    main()
