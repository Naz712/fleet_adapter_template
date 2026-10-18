import sys, re, json, math
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.XCAFApp import XCAFApp_Application
from OCP.TDF import TDF_LabelSequence, TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.TopLoc import TopLoc_Location
from OCP.gp import gp_Pnt, gp_Dir, gp_Ax2, gp_Trsf, gp_Vec
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeBox
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
import cadquery as cq

SRC, OUT = sys.argv[1], sys.argv[2]
# ---------- read Nhien's assembly with names and world placements
app = XCAFApp_Application.GetApplication_s()
doc = TDocStd_Document(TCollection_ExtendedString("MDTV-XCAF")); app.NewDocument(TCollection_ExtendedString("MDTV-XCAF"), doc)
rd = STEPCAFControl_Reader(); rd.SetNameMode(True); rd.ReadFile(SRC); rd.Transfer(doc)
tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
def name_of(label):
    n = TDataStd_Name(); return n.Get().ToExtString() if label.FindAttribute(TDataStd_Name.GetID_s(), n) else ""
parts = []   # (group, name, shape in world coords)
def walk(label, loc, group):
    if tool.IsAssembly_s(label):
        comps = TDF_LabelSequence(); tool.GetComponents_s(label, comps)
        for i in range(1, comps.Length() + 1):
            c = comps.Value(i); ref = TDF_Label()
            if tool.GetReferredShape_s(c, ref):
                walk(ref, loc.Multiplied(tool.GetLocation_s(c)), group or name_of(label) if group else name_of(label) if name_of(label) else group)
    else:
        parts.append((group, name_of(label), tool.GetShape_s(label).Moved(loc)))
free = TDF_LabelSequence(); tool.GetFreeShapes(free)
for i in range(1, free.Length() + 1):
    top = free.Value(i)
    comps = TDF_LabelSequence(); tool.GetComponents_s(top, comps)
    for j in range(1, comps.Length() + 1):
        c = comps.Value(j); ref = TDF_Label()
        if tool.GetReferredShape_s(c, ref): walk(ref, tool.GetLocation_s(c), name_of(ref))
print("parts read:", len(parts))

# ---------- helpers
def cyl(p, d, r, h): return BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(*p), gp_Dir(*d)), r, h).Shape()
def box(x0, y0, z0, x1, y1, z1): return BRepPrimAPI_MakeBox(gp_Pnt(min(x0,x1), min(y0,y1), min(z0,z1)), abs(x1-x0), abs(y1-y0), abs(z1-z0)).Shape()
def cut(a, b): return BRepAlgoAPI_Cut(a, b).Shape()
def fuse(a, b): return BRepAlgoAPI_Fuse(a, b).Shape()
def moved(s, dx, dy, dz): t = gp_Trsf(); t.SetTranslation(gp_Vec(dx, dy, dz)); return s.Moved(TopLoc_Location(t))
def bbox(s): b = Bnd_Box(); BRepBndLib.Add_s(s, b, True); return b.Get()
def ring(z0, z1, ro, ri, x=0.0, y=0.0): return cut(cyl((x, y, z0), (0, 0, 1), ro, z1 - z0), cyl((x, y, z0 - 1), (0, 0, 1), ri, z1 - z0 + 2))

