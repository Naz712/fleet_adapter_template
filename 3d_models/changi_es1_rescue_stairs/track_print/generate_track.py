#!/usr/bin/env python3
"""Printable track for the 1:5 prototype of the ES1 stair carrier.

The prototype is the 2-part carrier from ../track_sim/bending.html: two track units, 140 mm
axle to axle (0.70 m at full size), one track per side on each unit, on 8 mm axles.

The track is a one-piece TPU loop with drive lugs inside and cleats outside, printed upright
as a ring, on printed sprockets. The tracks are matched to the ES1 steps. Measured at
175 mm x 250 mm, they are 35 x 50 mm at 1:5, so their nosings are 61.03 mm apart along the
slope. The cleats are exactly a fifth of that apart (12.21 mm), so when the track lies on the
flight, every step nosing sits in a gap between two cleats. The cleat just above each nosing
then stands on that step's tread, and every step in contact shares the load, like a rack in
a gear. With any other spacing, some nosings land on cleat tips and the track rides on them.

The loop has 31 cleats and the sprockets 8 teeth, which puts the axles (31 - 8) / 2 = 11.5
cleat spacings apart: 140.4 mm, the 0.70 m units of the simulation at 1:5. For other steps
the script picks the cleat count that keeps the axles nearest 140 mm.

Usage:
    pip install manifold3d trimesh numpy matplotlib shapely
    python3 generate_track.py                     # ES1 steps, 35 x 50 mm at 1:5
    python3 generate_track.py --rise 34 --going 56    # other test stairs, at model size

All sizes are millimetres at model size (1:5).
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import trimesh
from manifold3d import CrossSection, JoinType, Manifold, OpType
from shapely.affinity import translate as shp_translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

SEG = 24  # facets on rounded corners
CIRCLE_SEG = 360  # facets on full circles


@dataclass
class Design:
    # The steps the cleats are matched to, at model size: ES1 as measured (175 x 250 mm) at 1:5
    rise: float = 35.0
    going: float = 50.0
    cleats_per_step: int = 5
    # Loop
    sprocket_teeth: int = 8
    cleats: int = 0  # cleats (and drive lugs) around the loop; 0 picks the count nearest the target
    target_centres: float = 140.0  # axle to axle: the 0.70 m units at 1:5
    width: float = 15.0  # across the track
    backing: float = 1.8  # belt thickness between the lugs and the cleats
    # Drive lugs inside and cleats outside: trapezoids (base width, tip width, height)
    lug_base: float = 4.4
    lug_tip: float = 3.0
    lug_height: float = 2.4
    cleat_base: float = 4.4
    cleat_tip: float = 2.4
    cleat_height: float = 3.0  # 15 mm at full size
    tip_round: float = 0.5
    root_fillet: float = 0.4
    # Sprocket
    groove_clearance: float = 0.35  # each side of a lug
    groove_extra_depth: float = 0.4  # below the lug tip
    tooth_round: float = 0.6  # rounds the groove mouths so the lugs slide in
    lane_clearance: float = 0.4  # each side of the track, between the flanges
    flange: float = 1.6  # the flat flange printed on the bed
    flange_flat: float = 0.6  # flat rim on the 45-degree flanges printed above a lane
    flange_inside_back: float = 0.25  # the flange rim stays this far inside the track's outer face
    bore: float = 8.25  # 8 mm axle
    hub_radius: float = 9.5
    hub_length: float = 9.0
    screw_hole: float = 3.2  # M3 grub screw
    nut_slot: float = 5.9  # across the flats of an M3 nut (5.5 mm), plus clearance
    nut_thick: float = 2.8
    # Step gauge: three 1:5 ES1 steps to check the cleats on
    gauge_steps: int = 3
    gauge_width: float = 25.0
    gauge_foot: float = 20.0
    gauge_top: float = 60.0


class Geometry:
    """Everything that follows from the design values."""

    def __init__(self, d: Design):
        self.d = d
        self.slope = math.atan2(d.rise, d.going)
        self.step_pitch = math.hypot(d.rise, d.going)  # nosing to nosing, along the slope
        self.pitch = self.step_pitch / d.cleats_per_step
        if not d.cleats:  # axles are (cleats - teeth) / 2 cleat spacings apart
            d.cleats = d.sprocket_teeth + round(2 * d.target_centres / self.pitch)
        self.centres = (d.cleats - d.sprocket_teeth) * self.pitch / 2
        self.length = d.cleats * self.pitch
        self.ring_radius = self.length / (2 * math.pi)  # backing mid-plane when printed as a ring
        # On a sprocket the belt is rigid over each lug (lug + backing + cleat) and bends between
        # them, so its mid-plane is a polygon of rigid chords and arcs. Solve for its radius.
        b = max(d.lug_base, d.cleat_base)
        theta = 2 * math.pi / d.sprocket_teeth
        lo, hi = b, 10 * self.pitch
        for _ in range(100):
            r = (lo + hi) / 2
            per = r * (theta - 2 * math.asin(b / (2 * r))) + b
            lo, hi = (r, hi) if per < self.pitch else (lo, r)
        self.pitch_radius = (lo + hi) / 2
        self.chord_sag = self.pitch_radius * (1 - math.cos(math.asin(b / (2 * self.pitch_radius))))
        self.land = self.pitch_radius - d.backing / 2  # sprocket surface the belt rests on
        self.back = self.pitch_radius + d.backing / 2  # track's outer face on a sprocket
        self.cleat_tip = self.back + d.cleat_height
        self.groove_bottom = self.land - d.lug_height - d.groove_extra_depth
        self.flange_rim = self.back - d.flange_inside_back
        self.lane = d.width + 2 * d.lane_clearance
        self.chamfer = self.flange_rim - self.land  # 45-degree flange: as tall as it is wide

    def summary(self) -> dict:
        d = self.d
        return {
            "step_mm": [d.rise, d.going],
            "slope_deg": round(math.degrees(self.slope), 2),
            "nosing_to_nosing_mm": round(self.step_pitch, 3),
            "cleat_spacing_mm": round(self.pitch, 3),
            "cleats_per_step": d.cleats_per_step,
            "cleats_per_loop": d.cleats,
            "loop_length_mm": round(self.length, 2),
            "axle_to_axle_mm": round(self.centres, 2),
            "full_size_unit_m": round(self.centres * 5 / 1000, 3),
            "sprocket_teeth": d.sprocket_teeth,
            "sprocket_pitch_diameter_mm": round(2 * self.pitch_radius, 2),
            "axle_to_track_face_mm": round(self.back, 2),
            "axle_to_cleat_tip_mm": round(self.cleat_tip, 2),
            "track_height_over_cleats_mm": round(2 * self.cleat_tip, 2),
        }


# --------------------------------------------------------------------------- 2D profiles
def trapezoid(base: float, tip: float, height: float, sink: float = 0.3):
    """Lug or cleat outline in its own frame: t along the belt, h away from the backing face.
    It starts `sink` inside the backing so it joins it cleanly."""
    return [(-base / 2, -sink), (base / 2, -sink), (base / 2, 0.0), (tip / 2, height),
            (-tip / 2, height), (-base / 2, 0.0)]


def rounded(points, r: float) -> CrossSection:
    cs = CrossSection([points])
    return cs.offset(-r, JoinType.Round, 2.0, SEG).offset(r, JoinType.Round, 2.0, SEG)


def on_circle(points, radius: float, phi: float, outward: int):
    """Map a local outline onto a circle: t along the tangent, h outward (+1) or inward (-1)."""
    u = np.array([math.cos(phi), math.sin(phi)])
    v = np.array([-math.sin(phi), math.cos(phi)])
    out = [tuple((radius + outward * h) * u + t * v) for t, h in points]
    xs, ys = np.array(out).T
    if np.dot(xs, np.roll(ys, -1)) - np.dot(ys, np.roll(xs, -1)) < 0:  # keep it anticlockwise
        out.reverse()
    return out


def circle(r: float) -> CrossSection:
    return CrossSection.circle(r, CIRCLE_SEG)


def track_profile(g: Geometry) -> CrossSection:
    """The track's outline when printed as an upright ring (looking down on the bed)."""
    d = g.d
    inner = g.ring_radius - d.backing / 2
    outer = g.ring_radius + d.backing / 2
    lug = trapezoid(d.lug_base, d.lug_tip, d.lug_height)
    cleat = trapezoid(d.cleat_base, d.cleat_tip, d.cleat_height)
    parts = [circle(outer) - circle(inner)]
    for k in range(d.cleats):
        phi = 2 * math.pi * k / d.cleats
        parts.append(CrossSection([on_circle(lug, inner, phi, -1)]))
        parts.append(CrossSection([on_circle(cleat, outer, phi, +1)]))
    cs = CrossSection.batch_boolean(parts, OpType.Add)
    # round the lug and cleat tips, then fillet their roots
    cs = cs.offset(-d.tip_round, JoinType.Round, 2.0, SEG).offset(d.tip_round, JoinType.Round, 2.0, SEG)
    cs = cs.offset(d.root_fillet, JoinType.Round, 2.0, SEG).offset(-d.root_fillet, JoinType.Round, 2.0, SEG)
    return cs.simplify(0.01)


