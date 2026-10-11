#!/usr/bin/env python3
"""Preview images for the printable track: a side view of one 1:5 track segment on the ES1
steps (with a close-up of one nosing), and renders of the printed track next to a stock
HTD 5M pulley.

    python3 preview_track.py        # after generate_track.py; writes preview/*.png
"""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from manifold3d import CrossSection, Manifold, OpType
from matplotlib.patches import Polygon as MPoly, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

import generate_track as gt

HERE = Path(__file__).resolve().parent
INK, MUTED = "#1f2933", "#5b6670"
TRACK_C, PULLEY_C, STAIR_C, STRIP_C, ACCENT = "#2f3b45", "#c9d2da", "#d5d9de", "#9db7d5", "#d9480f"


class Loop:
    """The track's pitch line in the segment's frame: u along the lower run from the rear tangent
    point, w up from the track's face on the stairs. Axles at (0, back) and (C, back)."""

    def __init__(self, g: gt.Geometry):
        self.g = g
        self.R = g.pulley_pitch_r
        self.C = g.centres
        self.wa = g.back
        self.segs = [self.C, math.pi * self.R, self.C, math.pi * self.R]

    def segment(self, s) -> int:
        """0 lower run, 1 front pulley, 2 upper run, 3 rear pulley."""
        s %= self.g.length
        for i, L in enumerate(self.segs):
            if s < L:
                return i
            s -= L
        return 3

    def at(self, s):
        """Pitch-line point, unit tangent and outward normal at path length s."""
        s %= self.g.length
        C, R, wa = self.C, self.R, self.wa
        if s < C:
            return np.array([s, wa - R]), np.array([1.0, 0]), np.array([0, -1.0])
        s -= C
        if s < math.pi * R:
            a = -math.pi / 2 + s / R
            n = np.array([math.cos(a), math.sin(a)])
            return np.array([C, wa]) + R * n, np.array([-math.sin(a), math.cos(a)]), n
        s -= math.pi * R
        if s < C:
            return np.array([C - s, wa + R]), np.array([-1.0, 0]), np.array([0, 1.0])
        s -= C
        a = math.pi / 2 + s / R
        n = np.array([math.cos(a), math.sin(a)])
        return np.array([0, wa]) + R * n, np.array([-math.sin(a), math.cos(a)]), n


def track_shapes(g: gt.Geometry, loop: Loop, s_cleat: float):
    """Backing band, teeth and cleats of the whole loop, in the segment's frame."""
    d = g.d
    cleat = gt.rounded(gt.trapezoid(d.cleat_base, d.cleat_tip, d.cleat_height), d.tip_round).to_polygons()[0]
    tooth = gt.tooth_outline(d)
    shapes, teeth = [], []
    for k in range(g.cleats):
        p, t, n = loop.at(s_cleat + k * g.pitch)
        face = p + n * (d.backing - d.pld)
        shapes.append([face + a * t + h * n for a, h in cleat])
    for j in range(d.belt_teeth):
        s = j * d.belt_pitch
        p, t, n = loop.at(s)
        root = p - n * d.pld
        shapes.append([root + a * t - h * n for a, h in tooth])
        teeth.append((s, p))
    ss = np.linspace(0, g.length, 1400)
    outer = np.array([loop.at(s)[0] + loop.at(s)[2] * (d.backing - d.pld) for s in ss])
    inner = np.array([loop.at(s)[0] - loop.at(s)[2] * d.pld for s in ss])
    return shapes, outer, inner, teeth


def pulley_outline(g: gt.Geometry, centre, groove_at):
    """A stock HTD 5M pulley in section (no flange): the outside circle with a groove under each
    tooth, one centred at angle groove_at."""
    d = g.d
    tooth = Polygon(gt.tooth_outline(d, sink=0)).buffer(0.15)
    grooves = []
    for k in range(d.pulley_teeth):
        a = groove_at + 2 * math.pi * k / d.pulley_teeth
        u = np.array([math.cos(a), math.sin(a)])
        v = np.array([-math.sin(a), math.cos(a)])
        pts = [tuple(np.asarray(centre) + (g.root - h) * u + t * v) for t, h in np.asarray(tooth.exterior.coords)]
        grooves.append(Polygon(pts).buffer(0))
    body = Point(centre).buffer(g.root, 180).difference(unary_union(grooves))
    return np.asarray(body.exterior.coords)


