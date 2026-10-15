"""STEP export of every part and a placed assembly of both track segments, from assembly/parts_spec.json.
STEP (AP214) opens in SolidWorks, Fusion, Onshape and FreeCAD; the assembly STEP comes in as an assembly with
one component per part. Vehicle frame: x forward (middle axle at x = 0), y up (axle centre line at y = 0),
z across (centre line at z = 0). Run: python3 export_step.py  -> step/"""
import json, math
from pathlib import Path
import cadquery as cq
from shapely import affinity
from shapely.geometry import Point, Polygon as SPoly, box as sbox
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
OUT = HERE / "step"; OUT.mkdir(exist_ok=True)
S = json.loads((HERE / "assembly/parts_spec.json").read_text())
P, Z, SEG = S["parts"], S["layout_decision"]["z_stations_one_side_mm"], S["segment"]
TR, PU, AX, BR, SP, CB = P["track"], P["pulley"], P["axle"], P["bearing"], P["side_plate"], P["cross_bar"]
C = SEG["axle_to_axle_mm"]
R_FACE, R_TIP = SEG["axle_to_track_face_mm"], SEG["axle_to_cleat_tip_mm"]
R_ROOT = R_FACE - TR["backing_thickness_mm"]
R_TOOTH = R_ROOT - TR["teeth"]["height_mm"]
R_PITCH = PU["pitch_dia_mm"] / 2
T, BELOW, ABOVE = SP["plate"]["thickness_mm"], SP["plate"]["bottom_edge_below_axle_mm"], SP["plate"]["top_edge_above_axle_mm"]
END_R, BOSS_R, ARC_CY = 20.0, SP["plate"]["boss_radius_mm"], (ABOVE - BELOW) / 2
POCKET = SP["bearing_pockets"]["dia_mm"]
RL = SP["rail"]; RW, RT, RTOP, RBOT, RX0, RX1 = RL["width_mm"], RL["thickness_mm"], RL["top_face_below_axle_mm"], RL["bottom_below_axle_mm"], RL["from_x_mm"], RL["to_x_mm"]
CBH, SB = SP["cross_bar_holes"], SP["sector_bolts"]
FL_T, FL_R, HUB_R, HUB_L, OD_R, FACE = PU["flange_thickness_mm"], PU["flange_dia_mm"] / 2, PU["hub_dia_mm"] / 2, PU["hub_length_mm"], PU["outside_dia_mm"] / 2, PU["face_width_between_flanges_mm"]
TRK_W = TR["width_mm"]


def poly_solid(shape, h):
    """shapely polygon (with holes) -> cq Solid extruded h along +z, from z = 0."""
    def wire(ring):
        pts = [cq.Vector(x, y, 0) for x, y in list(ring.coords)[:-1]]
        return cq.Wire.makePolygon(pts, close=True)
    face = cq.Face.makeFromWires(wire(shape.exterior), [wire(r) for r in shape.interiors])
    return cq.Workplane("XY").add(cq.Solid.extrudeLinear(face, cq.Vector(0, 0, h)))


def tooth():
    r, hgt = TR["teeth"]["tip_radius_mm"], TR["teeth"]["height_mm"]
    return unary_union([sbox(-r, -(hgt - r), r, 0.3), Point(0, -(hgt - r)).buffer(r, quad_segs=12)])


def cleat():
    c = TR["cleats"]; hb, ht = c["base_width_mm"] / 2, c["tip_width_mm"] / 2
    return SPoly([(-hb, -0.3), (hb, -0.3), (ht, c["height_mm"]), (-ht, c["height_mm"])])


def stadium(R):
    return unary_union([sbox(0, -R, C, R), Point(0, 0).buffer(R, quad_segs=48), Point(C, 0).buffer(R, quad_segs=48)])


def loop_point(s):
    arc = math.pi * R_PITCH
    if s < C: return (s, R_PITCH), (0.0, 1.0)
    if s < C + arc:
        a = math.pi / 2 - (s - C) / R_PITCH; return (C + R_PITCH * math.cos(a), R_PITCH * math.sin(a)), (math.cos(a), math.sin(a))
    if s < 2 * C + arc: return (C - (s - C - arc), -R_PITCH), (0.0, -1.0)
    a = -math.pi / 2 - (s - 2 * C - arc) / R_PITCH; return (R_PITCH * math.cos(a), R_PITCH * math.sin(a)), (math.cos(a), math.sin(a))


