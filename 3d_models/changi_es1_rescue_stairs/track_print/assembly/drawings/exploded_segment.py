#!/usr/bin/env python3
"""Exploded assembly sheet: one track segment (the FRONT segment, plates inboard) of the 1:5
ES1 stair-climber prototype. Flat 2D matplotlib drawing, no 3D rendering.

Every number comes from assembly/parts_spec.json. Where the spec is silent the number is
derived here and marked "derived" in the comments (and listed in the result notes):
  * pulley over flanges 20 = 17 + 2 x 1.5, overall 27 = 20 + 7 hub; with the hub at the spec's
    z 67-74 the flanges sit at z 47-67, which overlaps the plate (41-48) by 1 mm because the
    spec's 18 mm lane is 2 mm narrower than the pulley (spec problem, marked red on the sheet).
  * track radii: tooth tips 30.69/2 - 2 = 13.345, root 15.345, backing face 16.745, cleats 19.745.
  * plate at the axle: y -12 to +28 (stadium R20 ends centred 8 above the axle); front plate web
    z 41-49 (plate 7 + the 1 mm gap), rail z 49-67; web bottom 13.34 + 4 = 17.34.
  * sector holes as parts_spec.json sector_bolts (R17 at 50/90/130 deg).
  * plate length 265 = 225 + 2 x 20.
  * fastener sizes that are standards, not in the spec: M3 nut 2.4, M4 nut 3.2, M4 washer 0.8 x 9 (DIN 934 / 125).
  * the box wall is drawn 4 mm thick with a clearance bore: the box is not in this set.

Run:  python3 exploded_segment.py   ->  drawings/exploded_segment.png
"""
import math
import sys

from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle
from shapely.geometry import Point, box as shp_box
from shapely.ops import unary_union

sys.path.insert(0, "/home/user/fleet_adapter_template/3d_models/changi_es1_rescue_stairs/track_print/assembly")
from drawing import (DIM, FILL, INK, MUTED, RED, SPEC, centreline, circle, dim_h, dim_v, leader,  # noqa: E402
                     outline, rect, save, sheet)

# --------------------------------------------------------------------------- numbers (parts_spec.json)
P = SPEC["parts"]
LAY, SEG = SPEC["layout_decision"], SPEC["segment"]
TR, PU, AX, BR, SP, CB = P["track"], P["pulley"], P["axle"], P["bearing"], P["side_plate"], P["cross_bar"]
BOX_Z = 40.0                                   # "box (to 40)" in layout_decision.summary
GAP = 1.0                                      # "plate 41-48" after "box to 40": 1 mm between bands
CENTRES = SEG["axle_to_axle_mm"]               # 225
# plate
PL_T, PL_H, PL_BELOW, PL_ABOVE = (SP["plate"]["thickness_mm"], SP["plate"]["height_mm"],
                                  SP["plate"]["bottom_edge_below_axle_mm"], SP["plate"]["top_edge_above_axle_mm"])  # 7, 40, 12, 28
END_R = 20.0                                   # "R20 semicircular ends" (plate.shape)
ARC_CY = (PL_ABOVE - PL_BELOW) / 2             # derived 8: arc centre above the axle so the plate spans -12..28
PL_LEN = CENTRES + 2 * END_R                   # derived 265
POCKET_D, POCKET_DEPTH = SP["bearing_pockets"]["dia_mm"], SP["bearing_pockets"]["depth_mm"]   # 22.2, 7
RAIL_X0, RAIL_X1, RAIL_W, RAIL_T, RAIL_TOP = (SP["rail"]["from_x_mm"], SP["rail"]["to_x_mm"], SP["rail"]["width_mm"],
                                              SP["rail"]["thickness_mm"], SP["rail"]["top_face_below_axle_mm"])  # 20, 205, 18, 4, 13.34
RAIL_BOT = RAIL_TOP + RAIL_T                   # derived 17.34 (spec note rounds it to 17.3)
BAR_D, BAR_X, BAR_Y = SP["cross_bar_holes"]["dia_mm"], SP["cross_bar_holes"]["at_x_mm"], SP["cross_bar_holes"]["above_axle_mm"]  # 4.5, [60,200], 22
SECT_R, SECT_D, SECT_ANG = SP["sector_bolts"]["radius_mm"], SP["sector_bolts"]["dia_mm"], tuple(SP["sector_bolts"]["angles_deg"])
# z bands, one side (layout_decision.summary)
Z_PLATE = (BOX_Z + GAP, BOX_Z + GAP + PL_T)                  # 41-48
LANE_W = PU["over_flanges_mm"]                              # 20: the pulley over its flanges
Z_LANE = (Z_PLATE[1] + GAP, Z_PLATE[1] + GAP + LANE_W)       # 49-69
Z_HUB = (Z_LANE[1], Z_LANE[1] + PU["hub_length_mm"])         # 67-74
Z_RLANE = (Z_HUB[1] + GAP, Z_HUB[1] + GAP + LANE_W)          # 77-97 rear lane
RAIL_Z0 = (Z_LANE[0] + Z_LANE[1]) / 2 - RAIL_W / 2           # 50: the rail is centred under its lane
BOSS_R = SP["plate"]["boss_radius_mm"]                    # 14.5
Z_RHUB = (Z_RLANE[1], Z_RLANE[1] + PU["hub_length_mm"])      # 93-100
Z_RPLATE = (Z_RHUB[1] + GAP, Z_RHUB[1] + GAP + PL_T)         # 101-108
assert Z_RPLATE[1] * 2 == LAY["width_over_plates_mm"] and Z_RLANE[1] * 2 == LAY["width_over_tracks_mm"]
# pulley (stand-in sizes, spec parts.pulley)
FL_T, FACE, HUB_L, HUB_D, FL_D, OD, BORE = (PU["flange_thickness_mm"], PU["face_width_between_flanges_mm"], PU["hub_length_mm"],
                                            PU["hub_dia_mm"], PU["flange_dia_mm"], PU["outside_dia_mm"], PU["bore_mm"])
OVER_FL = 2 * FL_T + FACE                      # derived 20
PU_OAL = OVER_FL + HUB_L                       # 27, equals PU["overall_length_mm"]
assert PU_OAL == PU["overall_length_mm"]
Z_PUL = (Z_HUB[0] - OVER_FL, Z_HUB[1])         # derived: flanges 47-67 when the hub is at 67-74
R_FL, R_OD, R_HUB, R_AX = FL_D / 2, OD / 2, HUB_D / 2, AX["dia_mm"] / 2
# track on the pulley (radii derived from the pulley OD and the track section)
T_W, T_TOTAL, T_TOOTH, T_BACK, T_CLEAT = (TR["width_mm"], TR["total_thickness_mm"], TR["teeth"]["height_mm"],
                                           TR["backing_thickness_mm"], TR["cleats"]["height_mm"])   # 15, 6.4, 2, 1.4, 3
