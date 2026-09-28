# Changi AES "ES1" rescue stairs – 3D print model

This folder has 3D-print models of the rescue stairs on Changi Airport Emergency Service's
Rosenbauer E8000-type stair truck. They cover the staircase only, without the vehicle, at three
platform heights. The models are 1:100 scale and come with a display stand, so each one stands
on its own.

![Line-up](preview/lineup_3.2m_5.8m_8.4m.png)

## Design

| Item | Value | Source |
|---|---|---|
| Stair width (clear, between side panels) | 1500 mm | brief (matches Rosenbauer spec) |
| Step height | 170 mm | brief |
| Bottom flight | 18 treads / 19 risers, landing at 3230 mm | brief |
| Mid platform length | 1000 mm | brief |
| Tread depth (going) | 280 mm, about 31° pitch | assumed from photos |
| Top platform | 2800 × 3000 mm, flush with the right-hand side and extending left | Rosenbauer E8000 data, photos |
| Guard panel / handrail | 900 mm / 1050 mm above the pitch line | assumed |

The steps stay close to 170 mm at every setting, so only the upper flight changes:

| Model | Top platform | Upper flight | Size at 1:100 (L × W × H) |
|---|---|---|---|
| 3.2 m | 3.23 m (19 × 170) | none: the mid platform runs straight onto the top platform | 98 × 45 × 45 mm |
| 5.8 m | 5.80 m | 15 risers × 171.3 mm | 138 × 45 × 71 mm |
| 8.4 m | 8.40 m | 30 risers × 172.3 mm | 180 × 45 × 97 mm |

![Side elevations](preview/side_elevations_same_scale.png)

## Files

- `stl/ES1_stairs_<h>_1-100.stl`: the main print. One solid body with the display stand and a
  name plate on the base.
- `stl/stair_only/…_stair_only.stl`: the staircase with no stand, for mounting on your own base
  or vehicle.
- `stl/multicolour/<model>/…_{red,silver,grey,lime}.stl`: the same model split into colour
  bodies for multi-material printers such as Bambu AMS or Prusa MMU. Load all four files at
  once as a single object with multiple parts, then assign a filament to each part.
- `stl/models.json`: step counts and dimensions for every file.
- `generate_stairs.py`: the parametric generator.

Every STL is checked to be watertight (manifold) and a single connected body.

## Printing tips

- **FDM:** print upright on the base with a 0.4 mm nozzle and 0.12–0.16 mm layers. Turn on tree
  supports and allow them to start on the model, not only on the build plate. The underside of
  the flights and the platforms needs support, but the treads, panels and towers don't.
- **Resin:** tilt the model about 30° and put supports on the underside.
- The livery (lime stripes and "ES1") is raised by 0.4 mm, so it also serves as a painting guide
  on a single-colour print.
- **Other scales:** scaling in the slicer is fine for going bigger. For example, 200% gives 1:50,
  but the 8.4 m model is then about 360 mm long. For a smaller scale, regenerate the files so the
  thin parts stay printable:

```bash
pip install manifold3d trimesh numpy matplotlib
python3 generate_stairs.py --scale 87 --heights 3200 5800 8400
```

Every design value, such as tread depth, platform size, livery or the label, is in the
`Design` dataclass at the top of the script.

## Two-track stair climber simulation

`track_sim/` checks whether a tracked vehicle can cross the ES1 stairs, including the flat mid
platform, when it is split into a front and a rear track unit joined by a driven hinge. It
compares that vehicle with the same vehicle built as one long straight track.

Open `track_sim/index.html` in a browser, keeping `track-model.js` in the same folder. The page
animates the trip up or down at each height setting, plots load tilt and hinge bend, and
recalculates everything when you change the vehicle design. `track-model.js` also runs in Node:

```bash
node -e "const TM = require('./track_sim/track-model.js'); console.log(TM.simulate({ height: 8.4 }).summary)"
```

Results with the default design, at every height setting. The default is a 0.70 m unit
(sprocket centre to sprocket centre), a 90 mm sprocket radius, a ±55° hinge at 120°/m, and a
60 kg load 0.35 m above the hinge.

| | Two tracks + driven hinge | One long track |
|---|---|---|
| Worst change in load tilt per 10 cm of travel | 7.9° up, 9.8° down | 31.6° |
| Worst drop at a platform edge | 6 cm rock-back going up, none going down | 40 cm (tips over the edge) |
| Hinge bend used | ±40° | – |

Design rules from the math:

1. Each unit must always bridge two step nosings. Nosings are 328 mm apart, so a unit needs at
   least 657 mm.
2. One unit (0.88 m overall) must fit on the 1.0 m mid platform. The whole vehicle is longer than
   the platform, so it crosses in an S-bend.
3. The hinge needs a range of at least ±45°, even though the slope only changes by 31.6°. It has
   to fold the leading unit down before the middle reaches the edge. At ±35° the vehicle pivots
   over the edge like one long track.
4. The hinge must be driven. It needs at least 1.5 × 31.6° ÷ unit length, about 68°/m of travel,
   and works best at 90–150°/m; much faster than that and the fold snaps. With a free hinge, the
   units follow gravity and the front rears up on the risers.
5. To stay stable on the slope, unit length divided by the height of the centre of mass above the
   track must stay above 1.5 × tan(pitch). A 0.70 m unit allows the centre of mass up to about
   0.76 m above the track.
6. The tracks need a friction coefficient of at least tan 31.6° = 0.62 on the treads.

The model is quasi-static (slow speed). At every centimetre it solves how both units rest on the
real step geometry, then checks support, clearance and tipping. Tracks ride on the line joining
the step nosings. Traction, motor power and impact forces are not modelled.
