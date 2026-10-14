# Parts list and build guide: track segments of the 1:5 prototype

Numbers from `parts_spec.json` v2 and the TS-00 to TS-07 sheets. Prices S$ ex GST as seen in vendor
listings on 14 Oct 2026 (vendor pages could not be opened from this machine: confirm at checkout).

## 1. Does the track fit the school printers? Yes, in one piece.

| Machine (NUS CDE) | Bed | Track ring Ø183 x 15, printed standing | Side plate 265 x 50 x 11, flat |
|---|---|---|---|
| Tiertime UP300, Fab Lab E4-02-06 (has a TPU extruder head) | 205 x 255 x 225 mm | **fits** (183 wide, 183 tall) | **fits on the diagonal** (327 mm available; 265 needed) |
| Tiertime UP600, Fab Lab E4-02-06 | 400 x 500 x 600 mm | fits | fits straight |
| any hobby printer with a 190 mm bed or less | | does not fit: ask for the two-piece track with links | ask for the two-piece plate |

So: **no split, no links**, as long as the tracks go on the UP300 or UP600. Keep the two-piece version
as a fallback only.

## 2. What is made where, and the one-line justification for the request form

The Professional Workshop (E3-01-06) is CNC mills, a turn-mill and wire EDM: metal parts, done by the
staff from a drawing. The Fab Lab (E4-02-06) is the 3D printers and the laser cutter. Job requests go
through the EDIC request form.

| Part | Qty | Make how | Where | Justification (copy this) |
|---|---|---|---|---|
| Track | 4 | 3D print, TPU 95A, standing, 100% infill, 0.2 mm, no supports. File `stl/track_TPU_x4.stl` | Fab Lab UP300 (TPU head) | A toothed flexible belt with step-matched cleats on the outside; no stock belt has the cleats, and the cleat pitch (12.22 mm) is set by the ES1 step size. |
| Side plate, front L and R, rear L and R | 4 | **Option A:** 3D print PETG, flat, 4 walls, 30% infill. Files `stl/side_plate_{front,rear}_{L,R}.stl`. **Option B:** CNC-mill from 7 mm aluminium plate to sheets TS-02 / TS-03 (the drawings are made for this). | A: Fab Lab UP600 or UP300. B: Professional Workshop, by request form | One part carries the two bearing pockets, the slide rail under the lower track run and all holes; a cut sheet would need the rail and bearing housings as extra parts. |
| Cross bar spacer, 82 (front) and 65 (rear) | 2 + 4 | 3D print PETG (`stl/spacer_front_x2.stl`, `stl/spacer_rear_x4.stl`), or cut from Ø10 aluminium tube with a 4.5 bore on the lathe | Fab Lab, or Training Workshop with the plates | Non-standard lengths set the plate spacing; the rear ones sit between the box wall and the plate. |
| Stand-in pulley, PLA, test only | 1 | 3D print PLA (`stl/stand_in_pulley_20T_PLA_test_only.stl`) | Fab Lab, Tinkering Corner or NUS Library | Fit test of the printed teeth before the bought pulleys arrive. |

If printing is the hassle: **Option B for the plates** moves the biggest print (4 x 5 h) to the
Professional Workshop staff, who machine it from the TS-02/TS-03 drawings. The tracks cannot be
avoided: they must be printed in TPU. Everything else is bought.

## 3. Every piece, and which segment it belongs to

The prototype has two track segments: the **front segment** (hinged, plates inboard) and the **rear
segment** (fixed to the box, plates outboard). They share the middle axle.

### Front segment (sheet TS-00)

