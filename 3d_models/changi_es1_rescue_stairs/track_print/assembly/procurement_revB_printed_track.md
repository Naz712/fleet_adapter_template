# Procurement, Rev B build with my printed track

Date 15 Oct 2026. Prices S$ ex GST as seen in listings; confirm at checkout. Rev B = Nhien's pack
(`RB4107 Rev B`), whose BOM covers everything in section 2.

## 1. Mine (track side)

| Part | Qty | Make / buy | Where | Price | Arrives |
|---|---|---|---|---|---|
| Track, TPU 95A, `stl/track_TPU_x4.stl` | 4 | **Make**: Fab Lab UP300 (TPU head) | [Element14 SG TPU 95A filament](https://sg.element14.com/multicomp-pro/mc011460/3d-printer-filament-tpu-1-75mm/dp/3021512) if the lab has none | ~S$45/kg, uses 130 g | filament 1-2 days; 3 h print each |
| Fit-test slice, `stl/fit_test_track_5mm_TPU.stl` | 1 | Make | same | - | 10 min |
| Stand-in pulley, `stl/stand_in_pulley_20T_PLA_test_only.stl` | 1 | Make, PLA | any printer | - | 1 h |
| Timing pulley HTD 5M 20T, 15 mm belt, flanged, **plain (pilot) bore** | 8 | **Buy** | [MISUMI SG, Timing Pulleys HTD 5M](https://sg.misumi-ec.com/vona2/detail/110310532889/) | ~S$20 each | ships 1 day from SG stock; allow 2-5 days |
| Pulley bore modification: 4 x D-bore Ø8 (M1), 4 x Ø16 H7 (M2) | 8 | **Make**: Professional Workshop request, Rev B sheet 21 | E3-01-06 | free | workshop queue, allow 1-2 weeks |

## 2. Nhien's (frame, drive, hinge, electronics), from the Rev B BOM

| Part | Qty | Make / buy | Where |
|---|---|---|---|
| Side plates P1 (front) and P2 (rear), 5 mm Al, laser + tap | 2 + 2 | Make | DXF in the pack; Professional Workshop or a laser shop on the vendor list |
| Slide rails P3-P6, UHMW strip 189 x 20 x 5 | 8 | Buy + drill | [MISUMI SG UPA-189-20-5](https://sg.misumi-ec.com/vona2/mech/M1500000000/M1501000000/) |
| Rail brackets RS PRO 427-991 (angle 15 x 14.6 x 10) | 32 | Buy | [RS SG](https://sg.rs-online.com/) stock no. 427-991 |
| Hinge shafts P20 A 82.3 + B 77.3 (or one 212), Ø8 D-shaft flat 7 | 2 | Buy stock, cut | [RS SG linear shafts](https://sg.rs-online.com/web/c/bearings-seals/linear-motion/linear-shafts/) or MISUMI SG |
| Bearing 688-2RS 8 x 16 x 5 | 14 | Buy | [RS SG ball bearings](https://sg.rs-online.com/web/c/bearings-seals/bearings/ball-bearings/) |
| Shoulder screw ISO 7379 Ø8 x 25 M6 + washers, shim, spacer, nyloc | 4 sets | Buy | [RS SG shoulder screws](https://sg.rs-online.com/web/c/fasteners-fixings/screws-bolts/shoulder-screws/) |
| 2020 profile x 110 (P7) x2, 3030 x 160 (P8) x2, corner posts P15 x4 | 1 m + 0.5 m | Buy, cut | MISUMI SG / local |
| Corner brackets P18 (25x25x4 angle) x4, P19 (20x20x3) x4, T-nuts, E-clips, shims | - | Buy / make | Rev B BOM sections 3-4 |
| Deck P12, tray P16, cover P22, motors, drivers, ESP32, battery | - | Theirs | Rev B BOM |

## 3. What is no longer needed from my earlier list

Printed side plates (4), printed spacers (6), M4 rods and nuts, Ø8 plain rod for three axles, 608ZZ x10,
M4 set screws. Keep the STL files in case the team falls back to the all-printed frame.

## 4. Order of events

1. Order the 8 plain-bore pulleys today (critical path, then the workshop bore mod); print the stand-in
   pulley and fit-test slice; print the 4 tracks as soon as a UP300 slot is free.
2. Nhien: laser plates, order rails, bearings, shoulder screws, profiles.
3. Workshop: pulley bores, plate tapping, shaft cutting (one request form).
4. Assemble per Rev B sheet 3; fit my tracks on the real pulleys; tension at the slots.
