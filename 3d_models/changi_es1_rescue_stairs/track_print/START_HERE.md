# Start here: RB4107 track unit, what is where (19 Oct 2026)

Everything for building the track side, in the order you will want it. Paths are from this folder
(`track_print/`). A zipped copy of the same set, sorted into folders, is made from these files.

## 1. Guides (read first)

| File | What it is |
|---|---|
| `assembly/Track_unit_assembly_in_detail.pdf` | The build guide: hinge shaft and pins, idlers, tensioner, fitting the track, rails, order of work (18 pages) |
| `assembly/RB4107_track_complete_pack.pdf` | Everything in one file: checks, build sequence, a page per part, procurement, drawings, Nhien's Rev B sheets with his joint and fastener schedule (59 pages) |
| `assembly/procurement_revB.pdf` (`.md`) | What to buy, how many, where, and when it arrives |

## 2. Drawings to make parts from

`assembly/RB4107_track_drawings_current.pdf` has all of them in one file. Single sheets are in
`assembly/drawings/`: each `TS-` sheet is the dimensioned drawing, the `EX-` sheet after it explains it.

| Sheet | Part |
|---|---|
| TS-01B / EX-01B | The track: bought belt with 22 cleats, 5 high (chosen 19 Oct) |
| TS-01 / EX-01 | Printed TPU track: fallback only, if the bonded belts are late |
| TS-06 / EX-06 | Hinge wheel: bore and Ø2.5 pin hole |
| TS-09 / EX-09 | Tensioner tab, slider and jack screw |
| TS-10 / EX-10 | Rail carrier angle, and how plate, angle, rail and track stack up |
| TS-11 / EX-11 | Hinge shaft stack-up: every gap, shim and pin |
| TS-12 | Hinge shafts A and B; rail trim and pilot holes |

TS-00, TS-02 to TS-05, TS-07 and TS-08 are from the first own-frame layout and are stamped
SUPERSEDED. Do not make parts from them.

## 3. Files for making

- 3D printing (`stl/`), fallback and fit tests only: `track_TPU_x4.stl`, `fit_test_track_5mm_TPU.stl`, `stand_in_pulley_20T_PLA_test_only.stl`.
  The other STL files there belong to the superseded own-frame layout.
- 3D model: `cad/RB4107_track_unit_reviewed.step`. It is behind the Fusion model; see `cad/README.md`.
- Side plates P1 / P2: Nhien's DXF (his pack), being re-issued.
- Tabs, sliders, carrier angles, rails, shafts: made by hand from TS-09, TS-10 and TS-12; no cutting file needed.

## 4. Seeing how it all fits

- `viewer/index.html`: the 3D model to turn around; click a part for what it does and how it is fixed.
  It loads its parts with `fetch`, so open it through a local web server (for example
  `python -m http.server` in `viewer/`, then http://localhost:8000), not by double-clicking.
- Build plan with tick boxes: https://claude.ai/artifact/KMKrvZmELAaKJaMqqfntRJ
- Tensioner page (to scale, drag the jack screw): https://claude.ai/artifact/NDtjKuWCM3VHBkRL4dEiX7

## 5. Background

`FUSION_BRIEF.md` (what changed against Rev B and why), `HANDOVER.md` (decisions, open items, next
steps), `README.md` (dated change notes).
