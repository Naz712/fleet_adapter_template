#!/usr/bin/env python3
"""Part drawing: Track (TPU, printed) for the 1:5 ES1 stair-climber prototype.

Every number on the sheet comes from assembly/parts_spec.json (parts.track). The profile
outlines are rebuilt here from those numbers: round-topped HTD-style teeth inside, trapezoid
cleats outside, tip rounds and root fillets made with the same offset-in/offset-out steps that
generate_track.py uses, so the section looks like the printed part.

Run:  python3 part_track.py   ->  drawings/part_track.png
"""
import math
import sys

import numpy as np
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

sys.path.insert(0, "/home/user/fleet_adapter_template/3d_models/changi_es1_rescue_stairs/track_print/assembly")
from drawing import (DIM, FILL, INK, MUTED, SPEC, centreline, circle, dim_dia, dim_h, dim_v, leader,  # noqa: E402
                     note_block, outline, rect, save, sheet)

# --------------------------------------------------------------------------- numbers (parts_spec.json)
T = SPEC["parts"]["track"]
TE, CL, RING = T["teeth"], T["cleats"], T["as_printed_ring"]
P_T, H_T, W_T, R_T, N_T = TE["pitch_mm"], TE["height_mm"], TE["root_width_mm"], TE["tip_radius_mm"], TE["count"]
BACK = T["backing_thickness_mm"]
P_C, H_C, B_C, TIP_C, RND_C, FIL, N_C = (CL["pitch_mm"], CL["height_mm"], CL["base_width_mm"], CL["tip_width_mm"],
                                         CL["tip_round_mm"], CL["root_fillet_mm"], CL["count"])
TOTAL = T["total_thickness_mm"]
WIDTH, LOOP, MASS, QTY = T["width_mm"], T["loop_length_mm"], T["mass_g"], T["qty_total"]
ID_TIPS, PD, OD_BELT, OD_CLEATS, RING_H = (RING["inside_dia_over_tooth_tips_mm"], RING["pitch_dia_mm"],
                                            RING["outside_dia_of_belt_mm"], RING["outside_dia_over_cleats_mm"],
                                            RING["height_mm"])
# Derived (listed in the result notes): ring radii from the spec diameters, step numbers from the spec text
R_TIPS, R_BELT, R_CLEATS = ID_TIPS / 2, OD_BELT / 2, OD_CLEATS / 2
R_ROOT = R_BELT - BACK                      # 86.95: the tooth roots sit on this circle
STEP_RISE, STEP_GOING = 35.0, 50.0          # "ES1 steps are 35 x 50 mm at 1:5" (parts.track.why_these_cleats)
STEP_EDGE = 61.03                           # "their edges are 61.03 mm apart along the slope" (same field)
FIVE_CLEATS = round(5 * P_C, 2)             # 61.11, as the same field says
assert abs(H_T + BACK + H_C - TOTAL) < 1e-6
assert abs(2 * (R_ROOT - H_T) - ID_TIPS) < 0.05 and abs(2 * (R_BELT + H_C) - OD_CLEATS) < 0.05

SINK = 0.3  # teeth and cleats start this far inside the backing so the union is clean (as in generate_track.py)


# --------------------------------------------------------------------------- profile builders
def tooth_pts():
    """Round-topped tooth in its own frame: t along the belt, h in from the root line."""
    hc = H_T - R_T
    a0 = math.asin(hc / R_T)
    w0 = math.sqrt(R_T ** 2 - hc ** 2)
    arc = [(R_T * math.cos(a), hc + R_T * math.sin(a)) for a in np.linspace(-a0, math.pi + a0, 40)]
    return [(w0, -SINK)] + arc + [(-w0, -SINK)]


def cleat_pts():
    return [(-B_C / 2, -SINK), (B_C / 2, -SINK), (B_C / 2, 0.0), (TIP_C / 2, H_C), (-TIP_C / 2, H_C), (-B_C / 2, 0.0)]


def finish(shape):
    """Round the convex corners by RND_C (cleat tips), then fillet the concave ones by FIL (roots)."""
    shape = shape.buffer(-RND_C, quad_segs=12).buffer(RND_C, quad_segs=12)
    return shape.buffer(FIL, quad_segs=12).buffer(-FIL, quad_segs=12)