assert abs(T_TOOTH + T_BACK + T_CLEAT - T_TOTAL) < 1e-9
R_TIP, R_ROOT, R_FACE, R_CLEAT = R_OD - T_TOOTH, R_OD, R_OD + T_BACK, R_OD + T_BACK + T_CLEAT   # 13.345, 15.345, 16.745, 19.745
assert abs(R_CLEAT - SEG["axle_to_cleat_tip_mm"]) < 0.01 and abs(R_FACE - SEG["axle_to_track_face_mm"]) < 0.01
# bearing
BR_OD, BR_W = BR["outside_dia_mm"], BR["width_mm"]           # 22, 7
R_BR = BR_OD / 2
assert BR_W == PL_T == POCKET_DEPTH, "608 is flush both faces of the 7 mm plate"
# axles
AX_MID, AX_FRONT = AX["lengths_mm"]["middle"], AX["lengths_mm"]["front"]      # 220, 160
FLAT_DEPTH, FLAT_LEN = 0.5, 10.0                                              # axle.flats
# cross bars
ROD_F, SPC_F, SPC_OD = CB["front_segment"]["rod_length_mm"], CB["front_segment"]["spacer_length_mm"], CB["front_segment"]["spacer_od_mm"]  # 110, 82, 10
ROD_R, SPC_R = CB["rear_segment"]["rod_length_mm"], CB["rear_segment"]["spacer_length_mm"]   # 230, 202
END_F = (ROD_F - SPC_F - 2 * PL_T) / 2         # derived 7 per end (nut + washer + proud)
assert END_F == (ROD_R - SPC_R - 2 * PL_T) / 2 == 7.0
M4_NUT, M4_WASHER, M4_WASHER_D = 3.2, 0.8, 9.0  # DIN 934 / DIN 125, not in the spec
M3_NUT, M3_BOLT_L, SECTOR_T = 2.4, 14.0, 3.0    # DIN 934; "6 x M3 x 14"; sector 3 thick (spec sector_bolts.note)
SET_SCREW_STAND_IN = "M3 x 6"                   # set_screws_and_bolts
HUB_WALL = (HUB_D - BORE) / 2                   # derived 5: set-screw thread engagement
SS_D, SS_L = 4.0, 8.0                           # set screw as drawn: M4, 8 long (6 to 8 on the sheet)
BOX_T = 4.0                                     # box wall thickness: not in the spec, drawn 4

FIG_W, FIG_H = 11.69, 8.27                      # A4 landscape, inches
fig, add_view = sheet("EXPLODED ASSEMBLY  -  one track segment  (front segment, plates inboard)",
                      "ES1 stair-climbing rescue carrier, 1:5 prototype.   Dimensions in mm at model size.   "
                      "One side shown (z from the vehicle centre line); the other side mirrors.   Sheet 1 of 1.",
                      size=(FIG_W, FIG_H))


def view_in(x_in, y_in, xlim, ylim, scale, name=None):
    """Equal-aspect axes placed by inches from the sheet's bottom-left, data window xlim x ylim at `scale` (1 = full model size)."""
    w_in = (xlim[1] - xlim[0]) * scale / 25.4
    h_in = (ylim[1] - ylim[0]) * scale / 25.4
    ax = add_view([x_in / FIG_W, y_in / FIG_H, w_in / FIG_W, h_in / FIG_H], name)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_anchor("SW")
    return ax


def th(scale, pt=8):
    """Height of a text line in data units (mm) at this scale."""
    return 1.05 * pt / 72 * 25.4 / scale


def balloon(ax, x, y, n, r, text=None, fontsize=7.5, to=None, ha="left"):
    """Key number in a circle, optional text beside it, optional thin leader to the part."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=0.8, zorder=6))
    ax.text(x, y, str(n), ha="center", va="center", fontsize=7.5, fontweight="bold", color=INK, zorder=7)
    if text:
        sgn = 1 if ha == "left" else -1
        ax.text(x + sgn * 1.4 * r, y, text, ha=ha, va="center", fontsize=fontsize, color=INK, zorder=7,
                bbox=dict(fc="white", ec="none", pad=0.6))
    if to:
        ax.plot([x, to[0]], [y - r if to[1] < y else y + r, to[1]], color=MUTED, lw=0.5, zorder=5)


def break_edge(ax, x0, x1, y, amp, n=3):
    """A zig-zag break line between x0 and x1 at height y."""
    xs, ys = [x0], [y]
    for i in range(1, 2 * n):
        xs.append(x0 + (x1 - x0) * i / (2 * n))
        ys.append(y + (amp if i % 2 else -amp))
    xs.append(x1)
    ys.append(y)
    ax.plot(xs, ys, color=INK, lw=0.7, zorder=4)


def bearing_section(ax, z0, z1):
    """608 cut along the axle: hatched ring above and below the bore, a ball in each (schematic)."""
    for s in (+1, -1):
        rect(ax, z0, min(s * R_AX, s * R_BR), z1 - z0, R_BR - R_AX, FILL["bearing"], hatch=True, lw=0.6)
        ax.add_patch(Circle(((z0 + z1) / 2, s * (R_AX + R_BR) / 2), 1.7, fc="white", ec=INK, lw=0.5, zorder=3))


def pulley_section(ax, z0, lw=0.7):
    """Pulley cut along the axle, first flange at z0: flange | face | flange | hub. Returns the hub's z range."""
    fill = FILL["pla"]
    zf1, zb, zf2, zh = z0, z0 + FL_T, z0 + FL_T + FACE, z0 + OVER_FL
    for s in (+1, -1):
        lo = lambda r: min(s * R_AX, s * r)  # noqa: E731
        rect(ax, zf1, lo(R_FL), FL_T, R_FL - R_AX, fill, hatch=True, lw=lw)
        rect(ax, zf2, lo(R_FL), FL_T, R_FL - R_AX, fill, hatch=True, lw=lw)
        rect(ax, zb, lo(R_TIP), FACE, R_TIP - R_AX, fill, hatch=True, lw=lw)      # body below the grooves
        rect(ax, zb, R_TIP if s > 0 else -R_OD, FACE, R_OD - R_TIP, fill, hatch=False, lw=lw)  # tooth band, unsectioned
        rect(ax, zh, lo(R_HUB), HUB_L, R_HUB - R_AX, fill, hatch=True, lw=lw)
    return zh, zh + HUB_L


def track_on_pulley(ax, zc, lw=0.5):
    """Track cut at the axle, 15 wide centred on the pulley face: teeth in the grooves, backing, cleats out."""
    z0 = zc - T_W / 2
    for s in (+1, -1):
        rect(ax, z0, min(s * R_TIP, s * R_ROOT), T_W, T_TOOTH, FILL["tpu"], lw=lw)
        rect(ax, z0, min(s * R_ROOT, s * R_FACE), T_W, T_BACK, FILL["tpu"], lw=lw)
        rect(ax, z0, min(s * R_FACE, s * R_CLEAT), T_W, T_CLEAT, FILL["tpu"], lw=lw, alpha=0.45)
        for k in range(1, 5):   # a few tooth marks so the inner band reads as teeth
            zz = z0 + T_W * k / 5
            ax.plot([zz, zz], [s * R_TIP, s * R_ROOT], color="white", lw=0.5, zorder=3)


def hex_nut(ax, x, y, w, h, fill=FILL["steel"], lw=0.6):
    """Nut seen from the side: a rectangle with the two chamfer lines."""
    rect(ax, x, y, w, h, fill, lw=lw)
    ax.plot([x, x + w], [y + h * 0.33] * 2, color=INK, lw=0.3)
    ax.plot([x, x + w], [y + h * 0.67] * 2, color=INK, lw=0.3)


def text_in(x_in, y_in, s, **kw):
    """Figure text placed in inches."""
    kw.setdefault("fontsize", 7)
    kw.setdefault("color", INK)
    return fig.text(x_in, y_in, s, transform=fig.dpi_scale_trans, **kw)


