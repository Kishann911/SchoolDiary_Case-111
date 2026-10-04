"""
SchoolDiary — Parent–Teacher Communication Platform (Case 111)
Interactive Streamlit Application implementing all 10 Functional Requirements (FR-01 to FR-10).
Sole Author: Kishan Ojha (@Kishann911)
"""

import streamlit as st
from datetime import datetime, time, timedelta
import pandas as pd

from src.models import (
    Role, NoticeScope, NoticeStatus, MessageStatus, PolicyDecision, User
)
from src.policy import MessagingPolicy
from src.database import db
from src.services import (
    NoticeService, ReadReceiptService, MessagingService,
    AttendanceService, HomeworkService, AdminService, AuditReportService, dispatcher
)

# ─── PAGE CONFIGURATION & BRUTALIST/MINIMALIST CSS ────────────────────────────
st.set_page_config(
    page_title="SchoolDiary · Parent-Teacher Communication",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    /* Minimalist typography & palette */
    :root {
        --navy: #1B2A4A;
        --coral: #E05A4E;
        --teal: #2D7D8E;
        --slate: #4A5568;
        --light-grey: #F7F9FC;
        --border-grey: #CBD5E0;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1B2A4A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4A5568;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background-color: #F7F9FC;
        border: 1px solid #CBD5E0;
        border-left: 4px solid #2D7D8E;
        padding: 14px 18px;
        border-radius: 6px;
        margin-bottom: 12px;
    }
    .status-badge-open {
        background-color: #E8F5E9;
        color: #2E7D32;
        border: 1px solid #A5D6A7;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .status-badge-closed {
        background-color: #FFEBEE;
        color: #C62828;
        border: 1px solid #FFCDD2;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .chat-bubble-teacher {
        background-color: #E8F1FB;
        border: 1px solid #CBD5E0;
        border-radius: 8px 8px 8px 0px;
        padding: 10px 14px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .chat-bubble-parent {
        background-color: #F7F9FC;
        border: 1px solid #CBD5E0;
        border-radius: 8px 8px 0px 8px;
        padding: 10px 14px;
        margin-bottom: 10px;
        margin-left: auto;
        max-width: 80%;
    }
    .auto-reply-box {
        background-color: #FFF9C4;
        border-left: 4px solid #FBC02D;
        padding: 10px 14px;
        border-radius: 4px;
        font-size: 0.9rem;
        margin-bottom: 10px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ─── SIDEBAR: CLOCK SIMULATOR & ROLE SWITCHER ────────────────────────────────
with st.sidebar:
    st.markdown("### 🏫 SchoolDiary Console")
    st.markdown("**Case #111 · Author: Kishan Ojha**")
    st.divider()

    # 1. Interactive Clock Simulator Toolbar
    st.markdown("#### ⏰ System Clock Control")
    use_simulation = st.checkbox("Override Current Clock", value=False, help="Enable to test out-of-hours boundaries (e.g., 20:00 vs 19:59)")
    
    if use_simulation:
        sim_col1, sim_col2 = st.columns(2)
        with sim_col1:
            hour_val = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=20)
        with sim_col2:
            min_val = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=5)
        active_time = time(hour_val, min_val)
        st.info(f"Mock Clock: **{active_time.strftime('%H:%M')} IST**")
    else:
        active_time = datetime.now().time()
        st.caption(f"Real Time: **{active_time.strftime('%H:%M:%S')} IST**")

    # Evaluate window status
    is_window_open = MessagingPolicy.is_inside_window(active_time)
    if is_window_open:
        st.markdown('<span class="status-badge-open">🟢 WINDOW OPEN (07:00–19:59 IST)</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge-closed">🔴 WINDOW CLOSED (20:00–06:59 IST)</span>', unsafe_allow_html=True)
        st.caption("Routine teacher messages will queue for 07:00 AM dispatch.")

    st.divider()

    # 2. Scoped Role Switcher
    st.markdown("#### 👤 Switch Active Persona")
    role_options = {
        "Parent (Meena Kulkarni)": ("USR-PAR-01", Role.PARENT),
        "Teacher (Rahul Deshmukh)": ("USR-TCH-01", Role.TEACHER),
        "School Admin (Sunita Rao)": ("USR-ADM-01", Role.SCHOOL_ADMIN),
        "Principal (Dr. Anil Menon)": ("USR-PRIN-01", Role.PRINCIPAL),
        "Management (Group Director)": ("USR-MGMT-01", Role.MANAGEMENT),
    }
    selected_role_label = st.selectbox("Current User Profile:", list(role_options.keys()))
    active_user_id, active_role = role_options[selected_role_label]
    current_user = db.users[active_user_id]

    st.caption(f"User ID: `{current_user.user_id}` | Role: `{current_user.role.value}`")
    st.caption(f"Institution: `{db.schools[current_user.school_id].name}`")

    st.divider()
    st.markdown("#### 📄 Key Metrics")
    st.markdown("- **Pilot Parents:** 2,300 (16.4%)")
    st.markdown("- **Effort:** 68 Person-Days")
    st.markdown("- **Schedule:** 27 Working Days")
    st.markdown("- **DRE Benchmark:** 94.4%")


# ─── HEADER BAR ───────────────────────────────────────────────────────────────
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown('<div class="main-title">SchoolDiary</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Parent–Teacher Communication Platform for School Groups (Case Study #111)</div>', unsafe_allow_html=True)
with header_col2:
    st.markdown(f"**Logged in as:** {current_user.name}")
    st.markdown(f"**Phone:** `{current_user.masked_contact}` *(Masked)*")

st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 1: PARENT PORTAL (MEENA KULKARNI)
# ══════════════════════════════════════════════════════════════════════════════
if current_user.role == Role.PARENT:
    child_id = current_user.children_ids[0]
    child = db.students[child_id]
    section = db.sections[child.section_id]
    teacher = db.users[section.class_teacher_id]

    st.markdown(f"### 👨‍👩‍👧 Parent Dashboard — Enrolled Student: **{child.name}** ({section.display_name})")

    p_tabs = st.tabs(["📢 Circulars & Notices", "📝 Homework", "🚨 Absence Alerts", "💳 Fee Reminders (No Pay)", "💬 Chat with Teacher"])

    # Tab 1: Notices
    with p_tabs[0]:
        st.markdown("#### Official Circulars & Notices")
        # Filter notices visible to student's section or whole school
        visible_notices = [
            n for n in db.notices.values()
            if n.status == NoticeStatus.PUBLISHED and (n.scope == NoticeScope.SCHOOL or n.section_id == section.section_id)
        ]
        if not visible_notices:
            st.info("No published circulars at this time.")
        else:
            for notif in visible_notices:
                with st.expander(f"📌 {notif.title} ({notif.scope.value} Notice)", expanded=True):
                    st.write(notif.body)
                    if notif.attachment_name:
                        st.caption(f"📎 Attachment: `{notif.attachment_name}`")
                    st.caption(f"Published by: {notif.author_name} at {notif.publish_at.strftime('%Y-%m-%d %H:%M') if notif.publish_at else ''}")
                    
                    # Mark read button
                    ReadReceiptService.mark_read(notif.notice_id, current_user.user_id)
                    st.success("✓ Delivered & Read status recorded")

    # Tab 2: Homework
    with p_tabs[1]:
        st.markdown(f"#### Class Assignments for {section.display_name}")
        hw_list = [h for h in db.homeworks.values() if h.section_id == section.section_id]
        if not hw_list:
            st.info("No pending homework.")
        else:
            for hw in hw_list:
                with st.container():
                    st.markdown(f"**{hw.subject}: {hw.title}**")
                    st.write(hw.description)
                    st.caption(f"Due Date: **{hw.due_date}**")
                    
                    is_ack = current_user.user_id in hw.acknowledged_by
                    if is_ack:
                        st.button("✓ Acknowledged", key=f"hw_{hw.homework_id}", disabled=True)
                    else:
                        if st.button("Acknowledge (Seen)", key=f"hw_ack_{hw.homework_id}"):
                            HomeworkService.acknowledge_homework(hw.homework_id, current_user.user_id)
                            st.rerun()
                    st.divider()

    # Tab 3: Attendance
    with p_tabs[2]:
        st.markdown("#### Automated Absence Alerts (15-Minute SLA)")
        child_att = [a for a in db.attendance if a.student_id == child.student_id]
        if not child_att:
            st.info("All roll-calls indicate present. No absence alerts recorded.")
        else:
            for att in reversed(child_att):
                if att.status == "ABSENT":
                    st.error(f"🚨 **ABSENCE ALERT:** {child.name} was marked absent on {att.date} at {att.roll_call_at.strftime('%H:%M IST')}.")
                    st.caption(f"Instant push delivered at {att.alert_sent_at.strftime('%H:%M:%S IST')}")
                else:
                    st.success(f"✓ Present on {att.date} (Roll call at {att.roll_call_at.strftime('%H:%M IST')})")

    # Tab 4: Fee Reminders
    with p_tabs[3]:
        st.markdown("#### Fee Due Reminders")
        st.info("🔒 **Strict Security Constraint (SRS FR-06):** Reminders only. School does not process payments in this application.")
        fees = [f for f in db.fee_reminders if f.student_id == child.student_id]
        for f in fees:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Due Date: {f.due_date} (Reminder at D−{f.days_before})</h4>
                <p><strong>Amount:</strong> ₹{f.amount:,.2f}</p>
                <p><strong>Description:</strong> {f.description}</p>
                <p><em>Payment instructions: Please deposit via bank draft or school accounts office.</em></p>
            </div>
            """, unsafe_allow_html=True)

    # Tab 5: Chat
    with p_tabs[4]:
        st.markdown(f"#### Two-Way Message Thread with {teacher.name}")
        st.caption(f"Teacher Contact: `{teacher.masked_contact}` (Privacy Enforced) | Window: 07:00–19:59 IST")

        # Find or create conversation
        conv = next((c for c in db.conversations.values() if c.parent_id == current_user.user_id and c.teacher_id == teacher.user_id), None)
        conv_id = conv.conversation_id if conv else "CONV-NEW"

        # Display message history
        chat_msgs = [m for m in db.messages if m.conversation_id == conv_id]
        for msg in chat_msgs:
            if msg.sender_role == Role.PARENT:
                st.markdown(f"""
                <div class="chat-bubble-parent">
                    <strong>You</strong> ({msg.created_at.strftime('%H:%M')})<br/>
                    {msg.body}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-bubble-teacher">
                    <strong>{msg.sender_name}</strong> ({msg.created_at.strftime('%H:%M')})<br/>
                    {msg.body}
                </div>
                """, unsafe_allow_html=True)

        # Message input
        with st.form("parent_msg_form", clear_on_submit=True):
            p_text = st.text_input("Type your message to the class teacher:")
            submitted = st.form_submit_button("Send Message")
            if submitted and p_text.strip():
                msg_obj, info, auto_reply = MessagingService.send_message(
                    conversation_id=conv_id,
                    sender=current_user,
                    recipient=teacher,
                    body=p_text.strip(),
                    urgent=False,
                    simulated_time=active_time
                )
                st.success(info)
                if auto_reply:
                    st.markdown(f'<div class="auto-reply-box">🤖 <strong>Automated Auto-Reply:</strong> {auto_reply}</div>', unsafe_allow_html=True)
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 2: TEACHER PORTAL (RAHUL DESHMUKH)
# ══════════════════════════════════════════════════════════════════════════════
elif current_user.role == Role.TEACHER:
    st.markdown(f"### 👩‍🏫 Faculty Workspace — **{current_user.name}**")
    st.caption(f"Mapped Classes: {', '.join([db.sections[s].display_name for s in current_user.mapped_section_ids])}")

    t_tabs = st.tabs(["📋 Attendance Roll Call", "📢 Publish Notice", "📊 Read Receipts", "📝 Homework", "💬 Message Parents"])

    # Tab 1: Attendance
    with t_tabs[0]:
        st.markdown("#### Classroom Roll Call & Absence Alerting (FR-05)")
        selected_sec = st.selectbox("Select Classroom for Attendance:", current_user.mapped_section_ids, format_func=lambda s: db.sections[s].display_name)
        sec_students = [s for s in db.students.values() if s.section_id == selected_sec]

        st.write("Mark pupils who are **ABSENT** (Submitting will trigger instant parent push notification within 15 minutes):")
        with st.form("attendance_form"):
            absent_selected = []
            cols = st.columns(2)
            for idx, stu in enumerate(sec_students):
                col = cols[idx % 2]
                if col.checkbox(f"Roll #{stu.roll_number}: {stu.name}", key=f"att_check_{stu.student_id}"):
                    absent_selected.append(stu.student_id)
            
            submit_att = st.form_submit_button("Submit Roll Call & Send Alerts")
            if submit_att:
                records = AttendanceService.submit_roll_call(current_user, selected_sec, absent_selected)
                st.success(f"✓ Roll call submitted for {len(records)} students. {len(absent_selected)} absence alert(s) dispatched to parents.")
                st.rerun()

    # Tab 2: Publish Notice
    with t_tabs[1]:
        st.markdown("#### Compose Official Circular (FR-02)")
        with st.form("notice_compose_form"):
            n_title = st.text_input("Notice Title:")
            n_body = st.text_area("Notice Body / Text:")
            n_scope = st.radio("Target Scope:", [NoticeScope.CLASS, NoticeScope.SCHOOL], format_func=lambda s: "Class Only (Immediate if in window)" if s == NoticeScope.CLASS else "School-Wide (Requires Admin Approval)")
            n_sec = None
            if n_scope == NoticeScope.CLASS:
                n_sec = st.selectbox("Select Target Class:", current_user.mapped_section_ids, format_func=lambda s: db.sections[s].display_name)
            n_file = st.text_input("Attachment Name (Simulated PDF):", value="Curriculum_Notice.pdf")
            
            post_notice = st.form_submit_button("Submit Notice")
            if post_notice and n_title and n_body:
                notice, msg_info = NoticeService.compose_notice(
                    author=current_user,
                    title=n_title,
                    body=n_body,
                    scope=n_scope,
                    section_id=n_sec,
                    attachment_name=n_file,
                    simulated_time=active_time
                )
                st.success(msg_info)
                st.rerun()

    # Tab 3: Read Receipts Analytics
    with t_tabs[2]:
        st.markdown("#### Circular Read Receipt Analytics (FR-03)")
        class_notices = [n for n in db.notices.values() if n.created_by == current_user.user_id or n.section_id in current_user.mapped_section_ids]
        if not class_notices:
            st.info("No notices composed yet.")
        else:
            selected_n = st.selectbox("Select Notice to Inspect Receipts:", class_notices, format_func=lambda n: f"{n.title} ({n.scope.value})")
            analytics = ReadReceiptService.get_notice_analytics(selected_n.notice_id)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Audience Size", f"{analytics['total']} parents")
            c2.metric("Read Rate", f"{analytics['read_percent']}%", f"{analytics['read_count']} read")
            c3.metric("Unread", f"{analytics['unread_count']} parents")
            
            st.progress(analytics['read_percent'] / 100.0)
            
            if analytics['unread_parents']:
                st.markdown("##### Unread Parent List:")
                st.write(", ".join(analytics['unread_parents']))
                if st.button("Remind Unread Parents", key=f"remind_{selected_n.notice_id}"):
                    count = ReadReceiptService.remind_unread(selected_n.notice_id)
                    st.success(f"Dispatched targeted reminder to {count} unread parents.")

    # Tab 4: Homework
    with t_tabs[3]:
        st.markdown("#### Post New Assignment (FR-04)")
        with st.form("hw_form"):
            h_sec = st.selectbox("Class:", current_user.mapped_section_ids, format_func=lambda s: db.sections[s].display_name)
            h_sub = st.selectbox("Subject:", ["Mathematics", "Science", "English", "Social Studies"])
            h_title = st.text_input("Assignment Title:")
            h_desc = st.text_area("Instructions:")
            h_due = st.date_input("Due Date:", min_value=datetime.today()).strftime("%Y-%m-%d")
            submit_hw = st.form_submit_button("Publish Homework")
            if submit_hw and h_title:
                HomeworkService.post_homework(current_user, h_sec, h_sub, h_title, h_desc, h_due)
                st.success("Homework published to class roster.")
                st.rerun()

    # Tab 5: Messaging
    with t_tabs[4]:
        st.markdown("#### Parent-Teacher Communication Threads (FR-07, FR-08)")
        # Show conversations
        teacher_convs = [c for c in db.conversations.values() if c.teacher_id == current_user.user_id]
        if not teacher_convs:
            st.info("No active threads.")
        else:
            sel_conv = st.selectbox("Select Conversation:", teacher_convs, format_func=lambda c: f"Student: {db.students[c.student_id].name} (Parent: {db.users[c.parent_id].name})")
            parent_user = db.users[sel_conv.parent_id]
            
            st.caption(f"Parent Contact: `{parent_user.masked_contact}` (Masked) | Sending Window: 07:00–19:59 IST")
            
            chat_history = [m for m in db.messages if m.conversation_id == sel_conv.conversation_id]
            for m in chat_history:
                if m.sender_role == Role.TEACHER:
                    st.markdown(f"""
                    <div class="chat-bubble-parent">
                        <strong>You</strong> ({m.created_at.strftime('%H:%M')}) - <em>Status: {m.status.value}</em><br/>
                        {m.body}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-bubble-teacher">
                        <strong>{m.sender_name}</strong> ({m.created_at.strftime('%H:%M')})<br/>
                        {m.body}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Send message form
            with st.form("teacher_msg_form", clear_on_submit=True):
                t_body = st.text_input("Reply to Parent:")
                is_urgent = st.checkbox("Mark as URGENT (If after hours, requires Principal approval)", value=False)
                t_send = st.form_submit_button("Send Message")
                if t_send and t_body.strip():
                    msg_obj, info_msg, _ = MessagingService.send_message(
                        conversation_id=sel_conv.conversation_id,
                        sender=current_user,
                        recipient=parent_user,
                        body=t_body.strip(),
                        urgent=is_urgent,
                        simulated_time=active_time
                    )
                    st.info(info_msg)
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 3: SCHOOL ADMIN PORTAL (SUNITA RAO)
# ══════════════════════════════════════════════════════════════════════════════
elif current_user.role == Role.SCHOOL_ADMIN:
    st.markdown(f"### 🏫 School Administration Console — **{current_user.name}**")
    
    a_tabs = st.tabs(["📥 Notice Approval Queue", "📁 Bulk CSV Roster Import", "👥 Staff & Class Mappings"])

    # Tab 1: Approval Queue
    with a_tabs[0]:
        st.markdown("#### Pending School-Level Notice Approvals")
        pending_notices = [r for r in db.approval_requests.values() if r.target_type == "NOTICE" and r.state == "PENDING"]
        if not pending_notices:
            st.success("✓ No circulars pending administrative approval.")
        else:
            for req in pending_notices:
                notice = db.notices.get(req.target_id)
                if notice:
                    with st.expander(f"Review Circular: {notice.title} (By: {notice.author_name})", expanded=True):
                        st.write(notice.body)
                        st.caption(f"Attachment: `{notice.attachment_name}` | Submitted: {req.requested_at.strftime('%Y-%m-%d %H:%M')}")
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("✓ Approve & Publish Notice", key=f"app_{req.request_id}"):
                                NoticeService.approve_notice(req.request_id, current_user, approved=True)
                                st.success("Circular approved and published to all school parents.")
                                st.rerun()
                        with c2:
                            reject_reason = st.text_input("Rejection Reason:", key=f"rej_text_{req.request_id}", placeholder="Content revision needed")
                            if st.button("✕ Reject Notice", key=f"rej_{req.request_id}"):
                                NoticeService.approve_notice(req.request_id, current_user, approved=False, reason=reject_reason)
                                st.warning("Circular rejected.")
                                st.rerun()

    # Tab 2: Bulk CSV Import
    with a_tabs[1]:
        st.markdown("#### Bulk CSV Roster Import with Row-Level Syntax Validation (FR-09)")
        sample_csv_text = """RollNo, StudentName, Section, ParentName, ParentPhone, ParentEmail
101, Rohan Joshi, SEC-5A, Ramesh Joshi, 9821999901, ramesh.joshi@gmail.com
102, Priya Shah, SEC-5A, Neha Shah, INVALID_PHONE_NO, neha.shah@gmail.com
103, Siddharth Roy, SEC-5A, Anirudh Roy, 9821999903, anirudh.roy@gmail.com
"""
        csv_input = st.text_area("Paste Roster CSV Data:", value=sample_csv_text, height=140)
        if st.button("Execute CSV Import Validation"):
            success_count, errors = AdminService.parse_and_import_roster_csv(csv_input, current_user.school_id)
            if success_count > 0:
                st.success(f"✓ Successfully imported {success_count} student-parent records into the school roster.")
            if errors:
                st.error(f"⚠ Found {len(errors)} corrupted row(s). Row-by-row error report:")
                for err in errors:
                    st.write(f"- **Line {err['line']}:** {err['error']} (Raw: `{err.get('raw', '')}`)")

    # Tab 3: Mappings
    with a_tabs[2]:
        st.markdown("#### Class & Section Mappings")
        sec_df = pd.DataFrame([
            {
                "Section ID": s.section_id,
                "Class": s.display_name,
                "Class Teacher": db.users[s.class_teacher_id].name if s.class_teacher_id in db.users else "Unassigned",
                "Students Enrolled": sum(1 for stu in db.students.values() if stu.section_id == s.section_id)
            }
            for s in db.sections.values()
        ])
        st.dataframe(sec_df, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 4: PRINCIPAL PORTAL (DR. ANIL MENON)
# ══════════════════════════════════════════════════════════════════════════════
elif current_user.role == Role.PRINCIPAL:
    st.markdown(f"### 🎓 Principal Office — **{current_user.name}**")
    
    pr_tabs = st.tabs(["🚨 Urgent Out-of-Hours Message Approvals", "🏫 Campus Health"])

    with pr_tabs[0]:
        st.markdown("#### Urgent After-Hours Messaging Queue (Rule R3/R4/R5)")
        urgent_reqs = [r for r in db.approval_requests.values() if r.target_type == "MESSAGE" and r.state == "PENDING"]
        if not urgent_reqs:
            st.success("✓ Zero pending emergency message requests.")
        else:
            for req in urgent_reqs:
                target_m = next((m for m in db.messages if m.message_id == req.target_id), None)
                if target_m:
                    st.warning(f"🚨 **Emergency Message Request from {target_m.sender_name}**")
                    st.write(f"**Content:** {target_m.body}")
                    st.caption(f"Recipient: {target_m.recipient_name} | Submitted: {target_m.created_at.strftime('%H:%M IST')}")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("✓ Approve Emergency Send Now (Override Window)", key=f"app_urg_{req.request_id}"):
                            MessagingService.adjudicate_urgent_message(req.request_id, current_user, approved=True)
                            st.success("Message approved and dispatched immediately.")
                            st.rerun()
                    with c2:
                        if st.button("✕ Reject (Release at 07:00 AM next day)", key=f"rej_urg_{req.request_id}"):
                            MessagingService.adjudicate_urgent_message(req.request_id, current_user, approved=False, reason="Non-emergency")
                            st.info("Message rejected. Re-queued for 07:00 AM standard delivery.")
                            st.rerun()

    with pr_tabs[1]:
        st.markdown("#### Pilot Institution Summary")
        st.write(f"- **Enrolled Pupils:** {len(db.students)}")
        st.write(f"- **Active Parent Accounts:** {sum(1 for u in db.users.values() if u.role == Role.PARENT)}")
        st.write(f"- **Total Notices Published:** {sum(1 for n in db.notices.values() if n.status == NoticeStatus.PUBLISHED)}")


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 5: MANAGEMENT & AUDIT PORTAL (GROUP DIRECTOR)
# ══════════════════════════════════════════════════════════════════════════════
elif current_user.role == Role.MANAGEMENT:
    st.markdown(f"### 📊 Group Executive & Audit Portal — **{current_user.name}**")
    
    m_tabs = st.tabs(["📈 Executive Compliance KPIs", "🔍 Searchable Audit Log", "🧪 Automated Test Suite Runner"])

    # Tab 1: KPIs
    with m_tabs[0]:
        st.markdown("#### Governance Metrics & SLA Compliance")
        active_kpi = AuditReportService.get_monthly_active_parents_metric()
        late_kpi = AuditReportService.get_after_hours_teacher_messages_metric()

        k1, k2, k3 = st.columns(3)
        with k1:
            st.metric(
                "Monthly Active Parents",
                f"{active_kpi['percentage']}%",
                f"{active_kpi['active_count']} / {active_kpi['total_parents']} parents"
            )
            st.caption(f"Target: **90%** (Pilot goal: {active_kpi['target_count']} parents)")
            st.progress(active_kpi['percentage'] / 100.0)

        with k2:
            st.metric(
                "After-8 PM Routine Messages",
                f"{late_kpi['routine_after_8']} msgs",
                "Target: 0 messages"
            )
            if late_kpi['compliant']:
                st.success("✅ 100% SLA COMPLIANT (Zero late routine messages)")
            else:
                st.error("⚠ SLA BREACH")
            st.caption(f"Approved Urgent Overrides: **{late_kpi['urgent_approved_after_8']}**")

        with k3:
            st.metric("Defect Removal Efficiency (DRE)", "94.4%", "Target: ≥ 90%")
            st.caption("Pre-release defects: 34 | Escaped: 2")

    # Tab 2: Audit Log
    with m_tabs[1]:
        st.markdown("#### Searchable Communication Audit Log (FR-10)")
        search_kw = st.text_input("Filter by Keyword / Actor / Target:", "")
        logs = AuditReportService.search_audit_log(keyword=search_kw)
        
        log_data = [
            {
                "Timestamp": e.occurred_at.strftime("%Y-%m-%d %H:%M:%S"),
                "Actor": f"{e.actor_name} ({e.actor_role.value})",
                "Action": e.action,
                "Target ID": e.target_id,
                "Metadata": str(e.metadata)
            }
            for e in logs
        ]
        st.dataframe(pd.DataFrame(log_data), use_container_width=True)

    # Tab 3: Test Runner
    with m_tabs[2]:
        st.markdown("#### Embedded Regression Test Suite")
        st.write("Execute all 41 test cases (BVA 18 cases, Decision Table 13 rules, and System Acceptance TC-01 to TC-10):")
        if st.button("Run Complete Test Suite (41 Tests)"):
            import unittest
            loader = unittest.TestLoader()
            suite = loader.discover("tests")
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            if result.wasSuccessful():
                st.success(f"🎉 100% PASS: All {result.testsRun} tests executed successfully in <0.01 seconds!")
            else:
                st.error(f"Tests failed: {len(result.failures)} failures, {len(result.errors)} errors.")
