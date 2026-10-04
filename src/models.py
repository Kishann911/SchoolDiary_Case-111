"""
SchoolDiary Domain Data Models
Reflects UML Class Diagram (02_UML_Design.md) and SRS Data Concepts (01_SRS_and_Priorities.md).
"""

from dataclasses import dataclass, field
from datetime import datetime, time
from enum import Enum
from typing import List, Optional, Dict, Any


class Role(str, Enum):
    PARENT = "PARENT"
    TEACHER = "TEACHER"
    SCHOOL_ADMIN = "SCHOOL_ADMIN"
    PRINCIPAL = "PRINCIPAL"
    MANAGEMENT = "MANAGEMENT"


class NoticeScope(str, Enum):
    CLASS = "CLASS"
    SCHOOL = "SCHOOL"


class NoticeStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    QUEUED = "QUEUED"
    PUBLISHED = "PUBLISHED"
    REJECTED = "REJECTED"


class MessageStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    QUEUED = "QUEUED"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    READ = "READ"
    FAILED = "FAILED"
    RECEIVED_AFTER_HOURS = "RECEIVED_AFTER_HOURS"
    AUTO_REPLIED = "AUTO_REPLIED"
    HELD_FOR_TEACHER = "HELD_FOR_TEACHER"
    DELIVERED_TO_TEACHER = "DELIVERED_TO_TEACHER"


class PolicyDecision(str, Enum):
    ALLOW = "ALLOW"
    QUEUE_FOR_0700 = "QUEUE_FOR_0700"
    NEEDS_PRINCIPAL_APPROVAL = "NEEDS_PRINCIPAL_APPROVAL"
    HOLD_FOR_TEACHER = "HOLD_FOR_TEACHER"


@dataclass
class User:
    user_id: str
    name: str
    role: Role
    school_id: str
    email: str
    phone: str
    device_token: str = ""
    # Scoping attributes
    mapped_section_ids: List[str] = field(default_factory=list)  # for teachers
    children_ids: List[str] = field(default_factory=list)         # for parents

    @property
    def masked_contact(self) -> str:
        """Mask phone number for parent-teacher privacy (NFR-04)."""
        if len(self.phone) >= 10:
            return self.phone[:3] + "XXXX-XX" + self.phone[-2:]
        return "XXXX-XXXX"


@dataclass
class Student:
    student_id: str
    name: str
    section_id: str
    school_id: str
    parent_ids: List[str] = field(default_factory=list)
    roll_number: int = 1


@dataclass
class ClassSection:
    section_id: str
    school_id: str
    grade: str
    division: str
    class_teacher_id: str

    @property
    def display_name(self) -> str:
        return f"Class {self.grade}{self.division}"


@dataclass
class School:
    school_id: str
    name: str
    principal_id: str
    address: str = ""


@dataclass
class ReadReceipt:
    notice_id: str
    parent_id: str
    parent_name: str
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    state: str = "DELIVERED"  # DELIVERED or READ


@dataclass
class Notice:
    notice_id: str
    school_id: str
    title: str
    body: str
    scope: NoticeScope
    created_by: str
    author_name: str
    created_at: datetime
    status: NoticeStatus = NoticeStatus.DRAFT
    section_id: Optional[str] = None
    attachment_name: Optional[str] = None
    publish_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None


@dataclass
class Homework:
    homework_id: str
    section_id: str
    subject: str
    title: str
    description: str
    due_date: str  # YYYY-MM-DD
    created_by: str
    created_at: datetime
    acknowledged_by: List[str] = field(default_factory=list)  # parent_ids


@dataclass
class AttendanceRecord:
    record_id: str
    student_id: str
    student_name: str
    section_id: str
    date: str  # YYYY-MM-DD
    status: str  # PRESENT or ABSENT
    roll_call_at: datetime
    alert_sent_at: Optional[datetime] = None


@dataclass
class FeeReminder:
    reminder_id: str
    student_id: str
    student_name: str
    parent_id: str
    due_date: str  # YYYY-MM-DD
    amount: float
    description: str
    days_before: int  # 7 or 1
    sent_at: datetime


@dataclass
class Message:
    message_id: str
    conversation_id: str
    sender_id: str
    sender_name: str
    sender_role: Role
    recipient_id: str
    recipient_name: str
    body: str
    urgent: bool
    status: MessageStatus
    created_at: datetime
    scheduled_for: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None


@dataclass
class Conversation:
    conversation_id: str
    student_id: str
    parent_id: str
    teacher_id: str
    section_id: str


@dataclass
class ApprovalRequest:
    request_id: str
    school_id: str
    target_type: str  # NOTICE or MESSAGE
    target_id: str
    requester_id: str
    requester_name: str
    approver_role: Role  # SCHOOL_ADMIN for school notices, PRINCIPAL for urgent messages
    state: str = "PENDING"  # PENDING, APPROVED, REJECTED
    requested_at: datetime = field(default_factory=datetime.now)
    decided_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None


@dataclass
class AuditEntry:
    entry_id: str
    actor_id: str
    actor_name: str
    actor_role: Role
    action: str
    target_id: str
    school_id: str
    occurred_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
