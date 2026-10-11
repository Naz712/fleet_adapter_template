# Printable track for the 1:5 prototype

A 3D-print file for the tracks of the team's 1:5 base: two track segments, 225 mm axle to
axle (45 cm in all, 1.125 m segments at full size), each with a 550 mm track loop on wheels
about 1.5 cm in radius. The track is printed; the pulleys are bought.

![Track on the ES1 steps](preview/track_on_ES1_steps_1-5.png)

![Print and buy](preview/parts.png)

## How it fits the team's base

- **Bought pulleys:** HTD 5M, 20 teeth (31.8 mm pitch diameter, so about 1.5 cm to the track),
  for 15 mm belts, 8 mm bore. The track has 110 HTD 5M teeth inside, so its loop is 550 mm, and
  (550 − 100) / 2 puts the axles exactly 225 mm apart.
- **Segment length:** run in the simulator (`../track_sim`), 1.125 m segments (22.5 cm at 1:5)
  stop, bend and go over the ES1 stairs as well as the 0.70 m ones did: 14.5° of lean before
  tipping going down and 18° going up, the hinge bending 35° up and 37° down, and no drop at any
  edge. A stiff 2.25 m track tips at the edges, one end dropping up to 48 cm.

## Matched to the ES1 steps

The ES1 steps, measured at 175 × 250 mm, are 35 × 50 mm at 1:5, so their edges are 61.03 mm
apart along the slope. The track has 45 cleats round its 550 mm loop, 12.22 mm apart: five of
them span 61.11 mm, within 0.08 mm of a step. When the track lies on a flight, every step edge
under it (four under each segment) sits in a gap between two cleats, and the cleat above each
edge stands on that step. Every step in contact holds the track, like a gear on a rack, instead
of the track riding on cleat tips.

`generate_track.py` checks this by sliding the track along the flight:

| Cleat spacing | Four step edges under one segment |
|---|---|
| 11.2 mm (the full-size plan's 56 mm, at 1:5) | can't all sit in gaps |
| **12.22 mm (5 per step)** | **all sit in gaps, with 3.5 mm of play** |
| 13.0 mm | can't all sit in gaps |

The play lets each test step be about 1.2 mm out. With every step 1 mm deeper or shallower
(51 or 49 mm) it still seats, with about 1 mm of play. On the brief's 170 × 280 mm steps
(34 × 56 mm), it doesn't. **Build the 1:5 test stairs at 35 mm high and 50 mm deep**, or
regenerate the file for your stairs (below).

The cleats are 3 mm tall (15 mm at full size). Holding still on a flight needs a grip
(friction coefficient) of 0.61, and a hard stop going down 0.76; the TPU and the cleats provide
it.

## Files (`stl/`)

| File | Print | Qty | Notes |
|---|---|---|---|
| `track_TPU_x4.stl` | TPU 95A | 4 | 183 mm ring, 15 mm tall, about 32 g. Needs a bed at least 190 mm across |
| `fit_test_track_5mm_TPU.stl` | TPU 95A | 1 | A 5 mm slice of the track. Print it first and try it on a pulley |
| `step_gauge_3_steps_1-5_PLA.stl` | PLA | 1 | Optional: three ES1 steps at 1:5 to try a track on by hand |

`stl/track.json` lists every dimension and the check results.

**Print settings:** TPU 95A on a direct-drive extruder (Bambu, Prusa MK3/MK4 and similar). Print
the track as it is, standing up as a ring, with no supports, 0.2 mm layers, 20–30 mm/s and 100%
infill. The belt is pulled and bent along its layers, its strongest direction. The NUS Library
printer only prints PLA, so print the tracks on a printer that takes TPU or ask one of the 3D
printing services on the vendor list.

## Buy

- 8 × HTD 5M 20-tooth pulleys for 15 mm belts, 8 mm bore, with flanges (2 per segment per side).
- 8 mm steel rod for the 3 axles, 8 KFL08 flange bearings.
- All three from MISUMI Singapore, which is on the approved vendor list.
- Slide strips under each track's lower run: the teeth ride on them, so their top face sits
  13.3 mm below the axle centres. They run between the pulleys, about 185 mm long.

If the printed teeth skip on the pulleys, a stock 550-5M-15 belt (110 teeth) fits the same
pulleys and axle spacing; the cleats can then be printed as strips and glued on.

## Assembly

1. Print the fit-test slice. Check that its teeth drop into a pulley's grooves and that it wraps
   the pulley without riding up. Then print the four tracks.
2. Cut the end axles' holes in the side plates as slots about 3 mm long, and the same for the
   KFL08 bolt holes. Slide each end axle in to fit the track, then out to tension it. The tracks
   stretch a little when new, so check and re-tension after the first runs.
3. Line each pulley up with its lane with a straight edge, then tighten its set screws. File a
   flat on the middle axle under its set screws: it drives.
4. Try a track on the step gauge or the test stairs. Push the segment down the slope by hand: it
   should settle with a cleat standing on each tread.

## Other stairs

```bash
pip install manifold3d trimesh numpy matplotlib shapely
python3 generate_track.py --rise 34 --going 56   # your test stairs' step, at model size (mm)
python3 preview_track.py                         # redraws preview/
```

The cleat count becomes the nearest to five per step round the 550 mm loop. Every value
(belt teeth, pulley teeth, cleat size, track width) is in the `Design` dataclass at the top of
`generate_track.py`. Every file is checked to be a single closed solid.
