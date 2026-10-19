"""CAD-style A3 engineering sheets (TS-00 assembly with balloons and parts list, TS-01..TS-07 one per part).
Monochrome, true scale, third angle. Every number from ../parts_spec.json (v2). Run: python3 eng_sheets.py"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from drawing import DIM, INK, SPEC, centreline, dim_dia, dim_h, dim_v, leader  # noqa: E402
from drawing import circle as _circle, rect as _rect  # noqa: E402
from eng_sheet import a3_sheet, balloon, parts_list, save, section_mark  # noqa: E402
from matplotlib.patches import PathPatch, Polygon, Rectangle, RegularPolygon  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402
from shapely import affinity  # noqa: E402
from shapely.geometry import Point, Polygon as SPoly, box as sbox  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

P, Z, SEG = SPEC["parts"], SPEC["layout_decision"]["z_stations_one_side_mm"], SPEC["segment"]
TR, PU, AX, BR, SP, CB = P["track"], P["pulley"], P["axle"], P["bearing"], P["side_plate"], P["cross_bar"]
C = SEG["axle_to_axle_mm"]                                   # 225
R_FACE, R_TIP = SEG["axle_to_track_face_mm"], SEG["axle_to_cleat_tip_mm"]   # 16.74, 19.74
R_TOOTH = R_FACE - TR["backing_thickness_mm"] - TR["teeth"]["height_mm"]      # 13.34 tooth tips (lower run rides on the rail)
R_PITCH = PU["pitch_dia_mm"] / 2                             # 15.915 belt pitch line
T, BELOW, ABOVE = SP["plate"]["thickness_mm"], SP["plate"]["bottom_edge_below_axle_mm"], SP["plate"]["top_edge_above_axle_mm"]
END_R, BOSS_R, ARC_CY = 20.0, SP["plate"]["boss_radius_mm"], (SP["plate"]["top_edge_above_axle_mm"] - SP["plate"]["bottom_edge_below_axle_mm"]) / 2
POCKET = SP["bearing_pockets"]["dia_mm"]
RL = SP["rail"]
RX0, RX1, RW, RT, RTOP, RBOT = RL["from_x_mm"], RL["to_x_mm"], RL["width_mm"], RL["thickness_mm"], RL["top_face_below_axle_mm"], RL["bottom_below_axle_mm"]
CBH, SB = SP["cross_bar_holes"], SP["sector_bolts"]
FL_T, FL_R, HUB_R, HUB_L = PU["flange_thickness_mm"], PU["flange_dia_mm"] / 2, PU["hub_dia_mm"] / 2, PU["hub_length_mm"]
PU_OD_R, PU_FACE = PU["outside_dia_mm"] / 2, PU["face_width_between_flanges_mm"]
TRK_W = TR["width_mm"]
HIDDEN = dict(color=INK, lw=0.5, ls=(0, (4, 2)))


def rect(ax, x, y, w, h, fill="white", lw=0.8, hatch=False, zorder=2):
    p = _rect(ax, x, y, w, h, fill, lw=lw, hatch=hatch)
    p.set_zorder(zorder)
    return p


def circle(ax, cx, cy, r, fill="none", lw=0.8, ls="-", zorder=2):
    p = _circle(ax, cx, cy, r, fill=fill, lw=lw, ls=ls)
    p.set_zorder(zorder)
    return p


def lane_bands(lane):
    """(flange1, belt, flange2) z bands of a pulley lane: the belt is centred between the flanges."""
    z0, z1 = lane
    bc = (z0 + z1) / 2
    return (z0, z0 + FL_T), (bc - TRK_W / 2, bc + TRK_W / 2), (z1 - FL_T, z1)


def shape_patch(ax, shape, fc="white", lw=0.8, hatch=None, zorder=2):
    polys = list(shape.geoms) if shape.geom_type == "MultiPolygon" else [shape]
    verts, codes = [], []
    for p in polys:
        for ring in [p.exterior] + list(p.interiors):
            pts = list(ring.coords)
            verts += pts
            codes += [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 2) + [MPath.CLOSEPOLY]
    patch = PathPatch(MPath(verts, codes), fc=fc, ec=INK, lw=lw, hatch=hatch, zorder=zorder)
    ax.add_patch(patch)
    return patch


def stadium(R, x0=0.0, x1=C):
    return unary_union([sbox(x0, -R, x1, R), Point(x0, 0).buffer(R, quad_segs=64), Point(x1, 0).buffer(R, quad_segs=64)])


def plate_shape():
    return unary_union([sbox(0, -BELOW, C, ABOVE), Point(0, ARC_CY).buffer(END_R, quad_segs=64), Point(C, ARC_CY).buffer(END_R, quad_segs=64),
                        Point(0, 0).buffer(BOSS_R, quad_segs=64), Point(C, 0).buffer(BOSS_R, quad_segs=64)])


def hidden_rect(ax, x, y, w, h):
    ax.add_patch(Polygon([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], closed=True, fc="none", ec=INK, lw=0.5, ls=(0, (4, 2))))


def hidden_circle(ax, cx, cy, r):
    circle(ax, cx, cy, r, fill="none", lw=0.5, ls=(0, (4, 2)))


def centre_mark(ax, cx, cy, L):
    centreline(ax, cx - L, cy, cx + L, cy)
    centreline(ax, cx, cy - L, cx, cy + L)


def hex_nut(ax, cx, cy, af=7.0):
    ax.add_patch(RegularPolygon((cx, cy), numVertices=6, radius=af / math.sqrt(3), orientation=math.pi / 6, fc="white", ec=INK, lw=0.6, zorder=5))


def loop_point(s):
    """Point and outward normal on the belt pitch line, s along the loop from the top of the rear axle, forward."""
    Rp = R_PITCH
    arc = math.pi * Rp
    if s < C:
        return (s, Rp), (0.0, 1.0)
    if s < C + arc:
        a = math.pi / 2 - (s - C) / Rp
        return (C + Rp * math.cos(a), Rp * math.sin(a)), (math.cos(a), math.sin(a))
    if s < 2 * C + arc:
        return (C - (s - C - arc), -Rp), (0.0, -1.0)
    a = -math.pi / 2 - (s - 2 * C - arc) / Rp
    return (Rp * math.cos(a), Rp * math.sin(a)), (math.cos(a), math.sin(a))


def track_side(ax, zorder=3):
    """The track seen from the side: belt band (tooth tips to belt face) and 45 cleats."""
    shape_patch(ax, stadium(R_FACE).difference(stadium(R_TOOTH)), zorder=zorder)
    cl = TR["cleats"]
    hb, ht, hh = cl["base_width_mm"] / 2, cl["tip_width_mm"] / 2, cl["height_mm"]
    for k in range(cl["count"]):
        (px, py), (nx, ny) = loop_point(k * cl["pitch_mm"])
        tx, ty = -ny, nx
        b = R_FACE - R_PITCH
        pts = [(px + nx * b + tx * hb, py + ny * b + ty * hb), (px + nx * b - tx * hb, py + ny * b - ty * hb),
               (px + nx * (b + hh) - tx * ht, py + ny * (b + hh) - ty * ht), (px + nx * (b + hh) + tx * ht, py + ny * (b + hh) + ty * ht)]
        ax.add_patch(Polygon(pts, closed=True, fc="white", ec=INK, lw=0.5, zorder=zorder))


# ------------------------------------------------------------------ TS-00 assembly
def sheet_assembly():
    fig, view, bg = a3_sheet("FRONT TRACK SEGMENT ASSEMBLY", "TS-00", material="SEE PARTS LIST", qty="1 (REAR SIMILAR)", scale="1:2", notes=[
        "REAR SEGMENT: SAME, WITH ITS PLATES OUTBOARD (Z 105-112, TS-03), RAILS INBOARD, AND THE REAR AXLE (TS-04) INSTEAD OF THE FRONT AXLE.",
        "BOTH SEGMENTS SHARE THE MIDDLE AXLE (ITEM 4), TURNED BY THE DRIVE MOTOR. PULLEYS ARE SET-SCREWED TO THE AXLES; THE AXLES TURN IN ITEM 6.",
        "HINGE SECTOR GEAR (3 THICK, Z 38-41, NOT SHOWN) BOLTS TO THE INBOARD FACE OF EACH FRONT PLATE WITH ITEM 9. THE BOX STOPS AT Z 37 THERE.",
        "THE BOX (TEAM'S) MUST END BEFORE X 50 SO THE FRONT CROSS BAR AT X 60 CLEARS IT WHEN THE HINGE BENDS. MM AT 1:5; X 5 FOR FULL SIZE.",
    ])
    S = 0.5
    rows = [
        (1, "TS-01 TRACK", "TRACK, TPU 95A, 110T HTD 5M, 45 CLEATS", 2),
        (2, "TS-06 PULLEY_20T", "PULLEY HTD 5M 20T, 15 MM BELT, BORE 8, BOUGHT", 4),
        (3, "TS-02 SIDE_PLATE_FRONT", "SIDE PLATE, FRONT SEGMENT, PETG, 1 L + 1 R", 2),
        (4, "TS-04 AXLE_MIDDLE", "MIDDLE AXLE, ROD 8 x 230, SHARED W/ REAR SEG", 1),
        (5, "TS-04 AXLE_FRONT", "FRONT AXLE, ROD 8 x 160", 1),
        (6, "TS-07 BEARING_608ZZ", "BALL BEARING 608ZZ, 8 x 22 x 7, BOUGHT", 4),
        (7, "TS-05 SPACER_82", "SPACER OD 10 x 82, BORE 4.5, PETG", 2),
        (8, "M4_ROD_110", "M4 THREADED ROD x 110 + 2 NUTS + 2 WASHERS", 2),
        (9, "M3x14", "M3 x 14 BOLT + NUT, HINGE SECTOR GEAR, BOUGHT", 6),
    ]
    parts_list(bg, rows)
    fz1, fzb, fz2 = lane_bands(Z["front_lane"])
    pz0, pz1 = Z["front_plate"]
    hz0, hz1 = Z["front_hub"]
    rail_z = ((Z["front_lane"][0] + Z["front_lane"][1]) / 2 - RW / 2, (Z["front_lane"][0] + Z["front_lane"][1]) / 2 + RW / 2)
    half_mid, half_front = AX["lengths_mm"]["middle"] / 2, AX["lengths_mm"]["front"] / 2
    rod, spc = CB["front_segment"]["rod_length_mm"] / 2, CB["front_segment"]["spacer_length_mm"] / 2
    od = CB["front_segment"]["spacer_od_mm"]

    # ---- TOP VIEW (x along the segment, z across)
    ax = view(22, 125, (-70, 290), (-130, 130), S, "TOP VIEW")
    for sd in (1, -1):
        rect(ax, RX0, sd * pz0 if sd > 0 else -rail_z[1], RX1 - RX0, rail_z[1] - pz0, "white", lw=0.6)      # web + rail
        rect(ax, -END_R, sd * pz0 if sd > 0 else -pz1, C + 2 * END_R, T, "white")                           # plate
        for x in (0, C):
            for z0, z1 in (fz1, fz2):
                rect(ax, x - FL_R, sd * z0 if sd > 0 else -z1, 2 * FL_R, FL_T, "white", lw=0.6)             # flanges
            rect(ax, x - HUB_R, sd * hz0 if sd > 0 else -hz1, 2 * HUB_R, hz1 - hz0, "white", lw=0.6)         # hub
        rect(ax, -R_TIP, sd * fzb[0] if sd > 0 else -fzb[1], C + 2 * R_TIP, TRK_W, "white", zorder=3)       # track
        for k in range(int(C / TR["cleats"]["pitch_mm"]) + 1):
            x = k * TR["cleats"]["pitch_mm"]
            ax.plot([x, x], [sd * fzb[0], sd * fzb[1]], color=INK, lw=0.4, zorder=4)
        hidden_rect(ax, -25, sd * 38 if sd > 0 else -41, 50, 3)                                             # sector gear (ref)
    for x in CBH["at_x_mm"]:
        rect(ax, x - od / 2, -spc, od, 2 * spc, "white", lw=0.6, zorder=4)                                  # spacer
        rect(ax, x - 2, -rod, 4, 2 * rod, "white", lw=0.6, zorder=3)                                        # M4 rod
        for sd in (1, -1):
            rect(ax, x - 3.5, sd * pz1 if sd > 0 else -(pz1 + 3.2), 7, 3.2, "white", lw=0.6, zorder=5)      # nut
    rect(ax, -4, -half_mid, 8, 2 * half_mid, "white", lw=0.6, zorder=3)                                     # middle axle
    rect(ax, C - 4, -half_front, 8, 2 * half_front, "white", lw=0.6, zorder=3)                              # front axle
    hidden_rect(ax, -60, -40, 100, 80)
    ax.text(-10, 0, "BOX (REF), Z 0-40", fontsize=6.5, ha="center", va="center")
    centreline(ax, -60, 0, C + 45, 0)
    for x in (0, C):
        centreline(ax, x, -125, x, 125)
    dim_h(ax, 0, C, -124, "225", ext_from=-118)
    dim_v(ax, -half_mid, half_mid, -42, "230", ext_from=-4)
    dim_v(ax, -half_front, half_front, 252, "160", ext_from=C + 4)
    dim_v(ax, -fzb[1], fzb[1], 266, "194 OVER TRACKS", ext_from=C + 20)
    dim_v(ax, -pz1, pz1, 282, "224 OVER PLATES", ext_from=C + 20)
    dim_h(ax, CBH["at_x_mm"][0], CBH["at_x_mm"][1], 118, "140", ext_from=rod + 2)
    balloon(ax, (120, -fzb[1] + 2), (140, -103), 1)
    balloon(ax, (0, hz0 + 3), (-40, 100), 2)
    balloon(ax, (160, pz0 + 3), (175, 100), 3)
    balloon(ax, (0, -100), (-40, -110), 4)
    balloon(ax, (C, -70), (255, -100), 5)
    balloon(ax, (60, -20), (40, -105), 7)
    balloon(ax, (200, -(pz1 + 1.6)), (190, -108), 8)

    # ---- SIDE VIEW (from outboard)
    ax = view(22, 48, (-70, 290), (-50, 90), S, "SIDE VIEW (FROM OUTBOARD)")
    shape_patch(ax, plate_shape(), zorder=1)
    hidden_rect(ax, RX0, -RBOT, RX1 - RX0, RBOT - BELOW)
    track_side(ax, zorder=3)
    for x in (0, C):
        circle(ax, x, 0, FL_R, fill="white", lw=0.6).set_zorder(4)
        circle(ax, x, 0, HUB_R, fill="white", lw=0.6).set_zorder(5)
        circle(ax, x, 0, 4, fill="white", lw=0.6).set_zorder(6)
        hidden_circle(ax, x, 0, BR["outside_dia_mm"] / 2)
        centre_mark(ax, x, 0, 26)
    for x in CBH["at_x_mm"]:
        hex_nut(ax, x, CBH["above_axle_mm"])
        circle(ax, x, CBH["above_axle_mm"], 2, fill="white", lw=0.5).set_zorder(6)
    for a in SB["angles_deg"]:
        hidden_circle(ax, SB["radius_mm"] * math.cos(math.radians(a)), SB["radius_mm"] * math.sin(math.radians(a)), SB["dia_mm"] / 2)
    centreline(ax, -40, 0, C + 40, 0)
    dim_h(ax, 0, C, -34, "225", ext_from=-22)
    dim_h(ax, -R_TIP, C + R_TIP, -44, f"{SEG['length_over_cleats_mm']:g} OVER CLEATS", ext_from=-22)
    dim_v(ax, -R_TIP, R_TIP, 262, f"{SEG['height_over_cleats_mm']:g}", ext_from=C + 22)
    dim_v(ax, 0, ABOVE, 276, "33", ext_from=C + 22)
    dim_v(ax, 0, CBH["above_axle_mm"], -38, "28", ext_from=-22)
    balloon(ax, (C - 11, 0), (255, 60), 6)
    balloon(ax, (0, SB["radius_mm"]), (-40, 60), 9)

    # ---- END VIEW (from the front, looking along the axle)
    ax = view(232, 75, (-140, 140), (-55, 85), S, "END VIEW (FROM THE FRONT)")
    for sd in (1, -1):
        m = (lambda z0, z1: (z0, z1)) if sd > 0 else (lambda z0, z1: (-z1, -z0))
        z = m(pz0, pz1)
        rect(ax, z[0], -BOSS_R, T, BOSS_R + ABOVE, "white")                                                  # plate with boss
        z = m(pz0, rail_z[0])
        rect(ax, z[0], -RBOT, z[1] - z[0], RBOT - BELOW, "white", lw=0.6)                                   # web
        z = m(*rail_z)
        rect(ax, z[0], -RBOT, RW, RT, "white", lw=0.6)                                                      # rail
        z = m(fz1[1], fz2[0])
        rect(ax, z[0], -PU_OD_R, z[1] - z[0], 2 * PU_OD_R, "white", lw=0.6)                                 # pulley body
        for b in (fz1, fz2):
            z = m(*b)
            rect(ax, z[0], -FL_R, FL_T, 2 * FL_R, "white", lw=0.6)                                          # flanges
        z = m(hz0, hz1)
        rect(ax, z[0], -HUB_R, hz1 - hz0, 2 * HUB_R, "white", lw=0.6)                                       # hub
        z = m(*fzb)
        rect(ax, z[0], -R_TIP, TRK_W, 2 * R_TIP, "white", zorder=3)                                         # track
        z = m(pz1, pz1 + 3.2)
        rect(ax, z[0], CBH["above_axle_mm"] - 3.5, 3.2, 7, "white", lw=0.6, zorder=5)                       # nut
    rect(ax, -spc, CBH["above_axle_mm"] - od / 2, 2 * spc, od, "white", lw=0.6, zorder=4)                   # spacer
    rect(ax, -rod, CBH["above_axle_mm"] - 2, 2 * rod, 4, "white", lw=0.6, zorder=3)                         # rod
    rect(ax, -half_front, -4, 2 * half_front, 8, "white", lw=0.6, zorder=3)                                 # front axle
    hidden_rect(ax, -40, 2, 80, 20)
    ax.text(0, 12, "BOX ENVELOPE (REF), Z 0-40", fontsize=6, ha="center", va="center")
    centreline(ax, -130, 0, 130, 0)
    centreline(ax, 0, -30, 0, 75)
    dim_h(ax, -fzb[1], fzb[1], -30, "194 OVER TRACKS", ext_from=-R_TIP)
    dim_h(ax, -pz1, pz1, -40, "224 OVER PLATES", ext_from=-BOSS_R)
    dim_h(ax, -half_front, half_front, -50, "160", ext_from=-4)
    dim_h(ax, -rod, rod, 42, "110 ROD", ext_from=CBH["above_axle_mm"] + 2)
    dim_h(ax, -spc, spc, 50, "82 SPACER", ext_from=CBH["above_axle_mm"] + 2)
    dim_v(ax, -R_TIP, R_TIP, 96, f"{SEG['height_over_cleats_mm']:g}", ext_from=fzb[1])
    dim_v(ax, 0, CBH["above_axle_mm"], 110, "28", ext_from=pz1 + 3.2)
    dim_v(ax, -RBOT, -RTOP, 84, "4", ext_from=rail_z[1], offset=0)
    save(fig, "TS-00_assembly_front_segment")


# ------------------------------------------------------------------ TS-01 track
def tooth(x=0.0):
    r = TR["teeth"]["tip_radius_mm"]
    return unary_union([sbox(x - r, -(TR["teeth"]["height_mm"] - r), x + r, 0.3), Point(x, -(TR["teeth"]["height_mm"] - r)).buffer(r, quad_segs=24)])


def cleat(x=0.0, y0=0.0):
    cl = TR["cleats"]
    hb, ht = cl["base_width_mm"] / 2, cl["tip_width_mm"] / 2
    return SPoly([(x - hb, y0 - 0.3), (x + hb, y0 - 0.3), (x + ht, y0 + cl["height_mm"]), (x - ht, y0 + cl["height_mm"])])


def sheet_track():
    ring = TR["as_printed_ring"]
    r_od, r_root = ring["outside_dia_of_belt_mm"] / 2, ring["outside_dia_of_belt_mm"] / 2 - TR["backing_thickness_mm"]
    fig, view, bg = a3_sheet("TRACK, 110T HTD 5M, 45 CLEATS", "TS-01", material="TPU 95A, 3D PRINTED", finish="AS PRINTED", qty=4, scale="1:1, DETAIL 4:1", notes=[
        "FILE stl/track_TPU_x4.stl. PRINT STANDING AS A RING, NO SUPPORTS, 0.2 LAYERS, 100% INFILL, 20-30 MM/S, DIRECT-DRIVE EXTRUDER.",
        f"LOOP {TR['loop_length_mm']:g} ON THE PITCH LINE = 110 TEETH x 5 PITCH; RUNS ON TWO HTD 5M 20T PULLEYS (TS-06) AT 225 CENTRES. ABOUT 32 G.",
        "45 CLEATS AT 12.222 PITCH: 5 CLEATS = 61.11, ONE ES1 STEP ALONG THE SLOPE (35 x 50 AT 1:5), SO EVERY STEP EDGE SITS BETWEEN TWO CLEATS.",
        "BED SMALLER THAN 190 MM: ASK FOR THE TWO-PIECE TRACK. PRINT THE 5 MM FIT-TEST SLICE FIRST (stl/fit_test_track_5mm_TPU.stl).",
    ])
    # front view, 1:1
    ax = view(22, 62, (-104, 104), (-100, 108), 1.0, "FRONT VIEW")
    belt = Point(0, 0).buffer(r_od, quad_segs=180).difference(Point(0, 0).buffer(r_root, quad_segs=180))
    parts = [belt]
    for k in range(TR["teeth"]["count"]):
        a = 360.0 * k / TR["teeth"]["count"]
        parts.append(affinity.rotate(affinity.translate(tooth(), 0, r_root), a - 90, origin=(0, 0)))
    for k in range(TR["cleats"]["count"]):
        a = 360.0 * k / TR["cleats"]["count"]
        parts.append(affinity.rotate(affinity.translate(cleat(), 0, r_od), a - 90, origin=(0, 0)))
    shape_patch(ax, unary_union(parts))
    centre_mark(ax, 0, 0, 100)
    dim_dia(ax, 0, 0, ring["outside_dia_over_cleats_mm"] / 2, 62, f"Ø{ring['outside_dia_over_cleats_mm']:g} OVER CLEATS", length=104)
    dim_dia(ax, 0, 0, r_od, 47, f"Ø{ring['outside_dia_of_belt_mm']:g} BELT FACE", length=104)
    dim_dia(ax, 0, 0, ring["inside_dia_over_tooth_tips_mm"] / 2, 30, f"Ø{ring['inside_dia_over_tooth_tips_mm']:g} INSIDE", length=104)
    leader(ax, (-r_od - 1.5, 0), (-100, -60), "45 CLEATS\n12.222 PITCH\n(8°)")
    leader(ax, (-(r_root - 2) * math.cos(math.radians(20)), -(r_root - 2) * math.sin(math.radians(20))), (-60, -98), "110 TEETH HTD 5M, 5 PITCH\n(PD Ø175.1)")
    # edge view, 1:1 (third angle: to the right)
    ax = view(232, 62, (-14, 30), (-100, 108), 1.0, "EDGE VIEW")
    rect(ax, -TRK_W / 2, -ring["outside_dia_over_cleats_mm"] / 2, TRK_W, ring["outside_dia_over_cleats_mm"], "white")
    for y in (r_od, -r_od):
        ax.plot([-TRK_W / 2, TRK_W / 2], [y, y], color=INK, lw=0.5)
    centreline(ax, 0, -98, 0, 98)
    dim_h(ax, -TRK_W / 2, TRK_W / 2, 98, f"{TRK_W:g}", ext_from=ring["outside_dia_over_cleats_mm"] / 2)
    # section detail, belt straightened, 4:1
    S = 4.0
    ax = view(284, 180, (-4, 23), (-5.5, 8), S, "DETAIL: BELT SECTION, STRAIGHTENED (4:1)")
    tp, cp = TR["teeth"]["pitch_mm"], TR["cleats"]["pitch_mm"]
    sec = [sbox(0, 0, 20, TR["backing_thickness_mm"])] + [tooth(2.5 + i * tp) for i in range(4)] + [cleat(5.0, TR["backing_thickness_mm"]), cleat(5.0 + cp, TR["backing_thickness_mm"])]
    shape_patch(ax, unary_union(sec).intersection(sbox(0, -5, 20, 6)), hatch="////")
    bk, th, ch = TR["backing_thickness_mm"], TR["teeth"]["height_mm"], TR["cleats"]["height_mm"]
    dim_h(ax, 2.5, 2.5 + tp, -3.6, f"{tp:g}", ext_from=-th, fontsize=7)
    dim_h(ax, 5.0, 5.0 + cp, bk + ch + 1.2, f"{cp:g}", ext_from=bk + ch, fontsize=7)
    dim_v(ax, -th, 0, 21.2, f"{th:g}", ext_from=20, fontsize=7)
    dim_v(ax, 0, bk, 21.2, f"{bk:g}", ext_from=20, fontsize=7)
    dim_v(ax, -th, bk + ch, 22.6, f"{TR['total_thickness_mm']:g}", ext_from=20, fontsize=7)
    dim_v(ax, bk, bk + ch, -1.2, f"{ch:g}", ext_from=2.8, fontsize=7)
    dim_h(ax, 5.0 + cp - 2.2, 5.0 + cp + 2.2, -3.6, f"{TR['cleats']['base_width_mm']:g}", ext_from=bk, fontsize=7)
    dim_h(ax, 5.0 - 1.2, 5.0 + 1.2, bk + ch + 0.3, f"{TR['cleats']['tip_width_mm']:g}", fontsize=7)
    leader(ax, (2.5 - 1.45, -0.4), (-3.5, -4.7), f"ROOT {TR['teeth']['root_width_mm']:g} WIDE, TIP R{TR['teeth']['tip_radius_mm']:g}", fontsize=7)
    leader(ax, (5.0 + cp + 1.2, bk + ch), (18, 6.8), f"TIP R{TR['cleats']['tip_round_mm']:g}, ROOT R{TR['cleats']['root_fillet_mm']:g}", fontsize=7)
    ax.text(10, 7.6, "OUTSIDE (CLEATS)", fontsize=6.5, ha="center", va="bottom")
    ax.text(21, -5.4, "INSIDE (TEETH, ON THE PULLEY)", fontsize=6.5, ha="right", va="bottom")
    save(fig, "TS-01_track")


# ------------------------------------------------------------------ TS-01B bought track belt (Rev B B10)
B_PITCH, B_BACK, B_TIP = R_PITCH, 17.1, 13.3          # belt pitch line, back face and tooth-tip radii on the 20T wheel (back 3.8 thick)
B_T, B_TOOTH_H, B_W = 3.8, 2.06, 15.0                  # HTD 5M belt: total thickness, tooth height, width
CL_L, CL_H, CL_W, CL_PITCH, CL_N = 10.0, 5.0, 15.0, 25.0, 22   # cleats 10 along the belt x 5 high (cut down from 7.9, Nhien 19 Oct) x 15 wide, every 5th tooth


def belt_side(ax, zorder=3):
    """The bought belt on its two wheels, seen from the side: belt band and 22 bonded cleats."""
    shape_patch(ax, stadium(B_BACK).difference(stadium(B_TIP)), zorder=zorder)
    b = B_BACK - B_PITCH
    for k in range(CL_N):
        (px, py), (nx, ny) = loop_point(k * CL_PITCH + 12.5)
        tx, ty = -ny, nx
        h = CL_L / 2
        pts = [(px + nx * b + tx * h, py + ny * b + ty * h), (px + nx * b - tx * h, py + ny * b - ty * h),
               (px + nx * (b + CL_H) - tx * h, py + ny * (b + CL_H) - ty * h), (px + nx * (b + CL_H) + tx * h, py + ny * (b + CL_H) + ty * h)]
        ax.add_patch(Polygon(pts, closed=True, fc="white", ec=INK, lw=0.5, zorder=zorder))


def sheet_belt():
    fig, view, bg = a3_sheet("TRACK BELT, BOUGHT: HTD 550-5M-15 + 22 CLEATS", "TS-01B", material="NEOPRENE HTD BELT, RUBBER CLEATS", finish="AS BOUGHT, CLEATS BONDED", qty=4, scale="1:1, DETAILS 4:1 / 2:1", notes=[
        "BELT: HTD 5M, 550 PITCH LENGTH (110 TEETH), 15 WIDE, E.G. SKF PHG 550-5M-15 (RS SG 058-6535). RUNS ON TWO HTD 5M 20T PULLEYS (TS-06) AT 225 CENTRES.",
        f"CLEATS: {CL_N} PER BELT, RUBBER {CL_L:g} x {CL_H:g} x {CL_W:g}, ONE EVERY 5TH TOOTH ({CL_PITCH:g} PITCH), BONDED ON THE BELT BACK BY THE BELT SHOP (REV B BOM B10). 4 BELTS = 88 CLEATS.",
        "CLEATS 5 HIGH (CUT DOWN FROM 7.9, NHIEN 19 OCT): TIPS 22.1 FROM THE AXLE, 2.9 UNDER THE DECK UNDERSIDE, SO DECK P12 NEEDS NO NOTCH.",
        "ALTERNATIVE: TS-01 PRINTED TPU TRACK, 3 MM CLEATS, 5 MM UNDER THE DECK. SAME WHEELS, SAME CENTRES, SAME JOINTS.",
    ])
    # side view on the wheels, 1:1
    ax = view(22, 190, (-32, 254), (-32, 32), 1.0, "SIDE VIEW, ON THE TWO WHEELS (WHEELS DASHED)")
    belt_side(ax)
    for cx in (0.0, C):
        circle(ax, cx, 0, PU_OD_R, ls=(0, (4, 2)), lw=0.5)
        centre_mark(ax, cx, 0, 12)
    dim_h(ax, 0, C, -29, f"{C:g} CENTRES", ext_from=-PU_OD_R)
    dim_v(ax, -22.1, 22.1, 250, "44.2 OVER CLEATS", ext_from=C + 20)
    leader(ax, (112.5 + 5, 22.1), (150, 31), f"{CL_N} CLEATS AT {CL_PITCH:g} PITCH, EVERY 5TH TOOTH", fontsize=7)
    leader(ax, (-11.5, 9.0), (-30, 29.5), "110 TEETH HTD 5M INSIDE (PD 31.83 ON THE WHEEL)", fontsize=7)
    # section, straightened, 4:1
    S = 4.0
    ax = view(22, 60, (-3, 33), (-6, 15), S, "DETAIL: SECTION ALONG THE BELT, STRAIGHTENED (4:1)")
    back = B_T - B_TOOTH_H
    sec = [sbox(0, 0, 30, back)] + [tooth(2.5 + i * 5.0) for i in range(6)] + [SPoly([(5, back), (5 + CL_L, back), (5 + CL_L, back + CL_H), (5, back + CL_H)]), SPoly([(5 + CL_PITCH, back), (30, back), (30, back + CL_H), (5 + CL_PITCH, back + CL_H)])]
    shape_patch(ax, unary_union(sec).intersection(sbox(0, -5, 30, 12)), hatch="////")
    dim_h(ax, 2.5, 7.5, -4.0, "5", ext_from=-B_TOOTH_H, fontsize=7)
    dim_h(ax, 5, 5 + CL_L, back + CL_H + 1.2, f"{CL_L:g}", ext_from=back + CL_H, fontsize=7)
    dim_h(ax, 5, 5 + CL_PITCH, back + CL_H + 4.2, f"{CL_PITCH:g} CLEAT PITCH", ext_from=back + CL_H, fontsize=7)
    dim_v(ax, -B_TOOTH_H, back, 31.5, f"{B_T:g}", ext_from=30, fontsize=7)
    dim_v(ax, back, back + CL_H, 31.5, f"{CL_H:g}", ext_from=30, fontsize=7)
    dim_v(ax, -B_TOOTH_H, back + CL_H, 33.0, f"{B_T + CL_H:g}", ext_from=30, fontsize=7)
    ax.text(32, 12.0, "OUTSIDE (CLEATS, BONDED)", fontsize=6.5, ha="right", va="bottom")
    ax.text(29.5, -5.6, "INSIDE (TEETH, ON THE WHEEL)", fontsize=6.5, ha="right", va="bottom")
    # section across the belt, 2:1
    ax = view(190, 60, (-11, 11), (-6, 13), 2.0, "SECTION ACROSS THE BELT (2:1)")
    shape_patch(ax, unary_union([sbox(-B_W / 2, -B_TOOTH_H, B_W / 2, back), sbox(-CL_W / 2, back, CL_W / 2, back + CL_H)]), hatch="////")
    dim_h(ax, -B_W / 2, B_W / 2, -4.5, f"{B_W:g}", ext_from=-B_TOOTH_H, fontsize=7)
    dim_v(ax, back, back + CL_H, 9.5, f"{CL_H:g}", ext_from=CL_W / 2, fontsize=7)
    ax.text(0, 11.6, "CLEAT FULL WIDTH", fontsize=6.5, ha="center", va="bottom")
    save(fig, "TS-01B_track_belt")


# ------------------------------------------------------------------ TS-02 / TS-03 side plates
def sheet_side_plate(front):
    seg = "front" if front else "rear"
    pz0, pz1 = Z[f"{seg}_plate"]
    lane = Z[f"{seg}_lane"]
    lc = (lane[0] + lane[1]) / 2
    rail_z = (lc - RW / 2, lc + RW / 2)
    web_z = (pz0, rail_z[0]) if front else (rail_z[1], pz1)
    zlo, zhi = min(pz0, rail_z[0]), max(pz1, rail_z[1])
    fig, view, bg = a3_sheet(f"SIDE PLATE, {seg.upper()} SEGMENT", "TS-02" if front else "TS-03", material="PETG, 3D PRINTED",
                             finish="AS PRINTED", qty="2 (1 L + 1 R)", scale="1:1, SECTIONS 2:1", sheet="1 OF 2" if front else "2 OF 2", notes=[
        f"LEFT PLATE SHOWN; THE RIGHT ONE IS ITS MIRROR. FILES stl/side_plate_{seg}_L.stl, _R.stl.",
        "PRINT LYING ON THE PLATE FACE, 0.2 LAYERS, 4 WALLS, 30% INFILL, NO SUPPORTS.",
        "BED 235 MM (OR 225 DIAGONAL); ON A SMALLER BED ASK FOR THE TWO-PIECE PLATE.",
        f"Z FROM THE VEHICLE CENTRE LINE: PLATE {pz0:g}-{pz1:g}, WEB {web_z[0]:g}-{web_z[1]:g}, RAIL {rail_z[0]:g}-{rail_z[1]:g}",
        f"(RAIL CENTRED UNDER THE TRACK LANE {lane[0]:g}-{lane[1]:g}). R20 ENDS ARE CENTRED 10.5 ABOVE THE AXLE.",
        "POCKETS Ø22.2 THRU TAKE A 608ZZ (TS-07), LIGHT PRESS: MEASURE THE FIRST PRINT,",
        "REAM IF TIGHT, GLUE IF LOOSE. THE RAIL TOP CARRIES THE LOWER RUN'S TOOTH TIPS.",
        "X = 0 IS THE MIDDLE AXLE (HINGE); 3 x M3 SECTOR GEAR HOLES ON R17 ROUND IT, INBOARD FACE." if front else "X = 0 IS THE REAR AXLE. THE BOX BOLTS TO THESE PLATES THROUGH THE Ø4.5 CROSS-BAR HOLES.",
    ])
    # TOP VIEW (x-z), above the front view
    ax = view(20, 205, (-30, 255), (zlo - 3, zhi + 5), 1.0, "TOP VIEW")
    rect(ax, -END_R, pz0, C + 2 * END_R, T, "white")
    rect(ax, RX0, web_z[0], RX1 - RX0, web_z[1] - web_z[0], "white", lw=0.6)
    rect(ax, RX0, rail_z[0], RX1 - RX0, RW, "white", lw=0.6)
    for x in (0, C):
        for dx in (-POCKET / 2, POCKET / 2):
            ax.plot([x + dx, x + dx], [pz0, pz1], **HIDDEN)
        centreline(ax, x, zlo - 2, x, zhi + 3)
    dim_v(ax, pz0, pz1, -26, f"{T:g}", ext_from=-END_R)
    dim_v(ax, rail_z[0], rail_z[1], 214, f"{RW:g} RAIL", ext_from=RX1)
    dim_v(ax, zlo, zhi, 250, f"{zhi - zlo:g}", ext_from=RX1)
    # FRONT VIEW (x-y), seen from outboard
    ax = view(20, 92, (-30, 255), (-42, 65), 1.0, "FRONT VIEW (FROM OUTBOARD)")
    shape_patch(ax, plate_shape())
    rect(ax, RX0, -RBOT, RX1 - RX0, RBOT - BELOW, "white", lw=0.6)
    for x in (0, C):
        circle(ax, x, 0, POCKET / 2, fill="white")
        centre_mark(ax, x, 0, 26)
    for x in CBH["at_x_mm"]:
        circle(ax, x, CBH["above_axle_mm"], CBH["dia_mm"] / 2, fill="white", lw=0.6)
        centre_mark(ax, x, CBH["above_axle_mm"], 5)
    if front:
        for a in SB["angles_deg"]:
            circle(ax, SB["radius_mm"] * math.cos(math.radians(a)), SB["radius_mm"] * math.sin(math.radians(a)), SB["dia_mm"] / 2, fill="white", lw=0.6)
    centreline(ax, -28, 0, C + 28, 0)
    dim_h(ax, 0, C, 54, f"{C:g}", ext_from=ABOVE + 1)
    dim_h(ax, -END_R, C + END_R, 62, f"{C + 2 * END_R:g}", ext_from=ABOVE + 1)
    dim_h(ax, 0, CBH["at_x_mm"][0], 42, f"{CBH['at_x_mm'][0]:g}", ext_from=CBH["above_axle_mm"] + 2.5)
    dim_h(ax, 0, CBH["at_x_mm"][1], 46.5, f"{CBH['at_x_mm'][1]:g}", ext_from=CBH["above_axle_mm"] + 2.5)
    dim_h(ax, RX0, RX1, -26, f"{RX1 - RX0:g}", ext_from=-RBOT)
    dim_h(ax, 0, RX0, -38, f"{RX0:g}", ext_from=-RBOT)
    dim_v(ax, -BELOW, ABOVE, -24, f"{BELOW + ABOVE:g}", ext_from=-END_R - 1)
    dim_v(ax, 0, ABOVE, -17, f"{ABOVE:g}", ext_from=-END_R - 1)
    dim_v(ax, -BELOW, 0, -17, f"{BELOW:g}", ext_from=-END_R - 1)
    dim_v(ax, 0, CBH["above_axle_mm"], 240, f"{CBH['above_axle_mm']:g}")
    ax.plot([CBH["at_x_mm"][1] + 2.5, 240.5], [CBH["above_axle_mm"]] * 2, color=DIM, lw=0.5)
    dim_v(ax, -RBOT, -RTOP, 215, f"{RT:g}", ext_from=RX1)
    ax.plot([RX1, 258], [-RBOT, -RBOT], color=DIM, lw=0.5)
    dim_v(ax, -RBOT, 0, 258, f"{RBOT:g}", fontsize=7)
    ax.plot([RX1, 266], [-RTOP, -RTOP], color=DIM, lw=0.5)
    dim_v(ax, -RTOP, 0, 266, f"{RTOP:g}", fontsize=7)
    leader(ax, (C + END_R * math.cos(math.radians(-40)), ARC_CY + END_R * math.sin(math.radians(-40))), (228, -31), f"R{END_R:g}, 2 PL.")
    leader(ax, (-BOSS_R * math.cos(math.radians(60)), -BOSS_R * math.sin(math.radians(60))), (-28, -32), f"R{BOSS_R:g} BOSS, 2 PLACES")
    leader(ax, (C + POCKET / 2 * math.cos(math.radians(135)), POCKET / 2 * math.sin(math.radians(135))), (160, 36), f"2 x Ø{POCKET:g} THRU (608ZZ POCKET)")
    leader(ax, (CBH["at_x_mm"][0] + CBH["dia_mm"] / 2, CBH["above_axle_mm"]), (90, 36), f"2 x Ø{CBH['dia_mm']:g} THRU (CROSS BAR)")
    section_mark(ax, 100, -34, 62, "A", side=1)
    section_mark(ax, C, -34, 62, "B", side=1)
    # SECTION A-A through the rail (y-z), 2:1
    ax = view(285, 146, (zlo - 9, zlo + 51), (-27, 37.5), 2.0, "SECTION A-A (2:1)")
    rect(ax, pz0, -BELOW, T, BELOW + ABOVE, "white", hatch=True)
    rect(ax, web_z[0], -RBOT, web_z[1] - web_z[0], RBOT - BELOW, "white", hatch=True)
    rect(ax, rail_z[0], -RBOT, RW, RT, "white", hatch=True)
    b1, bb, b2 = lane_bands(lane)
    hidden_rect(ax, bb[0], -R_TIP, TRK_W, R_TIP - R_TOOTH)
    ax.text(bb[0] + TRK_W / 2, -R_TIP - 5.2, "TRACK LOWER RUN (REF)", fontsize=5.5, ha="center", va="top")
    centreline(ax, zlo - 8, 0, zhi + 8, 0)
    dim_h(ax, pz0, pz1, ABOVE + 3, f"{T:g}", ext_from=ABOVE, fontsize=7)
    dim_h(ax, rail_z[0], rail_z[1], -RBOT - 4.5, f"{RW:g}", ext_from=-RBOT, fontsize=7)
    dim_h(ax, web_z[0], web_z[1], -RBOT - 4.5, f"{web_z[1] - web_z[0]:g}", ext_from=-RBOT, fontsize=7)
    ps, rs = (-1, 1) if front else (1, -1)          # plate dims on the plate's side, rail dims on the rail's side
    px = pz0 if front else pz1
    dim_v(ax, -BELOW, ABOVE, px + ps * 3, f"{BELOW + ABOVE:g}", ext_from=px, fontsize=7)
    dim_v(ax, 0, ABOVE, px + ps * 7, f"{ABOVE:g}", ext_from=px, fontsize=7)
    rx = rail_z[1] if front else rail_z[0]
    dim_v(ax, -RBOT, -RTOP, rx + rs * 2.5, f"{RT:g}", ext_from=rx, fontsize=7)
    dim_v(ax, -RTOP, 0, rx + rs * 6.5, f"{RTOP:g}", ext_from=rx, fontsize=7)
    ax.text(zlo - 8, 37, f"Z {zlo:g} TO {zhi:g}", fontsize=6.5, va="top")
    # SECTION B-B through a pocket (y-z), 2:1
    ax = view(315, 70, (pz0 - 11, pz0 + 31), (-18, 18), 2.0, "SECTION B-B (2:1)")
    rect(ax, pz0, -BOSS_R, T, BOSS_R - POCKET / 2, "white", hatch=True)
    rect(ax, pz0, POCKET / 2, T, 18 - POCKET / 2 + 0.0, "white", hatch=True)
    ax.plot([pz0, pz0 + T], [18, 18], color="white", lw=1.2, zorder=4)
    centreline(ax, pz0 - 10, 0, pz0 + 30, 0)
    dim_v(ax, -POCKET / 2, POCKET / 2, pz1 + 8, f"Ø{POCKET:g}", ext_from=pz1, fontsize=7)
    dim_v(ax, -BOSS_R, -POCKET / 2, pz1 + 15, f"{BOSS_R - POCKET / 2:g}", ext_from=pz1, fontsize=7)
    dim_h(ax, pz0, pz1, -BOSS_R - 2.5, f"{T:g} THRU", ext_from=-BOSS_R, fontsize=7)
    ax.text(pz0 + 14, 16, "PLATE CUT\nABOVE", fontsize=5.5, va="top")
    # DETAIL C (front only): sector gear holes
    if front:
        ax = view(132, 17, (-24, 24), (-24, 24), 1.5, "DETAIL C: SECTOR GEAR HOLES (1.5:1)")
        shape_patch(ax, plate_shape())
        circle(ax, 0, 0, POCKET / 2, fill="white")
        circle(ax, 0, 0, SB["radius_mm"], fill="none", lw=0.5, ls=(0, (6, 2, 1.5, 2)))
        for a in SB["angles_deg"]:
            x, y = SB["radius_mm"] * math.cos(math.radians(a)), SB["radius_mm"] * math.sin(math.radians(a))
            circle(ax, x, y, SB["dia_mm"] / 2, fill="white", lw=0.6)
            ax.plot([0, x], [0, y], color=DIM, lw=0.4)
        centre_mark(ax, 0, 0, 23)
        ax.text(-23, -17, f"3 x Ø{SB['dia_mm']:g} THRU ON R{SB['radius_mm']:g}\nAT {', '.join(f'{a:g}°' for a in SB['angles_deg'])} FROM +X\nM3 x 14 + NUT", fontsize=6, va="top")
    save(fig, "TS-02_side_plate_front" if front else "TS-03_side_plate_rear")


# ------------------------------------------------------------------ TS-04 axles
def sheet_axles():
    D = AX["dia_mm"]
    L = AX["lengths_mm"]
    fig, view, bg = a3_sheet("AXLES AND HINGE CROSS SHAFT", "TS-04", material="STEEL ROD Ø8 h7, UNHARDENED", finish="CUT SQUARE, DEBURR", qty="3 + 1", scale="1:1, DETAIL 4:1", notes=[
        "BUY: MISUMI 8 MM LINEAR SHAFT (UNHARDENED, SO THE FLATS CAN BE FILED) OR DESIGN LAB SPARE ROD. CUT TO LENGTH, ENDS SQUARE, DEBURRED: THE 608ZZ BORES ARE A CLOSE FIT.",
        "FLATS 0.5 DEEP x 10 LONG UNDER EVERY PULLEY SET SCREW (AT THE HUB CENTRES, BOTH SIDES) AND UNDER THE DRIVE SPROCKET ON THE MIDDLE AXLE (Z 0).",
        "THE MIDDLE AXLE IS THE HINGE: BOTH SEGMENTS' PLATES TURN ON IT IN THEIR 608ZZ. Z = 0 IS THE VEHICLE CENTRE LINE; THE AXLES ARE SYMMETRICAL ABOUT IT.",
        "HINGE CROSS SHAFT: SAME ROD, 120 LONG, CARRIES THE TWO HINGE PINIONS ACROSS THE BOX IN 2 x 608ZZ; LENGTH TO BE CONFIRMED WITH THE HINGE GEAR DRAWING.",
    ])
    fh, rh = (Z["front_hub"][0] + Z["front_hub"][1]) / 2, (Z["rear_hub"][0] + Z["rear_hub"][1]) / 2
    axles = [
        ("MIDDLE AXLE (HINGE, DRIVEN), QTY 1", L["middle"], [fh, -fh, rh, -rh, 0.0], ["FRONT HUB", "", "REAR HUB", "", "SPROCKET"]),
        ("REAR AXLE, QTY 1", L["rear"], [rh, -rh], ["REAR HUB", ""]),
        ("FRONT AXLE, QTY 1", L["front"], [fh, -fh], ["FRONT HUB", ""]),
        ("HINGE CROSS SHAFT, QTY 1", P["hinge_cross_shaft"]["length_mm"], [], []),
    ]
    y = 236
    for name, length, flats, labels in axles:
        ax = view(22, y, (-128, 136), (-17, 17), 1.0, name)
        h = length / 2
        rect(ax, -h, -D / 2, length, D, "white")
        centreline(ax, -h - 8, 0, h + 8, 0)
        for zc, lab in zip(flats, labels):
            rect(ax, zc - 5, D / 2 - 0.5, 10, 0.5, "white", lw=0.4)
            if lab:
                leader(ax, (zc, D / 2), (zc + 6, 13), f"FLAT, {lab}", fontsize=6.5)
        dim_h(ax, -h, h, -12, f"{length:g}", ext_from=-D / 2)
        dim_v(ax, -D / 2, D / 2, h + 8, f"Ø{D:g} h7", ext_from=h)
        if flats:
            for zc in sorted(set(abs(z) for z in flats if z)):
                dim_h(ax, 0, zc, 9.5 if zc > 80 else 6, f"{zc:g}", ext_from=D / 2, fontsize=7)
            ax.plot([0, 0], [-D / 2 - 1, D / 2 + 8], color=DIM, lw=0.5)
            ax.text(0, -D / 2 - 1.5, "Z 0", fontsize=6, ha="center", va="top")
        y -= 46
    ax = view(300, 150, (-8, 18), (-7, 7), 4.0, "DETAIL: FLAT UNDER A SET SCREW (4:1)")
    rect(ax, -7, -D / 2, 24, D, "white")
    rect(ax, -5, D / 2 - 0.5, 10, 0.5, "white", lw=0.5)
    centreline(ax, -7.5, 0, 17.5, 0)
    dim_h(ax, -5, 5, 5.2, "10", ext_from=D / 2, fontsize=7)
    dim_v(ax, D / 2 - 0.5, D / 2, 8.5, "0.5", ext_from=5, fontsize=7)
    leader(ax, (0, D / 2 - 0.25), (6, -5.5), "SET SCREW TIP BEARS HERE", fontsize=6.5)
    save(fig, "TS-04_axles")


# ------------------------------------------------------------------ TS-05 spacer
def sheet_spacer():
    od, bore = CB["front_segment"]["spacer_od_mm"], 4.5
    lf, lr = CB["front_segment"]["spacer_length_mm"], CB["rear_segment"]["spacer_length_mm"]
    fig, view, bg = a3_sheet("CROSS BAR SPACER", "TS-05", material="PETG, 3D PRINTED", finish="AS PRINTED", qty="2 x 82 + 4 x 65", scale="1:1, DETAIL 3:1", notes=[
        "FILES stl/spacer_front_x2.stl (82) AND stl/spacer_rear_x4.stl (65). PRINT STANDING ON END, 0.2 LAYERS, 3 WALLS, 20% INFILL.",
        "FRONT: ONE 82 SPACER PER ROD BETWEEN THE FRONT PLATES (2 x 41). REAR: TWO 65 SPACERS PER ROD, ONE EACH SIDE BETWEEN THE BOX WALL (Z 40) AND THE REAR PLATE (Z 105).",
        "THE NUTS OUTSIDE THE PLATES PULL PLATE - SPACER - BOX - SPACER - PLATE TOGETHER (SEE TS-08). AT 28 ABOVE THE AXLE THE SPACER CLEARS THE UPPER RUN'S CLEAT TIPS BY 3.3.",
        "BORE 4.5 IS A CLEARANCE FOR THE M4 ROD. ENDS SQUARE: THEY SET THE PLATE SPACING.",
    ])
    for y, L, name in ((215, lr, "REAR SEGMENT SPACER, QTY 4 (2 PER ROD)"), (165, lf, "FRONT SEGMENT SPACER, QTY 2")):
        ax = view(22, y, (-12, 230), (-10, 12), 1.0, name)
        rect(ax, 0, -od / 2, L, od, "white")
        for yy in (bore / 2, -bore / 2):
            ax.plot([0, L], [yy, yy], **HIDDEN)
        centreline(ax, -8, 0, L + 8, 0)
        dim_h(ax, 0, L, -8.5, f"{L:g}", ext_from=-od / 2)
        dim_v(ax, -od / 2, od / 2, L + 8, f"Ø{od:g}", ext_from=L)
    ax = view(300, 190, (-9, 9), (-9, 9), 3.0, "END VIEW (3:1)")
    circle(ax, 0, 0, od / 2, fill="white")
    circle(ax, 0, 0, bore / 2, fill="white")
    centre_mark(ax, 0, 0, 8)
    dim_dia(ax, 0, 0, bore / 2, 45, f"Ø{bore:g}", length=8.2, fontsize=7)
    dim_dia(ax, 0, 0, od / 2, -45, f"Ø{od:g}", length=8.2, fontsize=7)
    ax = view(300, 105, (-3, 21), (-9, 9), 3.0, "SECTION, ONE END (3:1)")
    rect(ax, 0, bore / 2, 20, (od - bore) / 2, "white", hatch=True)
    rect(ax, 0, -od / 2, 20, (od - bore) / 2, "white", hatch=True)
    ax.plot([20, 20], [-od / 2, od / 2], color="white", lw=1.5, zorder=4)
    centreline(ax, -2, 0, 20, 0)
    dim_v(ax, bore / 2, od / 2, -1.8, f"{(od - bore) / 2:g}", ext_from=0, fontsize=7)
    leader(ax, (0, od / 2), (3, 8), "END SQUARE, NO CHAMFER", fontsize=6.5)
    save(fig, "TS-05_spacer")


# ------------------------------------------------------------------ TS-06 pulley (bought)
def sheet_pulley():
    fig, view, bg = a3_sheet("TIMING PULLEY HTD 5M 20T (BOUGHT, PLAIN BORE)", "TS-06", material="ALUMINIUM (VENDOR'S)", finish="VENDOR'S", qty=8, scale="2:1", notes=[
        "BOUGHT PART. ORDER: HTD 5M, 20 TEETH, FOR 15 MM BELT, FLANGES BOTH SIDES, PLAIN PILOT BORE.\n    MISUMI SINGAPORE (APPROVED VENDOR). 8 OFF, PLUS 1 TO PRACTISE THE BORING AND PINNING ON.",
        "WHAT MATTERS: 20T HTD 5M (PD 31.83) AND THE 15 MM BELT. ON NHIEN'S PLATES THE LANE IS 19-20 WIDE, SO NO HUB FITS:\n    THE HUB AND SET SCREW DRAWN ARE THE PLA STAND-IN'S ONLY.",
        "WORKSHOP: 4 x REAM Ø8 H7 (HINGE SHAFT, PLAIN ROUND, NO D-FLAT). Ø2.5 CROSS HOLE AT MID-FACE: DRILL THE HUB NOW,\n    ON THE PRESS IN A V-BLOCK. AT ASSEMBLY THE SHAFT IS DRILLED THROUGH THE HUB HOLE IN PLACE. SPRING PIN ISO 8752 2.5 x 24.",
        "THE PIN DRIVES AND LOCATES THE PULLEY: NO GRUB SCREW, NO E-CLIPS (TS-11).\n    4 x BORE Ø16 H7 THROUGH FOR 2 x 688-2RS EACH (IDLERS ON Ø8 SHOULDER SCREWS, SLEEVE 8 x 10 x 9 BETWEEN).",
        "PLA STAND-IN FOR FIT TESTS ONLY: stl/stand_in_pulley_20T_PLA_test_only.stl (M3 SET SCREW). NOT FOR DRIVING.",
    ])
    S = 2.0
    ax = view(40, 100, (-24, 24), (-24, 24), S, "FRONT VIEW")
    circle(ax, 0, 0, FL_R, fill="white")
    body = Point(0, 0).buffer(PU_OD_R, quad_segs=120)
    grooves = [Point((PU_OD_R - 0.45) * math.cos(a), (PU_OD_R - 0.45) * math.sin(a)).buffer(1.5, quad_segs=16) for a in [2 * math.pi * k / PU["teeth"] for k in range(PU["teeth"])]]
    shape_patch(ax, body.difference(unary_union(grooves)), zorder=3)
    circle(ax, 0, 0, HUB_R, fill="white").set_zorder(4)
    circle(ax, 0, 0, PU["bore_mm"] / 2, fill="white").set_zorder(5)
    circle(ax, 0, 0, R_PITCH, fill="none", lw=0.5, ls=(0, (6, 2, 1.5, 2))).set_zorder(6)
    centre_mark(ax, 0, 0, 22)
    dim_dia(ax, 0, 0, FL_R, 60, f"Ø{PU['flange_dia_mm']:g} FLANGE", length=24)
    dim_dia(ax, 0, 0, PU_OD_R, 40, f"Ø{PU['outside_dia_mm']:g} OD", length=24)
    dim_dia(ax, 0, 0, R_PITCH, 20, f"Ø{PU['pitch_dia_mm']:g} PD", length=24)
    dim_dia(ax, 0, 0, HUB_R, -20, f"Ø{PU['hub_dia_mm']:g} HUB", length=24)
    dim_dia(ax, 0, 0, PU["bore_mm"] / 2, -40, f"Ø{PU['bore_mm']:g} H7 BORE", length=24)
    ax.text(-23, -23, "20 TEETH HTD 5M, 5 PITCH", fontsize=7, va="bottom")
    ax = view(150, 92, (-6, 40), (-32, 24), S, "SECTION (ALONG THE AXLE)")
    OL = PU["overall_length_mm"]
    for sgn in (1, -1):
        y0 = PU["bore_mm"] / 2
        pts = [(0, sgn * y0), (0, sgn * FL_R), (FL_T, sgn * FL_R), (FL_T, sgn * PU_OD_R), (FL_T + PU_FACE, sgn * PU_OD_R), (FL_T + PU_FACE, sgn * FL_R),
               (2 * FL_T + PU_FACE, sgn * FL_R), (2 * FL_T + PU_FACE, sgn * HUB_R), (OL, sgn * HUB_R), (OL, sgn * y0)]
        ax.add_patch(Polygon(pts, closed=True, fc="white", ec=INK, lw=0.8, hatch="////"))
    for k in range(1, 8):
        yy = PU_OD_R - 2.06 * (k % 2)
    for x in (FL_T + 2.5 * i for i in range(1, 7)):
        ax.plot([x, x], [PU_OD_R - 2.06, PU_OD_R], color=INK, lw=0.4)
        ax.plot([x, x], [-PU_OD_R, -PU_OD_R + 2.06], color=INK, lw=0.4)
    rect(ax, FL_T + PU_FACE / 2 - 1.25, -12, 2.5, 24, "white", lw=0.5)
    leader(ax, (FL_T + PU_FACE / 2 + 1.25, -10), (22, -26), "CROSS PIN Ø2.5 x 24, HINGE PULLEYS:\nHUB DRILLED NOW, SHAFT THROUGH IT AT ASSEMBLY", fontsize=6.5)
    ax.text(2 * FL_T + PU_FACE + 3.5, HUB_R + 0.8, "HUB: STAND-IN\nONLY", fontsize=6, ha="center", va="bottom")
    centreline(ax, -5, 0, OL + 5, 0)
    dim_h(ax, 0, FL_T, -FL_R - 3, f"{FL_T:g}", ext_from=-FL_R, fontsize=7)
    dim_h(ax, FL_T, FL_T + PU_FACE, -FL_R - 3, f"{PU_FACE:g}", ext_from=-PU_OD_R, fontsize=7)
    dim_h(ax, 0, 2 * FL_T + PU_FACE, -FL_R - 8, f"{PU['over_flanges_mm']:g} OVER FLANGES", ext_from=-FL_R)
    dim_h(ax, 2 * FL_T + PU_FACE, OL, -FL_R - 3, f"{HUB_L:g}", ext_from=-HUB_R, fontsize=7)
    dim_h(ax, 0, OL, -FL_R - 13, f"{OL:g}", ext_from=-FL_R)
    dim_v(ax, -FL_R, FL_R, -4, f"Ø{PU['flange_dia_mm']:g}", ext_from=0)
    dim_v(ax, -HUB_R, HUB_R, OL + 4, f"Ø{PU['hub_dia_mm']:g}", ext_from=OL)
    dim_v(ax, -PU["bore_mm"] / 2, PU["bore_mm"] / 2, OL + 9, f"Ø{PU['bore_mm']:g}", ext_from=OL)
    leader(ax, (FL_T + 8, PU_OD_R), (14, 21), f"BELT {TRK_W:g} WIDE SITS HERE", fontsize=7)
    save(fig, "TS-06_pulley_20T")


# ------------------------------------------------------------------ TS-09 idler tensioner (tab, slider, jack screw)
def sheet_tensioner():
    fig, view, bg = a3_sheet("IDLER TENSIONER: TAB, SLIDER AND JACK SCREW", "TS-09", material="AL ANGLE 20x20x3; AL PLATE 3", finish="DEBURRED", qty="4 SETS", scale="2:1, PARTS 2:1", notes=[
        "THE SHOULDER SCREW IS CLAMPED IN THE SLOT BY FRICTION ONLY. THE JACK SCREW SETS THE IDLER, THEN THE NUT IS TIGHTENED.",
        "SLIDER REPLACES THE M6 WASHER UNDER THE NUT (3 THICK). TAB: NEW M3 TAPPED HOLE IN P1 / P2 AT x = +-223, y = +11\n    (ADD TO THE DXF, OR DRILL 2.5 AND TAP ON SITE).",
        "FIT: IDLER INTO THE LOOP, SHOULDER SCREW THROUGH, SLIDER, NUT LOOSE, THEN THE TAB. TENSION (MACHINE ON BLOCKS):\n    HOOK A CLEAT OF THE LOWER RUN AT MID-SPAN, PULL IT OFF ITS RAIL WITH 4 N, WIND THE JACK SCREW UNTIL IT GIVES 2-3 MM,\n    TIGHTEN THE NUT, BACK OFF 1/4 TURN. PUSHING A RUN INWARD MOVES NOTHING: THE RAILS SIT UNDER BOTH RUNS.",
        "DO NOT PUSH THE IDLER IN PAST x = 223 (RAIL END): TRAVEL 223 TO 232.6 = 9.6 MM = 19 MM OF LOOP.\n    JACK SCREW M4 x 20 SOCKET HEAD, KEY FROM THE HINGE SIDE, UNDER THE BAR; IT PUSHES THE SLIDER'S FOOT. LEG B 1.5 OFF THE SLOT END.",
    ])
    S = 2.0
    # view 1: nose end of P1 seen from inboard
    ax = view(22, 162, (195, 244), (-19, 19), S, "NOSE END OF P1, SEEN FROM INBOARD (THE z 55 FACE)")
    arc = [(225 + 15.2 * math.cos(a), 0.2 + 15.2 * math.sin(a)) for a in [math.radians(t) for t in range(-90, 91, 6)]]
    ax.add_patch(Polygon([(203, -15), (225, -15)] + arc + [(225, 15.4), (203, 15.4)], closed=True, fc="white", ec=INK, lw=0.8, zorder=2))
    shape_patch(ax, stadium(4.05, 220.4, 232.6), fc="white", zorder=3)
    circle(ax, 225, 0, 4, ls=(0, (4, 2)), lw=0.5).set_zorder(4)
    rect(ax, 221, -13, 8, 19, "white", lw=0.8, zorder=5)                                   # slider leg
    rect(ax, 221, -13, 8, 3, "white", lw=0.8, hatch="////", zorder=6)                     # its foot, edge on
    ax.add_patch(RegularPolygon((225, 0), 6, radius=5.77, orientation=math.radians(30), fc="white", ec=INK, lw=0.8, zorder=6))   # nut
    rect(ax, 215.5, -15, 3, 30, "white", lw=0.8, hatch="////", zorder=6)                 # tab leg B, edge on, 1.5 off the slot end
    rect(ax, 218.5, 7, 7.5, 8, "white", lw=0.8, zorder=5)                                # ear on the plate
    circle(ax, 223, 11, 1.7, fill="white", lw=0.6).set_zorder(7)
    rect(ax, 202.5, -12.1, 18.5, 2.2, "white", lw=0.5, zorder=7)                         # jack screw shank (through leg B to the foot)
    rect(ax, 198.5, -14.5, 4, 7, "white", lw=0.5, hatch="////", zorder=7)                # its head
    dim_h(ax, 220.4, 232.6, -17, "SLOT 12.2 x 8.1", ext_from=-4.05, fontsize=6.5)
    dim_h(ax, 215.5, 218.5, 17, "3", ext_from=15, fontsize=6.5)
    leader(ax, (229, -5), (233, -17), "SLIDER: 8 SLICE OF THE ANGLE, LEG 19 + FOOT 8", fontsize=6.5)
    leader(ax, (223, 12.7), (231, 16.5), "M3 x 6 INTO NEW TAPPED HOLE (223, +11)", fontsize=6.5)
    leader(ax, (200.5, -14.5), (199, -18.3), "JACK SCREW M4 x 20, ON THE FOOT", fontsize=6.5)
    leader(ax, (229.5, 2.5), (234, 8), "M6 NYLOC", fontsize=6.5)
    # view 2: plan from above (x along, z across)
    ax = view(22, 52, (195, 244), (34, 86), S * 0.9, "PLAN FROM ABOVE: PLATE, LANE, IDLER, TAB")
    rect(ax, 203, 55, 37.2, 5, "white", lw=0.8, hatch="////")                            # plate P1 (z 55-60) to its end
    ax.add_patch(Polygon([(240.2, 55), (240.2, 60)], closed=False, ec=INK, lw=0.8))
    rect(ax, 207, 60.5, 36, 1.5, "white", lw=0.6); rect(ax, 207, 78, 36, 1.5, "white", lw=0.6)   # flanges
    rect(ax, 209.6, 62, 30.8, 16, "white", lw=0.6)                                       # pulley body
    rect(ax, 203, 60, 1.5, 20, "white", lw=0.5, hatch="\\\\")                        # rail carrier leg (TS-10) at the plate face
    rect(ax, 221, 80.5, 8, 5.5, "white", lw=0.6)                                         # screw head
    rect(ax, 219.5, 79.5, 11, 1, "white", lw=0.5)                                        # head washer
    rect(ax, 221, 52, 8, 3, "white", lw=0.8)                                             # slider leg on the plate face
    rect(ax, 221, 47, 8, 5, "white", lw=0.8, hatch="\\\\")                              # slider foot, 8 inboard
    rect(ax, 220, 46, 10, 6, "white", lw=0.8)                                            # nut
    ax.add_patch(Rectangle((222, 44.5), 6, 41.5, fc="none", ec=INK, lw=0.5, ls=(0, (4, 2)), zorder=4))   # shoulder screw outline
    rect(ax, 218.5, 52, 7.5, 3, "white", lw=0.8, hatch="////")                           # ear (leg A) on the plate face
    rect(ax, 215.5, 35, 3, 20, "white", lw=0.8, hatch="////")                            # leg B
    rect(ax, 203, 30.5, 7.9, 24.5, "white", lw=0.5, hatch="\\\\")                      # 2020 bar end (x to 210.9)
    rect(ax, 202.5, 47.9, 18.5, 2.2, "white", lw=0.5)                                    # jack screw through leg B to the slider foot
    rect(ax, 198.5, 45.5, 4, 7, "white", lw=0.5, hatch="////")                           # its head
    dim_v(ax, 55, 60, 243, "5", ext_from=240.2, fontsize=6.5)
    dim_v(ax, 60.5, 79.5, 243, "19", ext_from=243, fontsize=6.5)
    dim_v(ax, 46, 55, 212, "NUT 6 + SLIDER 3", ext_from=220, fontsize=6.5)
    dim_v(ax, 35, 55, 213, "20", ext_from=215.5, fontsize=6.5)
    leader(ax, (210.9, 42), (206, 38.5), "2020 BAR P7 ENDS AT x 210.9", fontsize=6.5)
    leader(ax, (217, 49), (206, 70), "JACK SCREW AXIS y -11, UNDER THE BAR, TIP ON THE FOOT", fontsize=6.5)
    ax.text(203.5, 85, "OUTBOARD (LANE, TRACK)", fontsize=6.5, va="top"); ax.text(212, 35, "INBOARD", fontsize=6.5, va="bottom")
    # parts
    ax = view(190, 168, (-4, 36), (-4, 27), S, "TAB: AL ANGLE 20x20x3, CUT 30, LEG A CUT TO A 7.5 x 8 EAR")
    rect(ax, 0, 0, 30, 20, "white", lw=0.8)                                              # leg B, flat; the bend is its top edge (y 20)
    circle(ax, 4, 14, 1.7, fill="white").set_zorder(4)                                   # M4 tapped: 4 from the bottom end, 6 from the bend
    rect(ax, 22, 20, 8, 3, "white", lw=0.8, hatch="////")                                # ear seen edge on (leg A, 3 thick), 8 long at the top end
    dim_h(ax, 0, 30, -2.5, "30", ext_from=0, fontsize=6.5)
    dim_h(ax, 0, 4, 24.5, "4", ext_from=20, fontsize=6.5)
    dim_v(ax, 14, 20, 31, "6", ext_from=28, fontsize=6.5)
    dim_v(ax, 0, 20, 33, "20", ext_from=28, fontsize=6.5)
    dim_h(ax, 22, 30, 25.5, "8 (EAR)", ext_from=23, fontsize=6.5)
    leader(ax, (4, 15.7), (8, 10), "M4 TAPPED THROUGH (JACK SCREW)", fontsize=6.5)
    ax = view(190, 104, (-4, 14), (-4, 24), S, "TAB, END VIEW")
    rect(ax, 0, 0, 3, 20, "white", lw=0.8, hatch="////"); rect(ax, 0, 0, 7.5, 3, "white", lw=0.8, hatch="////")
    dim_h(ax, 0, 7.5, -2.5, "7.5", ext_from=0, fontsize=6.5); dim_v(ax, 0, 3, 9.5, "3", ext_from=7.5, fontsize=6.5)
    hidden_rect(ax, 2.8, 0, 3.4, 3)
    leader(ax, (3, 3), (6, 12), "Ø3.4 THROUGH THE EAR\n(4.5 FROM THE BEND)", fontsize=6.5)
    ax = view(160, 40, (-4, 26), (-4, 23), S, "SLIDER: 8 SLICE OF THE 20x20x3 ANGLE, FACE AND END VIEW")
    rect(ax, 0, 0, 8, 19, "white", lw=0.8); circle(ax, 4, 13, 3.2, fill="white").set_zorder(4)
    rect(ax, 14, 0, 3, 19, "white", lw=0.8, hatch="////"); rect(ax, 14, 0, 8, 3, "white", lw=0.8, hatch="////")   # end view: leg 19 and foot 8
    dim_h(ax, 14, 22, -2.5, "8 FOOT", ext_from=0, fontsize=6.5)
    dim_h(ax, 0, 8, -2.5, "8", ext_from=0, fontsize=6.5); dim_v(ax, 0, 19, 11, "19", ext_from=8, fontsize=6.5); dim_v(ax, 0, 13, -2.5, "13", ext_from=0, fontsize=6.5)
    leader(ax, (6.3, 14.5), (9, 18), "Ø6.4", fontsize=6.5)
    save(fig, "TS-09_tensioner")


# ------------------------------------------------------------------ TS-10 rail carrier angle (replaces the 4 small clips per rail)
def sheet_rail_carrier():
    fig, view, bg = a3_sheet("RAIL CARRIER ANGLE (REPLACES RS 427-991 CLIPS)", "TS-10", material="AL ANGLE 10x10x1.5", finish="DEBURRED", qty=8, scale="1:1, SECTION 4:1", notes=[
        "WHY: EACH UHMW RAIL HUNG ON 4 SMALL CLIPS (10 x 14.6 FEET). THE ANGLE RUNS THE FULL RAIL LENGTH: 186 x 10 OF CONTACT\n    ON THE PLATE AND ON THE RAIL INSTEAD OF 4 SMALL PATCHES.",
        "TRIM EACH RAIL FROM 189 TO 186 (3 OFF THE IDLER END): THE IDLER PULLEY FLANGE REACHES x 207 AT ITS INNERMOST SLOT POSITION\n    AND THE RAIL ENDED AT 207 (TS-11).",
        "PLATE LEG CUT TO 6.5 SO THE UPPER AND LOWER ANGLES DO NOT MEET ON THE PLATE'S CENTRELINE. 3 x Ø3.4 IN THE PLATE LEG AT\n    x 40, 105, 170 FROM THE HINGE, y +-3.5: SIX NEW M3 HOLES IN P1 / P2 (THE OLD CLIP HOLES ON THE CENTRELINE ARE NOT USED).\n    3 x Ø2.6 IN THE RAIL LEG AT 20, 93, 166 FROM THE RAIL'S HINGE END (x 38, 111, 184), 7.5 FROM THE PLATE FACE: 3 x 5 THREAD-FORMING SCREWS.\n    DO NOT DRILL THE OLD CLIP PILOTS IN THE RAIL: THEY OVERLAP THE NEW ONES AT x 38 / 40 AND 184 / 185.",
        "THE ANGLE SITS ON THE RAIL FACE AWAY FROM THE TRACK: UNDER THE UPPER RAIL, ON TOP OF THE LOWER RAIL. THE TRACK'S TOOTH TIPS\n    RIDE ON THE OTHER FACE (y 13.3).",
    ])
    ax = view(22, 170, (-5, 200), (-10, 14), 1.0, "PLAN OF ONE ANGLE, 1:1 (RAIL LEG FLAT)")
    rect(ax, 0, 0, 186, 10, "white", lw=0.8)
    for x in (20, 93, 166): circle(ax, x, 4, 1.3, fill="white").set_zorder(4)              # rail leg, 7.5 from the plate face (y 11.5)
    rect(ax, 0, 10, 186, 1.5, "white", lw=0.8, hatch="////")
    for x in (22, 87, 152): ax.plot([x, x], [10, 11.5], color=INK, lw=0.6, dashes=(1, 1))  # plate-leg holes, seen edge on
    dim_h(ax, 0, 186, -3.5, "186", ext_from=0, fontsize=7)
    dim_h(ax, 0, 20, -1.5, "20", ext_from=4, fontsize=6.5); dim_h(ax, 20, 93, -1.5, "73", ext_from=4, fontsize=6.5); dim_h(ax, 93, 166, -1.5, "73", ext_from=4, fontsize=6.5)
    dim_h(ax, 0, 22, 12.5, "22", ext_from=10, fontsize=7); dim_h(ax, 22, 87, 12.5, "65", ext_from=10, fontsize=7); dim_h(ax, 87, 152, 12.5, "65", ext_from=10, fontsize=7)
    dim_v(ax, 4, 11.5, 189, "7.5", ext_from=186, fontsize=6.5)
    leader(ax, (93, 2.7), (100, -8.5), "3 x Ø2.6 IN THE RAIL LEG AT 20 / 93 / 166 (RAIL SCREWS); 3 x Ø3.4 IN THE PLATE LEG AT 22 / 87 / 152 (DIMS ABOVE)", fontsize=6.5)
    S = 4.0
    ax = view(22, 60, (-12, 14), (-18, 2), S, "SECTION ACROSS THE LANE AT THE LOWER RAIL (4:1): PLATE, ANGLE, RAIL, TRACK")
    rect(ax, -5, -16, 5, 18, "white", lw=0.8, hatch="////")                               # plate P1 (z 55-60), y to 15.4 (cut off)
    rect(ax, 0, -13.3, 20 - 6, 5, "white", lw=0.8, hatch="\\\\")                        # rail z 60-74 (cut off at 74)
    rect(ax, 0, -6.8, 1.5, 6.5, "white", lw=0.8)                                          # plate leg of the angle, 6.5 tall, on the plate face
    rect(ax, 0, -8.3, 10, 1.5, "white", lw=0.8)                                            # rail leg on top of the lower rail
    rect(ax, 2.5, -16.7, 11.5, 3.4, "white", lw=0.6, hatch="....")                        # track lower run, teeth down onto the rail (z 62.5-77.5 cut off)
    for k in range(3): rect(ax, 3.5 + k * 4, -13.3, 2.0, -2.0, "white", lw=0.4)
    ax.plot([0, 0], [-13.3, -8.3], color=INK, lw=0.4)
    dim_v(ax, -13.3, -8.3, -7.5, "5 RAIL", ext_from=0, fontsize=6.5)
    dim_v(ax, -6.8, -0.3, -9.5, "6.5 LEG", ext_from=0, fontsize=6.5)
    dim_h(ax, 0, 10, 0.8, "10", ext_from=-6.8, fontsize=6.5)
    dim_h(ax, -5, 0, -17.5, "5", ext_from=-16, fontsize=6.5)
    leader(ax, (0.75, -3.5), (4, -2), "M3 x 6 INTO THE PLATE AT y -3.5 (3 OFF)", fontsize=6.5)
    leader(ax, (7.5, -7.6), (8, -4.5), "3 x 5 THREAD-FORMING INTO THE RAIL (3 OFF), PILOT 2.2 x 4 DEEP, BLIND", fontsize=6.5)
    leader(ax, (8, -15), (9, -17.6), "TRACK, TOOTH TIPS ON THE RAIL FACE y -13.3", fontsize=6.5)
    ax.text(-4.8, 1.4, "PLATE", fontsize=6, va="bottom"); ax.text(10.5, -11.5, "RAIL (UHMW)", fontsize=6)
    save(fig, "TS-10_rail_carrier")


# ------------------------------------------------------------------ TS-11 stack-ups and fits (the spacing between parts)
def sheet_stackup():
    fig, view, bg = a3_sheet("STACK-UPS AND FITS: HINGE SHAFT AND IDLER SCREW", "TS-11", material="SEE PARTS", finish="-", qty="PER SIDE", scale="2:1", notes=[
        "FITS: 688-2RS SEATS IN P1, P2, P17 LASER-CUT Ø15.8 THEN REAMED Ø16 H7, RETAINED WITH LOCTITE 641. HINGE PULLEYS Ø8 H7 ON A PLAIN Ø8 h7 ROUND SHAFT (NO D-FLAT, NO GROOVES).",
        "IDLER PULLEYS Ø16 H7, 688-2RS LIGHT PRESS. SLOTS 8.1 (+0.1 / 0) FOR THE Ø8 f9 SHOULDER. LANE 20.0 +-0.2 = (160 - 110) / 2 - 5 FROM THE BAR CUT LENGTHS: CUT BARS TO +-0.1 AND SQUARE.",
        "AXIAL LOCATION ON THE HINGE SHAFT: PINS, NOT E-CLIPS. PIN THE FRONT HINGE PULLEY FIRST: ONE 8x11x0.5 SHIM AGAINST THE P1 BEARING, 0.3-0.5 FEELER GAP TO THE P2 BEARING. THAT FIXES THE SHAFT.",
        "THEN PIN THE REAR PULLEY (0.3-0.5 GAP TO ITS BEARING) AND THE STAGE-2 PULLEY (1 MM SHIM AGAINST THE P17 BEARING). SHIMS BEAR ON INNER RINGS ONLY: NO PULLEY FACE ON AN OUTER RING OR A PLATE.",
        "IDLER SCREW: SHOULDER 25 vs STACK 25.5 (HEAD WASHER 1 + BEARINGS 10 + SLEEVE 9 + SHIM 0.5 + PLATE 5): THE NUT CLAMPS THE INNER-RING STACK AGAINST THE PLATE, AS INTENDED. KEEP THE 0.5 SHIM.",
        "IDLER FLANGE MEETS THE RAIL END IF THE IDLER IS PUSHED IN PAST x 223: RAILS TRIMMED TO 186 (TS-10), TENSIONER TS-09 ONLY EVER PUSHES OUTWARD.",
    ])
    S = 2.0
    # hinge shaft, B side: z along the sheet x, y vertical
    ax = view(22, 150, (26, 110), (-20, 22), S, "SECTION ALONG THE HINGE SHAFT P20-B, FROM THE CENTRE (z 28.7) OUTWARD TO 106. PINS REPLACE THE E-CLIPS.")
    rect(ax, 28.7, -4, 77.3, 8, "white", lw=0.8)                                           # shaft
    rect(ax, 30.2, -8.8, 9.8, 17.6, "white", lw=0.8, hatch="////")                          # M3 stage-2 pulley
    rect(ax, 40, -5.5, 1, 11, "white", lw=0.6)                                              # shim 1
    rect(ax, 41, -12, 5, 30, "white", lw=0.8, hatch="\\\\")                              # P17 plate face
    rect(ax, 41, -8, 5, 16, "white", lw=0.6)                                                # bearing in P17
    rect(ax, 55, -15, 5, 30.4, "white", lw=0.8, hatch="\\\\")                            # front plate
    rect(ax, 55, -8, 5, 16, "white", lw=0.6)                                                # bearing
    rect(ax, 60, -5.5, 0.5, 11, "white", lw=0.6)                                            # shim 0.5
    for z0 in (60.5, 85.5):
        rect(ax, z0, -17.85, 1.5, 35.7, "white", lw=0.6); rect(ax, z0 + 17.5, -17.85, 1.5, 35.7, "white", lw=0.6)
        rect(ax, z0 + 1.5, -15.3, 16, 30.6, "white", lw=0.8, hatch="////")
    rect(ax, 80, -15, 5, 30.4, "white", lw=0.8, hatch="\\\\"); rect(ax, 80, -8, 5, 16, "white", lw=0.6)
    for zc in (70, 95): rect(ax, zc - 1.25, -12, 2.5, 24, "white", lw=0.6)               # hinge pulley pins 2.5 x 24
    rect(ax, 35.1 - 1.25, -6, 2.5, 12, "white", lw=0.6)                                     # stage-2 pin 2.5 x 12 (tooth roots about Ø13.4)
    for z in (46, 55, 60.5, 79.5, 80, 85, 85.5): ax.plot([z, z], [-19, 19], color=DIM, lw=0.3, dashes=(2, 2))
    y = -19.5
    for a, b, t in ((28.7, 30.2, "1.5"), (30.2, 40, "9.8"), (40, 41, "1"), (41, 46, "5"), (46, 55, "9"), (55, 60, "5"), (60, 60.5, ".5"), (60.5, 79.5, "19"), (79.5, 80, ".5"), (80, 85, "5"), (85, 85.5, ".5"), (85.5, 104.5, "19"), (104.5, 106, "1.5")):
        dim_h(ax, a, b, y, t, fontsize=5.5)
    dim_h(ax, 28.7, 106, 21, "77.3 (P20-B)", ext_from=4, fontsize=6.5)
    for z, t in ((35.1, "STAGE-2\nPULLEY M3"), (43.5, "P17 +\n688"), (57.5, "P1 +\n688"), (70, "FRONT HINGE\nPULLEY M1"), (82.5, "P2 +\n688"), (95, "REAR HINGE\nPULLEY M1")):
        ax.text(z, 18.5, t, fontsize=5.5, ha="center", va="bottom")
    leader(ax, (70, 12), (64, -16.5), "PINS Ø2.5 AT MID-FACE, 3 OFF PER SHAFT:\nx 24 IN THE HINGE PULLEYS, x 12 IN THE STAGE-2", fontsize=6)
    leader(ax, (60.25, 5.5), (48, 14), "SHIM 8x11x0.5 ON THE INNER RING", fontsize=6)
    leader(ax, (79.75, 0), (96, -13), "0.3-0.5 FEELER GAP (NO SHIM)", fontsize=6)
    # idler screw, B side nose
    ax = view(22, 60, (42, 90), (-16, 16), S, "SECTION ALONG THE NOSE IDLER SCREW (ISO 7379 8 x 25 M6), INBOARD TO OUTBOARD")
    rect(ax, 44.5, -3, 11, 6, "white", lw=0.5, hatch="....")                                 # M6 thread
    rect(ax, 55.5, -4, 25, 8, "white", lw=0.8)                                               # shoulder
    rect(ax, 80.5, -6.5, 5.5, 13, "white", lw=0.8, hatch="////")                             # head
    rect(ax, 46, -5, 6, 10, "white", lw=0.8)                                                 # nut
    rect(ax, 52, -13, 3, 16, "white", lw=0.8)                                                # slider (TS-09)
    rect(ax, 55, -15, 5, 30.4 - 15, "white", lw=0.8, hatch="\\\\")                       # plate (cut)
    rect(ax, 60, -5.5, 0.5, 11, "white", lw=0.6)                                             # shim
    rect(ax, 60.5, -8, 5, 16, "white", lw=0.6); rect(ax, 74.5, -8, 5, 16, "white", lw=0.6)   # bearings
    rect(ax, 65.5, -5, 9, 10, "white", lw=0.6)                                               # sleeve
    rect(ax, 60.5, -17.85, 1.5, 35.7 / 2 + 2.85, "white", lw=0.6); rect(ax, 78, -17.85, 1.5, 35.7 / 2 + 2.85, "white", lw=0.6)
    rect(ax, 62, -15.3, 16, 15.3 + 8, "white", lw=0.8, hatch="////")                         # pulley body (cut at the top)
    rect(ax, 79.5, -5.5, 1, 11, "white", lw=0.6)                                             # head washer
    y = -15.5
    for a, b, t in ((46, 52, "6"), (52, 55, "3"), (55, 60, "5"), (60, 60.5, ".5"), (60.5, 65.5, "5"), (65.5, 74.5, "9"), (74.5, 79.5, "5"), (79.5, 80.5, "1"), (80.5, 86, "5.5")):
        dim_h(ax, a, b, y, t, fontsize=5.5)
    dim_h(ax, 55.5, 80.5, 13, "SHOULDER 25", ext_from=4, fontsize=6.5)
    dim_h(ax, 55, 80.5, 10, "STACK 25.5", ext_from=4, fontsize=6.5)
    for z, t in ((49, "NYLOC"), (53.5, "SLIDER"), (57.5, "P1"), (63, "688"), (70, "SLEEVE\n8x10x9"), (77, "688"), (83, "HEAD")):
        ax.text(z, -9.5 if t in ("688", "SLEEVE\n8x10x9") else 7, t, fontsize=5.5, ha="center", va="center")
    # fits table
    rows = [("P1 / P2 / P17 bearing seat", "laser Ø15.8, ream Ø16 H7", "688-2RS, Loctite 641"), ("hinge pulley bore M1, stage-2 M3", "ream Ø8 H7", "shaft Ø8 h7 round, pinned"),
            ("idler pulley bore M2", "bore Ø16 H7", "2 x 688-2RS, light press"), ("plate slot", "8.1 +0.1 / 0 wide", "shoulder Ø8 f9"), ("lane, plate face to plate face", "20.0 +-0.2", "pulley 19.0: 0.5 each side"),
            ("pulley to bearing gaps", "0.5 shim + 0.3-0.5 feeler", "never on the outer ring"), ("rail end to idler flange", "rail 186, idler >= x 223", "2 mm minimum"), ("deck over the front track", "25 above axis", "printed 19.7 / belt 25.0")]
    y0 = 262
    bg.text(250, y0 + 4, "FITS AND CLEARANCES", fontsize=7.5, fontweight="bold", va="bottom")
    for i, (a, b, c) in enumerate(rows):
        yy = y0 - 6 * i
        bg.text(250, yy, a, fontsize=6, va="center"); bg.text(318, yy, b, fontsize=6, va="center"); bg.text(366, yy, c, fontsize=6, va="center")
    save(fig, "TS-11_stackup")


# ------------------------------------------------------------------ TS-07 bearing (bought)
def sheet_bearing():
    OD, ID, Wd = BR["outside_dia_mm"], BR["bore_mm"], BR["width_mm"]
    fig, view, bg = a3_sheet("BALL BEARING 608ZZ (BOUGHT)", "TS-07", material="BEARING STEEL (VENDOR'S)", finish="SHIELDED (ZZ)", qty=BR["qty_total"], scale="3:1", notes=[
        "BOUGHT PART. 608ZZ, 8 x 22 x 7, SHIELDED BOTH SIDES. RS SINGAPORE (RS PRO 608-2Z) OR WHEELER MECTRADE / SKF (APPROVED VENDORS). ABOUT S$3 EACH.",
        "QTY 10: 8 PRESSED INTO THE SIDE PLATE POCKETS (2 PER PLATE, TS-02 / TS-03), 2 IN THE BOX WALLS FOR THE HINGE CROSS SHAFT (TS-04).",
        "POCKET Ø22.2 THRU IN THE PETG PLATE = OD + 0.2, A LIGHT PRESS. THE R14.5 BOSS GIVES A 3.4 WALL. MEASURE THE FIRST PRINT; REAM IF TIGHT, GLUE (CA) IF LOOSE.",
        "REPLACES THE KFL08 FLANGE BLOCK ON THE QUOTATION SLIDE: 48 x 26 x 12 DOES NOT FIT IN THE 9 MM BETWEEN THE BOX (Z 40) AND THE FIRST TRACK (Z 49).",
    ])
    S = 3.0
    ax = view(40, 110, (-16, 16), (-16, 16), S, "FRONT VIEW")
    circle(ax, 0, 0, OD / 2, fill="white")
    circle(ax, 0, 0, OD / 2 - 2.2, fill="white", lw=0.5)
    circle(ax, 0, 0, ID / 2 + 2.2, fill="white", lw=0.5)
    circle(ax, 0, 0, ID / 2, fill="white")
    centre_mark(ax, 0, 0, 14)
    dim_dia(ax, 0, 0, OD / 2, 45, f"Ø{OD:g}", length=15.5)
    dim_dia(ax, 0, 0, ID / 2, -45, f"Ø{ID:g}", length=15.5)
    ax = view(150, 110, (-4, 12), (-16, 16), S, "SECTION")
    for sgn in (1, -1):
        rect(ax, 0, sgn * (OD / 2 - 2.2) if sgn > 0 else -OD / 2, Wd, 2.2, "white", hatch=True)                # outer race
        rect(ax, 0, sgn * ID / 2 if sgn > 0 else -(ID / 2 + 2.2), Wd, 2.2, "white", hatch=True)              # inner race
        circle(ax, Wd / 2, sgn * (ID / 2 + 2.2 + (OD / 2 - 2.2 - ID / 2 - 2.2) / 2), 1.9, fill="white", lw=0.6)
        for x in (0.6, Wd - 0.6):
            ax.plot([x, x], [sgn * (ID / 2 + 2.2), sgn * (OD / 2 - 2.2)], color=INK, lw=0.5)
    centreline(ax, -3, 0, Wd + 3, 0)
    dim_h(ax, 0, Wd, OD / 2 + 2.5, f"{Wd:g}", ext_from=OD / 2)
    leader(ax, (0.6, 9), (-3.5, 14), "SHIELD (ZZ) BOTH SIDES", fontsize=7)
    ax = view(240, 90, (-8, 36), (-18, 30), S * 0.8, "FITTED IN THE PLATE POCKET (2.4:1)")
    rect(ax, 0, -BOSS_R, T, BOSS_R - POCKET / 2, "white", hatch=True)
    rect(ax, 0, POCKET / 2, T, 22 - POCKET / 2, "white", hatch=True)
    ax.plot([0, T], [22, 22], color="white", lw=1.5, zorder=4)
    for sgn in (1, -1):
        rect(ax, 0, sgn * (OD / 2 - 2.2) if sgn > 0 else -OD / 2, Wd, 2.2, "white", lw=0.6)
        rect(ax, 0, sgn * ID / 2 if sgn > 0 else -(ID / 2 + 2.2), Wd, 2.2, "white", lw=0.6)
    rect(ax, -5, -ID / 2, 32, ID, "white", lw=0.6)                                                           # axle
    for x in (-5, 27):
        ax.plot([x, x], [-ID / 2, ID / 2], color="white", lw=1.5, zorder=4)
    rect(ax, 8, -FL_R, FL_T, 2 * FL_R, "white", lw=0.5)                                                     # pulley flange, 1 mm from the plate
    ax.text(12, FL_R - 6, "PULLEY FLANGE\n(REF), 1 OFF\nTHE PLATE", fontsize=6, ha="left", va="top")
    ax.text(-1, -7.2, "AXLE Ø8 (REF)", fontsize=6, ha="left", va="top")
    centreline(ax, -7, 0, 34, 0)
    dim_h(ax, 0, T, 25, f"PLATE {T:g} = BEARING {Wd:g}", ext_from=22, fontsize=7)
    dim_v(ax, -POCKET / 2, POCKET / 2, -4, f"Ø{POCKET:g}", ext_from=0, fontsize=7)
    dim_v(ax, -BOSS_R, -POCKET / 2, 22, f"{BOSS_R - POCKET / 2:g} WALL", ext_from=T, fontsize=7)
    save(fig, "TS-07_bearing_608ZZ")


# ------------------------------------------------------------------ TS-08 rear segment to base
def sheet_rear_to_base():
    fig, view, bg = a3_sheet("REAR SEGMENT TO THE BOX", "TS-08", material="SEE TS-00", qty="1", scale="1.5:1 SECTIONS, 1:2 SIDE", notes=[
        "ATTACHMENT: THE REAR SEGMENT BOLTS TO THE BOX BY ITS TWO CROSS-BAR RODS (M4 x 238), NUT + WASHER EACH END:",
        "PLATE - 65 SPACER - BOX WALL - BOX WALL - 65 SPACER - PLATE. BOX NEEDS 2 x Ø4.5 HOLES PER WALL AT X 60 AND 200, 28 ABOVE THE AXLE.",
        "THE FRONT SEGMENT IS HELD ONLY BY THE MIDDLE AXLE (HINGE) AND THE SECTOR GEARS, SO IT CAN SWING.",
        "ONE SIDE SHOWN (Z FROM THE CENTRE LINE), THE OTHER MIRRORS. BOX, SECTOR GEAR AND PINION: TEAM'S PARTS, DASHED.",
    ])
    S = 1.5
    fz1, fzb, fz2 = lane_bands(Z["front_lane"])
    rz1, rzb, rz2 = lane_bands(Z["rear_lane"])
    fp, rp, fh, rh = Z["front_plate"], Z["rear_plate"], Z["front_hub"], Z["rear_hub"]
    half = AX["lengths_mm"]["middle"] / 2
    BOX_Z, BOX_Z_MID = 40.0, 37.0

    def plate_cut(ax, z0):
        for y0, y1 in ((-BOSS_R, -BR["outside_dia_mm"] / 2 - 0.1), (BR["outside_dia_mm"] / 2 + 0.1, ABOVE)):
            rect(ax, z0, y0, T, y1 - y0, "white", hatch=True)
        for sgn in (1, -1):                                   # 608 races
            rect(ax, z0, sgn * (BR["outside_dia_mm"] / 2 - 2.2) if sgn > 0 else -BR["outside_dia_mm"] / 2, T, 2.2, "white", lw=0.5)
            rect(ax, z0, sgn * 4 if sgn > 0 else -6.2, T, 2.2, "white", lw=0.5)
            circle(ax, z0 + T / 2, sgn * 8.1, 1.7, fill="white", lw=0.5)

    def pulley_cut(ax, b1, bb, b2, hub):
        for sgn in (1, -1):
            pts = [(b1[0], sgn * 4), (b1[0], sgn * FL_R), (b1[1], sgn * FL_R), (b1[1], sgn * PU_OD_R), (b2[0], sgn * PU_OD_R), (b2[0], sgn * FL_R),
                   (b2[1], sgn * FL_R), (b2[1], sgn * HUB_R), (hub[1], sgn * HUB_R), (hub[1], sgn * 4)]
            ax.add_patch(Polygon(pts, closed=True, fc="white", ec=INK, lw=0.7, hatch="////", zorder=3))
            rect(ax, bb[0], sgn * R_TOOTH if sgn > 0 else -R_TIP, TRK_W, R_TIP - R_TOOTH, "white", hatch=True, zorder=4)   # track wrapped on the pulley
        for k in range(1, 4):                                 # cleats on the top run
            x = bb[0] + 2 + k * 3.5
            ax.plot([x, x], [R_FACE, R_TIP], color=INK, lw=0.3)

    # ---- SECTION A-A through the middle axle
    ax = view(20, 160, (-8, 124), (-28, 46), S, "SECTION A-A THROUGH THE MIDDLE AXLE (HINGE), 1.5:1")
    rect(ax, 0, -4, half + 3, 8, "white", lw=0.7, zorder=5)                                            # axle (not hatched: solid shaft)
    hidden_rect(ax, 0, 6, BOX_Z_MID, 28)
    ax.text(18, 20, "BOX (REF)\nSTOPS AT Z 37 HERE", fontsize=6, ha="center", va="center")
    hidden_rect(ax, 38, -25, 3, 50)
    ax.text(39.5, -26.5, "SECTOR GEAR 3 THICK (REF)", fontsize=5.5, ha="center", va="top", rotation=0)
    plate_cut(ax, fp[0])
    pulley_cut(ax, fz1, fzb, fz2, fh)
    pulley_cut(ax, rz1, rzb, rz2, rh)
    plate_cut(ax, rp[0])
    rect(ax, fp[0], 0, T, 0, "white")  # no-op keeps order
    for z in (fp[0] + 3.5, rp[0] + 3.5):                                                                 # M3 sector bolt (front plate) / nothing on rear
        pass
    rect(ax, 38, 15, 10, 3.4, "white", lw=0.5, zorder=6)                                                 # M3 x 14 through sector gear + plate, nut outboard
    rect(ax, 48, 14.5, 2.4, 4.4, "white", lw=0.5, zorder=6)
    leader(ax, (43, 18.4), (2, 8), "M3 x 14 + NUT, 3 PER PLATE, ON R17\n(SECTOR GEAR TO FRONT PLATE)", fontsize=6)
    centreline(ax, -6, 0, 122, 0)
    y0 = -26
    for (z0, z1), lab in ((fp, "7"), (Z["front_lane"], "20"), (Z["rear_lane"], "20"), (rp, "7")):
        dim_h(ax, z0, z1, y0, lab, ext_from=-R_TIP - 1, fontsize=6.5)
    dim_h(ax, 0, BOX_Z, 37, "40 BOX", ext_from=34, fontsize=6.5)
    dim_h(ax, 0, rzb[1], 40.5, "97 (194 OVER TRACKS)", ext_from=R_TIP, fontsize=6.5)
    dim_h(ax, 0, rp[1], 44.5, "112 (224 OVER PLATES)", ext_from=ABOVE, fontsize=6.5)
    for z, t in ((fz1[0], "49"), (fz2[1], "69"), (rz1[0], "77"), (rz2[1], "97"), (rp[0], "105")):
        ax.text(z, -R_TIP - 2.2, t, fontsize=5, ha="center", va="top")
    leader(ax, (fzb[0] + 7, R_TIP), (54, 31), "TRACK ON ITS PULLEY", fontsize=6)
    leader(ax, (rh[1] - 2, HUB_R), (104, 30), "SET SCREW HUB", fontsize=6)
    leader(ax, (rp[0] + 3.5, BR["outside_dia_mm"] / 2 - 1), (100, -22), "608ZZ IN THE PLATE", fontsize=6)

    # ---- SECTION B-B through the rear cross bar (x = 60 from the rear axle)
    ax = view(20, 40, (-8, 124), (-28, 46), S, "SECTION B-B THROUGH A REAR CROSS BAR (X 60 FROM THE REAR AXLE), 1.5:1")
    rail_z = ((Z["rear_lane"][0] + Z["rear_lane"][1]) / 2 - RW / 2, (Z["rear_lane"][0] + Z["rear_lane"][1]) / 2 + RW / 2)
    rect(ax, rp[0], -BELOW, T, BELOW + ABOVE, "white", hatch=True)                                         # rear plate
    rect(ax, rail_z[1], -RBOT, rp[1] - rail_z[1], RBOT - BELOW, "white", hatch=True)                       # web
    rect(ax, rail_z[0], -RBOT, RW, RT, "white", hatch=True)                                                # rail
    for yy0 in (R_TOOTH, -R_TIP):                                                                          # track upper and lower runs, cut
        rect(ax, rzb[0], yy0, TRK_W, R_TIP - R_TOOTH, "white", hatch=True, zorder=4)
    hidden_rect(ax, 0, 6, BOX_Z, 38)
    ax.text(20, 12, "BOX (REF)", fontsize=6, ha="center")
    yb = CBH["above_axle_mm"]
    rect(ax, 0, yb - 2, CB["rear_segment"]["rod_length_mm"] / 2, 4, "white", lw=0.6, zorder=5)             # rod (solid)
    rect(ax, BOX_Z, yb - 5, CB["rear_segment"]["spacer_length_mm"], 10, "white", hatch=True, zorder=4)     # 65 spacer, cut
    rect(ax, BOX_Z, yb - 2.25, CB["rear_segment"]["spacer_length_mm"], 4.5, "white", lw=0.4, zorder=5)
    rect(ax, rp[1], yb - 4.5, 0.8, 9, "white", lw=0.5, zorder=6)                                           # washer
    rect(ax, rp[1] + 0.8, yb - 3.5, 3.2, 7, "white", lw=0.5, zorder=6)                                     # nut
    rect(ax, BOX_Z - 2, yb - 2.25, 2, 4.5, "white", lw=0.4, zorder=5)                                      # hole in the box wall
    centreline(ax, -6, 0, 122, 0)
    dim_v(ax, 0, yb, 120, "28", fontsize=6.5)
    dim_h(ax, BOX_Z, rp[0], yb + 8, "65 SPACER", ext_from=yb + 5, fontsize=6.5)
    dim_h(ax, 0, CB["rear_segment"]["rod_length_mm"] / 2, yb + 15, "119 (ROD 238)", ext_from=yb + 2, fontsize=6.5)
    dim_h(ax, rail_z[0], rail_z[1], -RBOT - 4, "18 RAIL", ext_from=-RBOT, fontsize=6.5)
    dim_v(ax, -RTOP, 0, rail_z[0] - 4, "13.34", fontsize=6.5)
    leader(ax, (rzb[0] + 7, -R_TOOTH - 3), (50, -24), "LOWER RUN RIDES ON THE RAIL", fontsize=6)
    leader(ax, (rp[1] + 2.4, yb + 3.5), (100, 42), "M4 NUT + WASHER", fontsize=6)
    leader(ax, (BOX_Z - 1, yb + 2.25), (12, 36), "Ø4.5 HOLE IN THE BOX WALL", fontsize=6)

    # ---- SIDE VIEW of the rear segment on the box, 1:2
    ax = view(232, 120, (-60, 290), (-50, 100), 0.5, "SIDE VIEW, REAR SEGMENT ON THE BOX (FROM OUTBOARD), 1:2")
    shape_patch(ax, plate_shape(), zorder=1)
    track_side(ax, zorder=3)
    for x in (0, C):
        circle(ax, x, 0, FL_R, fill="white", lw=0.6, zorder=4)
        circle(ax, x, 0, HUB_R, fill="white", lw=0.6, zorder=5)
        circle(ax, x, 0, 4, fill="white", lw=0.6, zorder=6)
        centre_mark(ax, x, 0, 26)
    for x in CBH["at_x_mm"]:
        hex_nut(ax, x, CBH["above_axle_mm"])
    hidden_rect(ax, -30, 6, C + 60, 80)
    ax.text(100, 70, "BOX (REF), BOLTED THROUGH THE TWO CROSS BARS", fontsize=6, ha="center")
    hidden_circle(ax, C, 0, 25)
    ax.text(C, 48, "FRONT SEGMENT HINGES HERE\n(MIDDLE AXLE)", fontsize=5.5, ha="center", va="bottom")
    centreline(ax, -40, 0, C + 40, 0)
    section_mark(ax, C, -40, 95, "A", side=1)
    section_mark(ax, CBH["at_x_mm"][0], -40, 95, "B", side=-1)
    dim_h(ax, 0, CBH["at_x_mm"][0], -34, "60", ext_from=-22, fontsize=6.5)
    dim_h(ax, 0, CBH["at_x_mm"][1], -42, "200", ext_from=-22, fontsize=6.5)
    ax.text(-55, -48, "REAR AXLE AT X 0, MIDDLE AXLE AT X 225", fontsize=6, va="bottom")
    save(fig, "TS-08_rear_segment_to_base")


# ------------------------------------------------------------------ TS-12 hinge shafts and rail drilling (what Nazim makes from bar and strip)
def sheet_shafts_rails():
    fig, view, bg = a3_sheet("HINGE SHAFTS A + B, RAIL TRIM AND PILOTS", "TS-12", material="Ø8 h7 GROUND STEEL; UHMW-PE 20 x 5", finish="DEBURRED", qty="2 SHAFTS, 8 RAILS", scale="1:1, DETAILS 4:1", notes=[
        "SHAFTS: CUT BOTH FROM ONE 300 MM Ø8 h7 GROUND SHAFT: A = 82.3, B = 77.3 (+-0.1). FACE SQUARE, CHAMFER 0.5 x 45° BOTH ENDS.\n    PLAIN ROUND: NO D-FLAT, NO E-CLIP GROOVES. KEEP THE GROUND SURFACE CLEAN: IT RUNS IN THE 688 BEARINGS.",
        "DO NOT DRILL THE Ø2.5 PIN HOLES NOW. AT ASSEMBLY EACH ONE IS DRILLED THROUGH THE SHAFT USING THE PULLEY'S HUB HOLE AS THE GUIDE,\n    AFTER THE SHIM AND FEELER GAP ARE SET (TS-11). THE PIN POSITIONS SHOWN ON B ARE NOMINAL, FOR REFERENCE ONLY; A IS THE SAME STACK.",
        "RAILS: MISUMI UPA-189-20-5. CUT 3 OFF THE IDLER END: 186 LONG. THE SAME PART SERVES AS UPPER AND LOWER RAIL: DRILL THE FACE\n    AWAY FROM THE TRACK, WHERE THE CARRIER ANGLE SITS (TS-10). MARK THE HINGE END AND THE PLATE EDGE ON EACH RAIL BEFORE DRILLING.",
        "PILOTS Ø2.2 x 4 DEEP, BLIND, WITH A DEPTH STOP: THE OTHER FACE IS WHAT THE TRACK SLIDES ON AND MUST STAY UNBROKEN.\n    DO NOT DRILL THE REV B SHEET 18 PILOTS: THEY OVERLAP THESE AT 20 / 22 AND 166 / 167.",
    ])
    D = 8.0
    for y, L, name, pins in ((222, 82.3, "SHAFT P20-A, 82.3, QTY 1 (1:1)", None),
                             (178, 77.3, "SHAFT P20-B, 77.3, QTY 1 (1:1). PIN POSITIONS NOMINAL, DRILLED AT ASSEMBLY", ((6.4, "STAGE-2 PULLEY, PIN 2.5 x 12"), (41.3, "FRONT HINGE WHEEL, PIN 2.5 x 24"), (66.3, "REAR HINGE WHEEL, PIN 2.5 x 24")))):
        ax = view(22, y, (-6, 100), (-14, 14), 1.0, name)
        ax.add_patch(Polygon([(0.5, -D / 2), (L - 0.5, -D / 2), (L, -D / 2 + 0.5), (L, D / 2 - 0.5), (L - 0.5, D / 2), (0.5, D / 2), (0, D / 2 - 0.5), (0, -D / 2 + 0.5)], closed=True, fc="white", ec=INK, lw=0.8))
        for xx in (0.5, L - 0.5): ax.plot([xx, xx], [-D / 2, D / 2], color=INK, lw=0.4)
        centreline(ax, -4, 0, L + 4, 0)
        dim_h(ax, 0, L, -10, f"{L:g}", ext_from=-D / 2, fontsize=7)
        dim_v(ax, -D / 2, D / 2, L + 6, "Ø8 h7", ext_from=L, fontsize=7)
        if pins:
            for k, (x, lab) in enumerate(pins):
                ax.plot([x, x], [-D / 2 - 1, D / 2 + 1], color=INK, lw=0.5, dashes=(2, 1.5))
                leader(ax, (x, D / 2), (x + 2, 9 + (k % 2) * 3.5), f"{x:g}: {lab}", fontsize=5.5)
            ax.text(-1, -D / 2 - 1, "INNER END", fontsize=5.5, ha="left", va="top")
    ax = view(150, 120, (-4, 7), (-6, 6), 4.0, "DETAIL: SHAFT END (4:1)")
    ax.add_patch(Polygon([(-4, -4), (-0.5, -4), (0, -3.5), (0, 3.5), (-0.5, 4), (-4, 4)], closed=True, fc="white", ec=INK, lw=0.8))
    centreline(ax, -4, 0, 2, 0)
    leader(ax, (-0.25, 3.75), (1.5, 5), "0.5 x 45°, BOTH ENDS", fontsize=6.5)
    # rail plan: hinge end at x 0, plate edge on top (y 20)
    ax = view(22, 72, (-10, 205), (-9, 30), 1.0, "RAIL P3-P6, DRILLING FACE UP (1:1). PLATE EDGE AT THE TOP, HINGE END ON THE LEFT")
    rect(ax, 0, 0, 186, 20, "white")
    rect(ax, 186, 0, 3, 20, "white", lw=0.4, hatch="////")
    for x in (20, 93, 166): circle(ax, x, 12.5, 1.1, fill="white")
    dim_h(ax, 0, 20, -4, "20", ext_from=0, fontsize=6.5); dim_h(ax, 20, 93, -4, "73", ext_from=0, fontsize=6.5); dim_h(ax, 93, 166, -4, "73", ext_from=0, fontsize=6.5)
    dim_h(ax, 0, 186, -8, "186", ext_from=0, fontsize=7)
    dim_v(ax, 12.5, 20, -5, "7.5", ext_from=0, fontsize=6.5)
    dim_v(ax, 0, 20, 194, "20", ext_from=189, fontsize=6.5)
    ax.text(93, 22, "PLATE EDGE (AGAINST THE CARRIER ANGLE'S PLATE LEG)", fontsize=6, ha="center", va="bottom")
    leader(ax, (187.5, 16), (170, 27), "CUT OFF 3 (189 TO 186), IDLER END", fontsize=6)
    leader(ax, (93, 13.6), (110, 26.5), "3 x Ø2.2 x 4 DEEP, BLIND", fontsize=6)
    ax = view(270, 92, (-3, 24), (-8, 10), 4.0, "SECTION THROUGH A PILOT (4:1)")
    rect(ax, 0, -5, 20, 5, "white", hatch="\\\\")
    rect(ax, 12.5 - 1.1, -4, 2.2, 4, "white", lw=0.6)
    ax.plot([12.5 - 1.1, 12.5, 12.5 + 1.1], [-4, -4.6, -4], color=INK, lw=0.6)
    dim_v(ax, -4, 0, 17, "4", ext_from=13.6, fontsize=6.5)
    dim_v(ax, -5, 0, 22, "5", ext_from=20, fontsize=6.5)
    ax.text(10, 1, "DRILLED FACE (CARRIER ANGLE SIDE)", fontsize=6, ha="center", va="bottom")
    ax.text(10, -6, "TRACK SLIDES ON THIS FACE: DO NOT BREAK THROUGH", fontsize=6, ha="center", va="top")
    save(fig, "TS-12_shafts_rails")


# Sheets from the first own-frame layout (608ZZ, printed spacers, own side plates), replaced by Nhien's Rev B frame.
SUPERSEDED = {"TS-00_assembly_front_segment", "TS-02_side_plate_front", "TS-03_side_plate_rear", "TS-04_axles", "TS-05_spacer", "TS-07_bearing_608ZZ", "TS-08_rear_segment_to_base"}
SUPERSEDED_NOTE = "SUPERSEDED 19 OCT 2026: FIRST OWN-FRAME LAYOUT, REPLACED BY NHIEN'S REV B FRAME. DO NOT MAKE FROM THIS SHEET.\nCURRENT SHEETS: TS-01, TS-01B, TS-06, TS-09, TS-10, TS-11, TS-12."
_save = save


def save(fig, name):
    if name in SUPERSEDED:
        fig.text(0.5, 0.52, "SUPERSEDED", fontsize=120, color="#B03A2E", alpha=0.28, rotation=22, ha="center", va="center", fontweight="bold")
        fig.text(0.5, 0.935, SUPERSEDED_NOTE, fontsize=10, color="#B03A2E", ha="center", va="top", fontweight="bold",
                 bbox=dict(boxstyle="square,pad=0.6", fc="white", ec="#B03A2E", lw=1.5))
    return _save(fig, name)


if __name__ == "__main__":
    which = sys.argv[1:] or ["all"]
    fns = dict(assembly=sheet_assembly, track=sheet_track, front=lambda: sheet_side_plate(True), rear=lambda: sheet_side_plate(False),
               axles=sheet_axles, spacer=sheet_spacer, pulley=sheet_pulley, bearing=sheet_bearing, base=sheet_rear_to_base, belt=sheet_belt, tensioner=sheet_tensioner, carrier=sheet_rail_carrier, stackup=sheet_stackup, shafts=sheet_shafts_rails)
    for k, f in fns.items():
        if "all" in which or k in which:
            f()