def groove_outline(g: Geometry):
    d = g.d
    c = d.groove_clearance
    depth = d.lug_height + d.groove_extra_depth + g.chord_sag
    # local: t along the land, h outward from the land (the groove goes inward, h < 0)
    return [(-(d.lug_base / 2 + c), 2.0), (d.lug_base / 2 + c, 2.0), (d.lug_base / 2 + c, 0.0),
            (d.lug_tip / 2 + c, -depth), (-(d.lug_tip / 2 + c), -depth), (-(d.lug_base / 2 + c), 0.0)]


def sprocket_profile(g: Geometry) -> CrossSection:
    d = g.d
    grooves = [CrossSection([on_circle(groove_outline(g), g.land, 2 * math.pi * k / d.sprocket_teeth + math.pi / 2, +1)])
               for k in range(d.sprocket_teeth)]
    cs = circle(g.land) - CrossSection.batch_boolean(grooves, OpType.Add)
    cs = cs.offset(-d.tooth_round, JoinType.Round, 2.0, SEG).offset(d.tooth_round, JoinType.Round, 2.0, SEG)
    cs = cs.offset(0.3, JoinType.Round, 2.0, SEG).offset(-0.3, JoinType.Round, 2.0, SEG)
    return cs.simplify(0.01)  # drop the slivers the offsets leave


