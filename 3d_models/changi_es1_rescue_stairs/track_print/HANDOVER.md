# Handover: RB4107 track unit, Nazim's side (18 October 2026)

For continuing the work in another Claude Code session (a local one with the Autodesk Fusion
MCP server, or any later cloud session). The fastest way to continue with the full conversation
is to pull the cloud session into a terminal from a clean checkout of this repository:

    claude --teleport session_014wM4fAmHBiJaRepdpStSox

That checks out branch `claude/optimistic-carson-htn1c9` and loads the conversation. If that is
not possible, this file is the context.

## Who and what

- Group RB4107, Safe Evacuation Robot: a two-track stair carrier for the ES1 rescue stairs
  (175 rise on 250 going, 35 degrees), built as a 1:5 prototype (steps 35 x 50 mm).
- Nazim owns the track unit: track loops, toothed wheels, hinge shafts and how the wheels fix to
  them, idlers, tensioners, rail support, and the track assembly. Nhien owns the frame (side
  plates P1 and P2, bars, deck), drive train, hinge motor and sector gear, electronics. Nhien's
  current design is Rev B (15 Oct 2026), exported from Fusion; his Rev_B_2 zip is byte-identical.
- Nazim is a first-time builder: instructions must be detailed and beginner friendly. Keep chat
  answers short and plain. Do not spawn agents or workflows (usage). Never commit personal
  reports (individual updates) or the vendor contact spreadsheet to this public repository.

## Where everything is

Repository folder `3d_models/changi_es1_rescue_stairs/track_print/`:

- `README.md`: the design, the buildability check and the decisions, dated.
- `assembly/procurement_revB.md`: what to buy or make, where, prices, lead times.
- `assembly/drawings/`: sheets TS-00 to TS-11 and their explainer pages EX-00 to EX-11 (PNG),
  made by `eng_sheets.py` and `explain_pages.py`.
