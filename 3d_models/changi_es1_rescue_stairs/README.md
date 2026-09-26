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