# =============================================================================================
# (1) MAIN: exploded end view, y-z plane, looking along the vehicle from the front.
# Horizontal = z from the vehicle centre line, vertical = y from the axle.  Parts drawn in
# section at the middle axle and pulled apart along z (not their assembled positions).
# =============================================================================================
S1 = 0.84
E_PLATE, E_BEAR, E_PUL = 24.0, 64.0, 95.0       # explode shifts along z
zp0, zp1 = Z_PLATE[0] + E_PLATE, Z_PLATE[1] + E_PLATE       # 65-72
zb0, zb1 = Z_PLATE[0] + E_BEAR, Z_PLATE[1] + E_BEAR         # 105-112
zq0 = Z_PUL[0] + E_PUL                                      # 142 (first flange)
Z_AX0, Z_AX1 = 20.0, 182.0                                  # drawn axle extent (both ends broken)
ax1 = view_in(0.35, 4.30, (18.0, 192.0), (-39.0, 48.0), S1,
              "1   EXPLODED END VIEW (y-z) at the middle axle, looking from the front: parts cut along the axle "
              "and pulled apart along z, the axle left in")

# axle, Ø8, drawn through everything, both ends broken
rect(ax1, Z_AX0, -R_AX, Z_AX1 - Z_AX0, 2 * R_AX, FILL["steel"], lw=0.7)
for zz in (Z_AX0, Z_AX1):
    rect(ax1, zz - 1.2, -R_AX - 0.3, 2.4, 2 * R_AX + 0.6, "white", lw=0)
    ax1.plot([zz - 1.0, zz + 0.3, zz - 0.3, zz + 1.0], [-R_AX - 0.4, -R_AX / 2, R_AX / 2, R_AX + 0.4], color=INK, lw=0.7)
# the flat under the hub (drawn under the exploded hub; on the axle it is at z 65.5-75.5)
zh0, zh1 = zq0 + OVER_FL, zq0 + OVER_FL + HUB_L
flat_c = (zh0 + zh1) / 2
rect(ax1, flat_c - FLAT_LEN / 2, R_AX - FLAT_DEPTH, FLAT_LEN, FLAT_DEPTH, "white", lw=0.5)

# box wall, outer face at z 40, thickness not in the spec: drawn 4, broken top and bottom
BW_Y0, BW_Y1 = -28.0, 30.0
rect(ax1, BOX_Z - BOX_T, BW_Y0, BOX_T, BW_Y1 - BW_Y0, FILL["light"], hatch=True, lw=0.7)
rect(ax1, BOX_Z - BOX_T - 0.5, -R_AX - 0.5, BOX_T + 1.0, 2 * R_AX + 1.0, "white", lw=0)   # clearance bore
rect(ax1, BOX_Z - BOX_T - 0.5, -R_AX, BOX_T + 1.0, 2 * R_AX, FILL["steel"], lw=0)          # axle through it
for yy in (BW_Y0, BW_Y1):
    rect(ax1, BOX_Z - BOX_T - 0.3, yy - 1.2, BOX_T + 0.6, 2.4, "white", lw=0)
    break_edge(ax1, BOX_Z - BOX_T, BOX_Z, yy, 1.0, n=2)

# front plate (4): cut at the middle axle: through the pocket and the top M3 sector hole
Y_SECT = SECT_R  # the 90-degree hole
rect(ax1, zp0, R_BR + 0.1, PL_T, Y_SECT - SECT_D / 2 - (R_BR + 0.1), FILL["petg"], hatch=True, lw=0.7)   # 11.1 to 12.3
rect(ax1, zp0, Y_SECT + SECT_D / 2, PL_T, PL_ABOVE - (Y_SECT + SECT_D / 2), FILL["petg"], hatch=True, lw=0.7)  # 15.7 to 28
rect(ax1, zp0, -BOSS_R, PL_T, BOSS_R - (R_BR + 0.1), FILL["petg"], hatch=True, lw=0.7)   # the boss wall under the pocket, 3.4
rect(ax1, zp0, Y_SECT - SECT_D / 2, PL_T, SECT_D, "white", lw=0.5)        # M3 hole, open
# web and rail foot: at x 20-205, beyond the cut, drawn unsectioned
rect(ax1, zp0, -RAIL_BOT, RAIL_Z0 - Z_PLATE[0], RAIL_BOT - PL_BELOW, FILL["petg"], lw=0.6, alpha=0.55)   # web z 41-50
rect(ax1, RAIL_Z0 + E_PLATE, -RAIL_BOT, RAIL_W, RAIL_T, FILL["petg"], lw=0.6, alpha=0.55)               # rail z 50-68
ax1.plot([zp0, zp1], [-R_BR - 0.1] * 2, color=INK, lw=0.5)   # pocket wall, top and bottom
ax1.plot([zp0, zp1], [R_BR + 0.1] * 2, color=INK, lw=0.5)

# bearing (3)
bearing_section(ax1, zb0, zb1)

# pulley (2) with the track (1) on it
pulley_section(ax1, zq0)
track_on_pulley(ax1, zq0 + FL_T + FACE / 2)
# set screw in the hub: M4 on bought pulleys (stand-in M3 x 6), tip on the flat
rect(ax1, flat_c - 1.65, R_AX - FLAT_DEPTH, 3.3, HUB_WALL + FLAT_DEPTH, "white", lw=0.4)       # tapped hole (3.3 tap drill)
rect(ax1, flat_c - SS_D / 2, R_AX - FLAT_DEPTH, SS_D, SS_L, FILL["steel"], lw=0.6)             # the screw
ax1.plot([flat_c - 1.0, flat_c + 1.0], [R_AX - FLAT_DEPTH + SS_L - 1.2] * 2, color=INK, lw=0.5)

# centre line through every bore, on top of the axle
centreline(ax1, 18.5, 0, 191.5, 0)
ax1.lines[-1].set_zorder(6)

