#!/usr/bin/env python3
"""Printable track for the 1:5 prototype of the ES1 stair carrier.

The prototype is the team's 2-part base at 1:5: two track segments, 225 mm axle to axle
(45 cm in all), each with a 550 mm track loop on wheels about 1.5 cm in radius. The track is a
one-piece TPU loop printed upright as a ring. Inside it has HTD 5M teeth, so it runs on bought
HTD 5M 20-tooth pulleys (31.8 mm pitch diameter): 110 teeth make the 550 mm loop, and
(550 - 100) / 2 puts the axles exactly 225 mm apart.

Outside, the cleats are matched to the ES1 steps. Measured at 175 x 250 mm, they are 35 x 50 mm
at 1:5, so their nosings are 61.03 mm apart along the slope. 45 cleats round the 550 mm loop are
12.22 mm apart, a fifth of that to within 0.1 mm a step, so when the track lies on the flight
every step nosing sits in a gap between two cleats and the cleat above it stands on the tread.
Every step in contact shares the load, like a rack in a gear. With other spacings some nosings
land on cleat tips and the track rides on them.

Usage:
    pip install manifold3d trimesh numpy matplotlib shapely
    python3 generate_track.py                         # ES1 steps, 35 x 50 mm at 1:5
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
    # Drive: bought HTD 5M pulleys
    belt_pitch: float = 5.0
    pld: float = 0.5715  # HTD 5M: pitch line to tooth root
    pulley_teeth: int = 20  # 31.8 mm pitch diameter, about 1.5 cm wheel radius
    belt_teeth: int = 110  # 550 mm loop, axles 225 mm apart
    # Track
    width: float = 15.0  # across the track, for pulleys made for 15 mm belts
    backing: float = 1.4  # belt thickness between the teeth and the cleats
    tooth_height: float = 2.0  # HTD 5M teeth are 2.06 mm; a hair less so they seat in stock pulleys
    tooth_radius: float = 1.45  # round-topped tooth, 2.7 mm wide at the root before the fillets
    cleat_base: float = 4.4
    cleat_tip: float = 2.4
    cleat_height: float = 3.0  # 15 mm at full size
    tip_round: float = 0.5
    root_fillet: float = 0.35
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
        self.length = d.belt_teeth * d.belt_pitch
        self.cleats = round(self.length * d.cleats_per_step / self.step_pitch)
        self.pitch = self.length / self.cleats  # cleat spacing
        self.pulley_pitch_r = d.pulley_teeth * d.belt_pitch / (2 * math.pi)
        self.centres = (self.length - d.pulley_teeth * d.belt_pitch) / 2
        self.ring_radius = self.length / (2 * math.pi)  # pitch line when printed as a ring
        self.root = self.pulley_pitch_r - d.pld  # pulley outside radius: the tooth roots sit on it
        self.back = self.root + d.backing  # axle to the track's outer face
        self.cleat_tip = self.back + d.cleat_height

    def summary(self) -> dict:
        d = self.d
        return {
            "step_mm": [d.rise, d.going],
            "slope_deg": round(math.degrees(self.slope), 2),
            "nosing_to_nosing_mm": round(self.step_pitch, 3),
            "cleats_per_loop": self.cleats,
            "cleat_spacing_mm": round(self.pitch, 3),
            "five_cleats_vs_step_mm": round(5 * self.pitch - self.step_pitch, 3),
            "loop_length_mm": round(self.length, 1),
            "belt_teeth": d.belt_teeth,
            "pulley": f"HTD 5M, {d.pulley_teeth} teeth, {2 * self.pulley_pitch_r:.2f} mm pitch diameter",
            "axle_to_axle_mm": round(self.centres, 2),
            "full_size_segment_m": round(self.centres * 5 / 1000, 3),
            "axle_to_track_face_mm": round(self.back, 2),
            "axle_to_cleat_tip_mm": round(self.cleat_tip, 2),
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


def tooth_outline(d: Design, sink: float = 0.3):
    """HTD-style round-topped tooth in its own frame: t along the belt, h in from the tooth root."""
    hc = d.tooth_height - d.tooth_radius
    a0 = math.asin(hc / d.tooth_radius)
    w0 = math.sqrt(d.tooth_radius ** 2 - hc ** 2)
    arc = [(d.tooth_radius * math.cos(a), hc + d.tooth_radius * math.sin(a))
           for a in np.linspace(-a0, math.pi + a0, 40)]
    return [(w0, -sink)] + arc + [(-w0, -sink)]


def track_profile(g: Geometry) -> CrossSection:
    """The track's outline when printed as an upright ring (looking down on the bed)."""
    d = g.d
    root = g.ring_radius - d.pld
    outer = root + d.backing
    tooth = tooth_outline(d)
    cleat = trapezoid(d.cleat_base, d.cleat_tip, d.cleat_height)
    parts = [circle(outer) - circle(root)]
    parts += [CrossSection([on_circle(tooth, root, 2 * math.pi * k / d.belt_teeth, -1)]) for k in range(d.belt_teeth)]
    parts += [CrossSection([on_circle(cleat, outer, 2 * math.pi * k / g.cleats, +1)]) for k in range(g.cleats)]
    cs = CrossSection.batch_boolean(parts, OpType.Add)
    # round the cleat tips, then fillet the tooth and cleat roots
    cs = cs.offset(-d.tip_round, JoinType.Round, 2.0, SEG).offset(d.tip_round, JoinType.Round, 2.0, SEG)
    cs = cs.offset(d.root_fillet, JoinType.Round, 2.0, SEG).offset(-d.root_fillet, JoinType.Round, 2.0, SEG)
    return cs.simplify(0.01)


# --------------------------------------------------------------------------- solids
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
    contact = g.centres  # length of track face lying on the flight, axle to axle
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


def check_teeth(g: Geometry) -> dict:
    """The printed teeth must be no bigger than a standard HTD 5M belt tooth (2.06 mm high,
    about 3.05 mm wide at the root) so they seat in stock pulleys."""
    d = g.d
    tooth = poly(tooth_outline(d, sink=0))
    minx, _, maxx, maxy = tooth.bounds
    return {"tooth_height_mm": round(maxy, 2), "tooth_root_width_mm": round(maxx - minx, 2),
            "fits_htd5m_pulley": bool(maxy <= 2.06 and maxx - minx <= 3.05)}


def to_mesh(m: Manifold) -> trimesh.Trimesh:
    mesh = m.to_mesh64()  # float32 would merge near-coincident points into slivers
    return trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3], faces=np.asarray(mesh.tri_verts), process=True)


# --------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rise", type=float, help="step height at model size (mm)")
    ap.add_argument("--going", type=float, help="step depth, nosing to nosing, at model size (mm)")
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "stl")
    args = ap.parse_args()
    d = Design()
    if args.rise:
        d.rise = args.rise
    if args.going:
        d.going = args.going
    g = Geometry(d)
    args.out.mkdir(parents=True, exist_ok=True)

    parts = {
        "track_TPU_x4": track(g),
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
    report["teeth"] = check_teeth(g)
    report["seating"] = check_seating(g)
    (args.out / "track.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report[k] for k in ("geometry", "teeth", "seating")}, indent=2))
    for k, v in report["parts"].items():
        print(f"{k:34s} {v['size_mm']} mm  {v['volume_cm3']} cm3")


if __name__ == "__main__":
    main()
