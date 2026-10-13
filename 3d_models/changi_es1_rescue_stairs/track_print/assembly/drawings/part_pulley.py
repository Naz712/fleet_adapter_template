#!/usr/bin/env python3
"""Part drawing: Timing pulley HTD 5M, 20 teeth (bought) for the 1:5 ES1 stair-climber prototype.

Every number on the sheet comes from assembly/parts_spec.json (parts.pulley, and parts.track.teeth
for the track tooth in the groove detail). The groove shape is the track tooth from
generate_track.tooth_outline sunk into the pulley's outside circle with 0.15 mm clearance, the
way preview_track.pulley_outline and generate_track.stand_in_pulley make it.

Two kinds of dimension are on the sheet:
  * marked with an asterisk  -> the ORDER SPEC (20 T HTD 5M, 15 mm belt, 8 mm bore); these are
                                 what the track is designed to and what MISUMI is asked for.
  unmarked                   -> the printed PLA stand-in's sizes (flanges, hub, lengths, set screw);
                                 the vendor's drawing overrides them.

Run:  python3 part_pulley.py   ->  drawings/part_pulley.png
"""
import math
import sys

import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

sys.path.insert(0, "/home/user/fleet_adapter_template/3d_models/changi_es1_rescue_stairs/track_print/assembly")
sys.path.insert(0, "/home/user/fleet_adapter_template/3d_models/changi_es1_rescue_stairs/track_print")
from drawing import (DIM, FILL, INK, MUTED, SPEC, centreline, circle, dim_dia, dim_h, dim_v, leader,  # noqa: E402
                     note_block, outline, rect, save, sheet)
import generate_track as gt  # noqa: E402  (tooth_outline: the HTD-style tooth the grooves are cut for)

# --------------------------------------------------------------------------- numbers (parts_spec.json)
P = SPEC["parts"]["pulley"]
TE = SPEC["parts"]["track"]["teeth"]
N_T = P["teeth"]                                   # 20
PD, OD, FD = P["pitch_dia_mm"], P["outside_dia_mm"], P["flange_dia_mm"]      # 31.83, 30.69, 35.7
FL_T, FACE, HUB_D, HUB_L = (P["flange_thickness_mm"], P["face_width_between_flanges_mm"],
                            P["hub_dia_mm"], P["hub_length_mm"])            # 1.5, 17, 18, 7
OAL, BORE = P["overall_length_mm"], P["bore_mm"]                              # 27, 8
QTY, QTY_SEG, VENDOR = P["qty_total"], P["qty_per_segment"], P["vendor"]
STAND_IN = P["stand_in_file"].split(" ")[0]
# track tooth (parts.track.teeth): what the groove has to take
T_PITCH, T_H, T_W, T_R = TE["pitch_mm"], TE["height_mm"], TE["root_width_mm"], TE["tip_radius_mm"]  # 5, 2, 2.9, 1.45
BELT_W = SPEC["parts"]["track"]["width_mm"]       # 15: "for 15 mm belt" in spec_to_order
BACKING = SPEC["parts"]["track"]["backing_thickness_mm"]   # 1.4, drawn in the groove detail

# Derived (listed in the result notes)
R_PD, R_OD, R_FD, R_HUB, R_BORE = PD / 2, OD / 2, FD / 2, HUB_D / 2, BORE / 2
PLD = round((PD - OD) / 2, 2)                     # 0.57: pitch line to tooth-root circle, from the two spec diameters
CLEAR = 0.15                                      # groove clearance round the tooth: generate_track.stand_in_pulley(clearance=0.15)
GROOVE_D = round(T_H + CLEAR, 2)                  # 2.15: groove depth below the outside circle
SCREW_FROM_END = HUB_L / 2                        # 3.5: generate_track.stand_in_pulley puts the M3 hole at mid hub
SCREW_M, SCREW_L = 3, 6                           # "M3 x 6 for the stand-in" (parts.set_screws_and_bolts)
assert abs(2 * FL_T + FACE + HUB_L - OAL) < 1e-6, "overall length must be flange + face + flange + hub"
assert abs(N_T * T_PITCH / math.pi - PD) < 0.01, "pitch dia must be 20 x 5 / pi"

