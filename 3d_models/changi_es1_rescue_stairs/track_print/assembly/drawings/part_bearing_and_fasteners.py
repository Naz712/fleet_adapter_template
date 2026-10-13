"""Bearing 608ZZ, its pocket, the cross bars and every fastener: one sheet. Numbers from parts_spec.json (v2)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from drawing import DIM, FILL, INK, MUTED, RED, SPEC, centreline, circle, dim_dia, dim_h, dim_v, leader, note_block, rect, save, sheet  # noqa: E402

P = SPEC["parts"]
BR, SP, CB, PU = P["bearing"], P["side_plate"], P["cross_bar"], P["pulley"]
OD, ID, W = BR["outside_dia_mm"], BR["bore_mm"], BR["width_mm"]       # 22, 8, 7
POCKET, T = SP["bearing_pockets"]["dia_mm"], SP["plate"]["thickness_mm"]  # 22.2, 7
BOSS = SP["plate"]["boss_radius_mm"]

fig, view = sheet("BEARING 608ZZ, CROSS BARS and FASTENERS  -  bought",
                  "ES1 stair-climbing rescue carrier, 1:5 prototype, track segment.  mm at model size.  Sheet 1 of 1.")

# 1. 608ZZ end view and section
ax = view([0.03, 0.50, 0.30, 0.38], "1  608ZZ: end view and section")
ax.set_xlim(-20, 48)
ax.set_ylim(-24, 24)
circle(ax, 0, 0, OD / 2, fill=FILL["bearing"])
circle(ax, 0, 0, OD / 2 - 2.2, fill="#d9dee3")
circle(ax, 0, 0, ID / 2 + 2.2, fill=FILL["bearing"])
circle(ax, 0, 0, ID / 2, fill="white")
centreline(ax, -16, 0, 16, 0)
centreline(ax, 0, -16, 0, 16)
dim_dia(ax, 0, 0, OD / 2, 40, f"Ø{OD:g}", length=16)
dim_dia(ax, 0, 0, ID / 2, -40, f"Ø{ID:g}", length=16)
xs = 30
rect(ax, xs, -OD / 2, W, OD, FILL["bearing"], hatch=True)
rect(ax, xs, -ID / 2, W, ID, "white", lw=0.5)
rect(ax, xs + 1.5, -OD / 2 + 2.2, W - 3, 2.6, "white", lw=0.4)
rect(ax, xs + 1.5, ID / 2 + 2.2, W - 3, 2.6, "white", lw=0.4)
dim_h(ax, xs, xs + W, OD / 2 + 3, f"{W:g}", ext_from=OD / 2)
centreline(ax, xs - 3, 0, xs + W + 3, 0)

# 2. pocket in the plate + press
ax2 = view([0.35, 0.50, 0.30, 0.38], "2  Pocket in the plate, 608 pressed in")
ax2.set_xlim(-12, 56)
ax2.set_ylim(-24, 24)
rect(ax2, 0, -BOSS, T, 2 * BOSS, FILL["petg"], hatch=True)          # the boss section round the pocket
rect(ax2, 0, -POCKET / 2, T, POCKET, "white", lw=0.5)
rect(ax2, 0, -OD / 2, W, OD, FILL["bearing"], hatch=True, alpha=0.85)
rect(ax2, 0, -ID / 2, W, ID, "white", lw=0.5)
rect(ax2, -4, -4, T + 8, 8, FILL["steel"], lw=0.6)                   # axle through it
centreline(ax2, -5, 0, 40, 0)
dim_h(ax2, 0, T, BOSS + 3, f"{T:g} plate = {W:g} bearing", ext_from=BOSS)
dim_v(ax2, -POCKET / 2, POCKET / 2, T + 6, f"Ø{POCKET:g} pocket", ext_from=T)
dim_v(ax2, -BOSS, BOSS, T + 14, f"Ø{2 * BOSS:g} boss", ext_from=T)
leader(ax2, (T, -BOSS + 1.5), (14, -17), f"{BOSS - POCKET / 2:.1f} wall all round")
ax2.text(23, 22, f"Pocket {POCKET:g} = {OD:g} + 0.2:\na light press fit.\nMeasure the first print;\nream if tight, glue if loose.",
         fontsize=7, color=INK, va="top")

# 3. KFL08, not chosen
ax3 = view([0.68, 0.50, 0.30, 0.38], "3  Not chosen: KFL08 flange block")
ax3.set_xlim(-32, 68)
ax3.set_ylim(-35, 35)
rect(ax3, -24, -13, 48, 26, FILL["light"], lw=0.8)
circle(ax3, 0, 0, 10, fill="#d9dee3")
circle(ax3, 0, 0, 4, fill="white")
for x in (-18.5, 18.5):
    circle(ax3, x, 0, 2.25, fill="white")
dim_h(ax3, -24, 24, 17, "48", ext_from=13)
dim_h(ax3, -18.5, 18.5, -17, "37 hole centres", ext_from=-13)
dim_v(ax3, -13, 13, 30, "26", ext_from=24)
rect(ax3, 40, -13, 12, 26, FILL["light"], hatch=True)
dim_h(ax3, 40, 52, 17, "12", ext_from=13)
ax3.text(-30, -33, "12 thick and 26 tall, but the gap between the box (z 40)\nand the first track (z 49) is 9 mm: it does not fit.\nThe 608ZZ in a pocket does, at a third of the price.",
         fontsize=7, color=RED, va="bottom")

# 4. cross bar
ax4 = view([0.03, 0.12, 0.50, 0.34], "4  CROSS BAR: M4 threaded rod + printed spacer, nut and washer each end (section)")
rf, sf, od = CB["front_segment"]["rod_length_mm"], CB["front_segment"]["spacer_length_mm"], CB["front_segment"]["spacer_od_mm"]
rr, sr = CB["rear_segment"]["rod_length_mm"], CB["rear_segment"]["spacer_length_mm"]
end = (rf - sf - 2 * T) / 2                 # 7 per end: washer 0.8 + nut 3.2 + 3 proud
s0 = 0
ax4.set_xlim(-24, sf + 2 * T + 2 * end + 24)
ax4.set_ylim(-30, 26)
rect(ax4, -T - end, -2, sf + 2 * T + 2 * end, 4, FILL["steel"], lw=0.6)      # rod
rect(ax4, 0, -od / 2, sf, od, FILL["petg"], hatch=True)                     # spacer
rect(ax4, 0, -2.25, sf, 4.5, "white", lw=0.4)
for x in (-T, sf):
    rect(ax4, x, -18, T, 36, FILL["petg"], hatch=True)                     # plates
    rect(ax4, x, -2.25, T, 4.5, "white", lw=0.4)
for x, sd in ((-T, -1), (sf + T, 1)):
    rect(ax4, x if sd > 0 else x - 0.8, -4.5, 0.8, 9, FILL["bearing"], lw=0.5)           # washer
    rect(ax4, (x + 0.8) if sd > 0 else x - 4.0, -3.5, 3.2, 7, FILL["bearing"], lw=0.5)   # nut
centreline(ax4, -T - end - 6, 0, sf + T + end + 6, 0)
dim_h(ax4, 0, sf, od / 2 + 9, f"{sf:g} spacer (rear {sr:g})", ext_from=od / 2)
dim_h(ax4, -T, 0, -20, f"{T:g}", ext_from=-18)
dim_h(ax4, sf, sf + T, -20, f"{T:g}", ext_from=-18)
dim_h(ax4, -T - end, sf + T + end, 21, f"{rf:g} rod (rear {rr:g})", ext_from=2)
dim_h(ax4, sf + T, sf + T + end, -20, f"{end:g}", ext_from=-5)
dim_v(ax4, -od / 2, od / 2, sf / 2, f"Ø{od:g}", ext_from=sf / 2 - 12)
leader(ax4, (sf + T + 0.8 + 1.6, -3.5), (sf * 0.45, -21), "washer 0.8 + nut 3.2 + 3 rod proud = 7 each end")
leader(ax4, (sf / 2 + 20, -2.25), (-10, -27), "spacer bore 4.5: the rod runs through it")

# 5. fastener table
ax5 = view([0.56, 0.12, 0.42, 0.34], "5  FASTENERS (all bought; Design Lab spares first)")
ax5.set_xlim(0, 100)
ax5.set_ylim(0, 60)
rows = [
    ("Item", "Qty", "Where"),
    ("Pulley set screws (come with the pulleys), M4", "16", "2 per pulley, on the axle flats"),
    ("M4 x 1 m threaded rod, cut 2 x 110 + 2 x 238", "1", "cross bars"),
    ("M4 nut + washer", "8 + 8", "cross bar ends"),
    ("M3 x 14 bolt + nut", "6 + 6", "hinge sector gears, front plates"),
    ("M4 x 12 bolt", "4", "box to the rear plates"),
    ("M3 x 6 set screw", "1", "stand-in pulley (test only)"),
    ("Printed spacer Ø10, bore 4.5: 82 and 210 long", "2 + 2", "cross bars (PETG, make)"),
]
for i, (a, b, c) in enumerate(rows):
    y = 56 - i * 7
    w = "bold" if i == 0 else "normal"
    ax5.text(1, y, a, fontsize=7.2, fontweight=w, va="center")
    ax5.text(62, y, b, fontsize=7.2, fontweight=w, va="center")
    ax5.text(70, y, c, fontsize=7.2, fontweight=w, va="center")
    ax5.plot([0, 100], [y - 3.5, y - 3.5], color="#e3e6e9", lw=0.6)
ax5.plot([0, 100], [52.5, 52.5], color=INK, lw=0.8)
note_block(fig, [
    f"BEARING: 608ZZ, {ID:g} x {OD:g} x {W:g}, shielded. Buy, qty {BR['qty_total']}: 8 in the plates, 2 on the hinge cross shaft.",
    "RS Singapore RS PRO 608-2Z about S$3 each; Wheeler Mectrade or any SKF distributor (approved list).",
], x=0.03, y=0.085, w=0.60)
save(fig, "part_bearing_and_fasteners")
