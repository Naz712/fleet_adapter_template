# RB4107 track unit, reviewed: CAD copy for Fusion

`RB4107_track_unit_reviewed.step` is a copy of Nhien's Rev B Fusion model ("Redesign", exported
15 Oct 2026) reduced to the track unit, with the design-review changes of 16 to 18 Oct applied.
Open it in Fusion with File > Open (or upload it to the project in the Data Panel and open it from there,
or Insert > Insert Derive into Nhien's design); it comes in as a component tree, grouped and named so the
browser reads as the build order, in Nhien's coordinates (origin on the hinge axis, +X toward the nose, +Y up, Z across,
A side at Z < 60, B side at Z > 60; the Z numbers below are Fusion's, 60 more than the viewer's).

154 parts. Nothing in it interferes with anything else (checked part against part with a solid
intersection, tolerance 0.05 mm3). Made by `build_track_step.py` from
`RB4107 assembly (Rev B) - SolidWorks.step`, then grouped and renamed by `relabel_track_step.py`;
`check_render.py` is the interference check. The full tree is in `part_tree.txt`.

## The part tree in Fusion's browser

| Group | What is in it |
|---|---|
| 01 Rear frame (step 2) | P2 plates with their hinge bearings; 3030 bars and corner brackets with screws and T-nuts; the deck T-nuts; P17 supports with bearings and screws |
| 02 Front frame (step 4) | P1 plates with their hinge bearings; 2020 bars and corner brackets with screws and T-nuts |
| 03 Rails and carrier angles (steps 2-3, TS-10) | Front rails A and B, rear rails A and B: upper and lower rail with their two carrier angles |
| 04 / 05 Hinge shaft A / B, wheels and pins (steps 6-7, TS-06, TS-11) | the plain shaft, front and rear hinge wheels, stage-2 pulley, three spring pins, the 0.5 and 1 mm shims |
| 06 / 07 Nose idler A / B and tensioner (steps 10-11, TS-09) | idler wheel, two bearings, sleeve, shoulder screw, head washer, 0.5 shim, nyloc, TS-09 tab, slider and jack screw |
| 08 / 09 Rear idler A / B and tensioner | the same at the rear |
| 10 Tracks (step 11) | Nhien's four cleated belts (option B); the printed loop has the same envelope |

Every part name says what it is, where it goes and what changed, for example
`Hinge wheel HTD 5M 20T, front A (bore 8 H7, cross pinned, TS-06)` or
`TS-09 slider, nose B (8 mm angle slice, 19 leg + 8 foot, d6.4)`. New parts are orange, plates blue,
rails off-white, belts dark, steel parts grey.

## What is in it

Side plates P1 and P2 (4), slide rails P3 to P6 (8), cross bars P7 and P8 (4), hinge shaft supports
P17 (2), corner brackets P18 and P19 (8) with their screws and T-nuts, bearings 688-2RS (14), the
idler sets (shoulder screws, head washers, 0.5 shims, sleeves, nyloc nuts), the eight track wheels, the
two stage-2 pulleys, the hinge shafts, Nhien's four cleated belts (option B track), and the new parts.

## What changed, part by part

| Part | Change |
|---|---|
| Hinge drive shafts A (82.3) and B (77.3) | plain round d8 h7, no D-flat, no E-clip grooves; d2.5 cross holes at each pulley |
| Track drive pulleys M1 (4) and stage-2 pulleys M3 (2) | bore rounded to d8 H7 (the D-flat removed), d2.5 cross hole at mid-face; grub screws deleted |
| Spring pins ISO 8752 2.5 x 24 (6) | new: through each hinge pulley and stage-2 pulley and the shaft. The two stage-2 pins should be 2.5 x 12 (tooth roots about Ø13.4); this STEP still shows 24 |
| E-clips DIN 6799-6 (4) | deleted: the pinned front wheel locates the shaft |
| Shim washers 8x11x0.5 (2) | new: front wheel to the P1 bearing (the 0.3 to 0.5 feeler gap is at the P2 side) |
| Side plates P1, P2 (4) | new M3 tap-drill hole for the tensioner tab at (+-223, +11); six M3 tap-drill holes for the rail carriers at x 40, 105, 170 and y +-3.5. Bearing seats stay at 16 in the model: the DXF carries 15.8 for the laser, reamed to 16 H7 |
| Slide rails P3 to P6 (8) | trimmed 3 mm at the idler end, 186 long |
| RS 427-991 rail clips (24) and their screws | deleted |
| Rail carrier angles TS-10 (8) | new: Al 10x10x1.5, 186 long, plate leg cut to 6.5 so the upper and lower carriers do not meet; the 10 leg sits under the upper rail and on top of the lower rail; three d3.4 holes in the plate leg at y +-3.5 |
| Tensioner tab TS-09 (4) | new: Al angle 20x20x3 cut 30, leg B standing 1.5 off the slot end (x 215.5 to 218.5), ear 7.5 x 8 at y 7 to 15 on the plate face with a d3.4 hole at (223, 11); M4 tapped through leg B at y -11, 6 from the plate face |
| Tensioner slider TS-09 (4) | new: an 8 mm slice of the same angle, 19 mm leg on the plate face with the d6.4 hole 13 from its bottom, 8 mm foot bent inboard at the bottom; replaces the M6 washer |
| Jack screw M4 x 20 (4) | new: through leg B, its tip on the slider's foot; pushes the idler out along the slot |
| M6 washers DIN 125 (4) | deleted (the slider takes their place) |
| Nyloc nuts M6 (4) | moved 1.4 mm inboard for the 3 mm slider |

Usable idler travel with the tab in place: 223 to 232.6 (9.6 mm, 19 mm of loop); the slider's foot
meets leg B at 223, which is also where the rail end limits the idler.

**This STEP is behind the Fusion model (19 Oct).** Nazim's Fusion design "RB4107 track unit, reviewed
18 Oct 2026" also has: the old Ø3.3 holes in the front hinge wheels removed; idler slots at arc
centres 220.4 to 232.6; three Ø2.6 holes in each carrier's rail leg and 2.2 x 4 blind pilots in the
rails at 20, 93, 166 from the rail's hinge end, 7.5 from the plate face; and the 52 screws. Export a
STEP from Fusion to replace this file (`build_track_step.py` needs Nhien's source STEP, which is not
in the repository).

## What is not in it (Nhien's parts, unchanged or his to change)

Deck P12, posts P15, tray P16, cover, battery; sector gear P11, angle P14, hinge motor and pinion; drive
motors, stage-1 and stage-2 belts and pulleys other than M3, intermediate shafts P21, P13 supports;
electronics. The review asks Nhien for: slot H 74 long (+3) and 3 longer at the rear, two more sector
teeth, P17 in aluminium with 15.8 seats, cast corner brackets in place of P18 and P19, the 12 to 40 rpm
hinge motor, a 20 A fuse, a microswitch and a second IMU for the hinge angle.

## Option A track

The printed TPU loop (TS-01, `stl/track_TPU_x4.stl`) is not in the STEP; Nhien's belts stand in for the
track. The wheels, shafts and every joint are the same for both options.
