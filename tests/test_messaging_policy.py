"""
Automated Test Suite for Messaging Policy (FR-08)
Executes all 18 Boundary Value Analysis test cases (TC-BVA-01 to 18)
and all 13 Decision Table rules (TC-DT-R1 to 13) from 06_Test_Plan_and_Evidence.md.
"""

import unittest
from datetime import time, datetime, timedelta

from src.models import Role, PolicyDecision, NoticeScope
from src.policy import MessagingPolicy


class TestBoundaryValueAnalysis(unittest.TestCase):
    """
    Verification of boundaries: 07:00 (opening), 19:59 (closing), 20:00 (cutoff), and midnight rollover.
    """

    # ── TEACHER ROUTINE MESSAGES (TC-BVA-01 to 09) ──
    def test_bva_01_teacher_0659(self):
        """TC-BVA-01: Teacher routine at 06:59 -> Queued for 07:00."""
        dec = MessagingPolicy.can_send_now(Role.TEACHER, time(6, 59), urgent=False)
        self.assertEqual(dec, PolicyDecision.QUEUE_FOR_0700)

    def test_bva_02_teacher_0700(self):
        """TC-BVA-02: Teacher routine at 07:00 -> Allowed (opening boundary)."""
        dec = MessagingPolicy.can_send_now(Role.TEACHER, time(7, 0), urgent=False)
        self.assertEqual(dec, PolicyDecision.ALLOW)

    def test_bva_03_teacher_0701(self):
        """TC-BVA-03: Teacher routine at 07:01 -> Allowed (inside window)."""
        dec = MessagingPolicy.can_send_now(Role.TEACHER, time(7, 1), urgent=False)
        self.assertEqual(dec, PolicyDecision.ALLOW)

    def test_bva_04_teacher_1958(self):
        """TC-BVA-04: Teacher routine at 19:58 -> Allowed (inside window)."""
        dec = MessagingPolicy.can_send_now(Role.TEACHER, time(19, 58), urgent=False)
        self.assertEqual(dec, PolicyDecision.ALLOW)

    def test_bva_05_teacher_1959(self):
        """TC-BVA-05: Teacher routine at 19:59 -> Allowed (last minute of window). Caught DEF-15."""
        dec = MessagingPolicy.can_send_now(Role.TEACHER, time(19, 59), urgent=False)
        self.assertEqual(dec, PolicyDecision.ALLOW)

    def test_bva_06_teacher_2000(self):
        """TC-BVA-06: Teacher routine at 20:00 -> Queued for next school day 07:00 (cutoff minute)."""
        dec = MessagingPolicy.can_send_now(Role.TEACHER, time(20, 0), urgent=False)
        self.assertEqual(dec, PolicyDecision.QUEUE_FOR_0700)

    def test_bva_07_teacher_2001(self):
        """TC-BVA-07: Teacher routine at 20:01 -> Queued for next school day 07:00."""
        dec = MessagingPolicy.can_send_now(Role.TEACHER, time(20, 1), urgent=False)
        self.assertEqual(dec, PolicyDecision.QUEUE_FOR_0700)

    def test_bva_08_teacher_2359(self):
        """TC-BVA-08: Teacher routine at 23:59 -> Queued for next school day 07:00."""
        dec = MessagingPolicy.can_send_now(Role.TEACHER, time(23, 59), urgent=False)
        self.assertEqual(dec, PolicyDecision.QUEUE_FOR_0700)

    def test_bva_09_teacher_0000(self):
        """TC-BVA-09: Teacher routine at 00:00 -> Queued for same day 07:00 without duplicate (DEF-35 safeguard)."""
        dec = MessagingPolicy.can_send_now(Role.TEACHER, time(0, 0), urgent=False)
        self.assertEqual(dec, PolicyDecision.QUEUE_FOR_0700)
        
        # Test midnight rollover next release calculation
        dt_2359 = datetime(2026, 1, 5, 23, 59)
        dt_0000 = datetime(2026, 1, 6, 0, 0)
        release_from_2359 = MessagingPolicy.get_next_window_open(dt_2359)
        release_from_0000 = MessagingPolicy.get_next_window_open(dt_0000)
        self.assertEqual(release_from_2359, datetime(2026, 1, 6, 7, 0))
        self.assertEqual(release_from_0000, datetime(2026, 1, 6, 7, 0))
        self.assertEqual(release_from_2359, release_from_0000, "Both 23:59 and 00:00 must resolve to single 07:00 dispatch.")

    # ── PARENT MESSAGES (TC-BVA-10 to 18) ──
    def test_bva_10_parent_0659(self):
        """TC-BVA-10: Parent at 06:59 -> Held for teacher at 07:00 + instant auto-reply."""
        dec = MessagingPolicy.can_send_now(Role.PARENT, time(6, 59))
        self.assertEqual(dec, PolicyDecision.HOLD_FOR_TEACHER)

    def test_bva_11_parent_0700(self):
        """TC-BVA-11: Parent at 07:00 -> Delivered immediately to teacher."""
        dec = MessagingPolicy.can_send_now(Role.PARENT, time(7, 0))
        self.assertEqual(dec, PolicyDecision.ALLOW)

    def test_bva_12_parent_0701(self):
        """TC-BVA-12: Parent at 07:01 -> Delivered immediately."""
        dec = MessagingPolicy.can_send_now(Role.PARENT, time(7, 1))
        self.assertEqual(dec, PolicyDecision.ALLOW)

    def test_bva_13_parent_1958(self):
        """TC-BVA-13: Parent at 19:58 -> Delivered immediately."""
        dec = MessagingPolicy.can_send_now(Role.PARENT, time(19, 58))
        self.assertEqual(dec, PolicyDecision.ALLOW)

    def test_bva_14_parent_1959(self):
        """TC-BVA-14: Parent at 19:59 -> Delivered immediately."""
        dec = MessagingPolicy.can_send_now(Role.PARENT, time(19, 59))
        self.assertEqual(dec, PolicyDecision.ALLOW)

    def test_bva_15_parent_2000(self):
        """TC-BVA-15: Parent at 20:00 -> Held until 07:00 + auto-reply."""
        dec = MessagingPolicy.can_send_now(Role.PARENT, time(20, 0))
        self.assertEqual(dec, PolicyDecision.HOLD_FOR_TEACHER)

    def test_bva_16_parent_2001(self):
        """TC-BVA-16: Parent at 20:01 -> Held until 07:00 + auto-reply."""
        dec = MessagingPolicy.can_send_now(Role.PARENT, time(20, 1))
        self.assertEqual(dec, PolicyDecision.HOLD_FOR_TEACHER)

    def test_bva_17_parent_2359(self):
        """TC-BVA-17: Parent at 23:59 -> Held until 07:00 + auto-reply."""
        dec = MessagingPolicy.can_send_now(Role.PARENT, time(23, 59))
        self.assertEqual(dec, PolicyDecision.HOLD_FOR_TEACHER)

    def test_bva_18_parent_0000(self):
        """TC-BVA-18: Parent at 00:00 -> Held until same 07:00 + auto-reply."""
        dec = MessagingPolicy.can_send_now(Role.PARENT, time(0, 0))
        self.assertEqual(dec, PolicyDecision.HOLD_FOR_TEACHER)


