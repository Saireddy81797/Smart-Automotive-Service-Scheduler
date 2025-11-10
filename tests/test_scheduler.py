import unittest
from datetime import datetime
from services.scheduler import Scheduler

class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.scheduler = Scheduler()

    def test_list_available(self):
        today = datetime.now()
        slots = self.scheduler.list_available(center_id=1, day=today)
        self.assertIsInstance(slots, list)
        if slots:
            sample = slots[0]
            self.assertIn("slot_id", sample)
            self.assertIn("remaining", sample)
            self.assertIn("start", sample)

    def test_hold_and_confirm(self):
        today = datetime.now()
        slots = self.scheduler.list_available(center_id=1, day=today)
        if not slots:
            self.skipTest("No slots available to test booking.")

        first_slot = slots[0]["slot_id"]

        booking_id = self.scheduler.hold_slot(
            slot_id=first_slot,
            customer_name="Test User",
            vehicle_reg="TS09AB1234",
            service_type="General Service"
        )

        self.assertIsNotNone(booking_id)

        result = self.scheduler.confirm_booking(booking_id)
        self.assertTrue(result)

    def test_cancel(self):
        today = datetime.now()
        slots = self.scheduler.list_available(center_id=1, day=today)

        if not slots:
            self.skipTest("No slots available to test cancellation.")

        first_slot = slots[0]["slot_id"]

        booking_id = self.scheduler.hold_slot(
            slot_id=first_slot,
            customer_name="Cancel User",
            vehicle_reg="AP39AB5555",
            service_type="Inspection"
        )

        result = self.scheduler.cancel_booking(booking_id)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
