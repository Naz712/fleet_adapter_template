#!/usr/bin/env python3
"""Drive and motion sheet: how the parts of the two track segments turn, and how they link to
the two motors and the box. A diagram at the spec's proportions, not a dimensioned part drawing.

Numbers come from ../parts_spec.json (1:5, mm). What the spec does not give (box length and
height, hinge gear radii, sprocket and motor sizes, laser position) is marked DERIVED below and
listed in the sheet's note block.
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, PathPatch, Polygon, Rectangle  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402

from drawing import DIM, FILL, INK, MUTED, RED, SPEC, circle, save, sheet  # noqa: E402

# ----------------------------------------------------------------------------- from the spec
P = SPEC["parts"]
L = SPEC["segment"]["axle_to_axle_mm"]  # 225
R_FACE = SPEC["segment"]["axle_to_track_face_mm"]  # 16.74
R_TIP = SPEC["segment"]["axle_to_cleat_tip_mm"]  # 19.74
CLEAT = P["track"]["cleats"]
R_IN = R_FACE - (P["track"]["total_thickness_mm"] - CLEAT["height_mm"])  # 13.34: tooth tips = rail top face
R_PULLEY = P["pulley"]["outside_dia_mm"] / 2  # 15.35
R_FLANGE = P["pulley"]["flange_dia_mm"] / 2  # 17.85
R_HUB = P["pulley"]["hub_dia_mm"] / 2  # 9
R_AXLE = P["axle"]["dia_mm"] / 2  # 4
R_BRG = P["bearing"]["outside_dia_mm"] / 2  # 11
PL = P["side_plate"]["plate"]
PLATE_BOT, PLATE_TOP, PLATE_R = -PL["bottom_edge_below_axle_mm"], PL["top_edge_above_axle_mm"], 20.0
RAIL = P["side_plate"]["rail"]
RAIL_BOT = -RAIL["top_face_below_axle_mm"] - RAIL["thickness_mm"]
BAR_X, BAR_Y = P["side_plate"]["cross_bar_holes"]["at_x_mm"], P["side_plate"]["cross_bar_holes"]["above_axle_mm"]
BOX_BAR_X = [-60, -200]  # rear_plate_extra: from the middle axle, towards the rear
SECTOR_BOLT_R = P["side_plate"]["sector_bolts"]["radius_mm"]  # 17
AXLE_HALF = P["axle"]["lengths_mm"]["middle"] / 2  # 110
# z stations, one side (layout_decision.z_stations_one_side_mm)
_zs = SPEC["layout_decision"]["z_stations_one_side_mm"]
Z = dict(box=_zs["box"][1], fplate=tuple(_zs["front_plate"]), flane=tuple(_zs["front_lane"]), fhub=tuple(_zs["front_hub"]),
         rlane=tuple(_zs["rear_lane"]), rhub=tuple(_zs["rear_hub"]), rplate=tuple(_zs["rear_plate"]))
SWING_UP, SWING_DOWN = 35, 37  # deg, the team's hinge range

# ----------------------------------------------------------------------------- DERIVED (not in the spec)
BOX_X0, BOX_X1 = -210.0, 24.0  # spans the two box cross bars (-60, -200) and the sprocket at the middle axle; +24 = full-size 120 / 5
BOX_Y0, BOX_Y1 = -10.0, 60.0  # must enclose the axle sprocket and the cross shaft with its 608s (45 + 11)
R_PINION, R_SECTOR = 10.0, 35.0  # pitch radii, the team's values; centre distance 45
MODULE = 1.25  # printable teeth: pinion 16 T, sector 56 T if it were a full circle
PINION_C = (0.0, R_PINION + R_SECTOR)  # cross shaft straight above the middle axle
R_SPROCKET, R_MOTOR_SPROCKET = 12.0, 6.0  # chain sprockets, indicative
DRIVE_MOTOR_C, R_DRIVE_MOTOR = (-95.0, 14.0), 18.5  # Pololu 37D: 37 mm dia, seen end-on
HINGE_MOTOR = (-92.0, 36.0, 80.0, 18.0)  # x, y, w, h of the worm gearmotor body, lying along x
LASER_X = L + 9  # 45 mm beyond the end axle at full size, / 5
SWING_DRAWN = 150.0  # the swung positions are drawn this far from the hinge, then broken

FS = 7.2  # label font size on the sheet


# ----------------------------------------------------------------------------- geometry helpers
def stadium(x0, x1, yc, r, n=40):
    """Closed counter-clockwise outline of a bar from x0 to x1 with semicircular ends of radius r, centred on y = yc."""
    a1 = np.linspace(-math.pi / 2, math.pi / 2, n)
    a2 = np.linspace(math.pi / 2, 3 * math.pi / 2, n)
    right = np.c_[x1 + r * np.cos(a1), yc + r * np.sin(a1)]
    left = np.c_[x0 + r * np.cos(a2), yc + r * np.sin(a2)]
    return np.vstack([right, left])


def rot(pts, deg):
    a = math.radians(deg)
    m = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    return np.asarray(pts, float) @ m.T


def gear(cx, cy, n, module, a0=0.0, a1=360.0, phase=0.0):
    """Outline of a spur gear (or a sector of one, a0..a1 deg) with simple trapezoid teeth."""
    rp = n * module / 2
    rt, rr = rp + module, rp - 1.25 * module
    p = 360.0 / n
    pts = []
    k0, k1 = math.floor((a0 - phase) / p), math.ceil((a1 - phase) / p)
    for k in range(k0, k1 + 1):
        a = phase + k * p
        for da, r in ((0.0, rr), (0.3 * p, rr), (0.4 * p, rt), (0.6 * p, rt), (0.7 * p, rr), (p, rr)):
            if a0 <= a + da <= a1:
                pts.append((cx + r * math.cos(math.radians(a + da)), cy + r * math.sin(math.radians(a + da))))
    return np.array(pts), rt, rr


def cleats_along(outline, n, h, base, tip):
    """n small trapezoid cleats standing on a closed counter-clockwise outline, evenly spaced along it."""
    pts = np.vstack([outline, outline[:1]])
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    s = np.r_[0, np.cumsum(seg)]
    out = []
    for i in range(n):
        d = s[-1] * i / n
        j = min(np.searchsorted(s, d, side="right") - 1, len(seg) - 1)
        t = (d - s[j]) / seg[j]
        p = pts[j] + t * (pts[j + 1] - pts[j])
        e = (pts[j + 1] - pts[j]) / seg[j]
        nrm = np.array([e[1], -e[0]])  # outward
        out.append(np.array([p - e * base / 2, p + e * base / 2, p + e * tip / 2 + nrm * h, p - e * tip / 2 + nrm * h]))
    return out


def ring_patch(ax, outer, inner, fc, lw=0.6, zorder=3):
    """A filled band between two closed outlines."""
    verts = np.vstack([outer, outer[:1], inner[::-1], inner[-1:]])
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(outer) - 1) + [MPath.CLOSEPOLY]
    codes += [MPath.MOVETO] + [MPath.LINETO] * (len(inner) - 1) + [MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(verts, codes), fc=fc, ec=INK, lw=lw, zorder=zorder))


def arc_arrow(ax, c, r, a0, a1, color=RED, lw=1.1, heads="end", zorder=9):
    """A curved arrow about c from a0 to a1 (deg, drawn in that direction), arrowhead at the end (or both)."""
    a = np.radians(np.linspace(a0, a1, 40))
    xs, ys = c[0] + r * np.cos(a), c[1] + r * np.sin(a)
    ax.plot(xs, ys, color=color, lw=lw, zorder=zorder, solid_capstyle="round")
    for h in (("end", "start") if heads == "both" else (heads,)):
        p0, p1 = ((xs[-2], ys[-2]), (xs[-1], ys[-1])) if h == "end" else ((xs[1], ys[1]), (xs[0], ys[0]))
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=9, color=color, lw=lw, zorder=zorder, shrinkA=0, shrinkB=0))


def straight_arrow(ax, p0, p1, color=RED, lw=1.1, zorder=9):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=9, color=color, lw=lw, zorder=zorder, shrinkA=0, shrinkB=0))


def note(ax, xy, xytext, text, ha="left", va="top", relpos=(0.5, 0.5), color=INK, arrow=True, fontsize=FS):
    """Label with a leader. relpos picks where on the text box the leader starts ((0,0) bottom left .. (1,1) top right)."""
    kw = dict(fontsize=fontsize, color=color, ha=ha, va=va, linespacing=1.25, zorder=12,
              bbox=dict(fc="white", ec="none", pad=1.0, alpha=0.92))
    if arrow:
        kw["arrowprops"] = dict(arrowstyle="-|>", lw=0.6, color=RED if color == RED else DIM, mutation_scale=7, shrinkA=0, shrinkB=1, relpos=relpos)
    ax.annotate(text, xy=xy, xytext=xytext, **kw)


# ----------------------------------------------------------------------------- view 1: side view at the middle axle
def draw_segment(ax, x0, x1, angle=0.0, swung=False, front=False):
    """One segment (plate, rail, cross bars, track, pulleys, axles) about the middle axle at (0, 0);
    the segment's axles are at x0 and x1 (x1 = middle axle for the rear, x0 = middle axle for the front)."""
    T = lambda pts: rot(pts, angle)
    if swung:  # only the cleat-tip envelope, SWING_DRAWN long, then a break
        s0, s1, w = 22.0, SWING_DRAWN, R_TIP
        for sgn in (1, -1):
            ax.plot(*T([(s0, sgn * w), (s1, sgn * w)]).T, color=MUTED, lw=0.8, ls=(0, (4, 2.5)), zorder=2)
        zig = T([(s1, w), (s1 + 5, w * 0.5), (s1 - 5, 0), (s1 + 5, -w * 0.5), (s1, -w)])
        ax.plot(zig[:, 0], zig[:, 1], color=MUTED, lw=0.8, zorder=2)
        return
    track_face = stadium(x0, x1, 0, R_FACE, 60)
    # plate: 40 tall stadium with R20 ends; bottom edge 12 below the axle, top 28 above -> arcs centred 8 above
    yc = (PLATE_BOT + PLATE_TOP) / 2
    ax.add_patch(Polygon(T(stadium(x0, x1, yc, PLATE_R)), closed=True, fc=FILL["petg"], ec=INK, lw=0.8, alpha=0.32, zorder=4))
    # rail + web under the lower run, from 20 to 205 along the segment
    rx0, rx1 = x0 + RAIL["from_x_mm"], x0 + RAIL["to_x_mm"]
    ax.add_patch(Polygon(T([(rx0, PLATE_BOT), (rx1, PLATE_BOT), (rx1, RAIL_BOT), (rx0, RAIL_BOT)]), closed=True,
                         fc=FILL["petg"], ec=INK, lw=0.6, alpha=0.55, zorder=4))
    # track: band from the tooth tips (13.34) to the face (16.74), cleats outside
    ring_patch(ax, T(track_face), T(stadium(x0, x1, 0, R_IN, 60)), FILL["tpu"], zorder=3)
    for c in cleats_along(track_face, CLEAT["count"], CLEAT["height_mm"], CLEAT["base_width_mm"], CLEAT["tip_width_mm"]):
        ax.add_patch(Polygon(T(c), closed=True, fc=FILL["tpu"], ec="none", zorder=3))
    # cross bars (M4 rod + spacer) and, on the rear segment, the two box cross bars
    for bx in BAR_X:
        p = T([(x0 + bx, BAR_Y)])[0]
        circle(ax, p[0], p[1], 2.0, fill=FILL["steel"], lw=0.5).set_zorder(5)
    if not front:
        for bx in BOX_BAR_X:
            circle(ax, bx, BAR_Y, 2.0, fill=INK, lw=0.5).set_zorder(8)
    # pulleys and axles
    for cx in (x0, x1):
        p = T([(cx, 0.0)])[0]
        circle(ax, p[0], p[1], R_IN, fill=FILL["light"], lw=0.5).set_zorder(2)
        circle(ax, p[0], p[1], R_FLANGE, fill="none", lw=0.5).set_zorder(5)
        circle(ax, p[0], p[1], R_HUB, fill=FILL["bearing"], lw=0.5).set_zorder(5)
        circle(ax, p[0], p[1], R_AXLE, fill=FILL["steel"], lw=0.6).set_zorder(6)


