#!/usr/bin/env python3
"""Printed frame parts of one track segment of the 1:5 ES1 stair-carrier prototype.

One segment has two side plates and two cross-bar spacers. A side plate is a 265 x 40 x 7 mm
stadium (R20 ends, 12 mm below and 28 mm above the axle line) with a 608ZZ pocket at each axle,
two 4.5 mm cross-bar holes along its top edge and an integral slide rail under the lower run of
the track. The rail is joined to the plate's bottom edge by a web. The front segment's plates sit
inboard of their track lanes (plate z 41-48, rail z 50-68); the rear segment's plates sit
outboard (plate z 105-112, rail z 78-96 under the lane, joined by a web under the pulley hub).
The front plates also carry three M3 holes on a 14 mm radius round the middle-axle pocket for
the hinge sector gear. Left and right plates are mirror images.

Every number comes from assembly/parts_spec.json (mm, 1:5 model size). The few values the spec
gives only in words (the z layout, the web bottom, the sector-hole angles) are derived here and
listed under "derived" in stl/frame.json.

Usage:
    python3 generate_frame.py        # writes stl/side_plate_*.stl, stl/spacer_*.stl,
                                     # stl/frame.json and preview/frame_parts.png

Every STL is oriented as it is printed: plates on their plate face with the rail standing up,
spacers standing on end. Every mesh is checked to be a single watertight body.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import trimesh
from manifold3d import CrossSection, Manifold, OpType

import generate_track as gt

HERE = Path(__file__).resolve().parent
SPEC_PATH = HERE / "assembly" / "parts_spec.json"
CIRCLE_SEG = 180  # facets on the plate ends and pockets
HOLE_SEG = 48  # facets on small holes
PETG_DENSITY = 1.27  # g/cm3


# --------------------------------------------------------------------------- numbers
@dataclass
class Frame:
    """Every size the frame parts need, pulled from parts_spec.json."""

    # plate outline
    centres: float  # axle to axle
    plate_t: float  # plate thickness (across, z)
    plate_h: float  # plate height
    end_r: float  # radius of the stadium ends
    below: float  # bottom edge below the axle line
    above: float  # top edge above the axle line
    # holes
    pocket_d: float  # bearing pocket
    bar_hole_d: float  # cross-bar holes
    bar_hole_x: list  # x of the cross-bar holes from the segment's rear axle
    bar_hole_y: float  # above the axle
    sector_hole_d: float  # hinge sector gear bolts (front plates only)
    sector_r: float  # on this radius round the middle-axle pocket
    sector_angles_deg: tuple
    boss_r: float  # bearing boss round each pocket
    # rail and web
    rail_x0: float
    rail_x1: float
    rail_w: float  # across, z
    rail_t: float  # rail thickness (vertical)
    rail_top: float  # rail top face below the axle line
    web_top: float  # web starts at the plate's bottom edge
    # z layout, one side, from the vehicle centre line (derived from layout_decision)
    box_z: float  # box outer face
    gap: float  # clearance between neighbours in the layout
    lane_w: float  # a track lane
    hub_l: float  # pulley hub length
    # spacers
    spacer_od: float
    spacer_bore: float
    spacer_len_front: float
    spacer_len_rear: float
    # bought parts the plate must clear (for the checks)
    hub_d: float
    flange_d: float
    flange_t: float
    pulley_face_w: float
    bearing_od: float
    bearing_w: float
    cleat_tip: float  # axle to cleat tip
    track_face: float  # axle to track outer face

    @classmethod
    def from_spec(cls, spec: dict) -> "Frame":
        p = spec["parts"]
        sp, rail, pk, cb = p["side_plate"], p["side_plate"]["rail"], p["side_plate"]["bearing_pockets"], p["side_plate"]["cross_bar_holes"]
        pl, pulley, bar, bearing = sp["plate"], p["pulley"], p["cross_bar"], p["bearing"]
        return cls(
            centres=spec["segment"]["axle_to_axle_mm"], plate_t=pl["thickness_mm"], plate_h=pl["height_mm"],
            end_r=20.0, below=pl["bottom_edge_below_axle_mm"], above=pl["top_edge_above_axle_mm"],
            pocket_d=pk["dia_mm"], bar_hole_d=cb["dia_mm"], bar_hole_x=list(cb["at_x_mm"]), bar_hole_y=cb["above_axle_mm"],
            sector_hole_d=sp['sector_bolts']['dia_mm'], sector_r=sp['sector_bolts']['radius_mm'], sector_angles_deg=tuple(sp['sector_bolts']['angles_deg']),
            boss_r=pl['boss_radius_mm'],
            rail_x0=rail["from_x_mm"], rail_x1=rail["to_x_mm"], rail_w=rail["width_mm"], rail_t=rail["thickness_mm"],
            rail_top=rail["top_face_below_axle_mm"], web_top=pl["bottom_edge_below_axle_mm"],
            box_z=40.0, gap=1.0, lane_w=pulley["over_flanges_mm"], hub_l=pulley["hub_length_mm"],
            spacer_od=bar["front_segment"]["spacer_od_mm"], spacer_bore=cb["dia_mm"],
            spacer_len_front=bar["front_segment"]["spacer_length_mm"], spacer_len_rear=bar["rear_segment"]["spacer_length_mm"],
            hub_d=pulley["hub_dia_mm"], flange_d=pulley["flange_dia_mm"], flange_t=pulley["flange_thickness_mm"],
            pulley_face_w=pulley["face_width_between_flanges_mm"], bearing_od=bearing["outside_dia_mm"], bearing_w=bearing["width_mm"],
            cleat_tip=spec["segment"]["axle_to_cleat_tip_mm"], track_face=spec["segment"]["axle_to_track_face_mm"],
        )

    # the plate's own length and the web / rail bottom follow from the above
    @property
    def length(self) -> float:
        return self.centres + 2 * self.end_r

    @property
    def rail_bottom(self) -> float:
        return self.rail_top + self.rail_t  # 17.34; the spec rounds it to 17.3

    @property
    def arc_centre_y(self) -> float:
        return (self.above - self.below) / 2  # the R20 end arcs are centred here, above the axle

    def layout(self) -> dict:
        """z of every band on one side, from the centre line outwards: [start, end]."""
        z = self.box_z
        bands = {}
        for name, w in (("front_plate", self.plate_t), ("front_lane", self.lane_w), ("front_hub", self.hub_l),
                        ("rear_lane", self.lane_w), ("rear_hub", self.hub_l), ("rear_plate", self.plate_t)):
            if name in ("front_plate", "front_lane", "rear_lane", "rear_plate"):
                z += self.gap
            bands[name] = [z, z + w]
            z += w
        return bands


def load_frame(spec_path: Path = SPEC_PATH) -> tuple[Frame, dict]:
    spec = json.loads(spec_path.read_text())
    f = Frame.from_spec(spec)
    lay = f.layout()
    assert 2 * lay["rear_plate"][1] == spec["layout_decision"]["width_over_plates_mm"], lay
    assert 2 * lay["rear_lane"][1] == spec["layout_decision"]["width_over_tracks_mm"], lay
    return f, spec


# --------------------------------------------------------------------------- solids
def plate_outline(f: Frame) -> CrossSection:
    """The stadium in the segment's frame: x from the rear axle, y up from the axle line."""
    bar = CrossSection.square((f.centres, f.plate_h)).translate((0.0, -f.below))
    ends = [CrossSection.circle(f.end_r, CIRCLE_SEG).translate((x, f.arc_centre_y)) for x in (0.0, f.centres)]
    bosses = [CrossSection.circle(f.boss_r, CIRCLE_SEG).translate((x, 0.0)) for x in (0.0, f.centres)]
    return CrossSection.batch_boolean([bar] + ends + bosses, OpType.Add)


