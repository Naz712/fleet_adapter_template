#!/usr/bin/env python3
"""Preview images for the printable track: a side view of one 1:5 track unit on the ES1
steps (with a close-up of one nosing), and renders of the printed parts.

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
from matplotlib.patches import Circle, Polygon as MPoly, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import generate_track as gt

HERE = Path(__file__).resolve().parent
INK, MUTED = "#1f2933", "#5b6670"
TRACK_C, SPROCKET_C, STAIR_C, STRIP_C, ACCENT = "#2f3b45", "#c9d2da", "#d5d9de", "#9db7d5", "#d9480f"


def rot(pts, ang, origin=(0.0, 0.0)):
    c, s = math.cos(ang), math.sin(ang)
    pts = np.asarray(pts, float)
    return pts @ np.array([[c, s], [-s, c]]) + np.asarray(origin)


class Loop:
    """The track's pitch path in the unit's frame: u along the lower run from the rear tangent
    point, w up from the track's face on the stairs. Axles at (0, back) and (C, back)."""

    def __init__(self, g: gt.Geometry):
        self.g = g
        self.R = g.pitch_radius
        self.C = g.centres
        self.wa = g.back  # axle height above the face
        arc = math.pi * self.R
        self.segs = [self.C, arc, self.C, arc]
        self.total = sum(self.segs)
        self.k = g.length / self.total  # stretch the circular wrap to the true loop length

    def segment(self, s) -> int:
        """0 lower run, 1 front sprocket, 2 upper run, 3 rear sprocket."""
        s = (s / self.k) % self.total
        for i, L in enumerate(self.segs):
            if s < L:
                return i
            s -= L
        return 3

    def at(self, s):
        """Point, unit tangent and outward normal at path length s (true loop length)."""
        s = (s / self.k) % self.total
        C, R, wa = self.C, self.R, self.wa
        if s < C:  # lower run, forward
            return np.array([s, wa - R]), np.array([1.0, 0]), np.array([0, -1.0])
        s -= C
        if s < math.pi * R:  # around the front axle, upward
            a = -math.pi / 2 + s / R
            n = np.array([math.cos(a), math.sin(a)])
            return np.array([C, wa]) + R * n, np.array([-math.sin(a), math.cos(a)]), n
        s -= math.pi * R
        if s < C:  # upper run, backward
            return np.array([C - s, wa + R]), np.array([-1.0, 0]), np.array([0, 1.0])
        s -= C
        a = math.pi / 2 + s / R
        n = np.array([math.cos(a), math.sin(a)])
        return np.array([0, wa]) + R * n, np.array([-math.sin(a), math.cos(a)]), n


def track_shapes(g: gt.Geometry, loop: Loop, s0: float):
    d = g.d
    cleat = gt.rounded(gt.trapezoid(d.cleat_base, d.cleat_tip, d.cleat_height), d.tip_round).to_polygons()[0]
    lug = gt.rounded(gt.trapezoid(d.lug_base, d.lug_tip, d.lug_height), d.tip_round).to_polygons()[0]
    shapes, lugs = [], []
    for k in range(d.cleats):
        s = s0 + k * g.pitch
        p, t, n = loop.at(s)
        face_out = p + n * d.backing / 2
        face_in = p - n * d.backing / 2
        shapes.append([face_out + a * t + h * n for a, h in cleat])
        shapes.append([face_in + a * t - h * n for a, h in lug])
        lugs.append((s, p))
    # backing: offset of the pitch path
    ss = np.linspace(0, g.length, 1200)
    outer = np.array([loop.at(s)[0] + loop.at(s)[2] * d.backing / 2 for s in ss])
    inner = np.array([loop.at(s)[0] - loop.at(s)[2] * d.backing / 2 for s in ss])
    return shapes, outer, inner, lugs


def sprocket_poly(g: gt.Geometry, centre, groove_at):
    """Sprocket section (no flange) with a groove centred at angle groove_at."""
    prof = gt.sprocket_profile(g).to_polygons()
    return [rot(p, groove_at - math.pi / 2, centre) for p in prof]