# --------------------------------------------------------------------------- solids
def cylinder(r: float, h: float, z0: float = 0.0) -> Manifold:
    return Manifold.cylinder(h, r, r, CIRCLE_SEG).translate((0, 0, z0))


def chamfer_flange(g: Geometry, z0: float) -> Manifold:
    """A flange printed above a lane: a full disc at the land radius (it bridges the grooves
    below), widening at 45 degrees to the rim, then a short flat rim."""
    d = g.d
    h = g.chamfer
    prof = CrossSection([[(0.0, 0.0), (g.land, 0.0), (g.flange_rim, h), (g.flange_rim, h + d.flange_flat),
                          (0.0, h + d.flange_flat)]])
    return Manifold.revolve(prof, CIRCLE_SEG).translate((0, 0, z0))


def hub(g: Geometry, z0: float) -> Manifold:
    """Boss with an M3 grub screw through a captive nut, to clamp the sprocket to its axle."""
    d = g.d
    boss = cylinder(d.hub_radius, d.hub_length, z0)
    zc = z0 + d.hub_length / 2
    screw = Manifold.cylinder(d.hub_radius + 2, d.screw_hole / 2, d.screw_hole / 2, 32) \
        .rotate((0, 90, 0)).translate((0, 0, zc))
    nut_r = (d.bore / 2 + d.hub_radius) / 2
    z_lo, z_hi = zc - 3.4, z0 + d.hub_length + 1  # open at the top, deep enough for the nut's corners
    nut = Manifold.cube((d.nut_thick, d.nut_slot, z_hi - z_lo), True).translate((nut_r, 0, (z_lo + z_hi) / 2))
    return boss - screw - nut


