from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .db import Base


class ServiceCenter(Base):
__tablename__ = "service_centers"
id = Column(Integer, primary_key=True)
name = Column(String, nullable=False)
tz = Column(String, default="Asia/Kolkata")
day_capacity = Column(Integer, default=40) # max bookings per day
slots = relationship("Slot", back_populates="center")


class Technician(Base):
__tablename__ = "technicians"
id = Column(Integer, primary_key=True)
name = Column(String, nullable=False)
center_id = Column(Integer, ForeignKey("service_centers.id"))


class Slot(Base):
__tablename__ = "slots"
id = Column(Integer, primary_key=True)
center_id = Column(Integer, ForeignKey("service_centers.id"))
start = Column(DateTime, nullable=False)
end = Column(DateTime, nullable=False)
capacity = Column(Integer, default=4) # parallel bays
center = relationship("ServiceCenter", back_populates="slots")
__table_args__ = (UniqueConstraint('center_id','start','end', name='uq_center_slot'),)


class Booking(Base):
__tablename__ = "bookings"
id = Column(Integer, primary_key=True)
center_id = Column(Integer, ForeignKey("service_centers.id"))
slot_id = Column(Integer, ForeignKey("slots.id"))
customer_name = Column(String, nullable=False)
vehicle_reg = Column(String, nullable=False)
service_type = Column(String, default="General Service")
created_at = Column(DateTime)
status = Column(String, default="CONFIRMED") # CONFIRMED/CANCELLED/NO_SHOW
hold = Column(Boolean, default=False) # temporary hold to avoid double booking
