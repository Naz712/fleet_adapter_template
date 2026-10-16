"""One plain-language explainer page per sheet: a locator copy of the sheet with numbered markers,
and a key saying what each marked thing is, what it joins to and with what. Output: drawings/EX-xx.png"""
import textwrap
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from PIL import Image

HERE = Path(__file__).resolve().parent
W, H = 420.0, 297.0
COL = ["#d7263d", "#1b6ca8", "#2a9d8f", "#e36414", "#7b2cbf", "#b5179e", "#4f772d", "#9c6644", "#f4a261", "#0b3954", "#ff5d8f", "#5e548e", "#386641"]

# (sheet file, title, [(x_mm, y_mm, name, explanation), ...]) in sheet mm, origin bottom-left
PAGES = [
 ("TS-00_assembly_front_segment", "How to read TS-00: the front track segment put together", [
  (117, 219.5, "Track (item 1)", "The printed TPU belt. Its inside teeth sit on the two toothed wheels; its outside cleats grip the steps. One each side."),
  (57, 226, "Pulley = toothed wheel (item 2)", "Bought HTD 5M 20-tooth wheel. Sits on the axle and is locked to it by 2 M4 set screws into a filed flat. Four per segment."),
  (137, 212, "Side plate (item 3)", "Printed PETG plate, one each side. Holds the two bearings the axles turn in and carries the slide rail under the track."),
  (57, 140, "Middle axle (item 4)", "Ø8 steel rod, 230 long, shared with the rear segment. It is the hinge: both segments' plates turn on it. The motor drives it."),
  (169.5, 155, "Front axle (item 5)", "Ø8 rod, 160 long. Only this segment's two front pulleys sit on it. It just idles."),
  (87, 190, "Cross bar spacer (item 7)", "Printed Ø10 tube, 82 long, between the two plates on each M4 rod. Sets the plate spacing."),
  (157, 215, "M4 rod, nut and washer (item 8)", "M4 threaded rod 110 long through plate, spacer, plate; a washer and nut on each end pull the plates onto the spacer. Two per segment."),
  (113, 64.5, "Track loop, side view", "The belt wraps the two wheels; cleats stand out of the loop. The flat lower run rests on the plate's rail (dashed, hidden inside the loop)."),
  (164, 73, "Bearing 608ZZ (item 6)", "Pressed into the plate's Ø22.2 pocket, dashed because it is hidden behind the pulley flange. The axle runs through its 8 mm bore."),
  (57, 81.5, "Sector gear bolts (item 9)", "Three Ø3.4 holes on a 17 mm circle round the middle axle. The hinge sector gear (team's part) bolts to the plate's inboard face with M3 x 14 and nuts."),
  (331.5, 95, "End view", "Looking from the front: box in the middle (dashed), then each side a plate, a toothed wheel with its track, and the hub. 194 over the tracks, 224 over the plates."),
  (330, 250, "Parts list", "Every balloon number on the drawing matches a row here: part number, description and how many for this segment."),
 ]),
 ("TS-01_track", "How to read TS-01: the track", [
  (38, 192, "Cleats, outside", "45 bumps 12.22 apart (8 degrees). Five of them span one ES1 step, so every step edge lands between two cleats and the track holds like a gear on a rack."),
  (126, 247, "Teeth, inside", "110 HTD 5M teeth, 5 apart. These mesh with the 20-tooth wheels; this is what stops the track slipping."),
  (246, 162, "Edge view", "The ring seen from the side: 15 wide, 182.7 tall over the cleats."),
  (340, 207.6, "Cleat profile (4:1)", "A cleat is 3 tall, 4.4 wide at its base and 2.4 at the tip, with rounded corners so it releases from the step."),
  (340, 194, "Tooth profile (4:1)", "A tooth is 2 deep with a 1.45 radius tip and a 2.9 root; the 1.4 backing between teeth and cleats is the belt itself. Whole section 6.4 thick."),
  (60, 28, "Notes", "Print standing up as a ring, no supports, 100% infill, TPU 95A, on the Fab Lab UP300. Four tracks, about 32 g each."),
 ]),
 ("TS-01B_track_belt", "How to read TS-01B: the bought track belt (Rev B B10)", [
  (167, 244, "Cleats, outside", "22 rubber blocks 10 long, 7.9 high and the full 15 width, bonded on the belt back every 25 mm (every 5th tooth). They grip the step edges. Their tips are 25 mm from the axle: level with the deck underside, see the note."),
  (115, 233, "Teeth, inside", "110 HTD 5M teeth, 5 apart, moulded into the belt. They mesh with the 20-tooth wheels, so the belt cannot slip."),
  (54, 222, "Hinge wheel (dashed)", "The belt wraps the driven 20T wheel on the hinge shaft at the left and the idler at the right, 225 apart: 450 straight plus the two half wraps = 550, the belt's pitch length."),
  (166, 196, "225 centres", "Same wheel spacing as the printed track, so the plates, slots and idlers do not change between the two versions."),
  (74, 108, "Cleat profile (4:1)", "A cleat is a plain block 10 long and 7.9 high, bonded to the belt back; no taper. 11.7 total from tooth tip to cleat tip."),
  (64, 80, "Tooth profile (4:1)", "HTD 5M tooth, 2.06 deep, on a 1.74 backing: 3.8 belt thickness. This is the belt as bought."),
  (212, 82, "Across the belt (2:1)", "Belt and cleat are both 15 wide; the cleat spans the full width."),
  (60, 28, "Notes", "Buy SKF PHG 550-5M-15 (RS SG 058-6535) x4; a belt shop cuts and bonds 88 cleats. The deck has to be notched 13 x 135 over each front lane, or the cleats cut to 5 high, before the belts fit under it."),
 ]),
 ("TS-02_side_plate_front", "How to read TS-02: the front segment's side plate", [
  (162, 211.5, "Plate, seen from above", "7 thick, 265 long, 45 tall. Printed flat on the bed in PETG. Left plate drawn; the right one is its mirror."),
  (162, 226, "Slide rail, seen from above", "An 18 wide, 4 thick strip 185 long, joined to the plate by a web. It sits under the track's lower run so the track cannot sag between the wheels."),
  (275, 134, "Bearing pocket", "Ø22.2 hole, one at each axle. A 608ZZ bearing is pressed in; the axle turns in it. The round boss round it keeps a 3.4 wall."),
  (110, 162, "Cross bar hole", "Ø4.5, two per plate at 60 and 200 from the axle, 28 above it. The M4 rods go through here."),
  (50, 151, "Sector gear holes (front plate only)", "Three Ø3.4 holes on R17 round the middle axle. The hinge sector gear bolts here with M3 x 14 and nuts, on the inboard face."),
  (162, 119, "Rail from the side", "The strip hanging below the plate between x 20 and 205. Its top is 13.34 below the axle centre: exactly where the track's tooth tips run."),
  (310, 222, "Section A-A: plate", "Cut through the rail at x 100 and looking along the plate: the 7 thick plate standing 45 tall."),
  (339, 171, "Section A-A: rail and web", "The rail (18 x 4) and the 9 web joining it to the plate, with the track's lower run dashed on top of it."),
  (344, 134, "Section B-B: pocket", "Cut through a bearing pocket: 7 thick, Ø22.2 straight through, 3.4 of wall round it."),
  (168, 53, "Detail C", "The three sector gear holes at 50, 90 and 130 degrees from the forward direction, 1.5 times size."),
 ]),
 ("TS-03_side_plate_rear", "How to read TS-03: the rear segment's side plate", [
  (162, 238.5, "Plate, seen from above", "Same plate as TS-02 but on the outside of the vehicle (z 105 to 112), so the rail is on its inboard face and it has no sector gear holes."),
  (162, 217, "Slide rail, inboard", "The rail sits under the rear track lane (z 78 to 96), joined to the plate by a 16 wide web that passes under the pulley hub."),
  (275, 134, "Bearing pocket", "Ø22.2, a 608ZZ is pressed in at each axle (rear axle and middle axle)."),
  (110, 162, "Cross bar hole", "Ø4.5 at 60 and 200 from the rear axle, 28 up. The M4 rods through these also clamp the box: plate, spacer, box wall, box wall, spacer, plate (sheet TS-08)."),
  (162, 119, "Rail from the side", "Hangs below the plate between x 20 and 205; its top carries the lower run's tooth tips."),
  (364, 222, "Section A-A: plate", "The 7 thick plate, 45 tall, now on the right of the section because it is outboard."),
  (321, 171, "Section A-A: rail", "18 x 4 rail with the track's lower run dashed on it, and the 16 web to the plate."),
  (344, 134, "Section B-B: pocket", "Cut through a pocket: Ø22.2 through the 7 plate, 3.4 wall."),
 ]),
 ("TS-04_axles", "How to read TS-04: the axles", [
  (150, 253, "Middle axle, 230", "The hinge shaft. Each side, from the centre out: front plate bearing, front segment wheel, rear segment wheel, rear plate bearing. Flats at z 0 (drive sprocket) and at both hubs each side."),
  (222.5, 257, "Flat", "A 0.5 deep, 10 long flat filed where each set screw lands, so the screw cannot slip round the shaft."),
  (150, 207, "Rear axle, 230", "Only the rear segment's two wheels and two plates. Flats at the rear hubs."),
  (150, 161, "Front axle, 160", "Only the front segment's two wheels and two plates. Shorter because the front plates are inboard."),
  (150, 115, "Hinge cross shaft, 120", "Same rod. Runs across the box in two spare 608ZZ and carries the hinge pinions (team's part)."),
  (332, 193, "Flat detail (4:1)", "What the flat looks like: 0.5 deep, 10 long. The set screw tip bears on the flat face."),
 ]),
 ("TS-05_spacer", "How to read TS-05: the cross bar spacers", [
  (139, 225, "Rear spacer, 65 long, 4 off", "Two per rear rod, one each side between the box wall (z 40) and the rear plate (z 105). The box sits between them."),
  (75, 175, "Front spacer, 82 long, 2 off", "One per front rod, filling the whole gap between the two front plates (z -41 to 41)."),
  (327, 217, "End view", "Ø10 outside, Ø4.5 bore: the M4 rod passes through with clearance."),
  (339, 143, "Section", "Just a tube, 2.75 wall, ends cut square because they set the plate spacing."),
 ]),
 ("TS-06_pulley_20T", "How to read TS-06: the toothed wheel (bought, plain bore)", [
  (88, 178, "20 grooves", "The track's teeth drop into these. HTD 5M profile, 5 pitch, pitch diameter 31.83."),
  (112, 122, "Flange", "A thin Ø35.7 disc on each side of the teeth. Keeps the 15 wide track from walking off sideways."),
  (88, 160, "Hub (stand-in only)", "On Nhien's plates there is no room for a hub: the real wheels are plain-bore and get a D-bore or a Ø16 bearing bore at the workshop."),
  (88, 148, "Bore", "Ordered plain. Workshop: 4 x D-bore Ø8 (driven by the hinge shaft's flat), 4 x Ø16 H7 (two 688 bearings, idlers on shoulder screws)."),
  (163.5, 188, "Flange, in section", "1.5 thick, both sides. Total 20 over the flanges, which is the lane width in the layout."),
  (182, 184, "Belt seat", "17 between the flanges; the 15 wide track sits here with 1 each side."),
  (209, 168, "Hub and set screws (stand-in only)", "Not used on the Rev B frame: the D-bore drives the wheel, E-clips locate it. Only the 20 over the flanges matters for the lane width."),
 ]),
 ("TS-07_bearing_608ZZ", "How to read TS-07: the bearing (bought)", [
  (88, 188, "Outer race, Ø22", "Pressed into the plate's Ø22.2 pocket. It does not turn."),
  (88, 158, "Bore, Ø8", "The axle slides through; the inner race turns with the axle."),
  (172.5, 182, "Balls", "Between the races, 7 wide in all. Shielded (ZZ) both sides so dust stays out."),
  (267.6, 174, "Plate", "The 7 PETG plate: plate thickness equals bearing width, so the bearing sits flush."),
  (267.6, 152, "Bearing in its pocket", "A light press fit (0.2 over). Measure the first print; ream if tight, glue if loose."),
  (295, 133, "Axle", "Ø8 rod through the bore, continuing to the wheel."),
  (280, 157, "Pulley flange next to it", "The wheel's flange starts 1 beyond the plate face, so the wheel never rubs the plate."),
 ]),
 ("TS-08_rear_segment_to_base", "How to read TS-08: how the rear segment hangs on the box", [
  (59, 232, "Box (dashed)", "The team's box, 80 wide. Near the middle axle it must stop at z 37 to leave 3 for the sector gear."),
  (91, 217, "Hinge sector gear (dashed)", "3 thick, bolted to the front plate's inboard face. The pinion on the hinge cross shaft turns it to bend the front segment."),
  (96.5, 227.5, "M3 x 14 bolt and nut", "One of three per plate, through the gear and the plate, nut on the outboard side."),
  (98.75, 239.5, "Front plate", "7 thick with its 608ZZ; the middle axle turns in it."),
  (120.5, 190, "Front segment wheel", "Set-screwed to the middle axle; its hub points outboard."),
  (120.5, 226.75, "Front track", "Wrapped on that wheel, cut through."),
  (162.5, 190, "Rear segment wheel and track", "Next outboard, same again. Both segments are driven by this one axle."),
  (194.75, 239.5, "Rear plate", "Outermost, 105 to 112, with its 608ZZ. 224 over the two rear plates."),
  (62, 124, "M4 rod, 238 long", "Runs plate to plate through the box. This is the only attachment of the rear segment to the box."),
  (140, 124, "65 spacer", "One each side between box wall and plate. The rod passes through it."),
  (90.5, 124, "Ø4.5 hole in the box wall", "The box needs two of these per wall at x 60 and 200 from the rear axle, 28 above the axle line."),
  (203, 124, "M4 nut and washer", "Tightened on each end: plate, spacer, box, spacer, plate are clamped as one."),
  (162.5, 59.5, "Rail under the track", "The lower run of the rear track rests on the plate's rail; the upper run is free above."),
  (312, 170, "Side view: box on the segment", "The box is bolted through the two cross bars (hex nuts visible). The front segment hinges on the middle axle at the right."),
 ]),
]

