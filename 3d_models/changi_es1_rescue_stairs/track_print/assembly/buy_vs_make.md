# Buy or make: the track segments of the 1:5 prototype

> **Superseded (21 Oct 2026).** This is from the first own-frame layout with the printed track. The build now uses
> Nhien's Rev B frame and **bought belts with 5 mm bonded cleats**. Current list: `procurement_revB.md`; start at `../START_HERE.md`.

Source of the parts and sizes: `parts_spec.json` in this folder (1:5 model size, mm). Quantities are
for the whole prototype, two segments, as `qty_total` gives them. Vendors are from the school's
approved vendor list (`vendors.txt`), or "print" for parts we make ourselves.

Prices are Singapore dollars **excluding GST** (9% is added at checkout). They come from web search
results of vendor listings seen on 13 Oct 2026; the vendor pages themselves could not be opened from
this machine, so confirm every price before ordering. Each price is marked:

- **est.** = seen in a listing (or worked out from one, and the working is shown), or
- **quote** = no Singapore price found; ask the vendor. No price here is made up.

## The table

| Part | Make or buy | Why (one line) | Where | Est. unit price S$ | Qty | Est. total S$ |
|---|---|---|---|---|---|---|
| Track, TPU 95A, 15 mm wide, 110 HTD 5M teeth inside, 45 cleats outside (`stl/track_TPU_x4.stl`, 32 g) | **Make** (3D print) | Only this design has this shape: belt teeth inside, step-matched cleats outside, one piece | **Print**: a direct-drive printer that takes TPU (Design Lab, or NUS E4-02-06 Centralised Lab). The NUS Library printer is PLA only. If none is free: a 3D printing service on the list, e.g. Siege Advanced Manufacturing (instant quote by file upload) | **quote** for filament. No SGD listing found for TPU 95A. Foreign listings converted run about S$35 to S$80 per kg, so material is about S$1 to S$3 per track (est.) | 4 | **quote** (material est. S$4 to S$12; a printing service: quote) |
| Timing pulley HTD 5M, 20 T, for 15 mm belt, 8 mm bore, flanges both sides, set-screw hub | **Buy** | A machined aluminium standard part; the track is designed to its 31.83 mm pitch diameter; a printed pulley wears and skips | **MISUMI Singapore** (sg.misumi-ec.com; its HTD 5M economy pulley series lists 20 T, 15 mm belt, 8 mm bore). Alternative: Hinode (gears and sprockets, on the list) | **quote** (MISUMI). For scale only: a US listing of the same spec is US$15.34, about S$20 at 1.28 S$/US$ (est.) | 8 | **quote** (about S$160 if the US price holds, est.) |
| Stand-in pulley, 20 T, PLA (`stl/stand_in_pulley_20T_PLA_test_only.stl`, 14 cm3, about 17 g) | **Make** (3D print), fit tests only | Checks that the printed teeth mesh before the real pulleys arrive; never for driving | **Print**: Design Lab, or NUS Library (PLA, UP Box+) | material est. under S$1 (17 g PLA); Library service fee: **quote** | 1 | est. under S$1 + any service fee |
| Axle, 8 mm steel rod, h7: rear 220, middle 220, front 160 | **Buy** (cut to length) | Stock 8 mm rod fits the 608 bores and the pulley bores; nobody prints an axle | **Design Lab spare 8 mm rod (EA-03-04) first.** Else RS Singapore: Ewellix 8 mm x 400 mm steel shaft, h6, S$37.36 ex GST. Or MISUMI linear shaft (quote), or plain 8 mm steel rod from Teck Huat Hardware or a hardware shop on the list (quote) | est. **S$37.36** per 400 mm length (RS). S$0 if from the Design Lab | 2 lengths: cut 220 + 160 from one, 220 from the other (180 mm left over) | est. **S$74.72** (or S$0) |
| Hinge cross shaft (carries the hinge pinions on the box; runs in the 2 spare 608ZZ) | **Buy** (cut from the same rod) | Same 8 mm rod as the axles, so the two 608ZZ the spec sets aside for it fit | Same as the axles | Diameter 8 mm follows from the 608ZZ. **Length is not in the spec**: at least the 80 mm box width (z = +/-40) plus the pinions and two bearings; fix it when the hinge drawing is done | 1 | **quote** (fits in the 180 mm offcut if it is 180 mm or shorter: S$0 extra) |
| Ball bearing 608ZZ, 8 x 22 x 7 | **Buy** | A S$3 standard part; pressed into a 22.2 mm pocket in each plate, so no KFL08 housing | **RS Singapore**: RS PRO 608-2Z/C3, S$3.11 ex GST each; pack of 5 S$14.82. Alternatives on the list: Wheeler Mectrade, Kaichin Electronics (Sim Lim Tower), any SKF distributor | est. **S$3.11** | 10 (8 in the plates + 2 for the hinge cross shaft) | est. **S$31.10** (S$29.64 as 2 packs of 5) |
| Side plate with slide rail, PETG, 265 x 40 x 7 stadium, rail 185 x 18 x 4, 2 bearing pockets dia 22.2; 4 variants (front/rear, left/right) | **Make** (3D print) | Bearing pockets, rail, web and all holes come out in one part; a flat sheet cannot carry the stepped rail | **Print**: Design Lab or NUS E4-02-06 (PETG, flat on the bed, 0.2 mm layers, 4 walls, 30% infill) | est. **S$1.10** material each: about 70 g PETG (86 to 87 cm3 of outline at roughly 60 to 65% solid), PETG at about S$10 to S$17 per kg on Carousell Singapore | 4 | est. **S$4.40** material (machine time is free in-house; a service: quote) |
| Cross bar rod, M4 threaded: 2 x 110 mm (front segment) + 2 x 230 mm (rear segment) = 680 mm | **Buy** (cut 4 from one 1 m rod) | Standard studding; ties the two plates of a segment parallel | **RS Singapore**: RS PRO stainless M4 x 1 m, sold as a pack of 5 at S$49.69 ex GST (about S$9.94 a rod). Or one rod from a hardware shop on the list (Teck Guan, Hillside Hardware delivers and quotes) | est. **S$9.94** per 1 m rod | 1 rod | est. **S$9.94** (but RS only sells 5: S$49.69; one rod from a hardware shop: quote) |
| Cross bar spacer, printed tube, 10 mm OD, 82 mm (front) / 202 mm (rear) long, bore to clear M4 | **Make** (3D print) | Odd lengths, trivial shape; prints with the plates | **Print** (same PETG as the plates) | est. **S$0.10** (82 mm, about 7 g) / **S$0.25** (202 mm, about 16 g) | 2 + 2 | est. **S$0.70** |
| M4 hex nuts for the cross bars | **Buy** (Design Lab spares first) | Standard | Design Lab. Else RS Singapore: M4 hex nut DIN 934, zinc steel, bag of 250, S$9.79 ex GST; or Element14 Singapore: M4 pack of 100, S$3.26 | est. **S$0.04** each | 8 (one each end of 4 rods; the spec says 4, see "Changes to report") | S$0 from spares, else est. **S$3.26 to S$9.79** for the smallest bag |
| Other fasteners: 8 x M4 washers, 6 x M3 x 10 (hinge sector gears), 4 x M4 x 12 (box cross bars), 1 x M3 x 6 set screw (stand-in pulley) | **Buy** (Design Lab spares first) | Standard | Design Lab. Else a hardware shop on the list, or RS / Element14 | **quote** | 19 | S$0 from spares, else **quote** |
| Pulley set screws (usually M4, 2 per pulley) | Come with the bought pulleys | Included | MISUMI, with the pulleys | included | 16 | S$0 |