# generate_track's Design holds the same tooth numbers; check, then use its tooth_outline for the grooves
D = gt.Design()
G = gt.Geometry(D)
assert (D.tooth_height, D.tooth_radius, D.belt_pitch, D.pulley_teeth) == (T_H, T_R, T_PITCH, N_T)
assert abs(G.root - R_OD) < 0.01

# section plane angles: the end view is cut so a groove sits at 12 o'clock (and, 20 being even, at 6 o'clock)
GROOVE_AT = math.pi / 2


# --------------------------------------------------------------------------- profile builders
def on_circle(points, radius, phi, outward):
    u = np.array([math.cos(phi), math.sin(phi)])
    v = np.array([-math.sin(phi), math.cos(phi)])
    return [tuple((radius + outward * h) * u + t * v) for t, h in points]


def groove_shape():
    """One groove in the tooth's own frame: the track tooth (sunk 0.5 so the cut is clean) plus clearance."""
    return Polygon(gt.tooth_outline(D, sink=0.5)).buffer(CLEAR, quad_segs=8)


def pulley_section(centre=(0.0, 0.0)):
    """The toothed body cut across: outside circle minus 20 grooves, bore in the middle."""
    g = groove_shape()
    grooves = [Polygon(on_circle(list(g.exterior.coords), R_OD, GROOVE_AT + 2 * math.pi * k / N_T, -1))
               for k in range(N_T)]
    body = Point(0, 0).buffer(R_OD, quad_segs=90).difference(unary_union(grooves))
    body = body.difference(Point(0, 0).buffer(R_BORE, quad_segs=60))
    from shapely.affinity import translate
    return translate(body, *centre)


def track_on_pulley():
    """The track wrapped on the pulley (teeth every 18 deg, backing outside); no cleats."""
    backing = Point(0, 0).buffer(R_OD + BACKING, quad_segs=120).difference(Point(0, 0).buffer(R_OD, quad_segs=120))
    teeth = [Polygon(on_circle(gt.tooth_outline(D, sink=0.3), R_OD, GROOVE_AT + 2 * math.pi * k / N_T, -1))
             for k in range(N_T)]
    shape = unary_union([backing] + teeth)
    fil = SPEC["parts"]["track"]["cleats"]["root_fillet_mm"]
    return shape.buffer(fil, quad_segs=12).buffer(-fil, quad_segs=12)


def draw_shape(ax, shape, fill, hatch=False, lw=0.6, shift=(0.0, 0.0)):
    polys = list(shape.geoms) if hasattr(shape, "geoms") else [shape]
    for p in polys:
        if p.is_empty:
            continue
        outline(ax, [(x + shift[0], y + shift[1]) for x, y in p.exterior.coords], fill, lw=lw, hatch=hatch)
        for hole in p.interiors:
            outline(ax, [(x + shift[0], y + shift[1]) for x, y in hole.coords], "white", lw=lw)


