# STEP files (CAD) for the track segments, 1:5

Made by `../export_step.py` from `../assembly/parts_spec.json`. STEP AP214 opens in SolidWorks
(File > Open, or Insert > Component in an assembly), Fusion, Onshape and FreeCAD. SolidWorks
imports `track_segments_assembly.step` as an assembly with one component per part (53 components,
named `front_plate_L`, `rear_pulley_front_end_R`, `axle_middle` and so on). Units mm. Vehicle frame:
x forward, middle axle at x = 0; y up, axle centre line at y = 0; z across, centre line at z = 0.

| File | Part | Make / buy |
|---|---|---|
| `track_segments_assembly.step` | both segments, all parts placed | |
| `track_running_shape.step` | track in its running shape round two pulleys (used in the assembly) | make, TPU |
| `track_ring_as_printed.step` | track as printed, a ring (same as `../stl/track_TPU_x4.stl`) | make, TPU |
| `side_plate_front.step`, `side_plate_rear.step` | left-hand plates; mirror for the right | make, PETG or CNC aluminium |
| `spacer_front_82.step`, `spacer_rear_65.step` | cross bar spacers | make |
| `axle_middle_230.step`, `axle_rear_230.step`, `axle_front_160.step`, `hinge_cross_shaft_120.step` | Ø8 rod with set-screw flats | buy rod, cut |
| `pulley_HTD5M_20T_ref.step` | bought pulley, reference geometry (stand-in sizes; replace with the vendor's model) | buy |
| `bearing_608ZZ_ref.step`, `nut_M4_ref.step`, `washer_M4_ref.step`, `rod_M4_*.step` | bought hardware, reference | buy |

Not included (other sub-assemblies): box, motor and drive sprocket, hinge sector gears and pinions.
The box interface is on drawing TS-08: Ø4.5 holes through each wall at x = -165 and -25 (60 and 200
from the rear axle), y = 28; walls at z = +/-40, stepping to +/-37 within 25 mm of x = 0.
