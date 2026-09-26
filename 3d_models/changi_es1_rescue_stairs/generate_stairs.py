#!/usr/bin/env python3
"""Parametric 3D-print model of the Changi Airport Emergency Service "ES1"
rescue stairs (Rosenbauer E8000-type), staircase only (no vehicle).

Every design dimension below is a real-world millimetre value. The finished
model is scaled down on export (default 1:100). Features that would be too thin
to print at that scale (handrails, side panels, embossed livery) are thickened
to a printable minimum automatically.

Layout of each model (X = up the stairs, Y = left, Z = up):

    ground -> bottom flight (18 treads / 19 risers of 170 mm) -> 1000 mm mid
    platform -> upper flight (as many ~170 mm risers as the height needs)
    -> 2800 x 3000 mm top platform (flush with the right-hand side, like the
    real vehicle, extending to the left)

Usage:
    pip install manifold3d trimesh numpy matplotlib
    python3 generate_stairs.py                        # 3.2 / 5.8 / 8.4 m at 1:100
    python3 generate_stairs.py --scale 50 --heights 3200 8400
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import trimesh
from manifold3d import CrossSection, FillRule, JoinType, Manifold, OpType


@dataclass
class Design:
    # From the brief
    stair_width: float = 1500.0  # clear walking width between the side panels
    rise: float = 170.0  # step height
    lower_treads: int = 18  # treads in the bottom flight; riser 19 lands on the mid platform
    mid_platform_len: float = 1000.0
    # Assumed / Rosenbauer E8000 data
    going: float = 280.0  # tread depth, nosing to nosing (31.3 deg flight)
    top_platform_len: float = 2800.0  # along the stair axis
    top_platform_width: float = 3000.0
    # Side structure, as vertical offsets from the walking line (pitch line / floor)
    guard_top: float = 900.0  # top of the solid red side panel
    rail_height: float = 1050.0  # handrail centre line
    panel_bottom: float = 300.0  # red panel lower edge
    beam_bottom: float = 750.0  # grey side beam lower edge
    soffit: float = 350.0  # underside of the steps / platform floor
    panel_thk: float = 100.0
    beam_inset: float = 30.0  # grey beam sits back from the red panel face
    rail_dia: float = 50.0
    post_dia: float = 50.0
    post_spacing: float = 1200.0
    hole_dia: float = 220.0  # lightening holes in the upper side beams
    hole_pitch: float = 600.0
    bumper: float = 120.0  # rubber bumper on the platform's docking edge
    # Livery (embossed so it can be painted or printed in a second colour)
    stripe_width: float = 150.0
    stripe_low: float = -120.0  # stripe centre on the rear half of the bottom flight
    stripe_high: float = 600.0  # ... after the jog, along the rest of the stairs
    stripe_platform: float = 150.0  # ... along the top platform fascia
    emboss: float = 5.0
    label: str = "ES1"
    label_height: float = 450.0


# Smallest printable sizes in *model* millimetres (0.4 mm nozzle FDM).
MIN_MODEL_MM = dict(panel_thk=1.0, rail_dia=1.0, post_dia=0.9, emboss=0.4, beam_inset=0.3)
# Display stand, in model millimetres (not part of the real vehicle).
STAND_MM = dict(column=3.0, brace=1.5, base_thk=2.0, base_margin=3.0, base_radius=3.0,
                label_strip=8.0, label_text=4.0, label_relief=0.6)

COLOURS = ("red", "silver", "grey", "lime")  # also the overlap priority order
SEG = 16  # facets on round parts


# --------------------------------------------------------------------------- primitives
def box(x0, x1, y0, y1, z0, z1) -> Manifold:
    return Manifold.cube((x1 - x0, y1 - y0, z1 - z0)).translate((x0, y0, z0))


def section(points) -> CrossSection:
    return CrossSection([np.asarray(points, dtype=float)], FillRule.NonZero)


def prism_xz(cs: CrossSection, y0: float, y1: float) -> Manifold:
    """Extrude a cross-section drawn in (x, z) between y0 and y1."""
    return Manifold.extrude(cs, y1 - y0).rotate((90, 0, 0)).translate((0, y1, 0))


def rod(p, q, r: float, seg: int = SEG) -> Manifold:
    p, q = np.asarray(p, float), np.asarray(q, float)
    d = q - p
    length = float(np.linalg.norm(d))
    u = d / length
    z = np.array([0.0, 0.0, 1.0])
    v = np.cross(z, u)
    s, c = float(np.linalg.norm(v)), float(z @ u)
    if s < 1e-9:
        rot = np.eye(3) if c > 0 else np.diag([1.0, -1.0, -1.0])
    else:
        vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        rot = np.eye(3) + vx + vx @ vx * ((1 - c) / s**2)
    return Manifold.cylinder(length, r, r, seg).transform(np.hstack([rot, p.reshape(3, 1)]))


def tube(points, r: float) -> Manifold:
    """Round tube along a 3D polyline with rounded joints and ends."""
    parts = [rod(a, b, r) for a, b in zip(points[:-1], points[1:])]
    parts += [Manifold.sphere(r, SEG).translate(tuple(p)) for p in points]
    return Manifold.batch_boolean(parts, OpType.Add)


def text_section(text: str, height: float, mirror: bool = False) -> CrossSection:
    from matplotlib.font_manager import FontProperties
    from matplotlib.textpath import TextPath

    path = TextPath((0, 0), text, size=1.0, prop=FontProperties(family="DejaVu Sans", weight="bold"))
    polys = [np.asarray(p, float) for p in path.to_polygons() if len(p) > 2]
    allp = np.vstack(polys)
    lo, hi = allp.min(axis=0), allp.max(axis=0)
    k = height / (hi[1] - lo[1])
    out = []
    for p in polys:
        q = (p - lo) * k
        if mirror:
            q[:, 0] = -q[:, 0]
        out.append(q)
    return CrossSection(out, FillRule.EvenOdd)


def union(parts) -> Manifold:
    parts = [p for p in parts if p is not None and not p.is_empty()]
    if not parts:
        return Manifold()
    return Manifold.batch_boolean(parts, OpType.Add)


def drop_slivers(m: Manifold, min_volume: float = 1e3) -> Manifold:
    """Remove the zero-volume sheets left where two colour bodies share a face."""
    keep = [c for c in m.decompose() if abs(c.volume()) > min_volume]
    return Manifold.compose(keep) if keep else Manifold()


# --------------------------------------------------------------------------- the model
class RescueStairs:
    def __init__(self, d: Design, height: float, scale: float, stand: bool = True):
        self.d, self.scale, self.stand = d, scale, stand
        s = scale
        self.t = max(d.panel_thk, MIN_MODEL_MM["panel_thk"] * s)
        self.rail_r = max(d.rail_dia, MIN_MODEL_MM["rail_dia"] * s) / 2
        self.post_r = max(d.post_dia, MIN_MODEL_MM["post_dia"] * s) / 2
        self.emb = max(d.emboss, MIN_MODEL_MM["emboss"] * s)
        self.inset = max(d.beam_inset, MIN_MODEL_MM["beam_inset"] * s)

        g, r = d.going, d.rise
        self.zL = (d.lower_treads + 1) * r  # mid platform floor
        self.xL0 = d.lower_treads * g  # mid platform starts (top nosing of bottom flight)
        self.xL1 = self.xL0 + d.mid_platform_len  # first riser of the upper flight
        self.n_up = max(0, round((height - self.zL) / r))
        self.r_up = (height - self.zL) / self.n_up if self.n_up else 0.0
        self.H = self.zL + self.n_up * self.r_up  # top platform floor
        self.xP0 = self.xL1 + max(self.n_up - 1, 0) * g  # top platform starts
        self.xP1 = self.xP0 + d.top_platform_len
        self.W2 = d.stair_width / 2
        self.y_min = -self.W2 - self.t  # platform is flush with the right-hand panel
        self.y_max = self.y_min + d.top_platform_width

        pts = [(-g, 0.0), (self.xL0, self.zL)]
        if self.n_up:
            pts.append((self.xL1 - g, self.zL))  # upper pitch line meets the landing
        pts += [(self.xP0, self.H), (self.xP1, self.H)]
        self.walk_x = np.array([p[0] for p in pts])
        self.walk_z = np.array([p[1] for p in pts])

    # walking line: pitch line through the nosings on flights, floor level on platforms
    def walk(self, x):
        return np.interp(x, self.walk_x, self.walk_z)

    def band(self, x0, x1, lo, hi, extra_breaks=()) -> CrossSection:
        """Region between walk+lo(x) and walk+hi(x) for x0<=x<=x1, clipped to z>=0."""
        lo_f = lo if callable(lo) else (lambda x, v=lo: v)
        hi_f = hi if callable(hi) else (lambda x, v=hi: v)
        xs = sorted({x0, x1, *[b for b in (*self.walk_x, *extra_breaks) if x0 < b < x1]})
        bottom = [(x, self.walk(x) + lo_f(x)) for x in xs]
        top = [(x, self.walk(x) + hi_f(x)) for x in reversed(xs)]
        ground = section([(x0 - 1e4, 0), (x1 + 1e4, 0), (x1 + 1e4, 1e6), (x0 - 1e4, 1e6)])
        return section(bottom + top) ^ ground

    def step_profile(self) -> CrossSection:
        d, g, r = self.d, self.d.going, self.d.rise
        pts = [(0.0, 0.0)]
        for i in range(1, d.lower_treads + 1):
            pts += [((i - 1) * g, i * r), (i * g, i * r)]
        pts += [(self.xL0, self.zL), (self.xL1, self.zL)]
        for j in range(1, self.n_up + 1):
            x = self.xL1 + (j - 1) * g
            pts += [(x, self.zL + j * self.r_up)]
            if j < self.n_up:
                pts += [(x + g, self.zL + j * self.r_up)]
        pts += [(self.xP0, self.H - d.soffit)]
        soffit = [(x, z - d.soffit) for x, z in zip(self.walk_x, self.walk_z) if x < self.xP0]
        pts += list(reversed(soffit))
        clip = section([(0, 0), (self.xP0, 0), (self.xP0, 1e6), (0, 1e6)])
        return section(pts) ^ clip

    def stripe_offset_right(self, x):
        d = self.d
        xj = 0.55 * self.xL0
        if x <= xj:
            return d.stripe_low
        if x <= xj + 450:
            return d.stripe_low + (d.stripe_high - d.stripe_low) * (x - xj) / 450
        if x <= self.xP0:
            return d.stripe_high
        if x <= self.xP0 + 450:
            return d.stripe_high + (d.stripe_platform - d.stripe_high) * (x - self.xP0) / 450
        return d.stripe_platform

    def stripe_offset_left(self, x):
        d = self.d
        if x >= self.xP0 - 450:  # jog down before the corner so it meets the rear guard stripe
            base = self.stripe_offset_right(self.xP0 - 450)
            f = min(1.0, (x - (self.xP0 - 450)) / 450)
            return base + (d.stripe_platform - base) * f
        return self.stripe_offset_right(x)

    def post_positions(self, pts):
        out = []
        for a, b in zip(pts[:-1], pts[1:]):
            a, b = np.asarray(a, float), np.asarray(b, float)
            n = max(1, math.ceil(np.linalg.norm(b[:2] - a[:2]) / self.d.post_spacing))
            out += [a + (b - a) * k / n for k in range(n)]
        out.append(np.asarray(pts[-1], float))
        return out

    def build(self) -> dict[str, Manifold]:
        d, g, t, W2 = self.d, self.d.going, self.t, self.W2
        H, xP0, xP1, y_min, y_max = self.H, self.xP0, self.xP1, self.y_min, self.y_max
        top_x_left = xP0 + t
        red, silver, grey, lime = [], [], [], []

        # ---- steps, mid platform and top platform floor
        silver.append(prism_xz(self.step_profile(), -W2, W2))
        silver.append(box(xP0, xP1, -W2, y_max - t, H - d.soffit, H))

        # ---- side panels (red) with the grey beams below them
        right_panel = self.band(-g, xP1, -d.panel_bottom, d.guard_top)
        left_panel = self.band(-g, top_x_left, -d.panel_bottom, d.guard_top)
        red.append(prism_xz(right_panel, y_min, -W2))
        red.append(prism_xz(left_panel, W2, W2 + t))
        red.append(box(xP0, xP1, y_max - t, y_max, H - d.panel_bottom, H + d.guard_top))  # left fascia
        red.append(box(xP0, xP0 + t, W2, y_max, H - d.panel_bottom, H + d.guard_top))  # rear guard

        beam_in = 0.5 * t  # beams reach a little under the steps for strength
        right_beam = prism_xz(self.band(-g, xP1, -d.beam_bottom, -d.panel_bottom), y_min + self.inset, -W2 + beam_in)
        left_beam = prism_xz(self.band(-g, top_x_left, -d.beam_bottom, -d.panel_bottom), W2 - beam_in, W2 + t - self.inset)
        holes = []
        x_a, x_b = self.xL0 + 300, xP0 - 300
        xm = self.xL0 + d.mid_platform_len / 2  # stand column under the mid platform
        col = STAND_MM["column"] * self.scale
        if x_b > x_a:
            n = max(1, round((x_b - x_a) / d.hole_pitch))
            for k in range(n + 1):
                x = x_a + (x_b - x_a) * k / n if n else x_a
                if self.stand and abs(x - xm) < col / 2 + d.hole_dia / 2 + 50:
                    continue
                zc = self.walk(x) - (d.panel_bottom + d.beam_bottom) / 2
                holes.append(rod((x, y_min - 10, zc), (x, W2 + t + 10, zc), d.hole_dia / 2, 24))
        if holes:
            cutter = union(holes)
            right_beam, left_beam = right_beam - cutter, left_beam - cutter
        grey += [right_beam, left_beam]

        # ---- top platform under-frame and bumper
        zb, zs = H - d.beam_bottom, H - d.soffit
        grey.append(box(xP0, xP1, y_max - t, y_max - self.inset, zb, H - d.panel_bottom))  # left edge
        grey.append(box(xP0 + self.inset, xP0 + t, W2, y_max, zb, H - d.panel_bottom))  # rear edge
        grey.append(box(xP1 - t, xP1, y_min, y_max, zb, zs))  # front edge
        self.col_y = [(y_min + y_max) / 2 - 1050, (y_min + y_max) / 2 + 1050]
        self.col_x = xP0 + d.top_platform_len / 2
        for yc in self.col_y:
            grey.append(box(xP0, xP1, yc - 75, yc + 75, zb, zs))
        grey.append(box(self.col_x - 75, self.col_x + 75, y_min, y_max, zb, zs))
        grey.append(box(xP1, xP1 + d.bumper, y_min, y_max, H - 300, H - 30))

        # ---- handrails on posts (silver)
        rr = d.rail_height
        xs_r = [-g + self.post_r + 20, *[x for x in self.walk_x if -g < x < xP1], xP1 - self.post_r - 20]
        right_rail = [(x, y_min + t / 2, self.walk(x) + rr) for x in xs_r]
        yl = W2 + t / 2
        xs_l = [-g + self.post_r + 20, *[x for x in self.walk_x if -g < x <= xP0]]
        left_rail = [(x, yl, self.walk(x) + rr) for x in xs_l]
        left_rail += [
            (xP0 + t / 2, yl, H + rr),
            (xP0 + t / 2, y_max - t / 2, H + rr),
            (xP1 - self.post_r - 20, y_max - t / 2, H + rr),
        ]
        for rail in (right_rail, left_rail):
            silver.append(tube(rail, self.rail_r))
            for p in self.post_positions(rail):
                z_top = p[2]
                z_bot = z_top - (d.rail_height - d.guard_top) - 20
                silver.append(rod((p[0], p[1], z_bot), (p[0], p[1], z_top), self.post_r))

        # ---- livery: lime stripes and the ES1 label (embossed)
        e, sw = self.emb, d.stripe_width / 2
        brk = [0.55 * self.xL0, 0.55 * self.xL0 + 450, xP0 - 450, xP0, xP0 + 450]

        def stripe(fn, x0, x1, panel):
            cs = self.band(x0, x1, lambda x: fn(x) - sw, lambda x: fn(x) + sw, brk)
            return cs ^ panel

        lime.append(prism_xz(stripe(self.stripe_offset_right, -g, xP1, right_panel), y_min - e, y_min))
        lime.append(prism_xz(stripe(self.stripe_offset_left, -g, top_x_left, left_panel), W2 + t, W2 + t + e))
        zc = H + d.stripe_platform
        lime.append(box(xP0, xP1, y_max, y_max + e, zc - sw, zc + sw))
        lime.append(box(xP0 - e, xP0, W2 + t, y_max + e, zc - sw, zc + sw))

        if d.label:
            z0 = H + d.stripe_platform + sw + 150
            right_txt = text_section(d.label, d.label_height)
            wx = right_txt.bounds()[2]
            silver.append(prism_xz(right_txt.translate((xP1 - 250 - wx, z0)), y_min - e, y_min))
            left_txt = text_section(d.label, d.label_height, mirror=True)
            silver.append(prism_xz(left_txt.translate((xP1 - 250, z0)), y_max, y_max + e))

        # ---- optional display stand (so the model stands on its own)
        if self.stand:
            s = self.scale
            brace = STAND_MM["brace"] * s
            base_t, margin = STAND_MM["base_thk"] * s, STAND_MM["base_margin"] * s
            rad = STAND_MM["base_radius"] * s
            strip = STAND_MM["label_strip"] * s if d.label else 0.0
            x0, x1 = -g - margin, xP1 + d.bumper + margin
            y0, y1 = y_min - e - margin - strip, y_max + e + margin
            base = CrossSection.square((x1 - x0 - 2 * rad, y1 - y0 - 2 * rad)).translate((x0 + rad, y0 + rad))
            base = base.offset(rad, JoinType.Round, circular_segments=32)
            grey.append(Manifold.extrude(base, base_t).translate((0, 0, -base_t)))
            if d.label:  # raised name plate along the front edge of the base
                txt = text_section(f"{d.label}  ·  {H / 1000:.1f} m  ·  1:{s:g}", STAND_MM["label_text"] * s)
                tx0, ty0, tx1, ty1 = txt.bounds()
                yc = (y0 + y_min - e) / 2
                txt = txt.translate((x0 + 2 * rad - tx0, yc - (ty0 + ty1) / 2))
                silver.append(Manifold.extrude(txt, STAND_MM["label_relief"] * s))

            def tower(xc, ys, z_top):
                parts = [box(xc - col / 2, xc + col / 2, y - col / 2, y + col / 2, -1, z_top + 1) for y in ys]
                bays = max(1, round(z_top / 2200))
                levels = [z_top * k / bays for k in range(bays + 1)]
                for k in range(bays):
                    za, zb_ = levels[k] + col / 2, levels[k + 1] - col / 2
                    parts.append(rod((xc, ys[0], za), (xc, ys[1], zb_), brace / 2, 8))
                    parts.append(rod((xc, ys[1], za), (xc, ys[0], zb_), brace / 2, 8))
                    if 0 < k:
                        parts.append(box(xc - brace / 2, xc + brace / 2, ys[0], ys[1], levels[k] - brace / 2, levels[k] + brace / 2))
                return parts

            xm = self.xL0 + d.mid_platform_len / 2
            ym = [-(W2 + t / 2), W2 + t / 2]
            z_mid = self.zL - d.beam_bottom
            grey += tower(xm, ym, z_mid)
            grey.append(box(xm - col / 2, xm + col / 2, ym[0], ym[1], z_mid, self.zL - d.soffit))
            grey += tower(self.col_x, self.col_y, zb)

        groups = dict(red=union(red), silver=union(silver), grey=union(grey), lime=union(lime))
        # make the colour bodies disjoint (earlier colours win overlaps)
        taken = Manifold()
        for name in COLOURS:
            groups[name] = drop_slivers(groups[name] - taken)
            taken = taken + groups[name]
        return groups

    def summary(self) -> dict:
        d = self.d
        return dict(
            platform_height_mm=round(self.H, 1),
            mid_platform_height_mm=round(self.zL, 1),
            bottom_flight=dict(treads=d.lower_treads, risers=d.lower_treads + 1, rise_mm=d.rise, going_mm=d.going,
                               pitch_deg=round(math.degrees(math.atan2(d.rise, d.going)), 1)),
            mid_platform_length_mm=d.mid_platform_len,
            upper_flight=dict(treads=max(self.n_up - 1, 0), risers=self.n_up, rise_mm=round(self.r_up, 1),
                              going_mm=d.going,
                              pitch_deg=round(math.degrees(math.atan2(self.r_up, d.going)), 1) if self.n_up else 0),
            top_platform_mm=[d.top_platform_len, d.top_platform_width],
            overall_length_mm=round(self.xP1 + d.bumper + d.going, 1),
        )


def to_trimesh(m: Manifold, scale: float, shift) -> trimesh.Trimesh:
    mesh = m.to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3] / scale - shift
    return trimesh.Trimesh(vertices=v, faces=np.asarray(mesh.tri_verts), process=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scale", type=float, default=100, help="scale denominator, e.g. 100 for 1:100")
    ap.add_argument("--heights", type=float, nargs="+", default=[3200, 5800, 8400], help="top platform heights, mm")
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "stl")
    args = ap.parse_args()

    d = Design()
    tag = f"1-{args.scale:g}"
    report = dict(scale=f"1:{args.scale:g}", design=asdict(d), models={})
    for h in args.heights:
        name = f"ES1_stairs_{h / 1000:.1f}m_{tag}"
        for stand in (True, False):
            model = RescueStairs(d, h, args.scale, stand=stand)
            groups = model.build()
            whole = drop_slivers(union(list(groups.values())))
            lo = np.array(whole.bounding_box()[:3]) / args.scale
            shift = np.array([lo[0], lo[1], lo[2]])
            sub = args.out if stand else args.out / "stair_only"
            sub.mkdir(parents=True, exist_ok=True)
            fname = name if stand else f"{name}_stair_only"
            tm = to_trimesh(whole, args.scale, shift)
            tm.export(sub / f"{fname}.stl")
            parts_dir = args.out / "multicolour" / fname
            parts_dir.mkdir(parents=True, exist_ok=True)
            for colour, body in groups.items():
                if not body.is_empty():
                    to_trimesh(body, args.scale, shift).export(parts_dir / f"{fname}_{colour}.stl")
            info = model.summary()
            info.update(
                model_size_mm=[round(float(x), 1) for x in tm.extents],
                watertight=bool(tm.is_watertight),
                bodies=len(whole.decompose()),
                triangles=int(len(tm.faces)),
            )
            report["models"][fname] = info
            print(f"{fname}: platform {info['platform_height_mm']:.0f} mm, upper risers {model.n_up}, "
                  f"model {info['model_size_mm']} mm, watertight={info['watertight']}, bodies={info['bodies']}")
    (args.out / "models.json").write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
