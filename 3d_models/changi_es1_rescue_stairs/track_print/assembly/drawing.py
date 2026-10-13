"""Shared helpers for the dimensioned part drawings in this folder (matplotlib, mm, 2D).

Every drawing uses these so the sheets look alike: thin dark outlines, light fills, grey
dimension lines with closed arrowheads, the value in mm centred on the line.
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Polygon, Rectangle

HERE = Path(__file__).resolve().parent
SPEC = json.loads((HERE / "parts_spec.json").read_text())

INK, MUTED, DIM, RED = "#0b0a0a", "#5b6168", "#3a4046", "#ed1c24"
FILL = {"tpu": "#3a4650", "pla": "#c9a227", "steel": "#9aa2a9", "petg": "#6f9bd1", "bearing": "#b8bfc6", "light": "#e6e9ec"}
plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans"})


def sheet(title, subtitle, size=(11, 7.5)):
    """A4-ish landscape sheet with a title block. Returns (fig, add_view) where add_view(rect, name)
    makes an equal-aspect axes at rect=[left, bottom, width, height] (figure fractions)."""
    fig = plt.figure(figsize=size, dpi=200)
    fig.patch.set_facecolor("white")
    fig.text(0.04, 0.955, title, fontsize=15, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.915, subtitle, fontsize=9, color=MUTED, va="top")
    fig.add_artist(plt.Line2D([0.04, 0.96], [0.895, 0.895], color=INK, lw=1.2))

    def add_view(rect, name=None):
        ax = fig.add_axes(rect)
        ax.set_aspect("equal")
        ax.axis("off")
        if name:
            ax.set_title(name, fontsize=9.5, color=INK, loc="left", pad=4)
        return ax

    return fig, add_view


def note_block(fig, lines, x=0.60, y=0.30, w=0.36):
    """Material / qty / process notes at the bottom right."""
    fig.text(x, y, "\n".join(lines), fontsize=8.5, color=INK, va="top", linespacing=1.5,
             bbox=dict(boxstyle="square,pad=0.6", fc=FILL["light"], ec="none"))


def dim_h(ax, x0, x1, y, text=None, ext_from=None, offset=0, fontsize=8):
    """Horizontal dimension between x0 and x1 at height y. ext_from: y where the extension lines start."""
    if ext_from is not None:
        for x in (x0, x1):
            ax.plot([x, x], [ext_from, y + (0.4 if y > ext_from else -0.4)], color=DIM, lw=0.5)
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="<|-|>", mutation_scale=7, lw=0.6, color=DIM, shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, y + offset, text if text is not None else f"{abs(x1 - x0):g}", ha="center", va="bottom", fontsize=fontsize, color=INK,
            bbox=dict(fc="white", ec="none", pad=0.8))


def dim_v(ax, y0, y1, x, text=None, ext_from=None, offset=0, fontsize=8):
    """Vertical dimension between y0 and y1 at x. ext_from: x where the extension lines start."""
    if ext_from is not None:
        for y in (y0, y1):
            ax.plot([ext_from, x + (0.4 if x > ext_from else -0.4)], [y, y], color=DIM, lw=0.5)
    ax.add_patch(FancyArrowPatch((x, y0), (x, y1), arrowstyle="<|-|>", mutation_scale=7, lw=0.6, color=DIM, shrinkA=0, shrinkB=0))
    ax.text(x + offset, (y0 + y1) / 2, text if text is not None else f"{abs(y1 - y0):g}", ha="center", va="center", fontsize=fontsize, color=INK, rotation=90,
            bbox=dict(fc="white", ec="none", pad=0.8))


def dim_dia(ax, cx, cy, r, angle_deg, text, length=None, fontsize=8):
    """Diameter dimension: a line through the centre at angle_deg, arrowheads on the circle, text past one end."""
    import math
    a = math.radians(angle_deg)
    dx, dy = math.cos(a), math.sin(a)
    ax.add_patch(FancyArrowPatch((cx - r * dx, cy - r * dy), (cx + r * dx, cy + r * dy), arrowstyle="<|-|>", mutation_scale=7, lw=0.6, color=DIM, shrinkA=0, shrinkB=0))
    L = length or r * 1.35
    ax.plot([cx + r * dx, cx + L * dx], [cy + r * dy, cy + L * dy], color=DIM, lw=0.5)
    ax.text(cx + L * dx, cy + L * dy, text, ha="left" if dx >= 0 else "right", va="center", fontsize=fontsize, color=INK,
            bbox=dict(fc="white", ec="none", pad=0.8))


def leader(ax, xy, xytext, text, fontsize=8):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=fontsize, color=INK, ha="left", va="center",
                arrowprops=dict(arrowstyle="-|>", lw=0.6, color=DIM, mutation_scale=7, shrinkA=0, shrinkB=1),
                bbox=dict(fc="white", ec="none", pad=0.8))


def centreline(ax, x0, y0, x1, y1):
    ax.plot([x0, x1], [y0, y1], color=DIM, lw=0.5, dashes=(8, 2, 1.5, 2))


def section_hatch(patch):
    patch.set_hatch("////")
    patch.set_linewidth(0.6)
    return patch


def outline(ax, pts, fill, lw=0.8, hatch=False, alpha=1.0):
    p = Polygon(pts, closed=True, fc=fill, ec=INK, lw=lw, alpha=alpha)
    if hatch:
        section_hatch(p)
    ax.add_patch(p)
    return p


def rect(ax, x, y, w, h, fill, lw=0.8, hatch=False, alpha=1.0):
    p = Rectangle((x, y), w, h, fc=fill, ec=INK, lw=lw, alpha=alpha)
    if hatch:
        section_hatch(p)
    ax.add_patch(p)
    return p


def circle(ax, cx, cy, r, fill="none", lw=0.8, ls="-"):
    p = Circle((cx, cy), r, fc=fill, ec=INK, lw=lw, ls=ls)
    ax.add_patch(p)
    return p


def save(fig, name):
    out = HERE / "drawings" / f"{name}.png"
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=200, facecolor="white")
    print(out)
    return out
