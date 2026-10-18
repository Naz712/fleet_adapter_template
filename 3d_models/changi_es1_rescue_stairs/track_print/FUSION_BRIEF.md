# Fusion brief: the RB4107 track unit (Nazim's side)

For a Claude Code session on Nazim's computer with the Autodesk Fusion MCP server, Fusion open.
Everything referred to here is in this repository on branch `claude/optimistic-carson-htn1c9`:
pull it first. Read `HANDOVER.md` for the wider context; this file is the job.

## 1. What the model is, and is not

`cad/RB4107_track_unit_reviewed.step` is Nhien's Rev B design (15 Oct 2026, exported from Fusion)
reduced to the track unit, with the track-side changes of the 16 to 18 Oct review applied. It is
not a different design. The deck, bars, motors, belts, sector gear, hinge motor and electronics
are Nhien's and are either unchanged or left out. Nhien merges this into his assembly.

154 parts in ten groups, in build order (full listing in `cad/part_tree.txt`):

    01 Rear frame (step 2)
    02 Front frame (step 4)
    03 Rails and carrier angles (steps 2-3, TS-10)
    04 Hinge shaft A, wheels and pins (steps 6-7, TS-06, TS-11)
    05 Hinge shaft B, wheels and pins
    06 Nose idler A and tensioner (steps 10-11, TS-09)
    07 Nose idler B and tensioner
    08 Rear idler A and tensioner
    09 Rear idler B and tensioner
    10 Tracks (step 11; option B belts shown, the printed loop has the same envelope)

Coordinates: origin on the hinge axis, +X toward the nose, +Y up, Z across; A side at Z < 60,
B side at Z > 60. Millimetres. Colours: new parts orange, plates blue, rails off-white, belts
dark, steel parts grey.

## 2. What changed against Nhien's Rev B, and why

| Nhien's Rev B | Reviewed model | Why |
|---|---|---|
| Hinge shaft Ø8 with a D-flat and E-clip grooves at both ends | plain round Ø8 h7, 82.3 (A) and 77.3 (B), no flat, no grooves | the flat only serves a set screw and gives no axial location; the grooves cut Ø8 to Ø6 at the ends |
| Hinge wheels M1 and stage-2 pulleys M3 with D-bores and M4 grub screws | bores round, reamed 8 H7; one Ø2.5 cross hole at mid-face; one ISO 8752 spring pin 2.5 x 24 each | a pin drives the part and fixes it along the shaft at once; nothing to loosen |
| E-clips DIN 6799-6 at the shaft ends | deleted | the pinned front wheel between the P1 and P2 bearings locates the shaft; the rear wheel's own pin keeps it at the shaft end |
| Idler shoulder screw clamped by its nut in the plate slot | slot kept; TS-09 tab, slider with foot and M4 x 20 jack screw added at each idler; M6 washer deleted, nut 1.4 mm inboard | nothing pushed the idler out or held it there except friction; tension could not be set or kept |
| Four RS clips per rail | one full-length 10 x 10 x 1.5 carrier angle per rail (TS-10), plate leg cut to 6.5, rails trimmed 189 to 186 | reviewer: contact area too small; the flange needs the rail to end short at x 207 |
| Plates as drawn | one M3 tap-drill hole for the tab at (±223, +11) and six for the carriers at x 40, 105, 170, y ±3.5; bearing seats to be laser-cut 15.8 and reamed 16 H7 | fits a laser cannot hold |
| Shim 8 x 11 x 0.5, front wheel to the P1 bearing | new | keeps the wheel face off the bearing's outer ring; the 0.3 to 0.5 feeler gap is at the P2 side |

Not changed, on purpose: the hinge motor pinion M6 on the motor's own D-shaft (Ø8, flat 7
across) with its set screws. The motor comes with the flat; an M3 on the flat drives the pinion
and a second M3 at 90° locks it. That is correct and stays as Nhien drew it.

## 3. Design notes the modeller must keep to

**Pins, not screws, on the hinge wheels.** The wheels have no hub: they sit in a 20 mm lane at
19 mm over their flanges, 0.5 mm each side. A set screw would have to go through the toothed rim
under the track, unreachable once the track is on. So each wheel takes a Ø2.5 pin through hub
and shaft at mid-face (9.5 from a flange face), driven flush.