def box(x0, x1, y0, y1, z0, z1) -> Manifold:
    return Manifold.cube((x1 - x0, y1 - y0, z1 - z0)).translate((x0, y0, z0))


def hole(x: float, y: float, d: float, z0: float, z1: float, seg: int = HOLE_SEG) -> Manifold:
    return Manifold.cylinder(z1 - z0 + 2.0, d / 2, d / 2, seg).translate((x, y, z0 - 1.0))


def side_plate(f: Frame, segment: str, side: str) -> Manifold:
    """One side plate in the vehicle's frame (x from the segment's rear axle, y up, z across).
    segment: 'front' or 'rear'; side: 'L' (built at +z) or 'R' (its mirror)."""
    lay = f.layout()
    pz0, pz1 = lay[f"{segment}_plate"]
    lz0, lz1 = lay[f"{segment}_lane"]
    lc = (lz0 + lz1) / 2  # the rail is centred under its lane
    rail_z = (lc - f.rail_w / 2, lc + f.rail_w / 2)
    if segment == "front":  # rail outboard of the plate, the web spans the gap
        web_z = (pz0, rail_z[0])
    else:  # rail inboard under the outer lane, the web bridges under the pulley hub
        web_z = (rail_z[1], pz1)
    plate = Manifold.extrude(plate_outline(f), f.plate_t).translate((0, 0, pz0))
    web = box(f.rail_x0, f.rail_x1, -f.rail_bottom, -f.web_top, *web_z)
    rail = box(f.rail_x0, f.rail_x1, -f.rail_bottom, -f.rail_top, *rail_z)
    zlo, zhi = min(pz0, rail_z[0], web_z[0]), max(pz1, rail_z[1], web_z[1])
    holes = [hole(x, 0.0, f.pocket_d, pz0, pz1, CIRCLE_SEG) for x in (0.0, f.centres)]
    holes += [hole(x, f.bar_hole_y, f.bar_hole_d, pz0, pz1) for x in f.bar_hole_x]
    if segment == "front":  # the hinge sector gear bolts round the middle axle, the front segment's rear end
        for a in f.sector_angles_deg:
            holes.append(hole(f.sector_r * math.cos(math.radians(a)), f.sector_r * math.sin(math.radians(a)), f.sector_hole_d, zlo, zhi))
    m = Manifold.batch_boolean([plate, web, rail], OpType.Add) - Manifold.batch_boolean(holes, OpType.Add)
    return m.mirror((0, 0, 1)) if side == "R" else m


