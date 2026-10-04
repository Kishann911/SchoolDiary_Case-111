"""
SchoolDiary Data Store and Seeding Engine
Pre-seeded with rich, realistic mock data for 2 pilot schools, multiple classrooms,
faculty, parents, multi-message chat threads, and approval queues.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

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
        """Seed comprehensive pilot data matching Case 111 specifications."""
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

        now = datetime.now()
        in_window_time = now.replace(hour=10, minute=30, second=0, microsecond=0)

        # ── 1. PILOT SCHOOLS (2 Schools) ──
        s1 = School("SCH-01", "St. Mary's Convent School", "USR-PRIN-01", "Camp Road, Pune")
        s2 = School("SCH-02", "Delhi Public Academy", "USR-PRIN-02", "Kalyani Nagar, Pune")
        self.schools[s1.school_id] = s1
        self.schools[s2.school_id] = s2

        # ── 2. EXECUTIVE, ADMINISTRATIVE & FACULTY USERS ──
        prin1 = User("USR-PRIN-01", "Dr. Anil Menon (Principal)", Role.PRINCIPAL, "SCH-01", "principal@stmarys.edu", "9820011111")
        prin2 = User("USR-PRIN-02", "Sister Theresa (Principal)", Role.PRINCIPAL, "SCH-02", "principal@dpa.edu", "9820022222")
        self.users[prin1.user_id] = prin1
        self.users[prin2.user_id] = prin2

        admin1 = User("USR-ADM-01", "Sunita Rao (School Admin)", Role.SCHOOL_ADMIN, "SCH-01", "admin@stmarys.edu", "9820033333")
        admin2 = User("USR-ADM-02", "Manoj Kadam (School Admin)", Role.SCHOOL_ADMIN, "SCH-02", "admin@dpa.edu", "9820044444")
        self.users[admin1.user_id] = admin1
        self.users[admin2.user_id] = admin2

        mgmt = User("USR-MGMT-01", "K. V. Raman (Group Director)", Role.MANAGEMENT, "SCH-01", "director@schoolgroup.org", "9820055555")
        self.users[mgmt.user_id] = mgmt

        t1 = User("USR-TCH-01", "Rahul Deshmukh (Maths)", Role.TEACHER, "SCH-01", "rahul.d@stmarys.edu", "9820066666", mapped_section_ids=["SEC-5A", "SEC-7B"])
        t2 = User("USR-TCH-02", "Priya Sen (Science)", Role.TEACHER, "SCH-01", "priya.s@stmarys.edu", "9820077777", mapped_section_ids=["SEC-5B"])
        t3 = User("USR-TCH-03", "Kavita Iyer (English)", Role.TEACHER, "SCH-01", "kavita.i@stmarys.edu", "9820088888", mapped_section_ids=["SEC-7A"])
        t4 = User("USR-TCH-04", "Rajesh Verma (Social Studies)", Role.TEACHER, "SCH-01", "rajesh.v@stmarys.edu", "9820099999", mapped_section_ids=["SEC-8A"])
        self.users[t1.user_id] = t1
        self.users[t2.user_id] = t2
        self.users[t3.user_id] = t3
        self.users[t4.user_id] = t4

        # ── 3. CLASSROOM SECTIONS ──
        sec_5a = ClassSection("SEC-5A", "SCH-01", "5", "A", t1.user_id)
        sec_5b = ClassSection("SEC-5B", "SCH-01", "5", "B", t2.user_id)
        sec_7a = ClassSection("SEC-7A", "SCH-01", "7", "A", t3.user_id)
        sec_7b = ClassSection("SEC-7B", "SCH-01", "7", "B", t1.user_id)
        sec_8a = ClassSection("SEC-8A", "SCH-01", "8", "A", t4.user_id)
        self.sections[sec_5a.section_id] = sec_5a
        self.sections[sec_5b.section_id] = sec_5b
        self.sections[sec_7a.section_id] = sec_7a
        self.sections[sec_7b.section_id] = sec_7b
        self.sections[sec_8a.section_id] = sec_8a

        # ── 4. PARENTS & STUDENTS (CLASS 5A COHORT) ──
        # Primary Persona: Meena Kulkarni (Nurse, Aarav's mother)
        p1 = User("USR-PAR-01", "Meena Kulkarni", Role.PARENT, "SCH-01", "meena.kulkarni@gmail.com", "9821100001", device_token="TOKEN-MEENA", children_ids=["STU-01"])
        stu1 = Student("STU-01", "Aarav Kulkarni", "SEC-5A", "SCH-01", parent_ids=[p1.user_id], roll_number=1)
        self.users[p1.user_id] = p1
        self.students[stu1.student_id] = stu1

        # Additional 9 Class 5A Students & Parents (Giving exactly 10 parents for TC-03 test)
        class5a_cohort = [
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

        for idx, (p_name, s_name, phone) in enumerate(class5a_cohort, start=2):
            p_id = f"USR-PAR-{idx:02d}"
            s_id = f"STU-{idx:02d}"
            par = User(p_id, p_name, Role.PARENT, "SCH-01", f"{p_name.lower().replace(' ', '.')}@mail.com", phone, device_token=f"TOKEN-{idx}", children_ids=[s_id])
            stu = Student(s_id, s_name, "SEC-5A", "SCH-01", parent_ids=[p_id], roll_number=idx)
            self.users[p_id] = par
            self.students[s_id] = stu

        # Additional Class 7B Students & Parents (for Class Teacher Rahul Deshmukh's second class)
        class7b_cohort = [
            ("Devendra More", "Yash More", "9821200001"),
            ("Sunil Jadhav", "Aniket Jadhav", "9821200002"),
            ("Rekha Bhatt", "Pooja Bhatt", "9821200003"),
            ("Girish Kulkarni", "Aditi Kulkarni", "9821200004"),
        ]
        for idx, (p_name, s_name, phone) in enumerate(class7b_cohort, start=11):
            p_id = f"USR-PAR-{idx:02d}"
            s_id = f"STU-{idx:02d}"
            par = User(p_id, p_name, Role.PARENT, "SCH-01", f"{p_name.lower().replace(' ', '.')}@mail.com", phone, device_token=f"TOKEN-{idx}", children_ids=[s_id])
            stu = Student(s_id, s_name, "SEC-7B", "SCH-01", parent_ids=[p_id], roll_number=idx - 10)
            self.users[p_id] = par
            self.students[s_id] = stu

        # ── 5. SEED ACTIVE CONVERSATION & RICH CHAT HISTORY ──
        conv1 = Conversation("CONV-01", "STU-01", p1.user_id, t1.user_id, "SEC-5A")
        self.conversations[conv1.conversation_id] = conv1

        seed_dialogue = [
            (t1, p1, "Welcome to the Class 5A official diary thread for Aarav. Please feel free to message if you have any academic queries or concerns.", 4, 10, 15),
            (p1, t1, "Good morning Sir. Aarav was feeling unwell on Wednesday with mild seasonal fever. Does he require a formal doctor's certificate for the 2 days missed?", 3, 11, 20),
            (t1, p1, "A written note in this app is sufficient for up to two days. Please ensure he catches up on the Mathematics fractions notes from Sneha or Vikram.", 3, 11, 45),
            (p1, t1, "Thank you, Sir. He has copied the fractions notes and completed questions 1 to 5 from Exercise 4.2.", 2, 9, 30),
            (t1, p1, "Excellent! I reviewed his notebook during zero period today; his simplification steps were very neat and accurate.", 2, 10, 50),
            (p1, t1, "Sir, what time will the bus drop him tomorrow after the remedial mathematics session?", 1, 16, 40),
            (t1, p1, "The remedial bus departs campus at 4:30 PM. He should reach your society entrance gate at approximately 4:55 PM.", 1, 17, 10),
        ]

        for sdr, rcpt, body, days_ago, hr, mn in seed_dialogue:
            msg_dt = now.replace(hour=hr, minute=mn, second=0, microsecond=0) - timedelta(days=days_ago)
            self.messages.append(Message(
                message_id=f"MSG-{len(self.messages)+1:02d}",
                conversation_id=conv1.conversation_id,
                sender_id=sdr.user_id,
                sender_name=sdr.name,
                sender_role=sdr.role,
                recipient_id=rcpt.user_id,
                recipient_name=rcpt.name,
                body=body,
                urgent=False,
                status=MessageStatus.READ,
                created_at=msg_dt,
                delivered_at=msg_dt + timedelta(seconds=2),
                read_at=msg_dt + timedelta(minutes=5)
            ))

        # ── 6. SEED CIRCULARS & NOTICES (CLASS & SCHOOL-WIDE) ──
        # Notice 1: Class 5A Math Quiz (Published, 6 of 10 read = 60% for TC-03)
        n1 = Notice(
            notice_id="NOT-01",
            school_id="SCH-01",
            title="Class 5A: Term 1 Mathematics Unit Assessment",
            body="The first unit assessment for Mathematics (Fractions & Decimals) will be conducted on Friday. Please review chapters 3 & 4. Calculators are strictly prohibited.",
            scope=NoticeScope.CLASS,
            created_by=t1.user_id,
            author_name=t1.name,
            created_at=in_window_time - timedelta(days=2),
            status=NoticeStatus.PUBLISHED,
            section_id="SEC-5A",
            attachment_name="Maths_Syllabus_Class5.pdf",
            publish_at=in_window_time - timedelta(days=2)
        )
        self.notices[n1.notice_id] = n1

        # Seed read receipts for NOT-01: 6 of 10 parents have opened it (60.0% read rate)
        for i in range(1, 11):
            p_id = f"USR-PAR-{i:02d}"
            par = self.users[p_id]
            is_read = (i <= 6)
            self.read_receipts.append(ReadReceipt(
                notice_id=n1.notice_id,
                parent_id=p_id,
                parent_name=par.name,
                delivered_at=in_window_time - timedelta(days=2),
                read_at=(in_window_time - timedelta(days=2, hours=-2)) if is_read else None,
                state="READ" if is_read else "DELIVERED"
            ))

        # Notice 2: School-wide Sports Meet (Published)
        n2 = Notice(
            notice_id="NOT-02",
            school_id="SCH-01",
            title="Annual Inter-School Athletics & Sports Meet 2026",
            body="We are pleased to announce the 32nd Annual Inter-School Sports Meet on October 24-25. Parents are cordially invited to the opening ceremony at 08:30 AM at the Main Sports Complex.",
            scope=NoticeScope.SCHOOL,
            created_by=admin1.user_id,
            author_name=admin1.name,
            created_at=in_window_time - timedelta(days=4),
            status=NoticeStatus.PUBLISHED,
            attachment_name="Sports_Meet_Event_Schedule.pdf",
            publish_at=in_window_time - timedelta(days=4)
        )
        self.notices[n2.notice_id] = n2

        # Notice 3: Monsoon Advisory (Published)
        n3 = Notice(
            notice_id="NOT-03",
            school_id="SCH-01",
            title="Monsoon Advisory: Rain Contingency & School Bus Schedules",
            body="Due to continuous rainfall forecasts in Pune district, all morning pickup routes will operate 10 minutes earlier than scheduled. Please ensure your child is at the designated bus stop on time.",
            scope=NoticeScope.SCHOOL,
            created_by=admin1.user_id,
            author_name=admin1.name,
            created_at=in_window_time - timedelta(days=1),
            status=NoticeStatus.PUBLISHED,
            attachment_name="Bus_Routes_Monsoon_2026.pdf",
            publish_at=in_window_time - timedelta(days=1)
        )
        self.notices[n3.notice_id] = n3

        # Notice 4: Science Exhibition (PENDING APPROVAL -> shows in Admin Queue!)
        n4 = Notice(
            notice_id="NOT-04",
            school_id="SCH-01",
            title="Inter-Branch Science & Robotics Exhibition Showcase",
            body="Faculty proposal to host an inter-branch STEM & Robotics project competition for grades 5 through 10. External evaluators from College of Engineering Pune will judge entries.",
            scope=NoticeScope.SCHOOL,
            created_by=t1.user_id,
            author_name=t1.name,
            created_at=in_window_time - timedelta(hours=3),
            status=NoticeStatus.PENDING_APPROVAL,
            attachment_name="STEM_Exhibition_Proposal.pdf"
        )
        self.notices[n4.notice_id] = n4

        # Request for Admin approval
        req1 = ApprovalRequest(
            request_id="REQ-01",
            school_id="SCH-01",
            target_type="NOTICE",
            target_id=n4.notice_id,
            requester_id=t1.user_id,
            requester_name=t1.name,
            approver_role=Role.SCHOOL_ADMIN,
            requested_at=in_window_time - timedelta(hours=3)
        )
        self.approval_requests[req1.request_id] = req1

        # Notice 5: Diwali Break Schedule (PENDING APPROVAL -> shows in Admin Queue!)
        n5 = Notice(
            notice_id="NOT-05",
            school_id="SCH-01",
            title="Diwali Vacation Schedule & Term 1 Report Card Distribution",
            body="The school will remain closed for Diwali break from November 1 to November 14. Term 1 progress cards will be handed over during the mandatory Parent-Teacher Meeting on October 31.",
            scope=NoticeScope.SCHOOL,
            created_by=t2.user_id,
            author_name=t2.name,
            created_at=in_window_time - timedelta(hours=1),
            status=NoticeStatus.PENDING_APPROVAL,
            attachment_name="Diwali_PTM_Schedule.pdf"
        )
        self.notices[n5.notice_id] = n5

        req2 = ApprovalRequest(
            request_id="REQ-02",
            school_id="SCH-01",
            target_type="NOTICE",
            target_id=n5.notice_id,
            requester_id=t2.user_id,
            requester_name=t2.name,
            approver_role=Role.SCHOOL_ADMIN,
            requested_at=in_window_time - timedelta(hours=1)
        )
        self.approval_requests[req2.request_id] = req2

        # ── 7. SEED PENDING URGENT MESSAGE REQUEST (FOR PRINCIPAL QUEUE) ──
        # Urgent emergency message submitted by teacher outside hours (20:30 IST)
        urgent_msg = Message(
            message_id="MSG-URG-01",
            conversation_id="CONV-01",
            sender_id=t1.user_id,
            sender_name=t1.name,
            sender_role=Role.TEACHER,
            recipient_id=p1.user_id,
            recipient_name=p1.name,
            body="Urgent Transport Alert: School Bus #4 experienced a radiator leakage on Sinhagad Road. All 18 pupils are safe and transfer to backup bus #9 is complete. Estimated arrival delay is 25 minutes.",
            urgent=True,
            status=MessageStatus.PENDING_APPROVAL,
            created_at=now.replace(hour=20, minute=30, second=0, microsecond=0)
        )
        self.messages.append(urgent_msg)

        req_urgent = ApprovalRequest(
            request_id="REQ-03",
            school_id="SCH-01",
            target_type="MESSAGE",
            target_id=urgent_msg.message_id,
            requester_id=t1.user_id,
            requester_name=t1.name,
            approver_role=Role.PRINCIPAL,
            requested_at=urgent_msg.created_at
        )
        self.approval_requests[req_urgent.request_id] = req_urgent

        # ── 8. SEED HOMEWORK ASSIGNMENTS ACROSS SUBJECTS ──
        hw1 = Homework(
            homework_id="HW-01",
            section_id="SEC-5A",
            subject="Mathematics",
            title="Exercise 4.2: Fractions Simplification & Decimals",
            description="Solve questions 1 through 10 on page 48 in the NCERT Mathematics textbook. Show all intermediate prime factorisation and reduction steps.",
            due_date=(now + timedelta(days=1)).strftime("%Y-%m-%d"),
            created_by=t1.user_id,
            created_at=now - timedelta(hours=6),
            acknowledged_by=[p1.user_id, "USR-PAR-02", "USR-PAR-03"]
        )
        hw2 = Homework(
            homework_id="HW-02",
            section_id="SEC-5A",
            subject="Science",
            title="Human Digestive System: Diagram with Color-Coded Labels",
            description="Draw a neat, fully labeled diagram of the human alimentary canal in your science practical workbook. Highlight salivary glands, stomach, liver, and intestines.",
            due_date=(now + timedelta(days=2)).strftime("%Y-%m-%d"),
            created_by=t1.user_id,
            created_at=now - timedelta(hours=4),
            acknowledged_by=[p1.user_id]
        )
        hw3 = Homework(
            homework_id="HW-03",
            section_id="SEC-5A",
            subject="English",
            title="Creative Composition: 'A Memorable Rainy Morning in Pune'",
            description="Write a 150-to-200-word descriptive essay describing the sight, sounds, and experience of a monsoon morning. Pay attention to adjectives and past tense verbs.",
            due_date=(now + timedelta(days=4)).strftime("%Y-%m-%d"),
            created_by=t1.user_id,
            created_at=now - timedelta(hours=2),
            acknowledged_by=[]
        )
        hw4 = Homework(
            homework_id="HW-04",
            section_id="SEC-5A",
            subject="Social Studies",
            title="Map Work: States, Capitals, and Major Rivers of Southern India",
            description="Locate and shade the states of Maharashtra, Karnataka, Telangana, and Tamil Nadu on the political outline map. Mark rivers Godavari, Krishna, and Cauvery.",
            due_date=(now + timedelta(days=5)).strftime("%Y-%m-%d"),
            created_by=t1.user_id,
            created_at=now - timedelta(hours=1),
            acknowledged_by=[]
        )
        self.homeworks[hw1.homework_id] = hw1
        self.homeworks[hw2.homework_id] = hw2
        self.homeworks[hw3.homework_id] = hw3
        self.homeworks[hw4.homework_id] = hw4

        # ── 9. SEED ATTENDANCE HISTORY (WITH 15-MIN ABSENCE ALERT) ──
        # Oct 1 (Present)
        self.attendance.append(AttendanceRecord(
            "ATT-01", "STU-01", "Aarav Kulkarni", "SEC-5A",
            (now - timedelta(days=4)).strftime("%Y-%m-%d"),
            "PRESENT", now.replace(hour=8, minute=52) - timedelta(days=4)
        ))
        # Oct 3 (ABSENT with 15-minute alert timestamp)
        absent_time = now.replace(hour=8, minute=55) - timedelta(days=2)
        alert_time = now.replace(hour=9, minute=10) - timedelta(days=2)
        self.attendance.append(AttendanceRecord(
            "ATT-02", "STU-01", "Aarav Kulkarni", "SEC-5A",
            (now - timedelta(days=2)).strftime("%Y-%m-%d"),
            "ABSENT", absent_time, alert_time
        ))
        # Oct 4 (Present)
        self.attendance.append(AttendanceRecord(
            "ATT-03", "STU-01", "Aarav Kulkarni", "SEC-5A",
            (now - timedelta(days=1)).strftime("%Y-%m-%d"),
            "PRESENT", now.replace(hour=8, minute=50) - timedelta(days=1)
        ))
        # Today (Present)
        self.attendance.append(AttendanceRecord(
            "ATT-04", "STU-01", "Aarav Kulkarni", "SEC-5A",
            now.strftime("%Y-%m-%d"),
            "PRESENT", now.replace(hour=8, minute=48)
        ))

        # ── 10. SEED FEE REMINDERS (NO PAYMENT IN APP) ──
        self.fee_reminders.append(FeeReminder(
            "FEE-01", "STU-01", "Aarav Kulkarni", p1.user_id,
            (now + timedelta(days=7)).strftime("%Y-%m-%d"),
            8500.0,
            "Term 2 Tuition & Activity Fee (Reminders only — School does not accept payments online)",
            7, now - timedelta(days=1)
        ))
        self.fee_reminders.append(FeeReminder(
            "FEE-02", "STU-01", "Aarav Kulkarni", p1.user_id,
            (now + timedelta(days=1)).strftime("%Y-%m-%d"),
            1200.0,
            "Annual Computer Lab & Digital Resource Subscription (Due Tomorrow)",
            1, now - timedelta(hours=4)
        ))
        self.fee_reminders.append(FeeReminder(
            "FEE-03", "STU-01", "Aarav Kulkarni", p1.user_id,
            (now + timedelta(days=20)).strftime("%Y-%m-%d"),
            2400.0,
            "Annual Inter-School Sports Kit & Athletics Uniform Fee",
            20, now - timedelta(days=3)
        ))

        # ── 11. SEED AUDIT LOG ENTRIES ──
        audit_events = [
            (admin1, "PUBLISH_NOTICE", n2.notice_id, "Published Annual Sports Meet Circular"),
            (t1, "SUBMIT_NOTICE", n1.notice_id, "Composed Class 5A Math Quiz Circular"),
            (t1, "SUBMIT_ATTENDANCE", "SEC-5A", "Submitted Daily Attendance Roll Call (1 pupil absent)"),
            (t1, "POST_HOMEWORK", hw1.homework_id, "Published Math Exercise 4.2 assignment"),
            (p1, "ACKNOWLEDGE_HOMEWORK", hw1.homework_id, "Parent acknowledged Math homework"),
            (t1, "SUBMIT_NOTICE", n4.notice_id, "Submitted Science Exhibition notice for approval"),
            (t2, "SUBMIT_NOTICE", n5.notice_id, "Submitted Diwali Vacation notice for approval"),
            (t1, "SEND_URGENT_MESSAGE", urgent_msg.message_id, "Dispatched emergency bus delay request"),
        ]
        for idx, (actor, act, target, note) in enumerate(audit_events, start=1):
            self.audit_log.append(AuditEntry(
                entry_id=f"AUD-{idx:02d}",
                actor_id=actor.user_id,
                actor_name=actor.name,
                actor_role=actor.role,
                action=act,
                target_id=target,
                school_id=actor.school_id,
                occurred_at=in_window_time - timedelta(hours=idx * 2),
                metadata={"details": note}
            ))


# Singleton instance
db = DataStore()
