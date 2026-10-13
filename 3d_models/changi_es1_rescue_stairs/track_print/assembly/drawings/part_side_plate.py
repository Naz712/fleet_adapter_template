"""Side plate with slide rail: dimensioned sheet. Every number from parts_spec.json (v2)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from drawing import DIM, FILL, INK, MUTED, SPEC, centreline, circle, dim_h, dim_v, leader, note_block, rect, save, sheet  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402
from shapely.geometry import Point, box as shp_box  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

P = SPEC["parts"]
SP = P["side_plate"]
Z = SPEC["layout_decision"]["z_stations_one_side_mm"]
C = SPEC["segment"]["axle_to_axle_mm"]                       # 225
T, BELOW, ABOVE = SP["plate"]["thickness_mm"], SP["plate"]["bottom_edge_below_axle_mm"], SP["plate"]["top_edge_above_axle_mm"]  # 7, 12, 33
END_R, BOSS_R = 20.0, SP["plate"]["boss_radius_mm"]          # R20 ends, R14.5 bosses
ARC_CY = (ABOVE - BELOW) / 2                                  # 10.5: the end arcs are centred half way up
POCKET = SP["bearing_pockets"]["dia_mm"]                      # 22.2
RAIL = SP["rail"]
RX0, RX1, RW, RT, RTOP, RBOT = RAIL["from_x_mm"], RAIL["to_x_mm"], RAIL["width_mm"], RAIL["thickness_mm"], RAIL["top_face_below_axle_mm"], RAIL["bottom_below_axle_mm"]
CB = SP["cross_bar_holes"]
SB = SP["sector_bolts"]
# z bands (one side): plate, web, rail for the front and the rear plate
FZ = dict(plate=Z["front_plate"], rail=((Z["front_lane"][0] + Z["front_lane"][1]) / 2 - RW / 2, (Z["front_lane"][0] + Z["front_lane"][1]) / 2 + RW / 2))
FZ["web"] = (FZ["plate"][0], FZ["rail"][0])
RZ = dict(plate=Z["rear_plate"], rail=((Z["rear_lane"][0] + Z["rear_lane"][1]) / 2 - RW / 2, (Z["rear_lane"][0] + Z["rear_lane"][1]) / 2 + RW / 2))
RZ["web"] = (RZ["rail"][1], RZ["plate"][1])

fig, view = sheet("SIDE PLATE with slide rail  -  PETG, 3D printed",
                  "ES1 stair-climbing rescue carrier, 1:5 prototype, track segment.  Files stl/side_plate_front_L/R.stl, side_plate_rear_L/R.stl.  mm at model size.  Sheet 1 of 1.")

# ---------------------------------------------------------------- 1. side view (x-y), front left plate seen from outboard
ax = view([0.03, 0.47, 0.70, 0.40], "1  SIDE VIEW (x-y), front plate, seen from outboard. x from the middle axle (the front segment's rear end) to the front axle")
ax.set_xlim(-48, C + 50)
ax.set_ylim(-52, 62)
shape = unary_union([shp_box(0, -BELOW, C, ABOVE), Point(0, ARC_CY).buffer(END_R, quad_segs=64), Point(C, ARC_CY).buffer(END_R, quad_segs=64),
                     Point(0, 0).buffer(BOSS_R, quad_segs=64), Point(C, 0).buffer(BOSS_R, quad_segs=64)])
ax.add_patch(Polygon(list(shape.exterior.coords), closed=True, fc=FILL["petg"], ec=INK, lw=0.8))
rect(ax, RX0, -RBOT, RX1 - RX0, RBOT - BELOW, FILL["petg"], lw=0.6)          # web + rail seen edge-on below the plate
for x in (0, C):
    circle(ax, x, 0, POCKET / 2, fill="white")
    centreline(ax, x, -30, x, 48)
for x in CB["at_x_mm"]:
    circle(ax, x, CB["above_axle_mm"], CB["dia_mm"] / 2, fill="white")
for a in SB["angles_deg"]:
    circle(ax, SB["radius_mm"] * math.cos(math.radians(a)), SB["radius_mm"] * math.sin(math.radians(a)), SB["dia_mm"] / 2, fill="white")
centreline(ax, -40, 0, C + 40, 0)
# dimensions
dim_h(ax, 0, C, 50, f"{C:g} axle to axle", ext_from=ABOVE + 1)
dim_h(ax, -END_R, C + END_R, 58, f"{C + 2 * END_R:g} over the plate", ext_from=ABOVE + 1)
dim_h(ax, 0, CB["at_x_mm"][0], 41, f"{CB['at_x_mm'][0]:g}", ext_from=CB["above_axle_mm"] + 2.5)
dim_h(ax, 0, CB["at_x_mm"][1], 45.5, f"{CB['at_x_mm'][1]:g}", ext_from=CB["above_axle_mm"] + 2.5)
dim_h(ax, RX0, RX1, -26, f"{RX1 - RX0:g} rail", ext_from=-RBOT)
dim_h(ax, 0, RX0, -31, f"{RX0:g}", ext_from=-RBOT)
dim_v(ax, -BELOW, ABOVE, -30, f"{BELOW + ABOVE:g}", ext_from=-END_R - 2)
dim_v(ax, 0, ABOVE, -38, f"{ABOVE:g}", ext_from=-END_R - 2)
dim_v(ax, -BELOW, 0, -38, f"{BELOW:g}", ext_from=-END_R - 2)
dim_v(ax, 0, CB["above_axle_mm"], C + 38, f"{CB['above_axle_mm']:g}", ext_from=C + 2)
dim_v(ax, -RBOT, -RTOP, C + 30, f"{RT:g}", ext_from=RX1, offset=0)
dim_v(ax, 0, -RTOP, C + 38, f"{RTOP:g}", ext_from=RX1)
leader(ax, (C + END_R * math.cos(math.radians(35)), ARC_CY + END_R * math.sin(math.radians(35))), (C + 28, 44), f"R{END_R:g}, centred {ARC_CY:g} above the axle")
leader(ax, (C + BOSS_R * math.cos(math.radians(-50)), BOSS_R * math.sin(math.radians(-50))), (C + 22, -22), f"R{BOSS_R:g} boss: {BOSS_R - POCKET / 2:.1f} wall round the pocket")
leader(ax, (POCKET / 2 * math.cos(math.radians(300)), POCKET / 2 * math.sin(math.radians(300))), (-46, -47), f"Ø{POCKET:g} pocket x 2, through (608ZZ press fit)")
leader(ax, (CB["at_x_mm"][0] + 2, CB["above_axle_mm"] + 1.5), (95, 36), f"Ø{CB['dia_mm']:g} x 2, cross bars (M4 rod)")
leader(ax, (SB["radius_mm"] * math.cos(math.radians(130)) - 1.2, SB["radius_mm"] * math.sin(math.radians(130)) - 1.2), (-46, -40),
       f"3 x Ø{SB['dia_mm']:g} on R{SB['radius_mm']:g} at {SB['angles_deg'][0]:g}/{SB['angles_deg'][1]:g}/{SB['angles_deg'][2]:g} deg: hinge sector (front plates)")
leader(ax, (150, -RBOT + 0.5), (120, -47), f"rail and web below the plate, x {RX0:g} to {RX1:g}: see section 2")

# ---------------------------------------------------------------- 2. end sections (y-z) at x = 100
def end_section(ax, zz, title, box_edge=None):
    pz0, pz1 = zz["plate"]
    rz0, rz1 = zz["rail"]
    wz0, wz1 = zz["web"]
    ax.set_title(title, fontsize=9.5, color=INK, loc="left", pad=4)
    rect(ax, pz0, -BELOW, T, BELOW + ABOVE, FILL["petg"], hatch=True)                 # plate
    rect(ax, wz0, -RBOT, wz1 - wz0, RBOT - BELOW, FILL["petg"], hatch=True)            # web
    rect(ax, rz0, -RBOT, RW, RT, FILL["petg"], hatch=True)                             # rail
    # the track's lower run on the rail, for position only
    rect(ax, (rz0 + rz1) / 2 - 7.5, -RTOP, 15, 2.0, "#9aa2a9", lw=0.4, alpha=0.5)
    ax.text((rz0 + rz1) / 2, -RTOP + 3.2, "track, tooth tips", fontsize=6.5, color=MUTED, ha="center")
    centreline(ax, min(pz0, rz0) - 8, 0, max(pz1, rz1) + 8, 0)
    y = -RBOT - 5
    dim_h(ax, pz0, pz1, y, f"{T:g}", ext_from=-RBOT)
    dim_h(ax, rz0, rz1, y, f"{RW:g}", ext_from=-RBOT)
    dim_h(ax, wz0, wz1, y - 6, f"{wz1 - wz0:g} web", ext_from=-RBOT)
    xr = max(pz1, rz1) + 3
    dim_v(ax, -RBOT, -RTOP, xr, f"{RT:g}", ext_from=max(pz1, rz1))
    dim_v(ax, -BELOW, -RBOT, xr + 7, f"{RBOT - BELOW:.2f}", ext_from=max(pz1, rz1))
    dim_v(ax, 0, -RTOP, xr + 14, f"{RTOP:g}", ext_from=max(pz1, rz1))
    xl = min(pz0, rz0) - 3
    dim_v(ax, -BELOW, ABOVE, xl, f"{BELOW + ABOVE:g}", ext_from=min(pz0, rz0))
    for z in (pz0, pz1, rz0, rz1):
        ax.text(z, ABOVE + 3, f"{z:g}", fontsize=6.5, ha="center", color=INK, rotation=90, va="bottom")
    ax.text((pz0 + pz1) / 2, ABOVE + 13, "z from the\ncentre line", fontsize=6.5, ha="center", color=MUTED)
    if box_edge is not None:
        ax.plot([box_edge, box_edge], [-BELOW, ABOVE], color=DIM, lw=0.8, dashes=(4, 2))
        ax.text(box_edge - 1, ABOVE - 2, "box wall", fontsize=6.5, ha="right", va="top", color=MUTED, rotation=90)
    ax.set_xlim(min(pz0, rz0) - 16, max(pz1, rz1) + 24)
    ax.set_ylim(-RBOT - 16, ABOVE + 26)

end_section(view([0.03, 0.04, 0.26, 0.40]), FZ, "2a  FRONT plate, section at x = 100", box_edge=Z["box"][1])
end_section(view([0.31, 0.04, 0.26, 0.40]), RZ, "2b  REAR plate, section at x = 100")

# ---------------------------------------------------------------- 3. printing and notes
axp = view([0.58, 0.22, 0.38, 0.22], "3  AS PRINTED: plate face down, rail standing up")
axp.set_xlim(-30, 300)
axp.set_ylim(-14, 40)
rect(axp, 0, 0, 265, T, FILL["petg"])                       # plate lying flat, seen from the side (print Z up)
rect(axp, RX0 + END_R, T, RX1 - RX0, RBOT - BELOW, FILL["petg"])   # web standing up
rect(axp, RX0 + END_R, T + (RBOT - BELOW) - RT, RX1 - RX0, 0, FILL["petg"], lw=0)
axp.plot([-20, 290], [0, 0], color=INK, lw=1.2)
axp.text(135, -6, "print bed", fontsize=7, ha="center", color=MUTED)
dim_v(axp, 0, T, 280, f"{T:g}", ext_from=265)
leader(axp, (120, T + 3), (120, 26), f"web and rail stand {RBOT - BELOW:.2f} above the plate;\nthe sliding face is a side wall, so its\nlayer lines run along the track")
note_block(fig, [
    "SIDE PLATE  (parts_spec.json: parts.side_plate)",
    "PETG.  Make (3D print).  Qty 4: front L/R, rear L/R (mirror pairs).",
    "0.2 mm layers, 4 walls, 30% infill, no supports, plate face down.",
    f"Plate {C + 2 * END_R:g} x {BELOW + ABOVE:g} x {T:g}; rail {RX1 - RX0:g} x {RW:g} x {RT:g},",
    f"top {RTOP:g} below the axle: the lower run's tooth tips ride on it.",
    f"Front: plate z {FZ['plate'][0]:g}-{FZ['plate'][1]:g}, web {FZ['web'][0]:g}-{FZ['web'][1]:g}, rail {FZ['rail'][0]:g}-{FZ['rail'][1]:g}; sector holes.",
    f"Rear: plate z {RZ['plate'][0]:g}-{RZ['plate'][1]:g}, rail {RZ['rail'][0]:g}-{RZ['rail'][1]:g}, web {RZ['web'][0]:g}-{RZ['web'][1]:g} (under the hub).",
    "Press the 608ZZ in after printing (pocket 0.2 over; ream if tight).",
    f"Footprint {C + 2 * END_R:g} x {RBOT + ABOVE:.0f}: bed 235 on one side, or 225 diagonally. About 75-80 g.",
], x=0.58, y=0.235, w=0.38)
save(fig, "part_side_plate")
