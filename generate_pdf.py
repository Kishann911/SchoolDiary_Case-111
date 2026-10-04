"""
SchoolDiary Case 111 — Complete Project PDF Generator
Executive-grade professional theme: clean white, slate navy accents, coral highlights, muted teal tables.
Includes dynamically calculated TOC page numbers and embedded high-res diagrams.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Image, Flowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas as pdfcanvas
import os

PAGE_W, PAGE_H = A4
MARGIN = 2.0 * cm
INNER_W = PAGE_W - 2 * MARGIN

# ─── COLOUR PALETTE ────────────────────────────────────────────────────────────
NAVY       = colors.HexColor("#1B2A4A")   # Deep slate navy – headers, accents
CORAL      = colors.HexColor("#E05A4E")   # Warm coral – section tags, critical path, highlights
TEAL       = colors.HexColor("#2D7D8E")   # Muted teal – table headers, rules
SLATE      = colors.HexColor("#4A5568")   # Slate grey – body text
LIGHT_GREY = colors.HexColor("#F7F9FC")   # Page accent backgrounds
MID_GREY   = colors.HexColor("#CBD5E0")   # Table borders, rules
WHITE      = colors.white
BLACK      = colors.HexColor("#1A1A1A")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIAGRAMS_DIR = os.path.join(SCRIPT_DIR, "diagrams")
OUTPUT = os.path.join(SCRIPT_DIR, "SchoolDiary_Case111_Full_Report.pdf")

# ─── PAGE TRACKER FLOWABLE ─────────────────────────────────────────────────────
class PageTracker(Flowable):
    """Zero-size flowable that records its current page number into a dictionary."""
    def __init__(self, key, registry):
        super().__init__()
        self.key = key
        self.registry = registry
        self.width = 0
        self.height = 0

    def draw(self):
        self.registry[self.key] = self.canv._pageNumber

# ─── NUMBERED CANVAS FOR HEADER/FOOTER ─────────────────────────────────────────
class NumberedCanvas(pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        pg = self._pageNumber
        if pg == 1:
            self.restoreState()
            return

        # Top Running Header
        self.setFont('Helvetica-Bold', 7.5)
        self.setFillColor(NAVY)
        self.drawString(MARGIN, PAGE_H - 1.2*cm, "SchoolDiary  |  Case Study #111")
        self.setFont('Helvetica', 7.5)
        self.setFillColor(SLATE)
        self.drawRightString(PAGE_W - MARGIN, PAGE_H - 1.2*cm, "Software Engineering & Project Management")
        self.setStrokeColor(MID_GREY)
        self.setLineWidth(0.4)
        self.line(MARGIN, PAGE_H - 1.35*cm, PAGE_W - MARGIN, PAGE_H - 1.35*cm)

        # Bottom Navy Bar
        self.setFillColor(NAVY)
        self.rect(0, 0, PAGE_W, 1.0*cm, fill=1, stroke=0)
        
        # Bottom text
        self.setFont('Helvetica', 8)
        self.setFillColor(WHITE)
        self.drawCentredString(PAGE_W/2, 0.35*cm, f"SchoolDiary · Case 111 · Kishan Ojha   |   Page {pg} of {page_count}")
        
        self.setFont('Helvetica', 7)
        self.setFillColor(MID_GREY)
        self.drawString(MARGIN, 0.35*cm, "B.Tech CSE 2025–29 · Semester III")
        self.restoreState()

# ─── STYLES ────────────────────────────────────────────────────────────────────
def build_styles():
    s = {}
    base = getSampleStyleSheet()

    s['cover_title'] = ParagraphStyle('cover_title',
        fontName='Helvetica-Bold', fontSize=28, leading=34,
        textColor=NAVY, spaceAfter=6)

    s['cover_sub'] = ParagraphStyle('cover_sub',
        fontName='Helvetica', fontSize=12.5, leading=17,
        textColor=SLATE, spaceAfter=4)

    s['section_tag'] = ParagraphStyle('section_tag',
        fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=WHITE)

    s['h1'] = ParagraphStyle('h1',
        fontName='Helvetica-Bold', fontSize=17, leading=21,
        textColor=NAVY, spaceBefore=12, spaceAfter=6)

    s['h2'] = ParagraphStyle('h2',
        fontName='Helvetica-Bold', fontSize=12, leading=16,
        textColor=NAVY, spaceBefore=10, spaceAfter=5)

    s['h3'] = ParagraphStyle('h3',
        fontName='Helvetica-Bold', fontSize=10, leading=14,
        textColor=TEAL, spaceBefore=8, spaceAfter=4)

    s['body'] = ParagraphStyle('body',
        fontName='Helvetica', fontSize=9, leading=13.5,
        textColor=SLATE, spaceBefore=2.5, spaceAfter=2.5,
        alignment=TA_JUSTIFY)

    s['body_bold'] = ParagraphStyle('body_bold',
        fontName='Helvetica-Bold', fontSize=9, leading=13.5,
        textColor=NAVY, spaceBefore=2.5, spaceAfter=2.5)

    s['caption'] = ParagraphStyle('caption',
        fontName='Helvetica-Oblique', fontSize=7.8, leading=11,
        textColor=SLATE, alignment=TA_CENTER, spaceBefore=3, spaceAfter=6)

    s['highlight'] = ParagraphStyle('highlight',
        fontName='Helvetica-Bold', fontSize=9, leading=13.5,
        textColor=CORAL, spaceBefore=3, spaceAfter=3)

    return s

# ─── TABLE & UI HELPERS ────────────────────────────────────────────────────────
def make_table(headers, rows, col_widths, st):
    """Build a professional minimalist table with teal header and alternating rows."""
    header_para = [Paragraph(f'<b>{h}</b>', ParagraphStyle('th',
        fontName='Helvetica-Bold', fontSize=8, leading=11,
        textColor=WHITE, alignment=TA_LEFT)) for h in headers]
    data = [header_para]
    for i, row in enumerate(rows):
        para_row = []
        for cell in row:
            para_row.append(Paragraph(str(cell), ParagraphStyle('td',
                fontName='Helvetica', fontSize=8, leading=11.5,
                textColor=SLATE if i % 2 == 0 else BLACK, alignment=TA_LEFT)))
        data.append(para_row)

    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1,  0), TEAL),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ('GRID',          (0, 0), (-1, -1), 0.35, MID_GREY),
        ('TOPPADDING',    (0, 0), (-1, -1), 3.8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.8),
        ('LEFTPADDING',   (0, 0), (-1, -1), 4.0),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 4.0),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
    ]))
    return tbl

def coral_rule():
    return HRFlowable(width=3.5*cm, thickness=2.2, color=CORAL, spaceAfter=8, spaceBefore=2)

def section_badge(text, st):
    badge = Table([[Paragraph(text, st['section_tag'])]], colWidths=[2.8*cm])
    badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CORAL),
        ('TOPPADDING',  (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING',(0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING',(0,0), (-1,-1), 5),
        ('ROUNDEDCORNERS', [2]),
    ]))
    return badge

def navy_box(content_list):
    inner = Table([[c] for c in content_list], colWidths=[INNER_W - 0.8*cm])
    inner.setStyle(TableStyle([
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('TOPPADDING',    (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LINEBEFORE',    (0,0), (-1,-1), 3, CORAL),
        ('BACKGROUND',    (0,0), (-1,-1), LIGHT_GREY),
    ]))
    return inner

def image_box(img_path, width_cm, height_cm, caption_text, st):
    if not os.path.exists(img_path):
        return Paragraph(f"<i>[Diagram missing: {os.path.basename(img_path)}]</i>", st['caption'])
    img = Image(img_path, width=width_cm*cm, height=height_cm*cm)
    tbl = Table([[img]], colWidths=[width_cm*cm])
    tbl.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, MID_GREY),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    return KeepTogether([
        Spacer(1, 4),
        tbl,
        Paragraph(caption_text, st['caption']),
        Spacer(1, 4)
    ])

# ─── TOC BUILDER ───────────────────────────────────────────────────────────────
def build_toc_table(page_map, st):
    """Build a balanced, compact 2-column TOC table that fits cleanly on Page 2."""
    left_items = [
        ('1', 'Software Requirements Specification', page_map.get('s1', '3'), True),
        ('1.1', 'Purpose, Scope & Definitions', page_map.get('s1_1', '3'), False),
        ('1.2', 'Users & System Constraints', page_map.get('s1_2', '3'), False),
        ('1.3', 'Functional Requirements (FR-01 to 10)', page_map.get('s1_3', '4'), False),
        ('1.4', 'Measurable Non-Functional Reqs (NFR-01 to 06)', page_map.get('s1_4', '4'), False),
        ('1.5', 'Messaging-Hours Rule (FR-08)', page_map.get('s1_5', '5'), False),
        ('1.6', 'MoSCoW Priorities & Traceability Matrix', page_map.get('s1_6', '5'), False),
        ('2', 'UML Design Package', page_map.get('s2', '6'), True),
        ('2.1', 'Use-Case Model & Actors', page_map.get('s2_1', '6'), False),
        ('2.2', 'Class Model & Domain Architecture', page_map.get('s2_2', '6'), False),
        ('2.3', 'Sequence: Send Notice & Track Receipts', page_map.get('s2_3', '7'), False),
        ('2.4', 'Activity: Teacher Sends a Message', page_map.get('s2_4', '7'), False),
        ('2.5', 'State Diagram: Message Lifecycle', page_map.get('s2_5', '8'), False),
        ('2.6', 'Cohesion & Loose Coupling Rationale', page_map.get('s2_6', '8'), False),
        ('3', 'Project Plan', page_map.get('s3', '10'), True),
        ('3.1', 'Work Breakdown Structure (WBS)', page_map.get('s3_1', '10'), False),
        ('3.2', 'Network Diagram & Critical Path (CPM)', page_map.get('s3_2', '10'), False),
        ('3.3', 'Milestones & Gantt Schedule', page_map.get('s3_3', '11'), False),
        ('3.4', 'Resource Allocation & Utilisation', page_map.get('s3_4', '11'), False),
        ('4', 'Estimation Sheet', page_map.get('s4', '12'), True),
        ('4.1', 'Inputs & Stated Assumptions', page_map.get('s4_1', '12'), False),
        ('4.2', 'Step-by-Step Calculations & Formulas', page_map.get('s4_2', '12'), False),
        ('4.3', 'Confidence Level & Estimate vs Promise', page_map.get('s4_3', '13'), False),
    ]

    right_items = [
        ('5', 'Scope Management', page_map.get('s5', '14'), True),
        ('5.1', 'Pilot Scope Statement (2 Schools)', page_map.get('s5_1', '14'), False),
        ('5.2', 'Scope Boundary & Time/Cost/Quality Impact', page_map.get('s5_2', '14'), False),
        ('5.3', 'Scope-Change Control Procedure', page_map.get('s5_3', '15'), False),
        ('6', 'Test Plan & Evidence', page_map.get('s6', '16'), True),
        ('6.1', 'IEEE 829-lite Test Strategy & Roles', page_map.get('s6_1', '16'), False),
        ('6.2', 'System Test Cases TC-01 to TC-10', page_map.get('s6_2', '16'), False),
        ('6.3', 'Equivalence Classes (EC-T1 to TC-EC-11)', page_map.get('s6_3', '17'), False),
        ('6.4', 'Boundary Value Analysis (TC-BVA-01 to 18)', page_map.get('s6_4', '17'), False),
        ('6.5', 'Decision Table for Messaging-Hours (R1 to R13)', page_map.get('s6_5', '18'), False),
        ('6.6', 'Test Log, Severity & Defect Log', page_map.get('s6_6', '19'), False),
        ('6.7', 'DRE & Defect Density Calculations', page_map.get('s6_7', '20'), False),
        ('7', 'Risk Register & Issue Log', page_map.get('s7', '21'), True),
        ('7.1', 'Scoring & Probability × Impact Matrix', page_map.get('s7_1', '21'), False),
        ('7.2', 'Risk Register (8 Exposure-Ranked Risks)', page_map.get('s7_2', '21'), False),
        ('7.3', 'RMMM Plans for Top 3 Risks (R1, R2, R5)', page_map.get('s7_3', '22'), False),
        ('7.4', 'Issue Log & Separation Rationale', page_map.get('s7_4', '23'), False),
        ('8', 'Closure Note & Lessons Learned', page_map.get('s8', '24'), True),
        ('8.1', 'Pilot Results & Conditional Rollout Decision', page_map.get('s8_1', '24'), False),
        ('8.2', 'Lessons Learned (6 Retrospective Lessons)', page_map.get('s8_2', '24'), False),
        ('8.3', 'Formal Sign-Off Matrix', page_map.get('s8_3', '25'), False),
    ]

    def render_col(items):
        col_rows = []
        for num, title, pg, is_head in items:
            font_name = 'Helvetica-Bold' if is_head else 'Helvetica'
            font_size = 8.2 if is_head else 7.5
            color = NAVY if is_head else SLATE
            num_color = CORAL if is_head else TEAL
            
            p_num = Paragraph(num, ParagraphStyle('t_n', fontName='Helvetica-Bold', fontSize=font_size, textColor=num_color))
            p_txt = Paragraph(title, ParagraphStyle('t_t', fontName=font_name, fontSize=font_size, textColor=color))
            p_pg  = Paragraph(f"{pg}", ParagraphStyle('t_p', fontName='Helvetica-Bold' if is_head else 'Helvetica',
                                                      fontSize=font_size, textColor=color, alignment=TA_RIGHT))
            col_rows.append([p_num, p_txt, p_pg])
        
        t = Table(col_rows, colWidths=[0.9*cm, 6.4*cm, 0.9*cm])
        t.setStyle(TableStyle([
            ('TOPPADDING', (0,0), (-1,-1), 1.6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
            ('LEFTPADDING', (0,0), (-1,-1), 1),
            ('RIGHTPADDING', (0,0), (-1,-1), 1),
            ('LINEBELOW', (0,0), (-1,-1), 0.2, LIGHT_GREY),
        ]))
        return t

    left_tbl = render_col(left_items)
    right_tbl = render_col(right_items)

    main_toc = Table([[left_tbl, right_tbl]], colWidths=[INNER_W/2, INNER_W/2])
    main_toc.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    return main_toc

# ─── STORY GENERATION ──────────────────────────────────────────────────────────
def build_story(page_map, st):
    story = []

    # ── COVER PAGE ──────────────────────────────────────────────────────────────
    cover_bar = Table(
        [[Paragraph('CASE STUDY #111', ParagraphStyle('cb', fontName='Helvetica-Bold', fontSize=9, textColor=CORAL)),
          Paragraph('Software Engineering &amp; Project Management', ParagraphStyle('cb2', fontName='Helvetica', fontSize=9, textColor=WHITE, alignment=TA_RIGHT))]],
        colWidths=[INNER_W/2, INNER_W/2])
    cover_bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('TOPPADDING',  (0,0), (-1,-1), 10),
        ('BOTTOMPADDING',(0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING',(0,0), (-1,-1), 12),
    ]))
    story.append(cover_bar)
    story.append(Spacer(1, 2.5*cm))

    story.append(Paragraph('SchoolDiary', st['cover_title']))
    story.append(coral_rule())
    story.append(Paragraph('Parent–Teacher Communication App for a School Group', st['cover_sub']))
    story.append(Spacer(1, 0.8*cm))

    meta_data = [
        ['Case ID', '111'],
        ['Candidate Author', 'Kishan Ojha (Sole Contributor)'],
        ['Academic Programme', 'B.Tech Computer Science & Engineering (2025–2029)'],
        ['Curriculum Subject', 'Software Engineering &amp; Project Management — Semester III'],
        ['Pilot Scope', '2 Schools · 2,300 Parents · ~107 Teachers (16.4% Group Share)'],
        ['Engineering Budget', '3 Developers · 68 Person-Days · 27 Working Days Scheduled'],
        ['Deliverables Included', 'Full IEEE 830 SRS, UML Suite, CPM Plan, Estimation, Scope, IEEE 829 Tests, Risk Register, Closure Note'],
    ]
    meta_rows = [[Paragraph(f'<b>{k}</b>', ParagraphStyle('mk', fontName='Helvetica-Bold', fontSize=8.5, textColor=NAVY)),
                  Paragraph(v, ParagraphStyle('mv', fontName='Helvetica', fontSize=8.5, textColor=SLATE))]
                 for k, v in meta_data]
    meta_tbl = Table(meta_rows, colWidths=[4.2*cm, INNER_W - 4.2*cm])
    meta_tbl.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [LIGHT_GREY, WHITE]),
        ('TOPPADDING',    (0,0), (-1,-1), 6.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6.5),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('LINEBEFORE',    (0,0), (-1,-1), 3, TEAL),
        ('GRID',          (0,0), (-1,-1), 0.3, MID_GREY),
    ]))
    story.append(meta_tbl)
    story.append(Spacer(1, 1.8*cm))

    story.append(navy_box([
        Paragraph('<b>Executive Problem Statement</b>', ParagraphStyle('pb', fontName='Helvetica-Bold', fontSize=9.5, textColor=NAVY)),
        Spacer(1, 3),
        Paragraph(
            'A group of 12 schools communicates with parents through paper diaries, circulars and dozens '
            'of WhatsApp groups run by individual teachers. Parents miss critical circulars, teachers receive messages late at night, '
            'and management maintains zero centralized audit trail. The group commissioned SchoolDiary to provide reliable circulars, '
            'homework distribution, 15-minute attendance alerts, fee reminders, and structured two-way messaging strictly constrained within school hours.',
            ParagraphStyle('pb2', fontName='Helvetica', fontSize=8.8, leading=13.5, textColor=SLATE)),
    ]))
    story.append(Spacer(1, 1.5*cm))

    kf_data = [
        ['14,000 Parents', '650 Teachers', '12 Schools', '2,300 Pilot Parents', '16.4% Pilot Share'],
        ['68 Person-Days', '27 Working Days', 'Team of 3', '90% Monthly Active Target', '0 Late Messages Target'],
    ]
    kf_rows = [[Paragraph(f'<b>{c}</b>', ParagraphStyle('kf', fontName='Helvetica-Bold', fontSize=8, textColor=WHITE, alignment=TA_CENTER)) for c in row] for row in kf_data]
    kf_tbl = Table(kf_rows, colWidths=[INNER_W/5]*5)
    kf_tbl.setStyle(TableStyle([
        ('ROWBACKGROUNDS',(0,0), (-1,-1), [TEAL, NAVY]),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('GRID',          (0,0), (-1,-1), 0.5, WHITE),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(kf_tbl)
    story.append(PageBreak())

    # ── TABLE OF CONTENTS ───────────────────────────────────────────────────────
    story.append(Paragraph('Table of Contents', st['h1']))
    story.append(coral_rule())
    story.append(Spacer(1, 4))
    story.append(build_toc_table(page_map, st))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════════
    # SECTION 1 — SRS
    # ══════════════════════════════════════════════════════════════════════════════
    story.append(PageTracker('s1', page_map))
    story.append(section_badge('SECTION 01', st))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Software Requirements Specification (SRS)', st['h1']))
    story.append(Paragraph('IEEE 830-Style Specification · Baseline Version 1.1', ParagraphStyle('sub',
        fontName='Helvetica-Oblique', fontSize=8.5, textColor=SLATE, spaceAfter=6)))
    story.append(coral_rule())

    story.append(PageTracker('s1_1', page_map))
    story.append(Paragraph('1.1 Purpose, Scope & Baseline Group Figures', st['h2']))
    story.append(Paragraph(
        'This SRS formally specifies the requirements for SchoolDiary across 12 schools, establishing the contractual '
        'baseline for the UML architecture, critical-path project schedule, test plan, and pilot rollout. '
        'SchoolDiary is architected as an Android application for parents and teachers coupled with a secure web administration console.',
        st['body']))
    story.append(Spacer(1, 4))

    story.append(make_table(
        ['Metric / Constraint', 'Baseline Value', 'Exact Mathematical Derivation & Operational Context'],
        [
            ['Total Parent Base', '14,000 parents', 'Total registered parent body across all 12 institutions (given).'],
            ['Total Faculty Staff', '650 teachers', 'Total instructional staff across the group (given).'],
            ['Institutions in Scope', '12 schools', 'Group footprint; pilot restricted to 2 institutions (given).'],
            ['Pilot Parent Cohort', '2,300 parents', 'Active parent group across the 2 pilot schools (given).'],
            ['Pilot Share of Parents', '16.43% (≈ 16.4%)', '2,300 ÷ 14,000 = 0.1642857... exactly 16.43% of total population.'],
            ['Pilot Faculty Allocation', '~107 teachers', '650 × (2,300 ÷ 14,000) = 106.78 ≈ 107 teachers (proportional).'],
            ['Monthly Active Target (Pilot)', '2,070 parents', '90% × 2,300 pilot parents = 2,070 parents active monthly.'],
            ['Full Rollout Active Target', '12,600 parents', '90% × 14,000 group parents = 12,600 parents active monthly.'],
            ['Late Messaging SLA Target', '0 messages', 'Teacher messages delivered after 20:00 reduced to absolute zero.'],
        ],
        [4.2*cm, 3.4*cm, INNER_W - 7.6*cm], st))
    story.append(Spacer(1, 6))

    story.append(PageTracker('s1_2', page_map))
    story.append(Paragraph('1.2 Users & System Constraints', st['h2']))
    story.append(make_table(
        ['User Class', 'Primary Operational Need', 'Strict Access Boundary & Data Scope'],
        [
            ['Parent', 'Receive notices, homework, absence alerts; message teachers', 'Strictly isolated to their own enrolled child\'s records (NFR-03)'],
            ['Teacher', 'Publish circulars/homework; mark attendance; message without night spam', 'Restricted strictly to mapped classrooms and assigned subjects'],
            ['School Admin', 'Approve school notices; manage rosters and staff mappings', 'Scoped strictly to their assigned institution'],
            ['Group Management', 'Audit group-wide communications and review compliance rates', 'Read-only access across all institutions; no direct messaging capability'],
            ['Principal', 'Adjudicate out-of-hours urgent teacher messaging approval requests', 'Institutional authority for emergency exception overrides'],
        ],
        [2.8*cm, 6.2*cm, INNER_W - 9.0*cm], st))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<b>Architectural Constraints:</b> Android 8.0+ clients with ≥2 GB RAM; web administration console for desktop browsers; '
        'Indian Standard Time (IST, UTC+05:30) at minute-level granularity; English UI for pilot; strict exclusion of payment processing; '
        '3-person engineering team with 68 person-day bottom-up budget; end-to-end TLS 1.2+ and AES-256 encryption at rest.', st['body']))

    story.append(PageTracker('s1_3', page_map))
    story.append(Paragraph('1.3 Functional Requirements (FR-01 to FR-10)', st['h2']))
    story.append(make_table(
        ['ID', 'Requirement Statement', 'Priority', 'Measurable Acceptance Check & Test Oracle'],
        [
            ['FR-01', 'Role-scoped authentication for parent, teacher, admin, management, principal', 'Must',
             'Authenticate credentials per role; deny cross-class and cross-child unauthorized access requests (TC-01)'],
            ['FR-02', 'Circular publishing: class-level immediate; school-level requires admin approval', 'Must',
             'Class notice posts immediately; school-level notice remains in PENDING state until admin approves (TC-02)'],
            ['FR-03', 'Per-parent read receipts: delivered and read timestamps with aggregate read %', 'Must',
             'Simulate 10 parents: 6 open notice -> system displays 60% read and lists 4 unread parents by name (TC-03)'],
            ['FR-04', 'Homework module: post tasks with due dates; track parent acknowledgements', 'Should',
             'Post class homework; parent acknowledgement persists and reports to faculty dashboard (TC-04)'],
            ['FR-05', 'Attendance alerts: notify parents within 15 min of roll-call submission', 'Must',
             'Mark student absent at 09:00 roll call -> push notification delivered to parent device by 09:15 (TC-05)'],
            ['FR-06', 'Fee reminders: automated triggers at D−7 and D−1 before due dates (No Payment)', 'Should',
             'Reminders fire at D−7 and D−1 only; interface contains zero payment gateway or link (TC-06)'],
            ['FR-07', 'Two-way parent-teacher threads per child with mutual phone number masking', 'Must',
             'Parent messages class teacher; thread isolates by child; phone numbers masked as XXXX-XXXX (TC-07)'],
            ['FR-08', 'Messaging-hours enforcement engine (07:00–19:59 window and queueing)', 'Must',
             'Execute all boundary and decision table tests; block or queue out-of-window attempts (TC-08)'],
            ['FR-09', 'Admin portal: bulk CSV roster import with row-level validation; approval queue', 'Must',
             'Import 100 rows with 1 error: 99 commit, 1 reports exact line number and failure reason (TC-09)'],
            ['FR-10', 'Communication audit log and compliance reports (Active Parents & Late Messages)', 'Should',
             'Audit log searchable by date/sender; reports output exact numerator, denominator, and % (TC-10)'],
        ],
        [1.3*cm, 5.7*cm, 1.6*cm, INNER_W - 8.6*cm], st))

    story.append(PageTracker('s1_4', page_map))
    story.append(Paragraph('1.4 Measurable Non-Functional Requirements (NFR-01 to NFR-06)', st['h2']))
    story.append(make_table(
        ['ID', 'Quality Attribute', 'Specification (Zero Ambiguity)', 'Verification Method'],
        [
            ['NFR-01', 'Delivery Timeliness', '≥99% of circulars, homework and alerts reach push gateway within 5 min; attendance alerts reach device within 15 min of roll-call submission', '10,000 synthetic message load test + gateway timestamp audit'],
            ['NFR-02', 'Delivery Integrity', '0 lost or duplicated messages across 10,000 retried deliveries via idempotency keys; read receipts stored within 60 s of user view', 'Chaos-injection retry test harness and database consistency check'],
            ['NFR-03', 'Access Control Privacy', '100% pass rate on role-boundary penetration tests; zero cross-tenant, cross-class, or cross-child leakage', 'Automated security test suite executing 500 boundary test permutations'],
            ['NFR-04', 'Data Protection', '100% TLS 1.2+ in transit; AES-256 at rest; phone numbers masked in all user UI; student data scrubbed 12 months after exit', 'Cryptographic configuration review, database dumps, and code audit'],
            ['NFR-05', 'System Usability', '≥90% of 20 test parents read notice and reply in ≤3 taps from home; operates smoothly on Android 8+ (2 GB RAM); Class-5 reading level', 'Structured usability laboratory evaluation with 20 representative parents'],
            ['NFR-06', 'High Availability', '≥99.5% uptime during operational core hours (06:30–21:00 IST Monday–Saturday)', 'Automated synthetic probe checks every 60 seconds from external vantage points'],
        ],
        [1.4*cm, 2.9*cm, 5.7*cm, INNER_W - 10.0*cm], st))

    story.append(PageTracker('s1_5', page_map))
    story.append(Paragraph('1.5 Messaging-Hours & Approval Rules (FR-08)', st['h2']))
    story.append(navy_box([
        Paragraph('<b>Governing Messaging Rules (Indian Standard Time, Minute-Level Oracle):</b>', ParagraphStyle('rb', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)),
        Paragraph('1. <b>Faculty Sending Window:</b> 07:00–19:59 IST inclusive. Teacher messages dispatched immediately.', st['body']),
        Paragraph('2. <b>Routine Out-of-Hours Messaging:</b> Between 20:00 and 06:59 IST, routine messages are blocked and queued for automated dispatch at 07:00 next school day.', st['body']),
        Paragraph('3. <b>Urgent Messaging Exception:</b> Out-of-hours messages marked Urgent trigger an instant alert to the Principal. If approved, sent immediately; if rejected or undecided by 07:00, released at 07:00.', st['body']),
        Paragraph('4. <b>Parent Submission Flexibility:</b> Parents may send messages 24/7. Out-of-hours parent messages are held for faculty review at 07:00, and parent receives an instant automated auto-reply.', st['body']),
        Paragraph('5. <b>Zero Late Messaging Target:</b> Teacher-initiated routine messages delivered after 20:00 must equal zero.', st['body']),
    ]))
    story.append(Spacer(1, 4))

    story.append(PageBreak())
    story.append(PageTracker('s1_6', page_map))
    story.append(Paragraph('1.6 MoSCoW Priorities & Traceability Matrix', st['h2']))
    story.append(make_table(
        ['MoSCoW Tier', 'Requirements Allocated', 'Strategic Rationale & Trade-Off Analysis'],
        [
            ['Must Have', 'FR-01, FR-02, FR-03, FR-05, FR-07, FR-08, FR-09', 'Non-negotiable core: solves the primary brief problems (missed notices, late messages, no records).'],
            ['Should Have', 'FR-04, FR-06, FR-10', 'High-value items: homework posting, fee reminders, and compliance audit reporting. Pilot viable temporarily without them.'],
            ['Could Have (Backlog)', 'C-01 Multilingual UI (Hindi/Marathi), C-02 SMS Fallback, C-03 PTM Slot Booking', 'Valuable extensions. C-02 SMS fallback is prioritised as contingency if parent app adoption lags below target.'],
            ['Won\'t Have (Release 1)', 'Payment Gateway, Video Calls, Student Accounts, WhatsApp Integration', 'Excluded to eliminate security liabilities, telecom fees, minor data risks, and channel circumvention.'],
        ],
        [2.2*cm, 4.8*cm, INNER_W - 7.0*cm], st))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Requirements Traceability Matrix (RTM)', st['h3']))
    story.append(make_table(
        ['Requirement', 'System Test Case', 'Unit / Integration / Boundary Test Verification'],
        [
            ['FR-01 Accounts & Scoping', 'TC-01', 'TC-EC-05, TC-EC-06; Automated role-boundary test suite (NFR-03)'],
            ['FR-02 Circulars & Approval', 'TC-02', 'Decision table rules TC-DT-R8 to R13; TC-EC-10, TC-EC-11'],
            ['FR-03 Read Receipts', 'TC-03', 'Receipt latency benchmark harness (NFR-02); database uniqueness test'],
            ['FR-04 Homework & Acknowledge', 'TC-04', 'Class filtering test; parent acknowledgement persistence check'],
            ['FR-05 Attendance Alerts', 'TC-05', 'End-to-end roll call timer benchmark; 15-minute SLA check (NFR-01)'],
            ['FR-06 Fee Reminders (No Pay)', 'TC-06', 'D−7 and D−1 scheduler tests; static security scan for payment endpoints'],
            ['FR-07 Two-Way Messaging', 'TC-07', 'Thread isolation tests; TC-BVA-10 to 18; phone masking verification'],
            ['FR-08 Messaging Hours Engine', 'TC-08', 'TC-BVA-01 to 18; TC-DT-R1 to R13; TC-EC-01 to 09'],
            ['FR-09 Admin Roster Management', 'TC-09', '100-row CSV parser test; line-error reporting validation'],
            ['FR-10 Audit Log & Compliance', 'TC-10', 'Audit log query benchmarks; monthly active & after-8 p.m. formula verification'],
        ],
        [3.0*cm, 2.5*cm, INNER_W - 5.5*cm], st))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════════
    # SECTION 2 — UML DESIGN
    # ══════════════════════════════════════════════════════════════════════════════
    story.append(PageTracker('s2', page_map))
    story.append(section_badge('SECTION 02', st))
    story.append(Spacer(1, 4))
    story.append(Paragraph('UML Software Design Package', st['h1']))
    story.append(coral_rule())

    story.append(PageTracker('s2_1', page_map))
    story.append(Paragraph('2.1 Use-Case Model & System Actors', st['h2']))
    story.append(Paragraph(
        'The use-case model delineates the exact operational boundary of SchoolDiary. Actors sit outside the system boundary: '
        'Parent, Teacher, School Admin, Principal, Group Management, and the external Push Gateway (secondary system actor).', st['body']))
    story.append(make_table(
        ['Actor', 'Primary Use Cases Executed', 'Relationship Details («include» / «extend»)'],
        [
            ['Parent', 'View & acknowledge notice; view homework; send message to teacher', 'Send message «include» Sign in; Auto-reply «extend» Send message [parent after hours]'],
            ['Teacher', 'Publish notice; track read receipts; post homework; mark attendance; message parent', 'Send message «include» Check hours; Send urgent «extend» Send message; Notice «include» Push'],
            ['School Admin', 'Approve/reject school notices; manage rosters and mappings; view queue', 'Publish school notice «include» Admin approval; Bulk CSV import «include» Sign in'],
            ['Principal', 'Adjudicate emergency out-of-hours teacher messages', 'Approve urgent message «extend» Send urgent message [outside window]'],
            ['Management', 'View central audit log; inspect monthly active and late-message reports', 'View reports «include» Sign in; Read-only scoping strictly enforced'],
            ['Push Gateway', 'Deliver push notifications to mobile client devices (secondary actor)', 'Invoked asynchronously by NotificationDispatcher; accepts idempotency key'],
        ],
        [2.8*cm, 5.2*cm, INNER_W - 8.0*cm], st))

    story.append(PageTracker('s2_2', page_map))
    story.append(Paragraph('2.2 Class Model & Domain Architecture', st['h2']))
    story.append(make_table(
        ['Domain Class / Enum', 'Key Structural Attributes & Public Interfaces', 'Architectural Role & Invariants'],
        [
            ['School', 'schoolId, name, principalId, addClass(section)', 'Institutional root aggregate; encapsulates ClassSections'],
            ['ClassSection', 'sectionId, grade, division, classTeacherId, students()', 'Classroom container; maps faculty to enrolled pupil rosters'],
            ['Parent', 'parentId, name, maskedContact, deviceToken, childrenIds', 'Guardian account; contact masked in all teacher-facing displays'],
            ['Teacher', 'teacherId, name, mappedSectionIds, isClassTeacher()', 'Faculty account; restricted strictly to assigned section boundaries'],
            ['Notice', 'noticeId, scope (CLASS/SCHOOL), status, submit(), publish()', 'Status: DRAFT, PENDING_APPROVAL, QUEUED, PUBLISHED, REJECTED'],
            ['ReadReceipt', 'noticeId, parentId, deliveredAt, readAt, markRead()', 'Composite primary key (noticeId, parentId) prevents duplicate counts'],
            ['Message', 'messageId, senderRole, body, urgent, status, scheduledFor', 'Status: DRAFT, SUBMITTED, QUEUED, PENDING_APPROVAL, SENT, DELIVERED, READ, FAILED'],
            ['MessagingPolicy', 'windowStart=07:00, windowEnd=19:59, canSendNow()', 'Stateless pure rules engine; evaluates (role, time, urgency) -> Decision'],
            ['NoticeService', 'compose(), submit(), onApproved(), remindUnread()', 'Circular orchestration service; publishes NoticePublished domain event'],
            ['MessagingService', 'send(), onParentMessage(), releaseQueued(), retry()', 'Thread orchestration service; publishes MessageReady domain event'],
            ['NotificationDispatcher', 'onNoticePublished(), onMessageReady(), fanOut(), retry()', 'Shared event consumer; manages retry queue, idempotency, and gateway'],
            ['PushGateway', 'push(deviceToken, payload, idempotencyKey): Result', 'Abstract gateway interface; concrete FcmPushAdapter implements it'],
        ],
        [3.0*cm, 5.4*cm, INNER_W - 8.4*cm], st))

    story.append(PageTracker('s2_3', page_map))
    story.append(Paragraph('2.3 Sequence Diagram: Send Notice & Track Receipts', st['h2']))
    story.append(Paragraph(
        'Illustrates the lifecycle of publishing a circular and capturing receipts. Two alt frames handle approval and window checking.', st['body']))
    seq_steps = [
        ('1', 'Teacher -> TeacherApp', 'Compose notice (title, body, attachment, scope=SCHOOL)'),
        ('2', 'TeacherApp -> NoticeService', 'submit(draftNotice)'),
        ('3', 'NoticeService', 'Validate payload size (<=10MB), recipient scopes, author credentials'),
        ('4', '[alt: scope == SCHOOL]', 'Raise ApprovalRequest -> route to SchoolAdmin portal queue'),
        ('4a', '[opt: Admin Rejects]', 'SchoolAdmin -> NoticeService: reject(reason) -> Status REJECTED; process halts'),
        ('4b', '[opt: Admin Approves]', 'SchoolAdmin -> NoticeService: approve(requestId) -> proceed to window check'),
        ('5', '[alt: scope == CLASS]', 'Bypass admin approval; proceed directly to window check'),
        ('6', 'NoticeService -> Policy', 'canSendNow(role=TEACHER, timestamp=now, urgent=false)'),
        ('7', '[alt: In Window]', 'Policy -> ALLOW -> Status PUBLISHED; emit NoticePublished(noticeId, audience)'),
        ('8', '[alt: Out of Window]', 'Policy -> QUEUE_FOR_0700 -> Status QUEUED; emit NoticePublished at 07:00'),
        ('9', 'Dispatcher -> Gateway', 'Fan-out to parent device tokens; push(token, payload, idempotencyKey)'),
        ('10', '[opt: Network Failure]', 'Gateway returns timeout -> Dispatcher retries (exponential backoff, <=3 attempts)'),
        ('11', 'Parent -> ParentApp', 'Parent opens push notification -> views notice attachment'),
        ('12', 'ParentApp -> ReceiptService', 'record(noticeId, parentId, state=READ) -> persistent timestamp <=60s'),
        ('13', 'Teacher -> TeacherApp', 'Refresh notice analytics -> ReceiptService returns read % and unread names'),
        ('14', '[opt: Unread > 0]', 'Teacher taps "Remind Unread" -> triggers targeted notification to unread subset'),
    ]
    story.append(make_table(
        ['Step', 'Origin -> Destination', 'Invocation / State Transition Details'],
        seq_steps,
        [1.2*cm, 4.2*cm, INNER_W - 5.4*cm], st))

    story.append(PageTracker('s2_4', page_map))
    story.append(Paragraph('2.4 Activity Diagram: Teacher Sends a Message', st['h2']))
    story.append(make_table(
        ['Decision Node', 'Branch Evaluated', 'Execution Action & System State Transition'],
        [
            ['Teacher taps Send', '—', 'Initiate transaction; capture IST timestamp and sender credentials'],
            ['Current time in window?', 'Yes (07:00–19:59 IST)', 'Dispatch immediately -> Dispatcher enqueues push -> Write AuditEntry -> End'],
            ['Current time in window?', 'No (20:00–06:59 IST)', 'Evaluate urgency flag: is message marked Urgent?'],
            ['Urgency flag status', 'No (Routine Message)', 'Transition to QUEUED state; display "Queued for 07:00" to teacher; dispatch at 07:00'],
            ['Urgency flag status', 'Yes (Urgent Message)', 'Create ApprovalRequest -> alert Principal with push notification'],
            ['Principal adjudication', 'Approved by Principal', 'Transition to SENT state immediately -> Dispatcher pushes -> log urgent override'],
            ['Principal adjudication', 'Rejected OR No decision by 07:00', 'Transition to QUEUED state -> automatically dispatched at 07:00 next school day'],
        ],
        [3.5*cm, 3.8*cm, INNER_W - 7.3*cm], st))

    story.append(PageTracker('s2_5', page_map))
    story.append(Paragraph('2.5 State Diagram: Message Lifecycle', st['h2']))
    story.append(make_table(
        ['Initial State', 'Event / Trigger', 'Guard Condition', 'Target State', 'Lifecycle Meaning'],
        [
            ['DRAFT', 'Sender taps Send', '—', 'SUBMITTED', 'Message validated by client'],
            ['SUBMITTED', 'Evaluate sending window', 'Time in 07:00–19:59 IST', 'SENT', 'Immediate gateway dispatch'],
            ['SUBMITTED', 'Evaluate sending window', 'Time outside window & Routine', 'QUEUED', 'Held for 07:00 morning release'],
            ['SUBMITTED', 'Evaluate sending window', 'Time outside window & Urgent', 'PENDING_APPROVAL', 'Awaiting Principal adjudication'],
            ['PENDING_APPROVAL', 'Principal approves', 'Before 07:00 IST', 'SENT', 'Emergency override dispatch'],
            ['PENDING_APPROVAL', 'Principal rejects / timeout', 'Time reaches 07:00 IST', 'QUEUED', 'Released with regular morning queue'],
            ['SENT', 'Gateway pushes to client', 'Device confirms receipt', 'DELIVERED', 'Push delivered on device screen'],
            ['DELIVERED', 'Parent opens message', 'User interaction recorded', 'READ', 'Final terminal state for thread'],
            ['SENT', 'Network timeout / error', 'Retry attempts < 3', 'FAILED', 'Enqueued for exponential retry'],
            ['[START_PARENT]', 'Parent posts message', 'Time outside 07:00–19:59', 'RECEIVED_AFTER_HOURS', 'Parent initiates after hours'],
            ['RECEIVED_AFTER_HOURS', 'Auto-responder executes', 'Immediate', 'AUTO_REPLIED', 'Automated guidance sent to parent'],
            ['AUTO_REPLIED', 'Hold message for faculty', 'Until 07:00 next school day', 'HELD_FOR_TEACHER', 'Hidden from teacher notification tray'],
            ['HELD_FOR_TEACHER', 'Clock reaches 07:00', 'Morning release event', 'DELIVERED_TO_TEACHER', 'Faculty alerted at start of day'],
        ],
        [2.8*cm, 3.0*cm, 3.0*cm, 2.8*cm, INNER_W - 11.6*cm], st))

    story.append(PageTracker('s2_6', page_map))
    story.append(Paragraph('2.6 Cohesion & Loose Coupling Architecture', st['h2']))
    story.append(image_box(
        os.path.join(DIAGRAMS_DIR, "architecture.png"),
        15.5, 7.5,
        "Figure 2.1: Domain Architecture — Zero Direct Coupling Between NoticeService and MessagingService",
        st))
    story.append(navy_box([
        Paragraph('<b>Architectural Cohesion & Loose Coupling Justification:</b>', ParagraphStyle('cj', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)),
        Paragraph('1. <b>Zero Direct Service Coupling:</b> NoticeService and MessagingService maintain zero method calls, zero interfaces, and zero foreign keys between them. '
                  'Circulars evolve with administrative workflows; messaging evolves with parental communication policies.', st['body']),
        Paragraph('2. <b>Asynchronous Event-Driven Integration:</b> NoticeService publishes <code>NoticePublished</code> and MessagingService publishes <code>MessageReady</code>. '
                  'The shared <code>NotificationDispatcher</code> consumes both events asynchronously, centralizing token resolution, idempotency keys, and gateway retry policies.', st['body']),
        Paragraph('3. <b>Shared Stateless Rules Engine:</b> Both modules delegate sending window evaluations to <code>MessagingPolicy</code>. '
                  'This ensures a single, immutable source of truth for the 07:00–19:59 IST schedule without code duplication.', st['body']),
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════════
    # SECTION 3 — PROJECT PLAN
    # ══════════════════════════════════════════════════════════════════════════════
    story.append(PageTracker('s3', page_map))
    story.append(section_badge('SECTION 03', st))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Project Plan & Critical Path Analysis', st['h1']))
    story.append(coral_rule())

    story.append(PageTracker('s3_1', page_map))
    story.append(Paragraph('3.1 Work Breakdown Structure (WBS)', st['h2']))
    story.append(make_table(
        ['WBS Code', 'Work Package Name', 'Effort (pd)', 'Mapped Requirements', 'Key Engineering Deliverable'],
        [
            ['1.0', 'BUILD PHASE', '51 pd', 'FR-01 to FR-10', 'Fully functional, verified application build'],
            ['1.1 (A)', 'Notices & Circulars', '8 pd', 'FR-02, FR-03', 'Class/school notice engine, approval workflow, read receipt analytics'],
            ['1.2 (B)', 'Homework Module', '10 pd', 'FR-04', 'Assignment posting, due date schedulers, parent acknowledgement tracking'],
            ['1.3 (C)', 'Attendance Alerts', '6 pd', 'FR-05', 'Roll-call absence trigger; automated 15-minute push notification pipeline'],
            ['1.4 (D)', 'Fee Reminders', '5 pd', 'FR-06', 'D−7 and D−1 automated reminder engine; strictly zero payment code'],
            ['1.5 (E)', 'Messaging with Time Limits', '12 pd', 'FR-07, FR-08', 'Two-way threads, 07:00–19:59 window engine, auto-responder, approval queue'],
            ['1.6 (F)', 'Admin Console & Reports', '10 pd', 'FR-01, FR-09, FR-10', 'Roster CSV bulk loader, mapping UI, audit log query engine, reports'],
            ['2.0 (G)', 'VERIFY: Testing', '12 pd', 'All Requirements', 'System test execution, boundary analysis, defect log, DRE certification'],
            ['3.0 (H)', 'DEPLOY: Training', '5 pd', 'Operational Rollout', 'Staff and administrative training across 2 pilot institutions; live launch'],
            ['TOTAL', 'COMPLETE PILOT PROJECT', '68 pd', '—', 'Sum of 8 bottom-up work packages = 51 + 12 + 5 = 68 person-days'],
        ],
        [1.5*cm, 4.0*cm, 1.8*cm, 2.5*cm, INNER_W - 9.8*cm], st))

    story.append(PageTracker('s3_2', page_map))
    story.append(Paragraph('3.2 Network Diagram & Critical Path (CPM)', st['h2']))
    story.append(image_box(
        os.path.join(DIAGRAMS_DIR, "cpm_network.png"),
        16.0, 7.6,
        "Figure 3.1: CPM Network Diagram — Critical Path A -> B -> G -> H (27 Working Days)",
        st))
    story.append(make_table(
        ['ID', 'Task Name', 'Duration', 'Predecessors', 'ES', 'EF', 'LS', 'LF', 'Total Float', 'Criticality'],
        [
            ['A', 'Notices', '8 days', '—', '0', '8', '0', '8', '0 days', 'CRITICAL PATH'],
            ['B', 'Homework', '10 days', 'A', '8', '18', '8', '18', '0 days', 'CRITICAL PATH'],
            ['C', 'Attendance Alerts', '6 days', 'F', '10', '16', '12', '18', '2 days', 'Non-Critical (Float 2d)'],
            ['D', 'Fee Reminders', '5 days', 'F', '10', '15', '13', '18', '3 days', 'Non-Critical (Float 3d)'],
            ['E', 'Messaging Hours', '12 days', '—', '0', '12', '6', '18', '6 days', 'Non-Critical (Float 6d)'],
            ['F', 'Admin Panel', '10 days', '—', '0', '10', '2', '12', '2 days', 'Non-Critical (Float 2d)'],
            ['G', 'System Testing', '4 days*', 'B, C, D, E', '18', '22', '18', '22', '0 days', 'CRITICAL PATH'],
            ['H', 'Faculty Training', '5 days', 'G', '22', '27', '22', '27', '0 days', 'CRITICAL PATH'],
        ],
        [0.8*cm, 3.2*cm, 1.6*cm, 2.0*cm, 0.9*cm, 0.9*cm, 0.9*cm, 0.9*cm, 1.8*cm, INNER_W - 13.0*cm], st))
    story.append(Paragraph('*Testing effort (12 person-days) is executed in parallel by the entire 3-person team: 12 ÷ 3 = 4 working days.',
        ParagraphStyle('fn', fontName='Helvetica-Oblique', fontSize=7.5, textColor=SLATE)))
    story.append(navy_box([
        Paragraph('<b>Critical Path Formula & Working:</b> ES(G) = max(EF_B=18, EF_C=16, EF_D=15, EF_E=12) = 18 days.', st['body']),
        Paragraph('Critical Path Sequence: <b>Task A (8d) -> Task B (10d) -> Task G (4d) -> Task H (5d) = 27 working days.</b>',
            ParagraphStyle('cp', fontName='Helvetica-Bold', fontSize=9.5, textColor=CORAL)),
        Paragraph('Any delay in Tasks A, B, G, or H translates directly into a day-for-day slip of the pilot launch date.', st['body']),
    ]))

    story.append(PageTracker('s3_3', page_map))
    story.append(Paragraph('3.3 Milestones & Gantt Schedule', st['h2']))
    story.append(image_box(
        os.path.join(DIAGRAMS_DIR, "gantt_chart.png"),
        16.0, 6.7,
        "Figure 3.2: Project Gantt Schedule Across 27 Working Days with Milestone Gates",
        st))
    story.append(make_table(
        ['Milestone Gate', 'Target Day', 'Verifiable Exit Criteria & Evidence Required for Approval'],
        [
            ['M1: Admin Infrastructure Ready', 'Day 10', 'Admin console deployed; CSV roster loader verified; Tasks C and D unblocked.'],
            ['M2: Feature Freeze Baseline', 'Day 18', 'All 6 functional modules built and unit-tested; test data loaded; feature code frozen.'],
            ['M3: Quality Exit & Go/No-Go', 'Day 22', 'Testing phase complete; zero open critical or high defects; DRE confirmed; sign-off.'],
            ['M4: Pilot Operational Go-Live', 'Day 27', 'Faculty training concluded at 2 pilot schools; system deployed to 2,300 pilot parents.'],
        ],
        [4.2*cm, 1.8*cm, INNER_W - 6.0*cm], st))

    story.append(PageTracker('s3_4', page_map))
    story.append(Paragraph('3.4 Resource Allocation & Schedule Analysis', st['h2']))
    story.append(make_table(
        ['Engineer Profile', 'Days 0–10', 'Days 10–16', 'Days 16–18', 'Days 18–22', 'Days 22–27'],
        [
            ['P1: Lead Developer', 'Task F: Admin Panel', 'Task C: Attendance', 'Prepare test suites', 'Task G: Testing (All)', 'Post-launch pilot defect support'],
            ['P2: Frontend Developer', 'Task A: Notices (0–8d)', 'Task B: Homework', 'Task B: Homework', 'Task G: Testing (All)', 'Task H: Lead Trainer (2 schools)'],
            ['P3: Backend / QA Dev', 'Task E: Messaging (0–12d)', 'Task D: Fee Reminders', 'Task D finish & test data', 'Task G: Testing (All)', 'Post-launch pilot defect support'],
        ],
        [3.0*cm, 3.0*cm, 2.8*cm, 2.5*cm, 2.5*cm, INNER_W - 13.8*cm], st))
    story.append(Spacer(1, 4))
    story.append(navy_box([
        Paragraph('<b>Strategic Schedule Rationale — Why 27 Days and Not 23 Days?</b>', ParagraphStyle('sr', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)),
        Paragraph('The theoretical ideal duration equals total effort divided by headcount: 68 ÷ 3 = 22.67 ≈ 23 working days. '
                  'However, scheduling a project at 23 days is mathematically impossible due to physical dependencies:', st['body']),
        Paragraph('1. <b>Serial Dependency Chain:</b> Task B (Homework) reuses publishing infrastructure from Task A (Notices). Hence, Task B cannot conclude before Day 18 (8 + 10 = 18d).', st['body']),
        Paragraph('2. <b>Testing Feature Freeze Precondition:</b> Formal system and UAT verification (Task G) requires all features to be integrated, making Day 18 the earliest possible start.', st['body']),
        Paragraph('3. <b>Single-Trainer Constraint:</b> Institutional training (Task H) across 2 schools is conducted by Developer P2, requiring 5 contiguous working days that cannot be compressed.', st['body']),
        Paragraph('<b>Schedule Stretch:</b> 27 days − 23 days = 4 working days of schedule stretch, yielding an 84% resource utilisation rate (68 ÷ 81 pd).', st['body']),
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════════
    # SECTION 4 — ESTIMATION
    # ══════════════════════════════════════════════════════════════════════════════
    story.append(PageTracker('s4', page_map))
    story.append(section_badge('SECTION 04', st))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Estimation Sheet & Mathematical Proofs', st['h1']))
    story.append(coral_rule())

    story.append(PageTracker('s4_1', page_map))
    story.append(Paragraph('4.1 Inputs & Stated Assumptions', st['h2']))
    story.append(make_table(
        ['ID', 'Category', 'Stated Assumption & Engineering Basis'],
        [
            ['A1', 'Demographic Distribution', 'Parent population is distributed evenly across 12 schools: 14,000 ÷ 12 ≈ 1,167 parents per institution.'],
            ['A2', 'Faculty Distribution', 'Teacher staffing is directly proportional to parent count: pilot teachers = 650 × (2,300 ÷ 14,000) ≈ 107 teachers.'],
            ['A3', 'Effort Productivity', 'Each person-day represents 1 productive working day for 1 engineer; estimates include local code reviews.'],
            ['A4', 'Parallelism Bounds', 'Ideal duration assumes perfect, unconstrained parallel execution across 3 developers.'],
            ['A5', 'CPM Network Rigor', 'Scheduled duration is strictly derived from the Critical Path Method forward/backward pass (Section 3).'],
            ['A6', 'Calendar Framework', 'All durations represent elapsed working days (Mon–Sat); project start is established as Day 0.'],
            ['A7', 'Active Parent Definition', 'A parent is classified as Monthly Active if they open ≥1 circular, homework, or thread within the calendar month.'],
        ],
        [1.0*cm, 3.2*cm, INNER_W - 4.2*cm], st))

    story.append(PageTracker('s4_2', page_map))
    story.append(Paragraph('4.2 Step-by-Step Calculations & Formulas', st['h2']))
    story.append(make_table(
        ['#', 'Metric', 'Mathematical Formula', 'Exact Step-by-Step Working', 'Computed Result'],
        [
            ['1', 'Pilot Share of Parents', 'Pilot Parents ÷ Total Parents', '2,300 ÷ 14,000 = 0.1642857...', '16.43% (≈ 16.4%)'],
            ['2', 'Group Parents / School', 'Total Parents ÷ Schools', '14,000 ÷ 12 = 1,166.67...', '≈ 1,167 parents'],
            ['3', 'Pilot Parents / School', 'Pilot Parents ÷ Pilot Schools', '2,300 ÷ 2 = 1,150.0', '1,150 parents'],
            ['4', 'Pilot Faculty Allocation', 'Total Teachers × Pilot Share', '650 × 0.1642857... = 106.78...', '≈ 107 teachers'],
            ['5', 'Total Bottom-Up Effort', 'Sum of 8 Work Packages', '8 + 10 + 6 + 5 + 12 + 10 + 12 + 5 = 68', '68 person-days'],
            ['6', 'Ideal Duration', 'Total Effort ÷ Headcount', '68 ÷ 3 = 22.666...', '22.67 ≈ 23 working days'],
            ['7', 'Scheduled Duration', 'Critical Path A + B + G + H', '8 + 10 + 4 + 5 = 27', '27 working days'],
            ['8', 'Available Capacity', 'Headcount × Scheduled Duration', '3 × 27 = 81', '81 person-days'],
            ['9', 'Resource Utilisation', 'Total Effort ÷ Available Capacity', '68 ÷ 81 = 0.839506...', '83.95% ≈ 84%'],
            ['10', 'Schedule Stretch', 'Scheduled Duration − Ideal Duration', '27 − 22.67 = 4.33...', '4 working days'],
            ['11', 'Pilot Active Target', '90% × Pilot Parents', '0.90 × 2,300 = 2,070', '2,070 parents'],
            ['12', 'Full Rollout Active Target', '90% × Total Parents', '0.90 × 14,000 = 12,600', '12,600 parents'],
            ['13', 'Late Messaging Target', 'Direct SLA Objective', 'Zero messages delivered after 20:00', '0 messages'],
        ],
        [0.8*cm, 3.5*cm, 3.6*cm, 4.5*cm, INNER_W - 12.4*cm], st))

    story.append(PageTracker('s4_3', page_map))
    story.append(Paragraph('4.3 Confidence Level & Why the Result is an Estimate, Not a Promise', st['h2']))
    story.append(make_table(
        ['Estimation Metric', 'Baseline Point Estimate', 'Optimistic Bound (−20%)', 'Pessimistic Bound (+20%)'],
        [
            ['Engineering Effort', '68.0 person-days', '68.0 × 0.80 = 54.4 person-days', '68.0 × 1.20 = 81.6 person-days'],
            ['Ideal Duration (3 Engineers)', '22.7 working days', '54.4 ÷ 3 = 18.1 working days', '81.6 ÷ 3 = 27.2 working days'],
            ['Scheduled Duration (CPM)', '27.0 working days', 'Fast-tracked: 23 working days', 'Buffer-adjusted: 32 working days'],
        ],
        [4.2*cm, 3.2*cm, 3.2*cm, INNER_W - 10.6*cm], st))
    story.append(Spacer(1, 4))
    story.append(navy_box([
        Paragraph('<b>Professional Justification: An Estimate is a Probability Distribution, Not a Contractual Promise:</b>', ParagraphStyle('ep', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)),
        Paragraph('The figures of 68 person-days, 23 ideal days, and 27 scheduled days are professional engineering estimates developed '
                  'during the requirements elicitation stage prior to architectural design. Consequently, an honest industry confidence band '
                  'of ±20% applies (54.4 to 81.6 person-days).', st['body']),
        Paragraph('1. <b>Assumption Sensitivity:</b> The estimate presumes immediate CSV roster availability from pilot schools, zero engineer attrition, '
                  'and a maximum of 3 push retry cycles. If any assumption fails, effort variance increases.', st['body']),
        Paragraph('2. <b>Complexity Variance:</b> Task E (Messaging Hours) represents the single largest package (12 pd). While backed by 6 days of total float, '
                  'its state-machine edge cases represent the highest variance risk.', st['body']),
        Paragraph('3. <b>Commitment vs Forecast:</b> A promise represents a rigid commitment regardless of newly discovered scope; '
                  'an estimate is a data-driven forecast refined continuously at each milestone gate (M1 to M4).', st['body']),
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════════
    # SECTION 5 — SCOPE MANAGEMENT
    # ══════════════════════════════════════════════════════════════════════════════
    story.append(PageTracker('s5', page_map))
    story.append(section_badge('SECTION 05', st))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Scope Management & Change Control', st['h1']))
    story.append(coral_rule())

    story.append(PageTracker('s5_1', page_map))
    story.append(Paragraph('5.1 Pilot Scope Statement', st['h2']))
    story.append(navy_box([
        Paragraph('<b>Pilot Scope Boundary Specification:</b> Deliver a fully operational communication suite to 2 pilot schools, '
                  'encompassing 2,300 parents and ~107 faculty members. Deliverables comprise an Android native application, web admin portal, '
                  'and all 8 core functional modules (FR-01 to FR-10) within 68 person-days and 27 working days. '
                  'Key success targets: 90% monthly active parents (2,070 parents) and 0 late teacher messages after 20:00.', st['body']),
    ]))
    story.append(Spacer(1, 4))

    story.append(PageTracker('s5_2', page_map))
    story.append(Paragraph('5.2 Scope Boundary & Impact on Time, Cost & Quality', st['h2']))
    story.append(make_table(
        ['Scope Work Item', 'Lifecycle Boundary', 'Impact on Schedule (Time)', 'Impact on Budget (Cost)', 'Impact on Engineering Quality'],
        [
            ['Notices & Receipts (FR-02, 03)', 'IN SCOPE (Pilot)', 'Task A (8d): On critical path; slip delays go-live directly', '8 person-days allocated', 'Eliminates missed circulars; captures read verification'],
            ['Homework Module (FR-04)', 'IN SCOPE (Pilot)', 'Task B (10d): On critical path; drives Day 18 feature freeze', '10 person-days allocated', 'Standardizes assignments; reuses notice delivery pipeline'],
            ['Attendance Alerts (FR-05)', 'IN SCOPE (Pilot)', 'Task C (6d): Non-critical (2d float absorbs small slips)', '6 person-days allocated', 'Delivers 15-min safety alert; enforces roster integrity'],
            ['Fee Reminders (FR-06)', 'IN SCOPE (Pilot)', 'Task D (5d): Non-critical (3d float absorbs small slips)', '5 person-days allocated', 'Automates collection chasing without payment compliance burden'],
            ['Messaging Hours (FR-07, 08)', 'IN SCOPE (Pilot)', 'Task E (12d): Largest item; 6d float isolates critical path', '12 person-days allocated', 'Protects faculty work-life balance; stops night message spam'],
            ['Admin Panel (FR-01, 09, 10)', 'IN SCOPE (Pilot)', 'Task F (10d): Non-critical (2d float); hits M1 on Day 10', '10 person-days allocated', 'Enforces strict tenant scoping; central audit logging'],
            ['Testing & Training (G, H)', 'IN SCOPE (Pilot)', '12 pd testing (4d) + 5d training: Both on critical path', '17 person-days allocated', 'Testing guarantees 94.4% DRE; training drives 90% adoption'],
            ['10 Rollout Schools', 'Later Release', 'Zero pilot schedule impact; planned for Phase 2', 'Funded under Phase 2 budget', 'Pilot defect data hardens codebase before multi-tenant scale'],
            ['C-01 Multilingual UI', 'Later Release', 'Deferred; adding i18n would inflate critical path by 5d', 'Requires external translation', 'Improves vernacular reach; deferred to safeguard 27d launch'],
            ['C-02 SMS Fallback Gateway', 'Later Release', 'Deferred; telecom gateway integration adds 4d', 'Per-SMS carrier charges', 'Crucial contingency for offline parents; prioritised for rollout'],
            ['C-03 PTM Slot Booking', 'Later Release', 'Deferred; calendar conflict engine requires 8d', 'Additional dev budget', 'High user value; non-essential for initial communication problem'],
            ['Native iOS Client', 'Later Release', 'Deferred; dual-platform mobile build doubles UI effort', 'Requires iOS dev & test kits', 'Android covers 96% of pilot demographic; iOS deferred'],
            ['Online Fee Payment', 'OUT OF SCOPE', 'Excluded; PCI-DSS compliance & gateway testing adds 15d', 'Merchant fees & liability', 'Eliminates financial security, fraud, and audit liabilities'],
            ['Real-Time Video Calls', 'OUT OF SCOPE', 'Excluded; WebRTC infrastructure adds 20d', 'High server streaming costs', 'Unusable on 2GB RAM budget phones and constrained data plans'],
            ['Student User Accounts', 'OUT OF SCOPE', 'Excluded; child identity management adds 8d', 'Additional privacy audits', 'Eliminates child COPPA/DPDP regulatory compliance risks'],
            ['WhatsApp API Bridge', 'OUT OF SCOPE', 'Excluded; Meta BSP approval timeline is unpredictable', 'Per-conversation Meta fees', 'Defeats project objective by enabling out-of-hours message leaks'],
        ],
        [3.0*cm, 2.2*cm, 3.2*cm, 2.5*cm, INNER_W - 10.9*cm], st))

    story.append(PageBreak())
    story.append(PageTracker('s5_3', page_map))
    story.append(Paragraph('5.3 Scope-Change Control Procedure', st['h2']))
    story.append(make_table(
        ['Process Step', 'Governing Action & Evaluation Protocol', 'Accountable Role', 'Enforcement SLA'],
        [
            ['1. Request Submission', 'Formal Change Request (CR) logged with business justification and technical scope description.', 'Any Stakeholder', 'Continuous logging'],
            ['2. Impact Assessment', 'Evaluate CPM impact. If critical task affected -> project finish extends. If non-critical -> evaluate float. Recompute effort and cost.', 'Project Manager', 'Within 2 working days'],
            ['3. Governance Review', 'Management Sponsor evaluates CR. Decisions: Approve, Reject, or Defer to Phase 2 backlog. Changes >81.6 pd require re-estimation.', 'Management Sponsor', 'Within 3 working days'],
            ['4. Baseline Re-alignment', 'If approved, formally re-baseline SRS, CPM schedule, Estimation Sheet, and Test Plan under new version number.', 'Project Manager', 'Prior to task start'],
            ['5. Stakeholder Notice', 'Formal notification of schedule adjustments disseminated to faculty, admins, and engineering team.', 'Project Manager', 'Immediate dispatch'],
        ],
        [2.5*cm, 6.2*cm, 2.5*cm, INNER_W - 11.2*cm], st))
    story.append(Spacer(1, 4))
    story.append(navy_box([
        Paragraph('<b>Simulated Scope Creep Rejections During Pilot Formulation:</b>', ParagraphStyle('sc', fontName='Helvetica-Bold', fontSize=8.5, textColor=NAVY)),
        Paragraph('• <i>Payment Processing Integration:</i> Requested by school accounts; rejected due to PCI-DSS liability and 15-day critical path delay.', st['body']),
        Paragraph('• <i>WhatsApp Notification Mirror:</i> Requested by faculty; rejected because external messaging bypasses the 20:00 cutoff and audit trail.', st['body']),
        Paragraph('• <i>Student Direct Accounts:</i> Requested by senior teachers; rejected to eliminate child privacy and consent compliance exposure.', st['body']),
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════════
    # SECTION 6 — TEST PLAN & EVIDENCE
    # ══════════════════════════════════════════════════════════════════════════════
    story.append(PageTracker('s6', page_map))
    story.append(section_badge('SECTION 06', st))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Test Plan & Empirical Evidence', st['h1']))
    story.append(Paragraph('IEEE 829-lite Test Specification · Identifier: TP-SD-01', ParagraphStyle('subt',
        fontName='Helvetica-Oblique', fontSize=8.5, textColor=SLATE, spaceAfter=6)))
    story.append(coral_rule())

    story.append(PageTracker('s6_1', page_map))
    story.append(Paragraph('6.1 Test Strategy, Levels & Environmental Controls', st['h2']))
    story.append(make_table(
        ['Test Strategy Dimension', 'Operational Specification & Environmental Governance'],
        [
            ['Entry Criteria', 'Milestone M2 reached (Day 18); feature freeze enacted; synthetic rosters loaded; rules oracle confirmed.'],
            ['Exit Criteria', '100% of planned tests executed; zero open critical or high defects at Milestone M3 (Day 22); DRE certified ≥90%.'],
            ['Multi-Level Execution', 'Unit (BVA, Equivalence Partitioning, Decision Table); Integration (API, gateway retry); System (TC-01–10); UAT.'],
            ['Test Bed Environment', 'Synthetic roster data only; 2 test Android 8 handsets (2 GB RAM) + modern Android device; web admin console; gateway clock mock.'],
            ['Governance Roles', 'P3 (Developer/QA) leads test execution; P1/P2 resolve defects; School Admins & Principals participate in UAT sign-off.'],
        ],
        [3.5*cm, INNER_W - 3.5*cm], st))

    story.append(PageTracker('s6_2', page_map))
    story.append(Paragraph('6.2 System Test Cases TC-01 to TC-10', st['h2']))
    story.append(make_table(
        ['Case ID', 'Target FR', 'Execution Procedure & Operational Scenario', 'Expected Result & Verification Oracle'],
        [
            ['TC-01', 'FR-01', 'Log in as Parent, Teacher, Admin, Mgmt. Attempt cross-tenant and cross-child access.', 'Access granted to authorized scope; 403 Forbidden on cross-scope requests.'],
            ['TC-02', 'FR-02', 'Publish class circular (PDF). Submit school-level circular. Admin approves.', 'Class notice posts immediately; school circular stays Pending until admin approval.'],
            ['TC-03', 'FR-03', 'Dispatch circular to 10 test parents. Open as 6 parents. Inspect dashboard.', 'Dashboard displays exactly 60% read; unread roster lists 4 remaining parents by name.'],
            ['TC-04', 'FR-04', 'Post Math homework with due date. Open Parent client and tap Acknowledge.', 'Homework renders with due date; parent acknowledgement persists in faculty view.'],
            ['TC-05', 'FR-05', 'Submit roll call marking Student A absent at 09:00. Time push delivery.', 'Alert delivered to Student A parent device by 09:15 (<=15 min); zero alert for present pupils.'],
            ['TC-06', 'FR-06', 'Seed fee due date D. Advance mock system clock to D−7 and D−1.', 'Automated notifications trigger at D−7 and D−1; interface contains zero payment UI.'],
            ['TC-07', 'FR-07', 'Parent messages teacher at 10:30. Teacher replies at 10:40.', 'Single synchronized thread per child; mutual contact phone numbers masked as XXXX-XXXX.'],
            ['TC-08', 'FR-08', 'Execute full battery of BVA (18 cases) and Decision Table (13 rules).', 'All tests match oracle: Immediate send, queue for 07:00, approval, or parent hold.'],
            ['TC-09', 'FR-09', 'Bulk upload CSV of 100 pupils with 1 corrupt row. Map faculty to sections.', '99 pupils committed; 1 error flagged with exact row and column; mappings update.'],
            ['TC-10', 'FR-10', 'Search communication audit log. Generate Active Parents and Late Message reports.', 'Audit query returns exact match; reports show accurate numerator, denominator, and %.'],
        ],
        [1.3*cm, 1.2*cm, 5.8*cm, INNER_W - 8.3*cm], st))

    story.append(PageTracker('s6_3', page_map))
    story.append(Paragraph('6.3 Equivalence Classes (Message Time & Input Partitions)', st['h2']))
    story.append(make_table(
        ['Partition ID', 'Input Domain / Condition', 'Validity', 'Expected System Behavior', 'Representative Value'],
        [
            ['EC-T1', '07:00 <= t <= 19:59 (Teacher Sending Window)', 'Valid', 'In-window: Immediate gateway dispatch', '13:30 IST'],
            ['EC-T2', '00:00 <= t < 07:00 (Pre-Window Early Morning)', 'Valid', 'Out-of-window: Enqueued for 07:00 release', '03:15 IST'],
            ['EC-T3', '20:00 <= t <= 23:59 (Post-Window Night)', 'Valid', 'Out-of-window: Enqueued for next school day 07:00', '21:45 IST'],
            ['EC-T4', 'Malformed Time Input (hour > 23, minute > 59)', 'Invalid', 'Input validation error: Rejected at API boundary', '25:10 IST'],
            ['TC-EC-05', 'Parent Sender inside 07:00–19:59 IST', 'Valid', 'Immediate delivery to faculty thread', '13:30 IST'],
            ['TC-EC-06', 'Parent Sender outside 07:00–19:59 IST', 'Valid', 'Held for teacher at 07:00 + instant auto-reply', '21:45 IST'],
            ['TC-EC-07', 'Teacher Urgent Message, Out of Window, Pending', 'Valid', 'ApprovalRequest enqueued for Principal review', '21:45 IST'],
            ['TC-EC-08', 'Teacher Urgent Message, Out of Window, Approved', 'Valid', 'Immediate emergency dispatch override', '21:45 IST'],
            ['TC-EC-09', 'Teacher Urgent Message, Out of Window, Rejected', 'Valid', 'Queued for regular morning dispatch at 07:00', '21:45 IST'],
            ['TC-EC-10', 'Class Notice: In-Window vs Out-of-Window', 'Valid', 'Immediate publish (in-window) vs Queued for 07:00', '10:30 / 21:45 IST'],
            ['TC-EC-11', 'School Notice Submitted by Teacher', 'Valid', 'Routes to School Admin queue; Pending status', '10:30 IST'],
        ],
        [1.8*cm, 4.4*cm, 1.2*cm, 3.8*cm, INNER_W - 11.2*cm], st))

    story.append(PageTracker('s6_4', page_map))
    story.append(Paragraph('6.4 Boundary Value Analysis Around 8 p.m. & 7 a.m. (18 Test Cases)', st['h2']))
    story.append(make_table(
        ['Test ID', 'Sender Role', 'Exact Timestamp', 'Expected System Action & Test Outcome Significance'],
        [
            ['TC-BVA-01', 'Teacher (Routine)', '06:59 IST', 'Blocked; enqueued for 07:00. Faculty client displays "Queued for 07:00".'],
            ['TC-BVA-02', 'Teacher (Routine)', '07:00 IST', 'Allowed; immediate dispatch (Opening boundary minute of sending window).'],
            ['TC-BVA-03', 'Teacher (Routine)', '07:01 IST', 'Allowed; immediate dispatch (Inside window).'],
            ['TC-BVA-04', 'Teacher (Routine)', '19:58 IST', 'Allowed; immediate dispatch (Inside window).'],
            ['TC-BVA-05', 'Teacher (Routine)', '19:59 IST', 'Allowed; immediate dispatch. ⚠ Caught DEF-15 (off-by-one bug where t<=19:58 was coded).'],
            ['TC-BVA-06', 'Teacher (Routine)', '20:00 IST', 'Blocked; enqueued for next school day 07:00 (Closing boundary minute).'],
            ['TC-BVA-07', 'Teacher (Routine)', '20:01 IST', 'Blocked; enqueued for next school day 07:00 (After-hours window).'],
            ['TC-BVA-08', 'Teacher (Routine)', '23:59 IST', 'Blocked; enqueued for next school day 07:00 (Pre-midnight boundary).'],
            ['TC-BVA-09', 'Teacher (Routine)', '00:00 IST (Day D+1)', 'Blocked; enqueued for same Day D+1 07:00. Exactly 1 queue entry. ⚠ Caught DEF-35.'],
            ['TC-BVA-10', 'Parent Client', '06:59 IST', 'Held for faculty at 07:00. Instant auto-reply dispatched to parent.'],
            ['TC-BVA-11', 'Parent Client', '07:00 IST', 'Allowed; delivered immediately to faculty message inbox; zero auto-reply.'],
            ['TC-BVA-12', 'Parent Client', '07:01 IST', 'Allowed; delivered immediately to faculty message inbox.'],
            ['TC-BVA-13', 'Parent Client', '19:58 IST', 'Allowed; delivered immediately to faculty message inbox.'],
            ['TC-BVA-14', 'Parent Client', '19:59 IST', 'Allowed; delivered immediately to faculty message inbox.'],
            ['TC-BVA-15', 'Parent Client', '20:00 IST', 'Held until next school day 07:00. Instant auto-reply dispatched to parent.'],
            ['TC-BVA-16', 'Parent Client', '20:01 IST', 'Held until next school day 07:00. Instant auto-reply dispatched to parent.'],
            ['TC-BVA-17', 'Parent Client', '23:59 IST', 'Held until next school day 07:00. Instant auto-reply dispatched to parent.'],
            ['TC-BVA-18', 'Parent Client', '00:00 IST (Day D+1)', 'Held until Day D+1 07:00 once only. Instant auto-reply dispatched to parent.'],
        ],
        [1.8*cm, 2.4*cm, 2.4*cm, INNER_W - 6.6*cm], st))

    story.append(PageTracker('s6_5', page_map))
    story.append(Paragraph('6.5 Decision Table for Messaging-Hours & Approval Rules (13 Rules)', st['h2']))
    story.append(Paragraph('Condition Matrix: C1=Sender Role (T/P/A), C2=In Window (Y/N), C3=Urgent Flag (Y/N/–), '
                           'C4=Principal Approved (Y/N/Pending/–), C5=Item Scope (Msg/Class/School), C6=Decision Final (Y/N)', st['body']))
    story.append(make_table(
        ['Rule', 'C1: Role', 'C2: Window', 'C3: Urgent', 'C4: Approved', 'C5: Scope', 'System Action Executed by Policy Engine'],
        [
            ['R1', 'Teacher', 'Yes (07–20)', '—', '—', 'Message', 'A1: Send immediately via NotificationDispatcher'],
            ['R2', 'Teacher', 'No (20–07)', 'No', '—', 'Message', 'A2: Enqueue for automated release at 07:00 next school day'],
            ['R3', 'Teacher', 'No (20–07)', 'Yes', 'Pending', 'Message', 'A3: Create ApprovalRequest; alert Principal; hold delivery'],
            ['R4', 'Teacher', 'No (20–07)', 'Yes', 'Approved', 'Message', 'A1: Send immediately (Emergency Principal override dispatched)'],
            ['R5', 'Teacher', 'No (20–07)', 'Yes', 'Rejected/Timeout', 'Message', 'A2: Enqueue for 07:00 next school day. ⚠ Caught DEF-28.'],
            ['R6', 'Parent', 'Yes (07–20)', '—', '—', 'Message', 'A1: Deliver immediately to teacher inbox'],
            ['R7', 'Parent', 'No (20–07)', '—', '—', 'Message', 'A4: Deliver auto-reply to parent; hold message for teacher until 07:00'],
            ['R8', 'Teacher', 'Yes (07–20)', '—', '—', 'Class Notice', 'A5: Publish immediately to assigned classroom parent roster'],
            ['R9', 'Teacher', 'No (20–07)', '—', '—', 'Class Notice', 'A2: Enqueue class notice for automated publishing at 07:00'],
            ['R10', 'Teacher', '—', '—', '—', 'School Notice', 'A6: Route to School Admin approval queue; mark PENDING_APPROVAL'],
            ['R11', 'Admin', 'Yes (07–20)', '—', '—', 'School Notice', 'A5: Publish immediately across entire school parent body'],
            ['R12', 'Admin', 'No (20–07)', '—', '—', 'School Notice', 'A2: Enqueue school notice for 07:00 morning release'],
            ['R13', 'Admin', '—', '—', '—', 'School Notice', 'A7: Return notice to draft; alert sender with rejection reason'],
        ],
        [1.0*cm, 1.6*cm, 1.8*cm, 1.6*cm, 1.8*cm, 1.8*cm, INNER_W - 9.6*cm], st))

    story.append(PageTracker('s6_6', page_map))
    story.append(Paragraph('6.6 Empirical Test Log & Defect Distribution', st['h2']))
    story.append(make_table(
        ['Testing Level', 'Planned Cases Run', 'Failed Cases (Defects)', 'Passed Cases', 'Execution Pass Rate'],
        [
            ['Unit Testing (BVA, EC, Decision Table)', '90 cases', '11 defects', '79 cases', '87.78%'],
            ['Integration Testing (API & Gateway Mocks)', '30 cases', '7 defects', '23 cases', '76.67%'],
            ['System Testing (TC-01 to TC-10 Scenarios)', '40 cases', '6 defects', '34 cases', '85.00%'],
            ['User Acceptance Testing (UAT - Faculty & Parents)', '15 cases', '3 defects', '12 cases', '80.00%'],
            ['TOTAL PRE-RELEASE EXECUTION', '175 cases', '27 defects*', '148 cases', '84.57%'],
        ],
        [3.8*cm, 2.5*cm, 2.8*cm, 2.5*cm, INNER_W - 11.6*cm], st))
    story.append(Paragraph('*Note: The 27 test-phase defects combine with 7 review defects (4 requirements review + 3 design review) to yield 34 pre-release defects.',
        ParagraphStyle('fn2', fontName='Helvetica-Oblique', fontSize=7.5, textColor=SLATE)))
    story.append(Spacer(1, 4))
    story.append(make_table(
        ['Engineering Lifecycle Phase', 'Total Defects', 'Critical Severity', 'High Severity', 'Medium Severity', 'Low Severity'],
        [
            ['Requirements Formal Inspection', '4 defects', '0', '1', '2', '1'],
            ['Architectural Design Review', '3 defects', '0', '1', '1', '1'],
            ['Unit Testing Execution', '11 defects', '0', '1', '5', '5'],
            ['Integration Testing Execution', '7 defects', '1', '2', '3', '1'],
            ['System Testing Execution', '6 defects', '0', '1', '3', '2'],
            ['User Acceptance Testing (UAT)', '3 defects', '0', '0', '1', '2'],
            ['Post-Release Pilot (Weeks 1–2)', '2 defects', '0', '1', '1', '0'],
            ['CUMULATIVE DEFECT INVENTORY', '36 defects', '1', '7', '16', '12'],
        ],
        [3.8*cm, 2.2*cm, 2.0*cm, 1.8*cm, 1.8*cm, INNER_W - 11.6*cm], st))
    story.append(Spacer(1, 4))
    story.append(make_table(
        ['Defect ID', 'Lifecycle Phase', 'Severity', 'Root Cause & Empirical Failure Description', 'Verification Oracle'],
        [
            ['DEF-15', 'Unit Test', 'High', 'Off-by-one error: Sending window coded as <code>t <= 19:58</code> instead of <code>19:59</code>.', 'Caught by TC-BVA-05 (19:59 boundary)'],
            ['DEF-21', 'Integration', 'Critical', 'Authorization bypass: ClassSection mapping missing in message service; cross-class leak.', 'Caught by role security test harness'],
            ['DEF-28', 'System Test', 'High', 'Principal rejection bypassed: Message dispatched immediately at 21:20 instead of 07:00.', 'Caught by TC-DT-R5 (decision table)'],
            ['DEF-35', 'Post-Release', 'High', 'Midnight rollover double queue: Message sent at 23:59 re-queued at 00:00 -> dual delivery.', 'Caught in Pilot W1; patched immediately'],
        ],
        [1.6*cm, 2.0*cm, 1.6*cm, 5.8*cm, INNER_W - 11.0*cm], st))

    story.append(PageTracker('s6_7', page_map))
    story.append(Paragraph('6.7 Defect Removal Efficiency (DRE) & Defect Density', st['h2']))
    story.append(image_box(
        os.path.join(DIAGRAMS_DIR, "defect_density.png"),
        13.5, 6.8,
        "Figure 6.1: Defect Density per Module Against the 4.0 Defects/KLOC Benchmark",
        st))
    story.append(navy_box([
        Paragraph('<b>Defect Removal Efficiency (DRE) Mathematical Proof:</b>', ParagraphStyle('dp', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)),
        Paragraph('Formula: <b>DRE = E ÷ (E + D)</b> where <i>E</i> = pre-release defects found, <i>D</i> = post-release defects in pilot.', st['body']),
        Paragraph('• Pre-Release Defects (<i>E</i>) = 4 (Req) + 3 (Design) + 11 (Unit) + 7 (Integ) + 6 (System) + 3 (UAT) = <b>34 defects</b>', st['body']),
        Paragraph('• Post-Release Pilot Defects (<i>D</i>) = <b>2 defects</b> (DEF-35 rollover bug + DEF-36 read % UI anomaly)', st['body']),
        Paragraph('<b>DRE = 34 ÷ (34 + 2) = 34 ÷ 36 = 0.94444... = 94.4%  (Target: ≥ 90% EXCEEDED)</b>',
            ParagraphStyle('drec', fontName='Helvetica-Bold', fontSize=9.5, textColor=CORAL)),
        Paragraph('<i>Test-Phase Only DRE:</i> Considering only executable test stages (E_test = 27): 27 ÷ (27 + 2) = 27 ÷ 29 = <b>93.1%</b>.', st['body']),
    ]))
    story.append(Spacer(1, 4))
    story.append(make_table(
        ['Module Name', 'Size (KLOC)', 'Defect Count', 'Defect Density (Defects/KLOC)', 'Comparative Quality Interpretation'],
        [
            ['Notices & Circulars', '1.2 KLOC', '5 defects', '4.17 defects / KLOC', 'Close to group average; approval logic contributed 2 bugs'],
            ['Homework Module', '1.4 KLOC', '5 defects', '3.57 defects / KLOC', 'Below average; reuse of notice publishing pipeline mitigated defects'],
            ['Attendance Alerts', '0.9 KLOC', '4 defects', '4.44 defects / KLOC', 'Slightly elevated due to roll-call re-save duplicate bug'],
            ['Fee Reminders', '0.8 KLOC', '3 defects', '3.75 defects / KLOC', 'Below average; simple cron-based notification scheduling'],
            ['Messaging Hours Engine', '2.2 KLOC', '12 defects', '5.45 defects / KLOC', '⚠ Highest density (36% above average); contains 1/3 of all defects; high risk'],
            ['Admin Web Console', '2.5 KLOC', '7 defects', '2.80 defects / KLOC', 'Lowest density; standard CRUD screens with low architectural complexity'],
            ['SYSTEM TOTAL / BENCHMARK', '9.0 KLOC', '36 defects', '4.00 defects / KLOC', 'Overall baseline: 36 defects ÷ 9.0 KLOC = 4.0 defects / KLOC'],
        ],
        [2.8*cm, 1.8*cm, 2.0*cm, 3.2*cm, INNER_W - 9.8*cm], st))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════════
    # SECTION 7 — RISK MANAGEMENT
    # ══════════════════════════════════════════════════════════════════════════════
    story.append(PageTracker('s7', page_map))
    story.append(section_badge('SECTION 07', st))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Risk Management & Issue Log', st['h1']))
    story.append(coral_rule())

    story.append(PageTracker('s7_1', page_map))
    story.append(Paragraph('7.1 Scoring Methodology & Probability × Impact Heatmap', st['h2']))
    story.append(image_box(
        os.path.join(DIAGRAMS_DIR, "risk_matrix.png"),
        12.5, 7.8,
        "Figure 7.1: Probability × Impact Risk Matrix Heatmap with 8 Exposure-Ranked Risks",
        st))
    story.append(Paragraph(
        'Risks are scored using 5-point ordinal scales: Probability (P1=Very Low to P5=Very High) and '
        'Impact (I1=Negligible to I5=Catastrophic). <b>Exposure Score = P × I</b> (Range 1 to 25). '
        'Bands: High Exposure (>=15), Medium Exposure (9–14), Low Exposure (<=8). Ties broken by higher impact, then breadth of affected users.', st['body']))

    story.append(PageTracker('s7_2', page_map))
    story.append(Paragraph('7.2 Risk Register (8 Exposure-Ranked Risks)', st['h2']))
    story.append(make_table(
        ['Rank', 'ID', 'Risk Description', 'P', 'I', 'Exposure', 'Band', 'Mitigation Strategy', 'Accountable Owner'],
        [
            ['1', 'R1', 'Low parent adoption (<90% monthly active target)', '4', '5', '20', 'HIGH', 'Mitigate: Teacher-led onboarding drive; mirror circulars; SMS fallback', 'Project Manager & Management Sponsor'],
            ['2', 'R2', 'Push delivery failure on budget phones / battery savers', '3', '4', '12', 'MED', 'Mitigate: Test on 2GB RAM phones; in-app inbox; idempotent retries', 'Lead Developer (P1)'],
            ['3', 'R5', 'Messaging rule too strict; genuine emergencies delayed', '3', '4', '12', 'MED', 'Mitigate: Principal urgent override; school phone in auto-reply; audit', 'Developer/QA (P3) with Principals'],
            ['4', 'R3', 'Faculty continue running unofficial WhatsApp groups', '4', '3', '12', 'MED', 'Mitigate: Principal policy circular; publish after-8 p.m. compliance reports', 'Pilot School Principals'],
            ['5', 'R4', 'Tenant privacy breach: parent sees other child data', '2', '5', '10', 'MED', 'Avoid: Service-layer role checks; masked contacts; penetration tests', 'Lead Developer (P1)'],
            ['6', 'R6', 'Roster CSV data import corruption and invalid phones', '3', '3', '9', 'MED', 'Transfer: School admins sign off rosters; admin dry-run syntax check', 'School Administrative Staff'],
            ['7', 'R7', 'Schedule slip in Messaging module (12 pd budget)', '3', '3', '9', 'MED', 'Accept: Task E has 6d float; reassign P1 to Task D if E slips >1d', 'Project Manager'],
            ['8', 'R8', 'Management disputes "Monthly Active Parent" definition', '2', '3', '6', 'LOW', 'Avoid: Formal written consensus on definition prior to deployment', 'Project Manager'],
        ],
        [1.1*cm, 0.8*cm, 4.3*cm, 0.6*cm, 0.6*cm, 1.6*cm, 1.1*cm, 3.8*cm, INNER_W - 13.9*cm], st))

    story.append(PageTracker('s7_3', page_map))
    story.append(Paragraph('7.3 RMMM Plans for Top 3 Risks', st['h2']))
    for r_id, title, mit, mon, trig, cont, owner in [
        ('R1', 'Risk 1: Low Parent Adoption (Exposure Score: 20 — HIGH BAND)',
         'Conduct in-person onboarding drives during parent orientations at both pilot schools; distribute QR download sheets in paper diaries; '
         'mandate that official circulars are published exclusively on SchoolDiary; maintain school-office walk-in support desks.',
         'Weekly inspection of Monthly Active Parent compliance reports (FR-10).',
         'Active parent adoption drops below 80% (1,840 parents) by end of Week 3, OR 24-hour circular read rate falls below 75%.',
         'Immediately fast-track C-02 SMS Fallback integration; deploy classroom parent coordinators to assist non-registered families; '
         'steering committee convenes to assess adoption barriers prior to rollout expansion.',
         'Project Manager with Group Management Sponsor'),
        ('R2', 'Risk 2: Push Delivery Failure / Offline Budget Handsets (Exposure Score: 12 — MEDIUM)',
         'Rigorous physical testing on Android 8 devices with 2 GB RAM and active OEM aggressive battery savers; implement idempotent delivery '
         'queues (NFR-02); provide prominent in-app notification inbox ensuring notices are visible even when system push fails.',
         'Daily gateway telemetry monitoring; measure 5-minute delivery success against the 99% SLA (NFR-01).',
         'Push delivery success within 5 minutes falls below 99%, OR more than 5% of parent devices register invalid push tokens.',
         'Prioritise defect resolution for push adapters; send direct SMS notifications for critical circulars; release OEM battery-saver configuration guides.',
         'Lead Developer (P1)'),
        ('R5', 'Risk 5: Messaging Rule Too Strict — Urgent Communications Delayed (Exposure Score: 12 — MEDIUM)',
         'Implement streamlined emergency urgent route requiring Principal digital sign-off; default unapproved messages to 07:00 release; '
         'embed school office telephone numbers directly within the automated night auto-response.',
         'Weekly audit of urgent approval request counts, principal response latency, and parent complaint logs.',
         'More than 2 parental complaints per week regarding delayed urgent matters, OR Principal approval latency exceeds 30 minutes.',
         'Principals designate an authorized vice-principal backup approver; management reviews sending window hours; urgent messages remain segregated in compliance audits.',
         'Developer/QA (P3) with Pilot School Principals'),
    ]:
        story.append(KeepTogether([
            Paragraph(f'<b>{title}</b>', st['h3']),
            make_table(
                ['RMMM Dimension', 'Operational Protocol & Strategic Action Plan'],
                [
                    ['Risk Mitigation', mit],
                    ['Risk Monitoring', mon],
                    ['Trigger Metric', trig],
                    ['Contingency Management', cont],
                    ['Accountable Owner', owner],
                ],
                [3.0*cm, INNER_W - 3.0*cm], st),
            Spacer(1, 4)
        ]))

    story.append(PageTracker('s7_4', page_map))
    story.append(Paragraph('7.4 Issue Log & Rationale for Risk-Issue Separation', st['h2']))
    story.append(make_table(
        ['Issue ID', 'Date Raised', 'Empirical Incident Description', 'Operational Impact', 'Corrective Remediation Action', 'Status', 'Root Risk'],
        [
            ['I-01', 'Day 25', '186 of 2,300 parent contact numbers missing in pilot roster CSV', '186 parents unreachable via push or SMS, capping initial adoption', 'Office staff collected numbers during orientation; admin portal added error filter', 'Open', 'R6 (Roster), R1'],
            ['I-02', 'Day 23', 'Faculty training clash with scheduled terminal exams at School 2', 'Reduced faculty attendance and prep time at School 2 before go-live', 'Rescheduled session post-exams; distributed asynchronous video guides', 'Closed', 'R1 (Adoption)'],
            ['I-03', 'Day 31', 'Push alerts suppressed by OEM battery saver on budget handsets', 'Delayed notice delivery for subset of parents; parent frustration', 'Published battery-saver setup guide; prioritized C-02 SMS Fallback', 'Open', 'R2 (Push failure)'],
        ],
        [1.3*cm, 1.4*cm, 3.8*cm, 2.8*cm, 3.8*cm, 1.1*cm, INNER_W - 14.2*cm], st))
    story.append(Spacer(1, 4))
    story.append(navy_box([
        Paragraph('<b>Theoretical Justification — Why Risks and Issues Must Never Be Combined:</b>', ParagraphStyle('ir', fontName='Helvetica-Bold', fontSize=8.5, textColor=NAVY)),
        Paragraph('A <b>Risk</b> is an uncertain future event characterised by a probability (0 < P < 1) and potential impact, requiring proactive mitigation and threshold triggers. '
                  'An <b>Issue</b> is a realized, certain event (P = 1.0) currently disrupting project execution, requiring immediate corrective action, an owner, and a closure target.', st['body']),
        Paragraph('Combining both concepts into a single register destroys exposure scoring (a realized issue cannot be evaluated as P × I) and causes '
                  'urgent operational firefighting to crowd out long-term proactive risk mitigation. Maintaining separate logs illuminates how risks evolve '
                  'into live issues (e.g., Risk R6 evolved into Issue I-01; Risk R2 evolved into Issue I-03).', st['body']),
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════════
    # SECTION 8 — CLOSURE & LESSONS LEARNED
    # ══════════════════════════════════════════════════════════════════════════════
    story.append(PageTracker('s8', page_map))
    story.append(section_badge('SECTION 08', st))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Project Closure & Retrospective Lessons', st['h1']))
    story.append(coral_rule())

    story.append(PageTracker('s8_1', page_map))
    story.append(Paragraph('8.1 Pilot Results & Conditional Rollout Decision', st['h2']))
    story.append(make_table(
        ['Key Success Target', 'Target SLA', 'Actual Empirical Pilot Result', 'Variance & Contractual Status'],
        [
            ['Monthly Active Parents', '90.0% (2,070 / 2,300)', '1,978 / 2,300 parents = 86.0%', '⚠ Shortfall of −4.0 pp (92 parents short); Not Met'],
            ['Late Teacher Messages (>20:00)', '0 messages', '0 routine messages delivered after 20:00', '✅ 100% SLA Compliance; Met (3 approved urgent overrides)'],
            ['Circular Delivery Timeliness (NFR-01)', '≥99.0% within 5 min', '99.3% delivered within 5 minutes', '✅ Exceeded SLA (+0.3 pp); Met'],
            ['Defect Removal Efficiency (DRE)', '≥90.0%', '34 ÷ 36 = 94.4%', '✅ Exceeded Quality Target (+4.4 pp); Met'],
            ['Scheduled Duration Finish', '27 working days', '29 working days (+2 working days)', 'Slip of +7.4% due to UAT defect remediation'],
        ],
        [4.2*cm, 3.2*cm, 3.8*cm, INNER_W - 11.2*cm], st))
    story.append(Spacer(1, 4))
    story.append(navy_box([
        Paragraph('<b>EXECUTIVE GOVERNANCE DECISION: CONDITIONAL ROLLOUT TO REMAINING 10 SCHOOLS</b>',
            ParagraphStyle('cd', fontName='Helvetica-Bold', fontSize=10, textColor=CORAL)),
        Paragraph('The Project Steering Committee approves a <b>Conditional Rollout</b> to the remaining 10 institutions (11,700 parents). '
                  'While technical SLA benchmarks (Zero late messages, 99.3% delivery timeliness, 94.4% DRE) were successfully achieved, '
                  'parent adoption reached 86.0% against the 90.0% target. '
                  'Consequently, expansion to the next school group is contingent upon: (1) fast-tracking C-02 SMS Fallback for non-smartphone households, '
                  'and (2) achieving ≥80% adoption by Week 3 at each newly onboarded campus.', st['body']),
    ]))

    story.append(PageTracker('s8_2', page_map))
    story.append(Paragraph('8.2 Lessons Learned (Engineering Retrospective)', st['h2']))
    story.append(make_table(
        ['#', 'Empirical Incident', 'Root Cause Analysis', 'Engineering / PM Lesson Learned', 'Corrective Policy for 10-School Rollout'],
        [
            ['1', 'Project completed on Day 29 (+2d slip beyond 27d baseline)', 'UAT defects discovered late; fixes executed inside critical testing window without contingency buffer', 'The critical path requires dedicated rework contingency buffers immediately preceding launch', 'Insert a mandatory 2-day defect remediation buffer post-UAT; initiate component UAT earlier'],
            ['2', 'Adoption reached 86.0% vs 90.0% contractual target', 'Onboarding relied solely on faculty circulars; smartphone/data poverty in 8% of households', 'Parent engagement targets require dedicated socio-technical onboarding programs', 'Launch campus-wide onboarding weeks; fund and deploy C-02 SMS Fallback gateway'],
            ['3', 'Messaging module required 14 days instead of 12 days', 'State machine rules, edge cases, and principal approval flows were more complex than estimated', 'Resource-levelled float is substantially tighter than CPM free float in multi-tasking teams', 'Add a 20% complexity contingency factor to rule-heavy modules; maintain visible float boards'],
            ['4', 'DEF-35 (Midnight rollover dual delivery) escaped to pilot', 'TC-BVA-08/09 were executed on reset clocks; contiguous boundary rollover crossing 00:00 was never tested live', 'Time-dependent state engines require dynamic continuous clock boundary simulation', 'Introduce automated continuous clock-advance regression suites spanning midnight and month-ends'],
            ['5', '186 parent phone numbers missing at initial import (I-01)', 'Roster data sourced directly from unvalidated manual Excel sheets maintained by school offices', 'Data cleansing is a mandatory predecessor schedule task, not a benign project assumption', 'Enforce pre-pilot CSV data validation and dry-run syntax audits with formal admin sign-off'],
            ['6', 'Push suppression on aggressive battery saver phones (I-03)', 'Testing executed primarily on modern developer handsets, masking legacy budget OEM aggressive power policies', 'Physical test matrices must match actual demographic hardware profiles, not modern devices', 'Integrate dedicated low-end Android 8 devices into test racks; publish OS-specific guidance'],
        ],
        [0.5*cm, 3.4*cm, 3.4*cm, 3.4*cm, INNER_W - 10.7*cm], st))

    story.append(PageTracker('s8_3', page_map))
    story.append(Paragraph('8.3 Formal Project Sign-Off Matrix', st['h2']))
    story.append(make_table(
        ['Stakeholder Role', 'Sign-Off Authority', 'Governance Decision / Scope Endorsement', 'Formal Status'],
        [
            ['Project Manager', 'Kishan Ojha', 'Closure Note, Traceability Matrix, and Engineering Metrics Certified', 'APPROVED & SIGNED'],
            ['Group Management Sponsor', 'Representative', 'Conditional Rollout to Remaining 10 Institutions Endorsed', 'APPROVED (CONDITIONAL)'],
            ['Quality Assurance Lead', 'Developer/QA (P3)', '94.4% Defect Removal Efficiency and Test Logs Verified', 'CERTIFIED & ACCEPTED'],
            ['School 1 Principal', 'Campus Representative', 'Pilot Operational Handover and Faculty Transition Confirmed', 'ACCEPTED'],
            ['School 2 Principal', 'Campus Representative', 'Pilot Operational Handover and Faculty Transition Confirmed', 'ACCEPTED'],
        ],
        [3.5*cm, 3.5*cm, 6.2*cm, INNER_W - 13.2*cm], st))

    # ── FINAL CLOSING CARD ──────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Spacer(1, 4.0*cm))
    end_bar = Table(
        [[Paragraph('SCHOOLDIARY · CASE STUDY #111 · FORMAL PROJECT REPORT', ParagraphStyle('eb',
            fontName='Helvetica-Bold', fontSize=11, textColor=WHITE, alignment=TA_CENTER))]],
        colWidths=[INNER_W])
    end_bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('TOPPADDING',  (0,0), (-1,-1), 14),
        ('BOTTOMPADDING',(0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(end_bar)
    story.append(Spacer(1, 0.6*cm))
    story.append(coral_rule())
    story.append(Paragraph(
        'Sole Author: <b>Kishan Ojha</b> · B.Tech Computer Science &amp; Engineering (2025–2029)',
        ParagraphStyle('ft', fontName='Helvetica', fontSize=9, textColor=NAVY, alignment=TA_CENTER)))
    story.append(Paragraph(
        'Academic Evaluation: Software Engineering &amp; Project Management — Semester III',
        ParagraphStyle('ft1', fontName='Helvetica', fontSize=8.5, textColor=SLATE, alignment=TA_CENTER)))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        'Comprehensive Engineering Deliverables: IEEE 830 SRS · UML Package · CPM Network Plan · '
        'Estimation Formulas · Scope Boundary Matrix · IEEE 829 Test Suite · Risk Register &amp; RMMM · Closure Note',
        ParagraphStyle('ft2', fontName='Helvetica', fontSize=8, textColor=SLATE, alignment=TA_CENTER, spaceAfter=8)))
    story.append(Paragraph(
        'All empirical pilot results, defect data, issue records, and interview statements are simulated academic artefacts '
        'constructed in strict adherence to the Case 111 problem specification.',
        ParagraphStyle('disc', fontName='Helvetica-Oblique', fontSize=7.5, textColor=MID_GREY, alignment=TA_CENTER)))

    return story

# ─── TWO-PASS BUILD CONTROLLER ────────────────────────────────────────────────
def generate_complete_pdf():
    print("Beginning professional PDF generation for SchoolDiary Case 111...")
    
    st = build_styles()
    page_map = {}

    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=2.2*cm, bottomMargin=2.0*cm,
        title='SchoolDiary Case 111 — Complete Project Report',
        author='Kishan Ojha',
        subject='Software Engineering & Project Management'
    )

    # PASS 1: Dry run to record exact page numbers
    print("Pass 1: Mapping flowable page locations...")
    story_pass1 = build_story(page_map, st)
    doc.build(story_pass1, canvasmaker=NumberedCanvas)
    print(f"Pass 1 complete. Mapped {len(page_map)} structural anchors: {page_map}")

    # PASS 2: Final production build with exact TOC numbers
    print("Pass 2: Generating final publication PDF with exact TOC references...")
    story_pass2 = build_story(page_map, st)
    doc.build(story_pass2, canvasmaker=NumberedCanvas)
    print(f"\n✅ SUCCESS: Publication-grade PDF generated successfully!\nFile path: {OUTPUT}")

if __name__ == '__main__':
    generate_complete_pdf()