KEEP = re.compile(r"^(P1 Side plate|P2 Side plate|P3 Slide|P4 Slide|P5 Slide|P6 Slide|P7 Cross bar|P8 Cross bar|Hinge shaft bearing support|Inside corner bracket|Bearing 688|Shim washer 8x11|Bearing spacer sleeve|Washer 8x11x1|Nyloc nut M6|Shoulder screw|Track drive pulley|Track idler pulley|M3 Stage-2 hinge pulley|Hinge drive shaft|Track belt|M6x10 socket|T-nut M6 slot 8|M5x8 socket head cap screw ISO 4762, bracket|T-nut M5 slot (6|8)|M4x8 socket head cap screw ISO 4762, bracket|M5x10 socket)")
DROP_NOTE = {"E-clip": "E-clips deleted (pins locate the shaft)", "M4x8 grub": "grub screws deleted (cross pins drive the pulleys)", "Washer M6 DIN 125": "M6 washers replaced by the TS-09 sliders", "RS 427-991": "rail clips replaced by full-length carrier angles (TS-10)", "rail screw": "clip screws deleted", "plate screw": "clip screws deleted"}
out = []        # (name, shape, color)
log = []
AL = (0.80, 0.82, 0.85); STEEL = (0.55, 0.57, 0.60); NEW = (0.86, 0.45, 0.16); BELT = (0.20, 0.21, 0.24); PLATE = (0.62, 0.72, 0.82); UHMW = (0.95, 0.95, 0.92)
shafts = {}; pulleys = []
for group, name, shape in parts:
    if group not in ("Rear chassis", "Front section"): continue
    if not KEEP.search(name):
        for k, v in DROP_NOTE.items():
            if k in name: log.append(f"dropped: {name} ({v})"); break
        continue
    b = bbox(shape); zc = 0.5 * (b[2] + b[5])
    if name.startswith("Hinge drive shaft"):
        side = "A" if " A " in name else "B"
        s = cyl((0, 0, b[2]), (0, 0, 1), 4.0, b[5] - b[2]); shafts[side] = [s, b[2], b[5]]
        log.append(f"replaced: {name} -> plain round shaft d8 h7, {b[5]-b[2]:.1f} long, no flat, no grooves")
        continue
    if name.startswith("Track drive pulley") or name.startswith("M3 Stage-2"):
        s = cut(shape, cyl((0, 0, b[2] - 1), (0, 0, 1), 4.0, b[5] - b[2] + 2))           # round out the D-bore to d8
        s = cut(s, cyl((0, -20, zc), (0, 1, 0), 1.25, 40))                                  # cross hole d2.5 at mid-face
        pulleys.append((name, zc)); out.append((name.replace("D-bore 8, M4 grub", "bore 8 H7, pinned").replace("D-bore 8", "bore 8 H7, pinned") + " [reviewed]", s, AL))
        log.append(f"modified: {name} -> round bore 8 H7, d2.5 cross hole at z {zc:.1f}")
        continue
    if re.match(r"P[3-6] Slide", name):
        if b[0] > 0: s = cut(shape, box(204, -30, b[2] - 1, 260, 30, b[5] + 1))
        else: s = cut(shape, box(-260, -30, b[2] - 1, -204, 30, b[5] + 1))
        out.append((name + " [trimmed to 186]", s, UHMW)); log.append(f"modified: {name} -> trimmed 3 mm at the idler end (186 long)"); continue
    if name.startswith("P1 Side plate") or name.startswith("P2 Side plate"):
        x = 223 if b[3] > 100 else -223
        s = cut(shape, cyl((x, 11, b[2] - 1), (0, 0, 1), 1.25, 7))                           # new M3 tap-drill hole for the tensioner tab
        for xh in ((40, 105, 170) if x > 0 else (-40, -105, -170)):
            for yh in (3.5, -3.5): s = cut(s, cyl((xh, yh, b[2] - 1), (0, 0, 1), 1.25, 7))   # carrier angle holes, M3 tap drill
        out.append((name + " [reviewed: tab hole (223, +11), carrier holes y +-3.5]", s, PLATE))
        log.append(f"modified: {name} -> M3 tap-drill hole at ({x:+d}, +11) and 6 carrier holes at x {abs(40)},{105},{170} y +-3.5; seats to be laser-cut 15.8 and reamed 16 H7")
        continue
    if name.startswith("Nyloc nut M6"):
        # slider (3) replaces the M6 washer (1.6): nut moves 1.4 toward the plate's inboard side
        dz = 1.4 if b[2] > 50 and b[2] < 100 or (b[2] < 50 and b[2] > -10 and b[2] > 0) else -1.4
        if "nose idler A" in name: dz = +1.4
        if "nose idler B" in name: dz = -1.4
        if "rear idler A" in name: dz = +1.4
        if "rear idler B" in name: dz = -1.4
        out.append((name + " [moved 1.4 for the slider]", moved(shape, 0, 0, dz), STEEL)); continue
    col = BELT if "belt" in name else PLATE if "plate" in name.lower() and "support" not in name else STEEL if re.search(r"Bearing|screw|nut|Washer|Shim|sleeve|T-nut", name) else AL
    out.append((name, shape, col))

# ---------- shafts with cross holes, pins, shims
for side, (s, z0, z1) in shafts.items():
    for name, zc in pulleys:
        if (" A" in name.split("(")[-1] or name.endswith("pulley A")) == (side == "A") or ((" A," in name or "A)" in name) == (side == "A")):
            pass
    out.append((f"Hinge drive shaft {side} (d8 h7 plain round, {z1-z0:.1f} long) [reviewed]", s, STEEL))
for name, zc in pulleys:
    side = "A" if re.search(r"(front|rear|pulley) A", name) else "B"
    sh = shafts[side][0]; shafts[side][0] = cut(sh, cyl((0, -20, zc), (0, 1, 0), 1.25, 40))
    out.append((f"Spring pin ISO 8752 2.5x24, {name.split('(')[-1].rstrip(')').split(',')[0]} [new]", cyl((0, -12, zc), (0, 1, 0), 1.25, 24), NEW))