def side_view(g: gt.Geometry, out: Path, title: bool = True):
    """title=False leaves off the heading, for use on a slide that has its own."""
    d = g.d
    a = g.slope
    e = np.array([math.cos(a), math.sin(a)])
    nrm = np.array([-math.sin(a), math.cos(a)])
    loop = Loop(g)
    step = g.step_pitch
    rest = gt.check_seating(g)["rest_phase_mm"]
    s_rear = 50.0  # rear tangent point, along the slope from nosing 0
    nos_s = [i * step for i in range(-1, 6)]
    # cleats: the one just above each nosing stands on that step's tread
    first = nos_s[2] + rest - s_rear
    s0 = first - math.floor(first / g.pitch) * g.pitch

    def W(pts):  # unit frame -> world
        pts = np.asarray(pts, float)
        return (s_rear + pts[:, :1]) * e + pts[:, 1:2] * nrm

    fig = plt.figure(figsize=(12, 6.6), dpi=150)
    ax = fig.add_axes([0.03, 0.06, 0.6, 0.86])
    zx = fig.add_axes([0.66, 0.2, 0.32, 0.66])
    for axis, lim in ((ax, None), (zx, None)):
        # stairs
        prof = [(-150, -150)]
        for i in range(-2, 7):
            prof += [(i * d.going, (i - 1) * d.rise), (i * d.going, i * d.rise)]
        prof += [(7 * d.going, 6 * d.rise), (7 * d.going, -150)]
        axis.add_patch(MPoly(prof, closed=True, fc=STAIR_C, ec="#8a939b", lw=0.8, zorder=1))
        shapes, outer, inner, lugs = track_shapes(g, loop, s0)
        # slide strip under the lower run
        top_lug = d.backing + d.lug_height
        strip = [(19, top_lug + 0.1), (g.centres - 19, top_lug + 0.1), (g.centres - 19, top_lug + 3.1), (19, top_lug + 3.1)]
        axis.add_patch(MPoly(W(strip), closed=True, fc=STRIP_C, ec="#5d7fa8", lw=0.6, zorder=2))
        # sprockets, grooves turned to the lugs on them
        for cx, seg in ((0.0, 3), (g.centres, 1)):
            c = np.array([cx, g.back])
            on = [p for sk, p in lugs if loop.segment(sk) == seg]
            ang = math.atan2(*(on[0] - c)[::-1]) if on else math.pi / 2
            for poly in sprocket_poly(g, (0, 0), ang):
                axis.add_patch(MPoly(W(poly + c), closed=True, fc=SPROCKET_C, ec="#7d8892", lw=0.6, zorder=2))
            hole = np.array([[math.cos(t), math.sin(t)] for t in np.linspace(0, 2 * math.pi, 60)]) * d.bore / 2 + c
            axis.add_patch(MPoly(W(hole), closed=True, fc="#6b7680", ec="none", zorder=3))
        band = np.vstack([outer, inner[::-1]])
        axis.add_patch(MPoly(W(band), closed=True, fc=TRACK_C, ec="none", zorder=4))
        for sh in shapes:
            axis.add_patch(MPoly(W(sh), closed=True, fc=TRACK_C, ec="none", zorder=4))
    # whole unit
    nos_xy = [(i * d.going, i * d.rise) for i in range(-1, 6)]
    ax.set_xlim(-20, 230)
    ax.set_ylim(-10, 175)
    ax.set_aspect("equal")
    ax.axis("off")
    for i in (1, 2, 3):
        ax.plot(*nos_xy[i + 1], "o", ms=4, color=ACCENT, zorder=6)
    p1, p2 = np.array(nos_xy[2]), np.array(nos_xy[3])
    off = -nrm * 16
    ax.annotate("", p1 + off, p2 + off, arrowprops=dict(arrowstyle="<->", color=INK, lw=0.9))
    ax.text(*((p1 + p2) / 2 + off * 1.9), f"{step:.1f} mm nosing to nosing\n= exactly {d.cleats_per_step} cleats",
            ha="center", va="center", fontsize=9, color=INK, rotation=math.degrees(a))
    ax.text(*(W([[g.centres / 2, g.back + g.pitch_radius + 9]])[0]),
            f"one track unit at 1:5: {g.centres:.1f} mm axle to axle", ha="center", fontsize=9, color=INK,
            rotation=math.degrees(a))
    mid = W([[g.centres / 2, d.backing + d.lug_height + 1.6]])[0]
    ax.annotate("slide strip", mid, mid + np.array([28, -40]), fontsize=8.5, color="#3d5f86",
                arrowprops=dict(arrowstyle="-", color="#3d5f86", lw=0.7))
    if title:
        ax.set_title(f"Printed track on the ES1 steps at 1:5 ({d.rise:.0f} × {d.going:.0f} mm), section through one track",
                     fontsize=11, color=INK, loc="left")
    # close-up of the middle nosing
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
    zx.annotate("nosing sits in the gap\nbetween two cleats", (cx, cy), (cx - 15, cy + 11), fontsize=8.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    zx.annotate("the cleat above it\nstands on the tread", (cx + 5.2, cy - 0.2), (cx + 3, cy - 11), fontsize=8.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    seat = gt.check_seating(g)
    zx.set_title(f"Close-up: {seat['slack_mm']:.1f} mm of play, so the steps can be\n"
                 f"{seat['tolerance_per_step_mm']:.1f} mm out per step and still seat", fontsize=9, color=INK, loc="left")
    fig.savefig(out, facecolor="white")
    plt.close(fig)


def render(ax, path: Path, color, elev=28, azim=-55, rotate=None):
    """Shaded render of an STL."""
    mesh = trimesh.load(path, force="mesh")
    if rotate is not None:
        mesh.apply_transform(rotate)
    v = mesh.vertices - mesh.bounds.mean(axis=0)
    tris = v[mesh.faces]
    light = np.array([0.4, -0.5, 0.75])
    light /= np.linalg.norm(light)
    nrm = mesh.face_normals
    shade = 0.45 + 0.55 * np.clip(nrm @ light, 0, 1)
    base = np.array(matplotlib.colors.to_rgb(color))
    fc = np.clip(base[None, :] * shade[:, None] + 0.12 * (1 - shade[:, None]), 0, 1)
    pc = Poly3DCollection(tris, facecolors=fc, edgecolors="none", linewidths=0)
    ax.add_collection3d(pc)
    r = np.abs(v).max()
    ax.set_xlim(-r, r)
    ax.set_ylim(-r, r)
    ax.set_zlim(-r, r)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elev, azim=azim)
    ax.axis("off")


def parts_sheet(g: gt.Geometry, stl: Path, out: Path):
    items = [
        ("track_TPU_x4.stl", "#3a4650", "Track ×4 (TPU 95A)\nprinted standing up as a ring", 30),
        ("sprocket_end_PETG_x4.stl", "#8fa7bf", "End sprocket ×4 (PETG)\nflat flange down", 28),
        ("sprocket_middle_double_PETG_x2.stl", "#8fa7bf", "Middle sprocket ×2 (PETG)\ntwo lanes, both units", 28),
        ("step_gauge_3_steps_1-5_PLA.stl", "#c5cbd1", "Step gauge (PLA, optional)\n3 ES1 steps at 1:5, lies on its side", 20),
    ]
    fig = plt.figure(figsize=(12, 3.6), dpi=150)
    stand = trimesh.transformations.rotation_matrix(math.pi / 2, (1, 0, 0))
    for i, (name, col, label, elev) in enumerate(items):
        ax = fig.add_subplot(1, 4, i + 1, projection="3d")
        render(ax, stl / name, col, elev=elev, rotate=stand if name.startswith("step_gauge") else None)
        ax.set_title(label, fontsize=9.5, color=INK, y=-0.08)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0.08, wspace=0)
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