| Item | Piece | Qty | Note |
|---|---|---|---|
| 1 | Track | 2 | one each side |
| 2 | Pulley HTD 5M 20T | 4 | 2 each side: one on the middle axle, one on the front axle |
| 3 | Front side plate | 2 | 1 left + 1 right (mirror images, not the same part) |
| 6 | Bearing 608ZZ | 4 | 2 pressed into each plate |
| 5 | Front axle Ø8 x 160 | 1 | |
| 7 | Spacer Ø10 x 82 | 2 | one per cross bar |
| 8 | M4 threaded rod x 110 | 2 | cut from the 1 m rod |
| 8 | M4 nut + M4 washer | 4 + 4 | one each end of each rod |
| 9 | M3 x 14 bolt + M3 nut | 6 + 6 | 3 per plate, hold the hinge sector gears (team's part) |
| - | M4 set screw | 8 | 2 per pulley; MISUMI does not include them |

### Rear segment

| Item | Piece | Qty | Note |
|---|---|---|---|
| 1 | Track | 2 | |
| 2 | Pulley HTD 5M 20T | 4 | 2 each side: middle axle and rear axle |
| - | Rear side plate | 2 | 1 left + 1 right |
| 6 | Bearing 608ZZ | 4 | 2 per plate |
| - | Rear axle Ø8 x 230 | 1 | |
| - | Spacer Ø10 x 65 | 4 | two per rod, one each side between the box wall (z 40) and the plate (z 105) |
| - | M4 threaded rod x 238 | 2 | **these are what bolt the segment to the box**: plate - spacer - box wall - box wall - spacer - plate (sheet TS-08) |
| - | M4 nut + washer | 4 + 4 | one each end of each rod |
| - | M4 set screw | 8 | |

### Shared

| Piece | Qty | Note |
|---|---|---|
| Middle axle Ø8 x 230 (item 4) | 1 | the hinge; carries 4 pulleys (2 front-segment, 2 rear-segment) and runs in all 4 plates' bearings |
| Hinge cross shaft Ø8 x 120 | 1 | runs across the box, carries the hinge pinions (team's part) |
| Bearing 608ZZ | 2 | in the box walls, for the cross shaft |

### Totals to get

| Piece | Total | Make / buy |
|---|---|---|
| Track | 4 | make |
| Pulley 20T | 8 | buy |
| Side plate | 4 (2 front L/R + 2 rear L/R) | make |
| Bearing 608ZZ | 10 | buy (2 packs of 5) |
| Ø8 rod, cut to 230 + 230 + 160 + 120 = 740 mm | 2 x 400 mm | buy (or Design Lab spare) |
| Spacer | 6 (2 x 82, 4 x 65) | make |
| M4 threaded rod, cut to 110 + 110 + 238 + 238 = 696 mm | 1 x 1 m | buy |
| M4 nut / M4 washer | 8 / 8 | buy or Design Lab spares |
| M3 x 14 bolt + nut | 6 + 6 | buy or spares |
| M4 set screw (M4 x 4 or x 5, cup point) | 16 | buy with the pulleys |
| Stand-in pulley, PLA | 1 | make |

## 4. How it goes together (one segment; the other is the same)

1. **Bearings into plates.** Press two 608ZZ into each plate's Ø22.2 pockets (a vice with wood
   packing, or a 22 mm socket as a drift). Flush with the plate face.
2. **Pulleys onto the axles.** Slide each pulley onto its axle, hub facing outboard (away from the
   plate), and set-screw it on the filed flat at the z station on sheet TS-04. On the middle axle
   the order from the centre out, each side, is: front plate bearing (z 41-48), front-segment pulley
   (49-69, hub 69-76), rear-segment pulley (77-97, hub 97-104), rear plate bearing (105-112).
3. **Track on, then the second plate.** Fit the left plate onto the middle and front axles. Loop a
   track over the two left pulleys (TPU stretches a little; walk it on like a bicycle chain). Then
   slide the right plate on and loop the right track. Doing the track before the outer plate is
   what makes it possible.
4. **Cross bars.** Front segment: M4 rod through one plate, the 82 spacer, the other plate; washer
   and nut each end. Rear segment: the same rods also hold the box. Rod through the plate, a 65 spacer,
   through the box wall, across the box, out the other wall, the second 65 spacer, the other plate;
   washer and nut each end, tightened until plates, spacers and box are clamped as one. Two per
   segment, at x 60 and 200 from the rear axle, 28 above the axle line. The box needs two Ø4.5 holes
   through each wall at those positions (sheet TS-08).
5. **Check:** turn the middle axle by hand, both tracks run without clicking; the lower run rests on
   the slide rails.
6. **Hinge (team's parts).** Sector gears bolt to the inboard face of the front plates with the six
   M3 x 14 and nuts (7 plate + 3 gear + nut). The front segment is held to the box only by the middle
   axle and these gears, so it can swing; nothing else is bolted.

## 5. Buy list with links

| Buy | Spec | Where | Price | Qty | Arrives |
|---|---|---|---|---|---|
| Pulley | HTD 5M, 20 T, 15 mm belt, Ø8 bore, flanged, set-screw hub (MISUMI economy family C-HTPA20H5M150, bore 8) | [MISUMI SG, Timing Pulleys HTD 5M](https://sg.misumi-ec.com/vona2/detail/110310532889/) | ~S$20 each (quote) | 8 | ships 1 day from SG stock per the catalogue; allow 2-5 working days |
| Set screws | M4 x 4 cup point (MISUMI MSSU4-3 or equal) | same order, or Design Lab | ~S$0.20 | 16 | with the pulleys |
| Bearing | 608ZZ (608-2Z/C3), 8 x 22 x 7, shielded | [RS SG pack of 5, 261-2603](https://sg.rs-online.com/web/p/ball-bearings/2612603) | S$14.82 per pack | 2 packs | next working day (order before 3:30 pm), max 4 working days |
| Ø8 rod | 8 mm x 400 mm steel shaft; hardened, so grind the flats (Dremel), or buy soft rod from a hardware shop on the vendor list | Design Lab spare first; else [RS SG linear shafts](https://sg.rs-online.com/web/c/bearings-seals/linear-motion/linear-shafts/) | S$37 each at RS; ~S$5 at a hardware shop | 2 | next working day / same day |
| M4 rod | stainless M4 x 1 m, DIN 975 | [RS SG 200-9958](https://sg.rs-online.com/web/p/products/2009958) (pack of 5, S$49.69) or one rod from a hardware shop | S$10 per rod | 1 | 4 working days / same day |
| Nuts, washers, bolts | M4 nuts x 8, M4 washers x 8, M3 x 14 + nuts x 6 | Design Lab spares; else [Element14 SG nuts](https://sg.element14.com/c/fasteners-mechanical/fasteners-fixings/nuts/hex-nuts) and RS SG | S$0 to S$15 | 22 | 1-2 business days |
| TPU filament | TPU 95A, 1.75 mm, 1 kg (4 tracks use about 130 g) | [Element14 SG, Multicomp Pro](https://sg.element14.com/multicomp-pro/mc011460/3d-printer-filament-tpu-1-75mm/dp/3021512), or the Fab Lab's own stock | ~S$45 | 1 | 1-2 business days |

**Totals:** about S$160 of Singapore-priced parts (bearings, rod, M4 rod, nuts), about S$45 with
Design Lab spares, plus the pulleys (~S$160, quote) and TPU (~S$45). Whole set roughly **S$300-370
ex GST**. RS: free delivery over S$150 ex GST on a private account, else S$25 handling.

**Order of events:** day 0 order everything and print the stand-in pulley + fit-test slice; day 1-2
fit test, print or request the plates; day 2-5 parts arrive, press bearings, cut rod; day 3-6 print
tracks, assemble one segment, run it on the test stairs. The pulleys are the only item that can hold
the build up, so order them first.