def spacer(f: Frame, length: float) -> Manifold:
    tube = Manifold.cylinder(length, f.spacer_od / 2, f.spacer_od / 2, CIRCLE_SEG)
    return tube - Manifold.cylinder(length + 2, f.spacer_bore / 2, f.spacer_bore / 2, HOLE_SEG).translate((0, 0, -1))


def as_printed(m: Manifold, face_z: float) -> Manifold:
    """Lay a plate on its plate face: the face plane z = face_z goes on the bed (print Z = 0) and
    the rest of the part stands above it. Then put the bounding box corner at the origin."""
    lo, hi = np.asarray(m.bounding_box()).reshape(2, 3)
    if abs(lo[2] - face_z) < 1e-6:
        m = m.translate((0, 0, -face_z))
    else:  # the body is below the face: turn it over (about y, so "up" stays up in the preview)
        m = m.rotate((0, 180, 0)).translate((0, 0, face_z))
    lo, _ = np.asarray(m.bounding_box()).reshape(2, 3)
    return m.translate((-lo[0], -lo[1], -lo[2]))


def build_parts(f: Frame) -> dict:
    """name -> (manifold as printed, details)."""
    lay = f.layout()
    parts = {}
    for segment in ("front", "rear"):
        for side in ("L", "R"):
            m = side_plate(f, segment, side)
            face = lay[f"{segment}_plate"][0 if segment == "front" else 1] * (1 if side == "L" else -1)
            parts[f"side_plate_{segment}_{side}"] = (as_printed(m, face), {
                "qty": 1, "material": "PETG", "make_or_buy": "make",
                "process": "3D print, plate face down, rail standing up, 0.2 mm layers, 4 walls, 30% infill, no supports",
                "print_orientation": "plate face on the bed (its %s face, z = %g), rail standing up" % ("inboard" if segment == "front" else "outboard", abs(face)),
            })
    for segment, length in (("front", f.spacer_len_front), ("rear", f.spacer_len_rear)):
        parts[f"spacer_{segment}_x2"] = (spacer(f, length), {
            "qty": 2, "material": "PETG", "make_or_buy": "make",
            "process": "3D print, standing on end, 0.2 mm layers, 3 walls, no supports",
            "print_orientation": "standing, axis vertical",
        })
    return parts


