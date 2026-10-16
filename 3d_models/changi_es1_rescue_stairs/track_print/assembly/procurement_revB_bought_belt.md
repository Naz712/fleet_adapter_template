# Procurement, Rev B build with the bought track belt

Date 16 Oct 2026. Prices S$ ex GST as seen in listings; confirm at checkout. Rev B = Nhien's pack
(`RB4107 Rev B`), whose BOM covers everything in section 2. This is the version with Nhien's belt
(BOM row B10) instead of my printed track; everything else is identical to the printed-track list.

## 1. Track side (bought belt, Rev B B10)

| Part | Qty | Make / buy | Where | Price | Arrives |
|---|---|---|---|---|---|
| Track belt HTD 550-5M-15, 110 teeth, 15 wide (e.g. SKF PHG 550-5M-15) | 4 | **Buy** | [RS SG, stock no. 058-6535](https://sg.rs-online.com/web/c/?searchTerm=058-6535) or MISUMI SG HTD 5M belts | see listing (about S$25-35 each) | RS SG stock: 1-3 days |
| Cleats, rubber 10 x 7.9 x 15, bonded on the belt back every 5th tooth (25 mm), 22 per belt | 88 | **Buy + bond**: belt shop | Local belt / conveyor shop (Fenner, Megadyne or Gates distributor), with the belts | quote | allow 1-2 weeks |
| Deck change for the belt: notch P12 13 x 135 over each front lane (x -25 to 110), or cut the cleats to 5 high | 1 | **Make**: with the deck laser cut, or file / mill after | Professional Workshop | - | with the deck |
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

## 3. What changes against the printed-track version

No TPU filament, no fit-test slice, no printing. Instead: 4 belts from RS, a belt-shop job for the 88
cleats (the long pole, 1-2 weeks), and the deck notch so the cleats clear the deck. The wheels, bore
modification, plates, shafts, bearings and shoulder screws are the same in both versions, so they can
be ordered before the track choice is final.

## 4. Order of events

1. Order the 8 plain-bore pulleys and the 4 belts today (critical path, then the workshop bore mod and
   the belt shop); send the belts with the cleat drawing (TS-01B) to the belt shop.
2. Nhien: laser plates and the notched deck, order rails, bearings, shoulder screws, profiles.
3. Workshop: pulley bores, plate tapping, shaft cutting (one request form).
4. Assemble per Rev B sheet 3; fit the cleated belts on the real pulleys; tension at the slots.
