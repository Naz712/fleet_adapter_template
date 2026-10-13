#!/usr/bin/env python3
"""Part drawing: Timing pulley HTD 5M, 20 teeth (bought) for the 1:5 ES1 stair-climber prototype.

Every number on the sheet comes from assembly/parts_spec.json: parts.pulley for the pulley,
parts.track.teeth and parts.track.backing_thickness_mm for the track tooth in the groove detail,
parts.set_screws_and_bolts for the stand-in's screw. Numbers the spec is silent on are derived
in the "derived" block below and come from generate_track.py (stand_in_pulley, tooth_outline).

Two kinds of dimension are on the sheet:
  *         ORDER SPEC: 20 T HTD 5M, 15 mm belt, 8 mm bore, and what follows from it (pitch and
            outside diameters, 20 grooves at 5 mm). The track is designed to these.
  unmarked  the printed PLA stand-in's sizes (flanges, face, hub, lengths, set screw); the
            vendor's drawing overrides them.

Run:  python3 part_pulley.py   ->  drawings/part_pulley.png
"""
import math
import sys

import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch
from shapely.affinity import translate
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
N_T = P["teeth"]                                                              # 20
PD, OD, FD = P["pitch_dia_mm"], P["outside_dia_mm"], P["flange_dia_mm"]       # 31.83, 30.69, 35.7
FL_T, FACE = P["flange_thickness_mm"], P["face_width_between_flanges_mm"]     # 1.5, 17
HUB_D, HUB_L = P["hub_dia_mm"], P["hub_length_mm"]                            # 18, 7
OAL, BORE = P["overall_length_mm"], P["bore_mm"]                              # 27, 8
QTY, QTY_SEG, VENDOR = P["qty_total"], P["qty_per_segment"], P["vendor"]      # 8, 4, MISUMI Singapore (...)
STAND_IN = P["stand_in_file"].split(" ")[0]
T_PITCH, T_H, T_W, T_R = TE["pitch_mm"], TE["height_mm"], TE["root_width_mm"], TE["tip_radius_mm"]  # 5, 2, 2.9, 1.45
BELT_W = SPEC["parts"]["track"]["width_mm"]                                   # 15: "for 15 mm belt"
BACKING = SPEC["parts"]["track"]["backing_thickness_mm"]                      # 1.4
FILLET = SPEC["parts"]["track"]["cleats"]["root_fillet_mm"]                   # 0.35, tooth roots too
AXLE_D = SPEC["parts"]["axle"]["dia_mm"]                                      # 8
AXLE_TOL = SPEC["parts"]["axle"]["tolerance"].split(" ")[0]                   # h7
SCREW_M, SCREW_L = 3, 6     # "M3 x 6 for the stand-in" (parts.set_screws_and_bolts.items[0])

# --------------------------------------------------------------------------- derived (not in the spec)
R_PD, R_OD, R_FD, R_HUB, R_BORE = PD / 2, OD / 2, FD / 2, HUB_D / 2, BORE / 2
PLD = round((PD - OD) / 2, 2)             # 0.57: pitch line to outside circle, from the two spec diameters
CLEAR = 0.15                              # groove clearance round the tooth: generate_track.stand_in_pulley(clearance=0.15)
GROOVE_D = round(T_H + CLEAR, 2)          # 2.15: groove depth below the outside circle (stand-in)
R_GROOVE = R_OD - GROOVE_D                # 13.195 -> groove-bottom dia 26.39 (stand-in)
SCREW_FROM_END = HUB_L / 2                # 3.5: generate_track.stand_in_pulley puts the screw at mid hub
TAP_D = 2.5                               # M3 tap drill in the stand-in (generate_track: cylinder r 1.25)
assert abs(2 * FL_T + FACE + HUB_L - OAL) < 1e-6, "overall length = flange + face + flange + hub"
assert abs(N_T * T_PITCH / math.pi - PD) < 0.01, "pitch dia = 20 x 5 / pi"

D = gt.Design()      # the track generator holds the same tooth numbers; check, then use its tooth_outline
G = gt.Geometry(D)
assert (D.tooth_height, D.tooth_radius, D.belt_pitch, D.pulley_teeth) == (T_H, T_R, T_PITCH, N_T)
assert abs(G.root - R_OD) < 0.01

GROOVE_AT = math.pi / 2   # a groove at 12 o'clock (and, 20 being even, one at 6 o'clock)