def track_running():
    """The track in its running shape round two pulleys 225 apart (for the assembly). Local: x along, y up, z 0..15."""
    parts = [stadium(R_FACE).difference(stadium(R_ROOT))]
    for k in range(TR["teeth"]["count"]):
        (px, py), (nx, ny) = loop_point(k * TR["teeth"]["pitch_mm"] + 2.5)
        a = math.degrees(math.atan2(ny, nx)) - 90
        off = R_ROOT - R_PITCH
        parts.append(affinity.translate(affinity.rotate(tooth(), a, origin=(0, 0)), px + nx * off, py + ny * off))
    for k in range(TR["cleats"]["count"]):
        (px, py), (nx, ny) = loop_point(k * TR["cleats"]["pitch_mm"])
        a = math.degrees(math.atan2(ny, nx)) - 90
        off = R_FACE - R_PITCH
        parts.append(affinity.translate(affinity.rotate(cleat(), a, origin=(0, 0)), px + nx * off, py + ny * off))
    return poly_solid(unary_union(parts).buffer(0), TRK_W)


def track_ring():
    """As printed: a ring (same as stl/track_TPU_x4.stl)."""
    ring = TR["as_printed_ring"]; r_od = ring["outside_dia_of_belt_mm"] / 2; r_root = r_od - TR["backing_thickness_mm"]
    parts = [Point(0, 0).buffer(r_od, quad_segs=120).difference(Point(0, 0).buffer(r_root, quad_segs=120))]
    for k in range(TR["teeth"]["count"]):
        parts.append(affinity.rotate(affinity.translate(tooth(), 0, r_root), 360 * k / TR["teeth"]["count"] - 90, origin=(0, 0)))
    for k in range(TR["cleats"]["count"]):
        parts.append(affinity.rotate(affinity.translate(cleat(), 0, r_od), 360 * k / TR["cleats"]["count"] - 90, origin=(0, 0)))
    return poly_solid(unary_union(parts).buffer(0), TRK_W)


def side_plate(front):
    """Local frame: x from the segment's rear axle, y up, z from the plate's inboard face = 0 outwards (left-hand plate)."""
    lane = Z["front_lane" if front else "rear_lane"]; pz0, pz1 = Z["front_plate" if front else "rear_plate"]
    lc = (lane[0] + lane[1]) / 2; rail_z = (lc - RW / 2 - pz0, lc + RW / 2 - pz0)
    web_z = (0, rail_z[0]) if front else (rail_z[1], pz1 - pz0)
    outline = unary_union([sbox(0, -BELOW, C, ABOVE), Point(0, ARC_CY).buffer(END_R, quad_segs=48), Point(C, ARC_CY).buffer(END_R, quad_segs=48),
                           Point(0, 0).buffer(BOSS_R, quad_segs=48), Point(C, 0).buffer(BOSS_R, quad_segs=48)])
    plate = poly_solid(outline, T)
    web = cq.Workplane("XY").box(RX1 - RX0, RBOT - BELOW, web_z[1] - web_z[0], centered=False).translate((RX0, -RBOT, web_z[0]))
    rail = cq.Workplane("XY").box(RX1 - RX0, RT, RW, centered=False).translate((RX0, -RBOT, rail_z[0]))
    body = plate.union(web).union(rail)
    zlo, zhi = min(0, rail_z[0]), max(T, rail_z[1])
    for x in (0, C):
        body = body.cut(cq.Workplane("XY").circle(POCKET / 2).extrude(zhi - zlo + 2).translate((x, 0, zlo - 1)))
    for x in CBH["at_x_mm"]:
        body = body.cut(cq.Workplane("XY").circle(CBH["dia_mm"] / 2).extrude(zhi - zlo + 2).translate((x, CBH["above_axle_mm"], zlo - 1)))
    if front:
        for a in SB["angles_deg"]:
            body = body.cut(cq.Workplane("XY").circle(SB["dia_mm"] / 2).extrude(zhi - zlo + 2)
                            .translate((SB["radius_mm"] * math.cos(math.radians(a)), SB["radius_mm"] * math.sin(math.radians(a)), zlo - 1)))
    return body