# ---- dimensions: widths (horizontal)
TH1 = th(S1)
dim_h(ax1, zp0, zp1, PL_ABOVE + 3.5, f"{PL_T:g}", ext_from=PL_ABOVE, offset=0.2)
dim_h(ax1, zb0, zb1, R_BR + 3.5, f"{BR_W:g}", ext_from=R_BR, offset=0.2)
dim_h(ax1, zq0 + FL_T, zq0 + FL_T + FACE, R_FL + 3.6, f"{FACE:g} between flanges", ext_from=R_FL, offset=0.2)
dim_h(ax1, zq0, zq0 + OVER_FL, R_FL + 3.6 + TH1 + 2.0, f"{OVER_FL:g} over the {FL_T:g} flanges", ext_from=R_FL, offset=0.2)
dim_h(ax1, zh0, zh1, -R_HUB - 3.5, f"{HUB_L:g} hub", ext_from=-R_HUB, offset=-TH1 - 0.4)
dim_h(ax1, zp0, zp0 + (RAIL_Z0 - Z_PLATE[0]), -RAIL_BOT - 3.5, f"{RAIL_Z0 - Z_PLATE[0]:g} web", ext_from=-RAIL_BOT, offset=-TH1 - 0.4)
dim_h(ax1, RAIL_Z0 + E_PLATE, RAIL_Z0 + RAIL_W + E_PLATE, -RAIL_BOT - 3.5, f"{RAIL_W:g} rail", ext_from=-RAIL_BOT, offset=-TH1 - 0.4)
zt0 = zq0 + FL_T + FACE / 2 - T_W / 2
dim_h(ax1, zt0, zt0 + T_W, -R_CLEAT - 3.2, f"{T_W:g} track", ext_from=-R_CLEAT, offset=-TH1 - 0.4)
y27 = -R_CLEAT - 3.2 - TH1 - 4.0
ax1.plot([zq0, zq0], [-R_FL, y27 - 0.4], color=DIM, lw=0.5)
ax1.plot([zh1, zh1], [-R_HUB, y27 - 0.4], color=DIM, lw=0.5)
dim_h(ax1, zq0, zh1, y27, f"{PU_OAL:g} overall", offset=-TH1 - 0.4)
# ---- dimensions: heights and diameters (vertical)
dim_v(ax1, -PL_BELOW, PL_ABOVE, zp0 - 7.0, f"{PL_H:g}", ext_from=zp0)
dim_v(ax1, 0, PL_ABOVE, zp0 - 13.5, f"{PL_ABOVE:g}", ext_from=zp0)
dim_v(ax1, -PL_BELOW, 0, zp0 - 13.5, f"{PL_BELOW:g}", ext_from=zp0)
zr1 = Z_LANE[1] + E_PLATE
dim_v(ax1, -RAIL_TOP, 0, zr1 + 4.5, f"{RAIL_TOP:g}", ext_from=zr1, offset=-0.2)
dim_v(ax1, -RAIL_BOT, -RAIL_TOP, zr1 + 4.5, f"{RAIL_T:g}", ext_from=zr1, offset=4.2)
dim_v(ax1, -R_BR, R_BR, zb1 + 6.0, f"Ø{BR_OD:g}", ext_from=zb1)
dim_v(ax1, -R_FL, R_FL, zq0 - 7.0, f"Ø{FL_D:g} flange", ext_from=zq0)
dim_v(ax1, -R_HUB, R_HUB, zh1 + 6.0, f"Ø{HUB_D:g} hub", ext_from=zh1)
dim_v(ax1, -R_AX, R_AX, Z_AX1 + 7.0, f"Ø{AX['dia_mm']:g}", ext_from=Z_AX1)
# ---- leaders and balloons (two rows above the parts)
Y_A, Y_B = 38.5, 44.5
ax1.text(BOX_Z - BOX_T / 2, Y_A, "box, to z 40", ha="center", va="center", fontsize=7.5, color=INK)
ax1.text(BOX_Z - BOX_T / 2, Y_A - 4.3, "(not in this set)", ha="center", va="center", fontsize=6.5, color=MUTED)
balloon(ax1, zp0 - 2.0, Y_A, 4, 2.4, f"plate, z {Z_PLATE[0]:g}-{Z_PLATE[1]:g}", to=(zp0 + 1.0, PL_ABOVE + 0.2))
balloon(ax1, zb0 - 1.0, Y_A, 3, 2.4, "608ZZ, in the plate pocket", to=(zb0 + 1.5, R_BR + 0.2))
balloon(ax1, zq0 + 14.0, Y_A, 2, 2.4, f"pulley, hub z {Z_HUB[0]:g}-{Z_HUB[1]:g}", to=(zq0 + 16.0, R_FL + 3.6 + TH1 + 2.0 + TH1 + 0.6))
balloon(ax1, 112.0, Y_B, 1, 2.4, f"track, {T_W:g} wide on the {FACE:g} face", to=(zt0 + 1.0, R_CLEAT + 0.2))
leader(ax1, (flat_c + SS_D / 2, R_AX + SS_L - 2.5), (zh1 + 3.0, 20.0), "set screw on\nthe flat: (a)", fontsize=6.5)
leader(ax1, (zp0 + PL_T / 2, Y_SECT), (zp1 + 5.0, 24.0), f"M3 hole on R{SECT_R:g}\n(hinge sector)", fontsize=7)
leader(ax1, (zp0 + PL_T / 2, -BOSS_R + 0.6), (42.0, -28.5), f"{BOSS_R - R_BR - 0.1:.1f} wall: R{BOSS_R:g} boss\nround the pocket", fontsize=7)
ax1.text(Z_AX0 + 7.0, -33.5, f"middle axle Ø{AX['dia_mm']:g} x {AX_MID:g}, z -{AX_MID / 2:g} to +{AX_MID / 2:g}, drawn broken at both ends;",
         fontsize=7, color=INK, ha="left", va="center")
ax1.text(Z_AX0 + 1.0, -37.0, "the parts slide on from the outboard (right) end.  Rail foot (x 20-205) drawn unsectioned.",
         fontsize=7, color=INK, ha="left", va="center")
balloon(ax1, Z_AX0 + 3.0, -33.5, 5, 2.4)
ax1.text(191.0, -37.0, f"scale {S1:g} : 1", fontsize=6.5, color=MUTED, ha="right", va="center")

# =============================================================================================
# (1b) ASSEMBLED stations: the same section, not exploded, upper half, both segments' parts on the shared axle
# =============================================================================================
S1B = 0.62
Y_TICK = 33.0
ax1b = view_in(6.30, 3.28, (30.0, 114.0), (-14.5, 54.0), S1B, "1b  ASSEMBLED, z stations")
ax1b.text(30.5, -12.8, "upper half; rear segment in grey", fontsize=6.5, color=MUTED, ha="left", va="center")
rect(ax1b, 30.0, 0, AX_MID / 2 - 30.0, R_AX, FILL["steel"], lw=0.6)                    # axle to its end at 110
rect(ax1b, BOX_Z - BOX_T, R_AX, BOX_T, 30.0 - R_AX, FILL["light"], hatch=True, lw=0.6)
break_edge(ax1b, BOX_Z - BOX_T, BOX_Z, 30.0, 0.8, n=2)
for (p0, p1), grey in ((Z_PLATE, False), (Z_RPLATE, True)):
    fc = FILL["light"] if grey else FILL["petg"]
    rect(ax1b, p0, R_BR + 0.1, p1 - p0, PL_ABOVE - R_BR - 0.1, fc, hatch=not grey, lw=0.6)
    rect(ax1b, p0, R_AX, p1 - p0, R_BR - R_AX, FILL["bearing"] if not grey else FILL["light"], hatch=not grey, lw=0.6)
    ax1b.add_patch(Circle(((p0 + p1) / 2, (R_AX + R_BR) / 2), 1.5, fc="white", ec=INK, lw=0.4, zorder=3))
rect(ax1b, Z_PLATE[0], Y_SECT - SECT_D / 2, PL_T, SECT_D, "white", lw=0.4)
for (h0, h1), grey in ((Z_HUB, False), (Z_RHUB, True)):
    q0 = h0 - OVER_FL
    fc = FILL["light"] if grey else FILL["pla"]
    rect(ax1b, q0, R_AX, FL_T, R_FL - R_AX, fc, hatch=not grey, lw=0.6)
    rect(ax1b, q0 + FL_T + FACE, R_AX, FL_T, R_FL - R_AX, fc, hatch=not grey, lw=0.6)
    rect(ax1b, q0 + FL_T, R_AX, FACE, R_OD - R_AX, fc, hatch=not grey, lw=0.6)
    rect(ax1b, h0, R_AX, h1 - h0, R_HUB - R_AX, fc, hatch=not grey, lw=0.6)
    zc = q0 + FL_T + FACE / 2
    for y0, hh, a in ((R_TIP, T_TOOTH, 1.0), (R_ROOT, T_BACK, 1.0), (R_FACE, T_CLEAT, 0.45)):
        rect(ax1b, zc - T_W / 2, y0, T_W, hh, FILL["tpu"] if not grey else "#b9bec4", lw=0.4, alpha=a)