def side_view(g: gt.Geometry, out: Path, title: bool = True):
    """title=False leaves off the heading, for use on a slide that has its own."""
    d = g.d
    a = g.slope
    e = np.array([math.cos(a), math.sin(a)])
    nrm = np.array([-math.sin(a), math.cos(a)])
    loop = Loop(g)
    step = g.step_pitch
    rest = gt.check_seating(g)["rest_phase_mm"]
    s_rear = 30.0  # rear tangent point, along the slope from nosing 0
    first = step + rest - s_rear  # the cleat just above nosing 1 stands on its tread
    s_cleat = first - math.floor(first / g.pitch) * g.pitch

    def W(pts):  # segment frame -> world
        pts = np.asarray(pts, float)
        return (s_rear + pts[:, :1]) * e + pts[:, 1:2] * nrm

    fig = plt.figure(figsize=(13, 6.4), dpi=150)
    ax = fig.add_axes([0.02, 0.05, 0.64, 0.88])
    zx = fig.add_axes([0.69, 0.2, 0.3, 0.62])
    for axis in (ax, zx):
        prof = [(-150, -150)]
        for i in range(-2, 7):
            prof += [(i * d.going, (i - 1) * d.rise), (i * d.going, i * d.rise)]
        prof += [(8 * d.going, 6 * d.rise), (8 * d.going, -150)]
        axis.add_patch(MPoly(prof, closed=True, fc=STAIR_C, ec="#8a939b", lw=0.8, zorder=1))
        shapes, outer, inner, teeth = track_shapes(g, loop, s_cleat)
        top = d.backing + d.tooth_height
        strip = [(19, top + 0.1), (g.centres - 19, top + 0.1), (g.centres - 19, top + 3.1), (19, top + 3.1)]
        axis.add_patch(MPoly(W(strip), closed=True, fc=STRIP_C, ec="#5d7fa8", lw=0.6, zorder=2))
        for cx, seg in ((0.0, 3), (g.centres, 1)):
            c = np.array([cx, g.back])
            on = [p for s, p in teeth if loop.segment(s) == seg]
            ang = math.atan2(*(on[0] - c)[::-1]) if on else math.pi / 2
            axis.add_patch(MPoly(W(pulley_outline(g, c, ang)), closed=True, fc=PULLEY_C, ec="#7d8892", lw=0.6, zorder=2))
            hole = np.array([[math.cos(t), math.sin(t)] for t in np.linspace(0, 2 * math.pi, 60)]) * 4 + c
            axis.add_patch(MPoly(W(hole), closed=True, fc="#6b7680", ec="none", zorder=3))
        band = np.vstack([outer, inner[::-1]])
        axis.add_patch(MPoly(W(band), closed=True, fc=TRACK_C, ec="none", zorder=4))
        for sh in shapes:
            axis.add_patch(MPoly(W(sh), closed=True, fc=TRACK_C, ec="none", zorder=4))
    nos_xy = [(i * d.going, i * d.rise) for i in range(0, 8)]
    ax.set_xlim(-25, 300)
    ax.set_ylim(-15, 230)
    ax.set_aspect("equal")
    ax.axis("off")
    for i in (1, 2, 3, 4):
        ax.plot(*nos_xy[i], "o", ms=4, color=ACCENT, zorder=6)
    p1, p2 = np.array(nos_xy[2]), np.array(nos_xy[3])
    off = -nrm * 18
    ax.annotate("", p1 + off, p2 + off, arrowprops=dict(arrowstyle="<->", color=INK, lw=0.9))
    ax.text(*((p1 + p2) / 2 + off * 1.9), f"{step:.1f} mm edge to edge\n= 5 cleats", ha="center", va="center",
            fontsize=10, color=INK, rotation=math.degrees(a))
    ax.text(*(W([[g.centres / 2, g.back + g.pulley_pitch_r + 10]])[0]),
            f"one track segment at 1:5: {g.centres:.0f} mm axle to axle, {g.length:.0f} mm loop",
            ha="center", fontsize=10, color=INK, rotation=math.degrees(a))
    mid = W([[g.centres * 0.62, d.backing + d.tooth_height + 1.6]])[0]
    ax.annotate("slide strip", mid, mid + np.array([34, -46]), fontsize=9, color="#3d5f86",
                arrowprops=dict(arrowstyle="-", color="#3d5f86", lw=0.7))
    pul = W([[g.centres, g.back]])[0]
    ax.annotate("bought HTD 5M\n20-tooth pulley", pul + np.array([10, 8]), pul + np.array([45, 45]), fontsize=9,
                color=INK, ha="center", arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    if title:
        ax.set_title(f"Printed track on the ES1 steps at 1:5 ({d.rise:.0f} × {d.going:.0f} mm), section through one track",
                     fontsize=11, color=INK, loc="left")
    cx, cy = nos_xy[3]
    zx.set_xlim(cx - 16, cx + 16)
    zx.set_ylim(cy - 13, cy + 15)
    zx.set_aspect("equal")
    zx.set_xticks([])
    zx.set_yticks([])
    for sp in zx.spines.values():
        sp.set_color("#8a939b")
    ax.add_patch(Rectangle((cx - 16, cy - 13), 32, 28, fill=False, ec="#8a939b", lw=0.8, zorder=7))
    zx.plot(cx, cy, "o", ms=5, color=ACCENT, zorder=6)
    zx.annotate("the step edge sits in the gap\nbetween two cleats", (cx, cy), (cx - 15, cy + 11), fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    zx.annotate("the cleat above it\nstands on the step", (cx + 5.2, cy - 0.2), (cx + 3, cy - 11), fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    seat = gt.check_seating(g)
    zx.set_title(f"Close-up: {seat['slack_mm']:.1f} mm of play, so each step can be\n"
                 f"{seat['tolerance_per_step_mm']:.1f} mm out and the track still seats", fontsize=9.5, color=INK, loc="left")
    fig.savefig(out, facecolor="white")
    plt.close(fig)


def pulley_mesh(g: gt.Geometry) -> trimesh.Trimesh:
    """Stand-in for the bought pulley in renders only (not a print file): flanged, with a hub."""
    d = g.d
    grooves = [CrossSection([gt.on_circle(gt.tooth_outline(d, sink=-2.0), g.root, 2 * math.pi * k / d.pulley_teeth, -1)])
               for k in range(d.pulley_teeth)]
    body = Manifold.extrude(gt.circle(g.root) - CrossSection.batch_boolean(grooves, OpType.Add), 17.0).translate((0, 0, 1.5))
    flange = Manifold.cylinder(1.5, g.root + 2.5, g.root + 2.5, 120)
    hub = Manifold.cylinder(7.0, 9.0, 9.0, 120).translate((0, 0, 18.4))
    m = Manifold.batch_boolean([body, flange, flange.translate((0, 0, 18.5)), hub], OpType.Add)
    m = m - Manifold.cylinder(40, 4.0, 4.0, 60).translate((0, 0, -5))
    return gt.to_mesh(m)


def render(ax, mesh: trimesh.Trimesh, color, elev=28, azim=-55, rotate=None):
    """Shaded render of a mesh."""
    mesh = mesh.copy()
    if rotate is not None:
        mesh.apply_transform(rotate)
    v = mesh.vertices - mesh.bounds.mean(axis=0)
    tris = v[mesh.faces]
    light = np.array([0.4, -0.5, 0.75])
    light /= np.linalg.norm(light)
    shade = 0.45 + 0.55 * np.clip(mesh.face_normals @ light, 0, 1)
    base = np.array(matplotlib.colors.to_rgb(color))
    fc = np.clip(base[None, :] * shade[:, None] + 0.12 * (1 - shade[:, None]), 0, 1)
    ax.add_collection3d(Poly3DCollection(tris, facecolors=fc, edgecolors="none", linewidths=0))
    r = np.abs(v).max()
    ax.set_xlim(-r, r)
    ax.set_ylim(-r, r)
    ax.set_zlim(-r, r)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elev, azim=azim)
    ax.axis("off")


def parts_sheet(g: gt.Geometry, stl: Path, out: Path):
    stand = trimesh.transformations.rotation_matrix(math.pi / 2, (1, 0, 0))
    items = [
        (trimesh.load(stl / "track_TPU_x4.stl"), "#3a4650", "Track ×4: print", "TPU 95A, standing up as a ring", 30, None),
        (pulley_mesh(g), "#a9b4bf", "HTD 5M 20-tooth pulley ×8: buy", "for 15 mm belts, 8 mm bore", 24, None),
        (trimesh.load(stl / "step_gauge_3_steps_1-5_PLA.stl"), "#c5cbd1", "Step gauge: print (optional)", "3 ES1 steps at 1:5", 20, stand),
    ]
    fig = plt.figure(figsize=(14, 4.4), dpi=150)
    for i, (mesh, col, label, sub, elev, rot) in enumerate(items):
        ax = fig.add_axes([i / 3, 0.18, 1 / 3, 0.82], projection="3d")
        render(ax, mesh, col, elev=elev, rotate=rot)
        fig.text((i + 0.5) / 3, 0.1, label, ha="center", fontsize=12, weight="bold", color=INK)
        fig.text((i + 0.5) / 3, 0.03, sub, ha="center", fontsize=10, color=MUTED)
    fig.savefig(out, facecolor="white")
    plt.close(fig)


def main():
    g = gt.Geometry(gt.Design())
    prev = HERE / "preview"
    prev.mkdir(exist_ok=True)
    side_view(g, prev / "track_on_ES1_steps_1-5.png")
    parts_sheet(g, HERE / "stl", prev / "parts.png")
    print("wrote", *sorted(p.name for p in prev.iterdir()))


if __name__ == "__main__":
    main()
