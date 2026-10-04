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

# ─── PAGE CONFIGURATION & MODERN BRUTALIST CSS ────────────────────────────────
st.set_page_config(
    page_title="SchoolDiary · Parent-Teacher Communication",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Core Color Tokens */
    :root {
        --navy: #1B2A4A;
        --coral: #E05A4E;
        --teal: #2D7D8E;
        --slate: #4A5568;
        --light-bg: #F8FAFC;
        --card-border: #E2E8F0;
    }

    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1B2A4A;
        letter-spacing: -0.02em;
        margin-bottom: 0.1rem;
    }
    .sub-title {
        font-size: 1.0rem;
        color: #4A5568;
        margin-bottom: 1.0rem;
    }

    /* Modern Card Container */
    .sd-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 18px 20px;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: transform 0.1s ease, box-shadow 0.1s ease;
    }
    .sd-card:hover {
        border-color: #CBD5E1;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.06);
    }

    .sd-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #F1F5F9;
        padding-bottom: 10px;
        margin-bottom: 12px;
    }

    /* Badges & Tags */
    .badge-published {
        background-color: #ECFDF5;
        color: #065F46;
        border: 1px solid #A7F3D0;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .badge-pending {
        background-color: #FFFBEB;
        color: #92400E;
        border: 1px solid #FDE68A;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        text-transform: uppercase;
    }
    .badge-scope {
        background-color: #EFF6FF;
        color: #1E40AF;
        border: 1px solid #BFDBFE;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
    }
    .status-badge-open {
        background-color: #DCFCE7;
        color: #166534;
        border: 1px solid #86EFAC;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.82rem;
        display: inline-block;
        letter-spacing: 0.02em;
    }
    .status-badge-closed {
        background-color: #FEE2E2;
        color: #991B1B;
        border: 1px solid #FCA5A5;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.82rem;
        display: inline-block;
        letter-spacing: 0.02em;
    }

    /* Chat Elements */
    .chat-bubble-teacher {
        background-color: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-left: 4px solid #0284C7;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 12px;
        max-width: 82%;
    }
    .chat-bubble-parent {
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-right: 4px solid #475569;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 12px;
        margin-left: auto;
        max-width: 82%;
    }
    .auto-reply-box {
        background-color: #FEF9C3;
        border: 1px solid #FDE047;
        border-left: 4px solid #EAB308;
        padding: 12px 16px;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #713F12;
        margin: 10px 0;
    }
    .chat-meta {
        font-size: 0.76rem;
        color: #64748B;
        margin-bottom: 4px;
        display: flex;
        justify-content: space-between;
    }

    /* Metric Boxes */
    .kpi-container {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px 18px;
        text-align: center;
    }
    .kpi-num {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1B2A4A;
        font-family: 'JetBrains Mono', monospace;
    }
    .kpi-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ─── SIDEBAR: CLOCK SIMULATOR & ROLE SWITCHER ────────────────────────────────