### Totals

- **Singapore prices found, per part (est.): about S$131** = bearings 31.10 + shaft 74.72 + M4 rod 9.94
  + M4 nuts 9.79 + plates 4.40 + spacers 0.70. This drops to about **S$46** if the Design Lab's spare
  8 mm rod and nuts are used.
- **Same list as RS actually sells it (pack sizes): about S$170**, because the M4 rod comes in a
  pack of 5 (S$49.69).
- **Still to quote**: the 8 pulleys (the largest item; about S$160 if the US price carries over),
  TPU filament or a print service, the hinge cross shaft length, screws and washers. With the
  foreign-listing estimates for pulleys and TPU added, the whole segment pair comes to roughly
  **S$300 ex GST** before any discount.
- Before ordering: RS gives students 5 to 15% off if asked; ask every vendor whether they take
  30-day terms without an NUS purchase order (see the top of the vendor list); check the Design Lab
  for small items (rod, nuts, screws) before buying any.

## How the parts turn, and how they link to the motor and the box

All of this is in `parts_spec.json` (`layout_decision`); it is repeated here because the drawings
show the parts one at a time.

- **Every pulley is set-screwed to its axle** (a filed flat under each set screw). The **axles turn**
  in the 608ZZ bearings pressed into the plates; the plates themselves do not turn with the axle.
- **One motor drives everything.** The drive motor turns the **middle axle** through a sprocket that
  sits on it between the two front plates, inside the box (the box ends at z = 40 each side; the
  front plates are at z = 41 to 48). Because the middle axle carries the rear pulley of the front
  segment and the front pulley of the rear segment, both segments' tracks are driven from it. The
  rear and front axles are idlers: they turn because the track turns their pulleys.
- **The middle axle is also the hinge.** The front segment pivots about it on its plate bearings.
  The hinge sector gear bolts to the rear end of each front plate (3 x M3 on a 14 mm radius); its
  pinion sits on the **hinge cross shaft**, which runs across the box in the two spare 608ZZ. Turning
  the cross shaft turns the sector gears, so the front segment bends up or down about the middle
  axle while the tracks keep running. The sector gear, pinion and hinge motor are outside this
  drawing set.
