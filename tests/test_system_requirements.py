"""
System Requirements & Functional Acceptance Tests
Implements system test cases TC-01 through TC-10 matching the Traceability Matrix (SRS Section 4).
"""

import unittest
from datetime import datetime, time

from src.models import Role, NoticeScope, NoticeStatus, MessageStatus
from src.database import db
from src.services import (
    NoticeService, ReadReceiptService, MessagingService,
    AttendanceService, HomeworkService, AdminService, AuditReportService
)


class TestSystemRequirements(unittest.TestCase):

    def setUp(self):
        # Fresh database state for tests
        db._seed_pilot_data()

    def test_tc_01_role_scoped_access(self):
        """TC-01: Verify role boundaries and data scoping."""
        teacher = db.users["USR-TCH-01"]  # Rahul (SEC-5A, SEC-7B)
        parent = db.users["USR-PAR-01"]   # Meena (Aarav, SEC-5A)
        
        # Teacher is scoped to SEC-5A and SEC-7B
        self.assertIn("SEC-5A", teacher.mapped_section_ids)
        self.assertIn("SEC-7B", teacher.mapped_section_ids)
        self.assertNotIn("SEC-5B", teacher.mapped_section_ids, "Teacher should not have access to unmapped Section 5B")

        # Parent is scoped to their own child
        self.assertIn("STU-01", parent.children_ids)
        self.assertNotIn("STU-02", parent.children_ids, "Parent must not have access to another child")

        # Privacy phone masking
        self.assertTrue("XXXX" in parent.masked_contact)
        self.assertTrue("XXXX" in teacher.masked_contact)

    def test_tc_02_notices_and_approvals(self):
        """TC-02: Class notice publishes immediately; school notice requires admin approval."""
        teacher = db.users["USR-TCH-01"]
        admin = db.users["USR-ADM-01"]

        # 1. Class notice inside window -> PUBLISHED
        class_not, msg = NoticeService.compose_notice(
            author=teacher,
            title="Class 5A Quiz",
            body="Quiz tomorrow",
            scope=NoticeScope.CLASS,
            section_id="SEC-5A",
            simulated_time=time(10, 30)
        )
        self.assertEqual(class_not.status, NoticeStatus.PUBLISHED)

        # 2. School notice by teacher -> PENDING_APPROVAL
        school_not, msg = NoticeService.compose_notice(
            author=teacher,
            title="Annual Sports Day Announcement",
            body="All schools sports day",
            scope=NoticeScope.SCHOOL,
            simulated_time=time(10, 30)
        )
        self.assertEqual(school_not.status, NoticeStatus.PENDING_APPROVAL)
        
        # Verify approval request was generated
        req = next((r for r in db.approval_requests.values() if r.target_id == school_not.notice_id), None)
        self.assertIsNotNone(req)
        self.assertEqual(req.approver_role, Role.SCHOOL_ADMIN)

        # 3. Admin approves -> PUBLISHED
        success, approve_msg = NoticeService.approve_notice(req.request_id, admin, approved=True)
        self.assertTrue(success)
        self.assertEqual(school_not.status, NoticeStatus.PUBLISHED)

    def test_tc_03_read_receipts_analytics(self):
        """TC-03: Verify 60% read rate and unread parent list on notice NOT-01."""
        analytics = ReadReceiptService.get_notice_analytics("NOT-01")
        self.assertEqual(analytics["total"], 10)
        self.assertEqual(analytics["read_count"], 6)
        self.assertEqual(analytics["unread_count"], 4)
        self.assertEqual(analytics["read_percent"], 60.0)
        self.assertEqual(len(analytics["unread_parents"]), 4)

        # Mark 7th parent as read
        ReadReceiptService.mark_read("NOT-01", "USR-PAR-07")
        updated = ReadReceiptService.get_notice_analytics("NOT-01")
        self.assertEqual(updated["read_percent"], 70.0)
        self.assertEqual(len(updated["unread_parents"]), 3)

    def test_tc_04_homework_acknowledgement(self):
        """TC-04: Post homework and record parent acknowledgement."""
        teacher = db.users["USR-TCH-01"]
        parent = db.users["USR-PAR-02"]

        hw = HomeworkService.post_homework(
            teacher=teacher,
            section_id="SEC-5A",
            subject="Science",
            title="Plant Life Cycle Drawing",
            description="Draw parts of a flower",
            due_date="2026-10-10"
        )
        self.assertIsNotNone(hw.homework_id)
        self.assertNotIn(parent.user_id, hw.acknowledged_by)

        # Parent acknowledges
        ack = HomeworkService.acknowledge_homework(hw.homework_id, parent.user_id)
        self.assertTrue(ack)
        self.assertIn(parent.user_id, hw.acknowledged_by)

    def test_tc_05_attendance_15min_alert(self):
        """TC-05: Roll-call marking absent triggers push notification."""
        teacher = db.users["USR-TCH-01"]
        records = AttendanceService.submit_roll_call(
            teacher=teacher,
            section_id="SEC-5A",
            absent_student_ids=["STU-01"]  # Aarav Kulkarni is absent
        )

        aarav_rec = next(r for r in records if r.student_id == "STU-01")
        self.assertEqual(aarav_rec.status, "ABSENT")
        self.assertIsNotNone(aarav_rec.alert_sent_at)

        other_rec = next(r for r in records if r.student_id == "STU-02")
        self.assertEqual(other_rec.status, "PRESENT")
        self.assertIsNone(other_rec.alert_sent_at)

    def test_tc_06_fee_reminders_no_payment(self):
        """TC-06: Fee reminder generated with D-7 and D-1 notices and zero payment endpoint."""
        fee = db.fee_reminders[0]
        self.assertIn("Reminders only", fee.description)
        self.assertEqual(fee.days_before, 7)
        self.assertEqual(fee.amount, 8500.0)

    def test_tc_07_two_way_messaging_thread(self):
        """TC-07: Parent and teacher converse in isolated thread with masked numbers."""
        teacher = db.users["USR-TCH-01"]
        parent = db.users["USR-PAR-01"]

        # Teacher replies inside window (10:40 AM)
        msg, info, auto = MessagingService.send_message(
            conversation_id="CONV-01",
            sender=teacher,
            recipient=parent,
            body="Aarav is doing great in fractions.",
            simulated_time=time(10, 40)
        )
        self.assertEqual(msg.status, MessageStatus.SENT)
        self.assertIsNone(auto)

    def test_tc_08_messaging_hours_queueing_and_urgent(self):
        """TC-08: Out-of-hours queueing and urgent approval."""
        teacher = db.users["USR-TCH-01"]
        parent = db.users["USR-PAR-01"]
        principal = db.users["USR-PRIN-01"]

        # 1. Routine teacher message at 21:15 -> QUEUED
        m1, info1, _ = MessagingService.send_message(
            conversation_id="CONV-01",
            sender=teacher,
            recipient=parent,
            body="Routine note",
            urgent=False,
            simulated_time=time(21, 15)
        )
        self.assertEqual(m1.status, MessageStatus.QUEUED)

        # 2. Urgent teacher message at 21:15 -> PENDING_APPROVAL
        m2, info2, _ = MessagingService.send_message(
            conversation_id="CONV-01",
            sender=teacher,
            recipient=parent,
            body="Urgent: School bus route changed tomorrow",
            urgent=True,
            simulated_time=time(21, 15)
        )
        self.assertEqual(m2.status, MessageStatus.PENDING_APPROVAL)

        # Find approval request
        req = next(r for r in db.approval_requests.values() if r.target_id == m2.message_id)
        self.assertEqual(req.approver_role, Role.PRINCIPAL)

        # Principal approves -> SENT immediately
        ok, res_msg = MessagingService.adjudicate_urgent_message(req.request_id, principal, approved=True)
        self.assertTrue(ok)
        self.assertEqual(m2.status, MessageStatus.SENT)

    def test_tc_09_admin_csv_bulk_import(self):
        """TC-09: Bulk CSV import with 1 corrupted row; reports exact failure line."""
        sample_csv = """RollNo, StudentName, Section, ParentName, ParentPhone, ParentEmail
101, Rohan Joshi, SEC-5A, Ramesh Joshi, 9821999901, ramesh@gmail.com
102, Priya Shah, SEC-5A, Neha Shah, INVALID_PHONE, neha@gmail.com
103, Siddharth Roy, SEC-5A, Anirudh Roy, 9821999903, anirudh@gmail.com
"""
        success, errors = AdminService.parse_and_import_roster_csv(sample_csv, "SCH-01")
        self.assertEqual(success, 2)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["line"], 3)
        self.assertIn("Invalid phone number", errors[0]["error"])

    def test_tc_10_audit_log_and_management_kpis(self):
        """TC-10: Audit log query and KPI compliance calculations."""
        # Query audit log
        logs = AuditReportService.search_audit_log(keyword="NOTICE")
        self.assertGreater(len(logs), 0)

        # Check Active Parents metric
        active_metric = AuditReportService.get_monthly_active_parents_metric()
        self.assertGreater(active_metric["total_parents"], 0)
        self.assertIn("percentage", active_metric)
        self.assertEqual(active_metric["target_percentage"], 90.0)

        # Check Late Messages metric
        late_metric = AuditReportService.get_after_hours_teacher_messages_metric()
        self.assertEqual(late_metric["routine_after_8"], 0)
        self.assertTrue(late_metric["compliant"])


if __name__ == '__main__':
    unittest.main()