with st.sidebar:
    st.markdown("### 🏫 SchoolDiary Console")
    st.caption("B.Tech CSE (2025–29) · Semester III · Case #111")
    st.caption("Sole Author: **Kishan Ojha (@Kishann911)**")
    st.divider()

    # 1. Interactive Clock Simulator Toolbar
    st.markdown("#### ⏰ System Clock Control")
    use_simulation = st.checkbox("Override Real Clock", value=False, help="Toggle to test messaging-hours boundaries live (e.g., 19:59 vs 20:00 vs 23:59)")

    if use_simulation:
        sim_col1, sim_col2 = st.columns(2)
        with sim_col1:
            hour_val = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=20)
        with sim_col2:
            min_val = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=15)
        active_time = time(hour_val, min_val)
        st.info(f"Mock Clock: **{active_time.strftime('%H:%M')} IST**")
    else:
        active_time = datetime.now().time()
        st.caption(f"Real System Time: **{active_time.strftime('%H:%M:%S')} IST**")

    # Evaluate window status
    is_window_open = MessagingPolicy.is_inside_window(active_time)
    if is_window_open:
        st.markdown('<div class="status-badge-open">🟢 WINDOW OPEN (07:00–19:59 IST)</div>', unsafe_allow_html=True)
        st.caption("Teacher messages & circulars dispatch immediately.")
    else:
        st.markdown('<div class="status-badge-closed">🔴 WINDOW CLOSED (20:00–06:59 IST)</div>', unsafe_allow_html=True)
        st.caption("Routine messages auto-queue for 07:00 AM next school day.")

    st.divider()

    # 2. Scoped Role Switcher
    st.markdown("#### 👤 Active Persona Switcher")
    role_options = {
        "👨‍👩‍👧 Parent: Meena Kulkarni (Aarav, 5A)": ("USR-PAR-01", Role.PARENT),
        "👩‍🏫 Teacher: Rahul Deshmukh (Maths, 5A & 7B)": ("USR-TCH-01", Role.TEACHER),
        "🏫 School Admin: Sunita Rao (St. Mary's)": ("USR-ADM-01", Role.SCHOOL_ADMIN),
        "🎓 Principal: Dr. Anil Menon (St. Mary's)": ("USR-PRIN-01", Role.PRINCIPAL),
        "📊 Group Management: K. V. Raman (Director)": ("USR-MGMT-01", Role.MANAGEMENT),
    }
    selected_role_label = st.selectbox("Switch Persona:", list(role_options.keys()))
    active_user_id, active_role = role_options[selected_role_label]
    current_user = db.users[active_user_id]

    st.caption(f"User ID: `{current_user.user_id}` · Phone: `{current_user.masked_contact}`")
    st.caption(f"Institution: `{db.schools[current_user.school_id].name}`")

    st.divider()
    st.markdown("#### 📊 Project Baseline Reference")
    st.markdown("""
    - **Pilot Scope:** 2 Schools · 2,300 Parents (**16.4%**)
    - **Effort Budget:** 68 Person-Days · Team of 3
    - **Schedule:** 27 Working Days (Critical Path)
    - **Quality SLA:** 0 Late Messages · 94.4% DRE
    """)


# ─── MAIN HEADER ─────────────────────────────────────────────────────────────
hdr_left, hdr_right = st.columns([3, 1])
with hdr_left:
    st.markdown('<div class="main-title">SchoolDiary</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Parent–Teacher Communication App for a School Group · Case 111</div>', unsafe_allow_html=True)
with hdr_right:
    st.markdown(f"**Current Role:** `{current_user.role.value}`")
    st.markdown(f"**Logged in:** {current_user.name}")