# station scale: ticks and values, staggered in two rows
stations = [BOX_Z, Z_PLATE[0], Z_PLATE[1], Z_LANE[0], Z_LANE[1], Z_HUB[1], Z_RLANE[0], Z_RLANE[1], Z_RHUB[1], Z_RPLATE[0], Z_RPLATE[1], AX_MID / 2]
row_hi = {Z_PLATE[0], Z_LANE[0], Z_HUB[1], Z_RHUB[1], Z_RPLATE[1]}
ax1b.plot([BOX_Z - 1, AX_MID / 2 + 1], [Y_TICK, Y_TICK], color=DIM, lw=0.5)
for z in stations:
    hi = z in row_hi
    ax1b.plot([z, z], [Y_TICK - 1.0, Y_TICK + (9.5 if hi else 1.5)], color=DIM, lw=0.5)
    ax1b.text(z, Y_TICK + (10.5 if hi else 2.5), f"{z:g}", rotation=90, ha="center", va="bottom", fontsize=7, color=INK)
# widths along the chain (the 1 mm gaps are not written)
for (a, b), t in (((Z_PLATE[0], Z_PLATE[1]), "7"), ((Z_LANE[0], Z_LANE[1]), f"{LANE_W:g} lane"), ((Z_HUB[0], Z_HUB[1]), "7"),
                  ((Z_RLANE[0], Z_RLANE[1]), f"{LANE_W:g} lane"), ((Z_RHUB[0], Z_RHUB[1]), "7"), ((Z_RPLATE[0], Z_RPLATE[1]), "7")):
    ax1b.add_patch(FancyArrowPatch((a, Y_TICK - 3.2), (b, Y_TICK - 3.2), arrowstyle="<|-|>", mutation_scale=5, lw=0.5, color=DIM, shrinkA=0, shrinkB=0))
    ax1b.text((a + b) / 2, Y_TICK - 3.2 + 0.6, t, ha="center", va="bottom", fontsize=6.5, color=INK, bbox=dict(fc="white", ec="none", pad=0.3))
ax1b.text(30.5, -4.0, f"each lane {LANE_W:g} = the pulley over its flanges;", fontsize=6.5, color=MUTED, ha="left", va="center")
ax1b.text(30.5, -8.5, "1 mm between bands", fontsize=6.5, color=MUTED, ha="left", va="center")
ax1b.text(BOX_Z - BOX_T / 2, 16.0, "box", rotation=90, fontsize=6.5, color=MUTED, ha="center", va="center",
          bbox=dict(fc="white", ec="none", pad=0.3))

# =============================================================================================
# (2) EXPLODED SIDE VIEW (x-y): the left front plate seen from outboard; pulleys, bearings, axles and cross bars lifted out
# =============================================================================================
S2 = 0.42
Y_BEAR, Y_BAR, Y_PUL, Y_AXLE = 48.0, 58.0, 96.0, 126.0
ax2 = view_in(0.35, 0.30, (-34.0, 258.0), (-50.0, 138.0), S2,
              "2   EXPLODED SIDE VIEW (x-y), left front plate seen from outboard")
ax2.text(-33.0, 134.5, "x from the middle axle (0) to the front axle (225).  Lifted parts drop onto the dashed lines.  "
         "Right plate mirrors.", fontsize=7, color=MUTED, ha="left", va="center")
plate_shape = unary_union([shp_box(0, -PL_BELOW, CENTRES, PL_ABOVE),
                           Point(0, ARC_CY).buffer(END_R, quad_segs=48), Point(CENTRES, ARC_CY).buffer(END_R, quad_segs=48),
                           Point(0, 0).buffer(BOSS_R, quad_segs=48), Point(CENTRES, 0).buffer(BOSS_R, quad_segs=48)])
outline(ax2, list(plate_shape.exterior.coords), FILL["petg"], lw=0.8)
rect(ax2, RAIL_X0, -RAIL_BOT, RAIL_X1 - RAIL_X0, RAIL_BOT - PL_BELOW, FILL["petg"], lw=0.7)   # web + rail silhouette
ax2.plot([RAIL_X0, RAIL_X1], [-RAIL_TOP] * 2, color=INK, lw=0.5)                            # rail top edge
for x in (0.0, CENTRES):
    circle(ax2, x, 0, POCKET_D / 2, fill="white", lw=0.7)
for x in BAR_X:
    circle(ax2, x, BAR_Y, BAR_D / 2, fill="white", lw=0.6)
for a in SECT_ANG:
    circle(ax2, SECT_R * math.cos(math.radians(a)), SECT_R * math.sin(math.radians(a)), SECT_D / 2, fill="white", lw=0.5)
for x in (0.0, CENTRES):
    centreline(ax2, x, -PL_BELOW - 2, x, Y_AXLE + 8)
    centreline(ax2, x - 14, 0, x + 14, 0)
for x in BAR_X:
    centreline(ax2, x, BAR_Y - 8, x, Y_BAR + 8)
# lifted parts
for x in (0.0, CENTRES):
    circle(ax2, x, Y_BEAR, R_BR, fill=FILL["bearing"], lw=0.7)
    circle(ax2, x, Y_BEAR, R_BR - 2.2, fill="none", lw=0.4)
    circle(ax2, x, Y_BEAR, R_AX + 2.0, fill="none", lw=0.4)
    circle(ax2, x, Y_BEAR, R_AX, fill="white", lw=0.6)
    circle(ax2, x, Y_PUL, R_FL, fill=FILL["pla"], lw=0.7)
    circle(ax2, x, Y_PUL, R_OD, fill="none", lw=0.4, ls=(0, (3, 2)))
    circle(ax2, x, Y_PUL, R_AX, fill="white", lw=0.6)
    circle(ax2, x, Y_AXLE, R_AX, fill=FILL["steel"], lw=0.7)
for x in BAR_X:
    circle(ax2, x, Y_BAR, SPC_OD / 2, fill=FILL["petg"], lw=0.6)
    ax2.add_patch(Polygon([(x + 4.0 * math.cos(math.radians(60 * k)), Y_BAR + 4.0 * math.sin(math.radians(60 * k))) for k in range(6)],
                          closed=True, fc=FILL["steel"], ec=INK, lw=0.5))
    circle(ax2, x, Y_BAR, R_AX / 2, fill="white", lw=0.4)
# dimensions
TH2 = th(S2)
Y_D1 = -RAIL_BOT - 5.0
dim_h(ax2, 0, RAIL_X0, Y_D1, f"{RAIL_X0:g}", ext_from=-RAIL_BOT, offset=-TH2 - 0.5)
dim_h(ax2, RAIL_X0, RAIL_X1, Y_D1, f"{RAIL_X1 - RAIL_X0:g} rail", ext_from=-RAIL_BOT, offset=-TH2 - 0.5)
Y_D2 = Y_D1 - TH2 - 4.5
dim_h(ax2, 0, CENTRES, Y_D2, f"{CENTRES:g} axle to axle", offset=-TH2 - 0.5)
Y_D3 = Y_D2 - TH2 - 4.5
dim_h(ax2, -END_R, CENTRES + END_R, Y_D3, f"{PL_LEN:g} over the plate", ext_from=-PL_BELOW + 4, offset=-TH2 - 0.5)
for x in (0.0, CENTRES):
    ax2.plot([x, x], [-PL_BELOW - 1, Y_D2 - 0.4], color=DIM, lw=0.5)