def cut_mark(ax, x0, y0, x1, y1, letter, arrow_dir, stub=4.0, gap=1.5):
    """Section plane: thick stubs just outside the part at both ends, arrows for the viewing direction."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    ax.plot([x0, x1], [y0, y1], color=DIM, lw=0.5, dashes=(8, 2, 1.5, 2))
    for (px, py), s in (((x0, y0), -1), ((x1, y1), +1)):
        ex, ey = px + s * ux * stub, py + s * uy * stub
        ax.plot([px, ex], [py, ey], color=INK, lw=1.6)
        ax.annotate("", xy=(ex + arrow_dir[0] * 4.5, ey + arrow_dir[1] * 4.5), xytext=(ex, ey),
                    arrowprops=dict(arrowstyle="-|>", lw=0.8, color=INK, mutation_scale=9))
        ax.text(ex + s * ux * gap * 1.6 + arrow_dir[0] * 1.5, ey + s * uy * gap * 1.6 + arrow_dir[1] * 1.5, letter,
                fontsize=10, fontweight="bold", color=INK, ha="center", va="center")


def dim_arc(ax, cx, cy, r, a0_deg, a1_deg, text, text_r, fontsize=8):
    """Dimension along an arc (for the 5 mm pitch, which is an arc length on the pitch line)."""
    ax.add_patch(Arc((cx, cy), 2 * r, 2 * r, theta1=min(a0_deg, a1_deg), theta2=max(a0_deg, a1_deg), color=DIM, lw=0.6))
    for a, s in ((a0_deg, +1), (a1_deg, -1)):
        ar = math.radians(a)
        tip = (cx + r * math.cos(ar), cy + r * math.sin(ar))
        # arrowhead tangent to the arc, pointing outward from the span
        s = +1 if a == max(a0_deg, a1_deg) else -1
        tail = (tip[0] - s * 0.9 * math.sin(ar) * -1, tip[1] - s * 0.9 * math.cos(ar))
        ax.add_patch(FancyArrowPatch(tail, tip, arrowstyle="-|>", mutation_scale=7, lw=0.6, color=DIM, shrinkA=0, shrinkB=0))
    am = math.radians((a0_deg + a1_deg) / 2)
    ax.text(cx + text_r * math.cos(am), cy + text_r * math.sin(am), text, ha="center", va="center", fontsize=fontsize,
            color=INK, bbox=dict(fc="white", ec="none", pad=0.8))


# --------------------------------------------------------------------------- sheet
FIG_W, FIG_H = 11.0, 7.5
fig, add_view = sheet("TIMING PULLEY  -  HTD 5M, 20 teeth, bought",
                      "ES1 stair-climbing rescue carrier, 1:5 prototype, track segment.   Part: Timing pulley HTD 5M 20T, "
                      f"for {BELT_W:g} mm belt, {BORE:g} mm bore.   Dimensions in mm at model size.   Sheet 1 of 1.",
                      size=(FIG_W, FIG_H))


def view(left, bottom, width, xlim, ylim, name):
    """Equal-aspect axes whose box exactly fits the data window, anchored at its bottom-left."""
    xr, yr = xlim[1] - xlim[0], ylim[1] - ylim[0]
    height = width * (FIG_W / FIG_H) * (yr / xr)
    ax = add_view([left, bottom, width, height], name)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_anchor("SW")
    return ax


# ---- (1) section A-A: cut along the axle ---------------------------------------------------
# x along the axle, 0 at the outer face of the first flange; y radial. Hatched = solid metal/PLA.
ax1 = view(0.03, 0.40, 0.42, (-18.0, 52.0), (-26.0, 31.0),
           "SECTION A-A  -  cut along the axle line; teeth shown unsectioned, as for gears")
X_F1, X_BODY, X_F2, X_HUB = 0.0, FL_T, FL_T + FACE, 2 * FL_T + FACE          # 0, 1.5, 18.5, 20
R_GROOVE = R_OD - GROOVE_D                                                   # groove bottoms
for s in (+1, -1):  # upper and lower halves
    y = lambda r: s * r
    rect(ax1, X_F1, min(y(R_BORE), y(R_FD)), FL_T, R_FD - R_BORE, FILL["pla"], hatch=True)          # flange 1
    rect(ax1, X_F2, min(y(R_BORE), y(R_FD)), FL_T, R_FD - R_BORE, FILL["pla"], hatch=True)          # flange 2
    rect(ax1, X_BODY, min(y(R_BORE), y(R_GROOVE)), FACE, R_GROOVE - R_BORE, FILL["pla"], hatch=True)  # body to the groove bottoms
    rect(ax1, X_BODY, min(y(R_GROOVE), y(R_OD)), FACE, R_OD - R_GROOVE, FILL["pla"], hatch=False)   # tooth band, unsectioned
    rect(ax1, X_HUB, min(y(R_BORE), y(R_HUB)), HUB_L, R_HUB - R_BORE, FILL["pla"], hatch=True)       # hub
# bore: a white band through everything
rect(ax1, X_F1, -R_BORE, OAL, 2 * R_BORE, "white", lw=0.8)
centreline(ax1, -6, 0, OAL + 6, 0)
# set screw: M3 x 6 at mid hub, radial, in the upper half. Hole = M3 tap drill 2.5 (generate_track: r 1.25)
X_S = X_HUB + SCREW_FROM_END
rect(ax1, X_S - 1.25, R_BORE, 2.5, R_HUB - R_BORE, "white", lw=0.6)                 # tapped hole
rect(ax1, X_S - SCREW_M / 2, R_BORE, SCREW_M, SCREW_L, FILL["steel"], lw=0.6)        # the screw, unsectioned
ax1.plot([X_S - 0.9, X_S + 0.9], [R_BORE + SCREW_L - 0.9] * 2, color=INK, lw=0.6)    # hex socket, a hint
# cutting plane B-B across the body, for the end view
cut_mark(ax1, X_BODY + FACE / 2, -R_FD - 2.0, X_BODY + FACE / 2, R_FD + 2.0, "B", arrow_dir=(1, 0))
# --- dimensions, lengths (horizontal) above and below
dim_h(ax1, X_F1, X_BODY, R_FD + 5.0, f"{FL_T:g}", ext_from=R_FD, offset=0.2)
dim_h(ax1, X_BODY, X_F2, R_FD + 5.0, f"{FACE:g} between flanges", ext_from=R_OD, offset=0.2)
dim_h(ax1, X_F2, X_HUB, R_FD + 5.0, f"{FL_T:g}", ext_from=R_FD, offset=0.2)
dim_h(ax1, X_HUB, OAL, R_HUB + 3.0, f"{HUB_L:g} hub", ext_from=R_HUB, offset=0.2)
dim_h(ax1, X_S, OAL, R_HUB + 8.5, f"{SCREW_FROM_END:g}", ext_from=R_HUB + 0.2, offset=0.2)
dim_h(ax1, X_F1, OAL, -R_FD - 6.0, f"{OAL:g} overall", ext_from=-R_FD, offset=-3.6)
# --- dimensions, diameters (vertical) at the left and right
dim_v(ax1, -R_FD, R_FD, -7.0, f"Ø{FD:g} flange", ext_from=X_F1, offset=-0.3)
dim_v(ax1, -R_OD, R_OD, -13.5, f"Ø{OD:g} *", ext_from=X_BODY + 0.2, offset=-0.3)
dim_v(ax1, -R_HUB, R_HUB, OAL + 7.0, f"Ø{HUB_D:g} hub", ext_from=OAL, offset=0.3)
dim_v(ax1, -R_BORE, R_BORE, OAL + 13.5, f"Ø{BORE:g} bore *", ext_from=OAL, offset=0.3)
leader(ax1, (X_S + SCREW_M / 2, R_BORE + SCREW_L - 1.0), (OAL + 5.5, R_FD + 6.5),
       f"set screw M{SCREW_M} x {SCREW_L}, 1 off (stand-in)\nbought: usually 2 x M4 at 90°, per vendor", fontsize=7.5)
leader(ax1, (X_BODY + 3.5, -R_GROOVE + 0.2), (-17.5, -R_FD - 12.5),
       f"groove bottoms Ø{2 * R_GROOVE:.2f}  ({GROOVE_D:g} deep)", fontsize=7.5)
ax1.text(-18.0, -25.6, "A-A is the plane marked on the end view; B-B (above) is the plane of the end view.",
         fontsize=7.5, color=MUTED, ha="left", va="bottom")

# ---- (2) end view = section B-B across the toothed body --------------------------------------
ax2 = view(0.50, 0.40, 0.30, (-30.0, 55.0), (-29.0, 31.0),
           "END VIEW, SECTION B-B  -  looking at the hub end; 20 grooves")
circle(ax2, 0, 0, R_FD, fill=FILL["light"], lw=0.6)                         # far flange, seen behind the body
draw_shape(ax2, pulley_section(), FILL["pla"], hatch=True)                  # the body, cut
circle(ax2, 0, 0, R_HUB, fill="none", lw=0.6, ls=(0, (4, 2)))               # hub behind the body: hidden
circle(ax2, 0, 0, R_PD, fill="none", lw=0.5, ls=(0, (8, 2, 1.5, 2)))        # pitch circle, reference
rect(ax2, -1.25, R_BORE, 2.5, R_HUB - R_BORE, "none", lw=0.5)               # set-screw hole behind: hidden
for p in ax2.patches[-1:]:
    p.set_linestyle((0, (3, 1.5)))
centreline(ax2, -14, 0, 14, 0)
centreline(ax2, 0, -14, 0, 14)
cut_mark(ax2, -R_FD - 3.0, 0, R_FD + 3.0, 0, "A", arrow_dir=(0, 1))
dim_dia(ax2, 0, 0, R_FD, 55, f"Ø{FD:g} flange (behind)", length=27)
dim_dia(ax2, 0, 0, R_PD, 27, f"Ø{PD:g} pitch *", length=27)
dim_dia(ax2, 0, 0, R_OD, 9, f"Ø{OD:g} outside *", length=27)
dim_dia(ax2, 0, 0, R_HUB, -16, f"Ø{HUB_D:g} hub (hidden)", length=27)
dim_dia(ax2, 0, 0, R_BORE, -40, f"Ø{BORE:g} bore *", length=27)
a = math.radians(GROOVE_AT) + 2 * math.pi * 2 / N_T  # a groove on the upper left
leader(ax2, (R_OD * math.cos(a), R_OD * math.sin(a)), (-29.5, 27.5),
       f"{N_T} grooves, pitch {T_PITCH:g} *\n(HTD 5M)", fontsize=7.5)
leader(ax2, (-1.25, R_BORE + 2.5), (-29.5, -20.0), "set-screw hole\n(hidden, 12 o'clock)", fontsize=7.5)

# ---- (3) detail: one groove with the track tooth in it ---------------------------------------
ax3 = view(0.50, 0.045, 0.46, (-11.5, 11.5), (-6.2, 5.6),
           "DETAIL  -  one groove with the track's tooth seated, enlarged (cleats not shown)")
SH = (0.0, -R_OD)                                              # pulley centre, so the groove at 12 o'clock is at the origin
win = box(-11.5, -6.2, 11.5, 5.6)
body = pulley_section().intersection(box(-11.5 - SH[0], -6.2 - SH[1], 11.5 - SH[0], 5.6 - SH[1]))
draw_shape(ax3, body, FILL["pla"], hatch=True, shift=SH)
trk = track_on_pulley().intersection(box(-11.5 - SH[0], -6.2 - SH[1], 11.5 - SH[0], 5.6 - SH[1]))
draw_shape(ax3, trk, FILL["tpu"], hatch=False, shift=SH)
# pitch circle (reference) and the outside circle, as thin arcs
ax3.add_patch(Arc(SH, 2 * R_PD, 2 * R_PD, theta1=55, theta2=125, color=DIM, lw=0.5, ls=(0, (8, 2, 1.5, 2))))
ax3.add_patch(Arc(SH, 2 * R_OD, 2 * R_OD, theta1=55, theta2=125, color=DIM, lw=0.4, ls=(0, (6, 3))))
# radial centre lines of the groove at 12 o'clock and its neighbour at 72 deg
for ang in (90.0, 72.0):
    ar = math.radians(ang)
    centreline(ax3, SH[0] + (R_OD - 3.6) * math.cos(ar), SH[1] + (R_OD - 3.6) * math.sin(ar),
               SH[0] + (R_OD + 3.6) * math.cos(ar), SH[1] + (R_OD + 3.6) * math.sin(ar))
# tooth: height, width, tip radius (track numbers)
dim_v(ax3, -T_H, 0.0, -4.3, f"{T_H:g} tooth", ext_from=-T_R - 0.15, offset=-0.25)
dim_v(ax3, 0.0, -GROOVE_D, 4.6, f"{GROOVE_D:g} groove", ext_from=T_R + CLEAR + 0.2, offset=0.25)
dim_h(ax3, -T_W / 2, T_W / 2, -4.9, f"{T_W:g}", ext_from=-(T_H - T_R), offset=-1.0)
leader(ax3, (T_R * math.cos(math.radians(-40)), -(T_H - T_R) - T_R * math.sin(math.radians(40))), (2.6, -3.4),
       f"R{T_R:g} tooth tip", fontsize=7.5)
leader(ax3, (-(T_R + CLEAR / 2) * math.cos(math.radians(20)), -(T_H - T_R) + (T_R + CLEAR / 2) * math.sin(math.radians(20))),
       (-11.3, -2.6), f"{CLEAR:g} clearance all round\n(stand-in; vendor's groove\nis the HTD 5M standard)", fontsize=7.5)
# pitch line and backing
dim_v(ax3, 0.0, PLD, -7.6, f"{PLD:g}", ext_from=-6.2, offset=-0.25, fontsize=7.5)
ax3.text(-9.2, 1.95, "pitch line\nabove the\noutside Ø", fontsize=7.5, color=INK, ha="center", va="bottom", linespacing=1.2)
dim_v(ax3, 0.0, BACKING, 7.6, f"{BACKING:g}", ext_from=6.2, offset=0.25, fontsize=7.5)
ax3.text(9.3, 1.95, "track\nbacking", fontsize=7.5, color=INK, ha="center", va="bottom", linespacing=1.2)
dim_arc(ax3, SH[0], SH[1], R_PD + 2.6, 72, 90, f"{T_PITCH:g} pitch *\n(arc on the pitch line)", R_PD + 4.3, fontsize=7.5)
ax3.text(0.0, -5.95, "pulley body (hatched)  -  track tooth in dark grey, TPU, from part_track.png",
         fontsize=7.5, color=MUTED, ha="center", va="bottom")

# ---- notes -------------------------------------------------------------------------------------
note_block(fig, [
    "TIMING PULLEY  (parts_spec.json: parts.pulley)",
    f"Buy.   Vendor: {VENDOR.split(' (')[0]}.   Qty: {QTY} ({QTY_SEG} per segment).",
    f"Order spec:  HTD 5M, {N_T} teeth, for {BELT_W:g} mm belt, Ø{BORE:g} bore,",
    "flanges both sides, set-screw hub.   Set screws come with the pulleys.",
    "",
    f"*  = ORDER SPEC: Ø{PD:g} pitch, Ø{OD:g} outside, {N_T} grooves at {T_PITCH:g}, Ø{BORE:g} bore.",
    "   These are fixed by 20 T HTD 5M and the track is designed to them.",
    "Unmarked sizes (flanges, hub, lengths, set screw) are the printed",
    f"stand-in's; the vendor's drawing overrides them.",
    "",
    f"Stand-in: {STAND_IN}",
    "PLA, 1 off, for fit tests only, never for driving.",
    f"Axle: Ø{SPEC['parts']['axle']['dia_mm']:g} {SPEC['parts']['axle']['tolerance'].split(' ')[0]} rod, "
    "with a filed flat under each set screw.",
], x=0.03, y=0.335, w=0.44)

save(fig, "part_pulley")
