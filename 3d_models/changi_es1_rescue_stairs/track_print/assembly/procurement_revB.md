# Procurement: the track unit on Nhien's Rev B frame

Date 16 Oct 2026, updated 20 Oct (3 x 5 rail screws; stage-2 pulleys with hub and set screws in seats, no stage-2 pins). Prices S$ ex GST as seen in listings; confirm at checkout. Rev B = Nhien's pack
(`RB4107 Rev B`), whose BOM covers everything in section 2. The track comes in two options, A and B;
everything else is the same whichever is chosen, so section 2 and the pulleys can be ordered first.

## 1A. Track: bought belts with cleats (chosen 19 Oct; Rev B B10)

| Part | Qty | Make / buy | Where | Price | Arrives |
|---|---|---|---|---|---|
| Track belt HTD 550-5M-15, 110 teeth, 15 wide (e.g. SKF PHG 550-5M-15), drawing TS-01B | 4 | **Buy** | [RS SG, stock no. 058-6535](https://sg.rs-online.com/web/c/?searchTerm=058-6535) or MISUMI SG HTD 5M belts | see listing (about S$25-35 each) | RS SG stock: 1-3 days |
| Cleats, rubber 10 x **5** x 15 (cut down from 7.9, Nhien 19 Oct), bonded on the belt back every 5th tooth (25 mm), 22 per belt | 88 | **Buy + bond**: belt shop | Local belt / conveyor shop (Fenner, Megadyne or Gates distributor), with the belts | quote | allow 1-2 weeks |
| Deck change for the belt: **not needed**, the 5 mm cleats pass 2.9 under the deck (Nhien 19 Oct) | 0 | - | - | - | - |

## 1B. Track fallback: printed TPU track (only if the bonded belts will be late)

| Part | Qty | Make / buy | Where | Price | Arrives |
|---|---|---|---|---|---|
| Track, TPU 95A, `stl/track_TPU_x4.stl` (drawing TS-01) | 4 | **Make**: Fab Lab UP300 (TPU head) | [Element14 SG TPU 95A filament](https://sg.element14.com/multicomp-pro/mc011460/3d-printer-filament-tpu-1-75mm/dp/3021512) if the lab has none | ~S$45/kg, uses 130 g | filament 1-2 days; 3 h print each |
| Fit-test slice, `stl/fit_test_track_5mm_TPU.stl` | 1 | Make | same | - | 10 min |
| Stand-in pulley, `stl/stand_in_pulley_20T_PLA_test_only.stl` | 1 | Make, PLA | any printer | - | 1 h |

Deck: no change needed; the 3 mm cleats sit 5 mm under the deck.

## 1C. Wheels

| Part | Qty | Make / buy | Where | Price | Arrives |
|---|---|---|---|---|---|
| Timing pulley HTD 5M 20T, 15 mm belt, flanged (19 Oct: MISUMI economy HTD 5M, code **H5M**, not S5M). **Hinge wheels: 4 + 1 with a finished Ø8 bore**: shaft-hole type H (plain round, no tapped hole) if the configurator offers it for 20T, else P (round with tapped hole, ignore the screw; pin hole 90° from it). **Idlers: 4 with the smallest bore offered**, bored to Ø16 at the workshop (20T stops at about Ø15, so no 16 bore). Before ordering, check on the drawing: width over the flanges 19 or less (the lane is 20) and no hub (shape B has a Ø19 hub) | 8 + 1 | **Buy** | [MISUMI SG, Timing Pulleys HTD 5M](https://sg.misumi-ec.com/vona2/detail/110310532889/) | ~S$20 each | ships 1 day from SG stock; allow 2-5 days |
| Pulley bore modification: 4 x bore Ø16 H7 (idlers, M2) only; the hinge wheels come bored Ø8. Stage-2 pulleys come bored Ø8 (no ream). Ø2.5 cross holes drilled on our drill press in a V-block, shaft drilled through them at assembly (TS-06, TS-11) | 4 + 2 | **Make**: Professional Workshop request | E3-01-06 | free | workshop queue, allow 1-2 weeks |
| Spring pins ISO 8752 2.5 x 24 (hinge pulleys, replaces E-clips F22 and the D-flats) | 4 + 4 spare | **Buy** | [RS SG spring pins](https://sg.rs-online.com/web/c/fasteners-fixings/pins/spring-pins/) | ~S$5 / pack | RS SG stock |
| ~~Spring pins 2.5 x 12~~: **not needed** since 20 Oct, the stage-2 pulleys use set screws in seats | 0 | - | - | - | - |
| Stage-2 pulley: MISUMI economy HTD 5M (code **H5M**) for 9 mm belt, **with hub**, bore Ø8 type P (two tapped holes); tooth count as in Nhien's model; check the hub length fits his base (it sets the shaft length) | 2 + 1 spare | **Buy** (Nhien, confirm) | [MISUMI SG timing pulleys](https://sg.misumi-ec.com/vona2/detail/110310532889/) | ~S$6-10 each | 1 day from SG stock; allow 2-5 days |
| Set screws, **cone point**, size to suit the pulley's tapped holes (usually M3 or M4 x 4-5), 2 per stage-2 pulley, each into a seat spot-drilled about 1 mm into the shaft, Loctite 243. Check whether MISUMI includes them | 4 + 4 spare | **Buy** | [RS SG set screws](https://sg.rs-online.com/web/c/fasteners-fixings/screws-bolts/set-screws/) | ~S$3 / pack | RS SG stock |
| Hinge shaft: plain round Ø8 h7 ground steel, 300 mm (100 mm to practise on) (replaces the D-shaft B13; cut to 82.3 and 77.3, no grooves) | 1 | **Buy**, cut | [RS SG linear shafts](https://sg.rs-online.com/web/c/bearings-seals/linear-motion/linear-shafts/) or MISUMI SG PSFJ8 | ~S$10 | RS SG stock |

## 1D. Tension and rail support (from the design review)

| Part | Qty | Make / buy | Where | Price | Arrives |
|---|---|---|---|---|---|
| Tensioner tab, Al angle 20 x 20 x 3 cut 30 with a 7.5 x 8 ear, M4 tapped (TS-09) | 4 | **Make**: hacksaw, drill, M4 tap | from BOM B16 angle (order 300 mm instead of 100) | - | 1 h |
| Tensioner slider, an 8 mm slice of the same angle, leg 19 with Ø6.4, foot 8 (TS-09; replaces the M6 washer under the nut) | 4 | **Make**: hacksaw, drill | from the same angle (order 400 mm) | - | 30 min |
| Thread-forming screws 3 x 5 pan head for plastics (rail to carrier angle, 3 per rail; 3 x 5 not 3 x 10: the rail is 5 thick) | 24 + 6 spare | **Buy** | [RS SG thread-forming screws](https://sg.rs-online.com/web/c/fasteners-fixings/screws-bolts/thread-forming-screws/) | ~S$6 / pack | RS SG stock |
| M3 x 6 SHCS ISO 4762 (carrier angles to plates 24, tensioner tab ears 4) | 28 + 4 spare | **Buy** | RS SG | ~S$5 / pack | RS SG stock |
| Jack screw M4 x 20 socket head + M3 x 6 for the tab | 4 + 4 | **Buy** | RS / local | - | stock |
| New M3 tapped holes in P1 and P2: (x +-223, y +11) for the tab (TS-09) and six at (x +-40, +-105, +-170; y +-3.5) for the carriers (TS-10) | 4 | **Make**: drill 2.5 + tap M3 on site (Nhien 19 Oct: no DXF re-issue) | with the plates | - | with the plates |
| Rail carrier angle, Al 10 x 10 x 1.5 x 186, plate leg cut to 6.5, 3 + 3 holes (TS-10; replaces the 32 RS 427-991 clips) | 8 | **Make**: from 1.6 m of angle | local metal supplier / MISUMI SG | ~S$10 | 1-3 days |
| Rails P3-P6 trimmed from 189 to 186 at the idler end (TS-10, TS-11) | 8 | Make: hacksaw | - | - | 10 min |

## 2. Nhien's (frame, drive, hinge, electronics), from the Rev B BOM

| Part | Qty | Make / buy | Where |
|---|---|---|---|
| Side plates P1 (front) and P2 (rear), 5 mm Al, laser + tap | 2 + 2 | Make | DXF in the pack; Professional Workshop or a laser shop on the vendor list |
| Slide rails P3-P6, UHMW strip 189 x 20 x 5 | 8 | Buy + drill | [MISUMI SG UPA-189-20-5](https://sg.misumi-ec.com/vona2/mech/M1500000000/M1501000000/) |
| ~~Rail brackets RS PRO 427-991~~: **do not order**, replaced by the TS-10 carrier angles (1D) | 0 | - | - |
| Hinge shafts P20 A 82.3 + B 77.3, now plain round Ø8 h7 (section 1C), no D-flat, no E-clip grooves | 2 | Buy stock, cut | see 1C |
| Sector gear P11: proposed KHK SSAY1-100 (module 1, 100 teeth, 20°, face 6, bore 10, S45C, flat plate) cut to a 23-tooth sector (plan 5.14); **Nhien OK 19 Oct**: centre distance 60.1 to 60.2, base already changed for the new sector | 1 | Buy, cut | KHK catalog (thin-face hubless SSAY series, about US$43) or MISUMI SG (KHK brand), search SSAY1-100; plan B any 1M 100T 45# steel gear from Shopee / AliExpress, faced to 6 mm at the Professional Workshop |
| Bearing 688-2RS 8 x 16 x 5 | 14 | Buy | [RS SG ball bearings](https://sg.rs-online.com/web/c/bearings-seals/bearings/ball-bearings/) |
| Shoulder screw ISO 7379 Ø8 x 25 M6 + washers, shim, spacer, nyloc | 4 sets | Buy | [RS SG shoulder screws](https://sg.rs-online.com/web/c/fasteners-fixings/screws-bolts/shoulder-screws/) |
| 2020 profile x 110 (P7) x2, 3030 x 160 (P8) x2, corner posts P15 x4 | 1 m + 0.5 m | Buy, cut | MISUMI SG / local |
| Corner brackets: standard cast 2020 and 3030 inside corner brackets instead of the P18 / P19 angle offcuts (bigger contact area, design review); T-nuts, shims 8x11x0.5 and 8x11x1; E-clips F22 no longer needed | - | Buy | MISUMI SG / local |
| Deck P12 (slot H 3 mm longer, see pack page 2), tray P16, cover P22, motors, drivers, ESP32, battery | - | Theirs | Rev B BOM |
| Bearing seats in P1, P2, P17: laser-cut Ø15.8, reamed Ø16 H7 on site, 688-2RS retained with Loctite 641 (TS-11) | 6 | Make | Professional Workshop, 16 H7 reamer |

## 3. Track choice: bought belts (decided 19 Oct)

**19 Oct: option B, Nhien's belts.** He has cut the cleats to 5 mm (no deck notch) and will have the
belt maker bond them, since they need a chemical bond to the belt. Allow 1 to 2 weeks for that, so the
belts go out first. Option A (printed track) stays as the fallback if the bonded belts are late.

## 4. Order of events (19 Oct)

1. Mon 19 to Tue 20 Oct: belts and cleats to the belt maker (Nhien, 1 to 2 weeks: now on the critical path).
   Check the MISUMI H5M 20T 150 drawing (19 or less over the flanges, no hub),
   then order the pulleys (4 + 1 bored 8, 4 idlers smallest bore), the RS order (shaft, pins, screws,
   jack screws) and the aluminium angle. (The printed track is only the fallback: no printing needed unless the belts run late.)
2. 22 to 29 Oct: plates from Nhien's existing DXF (no re-issue); drill and tap the new M3 holes on site. As parts arrive, make
   the tabs, sliders and carrier angles, trim and drill the rails, drill the hinge wheels' Ø2.5 holes.
3. When the idlers arrive (about 23 to 26 Oct): one workshop request for the idler bores (16 H7) and, once the plates are back, the bearing seats (16 H7). Allow 1 to 2 weeks.
4. 9 to 10 Nov: assemble; 11 to 13 Nov: tension and run tests; 16 Nov: advisor demo.
