# Printable track for the 1:5 prototype

3D-print files for the tracks of the 1:5 prototype of the 2-part carrier (see
`../track_sim/bending.html`): two units, 140 mm axle to axle (0.70 m at full size), one track
per side on each unit, on 8 mm axles in KFL08 bearings. They replace the HTD 5M belts and
pulleys on the parts list.

![Track on the ES1 steps](preview/track_on_ES1_steps_1-5.png)

![Parts](preview/parts.png)

## Matched to the ES1 steps

The ES1 steps, measured at 175 × 250 mm, are 35 × 50 mm at 1:5, so their nosings are
61.03 mm apart along the slope. The cleats are exactly a fifth of that apart, 12.21 mm. When the
track lies on a flight, every nosing under it sits in a gap between two cleats, and the cleat
above each nosing stands on that step's tread. Every step in contact then holds the track, like
a gear on a rack, instead of the track riding on whichever cleat tips land on the nosings.

`generate_track.py` checks this by sliding the track along the flight:

| Cleat spacing | Three nosings under one unit |
|---|---|
| 11.2 mm (the full-size plan's 56 mm, at 1:5) | can't all sit in gaps |
| **12.21 mm (5 per step)** | **all sit in gaps, with 3.7 mm of play** |
| 13.0 mm | can't all sit in gaps |

The play means the test stairs can be up to about 1.9 mm out per step and the track still
seats. On steps 1 mm deeper or shallower (51 or 49 mm), it still seats with 2 mm of play.
On the brief's 170 × 280 mm steps (34 × 56 mm), it doesn't. **Build the 1:5 test stairs at
35 mm high and 50 mm deep**, or regenerate the files for your stairs (below).

Other choices:

- **31 cleats on 8-tooth sprockets** put the axles (31 − 8) / 2 = 11.5 cleat spacings apart:
  140.4 mm, the 0.70 m units the simulation found steady.
- **3 mm cleats** (15 mm at full size, as simulated), 4.4 mm wide at the base and 2.4 mm at the
  tip, with rounded tips. The gap between them fits a square step edge with room to spare.
- **Axle to track face 16.5 mm, to the cleat tips 19.5 mm**: the 85 mm "axle to grip" of the
  simulation is 17 mm at 1:5.
- **TPU tread** for grip. Holding still on a flight needs a grip (friction coefficient) of
  0.61, and a hard stop going down 0.76. The cleats carry most of that on the steps.
- **Drive lugs inside**, one under each cleat, so the belt bends only in the thin sections
  between them. Each lug has 0.34 mm of clearance in its sprocket groove.

## Files (`stl/`)

| File | Print | Qty | Notes |
|---|---|---|---|
| `track_TPU_x4.stl` | TPU 95A | 4 | 128 mm ring, 15 mm tall. About 23 g and 2–3 hours each |
| `sprocket_end_PETG_x4.stl` | PETG | 4 | One lane, for the front and rear axles |
| `sprocket_middle_double_PETG_x2.stl` | PETG | 2 | Two lanes, one per unit, for the middle axle |
| `fit_test_track_5mm_TPU.stl` | TPU 95A | 1 | A 5 mm slice of the track. Print it first to check the fit on a sprocket |
| `step_gauge_3_steps_1-5_PLA.stl` | PLA | 1 | Optional: three ES1 steps at 1:5 to try a track on by hand |

`stl/track.json` lists every dimension and the check results.

### Print settings

- **Track:** TPU 95A on a direct-drive extruder (Bambu, Prusa MK3/MK4 and similar; a Bowden
  printer will struggle). Print it as it is, standing up as a ring, with no supports, 0.2 mm
  layers, 20–30 mm/s and 100% infill, so the cleats and lugs are solid. The belt is pulled
  and bent along its layers, its strongest direction.
- **Sprockets:** PETG, flat flange on the bed, no supports, 0.2 mm layers, 4 walls, 40% infill.
  The upper flanges are 45° chamfers, and the grooves are bridged under them.
- **Bore:** 8.25 mm for the 8 mm axle. If it is tight, run an 8 mm drill through it.

## Also needed

- 8 mm steel rod for the 3 axles, and 8 KFL08 flange bearings (as on the parts list).
- 6 M3 × 6 grub screws and 6 M3 nuts. The nut drops into the slot in each sprocket's hub.
  File a small flat on the axle where each grub screw sits, at least on the middle axle, which
  drives.
- The slide strips under each track's lower run, as on the parts list. With these tracks,
  the lugs ride on them, so their top face sits 12.2 mm below the axle centres. They run
  between the sprockets, about 100 mm long.

## Assembly

1. Print the fit-test slice and one end sprocket. Check that the lugs drop into the grooves and
   that the slice wraps the sprocket without riding up. Then print the rest.
2. Put a double sprocket on each end of the middle axle, hubs facing in. The outer lane carries
   the rear unit's track and the inner lane the front unit's.
3. Put the end sprockets on the rear axle in the outer lane and on the front axle in the inner
   lane. Line each one up with its lane on the middle sprocket using a straight edge, then
   tighten the grub screws.
4. Cut the end axles' holes in the side plates as slots, about 3 mm long, and do the same for
   the KFL08 bolt holes. Slide each end axle in to fit the track over its sprockets, then out to
   tension it. The tracks stretch a little when new, so check and re-tension after the first runs.
5. Try a track on the step gauge or the test stairs. Push the unit down the slope by hand: it
   should settle with a cleat standing on each tread.

## Other stairs

```bash
pip install manifold3d trimesh numpy matplotlib shapely
python3 generate_track.py --rise 34 --going 56   # your test stairs' step, at model size (mm)
python3 preview_track.py                         # redraws preview/
```

The cleat spacing becomes a fifth of the new nosing-to-nosing distance. The script picks the
number of cleats that keeps the axles closest to 140 mm, and prints the actual distance to
drill the plates at. Every value (cleat size, track width, clearances, bore) is in the
`Design` dataclass at the top of `generate_track.py`. Every file is checked to be a single
closed solid.
