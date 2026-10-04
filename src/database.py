"""
SchoolDiary Data Store and Seeding Engine
In-memory relational data store with pre-seeded pilot schools, classrooms, faculty, and parents.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import copy

from src.models import (
    User, Role, School, ClassSection, Student, Notice, ReadReceipt,
    Homework, AttendanceRecord, FeeReminder, Message, Conversation,
    ApprovalRequest, AuditEntry, NoticeScope, NoticeStatus, MessageStatus
)


class DataStore:
    def __init__(self):
        self.schools: Dict[str, School] = {}
        self.sections: Dict[str, ClassSection] = {}
        self.users: Dict[str, User] = {}
        self.students: Dict[str, Student] = {}
        self.notices: Dict[str, Notice] = {}
        self.read_receipts: List[ReadReceipt] = []
        self.homeworks: Dict[str, Homework] = {}
        self.attendance: List[AttendanceRecord] = []
        self.fee_reminders: List[FeeReminder] = []
        self.conversations: Dict[str, Conversation] = {}
        self.messages: List[Message] = []
        self.approval_requests: Dict[str, ApprovalRequest] = {}
        self.audit_log: List[AuditEntry] = []
        self._seed_pilot_data()

    def _seed_pilot_data(self):
        """Seed authentic data matching Case 111 specifications."""
        self.schools = {}
        self.sections = {}
        self.users = {}
        self.students = {}
        self.notices = {}
        self.read_receipts = []
        self.homeworks = {}
        self.attendance = []
        self.fee_reminders = []
        self.conversations = {}
        self.messages = []
        self.approval_requests = {}
        self.audit_log = []

        # Base timestamp inside school hours (10:30 AM)
        base_time = datetime.now().replace(hour=10, minute=30, second=0, microsecond=0) - timedelta(days=2)

        # 1. Pilot Schools (2 schools in pilot)
        s1 = School(school_id="SCH-01", name="St. Mary's Convent School", principal_id="USR-PRIN-01", address="Camp Road, Pune")
        s2 = School(school_id="SCH-02", name="Delhi Public Academy", principal_id="USR-PRIN-02", address="Kalyani Nagar, Pune")
        self.schools[s1.school_id] = s1
        self.schools[s2.school_id] = s2

        # 2. Staff & Management Users
        # Principals
        prin1 = User("USR-PRIN-01", "Dr. Anil Menon (Principal)", Role.PRINCIPAL, "SCH-01", "principal@stmarys.edu", "9820011111")
        prin2 = User("USR-PRIN-02", "Sister Theresa", Role.PRINCIPAL, "SCH-02", "principal@dpa.edu", "9820022222")
        self.users[prin1.user_id] = prin1
        self.users[prin2.user_id] = prin2

        # School Admins
        admin1 = User("USR-ADM-01", "Sunita Rao (Admin)", Role.SCHOOL_ADMIN, "SCH-01", "admin@stmarys.edu", "9820033333")
        admin2 = User("USR-ADM-02", "Manoj Kadam (Admin)", Role.SCHOOL_ADMIN, "SCH-02", "admin@dpa.edu", "9820044444")
        self.users[admin1.user_id] = admin1
        self.users[admin2.user_id] = admin2

        # Group Management
        mgmt = User("USR-MGMT-01", "K. V. Raman (Group Director)", Role.MANAGEMENT, "SCH-01", "director@schoolgroup.org", "9820055555")
        self.users[mgmt.user_id] = mgmt

        # Teachers (Rahul Deshmukh & Priya Sen)
        t1 = User("USR-TCH-01", "Rahul Deshmukh (Maths)", Role.TEACHER, "SCH-01", "rahul.d@stmarys.edu", "9820066666", mapped_section_ids=["SEC-5A", "SEC-7B"])
        t2 = User("USR-TCH-02", "Priya Sen (Science)", Role.TEACHER, "SCH-01", "priya.s@stmarys.edu", "9820077777", mapped_section_ids=["SEC-5B"])
        self.users[t1.user_id] = t1
        self.users[t2.user_id] = t2

        # 3. Class Sections
        sec_5a = ClassSection("SEC-5A", "SCH-01", "5", "A", t1.user_id)
        sec_5b = ClassSection("SEC-5B", "SCH-01", "5", "B", t2.user_id)
        sec_7b = ClassSection("SEC-7B", "SCH-01", "7", "B", t1.user_id)
        self.sections[sec_5a.section_id] = sec_5a
        self.sections[sec_5b.section_id] = sec_5b
        self.sections[sec_7b.section_id] = sec_7b

        # 4. Parents & Students (Seeding 10 parents in Class 5A for Read Receipts 60% verification)
        # Primary Persona: Meena Kulkarni
        p1 = User("USR-PAR-01", "Meena Kulkarni", Role.PARENT, "SCH-01", "meena.k@gmail.com", "9821100001", device_token="TOKEN-MEENA", children_ids=["STU-01"])
        stu1 = Student("STU-01", "Aarav Kulkarni", "SEC-5A", "SCH-01", parent_ids=[p1.user_id], roll_number=1)
        self.users[p1.user_id] = p1
        self.students[stu1.student_id] = stu1

        # Additional 9 Class 5A students and parents
        parent_names = [
            ("Vikram Sharma", "Sneha Sharma", "9821100002"),
            ("Rajesh Gupta", "Aditya Gupta", "9821100003"),
            ("Anita Desai", "Tanvi Desai", "9821100004"),
            ("Suresh Patil", "Rohan Patil", "9821100005"),
            ("Pooja Joshi", "Isha Joshi", "9821100006"),
            ("Nitin Shinde", "Varun Shinde", "9821100007"),
            ("Kavita Nair", "Arjun Nair", "9821100008"),
            ("Amit Verma", "Diya Verma", "9821100009"),
            ("Farhan Khan", "Zoya Khan", "9821100010"),
        ]

        for idx, (p_name, s_name, phone) in enumerate(parent_names, start=2):
            p_id = f"USR-PAR-{idx:02d}"
            s_id = f"STU-{idx:02d}"
            par = User(p_id, p_name, Role.PARENT, "SCH-01", f"{p_name.lower().replace(' ', '.')}@mail.com", phone, device_token=f"TOKEN-{idx}", children_ids=[s_id])
            stu = Student(s_id, s_name, "SEC-5A", "SCH-01", parent_ids=[p_id], roll_number=idx)
            self.users[p_id] = par
            self.students[s_id] = stu

        # 5. Seed Conversation between Meena Kulkarni and Rahul Deshmukh
        conv1 = Conversation(conversation_id="CONV-01", student_id="STU-01", parent_id=p1.user_id, teacher_id=t1.user_id, section_id="SEC-5A")
        self.conversations[conv1.conversation_id] = conv1

        # Seed initial greeting message
        msg1 = Message(
            message_id="MSG-01",
            conversation_id=conv1.conversation_id,
            sender_id=t1.user_id,
            sender_name=t1.name,
            sender_role=Role.TEACHER,
            recipient_id=p1.user_id,
            recipient_name=p1.name,
            body="Welcome to the Class 5A official diary thread for Aarav. Please let me know if you have questions.",
            urgent=False,
            status=MessageStatus.READ,
            created_at=base_time,
            delivered_at=base_time,
            read_at=base_time + timedelta(minutes=15)
        )
        self.messages.append(msg1)

        # 6. Seed Sample Notices
        n1 = Notice(
            notice_id="NOT-01",
            school_id="SCH-01",
            title="Class 5A: Term 1 Mathematics Unit Assessment",
            body="The first unit assessment for Mathematics (Fractions & Decimals) will be conducted on Friday. Please review chapters 3 & 4.",
            scope=NoticeScope.CLASS,
            created_by=t1.user_id,
            author_name=t1.name,
            created_at=datetime.now() - timedelta(days=1),
            status=NoticeStatus.PUBLISHED,
            section_id="SEC-5A",
            attachment_name="Maths_Syllabus_Class5.pdf"
        )
        self.notices[n1.notice_id] = n1

        # Seed Read Receipts: 6 of 10 parents have opened it (yielding exactly 60% read rate for TC-03)
        for i in range(1, 11):
            p_id = f"USR-PAR-{i:02d}"
            par = self.users[p_id]
            is_read = i <= 6  # First 6 read it
            self.read_receipts.append(ReadReceipt(
                notice_id=n1.notice_id,
                parent_id=p_id,
                parent_name=par.name,
                delivered_at=datetime.now() - timedelta(hours=20),
                read_at=datetime.now() - timedelta(hours=18) if is_read else None,
                state="READ" if is_read else "DELIVERED"
            ))

        # 7. Seed Sample Homework
        hw1 = Homework(
            homework_id="HW-01",
            section_id="SEC-5A",
            subject="Mathematics",
            title="Exercise 4.2 - Fractions Simplification",
            description="Solve questions 1 through 10 from page 48 in the textbook. Ensure all working steps are shown.",
            due_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            created_by=t1.user_id,
            created_at=datetime.now() - timedelta(hours=8),
            acknowledged_by=[p1.user_id]  # Meena already acknowledged
        )
        self.homeworks[hw1.homework_id] = hw1

        # 8. Seed Fee Reminders (Read-only, strictly no payment)
        fee1 = FeeReminder(
            reminder_id="FEE-01",
            student_id="STU-01",
            student_name="Aarav Kulkarni",
            parent_id=p1.user_id,
            due_date=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            amount=8500.0,
            description="Term 2 Tuition & Activity Fee (Reminders only — School does not accept payments online)",
            days_before=7,
            sent_at=datetime.now() - timedelta(days=1)
        )
        self.fee_reminders.append(fee1)

        # 9. Seed Audit Log Entry
        self.audit_log.append(AuditEntry(
            entry_id="AUD-01",
            actor_id=t1.user_id,
            actor_name=t1.name,
            actor_role=Role.TEACHER,
            action="PUBLISH_NOTICE",
            target_id=n1.notice_id,
            school_id="SCH-01",
            occurred_at=datetime.now() - timedelta(days=1),
            metadata={"title": n1.title, "scope": n1.scope.value}
        ))


# Singleton instance for the application
db = DataStore()