# --------------------------------------------------------------------------- checks
def checks(f: Frame, g: gt.Geometry) -> dict:
    """Walls and clearances the spec implies but does not state. Negative = interference."""
    lay = f.layout()
    hub_r, flange_r, pocket_r = f.hub_d / 2, f.flange_d / 2, f.pocket_d / 2
    tooth_tips = g.root - g.d.tooth_height  # the lower run's tooth tips, below the axle
    # the pulley flange reaches below the rail top; how far along x does it reach at that height?
    flange_x_at_rail_top = math.sqrt(max(flange_r ** 2 - f.rail_top ** 2, 0.0))
    spacer_bottom = f.bar_hole_y - f.spacer_od / 2
    rod_bottom = f.bar_hole_y - f.bar_hole_d / 2
    pulley_over_flanges = f.pulley_face_w + 2 * f.flange_t
    return {
        "rail_top_vs_lower_run_tooth_tips_mm": round(tooth_tips - f.rail_top, 3),
        "pocket_wall_mm": round(f.boss_r - pocket_r, 2),
        "pocket_wall_to_plate_end_mm": round(math.sqrt(f.end_r ** 2 - f.arc_centre_y ** 2) - pocket_r, 2),
        "sector_hole_wall_to_pocket_mm": round(f.sector_r - f.sector_hole_d / 2 - pocket_r, 2),
        "sector_hole_wall_to_plate_edge_mm": round(min(
            f.end_r - (math.hypot(f.sector_r * math.cos(math.radians(a)), f.sector_r * math.sin(math.radians(a)) - f.arc_centre_y) + f.sector_hole_d / 2)
            if f.sector_r * math.cos(math.radians(a)) < 0 else f.below + f.sector_r * math.sin(math.radians(a)) - f.sector_hole_d / 2
            for a in f.sector_angles_deg), 2),
        "bar_hole_wall_to_plate_top_mm": round(f.above - f.bar_hole_y - f.bar_hole_d / 2, 2),
        "rear_web_top_below_pulley_hub_mm": round(f.web_top - hub_r, 2),
        "rear_web_start_past_pulley_hub_in_x_mm": round(f.rail_x0 - hub_r, 2),
        "rail_end_to_pulley_flange_at_rail_top_mm": round(f.rail_x0 - flange_x_at_rail_top, 2),
        "rear_web_z_vs_rear_hub_z": {"web": [lay["rear_lane"][1], lay["rear_plate"][1]], "hub": lay["rear_hub"]},
        "rear_spacer_bottom_vs_upper_run_cleat_tips_mm": round(spacer_bottom - f.cleat_tip, 2),
        "rear_rod_bottom_vs_upper_run_cleat_tips_mm": round(rod_bottom - f.cleat_tip, 2),
        "front_spacer_runs_inside_box_width": lay["front_plate"][0] - f.gap <= f.box_z,
        "lane_width_vs_pulley_over_flanges_mm": round(f.lane_w - pulley_over_flanges, 2),
        "sector_gear_room_inboard_mm": round(lay["front_plate"][0] - f.box_z, 2),
        "sector_gear_room_outboard_mm": round(lay["front_lane"][0] - lay["front_plate"][1], 2),
        "plate_length_mm": f.length,
        "diagonal_footprint_on_square_bed_mm": round((f.length + f.rail_bottom + f.above) / math.sqrt(2), 1),
    }