# --------------------------------------------------------------------------- profile builders
def on_circle(points, radius, phi, outward):
    u = np.array([math.cos(phi), math.sin(phi)])
    v = np.array([-math.sin(phi), math.cos(phi)])
    return [tuple((radius + outward * h) * u + t * v) for t, h in points]


def groove_shape():
    """One groove in the tooth's own frame: the track tooth (sunk 0.5, so the cut is clean) plus clearance."""
    return Polygon(gt.tooth_outline(D, sink=0.5)).buffer(CLEAR, quad_segs=8)


def pulley_section():
    """The toothed body cut across: outside circle minus 20 grooves, bore in the middle."""
    g = list(groove_shape().exterior.coords)
    grooves = [Polygon(on_circle(g, R_OD, GROOVE_AT + 2 * math.pi * k / N_T, -1)) for k in range(N_T)]
    body = Point(0, 0).buffer(R_OD, quad_segs=90).difference(unary_union(grooves))
    return body.difference(Point(0, 0).buffer(R_BORE, quad_segs=60))


def track_on_pulley():
    """The track wrapped on the pulley: backing outside the outside circle, a tooth in every groove."""
    backing = Point(0, 0).buffer(R_OD + BACKING, quad_segs=120).difference(Point(0, 0).buffer(R_OD, quad_segs=120))
    teeth = [Polygon(on_circle(gt.tooth_outline(D, sink=0.3), R_OD, GROOVE_AT + 2 * math.pi * k / N_T, -1))
             for k in range(N_T)]
    shape = unary_union([backing] + teeth)
    return shape.buffer(FILLET, quad_segs=12).buffer(-FILLET, quad_segs=12)   # root fillets


def draw_shape(ax, shape, fill, hatch=False, lw=0.6):
    polys = list(shape.geoms) if hasattr(shape, "geoms") else [shape]
    for p in polys:
        if p.is_empty:
            continue
        outline(ax, list(p.exterior.coords), fill, lw=lw, hatch=hatch)
        for hole in p.interiors:
            outline(ax, list(hole.coords), "white", lw=lw)


def cut_plane(ax, p0, p1, stub, arrow, letter, letters_at):
    """Section plane: chain line p0-p1 through the part, thick stubs of length `stub` beyond both ends,
    an arrow at each stub for the viewing direction, the letter where letters_at says."""
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    ax.plot([x0, x1], [y0, y1], color=DIM, lw=0.5, dashes=(8, 2, 1.5, 2))
    for (px, py), s in ((p0, -1), (p1, +1)):
        ex, ey = px + s * ux * stub, py + s * uy * stub
        ax.plot([px, ex], [py, ey], color=INK, lw=1.6)
        ax.annotate("", xy=(ex + arrow[0] * 4.5, ey + arrow[1] * 4.5), xytext=(ex, ey),
                    arrowprops=dict(arrowstyle="-|>", lw=0.8, color=INK, mutation_scale=9))
    for lx, ly in letters_at:
        ax.text(lx, ly, letter, fontsize=10, fontweight="bold", color=INK, ha="center", va="center")


def dim_arc(ax, c, r, a0, a1, text, text_r, fontsize=7.5):
    """Dimension along an arc between angles a0 < a1 (deg): for the 5 mm pitch, an arc on the pitch line."""
    ax.add_patch(Arc(c, 2 * r, 2 * r, theta1=a0, theta2=a1, color=DIM, lw=0.6))
    for a, s in ((a0, -1), (a1, +1)):
        ar = math.radians(a)
        tip = (c[0] + r * math.cos(ar), c[1] + r * math.sin(ar))
        tail = (tip[0] - s * 0.6 * -math.sin(ar), tip[1] - s * 0.6 * math.cos(ar))
        ax.add_patch(FancyArrowPatch(tail, tip, arrowstyle="-|>", mutation_scale=7, lw=0.6, color=DIM, shrinkA=0, shrinkB=0))
    am = math.radians((a0 + a1) / 2)
    ax.text(c[0] + text_r * math.cos(am), c[1] + text_r * math.sin(am), text, ha="center", va="center",
            fontsize=fontsize, color=INK, bbox=dict(fc="white", ec="none", pad=0.8))