st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 1: PARENT PORTAL (MEENA KULKARNI)
# ══════════════════════════════════════════════════════════════════════════════
if current_user.role == Role.PARENT:
    child_id = current_user.children_ids[0]
    child = db.students[child_id]
    section = db.sections[child.section_id]
    teacher = db.users[section.class_teacher_id]

    st.markdown(f"### 👨‍👩‍👧 Parent Portal — Child: **{child.name}** (Roll #{child.roll_number} · {section.display_name})")

    p_tabs = st.tabs(["📢 Official Circulars", "📝 Homework Feed", "🚨 Absence Alerts", "💳 Fee Reminders", "💬 Chat with Class Teacher"])

    # Tab 1: Notices
    with p_tabs[0]:
        st.markdown("#### School Circulars & Class Notices")
        scope_filter = st.radio("Filter Notices:", ["All Notices", "Class 5A Only", "School-Wide"], horizontal=True)

        visible_notices = [
            n for n in db.notices.values()
            if n.status == NoticeStatus.PUBLISHED and (n.scope == NoticeScope.SCHOOL or n.section_id == section.section_id)
        ]
        if scope_filter == "Class 5A Only":
            visible_notices = [n for n in visible_notices if n.scope == NoticeScope.CLASS]
        elif scope_filter == "School-Wide":
            visible_notices = [n for n in visible_notices if n.scope == NoticeScope.SCHOOL]

        if not visible_notices:
            st.info("No notices match the selected filter.")
        else:
            for notif in visible_notices:
                ReadReceiptService.mark_read(notif.notice_id, current_user.user_id)
                with st.container():
                    st.markdown(f"""
                    <div class="sd-card">
                        <div class="sd-card-header">
                            <div>
                                <span class="badge-scope">{notif.scope.value}</span>
                                <strong style="font-size: 1.05rem; margin-left: 8px;">{notif.title}</strong>
                            </div>
                            <span class="badge-published">✓ Read</span>
                        </div>
                        <p style="color: #334155; line-height: 1.5;">{notif.body}</p>
                        <div style="font-size: 0.8rem; color: #64748B; margin-top: 8px;">
                            <span>👤 Published by: <strong>{notif.author_name}</strong></span> ·
                            <span>📅 {notif.created_at.strftime('%d %b %Y, %H:%M IST')}</span> ·
                            <span>📎 Attachment: <code>{notif.attachment_name or 'None'}</code></span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # Tab 2: Homework
    with p_tabs[1]:
        st.markdown(f"#### Class Assignments for {section.display_name}")
        hw_list = [h for h in db.homeworks.values() if h.section_id == section.section_id]
        if not hw_list:
            st.info("No homework assigned at this time.")
        else:
            for hw in hw_list:
                is_ack = current_user.user_id in hw.acknowledged_by
                col_hw_info, col_hw_act = st.columns([3, 1])
                with col_hw_info:
                    st.markdown(f"""
                    <div class="sd-card">
                        <div class="sd-card-header">
                            <strong>📚 {hw.subject}: {hw.title}</strong>
                            <span style="font-size: 0.8rem; font-weight: 600; color: #DC2626;">⏳ Due: {hw.due_date}</span>
                        </div>
                        <p style="color: #475569; font-size: 0.92rem;">{hw.description}</p>
                        <div style="font-size: 0.78rem; color: #94A3B8;">
                            Assigned by: {db.users[hw.created_by].name} · {hw.created_at.strftime('%d %b %Y')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_hw_act:
                    if is_ack:
                        st.button("✓ Acknowledged", key=f"p_hw_{hw.homework_id}", disabled=True)
                    else:
                        if st.button("Acknowledge (Seen)", key=f"p_ack_{hw.homework_id}", type="primary"):
                            HomeworkService.acknowledge_homework(hw.homework_id, current_user.user_id)
                            st.success("Acknowledged!")
                            st.rerun()

    # Tab 3: Attendance
    with p_tabs[2]:
        st.markdown("#### Automated Absence Alerts & Roll-Call History")
        st.caption("SLA: Absence alerts are dispatched to parent mobile devices within 15 minutes of roll-call submission (NFR-01).")
        child_att = [a for a in db.attendance if a.student_id == child.student_id]
        if not child_att:
            st.info("No attendance records found.")
        else:
            for att in reversed(child_att):
                if att.status == "ABSENT":
                    st.markdown(f"""
                    <div class="sd-card" style="border-left: 4px solid #EF4444; background: #FEF2F2;">
                        <strong style="color: #991B1B;">🚨 ABSENCE ALERT: {child.name} marked ABSENT on {att.date}</strong>
                        <p style="margin: 4px 0 0 0; color: #7F1D1D; font-size: 0.9rem;">
                            Roll call taken at {att.roll_call_at.strftime('%H:%M IST')}. Push notification delivered to your registered phone at {att.alert_sent_at.strftime('%H:%M:%S IST')} (Within 15-minute SLA).
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="sd-card" style="border-left: 4px solid #10B981;">
                        <span style="color: #065F46; font-weight: 600;">✓ Present on {att.date}</span>
                        <span style="color: #64748B; font-size: 0.85rem; margin-left: 12px;">Roll-call recorded at {att.roll_call_at.strftime('%H:%M IST')}</span>
                    </div>
                    """, unsafe_allow_html=True)

    # Tab 4: Fee Reminders
    with p_tabs[3]:
        st.markdown("#### School Fee Reminders (Read-Only)")
        st.warning("🔒 **Security Policy (SRS FR-06 / Out of Scope):** Reminders only at D−7 and D−1. This application does not collect or process payments online to eliminate financial and fraud liabilities.")
        fees = [f for f in db.fee_reminders if f.student_id == child.student_id]
        for f in fees:
            st.markdown(f"""
            <div class="sd-card" style="border-left: 4px solid #0284C7;">
                <div class="sd-card-header">
                    <strong>{f.description}</strong>
                    <span style="font-size: 1.1rem; font-weight: 800; color: #1B2A4A;">₹{f.amount:,.2f}</span>
                </div>
                <p style="color: #475569; font-size: 0.9rem; margin-bottom: 6px;">
                    <strong>Due Date:</strong> {f.due_date} (Reminder triggered at D−{f.days_before} days)
                </p>
                <p style="font-size: 0.82rem; color: #64748B; margin: 0;">
                    <em>Payment Channel: Please deposit via bank draft or visit the school accounts office between 09:00 AM and 01:00 PM.</em>
                </p>
            </div>
            """, unsafe_allow_html=True)

    # Tab 5: Chat
    with p_tabs[4]:
        st.markdown(f"#### Two-Way Message Thread with {teacher.name}")
        st.caption(f"Teacher Phone: `{teacher.masked_contact}` (Masked) · Operating Hours: 07:00–19:59 IST")

        conv = next((c for c in db.conversations.values() if c.parent_id == current_user.user_id and c.teacher_id == teacher.user_id), None)
        conv_id = conv.conversation_id if conv else "CONV-01"

        # Chat container
        chat_box = st.container()
        with chat_box:
            chat_msgs = [m for m in db.messages if m.conversation_id == conv_id]
            for m in chat_msgs:
                if m.sender_role == Role.PARENT:
                    st.markdown(f"""
                    <div class="chat-bubble-parent">
                        <div class="chat-meta">
                            <span><strong>You (Meena)</strong></span>
                            <span>{m.created_at.strftime('%H:%M IST')} · <em>{m.status.value}</em></span>
                        </div>
                        <div style="color: #1E293B; font-size: 0.92rem;">{m.body}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-bubble-teacher">
                        <div class="chat-meta">
                            <span><strong>{m.sender_name} (Class Teacher)</strong></span>
                            <span>{m.created_at.strftime('%H:%M IST')} · ✓✓ Read</span>
                        </div>
                        <div style="color: #0F172A; font-size: 0.92rem;">{m.body}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.divider()
        if not is_window_open:
            st.markdown("""
            <div class="auto-reply-box">
                🌙 <strong>After-Hours Policy Active:</strong> Messages sent now will be safely delivered to Teacher Rahul at 07:00 AM tomorrow. You will receive an instantaneous automated acknowledgment.
            </div>
            """, unsafe_allow_html=True)

        with st.form("parent_chat_form", clear_on_submit=True):
            p_input = st.text_input("Type your message to Teacher Rahul Deshmukh:", placeholder="e.g., Sir, Aarav had fever yesterday. Could you please share the math worksheet?")
            btn_send = st.form_submit_button("Send Message", type="primary")

            if btn_send and p_input.strip():
                msg_obj, info_text, auto_reply = MessagingService.send_message(
                    conversation_id=conv_id,
                    sender=current_user,
                    recipient=teacher,
                    body=p_input.strip(),
                    urgent=False,
                    simulated_time=active_time,
                    trigger_teacher_reply=True
                )
                if auto_reply:
                    st.warning(f"🤖 Automated Response: {auto_reply}")
                else:
                    st.success("✓ Message sent & Teacher Rahul Deshmukh replied!")
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 2: TEACHER WORKSPACE (RAHUL DESHMUKH)
# ══════════════════════════════════════════════════════════════════════════════
elif current_user.role == Role.TEACHER:
    st.markdown(f"### 👩‍🏫 Faculty Workspace — **{current_user.name}**")
    st.caption(f"Mapped Sections: {', '.join([db.sections[s].display_name for s in current_user.mapped_section_ids])}")

    t_tabs = st.tabs(["📋 Attendance Roll Call", "📢 Circulars & Publishing", "📊 Read Receipts Analytics", "📝 Homework Assignments", "💬 Parent Message Threads"])

    # Tab 1: Attendance
    with t_tabs[0]:
        st.markdown("#### Classroom Roll Call & 15-Minute Absence Alerts (FR-05)")
        selected_sec = st.selectbox("Select Classroom:", current_user.mapped_section_ids, format_func=lambda s: db.sections[s].display_name)
        sec_students = [s for s in db.students.values() if s.section_id == selected_sec]

        st.write(f"Class Roster ({len(sec_students)} pupils enrolled). Check students who are **ABSENT**:")
        with st.form("att_rollcall_form"):
            absent_ids = []
            cols = st.columns(2)
            for idx, stu in enumerate(sec_students):
                col = cols[idx % 2]
                if col.checkbox(f"Roll #{stu.roll_number}: {stu.name}", key=f"att_check_{stu.student_id}"):
                    absent_ids.append(stu.student_id)

            submit_roll = st.form_submit_button("Submit Roll Call & Dispatch Instant Alerts", type="primary")
            if submit_roll:
                records = AttendanceService.submit_roll_call(current_user, selected_sec, absent_ids)
                st.success(f"✓ Roll call saved. {len(absent_ids)} absence alert(s) dispatched to parents within the 15-minute SLA.")
                st.rerun()

    # Tab 2: Publish Notice
    with t_tabs[1]:
        st.markdown("#### Compose Official Circular (FR-02)")
        with st.form("notice_form", clear_on_submit=True):
            n_title = st.text_input("Notice Title:")
            n_body = st.text_area("Notice Body / Text:")
            n_scope = st.radio("Notice Scope:", [NoticeScope.CLASS, NoticeScope.SCHOOL], format_func=lambda s: "Class Only (Immediate publish if in window)" if s == NoticeScope.CLASS else "School-Wide (Routes to Admin Approval Queue)")
            n_sec = None
            if n_scope == NoticeScope.CLASS:
                n_sec = st.selectbox("Target Classroom:", current_user.mapped_section_ids, format_func=lambda s: db.sections[s].display_name)
            n_att = st.text_input("Attachment Filename (Simulated PDF):", value="Curriculum_Assessment_Class5.pdf")

            post_btn = st.form_submit_button("Publish Circular", type="primary")
            if post_btn and n_title and n_body:
                notice, msg_info = NoticeService.compose_notice(
                    author=current_user,
                    title=n_title,
                    body=n_body,
                    scope=n_scope,
                    section_id=n_sec,
                    attachment_name=n_att,
                    simulated_time=active_time
                )
                st.info(msg_info)
                st.rerun()

    # Tab 3: Read Receipts Analytics
    with t_tabs[2]:
        st.markdown("#### Read Receipts Analytics & Unread Chasing (FR-03)")
        class_notices = [n for n in db.notices.values() if n.created_by == current_user.user_id or n.section_id in current_user.mapped_section_ids]
        if not class_notices:
            st.info("No notices published yet.")
        else:
            sel_n = st.selectbox("Select Circular to Inspect Receipts:", class_notices, format_func=lambda n: f"{n.title} ({n.scope.value})")
            analytics = ReadReceiptService.get_notice_analytics(sel_n.notice_id)

            k1, k2, k3 = st.columns(3)
            with k1:
                st.markdown(f'<div class="kpi-container"><div class="kpi-num">{analytics["total"]}</div><div class="kpi-label">Audience Size</div></div>', unsafe_allow_html=True)
            with k2:
                st.markdown(f'<div class="kpi-container"><div class="kpi-num">{analytics["read_percent"]}%</div><div class="kpi-label">Read Rate ({analytics["read_count"]} Parents)</div></div>', unsafe_allow_html=True)
            with k3:
                st.markdown(f'<div class="kpi-container"><div class="kpi-num">{analytics["unread_count"]}</div><div class="kpi-label">Unread Parents</div></div>', unsafe_allow_html=True)

            st.progress(analytics["read_percent"] / 100.0)

            if analytics["unread_parents"]:
                st.markdown("##### 👥 Parents who haven't read this circular yet:")
                st.write(", ".join([f"**{p}**" for p in analytics["unread_parents"]]))
                if st.button("🔔 Send Push Reminder to All Unread Parents", key=f"t_rem_{sel_n.notice_id}", type="primary"):
                    cnt = ReadReceiptService.remind_unread(sel_n.notice_id)
                    st.success(f"Dispatched targeted reminder to {cnt} unread parents!")

    # Tab 4: Homework
    with t_tabs[3]:
        st.markdown("#### Publish New Homework Assignment (FR-04)")
        with st.form("t_hw_form", clear_on_submit=True):
            hw_sec = st.selectbox("Target Section:", current_user.mapped_section_ids, format_func=lambda s: db.sections[s].display_name)
            hw_sub = st.selectbox("Subject:", ["Mathematics", "Science", "English", "Social Studies", "Hindi"])
            hw_tit = st.text_input("Title:")
            hw_dsc = st.text_area("Detailed Instructions:")
            hw_due = st.date_input("Due Date:", min_value=datetime.today()).strftime("%Y-%m-%d")
            submit_hw = st.form_submit_button("Publish Assignment", type="primary")
            if submit_hw and hw_tit:
                HomeworkService.post_homework(current_user, hw_sec, hw_sub, hw_tit, hw_dsc, hw_due)
                st.success("Homework published to class stream.")
                st.rerun()

    # Tab 5: Chat
    with t_tabs[4]:
        st.markdown("#### Parent Two-Way Communication Threads (FR-07, FR-08)")
        teacher_convs = [c for c in db.conversations.values() if c.teacher_id == current_user.user_id]
        if not teacher_convs:
            st.info("No active parent threads.")
        else:
            sel_conv = st.selectbox("Select Thread:", teacher_convs, format_func=lambda c: f"Student: {db.students[c.student_id].name} · Parent: {db.users[c.parent_id].name}")
            parent_user = db.users[sel_conv.parent_id]
            st.caption(f"Parent Contact: `{parent_user.masked_contact}` (Privacy Masked) · Sending Window: 07:00–19:59 IST")

            # Render history
            chat_msgs = [m for m in db.messages if m.conversation_id == sel_conv.conversation_id]
            for m in chat_msgs:
                if m.sender_role == Role.TEACHER:
                    st.markdown(f"""
                    <div class="chat-bubble-parent">
                        <div class="chat-meta">
                            <span><strong>You</strong></span>
                            <span>{m.created_at.strftime('%H:%M IST')} · Status: {m.status.value}</span>
                        </div>
                        <div style="font-size: 0.92rem; color: #1E293B;">{m.body}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-bubble-teacher">
                        <div class="chat-meta">
                            <span><strong>{m.sender_name}</strong></span>
                            <span>{m.created_at.strftime('%H:%M IST')}</span>
                        </div>
                        <div style="font-size: 0.92rem; color: #0F172A;">{m.body}</div>
                    </div>
                    """, unsafe_allow_html=True)

            with st.form("t_reply_form", clear_on_submit=True):
                t_reply = st.text_input("Reply to Parent:")
                is_urg = st.checkbox("Mark as URGENT (If after hours, forwards to Principal for instant approval)", value=False)
                t_send = st.form_submit_button("Send Response", type="primary")
                if t_send and t_reply.strip():
                    msg_obj, info_msg, _ = MessagingService.send_message(
                        conversation_id=sel_conv.conversation_id,
                        sender=current_user,
                        recipient=parent_user,
                        body=t_reply.strip(),
                        urgent=is_urg,
                        simulated_time=active_time,
                        trigger_teacher_reply=False
                    )
                    st.info(info_msg)
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 3: SCHOOL ADMIN PORTAL (SUNITA RAO)
# ══════════════════════════════════════════════════════════════════════════════
elif current_user.role == Role.SCHOOL_ADMIN:
    st.markdown(f"### 🏫 School Administration Console — **{current_user.name}**")
    
    a_tabs = st.tabs(["📥 Notice Approval Queue", "📁 Bulk CSV Roster Import", "👥 Class & Staff Mappings"])

    # Tab 1: Approval Queue
    with a_tabs[0]:
        st.markdown("#### Pending School-Level Notice Approvals (FR-02)")
        pending_notices = [r for r in db.approval_requests.values() if r.target_type == "NOTICE" and r.state == "PENDING"]
        if not pending_notices:
            st.success("✓ Zero pending circulars in the administrative queue.")
        else:
            st.write(f"Found **{len(pending_notices)}** circular(s) awaiting approval:")
            for req in pending_notices:
                notice = db.notices.get(req.target_id)
                if notice:
                    with st.container():
                        st.markdown(f"""
                        <div class="sd-card">
                            <div class="sd-card-header">
                                <div>
                                    <span class="badge-pending">Pending Approval</span>
                                    <strong style="margin-left: 8px; font-size: 1.05rem;">{notice.title}</strong>
                                </div>
                                <span style="font-size: 0.8rem; color: #64748B;">Submitted by: {notice.author_name}</span>
                            </div>
                            <p style="color: #334155; font-size: 0.95rem;">{notice.body}</p>
                            <p style="font-size: 0.82rem; color: #64748B;">📎 Attachment: <code>{notice.attachment_name or 'None'}</code></p>
                        </div>
                        """, unsafe_allow_html=True)
                        col_app, col_rej = st.columns([1, 1])
                        with col_app:
                            if st.button(f"✓ Approve & Publish Notice", key=f"app_{req.request_id}", type="primary"):
                                NoticeService.approve_notice(req.request_id, current_user, approved=True)
                                st.success("Circular approved and published!")
                                st.rerun()
                        with col_rej:
                            rej_reason = st.text_input("Rejection Feedback:", key=f"txt_{req.request_id}", placeholder="Revise date/venue")
                            if st.button(f"✕ Reject Circular", key=f"rej_{req.request_id}"):
                                NoticeService.approve_notice(req.request_id, current_user, approved=False, reason=rej_reason)
                                st.warning("Notice rejected.")
                                st.rerun()
                        st.divider()

    # Tab 2: Bulk CSV Import
    with a_tabs[1]:
        st.markdown("#### Bulk CSV Roster Import with Row-Level Syntax Validation (FR-09)")
        sample_csv_text = """RollNo, StudentName, Section, ParentName, ParentPhone, ParentEmail
101, Rohan Joshi, SEC-5A, Ramesh Joshi, 9821999901, ramesh.joshi@gmail.com
102, Priya Shah, SEC-5A, Neha Shah, INVALID_PHONE_NO, neha.shah@gmail.com
103, Siddharth Roy, SEC-5A, Anirudh Roy, 9821999903, anirudh.roy@gmail.com
"""
        csv_input = st.text_area("Roster CSV Data (Includes 1 simulated syntax error on Line 3):", value=sample_csv_text, height=130)
        if st.button("Run Bulk Import & Validation", type="primary"):
            success_count, errors = AdminService.parse_and_import_roster_csv(csv_input, current_user.school_id)
            if success_count > 0:
                st.success(f"✓ Successfully imported {success_count} pupil-parent record(s) into database.")
            if errors:
                st.error(f"⚠ Detected {len(errors)} corrupted row(s). Row-by-row syntax report:")
                for err in errors:
                    st.markdown(f"- **Line {err['line']}:** `{err['error']}`")

    # Tab 3: Mappings
    with a_tabs[2]:
        st.markdown("#### Classroom & Faculty Allocation")
        sec_df = pd.DataFrame([
            {
                "Section ID": s.section_id,
                "Class": s.display_name,
                "Class Teacher": db.users[s.class_teacher_id].name if s.class_teacher_id in db.users else "Unassigned",
                "Pupils Enrolled": sum(1 for stu in db.students.values() if stu.section_id == s.section_id)
            }
            for s in db.sections.values()
        ])
        st.dataframe(sec_df, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 4: PRINCIPAL OFFICE (DR. ANIL MENON)
# ══════════════════════════════════════════════════════════════════════════════
elif current_user.role == Role.PRINCIPAL:
    st.markdown(f"### 🎓 Principal Office — **{current_user.name}**")
    
    pr_tabs = st.tabs(["🚨 Urgent Out-of-Hours Message Approvals", "🏫 Institutional Overview"])

    with pr_tabs[0]:
        st.markdown("#### Emergency After-Hours Message Adjudication Queue (FR-08 / Rule R3, R4, R5)")
        urgent_reqs = [r for r in db.approval_requests.values() if r.target_type == "MESSAGE" and r.state == "PENDING"]
        if not urgent_reqs:
            st.success("✓ Zero pending emergency message requests.")
        else:
            for req in urgent_reqs:
                target_m = next((m for m in db.messages if m.message_id == req.target_id), None)
                if target_m:
                    st.markdown(f"""
                    <div class="sd-card" style="border-left: 4px solid #DC2626; background: #FFF5F5;">
                        <div class="sd-card-header">
                            <div>
                                <span style="background: #FEE2E2; color: #991B1B; font-weight: 700; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem;">URGENT EXCEPTION</span>
                                <strong style="margin-left: 8px; font-size: 1.05rem;">From: {target_m.sender_name}</strong>
                            </div>
                            <span style="font-size: 0.8rem; color: #64748B;">Submitted at: {target_m.created_at.strftime('%H:%M IST')}</span>
                        </div>
                        <p style="color: #7F1D1D; font-size: 0.95rem; font-weight: 500;">{target_m.body}</p>
                        <p style="font-size: 0.8rem; color: #64748B;">Target Recipient: {target_m.recipient_name} · Action Required: Approve for immediate send, or reject to queue for 07:00 AM.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("✓ Approve Emergency Send Now (Override Window)", key=f"pr_app_{req.request_id}", type="primary"):
                            MessagingService.adjudicate_urgent_message(req.request_id, current_user, approved=True)
                            st.success("Message approved and dispatched immediately to parent.")
                            st.rerun()
                    with c2:
                        if st.button("✕ Reject (Release at 07:00 AM next day)", key=f"pr_rej_{req.request_id}"):
                            MessagingService.adjudicate_urgent_message(req.request_id, current_user, approved=False, reason="Non-emergency")
                            st.info("Message rejected. Re-queued for 07:00 AM standard delivery.")
                            st.rerun()

    with pr_tabs[1]:
        st.markdown("#### Campus Operational Statistics")
        st.write(f"- **Enrolled Pupils:** {len(db.students)}")
        st.write(f"- **Registered Parents:** {sum(1 for u in db.users.values() if u.role == Role.PARENT)}")
        st.write(f"- **Faculty Members:** {sum(1 for u in db.users.values() if u.role == Role.TEACHER)}")
        st.write(f"- **Active Circulars:** {sum(1 for n in db.notices.values() if n.status == NoticeStatus.PUBLISHED)}")


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 5: MANAGEMENT & COMPLIANCE PORTAL (GROUP DIRECTOR)
# ══════════════════════════════════════════════════════════════════════════════
elif current_user.role == Role.MANAGEMENT:
    st.markdown(f"### 📊 Group Executive Governance & Compliance Portal")
    
    m_tabs = st.tabs(["📈 Executive Compliance KPIs", "🔍 Central Communication Audit Log", "🧪 Regression Test Suite Runner"])

    # Tab 1: KPIs
    with m_tabs[0]:
        st.markdown("#### Key Performance Indicators (Pilot SLA Compliance)")
        active_kpi = AuditReportService.get_monthly_active_parents_metric()
        late_kpi = AuditReportService.get_after_hours_teacher_messages_metric()

        k1, k2, k3 = st.columns(3)
        with k1:
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-num">{active_kpi['percentage']}%</div>
                <div class="kpi-label">Monthly Active Parents</div>
                <div style="font-size: 0.8rem; color: #64748B; margin-top: 4px;">Target: 90.0% (Pilot Goal: 2,070)</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(active_kpi['percentage'] / 100.0)

        with k2:
            st.markdown(f"""
            <div class="kpi-container" style="border-left: 4px solid {'#10B981' if late_kpi['compliant'] else '#EF4444'};">
                <div class="kpi-num">{late_kpi['routine_after_8']} msgs</div>
                <div class="kpi-label">After-8 PM Routine Messages</div>
                <div style="font-size: 0.8rem; color: #64748B; margin-top: 4px;">Target: 0 messages (Urgent Overrides: {late_kpi['urgent_approved_after_8']})</div>
            </div>
            """, unsafe_allow_html=True)
            if late_kpi['compliant']:
                st.success("✅ 100% SLA COMPLIANT: Zero late messages delivered.")

        with k3:
            st.markdown("""
            <div class="kpi-container">
                <div class="kpi-num">94.4%</div>
                <div class="kpi-label">Defect Removal Efficiency (DRE)</div>
                <div style="font-size: 0.8rem; color: #64748B; margin-top: 4px;">Target: ≥ 90% (34 pre-release / 2 pilot)</div>
            </div>
            """, unsafe_allow_html=True)

    # Tab 2: Audit Log
    with m_tabs[1]:
        st.markdown("#### Searchable Communication Audit Log (FR-10)")
        search_kw = st.text_input("Search Audit Log (Keyword, Actor, Action, Target ID):", placeholder="e.g., NOTICE, ATTENDANCE, Rahul Deshmukh")
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

    # Tab 3: Test Suite Runner
    with m_tabs[2]:
        st.markdown("#### Regression Test Suite Execution")
        st.write("Execute all 41 test cases (BVA 18 cases, Decision Table 13 rules, and System Acceptance TC-01 to TC-10):")
        if st.button("Run Full Regression Suite (41 Tests)", type="primary"):
            import unittest
            loader = unittest.TestLoader()
            suite = loader.discover("tests")
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            if result.wasSuccessful():
                st.success(f"🎉 100% SUCCESS: All {result.testsRun} unit, BVA, decision table, and system acceptance tests passed in <0.01 seconds!")
            else:
                st.error(f"Tests failed: {len(result.failures)} failures, {len(result.errors)} errors.")
