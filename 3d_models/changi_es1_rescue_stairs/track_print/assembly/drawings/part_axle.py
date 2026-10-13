"""Axles: dimensioned sheet. Every number from parts_spec.json (v2)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from drawing import DIM, FILL, INK, MUTED, SPEC, centreline, dim_h, dim_v, leader, note_block, rect, save, sheet  # noqa: E402

P = SPEC["parts"]
AX = P["axle"]
Z = SPEC["layout_decision"]["z_stations_one_side_mm"]
D = AX["dia_mm"]
L = AX["lengths_mm"]                      # rear 230, middle 230, front 160
PU = P["pulley"]
FLAT_D, FLAT_L = 0.5, 10.0                # axle.flats
SPROCKET_W = 20.0                         # drive sprocket on the middle axle, drawn 20 wide at z 0 (the team's part)

# what sits on each axle, per side: (name, z0, z1, kind)
front_pulley = [("front pulley", Z["front_lane"][0], Z["front_lane"][1], "pulley"), ("hub", Z["front_hub"][0], Z["front_hub"][1], "hub")]
rear_pulley = [("rear pulley", Z["rear_lane"][0], Z["rear_lane"][1], "pulley"), ("hub", Z["rear_hub"][0], Z["rear_hub"][1], "hub")]
front_brg = [("front plate 608", Z["front_plate"][0], Z["front_plate"][1], "bearing")]
rear_brg = [("rear plate 608", Z["rear_plate"][0], Z["rear_plate"][1], "bearing")]
AXLES = [
    ("MIDDLE axle (the hinge): shared by both segments, driven", L["middle"], front_brg + front_pulley + rear_pulley + rear_brg, True),
    ("REAR axle: rear segment only", L["rear"], rear_pulley + rear_brg, False),
    ("FRONT axle: front segment only", L["front"], front_brg + front_pulley, False),
]
COL = {"pulley": "#c9a227", "hub": "#e0c76a", "bearing": FILL["bearing"]}

fig, view = sheet("AXLES  -  8 mm steel rod, bought and cut to length",
                  "ES1 stair-climbing rescue carrier, 1:5 prototype, track segment.  Part: axle (x3) and what sits on each, by z from the vehicle centre line.  mm.  Sheet 1 of 1.")

y0 = 0.60
for title, length, bands, sprocket in AXLES:
    ax = view([0.03, y0, 0.66, 0.26], title)
    h = length / 2
    ax.set_xlim(-h - 22, h + 40)
    ax.set_ylim(-26, 46)
    rect(ax, -h, -D / 2, length, D, FILL["steel"], lw=0.8)
    centreline(ax, -h - 15, 0, h + 15, 0)
    for sd in (1, -1):
        for name, z0, z1, kind in bands:
            rect(ax, sd * z0 if sd > 0 else -z1, D / 2, z1 - z0, 9 if kind != "hub" else 5, COL[kind], lw=0.5, alpha=0.9)
            if sd > 0:
                ax.text((z0 + z1) / 2, D / 2 + (10 if kind != "hub" else 6), f"{z0:g}-{z1:g}", fontsize=6.3, ha="center", va="bottom", color=INK, rotation=90)
        if sprocket:
            rect(ax, -SPROCKET_W / 2, D / 2, SPROCKET_W, 9, "#9fb7d4", lw=0.5)
    if sprocket:
        ax.text(0, D / 2 + 10, "drive\nsprocket", fontsize=6.3, ha="center", va="bottom", color=INK)
    # flats under every set screw: hub centres and the sprocket
    flats = [sd * (z0 + z1) / 2 for sd in (1, -1) for name, z0, z1, kind in bands if kind == "hub"] + ([0.0] if sprocket else [])
    for zc in flats:
        rect(ax, zc - FLAT_L / 2, -D / 2, FLAT_L, FLAT_D, "white", lw=0.4)
    ax.text(h + 4, -D / 2 - 1, "flat", fontsize=6.3, color=MUTED, va="top")
    dim_h(ax, -h, h, -16, f"{length:g}", ext_from=-D / 2)
    dim_v(ax, -D / 2, D / 2, h + 10, f"Ø{D:g}", ext_from=h)
    for name, z0, z1, kind in bands:
        if kind != "hub":
            ax.text(-(z0 + z1) / 2, D / 2 + 10, name, fontsize=6.0, ha="center", va="bottom", color=MUTED, rotation=90)
    y0 -= 0.27

# the flat, as a detail
axf = view([0.72, 0.58, 0.25, 0.28], "DETAIL: filed flat under each set screw")
axf.set_xlim(-12, 16)
axf.set_ylim(-9, 9)
rect(axf, -10, -D / 2, 20, D, FILL["steel"], lw=0.8)
rect(axf, -FLAT_L / 2, D / 2 - FLAT_D, FLAT_L, FLAT_D, "white", lw=0.5)
centreline(axf, -11, 0, 11, 0)
dim_h(axf, -FLAT_L / 2, FLAT_L / 2, 6.5, f"{FLAT_L:g}", ext_from=D / 2)
dim_v(axf, D / 2 - FLAT_D, D / 2, 11.5, f"{FLAT_D:g}", ext_from=10)
leader(axf, (0, D / 2 - FLAT_D / 2), (-11, -7.5), "set screw tip bears here")
note_block(fig, [
    "AXLES  (parts_spec.json: parts.axle)",
    f"Steel rod Ø{D:g} h7, unhardened (so it can be filed).",
    "Buy: MISUMI Singapore, or Design Lab spare rod.",
    f"Qty 3: rear {L['rear']:g}, middle {L['middle']:g}, front {L['front']:g};",
    f"plus a {P['hinge_cross_shaft']['length_mm']:g} mm hinge cross shaft.",
    "Cut square, deburr (the 608 bores are a close fit).",
    f"Flats {FLAT_D:g} x {FLAT_L:g} under each set screw.",
    "Pulleys set-screwed on; axles turn in the 608ZZ.",
    "Middle axle = hinge: both segments' plates turn on it.",
], x=0.70, y=0.50, w=0.27)
save(fig, "part_axle")