def straight_belt(x0, x1, tooth_xs, cleat_xs):
    """Belt running straight: root line at y=0, teeth down to -H_T, backing 0..BACK, cleats up to BACK+H_C."""
    parts = [box(x0 - 12, 0, x1 + 12, BACK)]
    parts += [Polygon([(xc + t, -h) for t, h in tooth_pts()]) for xc in tooth_xs]
    parts += [Polygon([(xc + t, BACK + h) for t, h in cleat_pts()]) for xc in cleat_xs]
    return finish(unary_union(parts)).intersection(box(x0, -20, x1, 20))


def on_circle(points, radius, phi, outward):
    u = np.array([math.cos(phi), math.sin(phi)])
    v = np.array([-math.sin(phi), math.cos(phi)])
    return [tuple((radius + outward * h) * u + t * v) for t, h in points]


def ring_profile():
    """The ring as printed: teeth on the inside of the root circle, cleats outside the belt circle."""
    annulus = Point(0, 0).buffer(R_BELT, quad_segs=120).difference(Point(0, 0).buffer(R_ROOT, quad_segs=120))
    parts = [annulus]
    parts += [Polygon(on_circle(tooth_pts(), R_ROOT, 2 * math.pi * k / N_T, -1)) for k in range(N_T)]
    parts += [Polygon(on_circle(cleat_pts(), R_BELT, 2 * math.pi * k / N_C, +1)) for k in range(N_C)]
    return finish(unary_union(parts))


def draw_shape(ax, shape, fill, hatch=False, lw=0.6, flip_y=None):
    """Draw a shapely (multi)polygon with the outline() helper. flip_y=c mirrors y about y=c."""
    polys = list(shape.geoms) if hasattr(shape, "geoms") else [shape]
    f = (lambda x, y: (x, 2 * flip_y - y)) if flip_y is not None else (lambda x, y: (x, y))
    for p in polys:
        outline(ax, [f(x, y) for x, y in p.exterior.coords], fill, lw=lw, hatch=hatch)
        for hole in p.interiors:
            outline(ax, [f(x, y) for x, y in hole.coords], "white", lw=lw)