def spec_problems(c: dict) -> list:
    """Anything the spec still gets wrong. Empty when the layout is clean."""
    out = []
    if c["pocket_wall_mm"] < 2.0:
        out.append(f"Bearing pocket wall is {c['pocket_wall_mm']} mm: a press fit will split it; enlarge the boss.")
    if c["sector_hole_wall_to_pocket_mm"] < 2.0:
        out.append(f"Hinge sector holes leave {c['sector_hole_wall_to_pocket_mm']} mm to the pocket; move them out.")
    if c["sector_hole_wall_to_plate_edge_mm"] < 2.0:
        out.append(f"Hinge sector holes leave {c['sector_hole_wall_to_plate_edge_mm']} mm to the plate edge.")
    if c["rear_spacer_bottom_vs_upper_run_cleat_tips_mm"] < 1.0:
        out.append(f"Rear cross-bar spacer clears the upper run's cleat tips by only {c['rear_spacer_bottom_vs_upper_run_cleat_tips_mm']} mm.")
    if c["lane_width_vs_pulley_over_flanges_mm"] < 0:
        out.append(f"Track lane is {-c['lane_width_vs_pulley_over_flanges_mm']} mm narrower than the pulley over its flanges.")
    if c["bar_hole_wall_to_plate_top_mm"] < 2.0:
        out.append(f"Cross-bar holes leave {c['bar_hole_wall_to_plate_top_mm']} mm to the plate's top edge.")
    if c["sector_gear_room_inboard_mm"] < 3 and c["sector_gear_room_outboard_mm"] < 3:
        out.append("No 3 mm face free for the hinge sector gear on the front plate at the middle axle: the box must stop at z 37 there.")
    return out


# --------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=HERE / "stl")
    ap.add_argument("--no-preview", action="store_true")
    args = ap.parse_args()
    f, spec = load_frame()
    g = gt.Geometry(gt.Design())
    args.out.mkdir(parents=True, exist_ok=True)

    lay = f.layout()
    report = {
        "_about": "Printed frame parts of one track segment, from assembly/parts_spec.json. mm at 1:5. Masses are for solid PETG; "
                  "printed at 4 walls and 30% infill a plate comes out at roughly two thirds of that.",
        "source": str(SPEC_PATH.relative_to(HERE)),
        "derived": {
            "plate_length_mm": f.length,
            "stadium_arc_centres_above_axle_mm": f.arc_centre_y,
            "web_bottom_below_axle_mm": f.rail_bottom,
            "z_layout_one_side_mm": lay,
            "front_plate": {"plate_z": lay["front_plate"], "web_z": [lay["front_plate"][0], lay["front_lane"][0]], "rail_z": lay["front_lane"]},
            "rear_plate": {"plate_z": lay["rear_plate"], "web_z": [lay["rear_lane"][1], lay["rear_plate"][1]], "rail_z": lay["rear_lane"]},
            "sector_holes": {"dia_mm": f.sector_hole_d, "radius_mm": f.sector_r, "angles_deg_from_x": list(f.sector_angles_deg),
                             "note": "angles are not in the spec; one up and one each side on the axle line. 120 degree spacing would break the plate edge."},
            "rear_plate_box_bar_holes": "same holes as the cross bars, x = 60 and 200 from the rear axle, 22 above",
            "rail_top_from_track": round(g.root - g.d.tooth_height, 3),
        },
        "parts": {},
    }
    for name, (m, info) in build_parts(f).items():
        mesh = gt.to_mesh(m)
        bodies = len(m.decompose())
        ok = mesh.is_watertight and bodies == 1
        assert ok, f"{name}: watertight={mesh.is_watertight}, bodies={bodies}"
        mesh.export(args.out / f"{name}.stl")
        ext = mesh.bounds[1] - mesh.bounds[0]
        vol = m.volume() / 1000
        report["parts"][name] = {"file": f"stl/{name}.stl", **info, "size_mm": [round(float(v), 2) for v in ext],
                                 "volume_cm3": round(float(vol), 2), "mass_g_solid": round(float(vol) * PETG_DENSITY, 1),
                                 "watertight": mesh.is_watertight, "bodies": bodies}
    report["checks"] = checks(f, g)
    report["spec_problems"] = spec_problems(report["checks"])
    (args.out / "frame.json").write_text(json.dumps(report, indent=2))
    for k, v in report["parts"].items():
        print(f"{k:24s} {v['size_mm']} mm  {v['volume_cm3']} cm3  {v['mass_g_solid']} g")
    print(json.dumps(report["checks"], indent=2))
    for p in report["spec_problems"]:
        print("-", p)
    if not args.no_preview:
        prev = HERE / "preview"
        prev.mkdir(exist_ok=True)
        preview(f, g, report, args.out, prev / "frame_parts.png")
        print("wrote", prev / "frame_parts.png")