def pulley():
    """Local: axis z, inboard flange face at z = 0, hub outboard."""
    b = cq.Workplane("XY").circle(FL_R).extrude(FL_T)
    b = b.union(cq.Workplane("XY").circle(OD_R).extrude(FACE).translate((0, 0, FL_T)))
    b = b.union(cq.Workplane("XY").circle(FL_R).extrude(FL_T).translate((0, 0, FL_T + FACE)))
    b = b.union(cq.Workplane("XY").circle(HUB_R).extrude(HUB_L).translate((0, 0, 2 * FL_T + FACE)))
    for k in range(PU["teeth"]):
        a = 2 * math.pi * k / PU["teeth"]
        b = b.cut(cq.Workplane("XY").circle(1.5).extrude(FACE + 0.2).translate(((OD_R - 0.45) * math.cos(a), (OD_R - 0.45) * math.sin(a), FL_T - 0.1)))
    b = b.cut(cq.Workplane("XY").circle(PU["bore_mm"] / 2).extrude(PU["overall_length_mm"] + 2).translate((0, 0, -1)))
    b = b.cut(cq.Workplane("XZ").circle(1.6).extrude(-HUB_R - 1).translate((0, 0, 2 * FL_T + FACE + HUB_L / 2)))   # set screw hole
    return b


def bearing():
    return cq.Workplane("XY").circle(BR["outside_dia_mm"] / 2).circle(BR["bore_mm"] / 2).extrude(BR["width_mm"])


def axle(length, flats_z):
    a = cq.Workplane("XY").circle(AX["dia_mm"] / 2).extrude(length).translate((0, 0, -length / 2))
    for zc in flats_z:
        a = a.cut(cq.Workplane("XY").box(10, 2, 10).translate((0, AX["dia_mm"] / 2 - 0.5 + 1, zc)))
    return a


def spacer(length):
    return cq.Workplane("XY").circle(CB["front_segment"]["spacer_od_mm"] / 2).circle(CBH["dia_mm"] / 2).extrude(length)


def rod(length):
    return cq.Workplane("XY").circle(2).extrude(length).translate((0, 0, -length / 2))


def nut():
    return cq.Workplane("XY").polygon(6, 7 / math.cos(math.pi / 6)).circle(2).extrude(3.2)


def washer():
    return cq.Workplane("XY").circle(4.5).circle(2.25).extrude(0.8)


# ---------------------------------------------------------------- parts
fh, rh = (Z["front_hub"][0] + Z["front_hub"][1]) / 2, (Z["rear_hub"][0] + Z["rear_hub"][1]) / 2
parts = {
    "track_ring_as_printed": track_ring(),
    "track_running_shape": track_running(),
    "side_plate_front": side_plate(True),
    "side_plate_rear": side_plate(False),
    "pulley_HTD5M_20T_ref": pulley(),
    "bearing_608ZZ_ref": bearing(),
    "axle_middle_230": axle(AX["lengths_mm"]["middle"], [fh, -fh, rh, -rh, 0.0]),
    "axle_rear_230": axle(AX["lengths_mm"]["rear"], [rh, -rh]),
    "axle_front_160": axle(AX["lengths_mm"]["front"], [fh, -fh]),
    "hinge_cross_shaft_120": axle(P["hinge_cross_shaft"]["length_mm"], []),
    "spacer_front_82": spacer(CB["front_segment"]["spacer_length_mm"]),
    "spacer_rear_65": spacer(CB["rear_segment"]["spacer_length_mm"]),
    "rod_M4_110": rod(CB["front_segment"]["rod_length_mm"]),
    "rod_M4_238": rod(CB["rear_segment"]["rod_length_mm"]),
    "nut_M4_ref": nut(),
    "washer_M4_ref": washer(),
}
for name, wp in parts.items():
    cq.exporters.export(wp, str(OUT / f"{name}.step"))
    print("part", name)