# --------------------------------------------------------------------------- sheet
FIG_W, FIG_H = 11.0, 7.5
fig, add_view = sheet("TRACK  -  TPU, 3D printed",
                      "ES1 stair-climbing rescue carrier, 1:5 prototype, track segment.   Part: Track, file stl/track_TPU_x4.stl.   "
                      "Dimensions in mm at model size.   Sheet 1 of 1.",
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


# ---- (1) front view: the ring as printed ---------------------------------------------------
ax1 = view(0.03, 0.465, 0.44, (-180, 180), (-100, 100), "FRONT VIEW  -  ring as printed, seen along its axis")
draw_shape(ax1, ring_profile(), FILL["tpu"])
circle(ax1, 0, 0, PD / 2, fill="none", lw=0.5, ls=(0, (8, 2, 1.5, 2)))  # pitch line, reference
centreline(ax1, -14, 0, 14, 0)
centreline(ax1, 0, -14, 0, 14)
dim_dia(ax1, 0, 0, R_CLEATS, 42, f"Ø{OD_CLEATS:g} over cleats", length=97)
dim_dia(ax1, 0, 0, R_BELT, 12, f"Ø{OD_BELT:g} belt outside", length=97)
dim_dia(ax1, 0, 0, R_TIPS, -30, f"Ø{ID_TIPS:g} over tooth tips", length=97)
dim_dia(ax1, 0, 0, PD / 2, 215, f"Ø{PD:g} pitch line (ref)", length=97)
a = math.radians(128)
leader(ax1, (R_CLEATS * math.cos(a), R_CLEATS * math.sin(a)), (-178, 84), f"{N_C} cleats outside, pitch {P_C:g}")
a = math.radians(160)
leader(ax1, (R_TIPS * math.cos(a), R_TIPS * math.sin(a)), (-178, 54), f"{N_T} teeth inside, HTD 5M, pitch {P_T:g}")

# ---- side view: the ring standing on the bed, with the cutting plane A-A ---------------------
ax1b = view(0.03, 0.37, 0.44, (-180, 180), (-6, 28), "SIDE VIEW  -  standing on the print bed")
rect(ax1b, -R_CLEATS, 0, OD_CLEATS, RING_H, FILL["tpu"], lw=0.6)
ax1b.plot([-R_CLEATS, R_CLEATS], [RING_H - H_C, RING_H - H_C], color="white", lw=0.4, alpha=0.5)  # cleat-root edge, faint
dim_v(ax1b, 0, RING_H, R_CLEATS + 7, f"{RING_H:g}", ext_from=R_CLEATS)
# cutting plane A-A at mid height: chain line across the part, thick stubs clear of the dimension,
# arrows show the viewing direction (along the ring's axis)
ax1b.plot([-R_CLEATS, R_CLEATS], [RING_H / 2, RING_H / 2], color="white", lw=0.5, dashes=(8, 2, 1.5, 2))
for sx in (-1, 1):
    x_in, x_out = sx * (R_CLEATS + 15), sx * (R_CLEATS + 33)
    ax1b.plot([x_in, x_out], [RING_H / 2, RING_H / 2], color=INK, lw=1.6)
    ax1b.annotate("", xy=(x_out, RING_H / 2 + 13), xytext=(x_out, RING_H / 2),
                  arrowprops=dict(arrowstyle="-|>", lw=0.8, color=INK, mutation_scale=9))
    ax1b.text(x_out + sx * 6, RING_H / 2 + 4, "A", fontsize=10, fontweight="bold", color=INK,
              ha="center", va="center")

# ---- (2) section A-A, enlarged, belt straight ------------------------------------------------
X0, X1 = -4.0, 28.0
tooth_xs = [0, 5, 10, 15, 20, 25]           # tooth pitch 5
cleat_xs = [0, P_C, 2 * P_C]                 # cleat pitch 12.222; cleat 0 and tooth 0 line up, as at angle 0 on the ring
ax2 = view(0.50, 0.505, 0.47, (-12.0, 40.5), (-10.2, 12.4),
           "SECTION A-A  -  enlarged; belt drawn straight, as it runs between the pulleys")
belt = straight_belt(X0, X1, tooth_xs, cleat_xs)
draw_shape(ax2, belt, FILL["light"], hatch=True)
for yy in (0.0, BACK):  # root line and backing outer face, to read the three layers
    ax2.plot([X0, X1], [yy, yy], color=DIM, lw=0.4, dashes=(6, 3))
ax2.text(X0, -10.1, "Cleats face outwards (onto the stairs); teeth face inwards (onto the pulleys).",
         fontsize=7.5, color=MUTED, ha="left", va="bottom")
# vertical: total thickness (left); cleat, tooth and backing heights (right)
dim_v(ax2, -H_T, BACK + H_C, -8.0, f"{TOTAL:g}", ext_from=X0)
dim_v(ax2, BACK, BACK + H_C, X1 + 5.5, f"{H_C:.1f}", ext_from=X1 + 0.3, offset=1.5)
dim_v(ax2, -H_T, 0, X1 + 5.5, f"{H_T:.1f}", ext_from=X1 + 0.3, offset=1.5)
dim_v(ax2, 0, BACK, X1 + 9.5, f"{BACK:g}", ext_from=X1 + 0.3, offset=1.5)
# teeth, below
dim_h(ax2, 5, 10, -4.6, f"{P_T:g}", ext_from=-H_T)
dim_h(ax2, 20 - W_T / 2, 20 + W_T / 2, -4.6, f"{W_T:g}", ext_from=-(H_T - R_T), offset=-1.45)
leader(ax2, (15 + R_T * math.cos(math.radians(-50)), -(H_T - R_T) - R_T * math.sin(math.radians(50))),
       (10.5, -7.4), f"R{R_T:g} tooth tip")
# cleats, above
dim_h(ax2, -TIP_C / 2, TIP_C / 2, BACK + H_C + 1.9, f"{TIP_C:g}", ext_from=BACK + H_C)
dim_h(ax2, -B_C / 2, B_C / 2, BACK + H_C + 4.6, f"{B_C:g}", ext_from=BACK)
dim_h(ax2, P_C, 2 * P_C, BACK + H_C + 1.9, f"{P_C:g}", ext_from=BACK + H_C)
leader(ax2, (2 * P_C + TIP_C / 2 - 0.15, BACK + H_C - 0.15), (2 * P_C + 2.6, BACK + H_C + 4.2), f"R{RND_C:g} tip round")
leader(ax2, (P_C - B_C / 2 - 0.25, BACK + 0.18), (4.6, BACK + H_C + 5.0), f"R{FIL:g} root fillet, cleats and teeth")

# ---- (3) detail: five cleats on one step -----------------------------------------------------
ax3 = view(0.52, 0.06, 0.42, (-12, 94), (-40.5, 18.5),
           "DETAIL  -  why the cleat pitch is 12.222: five cleats to one step")
# The belt lying on the stairs, cleats down: built cleats-up, then mirrored about the backing's outer face.
# After the mirror: cleat tips at y=0, backing outer face at y=H_C, tooth tips at y=TOTAL.
det = straight_belt(-9, 83, [5 * k for k in range(-1, 17)], [P_C * k for k in range(7)])
draw_shape(ax3, det, FILL["light"], hatch=True, flip_y=(BACK + H_C) / 2)
# two ES1 step edges 61.03 apart; the flight is turned so the line through the step edges is level
ang = math.atan2(STEP_RISE, STEP_GOING)
tread = np.array([math.cos(ang), -math.sin(ang)])      # along the tread
riser = np.array([math.sin(ang), math.cos(ang)])       # up the riser
n0 = np.array([P_C / 2, H_C])                           # first step edge: in the gap between cleats 0 and 1, on the belt face
n1 = n0 + np.array([STEP_EDGE, 0])
foot = n0 + STEP_GOING * tread
lo = -33.0
stairs = [tuple(n0 - 22 * riser), tuple(n0), tuple(foot), tuple(n1), tuple(n1 + 17 * tread),
          (float((n1 + 17 * tread)[0]), lo), (float((n0 - 22 * riser)[0]), lo)]
outline(ax3, stairs, FILL["pla"], lw=0.6, alpha=0.45)
ax3.text(36.5, -29.3, f"ES1 step at 1:5, {STEP_RISE:g} rise x {STEP_GOING:g} going,\nturned so the step edges are level",
         fontsize=7.5, color=INK, ha="center", va="center", linespacing=1.3)
for xc in (0, 5 * P_C):
    centreline(ax3, xc, -2.0, xc, TOTAL + 4.0)
dim_h(ax3, 0, 5 * P_C, TOTAL + 3.5, f"5 x {P_C:g} = {FIVE_CLEATS:g}  (cleat 0 to cleat 5)", fontsize=7.5)
dim_h(ax3, 3 * P_C, 4 * P_C, -9.0, f"{P_C:g}", ext_from=0)
dim_h(ax3, float(n0[0]), float(n1[0]), lo - 4.5, f"{STEP_EDGE:g}  step edge to step edge", ext_from=H_C, fontsize=7.5)
leader(ax3, (float(n1[0]) + 0.3, H_C - 0.3), (38.0, 15.8),
       "step edge in the gap between two cleats", fontsize=7.5)

# ---- notes -------------------------------------------------------------------------------------
note_block(fig, [
    "TRACK  (parts_spec.json: parts.track)",
    "Material: TPU 95A.   Make (3D print).   Qty: 4 (2 per segment).",
    "Printed upright as a ring, 0.2 mm layers, 100% infill, no supports.",
    f"Mass: {MASS:g} g each.   Width {WIDTH:g} mm.",
    f"Loop {LOOP:g} mm = {N_T} teeth x {P_T:g} mm (HTD 5M, inside).",
    f"{N_C} cleats outside at {P_C:g} mm; five cleats = one ES1 step at 1:5.",
    f"Teeth {H_T:g} high, backing {BACK:g}, cleats {H_C:g}: {TOTAL:g} mm thick in all.",
    "Runs on bought HTD 5M 20-tooth pulleys for 15 mm belts, 8 mm bore.",
    "Unmarked radii: cleat tips R0.5, all roots R0.35.",
], x=0.03, y=0.30)

save(fig, "part_track")