- `assembly/RB4107_track_complete_pack.pdf`: the 57-page pack (feasibility, build day, sheets,
  Nhien's Rev B sheets).
- `assembly/Track_unit_assembly_in_detail.pdf`: the focused track assembly document (shaft and
  pulleys, idlers, tensioner, loop, rails, order of work); built by `assembly/track_detail/`.
- `cad/RB4107_track_unit_reviewed.step`: Nhien's Rev B reduced to the track unit with every
  review change applied, 154 parts in ten named groups (`cad/part_tree.txt`, `cad/README.md`).
  Coordinates: origin on the hinge axis, +X toward the nose, +Y up, Z across, A side at
  Z < 60, B side at Z > 60 (the interactive viewer's Z is this minus 60).
- `viewer/index.html`: the interactive model (explode, 11 build steps, hinge swing, both tracks).
- `track_sim/`: the stair simulators that chose the 2-part layout.
- `stl/`: the printed track files (option A).

Living documents outside the repository (same claude.ai account):

- Manufacturing and assembly plan (Claude Docs, two tabs: the plan, and "Short version for
  Nhien"): https://claude.ai/code/artifact/103e3018-d014-4e9c-b1c5-eb941101f2c5
- Interactive assembly viewer: https://claude.ai/artifact/6gnfWidMkD9kDk2BQc1tBw
- Track pack page (every sheet as a page): https://claude.ai/artifact/VAqfyiG1Js4Yb2ELvSqrpu
- Combined page (short version, plan, viewer tabs): https://claude.ai/artifact/CGuGphcHHat8UFaKFG6BnY
- Nazim's primer page (his own): https://claude.ai/artifact/Ruuvv2HPPhhSFctbFkLrms

## State of the design: decided

| Decision | Where recorded |
|---|---|
| 2-part carrier with one hinge and a stop-bend-go routine (simulation, 26 Sep to 1 Oct) | README, track_sim, plan section 1 |
| Two track segments per side on Nhien's plates, HTD 5M 20T wheels at 225 centres; option A printed TPU loop (TS-01) recommended, option B bought belt with 22 bonded cleats (TS-01B) as fallback | plan 5.10, 5.11; procurement 1A, 1B |
| Plain round hinge shafts d8 h7, no D-flat, no E-clip grooves; d2.5 spring pins through hinge wheels and stage-2 pulleys, hub holes drilled on the press, shaft drilled through them in place | TS-06, TS-11, plan 5.3 to 5.5, 8.2 |
| Set screws: none on the hinge wheels (no hub in the 20 mm lane); allowed on the stage-2 pulley only as a cone point into a seat spot-drilled in the shaft, with Loctite 243 | plan Appendix C item 17; Track_unit_assembly_in_detail.pdf 1.3 |
| Jack-screw idler tensioner TS-09 (tab, slider with foot, M4 x 20); tension set by a 4 N pull on the lower run, 2 to 3 mm (belt 1.5 to 2.5); idler travel 223 to 232.6 | TS-09, plan 5.8, 8.3 |
| Full-length rail carrier angles TS-10 (10 x 10 x 1.5, plate leg 6.5, six new M3 holes per plate), rails trimmed to 186 | TS-10, plan 5.6, 5.7 |
| Bearing seats laser-cut 15.8, reamed 16 H7, Loctite 641; pulley bores reamed 8 H7 and 16 H7 at the Professional Workshop | plan 5.1, 5.3, 8.1 |
| Sector gear: two more teeth at the rear (travel 35 to 37 degrees as drawn against 35 needed); slot H 74 long; backlash 0.1 to 0.2 at centre distance 61.1 to 61.2 | plan 3.3, 8.4 |
| Proposed: buy a KHK SSAY1-100 (module 1, 100 teeth, 6 mm S45C plate) and cut a 23-tooth sector, which moves the centre distance to 60.1 to 60.2 or needs a 22-tooth pinion | plan 5.14, Appendix C item 16; procurement section 2 |
| Hinge motor 5840-31ZY in the 12 to 40 rpm variant; fuse 20 A; 2020 bars kept; hinge zero by microswitch plus a second IMU | plan Appendix C items 5, 11, 14 |

## Open with Nhien (plan Appendix C, items 1 to 17 in short)

Re-issue P1 and P2 DXF (seats 15.8, tap-drill holes, M3 tab hole at (+-223, +11), six carrier
holes, slots 8.1 +0.1/0); deck slot H 74 (+3 nose, +3 rear); option B deck notch; sector gear
(+2 teeth, or the bought gear and the centre distance choice); cast corner brackets; hinge motor
variant; 20 A fuse; P17 in aluminium with 15.8 seats; sheets 20 and 21 superseded (round shafts,
pins); the shared STEP for a re-check; hinge angle sensing; stage-2 pulley fixing choice.

## Immediate next steps

1. Fusion: import `cad/RB4107_track_unit_reviewed.step`, verify the tree against
   `cad/part_tree.txt`, make the A3 drawing (assembly with balloons and parts list; section along
   hinge shaft A with the shims, gaps and pins; nose tensioner detail at 2:1), export the PDF to
   `assembly/drawings/fusion/`, commit and push on the same branch.
2. 19 Oct: order pulleys (8 + 1), d8 h7 shaft (300), 688 bearings (14), shoulder screws (4 sets),
   spring pins, angle stock; workshop request for the bores (critical path, 1 to 2 weeks).
3. Nhien's DXF re-issue, laser 22 to 29 Oct; fit-test slice and four TPU rings; carriers, tabs,
   sliders; assembly 9 to 10 Nov, tests 11 to 13 Nov, advisor demo 16 Nov.
4. Individual update (one page plus appendix) exists outside the repository; the next one is due
   at week 7 and should carry photos and measured results.

## Numbers held

Lane 20.0 +-0.2 between plate faces (bars cut to +-0.1); bearing seats laser 15.8, ream 16 H7;
pulley bores 8 H7 (hinge, stage-2) and 16 H7 (idlers); pulley gaps 0.5 shim plus 0.3 to 0.5
feeler, pinned; track tension 2 to 3 mm at 4 N on the lower run; hinge 35 degrees needed; pinion
backlash 0.1 to 0.2; drive 2.5 kg.cm per side needed against 49 at stall, 0.11 m/s at 67 rpm;
hinge motor 5 kg.cm needed through the 5.1:1 sector; shaft 40 MPa bending at 100 N, pin shear
62 N; power 17.5 A if every motor stalls, so a 20 A fuse.

## Conventions

Work on branch `claude/optimistic-carson-htn1c9` only; commit messages end with the
Co-Authored-By and Claude-Session lines used in the log; push after every piece of work.
