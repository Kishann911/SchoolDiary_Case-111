"""
Generate high-resolution minimalist diagrams for SchoolDiary Case 111 PDF.
Color scheme: Slate Navy (#1B2A4A), Coral (#E05A4E), Teal (#2D7D8E), Light Grey (#F7F9FC).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

DIAGRAMS_DIR = os.path.join(os.path.dirname(__file__), "diagrams")
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

# Shared styles
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

NAVY = "#1B2A4A"
CORAL = "#E05A4E"
TEAL = "#2D7D8E"
SLATE = "#4A5568"
LIGHT_GREY = "#F7F9FC"
MID_GREY = "#CBD5E0"
WHITE = "#FFFFFF"

# ─── 1. CPM NETWORK DIAGRAM ──────────────────────────────────────────────────
def make_cpm_network():
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=300)
    ax.set_facecolor(WHITE)
    fig.patch.set_facecolor(WHITE)
    
    # Task definitions: (id, name, dur, ES, EF, LS, LF, float, critical, (x, y))
    nodes = {
        'A': ('A: Notices', '8d', '0/8', '0/8', 'F:0', True, (1.2, 3.2)),
        'B': ('B: Homework', '10d', '8/18', '8/18', 'F:0', True, (3.8, 3.2)),
        'F': ('F: Admin Panel', '10d', '0/10', '2/12', 'F:2', False, (1.2, 1.2)),
        'C': ('C: Attendance', '6d', '10/16', '12/18', 'F:2', False, (3.8, 1.8)),
        'D': ('D: Fee Reminders', '5d', '10/15', '13/18', 'F:3', False, (3.8, 0.6)),
        'E': ('E: Messaging', '12d', '0/12', '6/18', 'F:6', False, (2.5, 4.2)),
        'G': ('G: Testing', '4d', '18/22', '18/22', 'F:0', True, (6.5, 2.5)),
        'H': ('H: Training', '5d', '22/27', '22/27', 'F:0', True, (8.8, 2.5)),
    }
    
    # Draw edges
    edges = [
        ('A', 'B', True),
        ('F', 'C', False),
        ('F', 'D', False),
        ('B', 'G', True),
        ('C', 'G', False),
        ('D', 'G', False),
        ('E', 'G', False),
        ('G', 'H', True),
    ]
    
    for u, v, crit in edges:
        x1, y1 = nodes[u][6]
        x2, y2 = nodes[v][6]
        color = CORAL if crit else MID_GREY
        lw = 2.5 if crit else 1.2
        ax.annotate('', xy=(x2 - 0.75, y2), xytext=(x1 + 0.75, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                    mutation_scale=14, shrinkA=0, shrinkB=0))
    
    # Draw nodes
    for k, (name, dur, es_ef, ls_lf, flt, crit, (x, y)) in nodes.items():
        bg = "#FDF2F0" if crit else LIGHT_GREY
        border = CORAL if crit else TEAL
        lw = 2.2 if crit else 1.2
        
        # Node box
        rect = patches.FancyBboxPatch((x - 0.75, y - 0.45), 1.5, 0.9,
                                      boxstyle="round,pad=0.08,rounding_size=0.15",
                                      facecolor=bg, edgecolor=border, lw=lw)
        ax.add_patch(rect)
        
        # Text
        ax.text(x, y + 0.22, name, ha='center', va='center', fontsize=9, fontweight='bold',
                color=NAVY)
        ax.text(x, y + 0.02, f"Dur: {dur}  |  {flt}", ha='center', va='center', fontsize=7.5,
                color=CORAL if crit else SLATE, fontweight='bold' if crit else 'normal')
        ax.text(x, y - 0.22, f"ES/EF: {es_ef}   LS/LF: {ls_lf}", ha='center', va='center',
                fontsize=6.8, color=SLATE)
        
    ax.set_xlim(-0.2, 10.0)
    ax.set_ylim(-0.2, 5.0)
    ax.axis('off')
    
    # Legend
    leg_box = patches.FancyBboxPatch((0.2, 4.4), 4.2, 0.5, boxstyle="round,pad=0.05",
                                     facecolor=WHITE, edgecolor=MID_GREY, lw=0.8)
    ax.add_patch(leg_box)
    ax.plot([0.35, 0.75], [4.65, 4.65], color=CORAL, lw=2.5)
    ax.text(0.85, 4.65, 'Critical Path: A -> B -> G -> H (27 Days)', va='center', fontsize=7.5, fontweight='bold', color=CORAL)
    
    out_path = os.path.join(DIAGRAMS_DIR, "cpm_network.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=WHITE)
    plt.close()
    print("Saved:", out_path)

# ─── 2. GANTT CHART ──────────────────────────────────────────────────────────
def make_gantt():
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    ax.set_facecolor(WHITE)
    fig.patch.set_facecolor(WHITE)
    
    tasks = [
        ('H: Training (P2)', 22, 5, CORAL, True, 'M4 Live (D27)'),
        ('G: Testing (P1, P2, P3)', 18, 4, CORAL, True, 'M3 Exit (D22)'),
        ('D: Fee Reminders (P3)', 12, 5, TEAL, False, 'Float 3d'),
        ('C: Attendance Alerts (P1)', 10, 6, TEAL, False, 'Float 2d'),
        ('B: Homework (P2)', 8, 10, CORAL, True, 'M2 Freeze (D18)'),
        ('E: Messaging (P3)', 0, 12, TEAL, False, 'Float 6d'),
        ('F: Admin Panel (P1)', 0, 10, TEAL, False, 'M1 Admin (D10)'),
        ('A: Notices (P2)', 0, 8, CORAL, True, 'Critical'),
    ]
    
    y_pos = np.arange(len(tasks))
    
    for i, (name, start, dur, color, is_crit, annot) in enumerate(tasks):
        # Bar
        ax.barh(y_pos[i], dur, left=start, height=0.55, align='center',
                color=color, alpha=0.9, edgecolor=NAVY, linewidth=0.8)
        # Text label inside/next to bar
        ax.text(start + dur/2, y_pos[i], f"{dur}d", ha='center', va='center',
                color=WHITE, fontsize=8, fontweight='bold')
        # Annotation on right
        ax.text(start + dur + 0.4, y_pos[i], annot, ha='left', va='center',
                color=CORAL if is_crit else SLATE, fontsize=7.5,
                fontweight='bold' if is_crit else 'normal')
        
    ax.set_yticks(y_pos)
    ax.set_yticklabels([t[0] for t in tasks], fontsize=8.5, fontweight='bold', color=NAVY)
    ax.set_xlabel('Project Working Days (Day 0 to Day 27)', fontsize=8.5, fontweight='bold', color=NAVY)
    ax.set_xlim(0, 31)
    
    # Milestone vertical lines
    milestones = [
        (10, 'M1 (D10)', TEAL),
        (18, 'M2 (D18)', CORAL),
        (22, 'M3 (D22)', CORAL),
        (27, 'M4 (D27)', CORAL)
    ]
    for day, label, c in milestones:
        ax.axvline(x=day, color=c, linestyle='--', lw=1.2, alpha=0.8)
    
    # Grid lines
    ax.xaxis.grid(True, linestyle=':', alpha=0.4, color=MID_GREY)
    ax.set_axisbelow(True)
    
    # Styling spines
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(MID_GREY)
    
    out_path = os.path.join(DIAGRAMS_DIR, "gantt_chart.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=WHITE)
    plt.close()
    print("Saved:", out_path)

# ─── 3. LOOSE COUPLING ARCHITECTURE ──────────────────────────────────────────
def make_architecture():
    fig, ax = plt.subplots(figsize=(9, 4.4), dpi=300)
    ax.set_facecolor(WHITE)
    fig.patch.set_facecolor(WHITE)
    
    # Boxes
    boxes = {
        'notice': ('NoticeService\n(Notices & Approvals)', (1.2, 3.2), TEAL, WHITE),
        'msg': ('MessagingService\n(Threads & Hours)', (1.2, 1.2), TEAL, WHITE),
        'policy': ('MessagingPolicy\n(Pure Rules Engine\n07:00-19:59 IST)', (1.2, 2.2), NAVY, WHITE),
        'dispatch': ('NotificationDispatcher\n(Idempotency, Retries,\nFan-Out Queue)', (4.5, 2.2), CORAL, WHITE),
        'gateway': ('<<interface>>\nPushGateway', (7.2, 2.2), LIGHT_GREY, NAVY),
        'fcm': ('FcmPushAdapter\n(Google FCM)', (7.2, 1.0), LIGHT_GREY, NAVY),
    }
    
    for k, (text, (x, y), bg, fg) in boxes.items():
        w, h = (2.2, 0.85) if k != 'policy' else (2.2, 0.75)
        rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                      boxstyle="round,pad=0.08,rounding_size=0.12",
                                      facecolor=bg, edgecolor=NAVY, lw=1.2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=7.8, fontweight='bold', color=fg)
    
    # No dependency crossed link between Notice and Msg
    ax.plot([1.2, 1.2], [2.7, 1.7], color="#E05A4E", lw=2, linestyle=':')
    ax.text(1.2, 2.2, 'X  ZERO COUPLING / NO CALL', ha='center', va='center',
            fontsize=7, fontweight='bold', color=WHITE,
            bbox=dict(boxstyle='round,pad=0.2', facecolor=CORAL, edgecolor='none'))
    
    # Arrows from Notice & Msg to Dispatcher
    ax.annotate('', xy=(3.3, 2.45), xytext=(2.3, 3.2),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.6))
    ax.text(2.6, 2.95, 'NoticePublished (event)', fontsize=7, color=TEAL, fontweight='bold')
    
    ax.annotate('', xy=(3.3, 1.95), xytext=(2.3, 1.2),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.6))
    ax.text(2.6, 1.45, 'MessageReady (event)', fontsize=7, color=TEAL, fontweight='bold')
    
    # Arrow from Dispatcher to PushGateway
    ax.annotate('', xy=(6.0, 2.2), xytext=(5.6, 2.2),
                arrowprops=dict(arrowstyle="-|>", color=CORAL, lw=1.8))
    ax.text(5.8, 2.35, 'push()', fontsize=7.5, color=NAVY, fontweight='bold', ha='center')
    
    # Implement interface arrow
    ax.annotate('', xy=(7.2, 1.7), xytext=(7.2, 1.45),
                arrowprops=dict(arrowstyle="-|>", color=SLATE, lw=1.2, linestyle='--'))
    ax.text(7.35, 1.58, 'implements', fontsize=6.8, color=SLATE)
    
    ax.set_xlim(-0.2, 8.8)
    ax.set_ylim(0.4, 4.0)
    ax.axis('off')
    
    out_path = os.path.join(DIAGRAMS_DIR, "architecture.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=WHITE)
    plt.close()
    print("Saved:", out_path)

# ─── 4. RISK MATRIX HEATMAP ──────────────────────────────────────────────────
def make_risk_matrix():
    fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=300)
    ax.set_facecolor(WHITE)
    fig.patch.set_facecolor(WHITE)
    
    # 5x5 grid (Impact x Probability)
    # Impact 5 at top, 1 at bottom; Prob 1 at left, 5 at right
    matrix = np.array([
        [5, 10, 15, 20, 25],  # I=5
        [4,  8, 12, 16, 20],  # I=4
        [3,  6,  9, 12, 15],  # I=3
        [2,  4,  6,  8, 10],  # I=2
        [1,  2,  3,  4,  5],  # I=1
    ])
    
    # Background colors based on exposure bands
    # Low <= 8 (#EBF4E8 - light green), Med 9-14 (#FFF8E1 - light yellow), High >= 15 (#FFEBEE - light red)
    cmap_custom = np.zeros((5, 5, 3))
    for r in range(5):
        for c in range(5):
            val = matrix[r, c]
            if val >= 15:
                cmap_custom[r, c] = [0.98, 0.88, 0.88] # light red
            elif val >= 9:
                cmap_custom[r, c] = [1.0, 0.96, 0.86]  # light yellow
            else:
                cmap_custom[r, c] = [0.93, 0.96, 0.93] # light green
                
    ax.imshow(cmap_custom, aspect='auto')
    
    # Risk placements: (r, c, risk_label)
    # r=0 corresponds to I=5, c=0 corresponds to P=1
    risks = [
        (0, 3, "R1 (20)\nLow Adoption"),   # I5, P4
        (0, 1, "R4 (10)\nPrivacy"),        # I5, P2
        (1, 2, "R2, R5 (12)\nPush / Strict"), # I4, P3
        (2, 3, "R3 (12)\nWhatsApp"),       # I3, P4
        (2, 2, "R6, R7 (9)\nRoster / Slip"),# I3, P3
        (2, 1, "R8 (6)\nActive Def"),      # I3, P2
    ]
    
    for r, c, label in risks:
        is_high = matrix[r, c] >= 15
        color = CORAL if is_high else (NAVY if matrix[r, c] >= 9 else TEAL)
        ax.text(c, r, label, ha='center', va='center', fontsize=8, fontweight='bold',
                color=color, bbox=dict(boxstyle='round,pad=0.2', facecolor=WHITE, edgecolor=color, lw=1.2))
        
    ax.set_xticks(np.arange(5))
    ax.set_yticks(np.arange(5))
    ax.set_xticklabels(['P1: Very Low', 'P2: Low', 'P3: Med', 'P4: High', 'P5: Very High'], fontsize=7.5, fontweight='bold', color=NAVY)
    ax.set_yticklabels(['I5: Very High', 'I4: High', 'I3: Med', 'I2: Low', 'I1: Very Low'], fontsize=7.5, fontweight='bold', color=NAVY)
    ax.set_title('Probability × Impact Risk Matrix (Ranked by Exposure)', fontsize=9, fontweight='bold', color=NAVY, pad=10)
    
    # Grid lines
    ax.set_xticks(np.arange(-.5, 5, 1), minor=True)
    ax.set_yticks(np.arange(-.5, 5, 1), minor=True)
    ax.grid(which='minor', color=MID_GREY, linestyle='-', linewidth=1)
    ax.tick_params(which='minor', size=0)
    
    out_path = os.path.join(DIAGRAMS_DIR, "risk_matrix.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=WHITE)
    plt.close()
    print("Saved:", out_path)

# ─── 5. DEFECT DENSITY BY MODULE ─────────────────────────────────────────────
def make_defect_chart():
    fig, ax = plt.subplots(figsize=(7, 3.8), dpi=300)
    ax.set_facecolor(WHITE)
    fig.patch.set_facecolor(WHITE)
    
    modules = ['Admin', 'Homework', 'Fee Reminders', 'Notices', 'Attendance', 'Messaging']
    densities = [2.80, 3.57, 3.75, 4.17, 4.44, 5.45]
    colors_list = [TEAL, TEAL, TEAL, TEAL, TEAL, CORAL]
    
    bars = ax.bar(modules, densities, color=colors_list, width=0.55, edgecolor=NAVY, linewidth=0.8)
    
    # Benchmark line
    ax.axhline(y=4.0, color=CORAL, linestyle='--', lw=1.5, label='Overall Average: 4.0 defects/KLOC')
    
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.12, f"{h:.2f}",
                ha='center', va='bottom', fontsize=8, fontweight='bold', color=NAVY)
        
    ax.set_ylabel('Defect Density (defects / KLOC)', fontsize=8, fontweight='bold', color=NAVY)
    ax.set_title('Defect Density by Module (Messaging is Highest: 5.45 / KLOC)', fontsize=9, fontweight='bold', color=NAVY, pad=10)
    ax.set_ylim(0, 6.5)
    ax.legend(loc='upper left', fontsize=7.5)
    
    # Styling
    ax.yaxis.grid(True, linestyle=':', alpha=0.5, color=MID_GREY)
    ax.set_axisbelow(True)
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(MID_GREY)
    
    out_path = os.path.join(DIAGRAMS_DIR, "defect_density.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=WHITE)
    plt.close()
    print("Saved:", out_path)

if __name__ == '__main__':
    make_cpm_network()
    make_gantt()
    make_architecture()
    make_risk_matrix()
    make_defect_chart()
    print("All diagrams generated successfully!")
