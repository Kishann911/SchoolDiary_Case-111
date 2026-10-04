"""
MessagingPolicy Rules Engine (FR-08)
Pure rules engine governing sending window (07:00-19:59 IST), queueing, and approvals.
Stateless and isolated from I/O.
"""

from datetime import datetime, time, timedelta
from typing import Tuple, Optional
from src.models import Role, PolicyDecision, NoticeScope


class MessagingPolicy:
    """
    Stateless business policy for parent-teacher communication hours.
    All times operate in Indian Standard Time (IST) at minute granularity.
    """
    WINDOW_START: time = time(7, 0)    # 07:00 inclusive
    WINDOW_END: time = time(19, 59)   # 19:59 inclusive

    @classmethod
    def is_inside_window(cls, current_time: time) -> bool:
        """
        Check if time is within the teacher sending window: 07:00 to 19:59 inclusive.
        Handles minute granularity.
        """
        # Off-by-one safeguard: 19:59:59 is inside; 20:00:00 is outside.
        return cls.WINDOW_START <= current_time <= cls.WINDOW_END

    @classmethod
    def can_send_now(
        cls,
        role: Role,
        check_time: time,
        urgent: bool = False,
        principal_approved: Optional[bool] = None
    ) -> PolicyDecision:
        """
        Evaluate if a message can be dispatched immediately.
        Implements Decision Table rules R1 through R7.
        """
        in_window = cls.is_inside_window(check_time)

        if role == Role.TEACHER:
            if in_window:
                # Rule R1: Teacher in window -> Send now
                return PolicyDecision.ALLOW
            else:
                # Outside window (20:00 to 06:59)
                if not urgent:
                    # Rule R2: Routine message -> Queue for 07:00
                    return PolicyDecision.QUEUE_FOR_0700
                else:
                    # Urgent message outside window
                    if principal_approved is True:
                        # Rule R4: Principal approved -> Send now
                        return PolicyDecision.ALLOW
                    elif principal_approved is False:
                        # Rule R5: Principal rejected or timeout -> Queue for 07:00
                        return PolicyDecision.QUEUE_FOR_0700
                    else:
                        # Rule R3: Pending decision -> Request approval
                        return PolicyDecision.NEEDS_PRINCIPAL_APPROVAL

        elif role == Role.PARENT:
            if in_window:
                # Rule R6: Parent in window -> Delivered immediately
                return PolicyDecision.ALLOW
            else:
                # Rule R7: Parent outside window -> Hold for teacher until 07:00 & auto-reply
                return PolicyDecision.HOLD_FOR_TEACHER

        elif role in (Role.SCHOOL_ADMIN, Role.PRINCIPAL):
            # Administrative broadcasts follow sending window
            if in_window:
                return PolicyDecision.ALLOW
            else:
                return PolicyDecision.QUEUE_FOR_0700

        return PolicyDecision.ALLOW

    @classmethod
    def evaluate_notice_publishing(
        cls,
        scope: NoticeScope,
        author_role: Role,
        check_time: time,
        admin_approved: Optional[bool] = None
    ) -> PolicyDecision:
        """
        Evaluate if a circular notice can be published immediately.
        Implements Decision Table rules R8 through R13.
        """
        in_window = cls.is_inside_window(check_time)

        if scope == NoticeScope.CLASS:
            if in_window:
                # Rule R8: Class notice in window -> Publish now
                return PolicyDecision.ALLOW
            else:
                # Rule R9: Class notice outside window -> Queue for 07:00
                return PolicyDecision.QUEUE_FOR_0700

        elif scope == NoticeScope.SCHOOL:
            if author_role == Role.TEACHER:
                if admin_approved is True:
                    # Approved by admin -> check window
                    return PolicyDecision.ALLOW if in_window else PolicyDecision.QUEUE_FOR_0700
                elif admin_approved is False:
                    # Rule R13: Admin rejected -> Reject
                    return PolicyDecision.QUEUE_FOR_0700
                else:
                    # Rule R10: Teacher school notice -> Send to admin approval
                    return PolicyDecision.NEEDS_PRINCIPAL_APPROVAL
            elif author_role == Role.SCHOOL_ADMIN:
                # Rule R11 / R12: School Admin posting school notice
                return PolicyDecision.ALLOW if in_window else PolicyDecision.QUEUE_FOR_0700

        return PolicyDecision.ALLOW

    @classmethod
    def get_next_window_open(cls, dt: datetime) -> datetime:
        """
        Calculate next 07:00 release timestamp for queued items.
        Handles midnight rollover correctly without double queueing (DEF-35 safeguard).
        """
        # If currently between 00:00 and 06:59: release is today at 07:00
        if dt.time() < cls.WINDOW_START:
            return dt.replace(hour=7, minute=0, second=0, microsecond=0)
        # If currently >= 20:00: release is tomorrow at 07:00
        tomorrow = dt + timedelta(days=1)
        return tomorrow.replace(hour=7, minute=0, second=0, microsecond=0)

    @classmethod
    def get_parent_auto_reply_text(cls) -> str:
        """Standard automated response delivered to parents outside window."""
        return "Teachers reply between 07:00 and 20:00. For emergencies call the school office."