dim_h(ax2, 0, BAR_X[0], Y_BAR + SPC_OD / 2 + 4.0, f"{BAR_X[0]:g}", ext_from=Y_BAR + SPC_OD / 2, offset=0.3)
dim_h(ax2, 0, BAR_X[1], Y_BAR + SPC_OD / 2 + 4.0 + TH2 + 1.5, f"{BAR_X[1]:g}", ext_from=Y_BAR + SPC_OD / 2, offset=0.3)
dim_v(ax2, -PL_BELOW, PL_ABOVE, -27.0, f"{PL_H:g}", ext_from=-END_R)
dim_v(ax2, 0, BAR_Y, CENTRES + END_R + 7.0, f"{BAR_Y:g}", ext_from=BAR_X[1] + BAR_D / 2)
ax2.plot([CENTRES + R_BR, CENTRES + END_R + 7.4], [0, 0], color=DIM, lw=0.5)
# leaders and labels (inside the plate where there is room)
leader(ax2, (CENTRES + END_R * math.cos(math.radians(40)), ARC_CY + END_R * math.sin(math.radians(40))), (CENTRES + 23.0, 36.0), f"R{END_R:g}", fontsize=7)
leader(ax2, (POCKET_D / 2 * math.cos(math.radians(-35)), POCKET_D / 2 * math.sin(math.radians(-35))), (30.0, 3.0),
       f"Ø{POCKET_D:g} pocket x2, {POCKET_DEPTH:g} deep (through)", fontsize=6.5)
leader(ax2, (SECT_R + SECT_D / 2, 0.8), (30.0, 16.0), f"3 x Ø{SECT_D:g} on R{SECT_R:g} (hinge sector, M3)", fontsize=6.5)
leader(ax2, (BAR_X[0] + BAR_D / 2, BAR_Y + 1.0), (74.0, 36.0), f"Ø{BAR_D:g} x2, cross bars", fontsize=6.5)
leader(ax2, (120.0, -RAIL_BOT + 0.5), (30.0, -6.0), f"rail {RAIL_W:g} wide, {RAIL_T:g} thick, top {RAIL_TOP:g} below the axle", fontsize=6.5)
balloon(ax2, 142.0, 16.0, 4, 4.2, f"front plate {PL_LEN:g} x {PL_H:g} x {PL_T:g}, PETG", fontsize=6.3)
balloon(ax2, 26.0, Y_BEAR, 3, 4.2, f"608ZZ Ø{BR_OD:g} x {BR_W:g}, pressed in, flush: see (d)", fontsize=7)
balloon(ax2, 75.0, Y_BAR, 7, 4.2, f"cross bar: M4 rod {ROD_F:g} + spacer Ø{SPC_OD:g} x {SPC_F:g} (c)", fontsize=7)
balloon(ax2, 26.0, Y_PUL, 2, 4.2, f"pulley HTD 5M 20T, Ø{FL_D:g} over flanges, set-screwed: see (a)", fontsize=7)
balloon(ax2, 14.0, Y_AXLE, 5, 4.2, f"middle axle Ø{AX['dia_mm']:g} x {AX_MID:g}", fontsize=7)
balloon(ax2, CENTRES - 14.0, Y_AXLE, 6, 4.2, f"front axle Ø{AX['dia_mm']:g} x {AX_FRONT:g}", fontsize=7, ha="right")
ax2.text(257.0, -47.0, f"scale {S2:g} : 1", fontsize=6.5, color=MUTED, ha="right", va="center")

# =============================================================================================
# (3) SCREW DEPTHS: four small sections
# =============================================================================================
GX0, GY0, GW, GH = 5.50, 0.30, 2.92, 1.55        # grid origin and cell size, inches


def cell(col, row, xlim, ylim, scale, name):
    return view_in(GX0 + col * GW, GY0 + (1 - row) * GH, xlim, ylim, scale, name)


# (a) pulley set screw -------------------------------------------------------------------------
Sa = 1.3
axa = cell(0, 0, (-10.0, 47.0), (-7.5, 17.0), Sa, f"a   PULLEY SET SCREW  ({Sa:g}:1)")
rect(axa, -8.0, -R_AX, 23.0, 2 * R_AX, FILL["steel"], lw=0.6)                                   # axle
fc0 = HUB_L / 2
rect(axa, fc0 - FLAT_LEN / 2, R_AX - FLAT_DEPTH, FLAT_LEN, FLAT_DEPTH, "white", lw=0.4)          # the flat
rect(axa, 0.0, R_AX, HUB_L, HUB_WALL, FILL["pla"], hatch=True, lw=0.6)                          # hub wall, upper half
rect(axa, fc0 - 1.65, R_AX - FLAT_DEPTH, 3.3, HUB_WALL + FLAT_DEPTH, "white", lw=0.4)
rect(axa, fc0 - SS_D / 2, R_AX - FLAT_DEPTH, SS_D, SS_L, FILL["steel"], lw=0.6)
axa.plot([fc0 - 1.0, fc0 + 1.0], [R_AX - FLAT_DEPTH + SS_L - 1.2] * 2, color=INK, lw=0.5)
for i in range(5):  # thread marks
    yy = R_AX + 0.6 + i * 1.0
    axa.plot([fc0 - SS_D / 2 - 0.3, fc0 - SS_D / 2], [yy, yy + 0.4], color=INK, lw=0.3)
    axa.plot([fc0 + SS_D / 2, fc0 + SS_D / 2 + 0.3], [yy, yy + 0.4], color=INK, lw=0.3)
centreline(axa, -9.5, 0, 16.0, 0)
dim_v(axa, R_AX, R_AX + HUB_WALL, HUB_L + 3.0, f"{HUB_WALL:g}", ext_from=HUB_L, fontsize=7)
dim_v(axa, R_AX - FLAT_DEPTH, R_AX - FLAT_DEPTH + SS_L, -4.0, f"{SS_L:g}", ext_from=fc0 - SS_D / 2, fontsize=7)
dim_h(axa, fc0 - FLAT_LEN / 2, fc0 + FLAT_LEN / 2, R_AX + SS_L + 1.8, f"{FLAT_LEN:g} flat", ext_from=R_AX - FLAT_DEPTH, offset=0.2, fontsize=7)
leader(axa, (fc0 + FLAT_LEN / 2 - 0.5, R_AX - FLAT_DEPTH / 2), (11.0, -6.0), f"flat {FLAT_DEPTH:g} deep, filed", fontsize=6.3)
axa.text(17.5, 6.0, f"M4 on bought pulleys (2 at 90°),\nstand-in {SET_SCREW_STAND_IN}.\nThread in the hub wall = {HUB_WALL:g}\n"
         f"= (Ø{HUB_D:g} - Ø{BORE:g}) / 2.\nScrew 6 to 8 long: 6 ends flush,\n8 stands 2.5 proud.\nTip bears on the {FLAT_DEPTH:g} flat.",
         fontsize=6.3, color=INK, ha="left", va="center", linespacing=1.3)