def side_view(ax):
    draw_segment(ax, -L, 0.0)  # rear, to the left
    draw_segment(ax, 0.0, L, front=True)  # front, straight
    draw_segment(ax, 0.0, L, angle=SWING_UP, swung=True, front=True)
    draw_segment(ax, 0.0, L, angle=-SWING_DOWN, swung=True, front=True)

    # box (inboard of everything: drawn see-through) with its two motors
    ax.add_patch(Rectangle((BOX_X0, BOX_Y0), BOX_X1 - BOX_X0, BOX_Y1 - BOX_Y0, fc=FILL["light"], ec=INK, lw=0.9, alpha=0.62, zorder=6))
    mx, my = DRIVE_MOTOR_C
    circle(ax, mx, my, R_DRIVE_MOTOR, fill="#f4f5f6", lw=0.8).set_zorder(7)
    circle(ax, mx, my, R_MOTOR_SPROCKET, fill=FILL["bearing"], lw=0.6).set_zorder(7)
    ax.text(mx, my + 7.5, "37D", fontsize=6.5, ha="center", va="bottom", color=INK, zorder=8)
    # chain: the two outer tangents between the motor sprocket and the axle sprocket
    d = math.hypot(mx, my)
    base = math.atan2(my, mx)  # direction axle -> motor
    off = math.acos((R_SPROCKET - R_MOTOR_SPROCKET) / d)
    for sgn in (1, -1):
        a = base + sgn * off
        ax.plot([R_SPROCKET * math.cos(a), mx + R_MOTOR_SPROCKET * math.cos(a)],
                [R_SPROCKET * math.sin(a), my + R_MOTOR_SPROCKET * math.sin(a)], color=INK, lw=1.0, zorder=7, dashes=(3, 1.5))
    spk, _, _ = gear(0, 0, 15, 1.6)  # drive sprocket on the middle axle, 24 mm across
    ax.add_patch(Polygon(spk, closed=True, fc=FILL["bearing"], ec=INK, lw=0.6, zorder=7))
    hx, hy, hw, hh = HINGE_MOTOR
    ax.add_patch(Rectangle((hx, hy), hw, hh, fc="#f4f5f6", ec=INK, lw=0.8, zorder=7))
    ax.add_patch(Rectangle((hx + hw, hy + 4), 6, hh - 8, fc=FILL["steel"], ec=INK, lw=0.6, zorder=7))  # worm on the motor shaft
    ax.text(hx + hw / 2, hy + hh / 2, "worm gearmotor", fontsize=6.5, ha="center", va="center", color=INK, zorder=8)
    # cross shaft (608 in the box walls) with the worm wheel inside the box and the pinion outside it, at z 41-48
    px, py = PINION_C
    circle(ax, px, py, R_BRG, fill="none", lw=0.5, ls=(0, (2, 1.5))).set_zorder(7)
    pin, rt_p, _ = gear(px, py, 16, MODULE, phase=270 - 0.5 * 360 / 16)
    ax.add_patch(Polygon(pin, closed=True, fc=FILL["pla"], ec=INK, lw=0.6, zorder=8, alpha=0.9))
    circle(ax, px, py, R_AXLE, fill=FILL["steel"], lw=0.6).set_zorder(9)
    # sector gear on the rear end of each front plate: R35 pitch, toothed over the swing plus a tooth each end
    a0, a1 = 90 - SWING_UP - 5, 90 + SWING_DOWN + 5
    sec, rt_s, _ = gear(0, 0, 56, MODULE, a0=a0, a1=a1, phase=90 - 0.5 * 360 / 56)
    hub_a = np.radians(np.linspace(a1, a0, 30))
    hub = np.c_[17 * np.cos(hub_a), 17 * np.sin(hub_a)]
    ax.add_patch(Polygon(np.vstack([sec, hub]), closed=True, fc=FILL["pla"], ec=INK, lw=0.6, zorder=8, alpha=0.9))
    for k in range(3):
        a = math.radians(90 + 120 * k)
        circle(ax, SECTOR_BOLT_R * math.cos(a), SECTOR_BOLT_R * math.sin(a), 1.6, fill="white", lw=0.5).set_zorder(9)
    circle(ax, 0, 0, R_BRG, fill="none", lw=0.5, ls=(0, (2, 1.5))).set_zorder(9)  # the plates' 608s
    circle(ax, 0, 0, R_AXLE, fill=FILL["steel"], lw=0.6).set_zorder(9)

    # lasers at each end, looking down
    for sx in (-1, 1):
        lx = sx * LASER_X
        ax.add_patch(Rectangle((lx - 4, PLATE_TOP - 6), 8, 6, fc=INK, ec="none", zorder=6))
        ax.plot([lx, lx], [PLATE_TOP - 6, -34], color=MUTED, lw=0.6, ls=(0, (2, 2)), zorder=5)
        straight_arrow(ax, (lx, -34), (lx, -42), color=MUTED, lw=0.6)

    # ---- motion arrows (red)
    for cx in (-L, 0, L):
        arc_arrow(ax, (cx, 0), 25, 330, 215)  # axles: clockwise in this view = forward
    for xa, xb in ((-205, -160), (128, 173)):  # tracks: upper run forward, lower run back
        straight_arrow(ax, (xa, 30), (xb, 30))
        straight_arrow(ax, (xb, -30), (xa, -30))
    arc_arrow(ax, PINION_C, 14.5, 155, 25)  # pinion clockwise -> front swings up
    R_ARC = 165
    arc_arrow(ax, (0, 0), R_ARC, -SWING_DOWN, SWING_UP, heads="both", lw=1.2)  # front segment swing
    for ang, txt in ((SWING_UP, f"+{SWING_UP}°"), (-SWING_DOWN, f"−{SWING_DOWN}°")):
        ax.text((R_ARC + 14) * math.cos(math.radians(ang)), (R_ARC + 14) * math.sin(math.radians(ang)), txt,
                fontsize=FS, color=RED, ha="left", va="center", zorder=12, fontweight="bold")

    # ---- labels. Left column
    note(ax, (-170, BOX_Y1), (-262, 110), "BOX, drawn see-through: sits between\nthe rear plates, bolted to them by two\nM4 cross bars (x −60 and −200)")
    note(ax, (mx - 2, my + R_DRIVE_MOTOR), (-262, 78), "DRIVE MOTOR: 37D gearmotor in the box;\nchain (or belt) to the sprocket on the axle", relpos=(1, 0.5))
    note(ax, (-LASER_X, PLATE_TOP - 2), (-262, 50), "laser,\nlooks down")
    # top centre and right
    note(ax, (hx + 40, hy + hh), (-100, 104), "HINGE MOTOR: worm gearmotor, 7 N m, 7 rpm,\nin the box. Self-locking: holds the\nhinge angle with the power off")
    note(ax, (px - 5, py + 9), (170, 118), "PINION r ≈ 10 on the cross\nshaft (z 41–48): 2 × 608 in\nthe box walls; pot on its end", relpos=(0, 1))
    note(ax, (rt_s * math.cos(math.radians(55)), rt_s * math.sin(math.radians(55))), (170, 84),
         "SECTOR R ≈ 35 on the rear end\nof each front plate (3 × M3\non r 14): turns with the front", relpos=(0, 0.5))
    ax.text(172, 50, "front segment swings about\nthe middle axle: +35° up,\n−37° down; worm holds it", fontsize=FS, color=RED, ha="left", va="top",
            linespacing=1.25, zorder=12, bbox=dict(fc="white", ec="none", pad=1.0, alpha=0.92))
    # below the segments
    note(ax, (-L, -26), (-262, -46), "end axles idle:\nturn with the track\nin the plates' 608s")
    note(ax, (-150, RAIL_BOT), (-172, -46), f"rear plate (outboard, z {Z['rplate'][0]}–{Z['rplate'][1]})")
    note(ax, (-R_SPROCKET * 0.7, -R_SPROCKET * 0.72), (-172, -60), "SPROCKET on the middle axle\n(z 0, set screw), chain from the 37D", relpos=(1, 1))
    note(ax, (-1, -26), (-250, -82), color=RED, relpos=(1, 0.5), text=(
        "MIDDLE AXLE = HINGE, 8 mm rod: turns clockwise in this view\n"
        "= forward. Both plates turn on it (608s); its 4 pulleys and\n"
        "the sprocket are set-screwed, so it drives both tracks at once"))
    note(ax, (200, RAIL_BOT), (130, -46), "front plate (inboard, z 41–48)")
    ax.text(130, -60, "tracks: upper run forward,\nlower run back (vehicle moves →)", fontsize=FS, color=RED, ha="left", va="top",
            linespacing=1.25, zorder=12, bbox=dict(fc="white", ec="none", pad=1.0, alpha=0.92))
    ax.set_xlim(-266, 300)
    ax.set_ylim(-126, 124)