def sprocket(g: Geometry, lanes: int) -> Manifold:
    """Flat flange on the bed, then for each lane the grooved body and a 45-degree flange,
    then the hub. One lane for the end axles, two for the middle axle."""
    d = g.d
    body = sprocket_profile(g)
    parts = [cylinder(g.flange_rim, d.flange)]
    z = d.flange
    e = 0.05  # each piece overlaps the one below, so they fuse into one body
    for _ in range(lanes):
        parts.append(Manifold.extrude(body, g.lane + e).translate((0, 0, z - e)))
        z += g.lane
        parts.append(chamfer_flange(g, z - e))
        z += g.chamfer + d.flange_flat - e
    parts.append(hub(g, z - e))
    z += d.hub_length - e
    solid = Manifold.batch_boolean(parts, OpType.Add)
    bore = cylinder(d.bore / 2, z + 2, -1)
    # small 45-degree lead-in on the bed side so the first layer doesn't close the bore
    lead = Manifold.cylinder(0.6, d.bore / 2 + 0.6, d.bore / 2, CIRCLE_SEG).translate((0, 0, -0.001))
    return solid - bore - lead


def track(g: Geometry, width: float | None = None) -> Manifold:
    return Manifold.extrude(track_profile(g), width or g.d.width)


def step_gauge(g: Geometry, base: float = 5.0) -> Manifold:
    """A few 1:5 ES1 steps on a 5 mm base, printed lying on their side, to try the track on."""
    d = g.d
    x_last = d.gauge_foot + (d.gauge_steps - 1) * d.going  # the top riser
    x_end = x_last + d.gauge_top
    top = d.gauge_steps * d.rise
    outline = [(0.0, -base), (x_end, -base), (x_end, top)]  # anticlockwise: base, far end
    for i in range(d.gauge_steps, 0, -1):  # back down the steps: tread, then riser
        x = d.gauge_foot + (i - 1) * d.going
        outline += [(x, i * d.rise), (x, (i - 1) * d.rise)]
    outline.append((0.0, 0.0))
    return Manifold.extrude(CrossSection([outline]), d.gauge_width)


# --------------------------------------------------------------------------- checks
def poly(points) -> Polygon:
    return Polygon(points).buffer(0)