# (b) hinge sector gear bolts --------------------------------------------------------------------
Sb = 1.1
axb = cell(1, 0, (-8.0, 59.4), (-7.5, 14.0), Sb, f"b   SECTOR GEAR BOLTS, 3 x M3 x {M3_BOLT_L:g}  ({Sb:g}:1)")
rect(axb, 0.0, -7.0, PL_T, 14.0, FILL["petg"], hatch=True, lw=0.6)                     # plate 7
rect(axb, PL_T, -6.0, SECTOR_T, 12.0, FILL["light"], hatch=True, lw=0.6)               # sector, say 3
rect(axb, -0.2, -1.7, PL_T + SECTOR_T + 0.4, 3.4, "white", lw=0)                        # 3.4 clearance hole
hex_nut(axb, PL_T + SECTOR_T, -2.75, M3_NUT, 5.5)                                       # M3 nut 2.4
rect(axb, PL_T + SECTOR_T, -1.5, M3_NUT, 3.0, "white", lw=0.4)                          # its empty bore
rect(axb, -3.0, -2.75, 3.0, 5.5, FILL["steel"], lw=0.6)                                 # cap head 3 x Ø5.5
rect(axb, 0.0, -1.5, M3_BOLT_L, 3.0, FILL["steel"], lw=0.6)                             # shank 10
centreline(axb, -7.0, 0, 13.5, 0)
THb = th(Sb)
dim_h(axb, 0, PL_T, 8.5, f"{PL_T:g}", ext_from=7.0, offset=0.2, fontsize=7)
dim_h(axb, PL_T, PL_T + SECTOR_T, 8.5, f"{SECTOR_T:g}", ext_from=6.0, offset=0.2, fontsize=7)
dim_h(axb, PL_T + SECTOR_T, PL_T + SECTOR_T + M3_NUT, 8.5, f"{M3_NUT:g}", ext_from=2.75, offset=THb + 0.5, fontsize=7)
dim_h(axb, 0, M3_BOLT_L, -4.2, f"{M3_BOLT_L:g} bolt", ext_from=-1.5, offset=-THb - 0.3, fontsize=7)
axb.text(19.5, 3.0, f"Plate {PL_T:g} + sector {SECTOR_T:g} + nut {M3_NUT:g} = {PL_T + SECTOR_T + M3_NUT:g};\nthe {M3_BOLT_L:g} bolt stands {M3_BOLT_L - PL_T - SECTOR_T - M3_NUT:g} proud.\n"
         f"The sector sits on the inboard\nface (z {Z_PLATE[0] - SECTOR_T:g}-{Z_PLATE[0]:g}): the box must\nstop at z {Z_PLATE[0] - SECTOR_T - 1:g} near the middle axle.",
         fontsize=6.3, color=INK, ha="left", va="center", linespacing=1.3)

# (c) cross bar ----------------------------------------------------------------------------------
Sc = 0.72
axc = cell(0, 1, (-13.0, 90.0), (-30.0, 18.0), Sc, f"c   CROSS BAR  ({Sc:g}:1)")
SPC_DRAWN = 30.0                                                                       # spacer drawn shortened, with a break
x_pl1, x_sp = END_F, END_F + PL_T
x_pl2 = x_sp + SPC_DRAWN
x_end2 = x_pl2 + PL_T
rod_L = x_end2 + END_F
rect(axc, 0.0, -R_AX / 2, rod_L, R_AX, FILL["steel"], lw=0.6)                                    # M4 rod
for xp in (x_pl1, x_pl2):
    rect(axc, xp, -13.0, PL_T, 26.0, FILL["petg"], hatch=True, lw=0.6)                           # plates (broken)
    rect(axc, xp - 0.2, -BAR_D / 2, PL_T + 0.4, BAR_D, "white", lw=0)
    rect(axc, xp, -R_AX / 2, PL_T, R_AX, FILL["steel"], lw=0)
    for yy in (-13.0, 13.0):
        rect(axc, xp - 0.3, yy - 1.0, PL_T + 0.6, 2.0, "white", lw=0)
        break_edge(axc, xp, xp + PL_T, yy, 0.8, n=2)
rect(axc, x_sp, -SPC_OD / 2, SPC_DRAWN, SPC_OD, FILL["petg"], hatch=True, lw=0.6)                # spacer
rect(axc, x_sp, -BAR_D / 2, SPC_DRAWN, BAR_D, "white", lw=0)
rect(axc, x_sp, -R_AX / 2, SPC_DRAWN, R_AX, FILL["steel"], lw=0)
xb = x_sp + SPC_DRAWN / 2
rect(axc, xb - 1.5, -SPC_OD / 2 - 0.3, 3.0, SPC_OD + 0.6, "white", lw=0)                          # the break
for yy in (-SPC_OD / 2, SPC_OD / 2):
    axc.plot([xb - 1.5, xb - 0.5, xb + 0.5, xb + 1.5], [yy, yy + 1.2, yy - 1.2, yy], color=INK, lw=0.6)
for dx in (-1.0, 1.0):
    axc.plot([xb + dx, xb + dx], [-SPC_OD / 2, SPC_OD / 2], color=INK, lw=0.4, ls=(0, (2, 2)))
for xw, s in ((x_pl1, -1), (x_end2, +1)):                                                       # washer + nut each end
    xw0 = xw - M4_WASHER if s < 0 else xw
    rect(axc, xw0, -M4_WASHER_D / 2, M4_WASHER, M4_WASHER_D, FILL["steel"], lw=0.5)
    xn0 = xw0 - M4_NUT if s < 0 else xw0 + M4_WASHER
    hex_nut(axc, xn0, -3.5, M4_NUT, 7.0)
centreline(axc, -2.0, 0, rod_L + 2.0, 0)
THc = th(Sc)
dim_h(axc, x_pl1, x_sp, 14.5, f"{PL_T:g}", ext_from=13.0, offset=0.2, fontsize=7)
dim_h(axc, x_sp, x_pl2, 7.5, f"{SPC_F:g} spacer (rear {SPC_R:g})", ext_from=SPC_OD / 2, offset=0.2, fontsize=7)
dim_h(axc, x_pl2, x_end2, 14.5, f"{PL_T:g}", ext_from=13.0, offset=0.2, fontsize=7)
dim_h(axc, 0, x_pl1, -9.5, f"{END_F:g}", ext_from=-3.5, offset=-THc - 0.3, fontsize=7)
dim_h(axc, x_end2, rod_L, -9.5, f"{END_F:g}", ext_from=-3.5, offset=-THc - 0.3, fontsize=7)
dim_h(axc, 0, rod_L, -15.0, f"{ROD_F:g} rod (rear {ROD_R:g}), drawn broken", offset=-THc - 0.3, fontsize=7)
axc.text(-12.0, -21.0, f"front rod {ROD_F:g} = plate {PL_T:g} + spacer {SPC_F:g} + plate {PL_T:g} + 2 x {END_F:g} ends",
         fontsize=6.3, color=INK, ha="left", va="center")
axc.text(-12.0, -24.4, f"rear rod {ROD_R:g} = {PL_T:g} + {SPC_R:g} + {PL_T:g} + 2 x {END_F:g}  (spacer = plate to plate)",
         fontsize=6.3, color=INK, ha="left", va="center")
axc.text(-12.0, -27.8, f"each end {END_F:g} = washer {M4_WASHER:g} + nut {M4_NUT:g} + {END_F - M4_WASHER - M4_NUT:g} of rod proud  (DIN sizes)",
         fontsize=6.3, color=INK, ha="left", va="center")