# --------------------------------------------------------------------------- preview
def render_flat(ax, mesh: trimesh.Trimesh, color, elev: float = 42, azim: float = 100):
    """Shaded orthographic render into a plain 2D axes. The light and shading are the ones in
    preview_track.render; that function draws into an Axes3D, which matplotlib always squeezes
    into a square, so a 265 mm plate would come out tiny. Here the triangles are projected by hand
    and painted far to near."""
    import matplotlib
    from matplotlib.collections import PolyCollection

    e, a = math.radians(elev), math.radians(azim)
    d = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])  # towards the viewer
    r = np.array([-math.sin(a), math.cos(a), 0.0])  # screen right
    u = np.cross(d, r)  # screen up
    v = mesh.vertices - mesh.bounds.mean(axis=0)
    tris = v[mesh.faces]
    light = np.array([0.4, -0.5, 0.75])
    light /= np.linalg.norm(light)
    shade = 0.45 + 0.55 * np.clip(mesh.face_normals @ light, 0, 1)
    base = np.array(matplotlib.colors.to_rgb(color))
    fc = np.clip(base[None, :] * shade[:, None] + 0.12 * (1 - shade[:, None]), 0, 1)
    order = np.argsort((tris @ d).mean(axis=1))
    p2 = np.stack([tris @ r, tris @ u], axis=-1)[order]
    ax.add_collection(PolyCollection(p2, facecolors=fc[order], edgecolors=fc[order], linewidths=0.15))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(p2[..., 0].min() - 4, p2[..., 0].max() + 4)
    ax.set_ylim(p2[..., 1].min() - 4, p2[..., 1].max() + 4)