def page(sheet, title, marks, n):
    fig = plt.figure(figsize=(W / 25.4, H / 25.4), dpi=150)
    bg = fig.add_axes([0, 0, 1, 1]); bg.set_xlim(0, W); bg.set_ylim(0, H); bg.axis("off")
    bg.add_patch(Rectangle((10, 10), W - 20, H - 20, fc="none", ec="black", lw=0.8))
    bg.text(16, H - 18, title, fontsize=14, fontweight="bold", va="top")
    bg.text(16, H - 25, f"Markers below sit on a reduced copy of sheet {sheet.split('_')[0]} (previous page, full size). Numbers match the key on the right.", fontsize=7.5, va="top", color="#444")
    # locator image: 255 mm wide at the left
    img = Image.open(HERE / f"{sheet}.png")
    s = 268 / W
    x0, y0 = 16, 22
    ax = fig.add_axes([x0 / W, y0 / H, 268 / W, H * s / H])
    ax.imshow(img, extent=(0, W, 0, H)); ax.axis("off")
    for i, (x, y, name, _) in enumerate(marks):
        c = COL[i % len(COL)]
        dx, dy = (14, 11) if (i % 2 == 0) else (-14, 11)          # marker sits off the feature, leader points at it
        if y > 250: dy = -11
        ax.plot([x, x + dx * 0.72], [y, y + dy * 0.72], color=c, lw=0.9, zorder=5)
        ax.plot([x], [y], marker="o", ms=2.5, color=c, zorder=5)
        ax.add_patch(Circle((x + dx, y + dy), 3.6, fc=c, ec="white", lw=0.8, zorder=6))
        ax.text(x + dx, y + dy, str(i + 1), color="white", fontsize=5.5, fontweight="bold", ha="center", va="center", zorder=7)
    # key on the right
    kx, ky = 292, H - 32
    for i, (x, y, name, text) in enumerate(marks):
        c = COL[i % len(COL)]
        bg.add_patch(Circle((kx + 3, ky - 1.5), 2.8, fc=c, ec="none"))
        bg.text(kx + 3, ky - 1.5, str(i + 1), color="white", fontsize=6.5, fontweight="bold", ha="center", va="center")
        bg.text(kx + 8, ky, name, fontsize=8, fontweight="bold", va="top")
        lines = textwrap.wrap(text, 62)
        bg.text(kx + 8, ky - 4.2, "\n".join(lines), fontsize=6.4, va="top", linespacing=1.25, color="#222")
        ky -= 4.2 + 2.9 * len(lines) + 4.5
    out = HERE / f"EX-{sheet.split('_')[0][3:]}_{sheet.split('_', 1)[1]}.png"
    fig.savefig(out, dpi=150, facecolor="white"); plt.close(fig); print(out)

import sys
ONLY = sys.argv[1:]
for n, (sheet, title, marks) in enumerate(PAGES):
    if not ONLY or sheet in ONLY or sheet.split("_")[0] in ONLY:
        page(sheet, title, marks, n)