# ----------------------------------------------------------------------------- view 2: shaft-line schematic (x-z)
KEY = [
    ("A", "sprocket, z −3…3: fixed to the axle (set screw)"),
    ("B", "front plate + its 608, z 41–48: turns on the axle"),
    ("C", f"front pulley, z {Z['flane'][0]}–{Z['fhub'][1]}: fixed (set screw on a flat)"),
    ("D", f"rear pulley, z {Z['rlane'][0]}–{Z['rhub'][1]}: fixed (set screw on a flat)"),
    ("E", f"rear plate + its 608, z {Z['rplate'][0]}–{Z['rplate'][1]}: turns on the axle"),
    ("F", "worm wheel: fixed to the cross shaft; the hinge"),
    ("", "motor's worm turns it"),
    ("G", "cross shaft 608s in the box walls, z 33–40"),
    ("H", "pinion, z 41–48: fixed to the cross shaft; meshes"),
    ("", "with the sector on B"),
    ("J", "potentiometer on the shaft end (shown here): turns"),
    ("", "3.5 × the hinge angle"),
    ("K", "drive motor 37D (37 dia × 60–90 long) and its chain"),
    ("", "sprocket. With its shaft across (z) it is longer"),
    ("", "than the 80 between the box walls: see note 4"),
]