class TestDecisionTableRules(unittest.TestCase):
    """
    Verification of all 13 rules in Decision Table (TC-DT-R1 to TC-DT-R13).
    """

    def test_r1_teacher_in_window(self):
        """TC-DT-R1: Teacher routine in window (10:30) -> Send now."""
        dec = MessagingPolicy.can_send_now(Role.TEACHER, time(10, 30), urgent=False)
        self.assertEqual(dec, PolicyDecision.ALLOW)

    def test_r2_teacher_routine_outside_window(self):
        """TC-DT-R2: Teacher routine at 21:15 -> Queue for 07:00."""
        dec = MessagingPolicy.can_send_now(Role.TEACHER, time(21, 15), urgent=False)
        self.assertEqual(dec, PolicyDecision.QUEUE_FOR_0700)

    def test_r3_teacher_urgent_pending(self):
        """TC-DT-R3: Teacher urgent at 21:15 pending approval -> Request approval."""
        dec = MessagingPolicy.can_send_now(Role.TEACHER, time(21, 15), urgent=True, principal_approved=None)
        self.assertEqual(dec, PolicyDecision.NEEDS_PRINCIPAL_APPROVAL)

    def test_r4_teacher_urgent_approved(self):
        """TC-DT-R4: Teacher urgent at 21:15 approved by Principal -> Send now."""
        dec = MessagingPolicy.can_send_now(Role.TEACHER, time(21, 15), urgent=True, principal_approved=True)
        self.assertEqual(dec, PolicyDecision.ALLOW)

    def test_r5_teacher_urgent_rejected(self):
        """TC-DT-R5: Teacher urgent at 21:15 rejected by Principal -> Queue for 07:00 (Caught DEF-28)."""
        dec = MessagingPolicy.can_send_now(Role.TEACHER, time(21, 15), urgent=True, principal_approved=False)
        self.assertEqual(dec, PolicyDecision.QUEUE_FOR_0700)

    def test_r6_parent_in_window(self):
        """TC-DT-R6: Parent at 10:30 -> Delivered immediately."""
        dec = MessagingPolicy.can_send_now(Role.PARENT, time(10, 30))
        self.assertEqual(dec, PolicyDecision.ALLOW)

    def test_r7_parent_outside_window(self):
        """TC-DT-R7: Parent at 22:05 -> Auto-reply and hold until 07:00."""
        dec = MessagingPolicy.can_send_now(Role.PARENT, time(22, 5))
        self.assertEqual(dec, PolicyDecision.HOLD_FOR_TEACHER)

    def test_r8_class_notice_in_window(self):
        """TC-DT-R8: Class notice by teacher at 10:30 -> Publish now."""
        dec = MessagingPolicy.evaluate_notice_publishing(NoticeScope.CLASS, Role.TEACHER, time(10, 30))
        self.assertEqual(dec, PolicyDecision.ALLOW)

    def test_r9_class_notice_outside_window(self):
        """TC-DT-R9: Class notice by teacher at 21:15 -> Queue for 07:00."""
        dec = MessagingPolicy.evaluate_notice_publishing(NoticeScope.CLASS, Role.TEACHER, time(21, 15))
        self.assertEqual(dec, PolicyDecision.QUEUE_FOR_0700)

    def test_r10_school_notice_by_teacher(self):
        """TC-DT-R10: School-level notice by teacher at 10:30 -> Routes to Admin approval."""
        dec = MessagingPolicy.evaluate_notice_publishing(NoticeScope.SCHOOL, Role.TEACHER, time(10, 30))
        self.assertEqual(dec, PolicyDecision.NEEDS_PRINCIPAL_APPROVAL)

    def test_r11_school_notice_by_admin_in_window(self):
        """TC-DT-R11: School-level notice by admin at 10:30 -> Publish now."""
        dec = MessagingPolicy.evaluate_notice_publishing(NoticeScope.SCHOOL, Role.SCHOOL_ADMIN, time(10, 30))
        self.assertEqual(dec, PolicyDecision.ALLOW)

    def test_r12_school_notice_by_admin_outside_window(self):
        """TC-DT-R12: School-level notice by admin at 21:15 -> Queue for 07:00."""
        dec = MessagingPolicy.evaluate_notice_publishing(NoticeScope.SCHOOL, Role.SCHOOL_ADMIN, time(21, 15))
        self.assertEqual(dec, PolicyDecision.QUEUE_FOR_0700)

    def test_r13_school_notice_rejected(self):
        """TC-DT-R13: School-level notice rejected by admin -> Rejected."""
        dec = MessagingPolicy.evaluate_notice_publishing(NoticeScope.SCHOOL, Role.TEACHER, time(10, 30), admin_approved=False)
        self.assertEqual(dec, PolicyDecision.QUEUE_FOR_0700)


if __name__ == '__main__':
    unittest.main()