**Hole size.** The shaft sets it, not the pulley. An Ø8 shaft with a Ø2.5 hole keeps about half
its section modulus; the hole sits beside a bearing where bending is small, about 40 MPa against
a yield above 350. Never more than Ø3 through an 8 mm shaft. The pin sees about 60 N and carries
kilonewtons in double shear.

**How the shaft is held along its axis.** The front wheel is pinned first, sitting between the
P1 and P2 bearings with its 0.5 shim against the P1 bearing and a 0.3 to 0.5 feeler gap to the
P2 bearing. Once pinned, the shaft cannot move more than that gap. The rear wheel (outside P2)
and the stage-2 pulley (inboard of P17, with its 1 mm shim) are then pinned where they stand.
Shaft ends 1.5 mm proud of the wheel and pulley faces. No clips, collars or set screws.

**The stage-2 pulley.** Nhien's pulley has a hub boss with a tapped hole outside the belt. Two
ways are allowed, the same on both sides: the pin (tapped hole drilled through to Ø2.5, far side
of the hub drilled through it, shaft drilled in place), or a cone-point M4 set screw into a seat
spot-drilled 1 mm into the shaft through that hole, Loctite 243, about 1 N·m. A set screw on a
plain round shaft without a seat holds by friction only and is not allowed.

**D-flat versus plain round.** A flat gives a set screw something to push against: positive
drive instead of friction. It adds no friction and no bending stability, and it does not hold a
part along the shaft. On the track shaft it would have to run under three parts and would weaken
the shaft, and the clips would come back for axial location. With pins the shaft is plain round.

**Tension.** TS-09 at each idler: the tab's ear is screwed to the plate at (±223, +11); its
leg B stands off the plate 1.5 mm clear of the slot end with an M4 tapped through it; the slider
is an 8 mm slice of angle on the shoulder screw's thread with a foot bent inboard; the M4 x 20
jack screw through leg B pushes the foot. Half a turn moves the idler 0.35 mm; usable travel is
223 to 232.6 (9.6 mm, 19 mm of loop). Set when the lower run pulls 2 to 3 mm off its rail at
4 N (belt 1.5 to 2.5), lock the M6 nyloc at 7 N·m with the screw head held, back the jack screw
off a quarter turn.

## 4. The job in Fusion

1. Import the STEP as a new design named "RB4107 track unit, reviewed 18 Oct 2026" in the
   team project (upload through the Data Panel if the connector cannot import a local file).
2. Check the browser against `cad/part_tree.txt`: ten top-level groups, 154 bodies, names and
   colours kept. Report anything that did not come through. Do not rename or move parts.
3. Make an A3 drawing from it, three sheets:
   a. Assembly: isometric view with balloons on the ten groups and a parts list from the
      component names.
   b. Hinge shaft A: a section along the shaft (plane through the shaft axis, normal to Y)
      showing rear wheel, P2 bearing, front wheel, 0.5 shim, P1 bearing, P17 bearing, 1 mm shim,
      stage-2 pulley and the three pins; balloons; dimensions: lane 20.0 between the plate
      faces, shaft 82.3, ends 1.5 proud, feeler gap 0.3 to 0.5 at the P2 bearing, pin holes
      Ø2.5 at mid-face.
   c. Nose tensioner A, detail from inboard at 2:1: slot 8.1 x 20.3, shoulder screw Ø8 x 25 M6
      and nyloc, slider with foot, tab with ear and the M3 at (223, +11), M4 x 20 jack screw;
      dimension the idler travel 223 to 232.6 and the 1.5 between leg B and the slot end.
4. Export the drawing as PDF and a viewport screenshot of the assembly to
   `3d_models/changi_es1_rescue_stairs/track_print/assembly/drawings/fusion/`, then commit and
   push on the same branch with a one-line message.
5. If anything in the STEP contradicts section 2 or 3, stop and report it instead of fixing it
   in Fusion; the source of truth is `cad/build_track_step.py` and the sheets in
   `assembly/drawings/`.