def shaft_view(ax):
    """Top schematic of the middle axle (z across). The hinge cross shaft is really 45 mm above the axle;
    it is drawn behind it here, and the drive motor in front, so all three shaft lines show."""
    FIXED, TURNS = "#4a4a4a", "white"
    V_AXLE, V_SHAFT, V_MOTOR = 0.0, -75.0, 72.0

    def block(z0, z1, v, h, fc, zorder=5, lw=0.6):
        ax.add_patch(Rectangle((z0, v - h / 2), z1 - z0, h, fc=fc, ec=INK, lw=lw, zorder=zorder))

    def letter(z, v, s):
        ax.add_patch(Circle((z, v), 5.5, fc="white", ec=INK, lw=0.7, zorder=11))
        ax.text(z, v - 0.3, s, fontsize=6.8, ha="center", va="center", color=INK, zorder=12, fontweight="bold")

    # the box: floor and the two walls at z = ±40
    ax.add_patch(Rectangle((-Z["box"], V_SHAFT - 38), 2 * Z["box"], V_MOTOR + 22 - (V_SHAFT - 38), fc=FILL["light"], ec="none", alpha=0.6, zorder=2))
    for sgn in (1, -1):
        ax.plot([sgn * Z["box"]] * 2, [V_SHAFT - 38, V_MOTOR + 22], color=INK, lw=0.9, zorder=3)
    ax.text(Z["box"] + 1.5, V_MOTOR + 21, "box wall, z = ±40", fontsize=6.8, ha="left", va="bottom", color=MUTED, zorder=12)
    ax.plot([0, 0], [V_SHAFT - 45, V_MOTOR + 28], color=DIM, lw=0.5, dashes=(8, 2, 1.5, 2), zorder=1)
    ax.text(0, V_SHAFT - 47, "z = 0, the vehicle's centre line. The left side mirrors the right.", fontsize=6.8, ha="center", va="top", color=MUTED)

    # middle axle with its plates, bearings, pulleys and sprocket (one side; mirrored)
    block(-AXLE_HALF, AXLE_HALF, V_AXLE, 2 * R_AXLE, FILL["steel"], zorder=5)
    block(-3, 3, V_AXLE, 2 * R_SPROCKET, FIXED, zorder=6)
    for sgn in (1, -1):
        s = lambda a, b: (min(sgn * a, sgn * b), max(sgn * a, sgn * b))
        block(*s(*Z["fplate"]), V_AXLE - 9, 54, FILL["petg"], zorder=4)  # front plate stub (runs along x)
        block(*s(*Z["fplate"]), V_AXLE - 50, 28, FILL["pla"], zorder=4)  # its sector, reaching back to the pinion
        block(*s(*Z["rplate"]), V_AXLE, 36, FILL["petg"], zorder=4)
        block(*s(*Z["fplate"]), V_AXLE, 2 * R_BRG, TURNS, zorder=6)
        block(*s(*Z["rplate"]), V_AXLE, 2 * R_BRG, TURNS, zorder=6)
        for lane, hub in (("flane", "fhub"), ("rlane", "rhub")):
            z0, z1 = s(*Z[lane])
            block(z0, z1, V_AXLE, 2 * R_FLANGE, FIXED, zorder=6)
            block(z0 + 1.5, z1 - 1.5, V_AXLE, 2 * R_PULLEY, FIXED, zorder=7)
            block(*s(*Z[hub]), V_AXLE, 2 * R_HUB, FIXED, zorder=6)
    ax.text(-AXLE_HALF - 2, V_AXLE + 21, f"middle axle, 8 mm × {AXLE_HALF * 2:g}", fontsize=6.8, ha="left", va="bottom", color=INK, zorder=12)
    letter(0, -24, "A")
    letter(44.5, 27, "B")
    letter(61.5, -27, "C")
    letter(87.5, 27, "D")
    letter(104.5, -27, "E")

    # hinge cross shaft: worm wheel inside the box, 608s in the walls, pinions outside at z 41-48, pot on one end
    block(-62, 56, V_SHAFT, 2 * R_AXLE, FILL["steel"], zorder=5)
    block(-7, 7, V_SHAFT, 24, FIXED, zorder=6)
    for sgn in (1, -1):
        s = lambda a, b: (min(sgn * a, sgn * b), max(sgn * a, sgn * b))
        block(*s(33, 40), V_SHAFT, 2 * R_BRG, TURNS, zorder=6)
        block(*s(*Z["fplate"]), V_SHAFT, 2 * (R_PINION + MODULE), FILL["pla"], zorder=6)
    block(-62, -56, V_SHAFT, 10, FILL["bearing"], zorder=6)
    ax.add_patch(Rectangle((-10, V_SHAFT - 12), 20, -22, fc="#f4f5f6", ec=INK, lw=0.7, zorder=4))  # motor body, along x
    ax.add_patch(Rectangle((-3, V_SHAFT - 12), 6, 4, fc=FILL["steel"], ec=INK, lw=0.5, zorder=4))  # its worm
    ax.text(0, V_SHAFT - 23, "hinge\nmotor", fontsize=6.3, ha="center", va="center", color=INK, zorder=8, linespacing=1.15)
    ax.text(-66, V_SHAFT, "hinge cross shaft\n(really 45 above\nthe axle)", fontsize=6.8, ha="right", va="center", color=INK, linespacing=1.2, zorder=12)
    letter(18, V_SHAFT, "F")
    letter(27, V_SHAFT - 20, "G")
    letter(63, V_SHAFT, "H")
    letter(-59, V_SHAFT - 18, "J")

    # drive motor in front of the axle: body across (z), sprocket on its shaft at z 0, chain down to the axle sprocket
    ax.add_patch(Rectangle((5, V_MOTOR - 18.5), 60, 37, fc="#f4f5f6", ec=INK, lw=0.7, zorder=4))
    ax.text(35, V_MOTOR, "drive motor 37D", fontsize=6.5, ha="center", va="center", color=INK, zorder=8)
    block(0, 5, V_MOTOR, 4, FILL["steel"], zorder=5)
    block(-3, 3, V_MOTOR, 2 * R_MOTOR_SPROCKET, FIXED, zorder=6)
    for dz in (-2.2, 2.2):
        ax.plot([dz, dz], [V_MOTOR - R_MOTOR_SPROCKET, V_AXLE + R_SPROCKET], color=INK, lw=0.9, zorder=7, dashes=(3, 1.5))
    ax.text(-8, V_MOTOR + 9, "chain", fontsize=6.5, ha="right", va="center", color=INK, zorder=8)
    letter(-12, V_MOTOR - 4, "K")

    # key
    lines = [f"{k}   {t}" if k else f"      {t}" for k, t in KEY]
    ax.text(118, V_MOTOR + 24, "\n".join(lines), fontsize=6.5, ha="left", va="top", color=INK, linespacing=1.38, zorder=12)
    ax.add_patch(Rectangle((118, V_SHAFT - 28), 8, 7, fc=FIXED, ec=INK, lw=0.6))
    ax.text(129, V_SHAFT - 24.5, "fixed to its shaft", fontsize=6.8, va="center", color=INK)
    ax.add_patch(Rectangle((190, V_SHAFT - 28), 8, 7, fc=TURNS, ec=INK, lw=0.6))
    ax.text(201, V_SHAFT - 24.5, "turns on it (608ZZ)", fontsize=6.8, va="center", color=INK)
    ax.set_xlim(-128, 300)
    ax.set_ylim(V_SHAFT - 58, V_MOTOR + 30)