- **The rear segment is fixed to the box.** Its outboard plates (z = 101 to 108) carry 2 x M4 holes
  at x = -60 and -200 from the middle axle, 22 mm above the axle line, for the box cross bars
  (4 x M4 x 12). The front segment's plates are tied to each other only by their two cross bars
  (M4 rod + 82 mm spacer) so the segment can swing.
- **The lower run of each track rides on the plate's slide rail** (top face 13.34 mm below the axle),
  so the track cannot sag between the pulleys when it is on the steps.

## What changed from the quotation slide

| Slide said | Now | Why |
|---|---|---|
| 8 x KFL08 flange bearing blocks | 10 x 608ZZ ball bearings pressed into the printed plates | A KFL08 housing is 48 x 26 x 12 mm. At 1:5 there is no room for it between the box (z = 40) and the track lanes (z = 49 onwards); a 608ZZ is 22 mm across and sits inside the 7 mm plate. It also costs less (S$3.11 each at RS). The two extra bearings are for the hinge cross shaft. |
| Axles 200 / 200 / 150 mm | 220 / 220 / 160 mm | The layout puts the rear segment's plates outboard (to z = 108 each side), so the rear and middle axles must reach 216 mm plus a little; the front axle only reaches the front pulley hubs (z = 74, so 148 mm plus a little). |
| No cross bars | 4 cross bars: M4 threaded rod with printed spacers (82 mm front, 202 mm rear), nut each end | Something has to hold the two plates of a segment parallel and at the right distance; the axles alone cannot, because they turn in the bearings. |
| Plates laser-cut (sheet) | Plates 3D printed in PETG, 7 mm, with the slide rail, web, bearing pockets and holes in one part | The rail steps 4 mm out from the plate face and the pockets are blind to 7 mm; a cut sheet would need the rail as a second glued part and the bearings in housings. Printing gives one part per side, no glue, no extra hardware. |

## Decisions for the team

**Plates: printed PETG or laser-cut acrylic?**

- Print them (the current spec) when: the Design Lab printer is free (4 plates at about 70 g each,
  roughly 4 to 5 hours each at 0.2 mm layers), you want the bearing pockets and rail in one piece,
  and the layout may still change (a reprint costs about S$1.10 in material).
- Laser-cut them when: the printers are tied up or the prints warp, or you want a stiffer, flatter
  plate. Then: cut 2 flat plates per side from 6 mm or 8 mm acrylic (Latech Engineering, Top Point
  Plastics or Dama Enterprise on the list, all quote), cut the rail as a separate strip and glue or
  screw it on, and go back to housed bearings. With KFL08 housings the layout widens by 12 mm per
  side (`parts_spec.json`, bearing alternative), so the cross bars, axles and the box mounts all
  change. Acrylic also cracks at pressed-in bearings, so the 22.2 mm pocket does not transfer.
- Either way the four plates are two mirror pairs; do not cut or print four of the same.

**The stand-in pulley is for fit tests only.** Print one, press the 5 mm fit-test track slice onto it
and then a full track, and check the teeth drop in and the track does not ride up the flanges. Do not
run the prototype on it: PLA teeth round off and the M3 set screw will not hold the drive torque.
Order the 8 bought pulleys as soon as the fit test passes; MISUMI lead time is the critical path.

**Fallback belt: stock 550-5M-15.** If the printed TPU teeth skip on the pulleys, a stock
550-5M-15 HTD belt (110 teeth, 550 mm, 15 mm wide) fits the same pulleys and the same 225 mm axle
spacing; the cleats are then printed as TPU strips and glued to the belt back. Price: quote from
RS Singapore (the 9 mm wide version is listed there at S$13.67 ex GST; the 15 mm version is listed
on RS Netherlands at EUR 13.23 ex VAT, so expect about S$20 each, est.). Qty 4 if used. Decide after
the first full track has run on real pulleys, not before: the stock belt has no cleats and the whole
point of the printed track is the step-matched cleat pitch.

## Changes to report in `parts_spec.json` (not edited here)

1. `set_screws_and_bolts.items`: "4 x M4 nuts" should be **8 x M4 nuts** (a nut at each end of the
   4 cross bar rods, as `cross_bar.note` says).
2. Add a `hinge_cross_shaft` entry: 8 mm rod, length to be fixed from the hinge drawing, runs in the
   2 extra 608ZZ already counted in `bearing.qty_total`. Today the shaft exists only as a mention in
   the bearing note.
3. `axle`: add **"unhardened"** (or "soft steel") to the spec, or change `flats` to "grind". The
   off-the-shelf linear shafts (RS / Ewellix, 56 to 64 HRC) cannot be filed for the set-screw flats.
4. `cross_bar`: add the spacer bore (4.5 mm, the same as `cross_bar_holes.dia_mm`) so the spacer
   drawing has it.
5. `pulley`: record the vendor part number once MISUMI has quoted, and replace the stand-in's flange
   and hub sizes with the vendor's.