# rewrite the shaft entries with the holes cut
out = [(n, (shafts["A"][0] if n.startswith("Hinge drive shaft A") else shafts["B"][0] if n.startswith("Hinge drive shaft B") else s), c) for n, s, c in out]
out.append(("Shim washer 8x11x0.5, front pulley A to P1 bearing [new]", ring(-0.5, 0.0, 5.5, 4.0), NEW))
out.append(("Shim washer 8x11x0.5, front pulley B to P1 bearing [new]", ring(120.0, 120.5, 5.5, 4.0), NEW))

# ---------- rail carrier angles TS-10 (10x10x1.5, 186 long, plate leg cut to 6.5), one per rail
def carrier(x0, x1, upper, zface, into):   # into = +1 if the lane is at z > zface, -1 if at z < zface
    za, zb = (zface, zface + 10 * into)
    leg_under = box(x0, 6.8 if upper else -8.3, za, x1, 8.3 if upper else -6.8, zb)                      # 10 leg under/over the rail
    leg_plate = box(x0, 0.3 if upper else -6.8, zface, x1, 6.8 if upper else -0.3, zface + 1.5 * into)    # 6.5 leg on the plate face
    s = fuse(leg_under, leg_plate)
    for xh in (40, 105, 170):
        xx = xh if x1 > 0 else -xh
        s = cut(s, cyl((xx, 3.55 if upper else -3.55, zface - 2), (0, 0, 1), 1.7, 6))                    # d3.4 through the plate leg
    return s
for nm, x0, x1, zface, into in (("FA", 18, 204, 0, -1), ("FB", 18, 204, 120, +1), ("RA", -204, -18, -25, -1), ("RB", -204, -18, 145, +1)):
    for upper in (True, False):
        out.append((f"Rail carrier angle TS-10 {nm} {'upper' if upper else 'lower'} (Al 10x10x1.5 x 186, plate leg 6.5) [new]", carrier(x0, x1, upper, zface, into), NEW))

# ---------- tensioner sets TS-09: tab, slider, jack screw, at each idler
def tab(xs, zface, into):     # xs = +1 nose side, -1 rear side; the tab sits on the plate's inboard face
    legB = box(215.5 * xs, -15, zface, 218.5 * xs, 15, zface + 20 * into)
    ear = box(218.5 * xs, 7, zface, 226 * xs, 15, zface + 3 * into)
    s = fuse(legB, ear)
    s = cut(s, cyl((223 * xs, 11, zface - 10), (0, 0, 1), 1.7, 20))                       # d3.4 through the ear, M3 x 6 into the plate
    s = cut(s, cyl((214 * xs, -11, zface + 6 * into), (xs, 0, 0), 2.0, 6))               # M4 tapped through leg B (shown at 4.0): 6 from the plate face, 4 from the bottom
    return s
def slider(xs, zface, into):  # 8 mm slice of 20x20x3 angle: 19 leg on the plate with the d6.4 hole, 8 foot bent inboard at the bottom
    leg = cut(box(221 * xs, -13, zface, 229 * xs, 6, zface + 3 * into), cyl((225 * xs, 0, zface - 10), (0, 0, 1), 3.2, 20))
    foot = box(221 * xs, -13, zface, 229 * xs, -10, zface + 8 * into)
    return fuse(leg, foot)
def jack(xs, zface, into):    # M4 x 20 socket head: through leg B, tip on the slider's foot
    zc = zface + 6 * into
    shank = cyl((221 * xs, -11, zc), (-xs, 0, 0), 2.0, 18.5)
    head = cyl((202.5 * xs, -11, zc), (-xs, 0, 0), 3.5, 4)
    return fuse(shank, head)
for nm, xs, zface, into in (("nose A", 1, 5, +1), ("nose B", 1, 115, -1), ("rear A", -1, -20, +1), ("rear B", -1, 140, -1)):
    out.append((f"Tensioner tab TS-09, {nm} (Al angle 20x20x3 cut 30, leg B 1.5 off the slot, 7.5x8 ear at y 7..15) [new]", tab(xs, zface, into), NEW))
    out.append((f"Tensioner slider TS-09, {nm} (8 mm slice of 20x20x3 angle, 19 leg + 8 foot, d6.4) [new]", slider(xs, zface, into), NEW))
    out.append((f"Jack screw M4x20 ISO 4762, {nm} [new]", jack(xs, zface, into), NEW))

# ---------- export
asm = cq.Assembly(name="RB4107 track unit - reviewed 18 Oct 2026")
for n, s, c in out:
    asm.add(cq.Shape.cast(s), name=n[:120], color=cq.Color(*c))
asm.save(OUT, exportType="STEP")
json.dump({"parts": [n for n, s, c in out], "log": log}, open(OUT + ".json", "w"), indent=1)
names = [n for n, s, c in out]; print("written", OUT, "parts", len(out), "unique names", len(set(names))); print("\n".join(log[:12])); print("...", len(log), "log lines")
