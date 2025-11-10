from dataclasses import dataclass
from datetime import datetime


@dataclass
class BookingCreate:
    customer_name: str
    vehicle_reg: str
    service_type: str
    slot_id: int
    center_id: int


@dataclass
class SlotOut:
    slot_id: int
    start: datetime
    end: datetime
    remaining: int
