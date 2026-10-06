"""
Generate high-resolution professional UML diagrams for SchoolDiary Case 111.
Diagrams generated:
1. diagrams/uml_use_case.png        — Use-Case Model (Actors, Boundaries, <<include>>, <<extend>>)
2. diagrams/uml_class_diagram.png   — Class Diagram (Domain entities, loose coupling event bus)
3. diagrams/uml_sequence_notice.png — Sequence Diagram (Send notice & track read receipts)
4. diagrams/uml_activity_message.png— Activity Diagram (Message time check & approval flow)
5. diagrams/uml_state_message.png   — Statechart Diagram (Message 12-state lifecycle)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

DIAGRAMS_DIR = os.path.join(os.path.dirname(__file__), "diagrams")
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

NAVY = "#1B2A4A"
CORAL = "#E05A4E"
TEAL = "#2D7D8E"
SLATE = "#4A5568"
LIGHT_GREY = "#F7F9FC"
MID_GREY = "#CBD5E0"
WHITE = "#FFFFFF"
BORDER_DARK = "#1E293B"

# ══════════════════════════════════════════════════════════════════════════════
# 1. USE CASE DIAGRAM
# ══════════════════════════════════════════════════════════════════════════════
def make_use_case_diagram():
    fig, ax = plt.subplots(figsize=(11.5, 8.0), dpi=300)
    ax.set_facecolor(WHITE)
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.6, "SchoolDiary (Case 111) — UML Use Case Model", 
            ha='center', va='center', fontsize=14, fontweight='bold', color=NAVY)
    ax.text(7, 9.25, "System Boundary, Primary Human Actors, Secondary Push Gateway & Key Relationships", 
            ha='center', va='center', fontsize=9, color=SLATE)

    # System boundary box
    sys_box = patches.FancyBboxPatch((2.6, 0.4), 8.8, 8.4, boxstyle="round,pad=0.1,rounding_size=0.2",
                                     facecolor="#F8FAFC", edgecolor=NAVY, linewidth=2.0)
    ax.add_patch(sys_box)
    ax.text(2.9, 8.55, "System Boundary: SchoolDiary Platform", fontsize=10, fontweight='bold', color=NAVY)

    # Actors (Left)
    def draw_actor(x, y, name, role_desc):
        # Head
        head = plt.Circle((x, y + 0.35), 0.15, facecolor=LIGHT_GREY, edgecolor=NAVY, linewidth=1.5)
        ax.add_patch(head)
        # Body
        ax.plot([x, x], [y + 0.2, y - 0.15], color=NAVY, lw=1.5)
        # Arms
        ax.plot([x - 0.2, x + 0.2], [y + 0.08, y + 0.08], color=NAVY, lw=1.5)
        # Legs
        ax.plot([x, x - 0.15], [y - 0.15, y - 0.45], color=NAVY, lw=1.5)
        ax.plot([x, x + 0.15], [y - 0.15, y - 0.45], color=NAVY, lw=1.5)
        # Label
        ax.text(x, y - 0.65, name, ha='center', va='top', fontsize=8.5, fontweight='bold', color=NAVY)
        ax.text(x, y - 0.85, role_desc, ha='center', va='top', fontsize=7, color=SLATE)

    draw_actor(1.1, 7.8, "Teacher", "Class / Subject")
    draw_actor(1.1, 5.7, "Parent", "Enrolled Child")
    draw_actor(1.1, 3.6, "School Admin", "Campus Office")
    draw_actor(1.1, 1.7, "Principal", "Override Approver")

    # Secondary Actor (Right)
    draw_actor(12.8, 5.0, "Push Gateway", "FCM Adapter")
    draw_actor(12.8, 2.0, "Management", "Group Head")

    # Use Cases (Ovals)
    use_cases = [
        # (id, name, x, y, width, height, color)
        ("login", "Sign In (Role-Scoped)", 4.2, 8.0, 2.2, 0.55, TEAL),
        ("notice", "Publish Class Notice", 4.2, 6.9, 2.3, 0.55, NAVY),
        ("school_notice", "Publish School Notice", 4.2, 5.8, 2.3, 0.55, NAVY),
        ("admin_appr", "Approve School Notice", 7.2, 5.8, 2.3, 0.55, CORAL),
        ("read_rec", "Track Read Receipts", 7.2, 6.9, 2.2, 0.55, TEAL),
        ("remind", "Remind Unread Parents", 10.0, 6.9, 2.0, 0.5, TEAL),
        ("view_not", "View Notice & Receipts", 4.2, 4.7, 2.3, 0.55, TEAL),
        ("hw", "Post / Ack Homework", 4.2, 3.7, 2.2, 0.55, NAVY),
        ("att", "Mark Attendance Alert (15m)", 4.2, 2.7, 2.4, 0.55, CORAL),
        ("fee", "Read-Only Fee Reminder", 4.2, 1.7, 2.2, 0.55, TEAL),
        ("msg", "Send Two-Way Message", 7.2, 4.5, 2.3, 0.55, NAVY),
        ("hours", "Check Window (07:00-19:59)", 7.2, 3.4, 2.4, 0.55, CORAL),
        ("urgent", "Urgent Message Override", 10.0, 4.5, 2.1, 0.55, CORAL),
        ("pr_appr", "Principal Approval", 10.0, 3.4, 2.0, 0.55, CORAL),
        ("auto_rep", "After-Hours Auto-Reply", 7.2, 2.3, 2.3, 0.55, TEAL),
        ("csv", "Bulk CSV Roster Import", 7.2, 1.2, 2.3, 0.55, NAVY),
        ("reports", "Audit & Compliance KPI", 10.0, 1.8, 2.1, 0.55, NAVY),
        ("push", "Deliver Push Notification", 10.0, 8.0, 2.2, 0.55, TEAL)
    ]

    uc_dict = {}
    for uid, name, x, y, w, h, col in use_cases:
        ellipse = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.08,rounding_size=0.25",
                                          facecolor=WHITE, edgecolor=col, linewidth=1.5)
        ax.add_patch(ellipse)
        ax.text(x, y, name, ha='center', va='center', fontsize=7.2, fontweight='bold', color=NAVY)
        uc_dict[uid] = (x, y, w, h)

    # Actor to Use Case Associations
    def link_actor(ax_pos, uc_id):
        x1, y1 = ax_pos
        x2, y2, w2, h2 = uc_dict[uc_id]
        ax.plot([x1, x2 - w2/2], [y1, y2], color=SLATE, lw=1.1, zorder=1)

    # Teacher links
    link_actor((1.4, 7.8), "notice")
    link_actor((1.4, 7.8), "school_notice")
    link_actor((1.4, 7.8), "read_rec")
    link_actor((1.4, 7.8), "hw")
    link_actor((1.4, 7.8), "att")
    link_actor((1.4, 7.8), "msg")

    # Parent links
    link_actor((1.4, 5.7), "view_not")
    link_actor((1.4, 5.7), "hw")
    link_actor((1.4, 5.7), "msg")

    # Admin links
    link_actor((1.4, 3.6), "admin_appr")
    link_actor((1.4, 3.6), "fee")
    link_actor((1.4, 3.6), "csv")

    # Principal links
    link_actor((1.4, 1.7), "pr_appr")

    # Management links
    ax.plot([12.5, uc_dict["reports"][0] + uc_dict["reports"][2]/2], [2.0, uc_dict["reports"][1]], color=SLATE, lw=1.1)

    # Push Gateway links
    ax.plot([12.5, uc_dict["push"][0] + uc_dict["push"][2]/2], [5.0, uc_dict["push"][1]], color=SLATE, lw=1.1)

    # <<include>> and <<extend>> dashed arrows
    def draw_rel(src_id, dst_id, text, is_extend=False):
        x1, y1, w1, h1 = uc_dict[src_id]
        x2, y2, w2, h2 = uc_dict[dst_id]
        col = CORAL if is_extend else TEAL
        ax.annotate('', xy=(x2, y2 + h2/2 if y1 < y2 else y2 - h2/2 if y1 > y2 else y2),
                    xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=col, linestyle="--", lw=1.2, shrinkA=8, shrinkB=8))
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 0.12, f"«{text}»", fontsize=6.5, fontweight='bold', color=col, ha='center',
                bbox=dict(boxstyle="square,pad=0.1", fc=WHITE, ec="none", alpha=0.85))

    draw_rel("school_notice", "admin_appr", "include")
    draw_rel("msg", "hours", "include")
    draw_rel("notice", "hours", "include")
    draw_rel("urgent", "msg", "extend", is_extend=True)
    draw_rel("urgent", "pr_appr", "include")
    draw_rel("remind", "read_rec", "extend", is_extend=True)
    draw_rel("auto_rep", "msg", "extend", is_extend=True)
    draw_rel("notice", "push", "include")
    draw_rel("att", "push", "include")
    draw_rel("fee", "push", "include")

    out = os.path.join(DIAGRAMS_DIR, "uml_use_case.png")
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out)


# ══════════════════════════════════════════════════════════════════════════════
# 2. CLASS DIAGRAM
# ══════════════════════════════════════════════════════════════════════════
def make_class_diagram():
    fig, ax = plt.subplots(figsize=(12.0, 8.5), dpi=300)
    ax.set_facecolor(WHITE)
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(7, 9.7, "SchoolDiary (Case 111) — UML Class Diagram", 
            ha='center', va='center', fontsize=14, fontweight='bold', color=NAVY)
    ax.text(7, 9.35, "Domain Models, Architectural Entities & Event-Driven Loose Coupling Proof", 
            ha='center', va='center', fontsize=9, color=SLATE)

    def draw_class(x, y, w, h, name, attrs, methods, header_col=NAVY):
        # Header box
        header_h = 0.4
        box_header = patches.Rectangle((x - w/2, y + h/2 - header_h), w, header_h,
                                       facecolor=header_col, edgecolor=BORDER_DARK, linewidth=1.2)
        ax.add_patch(box_header)
        ax.text(x, y + h/2 - header_h/2, name, ha='center', va='center', fontsize=7.5, fontweight='bold', color=WHITE)

        # Body box
        body_h = h - header_h
        box_body = patches.Rectangle((x - w/2, y - h/2), w, body_h,
                                     facecolor="#F8FAFC", edgecolor=BORDER_DARK, linewidth=1.2)
        ax.add_patch(box_body)

        # Separator line inside body if methods exist
        attr_text = "\n".join(attrs)
        meth_text = "\n".join(methods)
        ax.text(x - w/2 + 0.1, y + h/2 - header_h - 0.15, attr_text, va='top', fontsize=6.2, color=SLATE)
        if methods:
            ax.axhline(y - 0.05, xmin=(x - w/2)/14, xmax=(x + w/2)/14, color=MID_GREY, lw=0.8)
            ax.text(x - w/2 + 0.1, y - 0.15, meth_text, va='top', fontsize=6.2, color=NAVY)

    # 1. Structural entities (Left column)
    draw_class(1.8, 8.0, 2.4, 1.4, "School", ["+ schoolId: String", "+ name: String", "+ principalId: String"], ["+ addClass()"])
    draw_class(1.8, 5.8, 2.4, 1.6, "ClassSection", ["+ sectionId: String", "+ grade: int", "+ division: String", "+ classTeacherId: String"], ["+ getStudents(): List"])
    draw_class(1.8, 3.5, 2.4, 1.6, "Student", ["+ studentId: String", "+ name: String", "+ sectionId: String", "+ parentIds: List"], ["+ getGuardian()"])
    draw_class(1.8, 1.4, 2.4, 1.6, "Parent", ["+ parentId: String", "+ name: String", "+ maskedPhone: String", "+ deviceToken: String"], ["+ getChildren(): List"])

    # 2. Functional entities (Center-Left)
    draw_class(5.0, 8.0, 2.5, 1.7, "Notice", ["+ noticeId: String", "+ title: String", "+ scope: NoticeScope", "+ status: NoticeStatus"], ["+ submit()", "+ publish()"])
    draw_class(5.0, 5.8, 2.5, 1.5, "ReadReceipt", ["+ noticeId: String", "+ parentId: String", "+ deliveredAt: DateTime", "+ readAt: DateTime"], ["+ markRead()"])
    draw_class(5.0, 3.8, 2.5, 1.4, "AttendanceRecord", ["+ studentId: String", "+ date: Date", "+ status: Present/Absent", "+ alertSentAt: DateTime"], ["+ markAbsent()"])
    draw_class(5.0, 1.8, 2.5, 1.4, "FeeReminder", ["+ studentId: String", "+ dueDate: Date", "+ daysBefore: 7|1", "+ sentAt: DateTime"], ["+ scheduleReminder()"])

    # 3. Messaging entities (Center-Right)
    draw_class(8.4, 8.0, 2.6, 1.7, "Message", ["+ messageId: String", "+ senderRole: Role", "+ body: String", "+ isUrgent: bool", "+ status: MessageStatus"], ["+ submit()", "+ markDelivered()"])
    draw_class(8.4, 5.8, 2.6, 1.5, "ApprovalRequest", ["+ requestId: String", "+ targetType: Notice|Msg", "+ approver: Admin|Principal", "+ status: ApprovalState"], ["+ decide(approved)"])
    draw_class(8.4, 3.8, 2.6, 1.5, "MessagingPolicy", ["+ windowStart = 07:00", "+ windowEnd = 19:59"], ["+ canSendNow(): Decision", "+ getNextWindowOpen()"], header_col=CORAL)
    draw_class(8.4, 1.8, 2.6, 1.4, "AuditEntry", ["+ entryId: String", "+ actorId: String", "+ action: String", "+ occurredAt: DateTime"], ["+ logImmutable()"])

    # 4. Service / Dispatcher Layer (Right column - Loose Coupling Highlight)
    draw_class(12.0, 8.0, 2.6, 1.6, "NoticeService", ["- notices: List", "- policy: Policy"], ["+ composeNotice()", "+ submitNotice()"], header_col=TEAL)
    draw_class(12.0, 6.0, 2.6, 1.6, "MessagingService", ["- threads: List", "- policy: Policy"], ["+ sendMessage()", "+ processAutoReply()"], header_col=TEAL)
    draw_class(12.0, 3.8, 2.6, 1.7, "NotificationDispatcher", ["- pushAdapter: Gateway"], ["+ onNoticePublished(e)", "+ onMessageReady(e)", "+ fanOutPush()"], header_col=NAVY)
    draw_class(12.0, 1.6, 2.6, 1.4, "PushGateway (Interface)", ["<<interface>>"], ["+ push(token, payload)"], header_col=BORDER_DARK)

    # Connections
    # Composition / Aggregation lines
    ax.plot([1.8, 1.8], [7.2, 6.6], color=NAVY, lw=1.2)  # School -> ClassSection
    ax.plot([1.8, 1.8], [5.0, 4.3], color=NAVY, lw=1.2)  # ClassSection -> Student
    ax.plot([1.8, 1.8], [2.7, 2.2], color=NAVY, lw=1.2)  # Student <-> Parent

    # Notice -> ReadReceipt
    ax.plot([5.0, 5.0], [7.15, 6.55], color=NAVY, lw=1.2)

    # Loose coupling event arrows (NoticeService & MessagingService -> Dispatcher)
    ax.annotate('NoticePublished event', xy=(12.0, 4.65), xytext=(12.0, 7.2),
                arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.5, linestyle="--"),
                fontsize=6.5, color=CORAL, fontweight='bold', ha='right')
    ax.annotate('MessageReady event', xy=(12.0, 4.65), xytext=(12.0, 5.2),
                arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.5, linestyle="--"),
                fontsize=6.5, color=CORAL, fontweight='bold', ha='right')
    ax.annotate('uses', xy=(12.0, 2.3), xytext=(12.0, 2.95),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.2),
                fontsize=6.5, color=NAVY, ha='right')

    # Box highlighting zero direct coupling
    decouple_box = patches.FancyBboxPatch((10.5, 0.4), 3.2, 0.6, boxstyle="round,pad=0.05,rounding_size=0.1",
                                          facecolor="#FDF2F0", edgecolor=CORAL, linewidth=1.2)
    ax.add_patch(decouple_box)
    ax.text(12.1, 0.7, "LOOSE COUPLING VERIFIED:\nNotice & Messaging have 0 direct links", 
            ha='center', va='center', fontsize=6.8, fontweight='bold', color=CORAL)

    out = os.path.join(DIAGRAMS_DIR, "uml_class_diagram.png")
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out)


# ══════════════════════════════════════════════════════════════════════════════
# 3. SEQUENCE DIAGRAM: SEND A NOTICE AND TRACK READ RECEIPTS
# ══════════════════════════════════════════════════════════════════════════
def make_sequence_diagram():
    fig, ax = plt.subplots(figsize=(11.5, 7.5), dpi=300)
    ax.set_facecolor(WHITE)
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(5.5, 9.7, "UML Sequence Diagram: Send Notice & Track Read Receipts", 
            ha='center', va='center', fontsize=13, fontweight='bold', color=NAVY)
    ax.text(5.5, 9.35, "Covers FR-02 (Notices), FR-03 (Read Receipts), Approval Flow & Messaging Window Governance", 
            ha='center', va='center', fontsize=8.5, color=SLATE)

    # Lifelines
    lifelines = [
        ("Teacher", 1.0),
        ("NoticeService", 2.5),
        ("SchoolAdmin", 4.0),
        ("MessagingPolicy", 5.5),
        ("Dispatcher", 7.0),
        ("PushGateway", 8.5),
        ("Parent", 10.0)
    ]

    for name, x in lifelines:
        box = patches.FancyBboxPatch((x - 0.65, 8.8), 1.3, 0.38, boxstyle="round,pad=0.05,rounding_size=0.08",
                                     facecolor=NAVY, edgecolor=BORDER_DARK, linewidth=1.0)
        ax.add_patch(box)
        ax.text(x, 9.0, name, ha='center', va='center', fontsize=7.2, fontweight='bold', color=WHITE)
        ax.plot([x, x], [0.6, 8.8], color=MID_GREY, linestyle="--", lw=1.0)

    # Message sequence steps
    def draw_msg(t, x1, x2, label, is_return=False, is_async=False, col=NAVY):
        arrow = "<-" if is_return else ("-|>" if not is_async else "->")
        style = "--" if is_return else "-"
        ax.annotate('', xy=(x2, t), xytext=(x1, t),
                    arrowprops=dict(arrowstyle=arrow, color=col, linestyle=style, lw=1.2))
        ax.text((x1 + x2)/2, t + 0.1, label, ha='center', va='bottom', fontsize=6.8, color=col, fontweight='bold')

    # 1. Compose
    draw_msg(8.4, 1.0, 2.5, "1. submit(noticeDraft)")
    # 2. Approval Request for School Scope
    draw_msg(7.8, 2.5, 4.0, "2. [if school scope] createApprovalRequest()")
    draw_msg(7.3, 4.0, 2.5, "3. approve(requestId)", is_return=True, col=CORAL)
    # 3. Time Check
    draw_msg(6.7, 2.5, 5.5, "4. canSendNow(TEACHER, now)")
    draw_msg(6.2, 5.5, 2.5, "5. ALLOW [07:00-19:59 IST]", is_return=True, col=TEAL)
    # 4. Publish Event
    draw_msg(5.6, 2.5, 7.0, "6. emit NoticePublished(id, audience)", is_async=True, col=CORAL)
    # 5. Push Gateway
    draw_msg(5.0, 7.0, 8.5, "7. push(token, payload, idempotencyKey)")
    # 6. Delivery to Parent
    draw_msg(4.4, 8.5, 10.0, "8. push notification delivered")
    # 7. Parent Reads
    draw_msg(3.7, 10.0, 2.5, "9. openNotice() -> recordReadReceipt(<=60s)", col=TEAL)
    # 8. Teacher views read status
    draw_msg(3.0, 1.0, 2.5, "10. viewReadStatus(noticeId)")
    draw_msg(2.4, 2.5, 1.0, "11. return read% (e.g. 60%) & unread list", is_return=True)
    # 9. Remind unread
    draw_msg(1.7, 1.0, 2.5, "12. [opt] remindUnread(noticeId)", col=CORAL)
    draw_msg(1.1, 2.5, 7.0, "13. emit NoticeReminderPublished(unreadOnly)", is_async=True, col=CORAL)

    out = os.path.join(DIAGRAMS_DIR, "uml_sequence_notice.png")
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out)


# ══════════════════════════════════════════════════════════════════════════════
# 4. ACTIVITY DIAGRAM: TEACHER SENDS A MESSAGE
# ══════════════════════════════════════════════════════════════════════════
def make_activity_diagram():
    fig, ax = plt.subplots(figsize=(9.0, 8.0), dpi=300)
    ax.set_facecolor(WHITE)
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(5, 9.7, "UML Activity Diagram: Send Message Business Workflow", 
            ha='center', va='center', fontsize=13, fontweight='bold', color=NAVY)
    ax.text(5, 9.35, "Covers FR-06, FR-08 Window Logic (07:00-19:59), Overnight Queueing & Urgent Principal Override", 
            ha='center', va='center', fontsize=8.2, color=SLATE)

    # Initial node (Filled circle)
    start = plt.Circle((5, 8.8), 0.16, facecolor=NAVY, edgecolor=BORDER_DARK)
    ax.add_patch(start)
    ax.text(5, 9.05, "Start", ha='center', fontsize=7.5, fontweight='bold', color=NAVY)

    # Arrow down
    def flow(x1, y1, x2, y2, label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.3))
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            ax.text(mx + 0.15, my, label, fontsize=7.0, fontweight='bold', color=CORAL, va='center')

    # Activity: Teacher writes message
    def act_box(x, y, w, h, text, bg=WHITE, border=NAVY):
        box = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                                     facecolor=bg, edgecolor=border, linewidth=1.3)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=7.2, color=NAVY, fontweight='bold')

    # Decision diamond
    def decision(x, y, text):
        diamond = patches.Polygon([[x, y + 0.4], [x + 0.9, y], [x, y - 0.4], [x - 0.9, y]],
                                  closed=True, facecolor="#FEF3C7", edgecolor=CORAL, linewidth=1.3)
        ax.add_patch(diamond)
        ax.text(x, y, text, ha='center', va='center', fontsize=6.8, fontweight='bold', color=NAVY)

    flow(5, 8.64, 5, 8.1)
    act_box(5, 7.8, 3.2, 0.55, "Teacher Writes Message & Taps Send")

    flow(5, 7.52, 5, 6.9)
    decision(5, 6.5, "Time inside\n07:00–19:59?")

    # Branch YES (In-window) -> Right
    ax.plot([5.9, 8.2], [6.5, 6.5], color=NAVY, lw=1.3)
    ax.plot([8.2, 8.2], [6.5, 3.2], color=NAVY, lw=1.3)
    ax.text(6.8, 6.65, "[Yes: In Window]", fontsize=6.8, fontweight='bold', color=TEAL)

    # Branch NO (Outside window 20:00-06:59) -> Down
    flow(5, 6.1, 5, 5.4, "[No: After 20:00]")
    decision(5, 5.0, "Marked\nURGENT?")

    # Urgent NO -> Queue for 07:00
    ax.plot([4.1, 2.2], [5.0, 5.0], color=NAVY, lw=1.3)
    ax.plot([2.2, 2.2], [5.0, 4.3], color=NAVY, lw=1.3)
    ax.text(3.0, 5.15, "[No: Routine]", fontsize=6.8, fontweight='bold', color=CORAL)
    act_box(2.2, 4.0, 2.6, 0.55, "Queue for Next Day 07:00\n(Status: QUEUED)", bg="#EEF2FF")

    # Urgent YES -> Request Principal Approval
    flow(5, 4.6, 5, 3.8, "[Yes: Urgent]")
    act_box(5, 3.5, 2.8, 0.55, "Route to Principal\nOverride Queue", bg="#FDF2F0", border=CORAL)

    flow(5, 3.22, 5, 2.6)
    decision(5, 2.2, "Principal\nApproved?")

    # Principal APPROVED -> Send now
    ax.plot([5.9, 8.2], [2.2, 2.2], color=NAVY, lw=1.3)
    ax.plot([8.2, 8.2], [2.2, 3.2], color=NAVY, lw=1.3)
    ax.text(6.8, 2.35, "[Approved]", fontsize=6.8, fontweight='bold', color=TEAL)

    # Principal REJECTED -> Queue
    ax.plot([4.1, 2.2], [2.2, 2.2], color=NAVY, lw=1.3)
    ax.plot([2.2, 2.2], [2.2, 3.7], color=NAVY, lw=1.3)
    ax.text(3.0, 2.35, "[Rejected/Timeout]", fontsize=6.8, fontweight='bold', color=CORAL)

    # Converge Queue to Wait until 07:00
    flow(2.2, 3.72, 2.2, 2.6)
    act_box(2.2, 2.3, 2.4, 0.5, "Wait until 07:00 AM\nMorning Batch Release")
    ax.plot([2.2, 2.2], [2.05, 1.4], color=NAVY, lw=1.3)
    ax.plot([2.2, 8.2], [1.4, 1.4], color=NAVY, lw=1.3)

    # Send Box (Converged)
    act_box(8.2, 3.2, 2.6, 0.55, "Dispatch Immediately\n(Status: SENT)", bg="#ECFDF5", border=TEAL)
    flow(8.2, 2.92, 8.2, 2.2)

    act_box(8.2, 1.9, 2.6, 0.55, "NotificationDispatcher\nPushes to Parent Device")
    flow(8.2, 1.62, 8.2, 1.0)

    # Final Node (Bullseye)
    final_outer = plt.Circle((8.2, 0.7), 0.22, facecolor=WHITE, edgecolor=NAVY, lw=1.5)
    final_inner = plt.Circle((8.2, 0.7), 0.12, facecolor=NAVY, edgecolor=NAVY)
    ax.add_patch(final_outer)
    ax.add_patch(final_inner)
    ax.text(8.2, 0.35, "Message Delivered & Logged", ha='center', fontsize=7.2, fontweight='bold', color=NAVY)

    out = os.path.join(DIAGRAMS_DIR, "uml_activity_message.png")
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out)


# ══════════════════════════════════════════════════════════════════════════════
# 5. STATE DIAGRAM: MESSAGE LIFECYCLE
# ══════════════════════════════════════════════════════════════════════════
def make_state_diagram():
    fig, ax = plt.subplots(figsize=(11.0, 7.0), dpi=300)
    ax.set_facecolor(WHITE)
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    ax.text(6, 8.1, "UML Statechart: Message Finite State Machine (12 States)", 
            ha='center', va='center', fontsize=13, fontweight='bold', color=NAVY)
    ax.text(6, 7.75, "Formal state transitions covering Daytime window, Overnight Queueing, and Parent Auto-Replies", 
            ha='center', va='center', fontsize=8.5, color=SLATE)

    def state_box(x, y, w, h, name, bg="#F8FAFC", border=NAVY):
        box = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                                     facecolor=bg, edgecolor=border, linewidth=1.4)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=7.5, fontweight='bold', color=NAVY)

    # Start circle
    start = plt.Circle((1.0, 6.5), 0.15, facecolor=NAVY, edgecolor=BORDER_DARK)
    ax.add_patch(start)

    # States
    state_box(2.8, 6.5, 1.8, 0.6, "Draft")
    state_box(5.5, 6.5, 2.0, 0.6, "Submitted")
    state_box(9.2, 6.5, 1.8, 0.6, "Sent", bg="#ECFDF5", border=TEAL)
    state_box(9.2, 4.8, 1.8, 0.6, "Delivered", bg="#ECFDF5", border=TEAL)
    state_box(9.2, 3.2, 1.8, 0.6, "Read", bg="#ECFDF5", border=TEAL)

    state_box(5.5, 4.8, 2.0, 0.6, "Queued\n(for 07:00)", bg="#EEF2FF", border=CORAL)
    state_box(5.5, 3.2, 2.2, 0.6, "PendingApproval\n(Urgent Override)", bg="#FEF3C7", border=CORAL)

    state_box(11.0, 4.8, 1.6, 0.6, "Failed\n(retry <= 3)", bg="#FDF2F0", border=CORAL)

    # Parent night branch (Bottom)
    state_box(2.2, 1.6, 2.4, 0.6, "ReceivedAfterHours", bg="#FEF3C7")
    state_box(5.2, 1.6, 2.2, 0.6, "AutoReplied", bg="#E0F2FE")
    state_box(8.2, 1.6, 2.2, 0.6, "HeldForTeacher", bg="#EEF2FF")
    state_box(10.8, 1.6, 2.2, 0.6, "DeliveredToTeacher", bg="#ECFDF5", border=TEAL)

    # Transitions
    def trans(x1, y1, x2, y2, label="", rad=0.0, col=NAVY):
        conn = f"arc3,rad={rad}" if rad != 0 else "arc3,rad=0"
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.2, connectionstyle=conn))
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            ax.text(mx, my + 0.12, label, fontsize=6.2, fontweight='bold', color=col, ha='center',
                    bbox=dict(boxstyle="square,pad=0.1", fc=WHITE, ec="none", alpha=0.8))

    trans(1.15, 6.5, 1.9, 6.5)
    trans(3.7, 6.5, 4.5, 6.5, "taps Send")
    trans(6.5, 6.5, 8.3, 6.5, "in-window (07:00-19:59)", col=TEAL)
    trans(5.5, 6.2, 5.5, 5.1, "routine, after 20:00", col=CORAL)
    trans(5.5, 6.2, 5.5, 3.5, "urgent, after 20:00", rad=-0.2, col=CORAL)

    trans(6.5, 4.8, 8.3, 6.5, "07:00 batch release", rad=0.1, col=TEAL)
    trans(6.6, 3.2, 8.3, 6.5, "Principal approves", rad=-0.1, col=TEAL)
    trans(5.5, 3.5, 5.5, 4.5, "Principal rejects/timeout", col=CORAL)

    trans(9.2, 6.2, 9.2, 5.1, "push accepted")
    trans(9.2, 4.5, 9.2, 3.5, "parent opens")

    trans(9.2, 6.2, 10.2, 4.8, "push error", col=CORAL)
    trans(10.2, 5.1, 9.2, 6.5, "retry attempts <= 3", rad=-0.1, col=CORAL)

    # Final circle for Read
    end_read = plt.Circle((9.2, 2.2), 0.16, facecolor=WHITE, edgecolor=NAVY, lw=1.5)
    end_read_in = plt.Circle((9.2, 2.2), 0.09, facecolor=NAVY)
    ax.add_patch(end_read)
    ax.add_patch(end_read_in)
    trans(9.2, 2.9, 9.2, 2.36)

    # Parent transitions
    trans(3.4, 1.6, 4.1, 1.6, "parent sends")
    trans(6.3, 1.6, 7.1, 1.6, "instant SMS/bot reply")
    trans(9.3, 1.6, 9.7, 1.6, "at 07:00 AM")

    # Header label for branches
    ax.text(5.5, 7.2, "--- TEACHER / SYSTEM MESSAGING PIPELINE ---", fontsize=7.5, fontweight='bold', color=NAVY, ha='center')
    ax.text(6.0, 2.4, "--- PARENT OUT-OF-HOURS RECEPTION PIPELINE (24/7 OPEN) ---", fontsize=7.5, fontweight='bold', color=SLATE, ha='center')

    out = os.path.join(DIAGRAMS_DIR, "uml_state_message.png")
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out)


if __name__ == "__main__":
    print("Generating UML diagrams for SchoolDiary Case 111...")
    make_use_case_diagram()
    make_class_diagram()
    make_sequence_diagram()
    make_activity_diagram()
    make_state_diagram()
    print("All 5 UML diagrams generated successfully in diagrams/!")
