# Procurement list: track segments of the 1:5 prototype

Short answer: **print the track, buy the wheels.** The wheels are the HTD 5M 20-tooth timing pulleys
(item 2 on sheet TS-00, sheet TS-06). Everything with a shape only this design needs is printed;
everything that is a standard part is bought. Quantities are for the whole prototype (two segments),
from `parts_spec.json` v2. Prices are S$ ex GST as seen in vendor listings on 14 Oct 2026; the
vendor pages could not be opened from this machine, so confirm at checkout. "Arrives" is the
vendor's stated delivery for Singapore stock, counted from the order.

| # | Part (sheet) | Make / buy | Where (link) | Price | Qty | Arrives |
|---|---|---|---|---|---|---|
| 1 | Track, TPU 95A (TS-01) `stl/track_TPU_x4.stl` | **Make**: 3D print | Design Lab or NUS E4-02-06 printer with a direct-drive extruder (the Library printer is PLA only). Filament: [Multicomp Pro TPU 95A 1.75 mm 1 kg, Element14 Singapore](https://sg.element14.com/multicomp-pro/mc011460/3d-printer-filament-tpu-1-75mm/dp/3021512) | about S$35-55 per kg (uses ~130 g for 4 tracks) | 4 | filament 1-2 business days (SG stock); printing about 3 h per track |
| 2 | Timing pulley HTD 5M, 20 T, 15 mm belt, Ø8 bore, flanged (TS-06) | **Buy** | [MISUMI Singapore, Timing Pulleys HTD 5M, economy series](https://sg.misumi-ec.com/vona2/detail/110310532889/): pick 20 teeth, belt width 15, bore 8 (part code family C-HTPA20H5M150). Fixing screws are not included: add 16 x M4 set screws (MISUMI MSSU4-3 or Design Lab spares) | about S$20 each (US listing of the same spec, converted); MISUMI quote | 8 | catalogue says ships in 1 day from Singapore stock; allow 2-5 working days with account set-up |
| 3 | Side plates, PETG (TS-02, TS-03) `stl/side_plate_*.stl` | **Make**: 3D print | Design Lab / E4-02-06, bed 235 mm or 225 diagonal | ~S$1.10 material each | 4 (2 L + 2 R) | 4-5 h print each |
| 4 | Axles Ø8: 230, 230, 160 + hinge cross shaft 120 (TS-04) | **Buy** rod, cut | First: Design Lab spare 8 mm rod (EA-03-04). Else [RS Singapore linear shafts](https://sg.rs-online.com/web/c/bearings-seals/linear-motion/linear-shafts/): 2 x 400 mm Ø8 (e.g. Ewellix, S$37.36 each, or Bosch Rexroth 724-3392). These are hardened: grind the set-screw flats with a Dremel instead of filing, or buy soft mild-steel rod from a hardware shop on the vendor list (Teck Huat, Hillside Hardware) | S$37.36 per 400 mm (RS) or ~S$5 at a hardware shop | 2 lengths (cut 230+160 and 230+120) | RS: next working day if ordered before 3:30 pm, Singapore stock; up to 4 working days otherwise |
| 5 | Ball bearing 608ZZ 8x22x7 (TS-07) | **Buy** | [RS PRO 608-2Z/C3, RS Singapore 188-3314](https://sg.rs-online.com/web/p/products/1883314) (single) or [pack of 5, 261-2603](https://sg.rs-online.com/web/p/ball-bearings/2612603) S$14.82 | S$3.11 each | 10 (2 packs of 5) | 657 in stock; within 4 working days (next working day for SG stock, order before 3:30 pm) |
| 6 | Cross bar spacers Ø10, 82 and 210 (TS-05) `stl/spacer_*.stl` | **Make**: 3D print | with the plates | ~S$0.70 all | 2 + 2 | 20 min each |
| 7 | M4 threaded rod: 2 x 110 + 2 x 238 = 696 mm | **Buy**, cut from 1 m | [RS PRO stainless M4 x 1 m, RS Singapore 200-9958](https://sg.rs-online.com/web/p/products/2009958) sold as pack of 5 S$49.69; or one rod from a hardware shop on the list | S$9.94 per rod (pack of 5 = S$49.69) | 1 rod | RS: within 4 working days; hardware shop: same day |
| 8 | M4 nuts x 8, M4 washers x 8, M4 x 12 bolts x 4, M3 x 14 bolts + nuts x 6 | **Buy** (Design Lab spares first) | Design Lab. Else [Element14 Singapore hex nuts](https://sg.element14.com/c/fasteners-mechanical/fasteners-fixings/nuts/hex-nuts) (M4 pack of 100 about S$6.46) and RS Singapore for the bolts | S$0 from spares, else ~S$15 for the smallest packs | 26 pieces | Element14: 1-2 business days (SG stock) |
| 9 | Stand-in pulley, PLA, test only `stl/stand_in_pulley_20T_PLA_test_only.stl` | **Make**: 3D print | NUS Library (PLA) or Design Lab | under S$1 | 1 | 1 h print |

Not in this list (team's parts, outside the track scope): the drive sprocket or gear on the middle
axle, the hinge sector gears and pinions, the hinge cross-shaft gears, both motors, and the box.

## Totals

- Bought, Singapore prices found: bearings 29.64 + 2 shafts 74.72 + M4 rod pack 49.69 + nuts 6.46 =
  **about S$160 ex GST**; about **S$45** if the Design Lab's spare rod, nuts and screws are used.
- Still to quote: 8 pulleys (about S$160 at the US price) and TPU filament (about S$45). Whole set
  roughly **S$300-370 ex GST**, before any student discount (RS gives 5-15% if asked).
- Delivery charges: RS is free over S$150 ex GST for private accounts (S$25 handling below that),
  or over S$28 with a business account. Element14 and MISUMI: check at checkout.

## Order of events (critical path = the pulleys)

1. **Day 0:** print the stand-in pulley and the 5 mm fit-test slice (PLA + TPU, same day if a TPU
   printer is free). Order the pulleys, bearings, rod and filament the same day; everything above is
   Singapore stock, so it all lands within about a week.
2. **Day 1-2:** fit test: the slice's teeth must drop into the stand-in pulley. Print the four plates
   and spacers meanwhile (about 20 h of printer time in all).
3. **Day 2-5:** pulleys, bearings and rod arrive. Press the bearings into the plates, cut and deburr
   the axles, grind the flats.
4. **Day 3-6:** print the four tracks (about 12 h). Assemble one segment, run it on the test stairs.

If MISUMI's lead time turns out longer than the catalogue's 1 day, the bought pulleys are the only
item that holds the build up: run the first tests on the PLA stand-ins, never the final ones.

Sources: [MISUMI SG HTD 5M page](https://sg.misumi-ec.com/vona2/detail/110310532889/),
[MISUMI SG economy catalogue p.547](https://sg.c.misumi-ec.com/book/MSEA_EconomySeries_e-Catalogue202401/files/basic-html/page547.html),
[RS SG delivery](https://sg.rs-online.com/web/content/support/all-articles/delivery),
[RS SG 608-2Z/C3](https://sg.rs-online.com/web/p/products/1883314),
[RS SG M4 rod](https://sg.rs-online.com/web/p/products/2009958),
[Element14 SG TPU](https://sg.element14.com/multicomp-pro/mc011460/3d-printer-filament-tpu-1-75mm/dp/3021512),
[Element14 SG hex nuts](https://sg.element14.com/c/fasteners-mechanical/fasteners-fixings/nuts/hex-nuts).
