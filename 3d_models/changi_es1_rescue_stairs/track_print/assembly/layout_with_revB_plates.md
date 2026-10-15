# Layout with Nhien's side plates (Rev B P1 / P2): what changes on the track side

Read from `RB4107 Rev B/STEP` (plates P1, P2 and the full assembly, 15 Oct 2026). Rev B's frame
origin is the hinge axis with the A side at z < 60; below everything is converted to **z from the
vehicle centre line**, one side (the other mirrors), mm at 1:5.

## Their plates

| | Rev B plate | My printed plate (for comparison) |
|---|---|---|
| Material | 5 mm aluminium 6061, laser cut, holes tapped | 7 mm PETG, printed |
| Size | 255 x 30.4 (R15 ends) | 265 x 45 (R20 ends) |
| Axle spacing | 225 (hinge hole to the middle of the idler slot) | 225 |
| Hinge hole | Ø16 for a 688-2RS bearing (8 x 16 x 5) | Ø22.2 for a 608ZZ |
| End hole | slot 220.4-232.6 for an Ø8 shoulder-screw stub axle: slide to tension the track | round pocket |
| Rail | separate UHMW strips P3-P6, screwed on through the C holes with small brackets | printed as part of the plate |
| Cross bars | 2020 profile x 110 (front), 3030 profile x 160 (rear), corner brackets + T-nuts | M4 rod + printed spacer |

## Where everything sits across the width (per side, from the centre line)

| z | What |
|---|---|
| 0 to 24 (A side) / 29 (B side) | free: hinge shaft ends here, hinge pinion / sector gear region |
| 36 to 41 | P17 hinge-shaft bearing support (688 bearing), bolted to the middle 3030 bar |
| **55 to 60** | **front plate P1** (688 bearing in it at the hinge) |
| 60.5 to 79.5 | front segment track lane: pulley 19 over flanges, track 62.5 to 77.5 |
| **80 to 85** | **rear plate P2** (688 bearing at the hinge) |
| 85.5 to 104.5 | rear segment track lane, **outboard of the rear plate**; track 87.5 to 102.5 |
| 106 | end of the hinge shaft |

So: 205 over the track faces, 209 over the pulley flanges, and the frame between the rear plates
is 160 wide inside (not 80 as in my layout): the box can be up to 160 wide.

## Consequences for the parts I was making

| Part | With their plates |
|---|---|
| **Track x4** | unchanged: 550 loop, 110 teeth, 15 wide, 45 cleats. Still printed. The only printed part left. |
| **Side plates** | theirs (P1, P2). Not printed. |
| **Spacers** | **none.** The 2020 and 3030 bars hold the plates apart. |
| **Cross bar rods, nuts, washers** | **none.** Replaced by the bars, P18/P19 corner brackets, T-nuts. |
| **Middle axle 230** | replaced by Rev B's two hinge half-shafts P20: Ø8 D-shaft (flat 7), A = 82.3 long (z 14 to 106 on the A side), B = 77.3 (z 31 to 106 on the B side). Two halves because Rev B has one motor per side. If the team goes to **one motor**, use one Ø8 D-shaft 212 long (z -106 to +106) instead, same stock. |
| **Front and rear axles** | **none.** The end pulleys ride on Ø8 x 25 M6 shoulder screws (ISO 7379) through the plate slots, one per plate, 4 in all, each with two 688-2RS inside a Ø16-bored pulley. |
| **Bearings** | 608ZZ x10 -> **688-2RS x14** (8 x 16 x 5): 4 in the plate hinge holes, 2 in the P17 supports, 8 in the idler pulleys. |
| **Pulleys** | same HTD 5M 20T 15 mm belt, but the lanes are only 19-20 wide, so there is **no room for a set-screw hub**. Rev B modifies them: the 4 on the hinge shaft get a D-bore 8 (M1), the 4 idlers get a Ø16 H7 bore for the 688s (M2). That is lathe work at the Professional Workshop; order plain-bore (pilot-bore) pulleys for it. |
| **Set screws** | none on the pulleys (D-bore drives them); E-clips DIN 6799-6 and a shim on each shaft end instead. |

## What I need from Nhien to finish the hybrid

1. One motor or two? It decides whether the hinge shaft is one piece (212) or two (82.3 + 77.3).
2. Confirm the rail strips P3-P6 are coming (MISUMI UPA-189-20-5 UHMW, 8 off) or whether the lower
   run just rides on nothing; my track's tooth tips sit 13.34 below the axle and need the rail.
3. The track is still mine to print; the step-matched cleat pitch (12.22) replaces Rev B's 22 cleats
   at 25 mm on a stock belt. Both fit the same pulleys, so either can be tested on their frame.
