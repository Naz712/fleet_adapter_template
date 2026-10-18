# Procurement: the track unit on Nhien's Rev B frame

Date 16 Oct 2026. Prices S$ ex GST as seen in listings; confirm at checkout. Rev B = Nhien's pack
(`RB4107 Rev B`), whose BOM covers everything in section 2. The track comes in two options, A and B;
everything else is the same whichever is chosen, so section 2 and the pulleys can be ordered first.

## 1A. Track, option A: my printed track

| Part | Qty | Make / buy | Where | Price | Arrives |
|---|---|---|---|---|---|
| Track, TPU 95A, `stl/track_TPU_x4.stl` (drawing TS-01) | 4 | **Make**: Fab Lab UP300 (TPU head) | [Element14 SG TPU 95A filament](https://sg.element14.com/multicomp-pro/mc011460/3d-printer-filament-tpu-1-75mm/dp/3021512) if the lab has none | ~S$45/kg, uses 130 g | filament 1-2 days; 3 h print each |
| Fit-test slice, `stl/fit_test_track_5mm_TPU.stl` | 1 | Make | same | - | 10 min |
| Stand-in pulley, `stl/stand_in_pulley_20T_PLA_test_only.stl` | 1 | Make, PLA | any printer | - | 1 h |

Deck: no change needed; the 3 mm cleats sit 5 mm under the deck.

## 1B. Track, option B: Nhien's bought belt with cleats (Rev B B10)

| Part | Qty | Make / buy | Where | Price | Arrives |
|---|---|---|---|---|---|
| Track belt HTD 550-5M-15, 110 teeth, 15 wide (e.g. SKF PHG 550-5M-15), drawing TS-01B | 4 | **Buy** | [RS SG, stock no. 058-6535](https://sg.rs-online.com/web/c/?searchTerm=058-6535) or MISUMI SG HTD 5M belts | see listing (about S$25-35 each) | RS SG stock: 1-3 days |
| Cleats, rubber 10 x 7.9 x 15, bonded on the belt back every 5th tooth (25 mm), 22 per belt | 88 | **Buy + bond**: belt shop | Local belt / conveyor shop (Fenner, Megadyne or Gates distributor), with the belts | quote | allow 1-2 weeks |
| Deck change for the belt: notch P12 13 x 135 over each front lane (x -25 to 110), or cut the cleats to 5 high | 1 | **Make**: with the deck laser cut, or file / mill after | Professional Workshop | - | with the deck |

## 1C. Wheels, both options

| Part | Qty | Make / buy | Where | Price | Arrives |
|---|---|---|---|---|---|
| Timing pulley HTD 5M 20T, 15 mm belt, flanged, **plain (pilot) bore** | 8 + 1 to practise boring and pinning on | **Buy** | [MISUMI SG, Timing Pulleys HTD 5M](https://sg.misumi-ec.com/vona2/detail/110310532889/) | ~S$20 each | ships 1 day from SG stock; allow 2-5 days |
| Pulley bore modification: 4 x ream Ø8 H7 (hinge, M1 and M3 stage-2) and 4 x bore Ø16 H7 (idlers, M2); hub cross holes Ø2.5 drilled on the press when boring, shaft drilled through them at assembly (TS-06, TS-11) | 8 + 2 | **Make**: Professional Workshop request | E3-01-06 | free | workshop queue, allow 1-2 weeks |
| Spring pins ISO 8752 2.5 x 24 (hinge pulleys and stage-2 pulleys, replaces E-clips F22 and the D-flats) | 6 + 4 spare | **Buy** | [RS SG spring pins](https://sg.rs-online.com/web/c/fasteners-fixings/pins/spring-pins/) | ~S$5 / pack | RS SG stock |
| Hinge shaft: plain round Ø8 h7 ground steel, 300 mm (100 mm to practise on) (replaces the D-shaft B13; cut to 82.3 and 77.3, no grooves) | 1 | **Buy**, cut | [RS SG linear shafts](https://sg.rs-online.com/web/c/bearings-seals/linear-motion/linear-shafts/) or MISUMI SG PSFJ8 | ~S$10 | RS SG stock |

## 1D. Tension and rail support (from the design review), both options

| Part | Qty | Make / buy | Where | Price | Arrives |
|---|---|---|---|---|---|
| Tensioner tab, Al angle 20 x 20 x 3 cut 30 with a 7.5 x 8 ear, M4 tapped (TS-09) | 4 | **Make**: hacksaw, drill, M4 tap | from BOM B16 angle (order 300 mm instead of 100) | - | 1 h |
| Tensioner slider, an 8 mm slice of the same angle, leg 19 with Ø6.4, foot 8 (TS-09; replaces the M6 washer under the nut) | 4 | **Make**: hacksaw, drill | from the same angle (order 400 mm) | - | 30 min |
| Jack screw M4 x 20 socket head + M3 x 6 for the tab | 4 + 4 | **Buy** | RS / local | - | stock |
| New M3 tapped holes in P1 and P2: (x +-223, y +11) for the tab (TS-09) and six at (x +-40, +-105, +-170; y +-3.5) for the carriers (TS-10) | 4 | **Make**: add to the DXF, or drill 2.5 + tap M3 on site | with the plates | - | with the plates |
| Rail carrier angle, Al 10 x 10 x 1.5 x 186, plate leg cut to 6.5, 3 + 3 holes (TS-10; replaces the 32 RS 427-991 clips) | 8 | **Make**: from 1.6 m of angle | local metal supplier / MISUMI SG | ~S$10 | 1-3 days |
| Rails P3-P6 trimmed from 189 to 186 at the idler end (TS-10, TS-11) | 8 | Make: hacksaw | - | - | 10 min |

## 2. Nhien's (frame, drive, hinge, electronics), from the Rev B BOM

| Part | Qty | Make / buy | Where |
|---|---|---|---|
| Side plates P1 (front) and P2 (rear), 5 mm Al, laser + tap | 2 + 2 | Make | DXF in the pack; Professional Workshop or a laser shop on the vendor list |
| Slide rails P3-P6, UHMW strip 189 x 20 x 5 | 8 | Buy + drill | [MISUMI SG UPA-189-20-5](https://sg.misumi-ec.com/vona2/mech/M1500000000/M1501000000/) |
| Rail brackets RS PRO 427-991 (angle 15 x 14.6 x 10) | 32 | Buy | [RS SG](https://sg.rs-online.com/) stock no. 427-991 |
| Hinge shafts P20 A 82.3 + B 77.3, now plain round Ø8 h7 (section 1C), no D-flat, no E-clip grooves | 2 | Buy stock, cut | see 1C |
| Bearing 688-2RS 8 x 16 x 5 | 14 | Buy | [RS SG ball bearings](https://sg.rs-online.com/web/c/bearings-seals/bearings/ball-bearings/) |
| Shoulder screw ISO 7379 Ø8 x 25 M6 + washers, shim, spacer, nyloc | 4 sets | Buy | [RS SG shoulder screws](https://sg.rs-online.com/web/c/fasteners-fixings/screws-bolts/shoulder-screws/) |
| 2020 profile x 110 (P7) x2, 3030 x 160 (P8) x2, corner posts P15 x4 | 1 m + 0.5 m | Buy, cut | MISUMI SG / local |
| Corner brackets: standard cast 2020 and 3030 inside corner brackets instead of the P18 / P19 angle offcuts (bigger contact area, design review); T-nuts, shims 8x11x0.5 and 8x11x1; E-clips F22 no longer needed | - | Buy | MISUMI SG / local |
| Deck P12 (slot H 3 mm longer, see pack page 2), tray P16, cover P22, motors, drivers, ESP32, battery | - | Theirs | Rev B BOM |
| Bearing seats in P1, P2, P17: laser-cut Ø15.8, reamed Ø16 H7 on site, 688-2RS retained with Loctite 641 (TS-11) | 6 | Make | Professional Workshop, 16 H7 reamer |

## 3. Choosing between A and B

Option A is in-house: four 3 h prints, no supplier, 5 mm deck clearance, and the cleat spacing is matched
to the ES1 step. Option B is bought: belts from RS in days, but the 88 cleats need a belt shop (1-2 weeks)
and the deck needs a notch or shorter cleats. Wheels, bore modification, plates, shafts, bearings and
shoulder screws are the same in both.

## 4. Order of events

1. Order the 8 plain-bore pulleys today (critical path, then the workshop bore mod); for option B also
   order the 4 belts and send them with TS-01B to the belt shop. For option A print the stand-in pulley
   and fit-test slice, then the 4 tracks as soon as a UP300 slot is free.
2. Nhien: laser plates and deck (slot H 74 long; notched if option B), order rails, bearings, shoulder
   screws, profiles.
3. Workshop: pulley bores, plate tapping, shaft cutting (one request form).
4. Assemble per Rev B sheet 3; fit the tracks on the real pulleys; tension at the slots.