# ---------------------------------------------------------------- assembly, vehicle frame (x forward, y up, z across)
asm = cq.Assembly(name="track_segments_1to5")
L = lambda x, y, z, ax=None, ang=0: cq.Location(cq.Vector(x, y, z), cq.Vector(*ax) if ax else cq.Vector(0, 0, 1), ang)
ROT_Z_TO_X = ((0, 1, 0), 90)     # part axis z -> vehicle x (rods along x)

def add(name, part, loc, col):
    asm.add(part, name=name, loc=loc, color=cq.Color(*col))

PETG, TPU, AL, STEEL, ZN = (0.45, 0.6, 0.85), (0.25, 0.3, 0.35), (0.8, 0.8, 0.82), (0.6, 0.62, 0.65), (0.75, 0.75, 0.7)
for seg, x0, front in (("front", 0.0, True), ("rear", -C, False)):
    pz0, pz1 = Z[f"{seg}_plate"]; lane = Z[f"{seg}_lane"]; hub = Z[f"{seg}_hub"]
    plate = parts[f"side_plate_{seg}"]
    for side, sd in (("L", 1), ("R", -1)):
        # plate: local z = 0 at inboard face; right side mirrored
        loc = L(x0, 0, sd * pz0) if sd > 0 else L(x0, 0, -pz0, (0, 1, 0), 180)
        add(f"{seg}_plate_{side}", plate if sd > 0 else plate.mirror("XY"), L(x0, 0, sd * pz0) if sd > 0 else L(x0, 0, -pz0), PETG)
        add(f"{seg}_track_{side}", parts["track_running_shape"], L(x0, 0, sd * (lane[0] + FL_T + 1) - (0 if sd > 0 else TRK_W)), TPU)
        for ax_name, ax_x in (("rear_end", x0), ("front_end", x0 + C)):
            pul = parts["pulley_HTD5M_20T_ref"] if sd > 0 else parts["pulley_HTD5M_20T_ref"].mirror("XY")
            add(f"{seg}_pulley_{ax_name}_{side}", pul, L(ax_x, 0, sd * lane[0]), AL)
            add(f"{seg}_bearing_{ax_name}_{side}", parts["bearing_608ZZ_ref"], L(ax_x, 0, sd * pz0 - (0 if sd > 0 else BR["width_mm"])), STEEL)
    rodL, spL = CB[f"{seg}_segment"]["rod_length_mm"], CB[f"{seg}_segment"]["spacer_length_mm"]
    for x in CBH["at_x_mm"]:
        xv, yv = x0 + x, CBH["above_axle_mm"]
        add(f"{seg}_rod_x{x:g}", parts[f"rod_M4_{rodL:g}"], L(xv, yv, 0), ZN)
        if front:
            add(f"{seg}_spacer_x{x:g}", parts["spacer_front_82"], L(xv, yv, -spL / 2), PETG)
        else:
            for sd in (1, -1):
                add(f"{seg}_spacer_x{x:g}_{'L' if sd > 0 else 'R'}", parts["spacer_rear_65"], L(xv, yv, 40 if sd > 0 else -105), PETG)
        for sd in (1, -1):
            zb = sd * pz1
            add(f"{seg}_washer_x{x:g}_{'L' if sd > 0 else 'R'}", parts["washer_M4_ref"], L(xv, yv, zb if sd > 0 else zb - 0.8), ZN)
            add(f"{seg}_nut_x{x:g}_{'L' if sd > 0 else 'R'}", parts["nut_M4_ref"], L(xv, yv, zb + 0.8 if sd > 0 else zb - 4.0), ZN)
add("axle_middle", parts["axle_middle_230"], L(0, 0, 0), STEEL)
add("axle_front", parts["axle_front_160"], L(C, 0, 0), STEEL)
add("axle_rear", parts["axle_rear_230"], L(-C, 0, 0), STEEL)
asm.save(str(OUT / "track_segments_assembly.step"))
print("assembly", OUT / "track_segments_assembly.step", len(asm.children), "components")
