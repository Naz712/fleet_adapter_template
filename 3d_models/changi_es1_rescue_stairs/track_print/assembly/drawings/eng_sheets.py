"""CAD-style A3 engineering sheets (TS-00 assembly with balloons and parts list, TS-01..TS-07 one per part).
Monochrome, true scale, third angle. Every number from ../parts_spec.json (v2). Run: python3 eng_sheets.py"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from drawing import DIM, INK, SPEC, centreline, dim_dia, dim_h, dim_v, leader  # noqa: E402
from drawing import circle as _circle, rect as _rect  # noqa: E402
from eng_sheet import a3_sheet, balloon, parts_list, save, section_mark  # noqa: E402
from matplotlib.patches import PathPatch, Polygon, RegularPolygon  # noqa: E402
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
        (8, "M4_ROD_110", "M4 THREADED ROD x 110 + 4 NUTS + 4 WASHERS", 2),
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
    fig, view, bg = a3_sheet("CROSS BAR SPACER", "TS-05", material="PETG, 3D PRINTED", finish="AS PRINTED", qty="2 x 82 + 2 x 210", scale="1:1, DETAIL 3:1", notes=[
        "FILES stl/spacer_front_x2.stl (82) AND stl/spacer_rear_x2.stl (210). PRINT STANDING ON END, 0.2 LAYERS, 3 WALLS, 20% INFILL.",
        "ONE SPACER SITS BETWEEN THE TWO PLATES OF A SEGMENT ON EACH M4 THREADED ROD (ROD 110 FRONT, 238 REAR); THE NUTS OUTSIDE THE PLATES PULL THE PLATES ONTO IT.",
        "LENGTH = INSIDE DISTANCE BETWEEN THE PLATES: FRONT 2 x 41 = 82, REAR 2 x 105 = 210. AT 28 ABOVE THE AXLE IT CLEARS THE UPPER RUN'S CLEAT TIPS BY 3.3.",
        "BORE 4.5 IS A CLEARANCE FOR THE M4 ROD. ENDS SQUARE: THEY SET THE PLATE SPACING.",
    ])
    for y, L, name in ((215, lr, "REAR SEGMENT SPACER, QTY 2"), (165, lf, "FRONT SEGMENT SPACER, QTY 2")):
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
    fig, view, bg = a3_sheet("TIMING PULLEY HTD 5M 20T (BOUGHT)", "TS-06", material="ALUMINIUM (VENDOR'S)", finish="VENDOR'S", qty=8, scale="2:1", notes=[
        "BOUGHT PART. ORDER: HTD 5M, 20 TEETH, FOR 15 MM BELT, 8 MM BORE, FLANGES BOTH SIDES, SET-SCREW HUB. MISUMI SINGAPORE (APPROVED VENDOR). 4 PER SEGMENT.",
        "WHAT MATTERS: 20T HTD 5M (PD 31.83), 15 MM BELT, 8 BORE. FLANGE, HUB AND LENGTH SHOWN ARE THE STAND-IN'S: CHECK THE VENDOR DRAWING.",
        "LAYOUT ALLOWS 20 OVER THE FLANGES AND 7 FOR THE HUB (27 OVERALL) PER PULLEY. A LONGER PULLEY MOVES THE LANES: TELL THE TEAM BEFORE ORDERING.",
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
    rect(ax, 2 * FL_T + PU_FACE + 2, HUB_R - 0.2, 3, -(HUB_R - PU["bore_mm"] / 2) + 0.2, "white", lw=0.4)
    ax.text(2 * FL_T + PU_FACE + 3.5, HUB_R + 0.8, "SET SCREW\n2 x M4", fontsize=6, ha="center", va="bottom")
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


if __name__ == "__main__":
    which = sys.argv[1:] or ["all"]
    fns = dict(assembly=sheet_assembly, track=sheet_track, front=lambda: sheet_side_plate(True), rear=lambda: sheet_side_plate(False),
               axles=sheet_axles, spacer=sheet_spacer, pulley=sheet_pulley, bearing=sheet_bearing)
    for k, f in fns.items():
        if "all" in which or k in which:
            f()