# (d) bearing press ------------------------------------------------------------------------------
Sd = 0.8
axd = cell(1, 1, (-20.0, 73.0), (-18.0, 20.5), Sd, f"d   BEARING PRESS, 608ZZ  ({Sd:g}:1)")
rect(axd, 0.0, -16.0, PL_T, 32.0, FILL["petg"], hatch=True, lw=0.6)                               # plate (broken)
rect(axd, -0.2, -POCKET_D / 2, PL_T + 0.4, POCKET_D, "white", lw=0)
axd.plot([0, PL_T], [POCKET_D / 2] * 2, color=INK, lw=0.5)
axd.plot([0, PL_T], [-POCKET_D / 2] * 2, color=INK, lw=0.5)
for yy in (-16.0, 16.0):
    rect(axd, -0.3, yy - 1.0, PL_T + 0.6, 2.0, "white", lw=0)
    break_edge(axd, 0.0, PL_T, yy, 0.8, n=2)
XB = -16.0                                                                                        # bearing, pulled out to the left
for s in (+1, -1):
    rect(axd, XB, min(s * R_AX, s * R_BR), BR_W, R_BR - R_AX, FILL["bearing"], hatch=True, lw=0.6)
    axd.add_patch(Circle((XB + BR_W / 2, s * (R_AX + R_BR) / 2), 1.7, fc="white", ec=INK, lw=0.5, zorder=3))
rect(axd, XB, -R_AX, BR_W, 2 * R_AX, "white", lw=0.5)
centreline(axd, -19.5, 0, PL_T + 4.0, 0)
axd.annotate("", xy=(-1.0, 0.0), xytext=(XB + BR_W + 1.0, 0.0), arrowprops=dict(arrowstyle="-|>", lw=0.9, color=INK, mutation_scale=9))
dim_h(axd, XB, XB + BR_W, R_BR + 2.5, f"{BR_W:g}", ext_from=R_BR, offset=0.2, fontsize=7)
dim_h(axd, 0, PL_T, 16.0 + 1.5, f"{PL_T:g}", ext_from=16.0, offset=0.2, fontsize=7)
dim_v(axd, -R_BR, R_BR, XB - 3.0, f"Ø{BR_OD:g}", ext_from=XB, fontsize=7)
dim_v(axd, -POCKET_D / 2, POCKET_D / 2, PL_T + 3.5, f"Ø{POCKET_D:g}", ext_from=PL_T, fontsize=7)
axd.text(PL_T + 9.0, 19.5, f"Pocket {POCKET_DEPTH:g} deep = plate {PL_T:g} = bearing {BR_W:g}:\nflush both faces, through pocket.",
         fontsize=6.3, color=INK, ha="left", va="top", linespacing=1.3)
axd.text(PL_T + 9.0, 9.5, f"Pocket modelled Ø{POCKET_D:g} for the Ø{BR_OD:g}\nbearing: {POCKET_D - BR_OD:.1f} is print allowance for\n"
         "a light press fit. Measure the first\nprint; ream if tight, glue if loose.",
         fontsize=6.3, color=INK, ha="left", va="top", linespacing=1.3)
axd.text(PL_T + 9.0, -7.0, f"{BOSS_R - R_BR - 0.1:.1f} mm wall all round the pocket\n(R{BOSS_R:g} boss). Press with the plate\nsupported on a block.",
         fontsize=6.3, color=INK, ha="left", va="top", linespacing=1.3)

# =============================================================================================
# (4) KEY and notes
# =============================================================================================
KX = [6.32, 6.56, 8.02, 8.50]      # No, Part, Qty, Make/buy + material/process (inches)
KY_TOP = 7.22
rows = [
    ("No", "Part", "Qty*", "Make or buy; material, process"),
    ("1", "Track", f"{TR['qty_per_segment']} / {TR['qty_total']}", "Print, TPU 95A, upright ring, 100 % infill"),
    ("2", "Pulley HTD 5M 20T", f"{PU['qty_per_segment']} / {PU['qty_total']}", "Buy (MISUMI): 15 belt, Ø8 bore, flanged, set screw"),
    ("3", "Bearing 608ZZ, 8 x 22 x 7", f"{BR['qty_per_segment']} / {BR['qty_total']}", "Buy; 8 in the plates, 2 on the hinge shaft"),
    ("4", "Side plate with rail", f"{SP['qty_total'] // 2} / {SP['qty_total']}", "Print, PETG, plate face down, 4 walls, 30 %"),
    ("5", f"Middle axle Ø8 x {AX_MID:g}", "1 / 1", "Buy, Ø8 h7 rod; shared with the rear segment"),
    ("6", f"Front axle Ø8 x {AX_FRONT:g}", "1 / 1", f"Buy, Ø8 h7 rod (ends at z {AX_FRONT / 2:g}; hubs end at {Z_HUB[1]:g})"),
    ("7", "Cross bar, M4 rod + spacer", f"{CB['qty_per_segment']} / {CB['qty_total']}",
     f"Buy M4 rod {ROD_F:g} (rear {ROD_R:g}) + nuts, washers;\nprint spacer PETG Ø{SPC_OD:g} x {SPC_F:g} (rear {SPC_R:g})"),
    ("8", "Fasteners", "-", f"Buy: set screws (with the pulleys), 8 M4 nuts,\n8 M4 washers, 6 x M3 x {M3_BOLT_L:g}, 4 x M4 x 12"),
]
y = KY_TOP
for i, r in enumerate(rows):
    header = i == 0
    y -= 0.185 if i < 7 else 0.27
    for xk, t in zip(KX, r):
        text_in(xk, y, t, fontsize=7.2, va="center", fontweight="bold" if header else "normal", linespacing=1.25)
    if i < 8:
        yl = y - 0.09 if i < 7 else y - 0.135
        fig.add_artist(Line2D([KX[0], 11.35], [yl, yl], color=INK if header else "#c9ced3", lw=0.6 if header else 0.4, transform=fig.dpi_scale_trans))
y_bot = y - 0.135
fig.add_artist(Line2D([KX[0], 11.35], [y_bot, y_bot], color=INK, lw=0.6, transform=fig.dpi_scale_trans))
text_in(KX[0], y_bot - 0.07, "* per segment / total for both segments", fontsize=6.3, color=MUTED, va="center")

notes = [
    f"REAR SEGMENT: mirror image, plates outboard at",
    f"z {Z_RPLATE[0]:g}-{Z_RPLATE[1]:g}, rail under the lane at z {Z_RLANE[0]:g}-{Z_RLANE[1]:g} (its web",
    f"bridges under the hub). Rear axle {AX_MID:g}, front {AX_FRONT:g}.",
    "",
    "All numbers from assembly/parts_spec.json (mm, 1:5).",
    f"Derived: pulley {OVER_FL:g} over flanges, {PU_OAL:g} overall, so",
    f"flanges at z {Z_PUL[0]:g}-{Z_PUL[1]:g} with the hub at {Z_HUB[0]:g}-{Z_HUB[1]:g}; plate {PL_LEN:g}",
    f"= 225 + 2 x R20; web {RAIL_Z0 - Z_PLATE[0]:g} = plate 7 + gap 1 + 1 (rail centred);",
    f"web bottom {RAIL_BOT:g} = {RAIL_TOP:g} + {RAIL_T:g}; sector holes Ø{SECT_D:g} on R{SECT_R:g}",
    f"at {SECT_ANG[0]:g}, {SECT_ANG[1]:g}, {SECT_ANG[2]:g} deg; nut and washer sizes DIN.",
    "Hatched = cut.",
    "Bought parts drawn at the stand-in's sizes; the",
    "vendor's drawing overrides them.",
]
text_in(8.50, 5.05, "\n".join(notes), fontsize=6.8, va="top", ha="left", linespacing=1.4,
        bbox=dict(boxstyle="square,pad=0.5", fc=FILL["light"], ec="none"))

save(fig, "exploded_segment")