def preview(f: Frame, g: gt.Geometry, report: dict, stl: Path, out: Path):
    """One sheet: the four plates and the spacers as printed (shaded renders), and two sections
    that show how the plates sit against the box, the axle, the pulleys and the tracks."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    INK, MUTED, RED = "#1f2933", "#5b6670", "#c92a2a"
    C = {"petg": "#6f9bd1", "petg_dark": "#4f7fb5", "bearing": "#b8bfc6", "steel": "#8d959c", "pulley": "#c9d2da",
         "track": "#3a4650", "cleat": "#6b7a86", "box": "#eef1f4", "spacer": "#a7c4e4"}
    lay = f.layout()
    hub_r, flange_r = f.hub_d / 2, f.flange_d / 2
    fig = plt.figure(figsize=(16, 11.5), dpi=150)
    fig.text(0.03, 0.975, "Frame parts of one track segment, 1:5, as printed", fontsize=15, weight="bold", color=INK, va="top")
    fig.text(0.03, 0.950, "PETG. Left and right are mirror images. Masses are solid PETG at 1.27 g/cm3; printed at 4 walls / 30% infill expect "
             "about two thirds. All sizes in mm.\nIn the sections, z runs across from the vehicle centre line and y up from the axle line; "
             "the box, pulleys, bearings, axle and track are shown for position only.", fontsize=10, color=MUTED, va="top", linespacing=1.4)

    def panel(rect, mesh, color, title, sub, elev=42, azim=100):
        ax = fig.add_axes(rect)
        render_flat(ax, mesh, color, elev=elev, azim=azim)
        fig.text(rect[0] + rect[2] / 2, rect[1] - 0.008, title, ha="center", va="top", fontsize=11.5, weight="bold", color=INK)
        fig.text(rect[0] + rect[2] / 2, rect[1] - 0.030, sub, ha="center", va="top", fontsize=9.5, color=MUTED)

    def size_text(name):
        p = report["parts"][name]
        s = p["size_mm"]
        return f"{s[0]:.0f} x {s[1]:.0f} x {s[2]:.0f} mm, {p['mass_g_solid']:.0f} g solid"

    plates = [("side_plate_front_L", "Front plate, left", "rail outboard (z 50 to 68); 3 x M3 hinge holes on R17 round the middle-axle pocket"),
              ("side_plate_front_R", "Front plate, right", "mirror of the left"),
              ("side_plate_rear_L", "Rear plate, left", "rail inboard under the lane (z 78 to 96), 9 mm web under the pulley hub"),
              ("side_plate_rear_R", "Rear plate, right", "mirror of the left")]
    for i, (name, title, sub) in enumerate(plates):
        col, row = i % 2, i // 2
        rect = [0.02 + col * 0.49, 0.725 - row * 0.215, 0.47, 0.18]
        panel(rect, trimesh.load(stl / f"{name}.stl"), C["petg"], f"{title}: {name}.stl", f"{size_text(name)}. {sub}")

    sp_f, sp_r = trimesh.load(stl / "spacer_front_x2.stl"), trimesh.load(stl / "spacer_rear_x2.stl")
    sp_f.apply_translation((-22, 0, 0))
    panel([0.02, 0.10, 0.13, 0.30], trimesh.util.concatenate([sp_f, sp_r]), C["spacer"], "Spacers",
          f"front {f.spacer_len_front:g} long (x2), rear {f.spacer_len_rear:g} long (x2)\nOD {f.spacer_od:g}, bore {f.spacer_bore:g}, printed standing", elev=18, azim=100)

    def section_axes(rect, title, xmax):
        ax = fig.add_axes(rect)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-6, xmax)
        ax.set_ylim(-44, 52)
        ax.set_title(title, fontsize=9.5, color=INK, loc="left")
        ax.add_patch(Rectangle((0, -28), f.box_z, 60, fc=C["box"], ec="#8a939b", lw=0.6, ls="--"))  # the box
        ax.plot([0, 0], [-32, 50], color="#8a939b", lw=0.6, dashes=(6, 2, 1, 2))  # vehicle centre line
        ax.plot([-4, xmax - 2], [0, 0], color="#8a939b", lw=0.5, dashes=(6, 2, 1, 2))  # axle line

        def R(z0, z1, y0, y1, fc, ec=INK, lw=0.6, **kw):
            ax.add_patch(Rectangle((z0, y0), z1 - z0, y1 - y0, fc=fc, ec=ec, lw=lw, **kw))

        def lab(xy, xytext, text, color=INK, ha="center"):
            ax.annotate(text, xy=xy, xytext=xytext, fontsize=8.5, color=color, ha=ha, va="center",
                        arrowprops=dict(arrowstyle="-", lw=0.6, color=MUTED if color == INK else color, shrinkA=0, shrinkB=0))

        return ax, R, lab

    def track_section(R, z0, z1):
        """Teeth, backing and cleats of the track across one lane, upper and lower run."""
        for s in (+1, -1):
            R(z0, z1, s * (g.root - g.d.tooth_height), s * f.track_face, C["track"], lw=0.4)
            R(z0, z1, s * f.track_face, s * f.cleat_tip, C["cleat"], lw=0.4)

    # ---- section A: at the middle axle, left half, looking forward
    ax, R, lab = section_axes([0.17, 0.05, 0.41, 0.37], "A: section at the middle axle (the hinge), left half, looking forward", 136)
    R(0, 115, -4, 4, C["steel"])  # the middle axle, 230 long
    for seg in ("front", "rear"):
        pz0, pz1 = lay[f"{seg}_plate"]
        lz0, lz1 = lay[f"{seg}_lane"]
        hz0, hz1 = lay[f"{seg}_hub"]
        R(pz0, pz1, -f.below, f.above, C["petg"])
        R(pz0, pz1, -f.bearing_od / 2, f.bearing_od / 2, C["bearing"])  # 608ZZ, flush in the 7 mm plate
        R(pz0, pz1, -4, 4, C["steel"], lw=0)
        if seg == "front":
            R(pz0, pz1, f.sector_r - f.sector_hole_d / 2, f.sector_r + f.sector_hole_d / 2, "white")  # the top M3 hole
        R(lz0, lz1, -flange_r, flange_r, C["pulley"])  # pulley over its flanges
        R(lz0 + f.flange_t, lz1 - f.flange_t, -g.root, g.root, C["pulley"], lw=0)  # toothed body
        track_section(R, lz0 + f.flange_t, lz1 - f.flange_t)
        R(hz0, hz1, -hub_r, hub_r, C["pulley"])  # hub, set-screwed to the axle
        R(hz0, hz1, -4, 4, C["steel"], lw=0)
    ax.text(18, 46, "box, to z = 40:\nthe drive motor turns\nthis axle by a sprocket\ninside the box", ha="center", va="center", fontsize=8.5, color=INK)
    lab((44.5, f.above), (60, 46), f"front plate {lay['front_plate'][0]:g}-{lay['front_plate'][1]:g}, its rear end:\n608ZZ + 3 x M3 on R{f.sector_r:g}\nfor the hinge sector gear")
    lab((58, f.cleat_tip), (64, 35.5), f"front lane {lay['front_lane'][0]:g}-{lay['front_lane'][1]:g},\nhub {lay['front_hub'][0]:g}-{lay['front_hub'][1]:g}")
    lab((84, f.cleat_tip), (97, 46), f"rear lane {lay['rear_lane'][0]:g}-{lay['rear_lane'][1]:g},\nhub {lay['rear_hub'][0]:g}-{lay['rear_hub'][1]:g}")
    lab((104.5, f.above), (112, 35.5), f"rear plate {lay['rear_plate'][0]:g}-{lay['rear_plate'][1]:g},\nits front end")
    lab((108, -4), (96, -23), "middle axle, 8 mm steel, 230 long: the hinge axis")
    lab((58, -f.cleat_tip), (40, -30), "track: teeth inside, cleats outside")
    ax.text(0, -39, "Every pulley is set-screwed to the axle and the axle turns in the 608ZZ.\nThe front segment pivots about this axle; the box and the rear segment do not.",
            fontsize=8, color=MUTED, ha="left", va="center")

    # ---- section B: through the rails at x = 100 of the rear segment, left half
    bx, RB, labB = section_axes([0.60, 0.05, 0.39, 0.37], "B: section through the rails at x = 100, rear segment, left half", 128)
    pz0, pz1 = lay["rear_plate"]
    lz0, lz1 = lay["rear_lane"]
    RB(pz0, pz1, -f.rail_bottom, f.above, C["petg"])  # plate, with the web's in-plane part
    RB(lz1, pz0, -f.rail_bottom, -f.web_top, C["petg"])  # web bridging under the hub
    RB(lz0, lz1, -f.rail_bottom, -f.rail_top, C["petg_dark"])  # rail
    tz0, tz1 = lz0 + f.flange_t, lz1 - f.flange_t
    track_section(RB, tz0, tz1)
    sb = f.bar_hole_y - f.spacer_od / 2
    RB(0, pz0, sb, f.bar_hole_y + f.spacer_od / 2, C["spacer"])  # spacer between the plates
    RB(0, pz1 + 6, f.bar_hole_y - 2, f.bar_hole_y + 2, C["steel"], lw=0.4)  # M4 rod
    RB(pz1, pz1 + 3.2, f.bar_hole_y - 3.5, f.bar_hole_y + 3.5, C["steel"])  # nut
    RB(tz0, tz1, sb, f.cleat_tip, "none", ec=RED, lw=0.8, hatch="////")  # where the spacer meets the cleats
    bx.text(20, -9, "box: the rear\nsegment is fixed to it", ha="center", va="center", fontsize=8.5, color=INK)
    labB((40, f.bar_hole_y + 5), (40, 45), f"cross bar: M4 rod + 10 mm spacer, {f.spacer_len_rear:g}\nlong, holds the two plates apart; it runs\nthrough the box, so it ties the segment to it")
    labB((108.5, f.above), (100, 45), f"rear plate {lay['rear_plate'][0]:g}-{lay['rear_plate'][1]:g}")
    labB((tz1, 18.4), (84, 34.5), f"upper run, cleat tips {f.cleat_tip:g} up: the spacer\n(bottom at {sb:g}) clears them by {sb - f.cleat_tip:.1f} mm")
    labB((lz0, -f.rail_top - 2), (46, -24), "rail 78-96, 4 thick, top 13.34 below the axle:\nthe lower run's tooth tips ride on it")
    labB((97, -f.rail_bottom), (100, -30), "web 96-112 under the pulley hub\n(hub bottom at 9, web top at 12)")
    bx.text(0, -39, "Front segment, same section: plate 41-48, web 41-50, rail 50-68 under the front lane;\nits 82 mm spacer runs between the plates, inside the box width.",
            fontsize=8, color=MUTED, ha="left", va="center")
    fig.savefig(out, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