def check_seating(g: Geometry, rise: float | None = None, going: float | None = None) -> dict:
    """Lay the track's lower run on a flight and slide it along the slope. Reports how far it
    can move with every nosing in contact sitting in a gap (no cleat in a step), and where it
    rests: with the cleat above each nosing standing on that step's tread.

    Frame: s along the slope (uphill +), n out of the stairs. The track face lies on n = 0,
    touching the nosings; the cleats hang below it, into the stairs' side."""
    d = g.d
    rise = rise or d.rise
    going = going or d.going
    slope = math.atan2(rise, going)
    step = math.hypot(rise, going)
    contact = g.centres  # length of track face lying on the flight
    nosings = [i * step for i in range(int(contact // step) + 1)]
    # one step's solid near its nosing, in (s, n): the tread runs uphill below the face at the
    # slope angle, the riser runs downhill below it at 90 degrees minus the slope
    deep = 3 * d.cleat_height

    def step_solid(s0):
        return poly([(s0, 0), (s0 + deep / math.tan(slope), -deep), (s0 - deep / math.tan(math.pi / 2 - slope), -deep)])

    stairs = unary_union([step_solid(s) for s in nosings])
    cleat = trapezoid(d.cleat_base, d.cleat_tip, d.cleat_height)
    cleat_poly = rounded(cleat, d.tip_round).to_polygons()[0]
    one = poly([(t, -h) for t, h in cleat_poly])

    def cleats_at(phase):
        n = int((contact + 2 * g.pitch) // g.pitch) + 2
        return unary_union([shp_translate(one, phase + k * g.pitch - g.pitch, 0) for k in range(n)])

    # scan the phase over one cleat spacing for clear positions
    phases = np.linspace(0, g.pitch, 1201)[:-1]
    clear = np.array([cleats_at(p).intersection(stairs).area < 1e-6 for p in phases])
    out = {"rise": rise, "going": going, "nosings_in_contact": len(nosings)}
    if not clear.any():
        out.update(seated=False, slack_mm=0.0)
        return out
    # longest run of clear phases (wrapping round)
    runs = []
    c2 = np.concatenate([clear, clear])
    i = 0
    while i < len(c2):
        if c2[i]:
            j = i
            while j < len(c2) and c2[j]:
                j += 1
            runs.append((i, j))
            i = j
        else:
            i += 1
    best = max(runs, key=lambda r: r[1] - r[0])
    dp = phases[1] - phases[0]
    slack = min(best[1] - best[0], len(clear)) * dp
    out.update(seated=True, slack_mm=round(slack, 2),
               rest_phase_mm=round((best[0] * dp) % g.pitch, 3),
               tolerance_per_step_mm=round(slack / max(1, len(nosings) - 1), 2))
    return out


def check_mesh(g: Geometry) -> dict:
    """Pose a lug as it sits on the sprocket (a rigid chord of the belt) and measure its
    clearance to the groove."""
    d = g.d
    prof = sprocket_profile(g)
    sprocket_poly = unary_union([Polygon(p) for p in prof.to_polygons()])
    # the groove centred at the top of the sprocket (phi = 90 degrees + k * 45)
    lug = rounded(trapezoid(d.lug_base, d.lug_tip, d.lug_height, sink=0), d.tip_round).to_polygons()[0]
    base_r = g.land - g.chord_sag  # the rigid chord's inner face at the groove centre
    lug_poly = poly([(t, base_r - h) for t, h in lug])
    return {
        "lug_overlaps_sprocket_mm2": round(lug_poly.intersection(sprocket_poly).area, 4),
        "lug_clearance_mm": round(lug_poly.distance(sprocket_poly), 3),
    }


def to_mesh(m: Manifold) -> trimesh.Trimesh:
    mesh = m.to_mesh64()  # float32 would merge near-coincident points into slivers
    return trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3], faces=np.asarray(mesh.tri_verts), process=True)


# --------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rise", type=float, help="step height at model size (mm)")
    ap.add_argument("--going", type=float, help="step depth, nosing to nosing, at model size (mm)")
    ap.add_argument("--cleats", type=int, help="cleats around the loop (default: nearest to 140 mm axle to axle)")
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "stl")
    args = ap.parse_args()
    d = Design()
    if args.rise:
        d.rise = args.rise
    if args.going:
        d.going = args.going
    if args.cleats:
        d.cleats = args.cleats
    g = Geometry(d)
    args.out.mkdir(parents=True, exist_ok=True)

    parts = {
        "track_TPU_x4": track(g),
        "sprocket_end_PETG_x4": sprocket(g, 1),
        "sprocket_middle_double_PETG_x2": sprocket(g, 2),
        "fit_test_track_5mm_TPU": track(g, 5.0),
        "step_gauge_3_steps_1-5_PLA": step_gauge(g),
    }
    report = {"design": asdict(d), "geometry": g.summary(), "parts": {}}
    for name, m in parts.items():
        mesh = to_mesh(m)
        bodies = len(m.decompose())
        ok = mesh.is_watertight and bodies == 1
        assert ok, f"{name}: watertight={mesh.is_watertight}, bodies={bodies}"
        mesh.export(args.out / f"{name}.stl")
        ext = mesh.bounds[1] - mesh.bounds[0]
        report["parts"][name] = {"size_mm": [round(v, 1) for v in ext], "volume_cm3": round(m.volume() / 1000, 2),
                                 "watertight": mesh.is_watertight, "bodies": bodies}
    report["mesh_check"] = check_mesh(g)
    report["seating"] = check_seating(g)
    (args.out / "track.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report[k] for k in ("geometry", "mesh_check", "seating")}, indent=2))
    for k, v in report["parts"].items():
        print(f"{k:34s} {v['size_mm']} mm  {v['volume_cm3']} cm3")


if __name__ == "__main__":
    main()