# ----------------------------------------------------------------------------- view 3: the table
TABLE = [
    ("Part", "Fixed to", "Turns relative to", "Driven by"),
    ("Middle axle", "its 4 pulleys and the\nsprocket (set screws)", "rear and front plates\n(a 608 in each)", "drive motor, chain"),
    ("Rear axle,\nfront axle", "its 2 pulleys", "its plates (608s)", "its track (idles)"),
    ("Pulleys, 8", "their axle", "—", "the axle"),
    ("Rear tracks, 2", "—", "run round their pulleys;\nlower run slides on the rail", "middle-axle rear\npulleys (teeth)"),
    ("Front tracks, 2", "—", "as above", "middle-axle front\npulleys"),
    ("Rear plates + box", "each other: cross bars\nand box bars (M4)", "middle axle (608s)", "— (the frame)"),
    ("Front plates +\nsector gears", "each other (cross bars);\nsector 3 × M3", "middle axle (608s);\nrear plates: +35° / −37°", "hinge motor, via\npinion and sector"),
    ("Cross shaft +\n2 pinions", "worm wheel", "box (2 × 608)", "hinge worm\ngearmotor"),
    ("Both motors", "box", "—", "battery, controller"),
    ("Potentiometer", "box (body)", "— (wiper turned by\nthe cross shaft)", "cross shaft: reads\nthe hinge angle"),
    ("Lasers, 2", "a plate end each,\nlooking down", "—", "—"),
]