# --------------------------------------------------------------------------- sheet
FIG_W, FIG_H = 11.0, 7.5
fig, add_view = sheet("TIMING PULLEY  -  HTD 5M, 20 teeth, bought",
                      "ES1 stair-climbing rescue carrier, 1:5 prototype, track segment.   Bought part: HTD 5M 20T pulley, "
                      f"{BELT_W:g} mm belt, Ø{BORE:g} bore.   All mm at model size.   Sheet 1 of 1.",
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


# ---- (1) section A-A: cut along the axle, through the 12 o'clock groove and the set screw --------
# x along the axle, 0 at the outer face of the first flange; y radial. Hatched = cut material.
ax1 = view(0.03, 0.345, 0.38, (-17.0, 52.0), (-32.5, 31.5),
           "SECTION A-A  -  cut along the axle line (plane A-A on the end view)")
X_F1, X_BODY, X_F2, X_HUB = 0.0, FL_T, FL_T + FACE, 2 * FL_T + FACE          # 0, 1.5, 18.5, 20
for s in (+1, -1):                                                           # upper and lower halves
    lo = lambda a, b: min(s * a, s * b)  # noqa: E731
    rect(ax1, X_F1, lo(R_BORE, R_FD), FL_T, R_FD - R_BORE, FILL["pla"], hatch=True)            # flange 1
    rect(ax1, X_F2, lo(R_BORE, R_FD), FL_T, R_FD - R_BORE, FILL["pla"], hatch=True)            # flange 2
    rect(ax1, X_BODY, lo(R_BORE, R_GROOVE), FACE, R_GROOVE - R_BORE, FILL["pla"], hatch=True)  # body to the groove bottom
    rect(ax1, X_BODY, lo(R_GROOVE, R_OD), FACE, R_OD - R_GROOVE, FILL["pla"], hatch=False)     # teeth beyond the cut
    rect(ax1, X_HUB, lo(R_BORE, R_HUB), HUB_L, R_HUB - R_BORE, FILL["pla"], hatch=True)        # hub
rect(ax1, X_F1, -R_BORE, OAL, 2 * R_BORE, "white", lw=0)                      # the bore, open both ends
for yy in (R_BORE, -R_BORE):
    ax1.plot([X_F1, OAL], [yy, yy], color=INK, lw=0.8)
centreline(ax1, -4, 0, OAL + 4, 0)
# set screw: M3 x 6 at mid hub, radial, in the upper half (tapped hole 2.5, in section)
X_S = X_HUB + SCREW_FROM_END
rect(ax1, X_S - TAP_D / 2, R_BORE, TAP_D, R_HUB - R_BORE, "white", lw=0.6)
rect(ax1, X_S - SCREW_M / 2, R_BORE, SCREW_M, SCREW_L, FILL["steel"], lw=0.6)
ax1.plot([X_S - 0.8, X_S + 0.8], [R_BORE + SCREW_L - 0.8] * 2, color=INK, lw=0.6)   # hex socket, a hint
# cutting plane B-B through the body, looking towards the hub (the end view)
cut_plane(ax1, (4.0, -R_FD - 6.5), (4.0, R_FD + 6.5), 3.5, (1, 0), "B", [(5.6, 30.0), (5.6, -30.0)])
# --- lengths: a chain above (1.5 | 17 | 1.5 | 7), overall below
Y_C = R_FD + 4.5
dim_h(ax1, X_F1, X_BODY, Y_C, " ", ext_from=R_FD)
dim_h(ax1, X_BODY, X_F2, Y_C, f"{FACE:g} face", ext_from=R_FD, offset=0.3)
dim_h(ax1, X_F2, X_HUB, Y_C, " ", ext_from=R_FD)
for xx, y_from in ((X_HUB, R_FD), (OAL, R_HUB)):
    ax1.plot([xx, xx], [y_from, Y_C + 0.4], color=DIM, lw=0.5)
dim_h(ax1, X_HUB, OAL, Y_C, f"{HUB_L:g} hub", offset=0.3)
for xx in (X_F1 + FL_T / 2, X_F2 + FL_T / 2):
    ax1.text(xx, Y_C - 0.9, f"{FL_T:g}", ha="center", va="top", fontsize=8, color=INK, bbox=dict(fc="white", ec="none", pad=0.6))
dim_h(ax1, X_F1, OAL, -R_FD - 4.5, f"{OAL:g} overall", ext_from=-R_HUB, offset=0.3)
# set-screw position from the hub end
for xx in (X_S, OAL):
    ax1.plot([xx, xx], [R_BORE + SCREW_L, R_HUB + 4.9], color=DIM, lw=0.5)
dim_h(ax1, X_S, OAL, R_HUB + 4.5, f"{SCREW_FROM_END:g}", offset=0.3)
# --- diameters, left and right
dim_v(ax1, -R_OD, R_OD, -6.0, f"Ø{OD:g} outside *", ext_from=X_BODY, offset=-0.3)
dim_v(ax1, -R_FD, R_FD, -12.5, f"Ø{FD:g} flange", ext_from=X_F1, offset=-0.3)
dim_v(ax1, -R_BORE, R_BORE, OAL + 5.0, f"Ø{BORE:g} bore *", ext_from=OAL, offset=0.3)
dim_v(ax1, -R_HUB, R_HUB, OAL + 11.0, f"Ø{HUB_D:g} hub", ext_from=OAL, offset=0.3)
leader(ax1, (X_S + SCREW_M / 2, R_BORE + SCREW_L), (29.0, 13.2),
       f"M{SCREW_M} x {SCREW_L} set screw\n(stand-in); bought:\nusually 2 x M4", fontsize=7.5)
leader(ax1, (X_BODY + 3.0, -R_GROOVE), (-16.5, -28.0),
       f"groove bottom Ø{2 * R_GROOVE:.2f}\n({GROOVE_D:g} deep, stand-in)", fontsize=7.5)

# ---- (2) end view = section B-B across the toothed body ----------------------------------------
ax2 = view(0.52, 0.50, 0.36, (-30.0, 56.0), (-30.0, 30.0),
           "SECTION B-B  -  end view towards the hub; 20 grooves")
circle(ax2, 0, 0, R_FD, fill=FILL["light"], lw=0.6)                         # far flange, seen past the body
draw_shape(ax2, pulley_section(), FILL["pla"], hatch=True)                  # the body, cut
circle(ax2, 0, 0, R_HUB, fill="none", lw=0.6, ls=(0, (4, 2)))               # hub behind the body: hidden
circle(ax2, 0, 0, R_PD, fill="none", lw=0.5, ls=(0, (8, 2, 1.5, 2)))        # pitch circle, reference
ax2.plot([-TAP_D / 2, -TAP_D / 2, TAP_D / 2, TAP_D / 2], [R_BORE, R_HUB, R_HUB, R_BORE],
         color=INK, lw=0.5, ls=(0, (3, 1.5)))                               # set-screw hole behind: hidden
centreline(ax2, -14, 0, 14, 0)
cut_plane(ax2, (0.0, -R_FD - 2.0), (0.0, R_FD + 2.0), 4.0, (-1, 0), "A", [(-2.2, -26.5), (-2.2, 26.5)])
dim_dia(ax2, 0, 0, R_FD, 55, f"Ø{FD:g} flange (behind)", length=27)
dim_dia(ax2, 0, 0, R_PD, 27, f"Ø{PD:g} pitch *", length=27)
dim_dia(ax2, 0, 0, R_OD, 7, f"Ø{OD:g} outside *", length=27)
dim_dia(ax2, 0, 0, R_HUB, -15, f"Ø{HUB_D:g} hub (hidden)", length=27)
dim_dia(ax2, 0, 0, R_BORE, -38, f"Ø{BORE:g} bore *", length=27)
a = GROOVE_AT + 2 * math.pi * 2 / N_T                                       # the groove at 126 deg
leader(ax2, (R_OD * math.cos(a), R_OD * math.sin(a)), (-29.5, 20.5), f"{N_T} grooves at\npitch {T_PITCH:g} * (HTD 5M)", fontsize=7.5)
leader(ax2, (-TAP_D / 2, R_BORE + 2.5), (-29.5, -21.0), "set-screw hole (hidden)", fontsize=7.5)

# ---- (3) detail: one groove with the track tooth in it -------------------------------------------
X3, Y3 = (-9.5, 9.5), (-6.1, 4.9)
ax3 = view(0.52, 0.06, 0.45, X3, Y3, "DETAIL  -  one groove with the track tooth seated (enlarged)")
SH = (0.0, -R_OD)                                              # pulley centre: the 12 o'clock groove sits at the origin
win = box(X3[0] - SH[0], Y3[0] - SH[1], X3[1] - SH[0], Y3[1] - SH[1])
draw_shape(ax3, translate(pulley_section().intersection(win), *SH), FILL["pla"], hatch=True)
draw_shape(ax3, translate(track_on_pulley().intersection(win), *SH), FILL["tpu"])
ax3.add_patch(Arc(SH, 2 * R_PD, 2 * R_PD, theta1=50, theta2=130, color=DIM, lw=0.5, ls=(0, (8, 2, 1.5, 2))))  # pitch line
for ang in (90.0, 72.0):                                       # groove centre lines, this groove and its neighbour
    ar = math.radians(ang)
    centreline(ax3, SH[0] + (R_OD - 3.2) * math.cos(ar), SH[1] + (R_OD - 3.2) * math.sin(ar),
               SH[0] + (R_OD + 3.4) * math.cos(ar), SH[1] + (R_OD + 3.4) * math.sin(ar))
dim_arc(ax3, SH, R_PD + 1.8, 72, 90, f"{T_PITCH:g} pitch *\n(arc on the pitch line)", R_PD + 3.1)
# tooth height (track) and groove depth (stand-in), either side of the tooth
dim_v(ax3, -T_H, 0.0, 2.7, f"{T_H:g} tooth", ext_from=0.3, offset=0.3, fontsize=7.5)
dim_v(ax3, -GROOVE_D, 0.0, -2.7, f"{GROOVE_D:g} groove", ext_from=-0.3, offset=-0.3, fontsize=7.5)
dim_h(ax3, -T_W / 2, T_W / 2, -3.7, f"{T_W:g} root width", ext_from=-(T_H - T_R), offset=-0.62, fontsize=7.5)
leader(ax3, (T_R * math.cos(math.radians(-50)), -(T_H - T_R) + T_R * math.sin(math.radians(-50))), (3.2, -5.0),
       f"R{T_R:g} tooth tip (track)", fontsize=7.5)
leader(ax3, (-(T_R + CLEAR / 2) * math.cos(math.radians(20)), -(T_H - T_R) - (T_R + CLEAR / 2) * math.sin(math.radians(20))),
       (-9.3, -4.6), f"{CLEAR:g} clearance all round\n(stand-in only)", fontsize=7.5)
ar = math.radians(115)
leader(ax3, (SH[0] + R_PD * math.cos(ar), SH[1] + R_PD * math.sin(ar)), (-9.3, 2.7),
       f"pitch line Ø{PD:g} *, {PLD:g}\nabove the outside Ø{OD:g} *", fontsize=7.5)
ar = math.radians(62)
leader(ax3, (SH[0] + (R_OD + BACKING / 2) * math.cos(ar), SH[1] + (R_OD + BACKING / 2) * math.sin(ar)), (6.3, 1.7),
       f"backing {BACKING:g}\n(track)", fontsize=7.5)
ax3.text(0.0, Y3[0] + 0.15, "Pulley body hatched (PLA stand-in; the bought pulley's groove is the HTD 5M standard).   "
         "Track tooth dark, TPU.", fontsize=7, color=MUTED, ha="center", va="bottom")

# ---- notes -----------------------------------------------------------------------------------------
fig.text(0.03, 0.327, "Teeth beyond the A-A cut are shown unhatched.  * = order spec;  unmarked = printed stand-in.",
         fontsize=7.5, color=MUTED, va="top")
note_block(fig, [
    "TIMING PULLEY  (parts_spec.json: parts.pulley)",
    f"Buy.   Vendor: {VENDOR.split(' (')[0]}.   Qty: {QTY} ({QTY_SEG} per segment).",
    f"Order spec: HTD 5M, {N_T} teeth, for {BELT_W:g} mm belt, Ø{BORE:g} bore,",
    "flanges both sides, set-screw hub (screws come with it).",
    f"*  = ORDER SPEC, fixed by 20T HTD 5M: Ø{PD:g} pitch, Ø{OD:g} outside,",
    f"    {N_T} grooves at {T_PITCH:g} mm pitch, Ø{BORE:g} bore, {BELT_W:g} mm belt.",
    "Unmarked = the printed stand-in's sizes (flanges, face, hub,",
    f"    length, M{SCREW_M} screw); the vendor's drawing overrides them.",
    f"Stand-in: {STAND_IN}",
    f"PLA, fit tests only, never for driving.   Axle: Ø{AXLE_D:g} {AXLE_TOL} rod,",
    "0.5 mm deep flat filed under each set screw.",
], x=0.03, y=0.30, w=0.44)

save(fig, "part_pulley")
