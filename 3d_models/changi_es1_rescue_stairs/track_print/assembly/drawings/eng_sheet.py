"""A3 engineering drawing sheet in the style of a CAD drawing: border with zone letters and
numbers, title block, parts list, balloons, true-scale views. Monochrome: black lines on white,
hatching for cut faces. Sheet coordinates are mm, origin bottom-left, 420 x 297.

Use with the dimension helpers in ../drawing.py (dim_h, dim_v, dim_dia, leader, centreline).
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle

HERE = Path(__file__).resolve().parent
SPEC = json.loads((HERE.parent / "parts_spec.json").read_text())
W, H = 420.0, 297.0           # A3 landscape, mm
MARGIN = 10.0                 # outer margin to the frame
INK = "#000000"
plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans"})


def _mm_axes(fig):
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")
    return ax


def a3_sheet(title, dwg_no, material="", finish="", qty="", scale="1:1", sheet="1 OF 1", drawn="NAZIM", project="RB4107 ES1 RESCUE CARRIER, 1:5 PROTOTYPE", notes=None):
    """Returns (fig, view) where view(x, y, xlim, ylim, scale, name) adds a true-scale view whose
    bottom-left corner sits at sheet (x, y) mm. 1 drawing mm at scale 1:2 is 0.5 sheet mm."""
    fig = plt.figure(figsize=(W / 25.4, H / 25.4), dpi=150)
    fig.patch.set_facecolor("white")
    bg = _mm_axes(fig)
    # frame and zones
    f0, f1 = MARGIN, MARGIN + 5
    bg.add_patch(Rectangle((f0, f0), W - 2 * f0, H - 2 * f0, fc="none", ec=INK, lw=0.5))
    bg.add_patch(Rectangle((f1, f1), W - 2 * f1, H - 2 * f1, fc="none", ec=INK, lw=1.2))
    cols, rows = 8, 6
    cw, rh = (W - 2 * f1) / cols, (H - 2 * f1) / rows
    for i in range(1, cols):
        for yy in (f0, H - f1):
            bg.plot([f1 + i * cw] * 2, [yy, yy + 5], color=INK, lw=0.5)
    for i in range(cols):
        for yy in (f0 + 2.5, H - f1 + 2.5):
            bg.text(f1 + (cols - i - 0.5) * cw, yy, str(i + 1), ha="center", va="center", fontsize=7)
    for j in range(1, rows):
        for xx in (f0, W - f1):
            bg.plot([xx, xx + 5], [f1 + j * rh] * 2, color=INK, lw=0.5)
    for j in range(rows):
        for xx in (f0 + 2.5, W - f1 + 2.5):
            bg.text(xx, f1 + (rows - j - 0.5) * rh, "ABCDEF"[j], ha="center", va="center", fontsize=7)
    for (x, y, dx, dy) in ((W / 2, f0, 0, 5), (W / 2, H - f0, 0, -5), (f0, H / 2, 5, 0), (W - f0, H / 2, -5, 0)):
        bg.plot([x, x + dx], [y, y + dy], color=INK, lw=1.0)
    # title block, bottom right: 180 x 48
    tx, ty, tw, th = W - f1 - 180, f1, 180, 48
    bg.add_patch(Rectangle((tx, ty), tw, th, fc="white", ec=INK, lw=0.8))
    for yy in (ty + 10, ty + 20, ty + 30):
        bg.plot([tx, tx + tw], [yy, yy], color=INK, lw=0.5)
    bg.plot([tx + 90, tx + 90], [ty, ty + th], color=INK, lw=0.5)
    bg.plot([tx + 130, tx + 130], [ty, ty + 20], color=INK, lw=0.5)
    bg.plot([tx + 160, tx + 160], [ty, ty + 10], color=INK, lw=0.5)
    small = dict(fontsize=5.5, va="top", ha="left")
    bg.text(tx + 2, ty + th - 2, "UNLESS OTHERWISE SPECIFIED:\nDIMENSIONS ARE IN MILLIMETERS\nAT 1:5 MODEL SIZE\nTOLERANCES: LINEAR 0.2, ANGULAR 1 DEG\nDO NOT SCALE DRAWING", **small)
    bg.text(tx + 2, ty + 28, f"DRAWN:  {drawn}", **small)
    bg.text(tx + 45, ty + 28, "DATE:  2026-10-14", **small)
    bg.text(tx + 2, ty + 18, f"MATERIAL:  {material}", **small)
    bg.text(tx + 2, ty + 13.5, f"FINISH:  {finish}", **small)
    bg.text(tx + 2, ty + 8, project, **small)
    bg.text(tx + 92, ty + th - 2, "TITLE:", **small)
    bg.text(tx + 92, ty + th - 8, title, fontsize=9.5, fontweight="bold", va="top", ha="left")
    bg.text(tx + 92, ty + 18, "DWG NO.", **small)
    bg.text(tx + 92, ty + 13, dwg_no, fontsize=9, va="top", ha="left")
    bg.text(tx + 132, ty + 18, "QTY.", **small)
    bg.text(tx + 132, ty + 13, str(qty), fontsize=9, va="top", ha="left")
    bg.text(tx + 92, ty + 8, "SCALE:", **small)
    bg.text(tx + 92, ty + 4.5, scale, fontsize=7, va="top", ha="left")
    bg.text(tx + 132, ty + 8, "SHEET", **small)
    bg.text(tx + 132, ty + 4.5, sheet, fontsize=7, va="top", ha="left")
    bg.text(tx + 162, ty + 8, "SIZE", **small)
    bg.text(tx + 162, ty + 4.5, "A3", fontsize=9, fontweight="bold", va="top", ha="left")
    # third-angle projection symbol, left of the title block
    sx, sy = tx - 22, ty + 6
    bg.add_patch(Circle((sx + 6, sy + 4), 3, fc="none", ec=INK, lw=0.5))
    bg.add_patch(Circle((sx + 6, sy + 4), 1.5, fc="none", ec=INK, lw=0.5))
    bg.add_patch(Polygon([(sx + 11, sy + 1), (sx + 19, sy + 2.2), (sx + 19, sy + 5.8), (sx + 11, sy + 7)], closed=True, fc="none", ec=INK, lw=0.5))
    bg.plot([sx + 13, sx + 13], [sy + 1.3, sy + 6.7], color=INK, lw=0.5)
    bg.text(sx + 10, sy + 10, "THIRD ANGLE", fontsize=5, ha="center")
    if notes:
        bg.text(f1 + 4, f1 + 4, "NOTES:\n" + "\n".join(f"{i + 1}. {n}" for i, n in enumerate(notes)), fontsize=6, va="bottom", ha="left", linespacing=1.4)

    def view(x, y, xlim, ylim, scale_num=1.0, name=None):
        """True-scale view: scale_num = sheet mm per drawing mm (1:2 -> 0.5)."""
        wmm = (xlim[1] - xlim[0]) * scale_num
        hmm = (ylim[1] - ylim[0]) * scale_num
        ax = fig.add_axes([x / W, y / H, wmm / W, hmm / H])
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.patch.set_visible(False)
        if name:
            bg.text(x + wmm / 2, y + hmm + 3, name, fontsize=7.5, ha="center", va="bottom")
        return ax

    return fig, view, bg


def balloon(ax, target, at, n, r=None):
    """Numbered balloon at `at` (data coords) with a leader to `target`."""
    xr = ax.get_xlim()
    r = r or (xr[1] - xr[0]) * 0.02
    ax.add_patch(FancyArrowPatch(at, target, arrowstyle="-", lw=0.5, color=INK, shrinkA=0, shrinkB=0))
    ax.plot([target[0]], [target[1]], marker="o", ms=2.0, color=INK)
    ax.add_patch(Circle(at, r, fc="white", ec=INK, lw=0.6, zorder=6))
    ax.text(at[0], at[1], str(n), ha="center", va="center", fontsize=7, zorder=7)


def parts_list(bg, rows, x=None, y=None, col_w=(14, 60, 70, 12)):
    """Parts list table on the sheet: rows of (item, part number, description, qty); top-left at (x, y) mm."""
    x = x if x is not None else W - MARGIN - 5 - sum(col_w)
    y = y if y is not None else H - MARGIN - 5 - 2
    rh = 6.0
    head = ("ITEM NO.", "PART NUMBER", "DESCRIPTION", "QTY.")
    for i, row in enumerate([head] + list(rows)):
        yy = y - i * rh
        xx = x
        for j, (cell, cw) in enumerate(zip(row, col_w)):
            bg.add_patch(Rectangle((xx, yy - rh), cw, rh, fc="white", ec=INK, lw=0.5))
            bg.text(xx + 1.5 if j != 0 and j != 3 else xx + cw / 2, yy - rh / 2, str(cell), fontsize=5.8 if i else 6.0,
                    fontweight="bold" if i == 0 else "normal", ha="left" if j in (1, 2) else "center", va="center")
            xx += cw
    return y - (len(rows) + 1) * rh


def section_mark(ax, x, y0, y1, label="A", side=1):
    """Cutting-plane line with arrows and letters."""
    L = (y1 - y0) * 0.12
    ax.plot([x, x], [y0, y0 + L], color=INK, lw=1.1)
    ax.plot([x, x], [y1 - L, y1], color=INK, lw=1.1)
    for yy in (y0, y1):
        ax.annotate("", xy=(x + 4 * side, yy), xytext=(x, yy), arrowprops=dict(arrowstyle="-|>", lw=0.9, color=INK, mutation_scale=9))
        ax.text(x + 6 * side, yy, f"{label}", fontsize=8, fontweight="bold", ha="center", va="center")


def save(fig, name):
    out = HERE / f"{name}.png"
    fig.savefig(out, dpi=150, facecolor="white")
    print(out)
    return out
