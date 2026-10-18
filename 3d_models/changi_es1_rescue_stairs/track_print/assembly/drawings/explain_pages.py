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
 ("TS-09_tensioner", "How to read TS-09: the idler tensioner", [
  (69, 198, "Slot and shoulder screw", "The idler's Ø8 shoulder screw sits in the plate's 12.2 x 8.1 slot. Sliding it outward tightens the track; before this sheet only the nut's friction held it."),
  (72, 203, "Nyloc nut", "M6 nyloc on the inboard side. Tightened last, after the jack screw has set the tension."),
  (62, 181, "Slider", "An 8 mm slice of the same 20 x 20 x 3 angle in place of the M6 washer: a 19 mm leg on the plate with the Ø6.4 hole, and an 8 mm foot standing off the plate. The jack screw pushes on the foot, so nothing pushes on the nut."),
  (53, 214, "Tab, leg B", "The angle's long leg stands off the plate, inboard. The M4 jack screw threads through it along the slot direction."),
  (62, 218, "Ear and M3", "The short leg is cut down to a 7.5 x 8 ear above the slot and bolted to the plate with one M3 x 6 into a new tapped hole at (223, +11). Leg B stands 1.5 mm clear of the slot end, so the nut's corners never touch it."),
  (32, 178, "Jack screw", "M4 x 20 socket head. Wind it in until the lower run, hooked at a cleat at mid-span and pulled off its rail with 4 N (machine on blocks), gives 2 to 3 mm; pushing a run inward moves nothing because the rails sit under both runs, tighten the nut, then back it off a quarter turn."),
  (66, 120, "Plan: the lane", "Seen from above: plate P1 at z 55 to 60, the idler wheel in the lane with the screw head outside, the nut, slider and tab inboard, the 2020 bar ending at x 210.9 just behind the tab."),
  (206, 201, "Tab, flat", "Angle 20 x 20 x 3 cut 30 long; the M4 hole is 4 from the bottom end and 6 from the bend; the ear is the top 8 of the other leg, trimmed to 7.5 wide."),
  (206, 64, "Slider", "8 mm slice of the angle: leg 19 with the Ø6.4 hole 13 from the bottom, foot 8 bent inboard."),
  (60, 28, "Notes", "Four sets: nose and rear idler on each side. The rear tab mirrors the front; the jack screw always pushes outward, never in past x 223."),
 ]),
 ("TS-10_rail_carrier", "How to read TS-10: the rail carrier angle", [
  (120, 181, "Angle, plan", "One 10 x 10 x 1.5 aluminium angle per rail, 186 long: three Ø2.6 holes in the rail leg for the thread-forming screws, three Ø3.4 in the plate leg at 22, 87 and 152 from the hinge end (x 40, 105, 170), 3.5 from the leg's edge, for M3 x 6 into six new tapped holes in the plate."),
  (177, 187, "Plate leg", "Seen edge on above the rail leg. It is cut down to 8 so it stays inside the 15.4 plate height."),
  (60, 100, "Plate", "P1 or P2, 5 thick. The three M3 x 6 go through the angle into the plate's tapped holes, the same ones the four RS clips used."),
  (73, 116, "Angle on the plate", "The 8 leg lies flat on the plate's lane-side face, full length: 186 x 8 of contact instead of four 10 x 14.6 clip feet."),
  (90, 102, "Angle on the rail", "The 10 leg lies on the rail's face away from the track: on top of the lower rail, under the upper one. Three 3 x 5 thread-forming screws into blind Ø2.2 pilots 4 deep: the rail is only 5 thick and its far face carries the track, so a longer screw would come out of the sliding face."),
  (98, 89, "Rail", "UHMW strip 20 wide, 5 thick, trimmed from 189 to 186 at the idler end so the idler wheel's flange can never reach it."),
  (102, 72, "Track", "The track's lower run rides tooth-tips-down on the rail's other face at y -13.3; the angle never touches the track."),
  (60, 28, "Notes", "Eight angles from 1.6 m of stock; the RS 427-991 clips and their 24 M3 x 6 are no longer needed (keep the thread-forming screws)."),
 ]),
 ("TS-11_stackup", "How to read TS-11: the spacing between parts", [
  (40, 190, "Stage-2 pulley", "The HTD 5M drive pulley on the hinge shaft, 9.8 wide, z 30.2 to 40, pinned, with a 1 mm shim between it and the P17 bearing."),
  (57, 190, "P17 and its bearing", "The hinge-shaft support on the middle bar, bearing at z 41 to 46. 9 mm of bare shaft follow before the front plate."),
  (85, 180, "P1 and its bearing", "Front plate at z 55 to 60; the 688 sits flush in a reamed Ø16 H7 seat with Loctite 641."),
  (90.5, 200, "Shim 0.5", "An 8 x 11 x 0.5 shim on the bearing's inner ring, so the pulley face never touches the outer ring. The pulley is pinned hard against it."),
  (110, 210, "Front hinge pulley", "19 over the flanges in the 20 lane, z 60.5 to 79.5. Pinned to the shaft first: it is what locates the whole shaft between the two plate bearings."),
  (110, 174, "Cross pin", "Ø2.5 x 24 spring pin at mid-face, drilled through pulley and shaft together. Three per shaft: front pulley, rear pulley, stage-2 pulley."),
  (129.5, 190, "Feeler gap", "0.3 to 0.5 mm between the front pulley and the P2 bearing, set with a feeler gauge before pinning. This is the shaft's total end float."),
  (160, 210, "Rear hinge pulley", "Outboard of P2 at z 85.5 to 104.5, pinned with its own 0.3 to 0.5 gap to the bearing. The shaft ends 1.5 past it; no E-clip."),
  (100, 151, "Station chain", "Every width along the shaft from the centre outward. Sum from 28.7: the 77.3 mm half shaft P20-B."),
  (36, 92, "Idler: nut", "M6 nyloc inboard, 6 tall, then the 3 mm slider of TS-09."),
  (53, 102, "Idler: plate", "P1, 5 thick; the shoulder's end sits 0.5 inside it, so the M6 washer face never touches the slot."),
  (78, 92, "Idler: bearings and sleeve", "Two 688s with the 8 x 10 x 9 sleeve between their inner rings, inside the Ø16 H7 bore of the idler wheel."),
  (74, 118, "Shoulder vs stack", "Shoulder 25 against a 25.5 stack: the nut clamps washer, inner rings, sleeve, shim and plate together. That is correct; do not leave the shim out."),
  (248, 250, "Fits table", "The fit or clearance for every mating pair that matters, and what the laser, reamer or saw has to hold."),
  (60, 28, "Notes", "The order of pinning and the shim rule in words."),
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
 ("TS-06_pulley_20T", "How to read TS-06: the toothed wheel (bought, reamed, pinned)", [
  (88, 179, "Teeth", "20 HTD 5M teeth on a 31.83 pitch circle: the same tooth form as the track's inside, so they mesh without slip."),
  (88, 148, "Bore", "Bought with a small pilot bore. The 4 hinge wheels and the 2 stage-2 pulleys are reamed Ø8 H7 to run on the plain round shaft; the 4 idlers are bored Ø16 H7 for two 688 bearings each."),
  (163.5, 176, "Flange", "Ø35.7 flanges both sides, 1.5 thick, keep the track on the wheel. 19 over the flanges, 0.5 clear of each plate in the 20 lane."),
  (181, 190, "Belt face", "16 between the flanges; the 15 wide track sits here."),
  (181, 166, "Cross pin", "Ø2.5 x 24 spring pin through wheel and shaft at mid-face: the hub is drilled on the press when the pulley is bored, the shaft is drilled through that hole at assembly, in place. It drives the wheel and holds it along the shaft: no D-flat, no grub screw, no E-clips (design review, TS-11)."),
  (210, 156, "Hub", "Only the printed stand-in has a hub and set screw. The bought wheel is a plain flanged disc, because the lane has no room for a hub."),
  (60, 28, "Notes", "Order 8 from MISUMI SG plain bore; the Professional Workshop reams and bores them; pins go in on the build day."),
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