def table(fig, x, y, w, h):
    cols = [0.19, 0.28, 0.30, 0.23]
    xs = [x + w * sum(cols[:i]) for i in range(4)]
    n = len(TABLE)
    rh = h / n
    fig.text(x, y + 0.006, "3  What is fixed to what, and what turns relative to what", fontsize=9.5, color=INK, va="bottom")
    for i, row in enumerate(TABLE):
        top = y - i * rh
        if i == 0:
            fig.add_artist(Rectangle((x, top - rh), w, rh, fc=FILL["light"], ec="none", transform=fig.transFigure, zorder=1))
        for j, cell in enumerate(row):
            fig.text(xs[j] + 0.004, top - rh / 2, cell, fontsize=6.6, color=INK, va="center", ha="left", linespacing=1.15,
                     fontweight="bold" if i == 0 else "normal", zorder=2)
        fig.add_artist(Line2D([x, x + w], [top - rh, top - rh], color=DIM if i == 0 else "#c9ced3", lw=0.8 if i == 0 else 0.4, transform=fig.transFigure))


# ----------------------------------------------------------------------------- the sheet
NOTES = [
    "NOTES",
    "1  Sizes from parts_spec.json (1:5, mm): axles 225 apart, pulleys",
    "   Ø31.8 pitch, track 16.74 to its face and 19.74 to the cleat tips,",
    "   plates 45 × 7, 608 bearings, z stations as listed in view 2.",
    "   A diagram, not a part drawing: nothing here is to be made from.",
    "2  Not in the spec, drawn to the team's values: pinion r 10 and",
    "   sector R 35 (module 1.25, 16 T, centre distance 45); chain",
    "   sprockets r 12 and r 6; box −210 to +24 long and −10 to +60",
    "   tall (its 80 width is the spec's); lasers 9 beyond the end",
    "   axles. Check them against the real parts before building.",
    "3  Forward = the front segment leads. Middle axle clockwise in",
    "   view 1 moves both tracks' lower runs backward. Hinge: pinion",
    "   clockwise = front up. The worm holds the angle with the power",
    "   off. The pot is drawn on the cross shaft, where it turns 3.5 ×",
    "   the hinge angle (±37° → ±130°, inside a 270° pot); the team's",
    "   pot may sit elsewhere on the hinge.",
    "4  Fit check: a 37D gearmotor with its shaft across (z) is 60–90",
    "   long, more than the 80 between the box walls. Offset the",
    "   sprocket, widen the box, or lie the motor along x behind a",
    "   right-angle stage.",
    "Make / buy: motors, pot, lasers, chain, sprockets, 608s, rod: buy",
    "(the team's). Sector and pinion: print, PETG, qty 2 each. Plates,",
    "tracks, pulleys, bearings, axles: as their own sheets.",
]


def main():
    fig, add_view = sheet("Drive and motion: how the two segments turn and link to the motors and the box",
                          "1:5 prototype, ES1 stairs. Diagram at the spec's proportions (mm). Rear segment left, front segment right. Red = motion.",
                          size=(11.69, 8.27))
    ax1 = add_view([0.02, 0.455, 0.66, 0.40], "1  Side view at the middle axle (x–y): front segment straight, and dashed at its two swing limits")
    side_view(ax1)
    ax2 = add_view([0.02, 0.02, 0.56, 0.39], "2  Shaft line from above (x–z): what is clamped to each shaft and what turns on it")
    shaft_view(ax2)
    table(fig, 0.60, 0.395, 0.38, 0.365)
    fig.text(0.695, 0.862, "\n".join(NOTES), fontsize=6.9, color=INK, va="top", linespacing=1.42,
             bbox=dict(boxstyle="square,pad=0.5", fc=FILL["light"], ec="none"))
    out = save(fig, "motion_and_drive")
    from PIL import Image  # drop the writer's metadata so the file carries nothing but the picture
    Image.open(out).save(out, pnginfo=None)


if __name__ == "__main__":
    main()
