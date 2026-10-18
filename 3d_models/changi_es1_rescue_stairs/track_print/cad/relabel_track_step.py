"""Re-export the reviewed track STEP as a grouped, clearly named part tree (for the Fusion browser).
usage: python3 relabel_track_step.py <in.step> <out.step>"""
import sys, re, json, collections
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.XCAFApp import XCAFApp_Application
from OCP.TDF import TDF_LabelSequence, TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.TopLoc import TopLoc_Location
import cadquery as cq

SRC, OUT = sys.argv[1], sys.argv[2]

def read(path):
    app = XCAFApp_Application.GetApplication_s()
    doc = TDocStd_Document(TCollection_ExtendedString("MDTV-XCAF")); app.NewDocument(TCollection_ExtendedString("MDTV-XCAF"), doc)
    rd = STEPCAFControl_Reader(); rd.SetNameMode(True); rd.ReadFile(path); rd.Transfer(doc)
    tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    def name_of(label):
        n = TDataStd_Name(); return n.Get().ToExtString() if label.FindAttribute(TDataStd_Name.GetID_s(), n) else ""
    rows = []
    def walk(label, loc, path, inst):
        if tool.IsAssembly_s(label):
            comps = TDF_LabelSequence(); tool.GetComponents_s(label, comps)
            for i in range(1, comps.Length() + 1):
                c = comps.Value(i); ref = TDF_Label()
                if tool.GetReferredShape_s(c, ref):
                    walk(ref, loc.Multiplied(tool.GetLocation_s(c)), path + [name_of(label)], name_of(c))
        else:
            rows.append((path, inst or name_of(label), name_of(label), tool.GetShape_s(label).Moved(loc)))
    free = TDF_LabelSequence(); tool.GetFreeShapes(free)
    for i in range(1, free.Length() + 1):
        walk(free.Value(i), TopLoc_Location(), [], name_of(free.Value(i)))
    return rows

AL = (0.80, 0.82, 0.85); STEEL = (0.55, 0.57, 0.60); NEW = (0.86, 0.45, 0.16); BELT = (0.20, 0.21, 0.24); PLATE = (0.62, 0.72, 0.82); UHMW = (0.95, 0.95, 0.92)
G = {"rear": "01 Rear frame (step 2)", "front": "02 Front frame (step 4)", "rails": "03 Rails and carrier angles (steps 2-3, TS-10)",
     "shaftA": "04 Hinge shaft A, wheels and pins (steps 6-7, TS-06, TS-11)", "shaftB": "05 Hinge shaft B, wheels and pins (steps 6-7, TS-06, TS-11)",
     "noseA": "06 Nose idler A and tensioner (steps 10-11, TS-09)", "noseB": "07 Nose idler B and tensioner (steps 10-11, TS-09)",
     "rearA": "08 Rear idler A and tensioner (steps 10-11, TS-09)", "rearB": "09 Rear idler B and tensioner (steps 10-11, TS-09)",
     "tracks": "10 Tracks (step 11; option B belts shown, option A printed loop has the same envelope)"}
FR = {"FRONT": "front", "REAR": "rear", "F": "front", "R": "rear", "front": "front", "rear": "rear"}

def classify(n):
    """-> (group key, subgroup or None, short name, colour)"""
    def m(p): return re.search(p, n)
    x = m(r"^P2 Side plate REAR (A|B)")
    if x: return "rear", "P2 side plates and hinge bearings", f"P2 side plate, rear {x[1]} (reviewed: tab hole at +11, six carrier holes)", PLATE
    x = m(r"^Bearing 688-2RS.*rear side plate R(A|B)")
    if x: return "rear", "P2 side plates and hinge bearings", f"Bearing 688-2RS, P2 plate {x[1]} (seat laser 15.8, reamed 16 H7)", STEEL
    x = m(r"^P8 Cross bar 3030 x 160 \((rear|middle)\)")
    if x: return "rear", "3030 bars and corner brackets", f"P8 bar 3030 x 160, {x[1]}", AL
    x = m(r"^Inside corner bracket \(Al 6061, 4 mm.*, (rear|middle) bar R(A|B)")
    if x: return "rear", "3030 bars and corner brackets", f"Corner bracket 3030, {x[1]} bar {x[2]}", AL
    x = m(r"^M6x10 socket head cap screw.*, bracket to (rear|middle) bar R(A|B)")
    if x: return "rear", "3030 bars and corner brackets", f"M6x10 SHCS, bracket into {x[1]} bar {x[2]}", STEEL
    x = m(r"^T-nut M6 slot 8.*, bracket to (rear|middle) bar R(A|B)")
    if x: return "rear", "3030 bars and corner brackets", f"T-nut M6 slot 8, bracket in {x[1]} bar {x[2]}", STEEL
    x = m(r"^M5x8 socket head cap screw.*, bracket to plate, (rear|middle) bar R(A|B) (\d)")
    if x: return "rear", "3030 bars and corner brackets", f"M5x8 SHCS, bracket into P2, {x[1]} bar {x[2]} #{x[3]}", STEEL
    x = m(r"^T-nut M5 slot 8 \(3030\), deck to (rear|middle) bar (\d)")
    if x: return "rear", "T-nuts for the deck screws (Nhien's deck P12)", f"T-nut M5 slot 8, deck to {x[1]} bar #{x[2]}", STEEL
    x = m(r"^Hinge shaft bearing support (A|B)")
    if x: return "rear", "P17 hinge shaft supports", f"P17 hinge shaft support {x[1]} (5 mm plate + 4 mm foot)", AL
    x = m(r"^Bearing 688-2RS.*, support (A|B)")
    if x: return "rear", "P17 hinge shaft supports", f"Bearing 688-2RS, P17 support {x[1]}", STEEL
    x = m(r"^M5x10 socket head cap screw.*, support (A|B) to middle bar (\d)")
    if x: return "rear", "P17 hinge shaft supports", f"M5x10 SHCS, P17 {x[1]} into middle bar #{x[2]}", STEEL
    x = m(r"^T-nut M5 slot 8 \(30-series\), support (A|B) (\d)")
    if x: return "rear", "P17 hinge shaft supports", f"T-nut M5 slot 8, P17 {x[1]} #{x[2]}", STEEL
    x = m(r"^Shim washer 8x11x1 \(DIN 988\), shaft (A|B) pulley to support bearing")
    if x: return "shaft" + x[1], None, f"Shim 8x11x1, stage-2 pulley {x[1]} to the P17 bearing", STEEL
    x = m(r"^Track idler pulley .*\((nose|rear) (A|B),")
    if x: return x[1] + x[2], None, f"Idler wheel HTD 5M 20T, {x[1]} {x[2]} (bore 16 H7 for two 688s)", AL
    x = m(r"(nose|rear) idler (A|B)")
    if x:
        key, s = x[1] + x[2], x[2]; pos = x[1]
        if m(r"^Bearing 688-2RS"):
            k = m(r"#(\d)")[1]
            return key, None, f"Bearing 688-2RS, {pos} idler {s} #{k}", STEEL
        if m(r"^Washer 8x11x1"): return key, None, f"Washer 8x11x1 under the shoulder screw head, {pos} idler {s}", STEEL
        if m(r"^Nyloc nut M6"): return key, None, f"Nyloc nut M6, {pos} idler {s} (1.4 inboard for the slider)", STEEL
        if m(r"^Track idler pulley"): return key, None, f"Idler wheel HTD 5M 20T, {pos} {s} (bore 16 H7 for two 688s)", AL
        if m(r"^Shim washer 8x11x0.5"): return key, None, f"Shim 8x11x0.5, {pos} idler {s} to the plate", STEEL
        if m(r"^Bearing spacer sleeve"): return key, None, f"Spacer sleeve 8x10x9, {pos} idler {s}", STEEL
        if m(r"^Shoulder screw"): return key, None, f"Shoulder screw ISO 7379 8x25 M6, {pos} idler {s} (stub axle)", STEEL
    x = m(r"^Tensioner tab TS-09, (nose|rear) (A|B)")
    if x: return x[1] + x[2], None, f"TS-09 tensioner tab, {x[1]} {x[2]} (20x20x3 angle cut 30, 7.5x8 ear, M3 into the plate)", NEW
    x = m(r"^Tensioner slider TS-09, (nose|rear) (A|B)")
    if x: return x[1] + x[2], None, f"TS-09 slider, {x[1]} {x[2]} (8 mm angle slice, 19 leg + 8 foot, d6.4)", NEW
    x = m(r"^Jack screw M4x20 ISO 4762, (nose|rear) (A|B)")
    if x: return x[1] + x[2], None, f"TS-09 jack screw M4x20, {x[1]} {x[2]} (through leg B, tip on the foot)", NEW
    x = m(r"^Track belt .*\((front|rear) (A|B)\)")
    if x: return "tracks", None, f"Track belt HTD 550-5M-15 with 22 cleats, {x[1]} {x[2]}", BELT
    x = m(r"^Track drive pulley .*\((front|rear) (A|B),")
    if x: return "shaft" + x[2], None, f"Hinge wheel HTD 5M 20T, {x[1]} {x[2]} (bore 8 H7, cross pinned, TS-06)", AL
    x = m(r"^M3 Stage-2 hinge pulley (A|B)")
    if x: return "shaft" + x[1], None, f"Stage-2 pulley M3, {x[1]} (bore 8 H7, cross pinned)", AL
    x = m(r"^Hinge drive shaft (A|B) \(d8 h7 plain round, ([\d.]+) long\)")
    if x: return "shaft" + x[1], None, f"Hinge shaft {x[1]}, d8 h7 plain round x {x[2]} (TS-11)", STEEL
    x = m(r"^Spring pin ISO 8752 2.5x24, (front|rear) (A|B)")
    if x: return "shaft" + x[2], None, f"Spring pin 2.5x24, {x[1]} wheel {x[2]}", NEW
    x = m(r"^Spring pin ISO 8752 2.5x24, M3 Stage-2 hinge pulley (A|B)")
    if x: return "shaft" + x[1], None, f"Spring pin 2.5x24, stage-2 pulley {x[1]}", NEW
    x = m(r"^Shim washer 8x11x0.5, front pulley (A|B) to P1 bearing")
    if x: return "shaft" + x[1], None, f"Shim 8x11x0.5, front wheel {x[1]} to the P1 bearing", NEW
    x = m(r"^P1 Side plate FRONT (A|B)")
    if x: return "front", "P1 side plates and hinge bearings", f"P1 side plate, front {x[1]} (reviewed: tab hole at +11, six carrier holes)", PLATE
    x = m(r"^Bearing 688-2RS.*, front side plate F(A|B)")
    if x: return "front", "P1 side plates and hinge bearings", f"Bearing 688-2RS, P1 plate {x[1]} (seat laser 15.8, reamed 16 H7)", STEEL
    x = m(r"^P7 Cross bar 2020 x 110 \((hinge side|nose)\)")
    if x: return "front", "2020 bars and corner brackets", f"P7 bar 2020 x 110, {x[1]}", AL
    x = m(r"^Inside corner bracket 2020 .*, (hinge-side|nose) bar F(A|B)")
    if x: return "front", "2020 bars and corner brackets", f"Corner bracket 2020, {x[1]} bar {x[2]}", AL
    x = m(r"^M5x8 socket head cap screw.*, bracket to (hinge-side|nose) bar F(A|B)$")
    if x: return "front", "2020 bars and corner brackets", f"M5x8 SHCS, bracket into {x[1]} bar {x[2]}", STEEL
    x = m(r"^T-nut M5 slot 6 \(2020\), bracket to (hinge-side|nose) bar F(A|B)")
    if x: return "front", "2020 bars and corner brackets", f"T-nut M5 slot 6, bracket in {x[1]} bar {x[2]}", STEEL
    x = m(r"^M4x8 socket head cap screw.*, bracket to plate, (hinge-side|nose) bar F(A|B) (\d)")
    if x: return "front", "2020 bars and corner brackets", f"M4x8 SHCS, bracket into P1, {x[1]} bar {x[2]} #{x[3]}", STEEL
    x = m(r"^P([3-6]) Slide rail (FRONT|REAR) (UPPER|LOWER) (A|B)")
    if x: return "rails", f"{FR[x[2]].capitalize()} rails {x[4]}", f"P{x[1]} rail, {FR[x[2]]} {x[3].lower()} {x[4]} (UHMW, trimmed to 186)", UHMW
    x = m(r"^Rail carrier angle TS-10 (F|R)(A|B) (upper|lower)")
    if x: return "rails", f"{FR[x[1]].capitalize()} rails {x[2]}", f"TS-10 carrier angle, {FR[x[1]]} {x[2]} {x[3]} (10x10x1.5 x 186, 6.5 leg, three M3)", NEW
    return None

rows = read(SRC)
print("read", len(rows), "parts")
tree = collections.OrderedDict((k, collections.OrderedDict()) for k in G)
unsorted = []
for path, inst, proto, shape in rows:
    c = classify(inst)
    if c is None: unsorted.append(inst); continue
    key, sub, short, col = c
    tree[key].setdefault(sub, []).append((short, shape, col))
print("unsorted:", unsorted)
assert not unsorted
used = set()
def uniq(nm):
    base, k = nm, 2
    while nm in used: nm = f"{base} ({k})"; k += 1
    used.add(nm); return nm
asm = cq.Assembly(name="RB4107 track unit, reviewed 18 Oct 2026 (Nazim)")
total = 0
for key, subs in tree.items():
    g = cq.Assembly(name=uniq(G[key]))
    for sub, items in subs.items():
        target = g if sub is None else cq.Assembly(name=uniq(sub))
        for short, shape, col in items:
            target.add(cq.Shape.cast(shape), name=uniq(short), color=cq.Color(*col)); total += 1
        if sub is not None: g.add(target, name=target.name)
    asm.add(g, name=g.name)
asm.save(OUT, exportType="STEP")
print("written", OUT, "parts", total)
# print and save the tree
lines = []
for key, subs in tree.items():
    lines.append(G[key])
    for sub, items in subs.items():
        if sub: lines.append("  " + sub)
        for short, _, _ in items: lines.append(("    " if sub else "  ") + short)
open(OUT + ".tree.txt", "w").write("\n".join(lines))
# verify by re-reading
back = read(OUT)
depths = collections.Counter(len(p) for p, *_ in back)
print("re-read", len(back), "parts; depth histogram", dict(depths))
print("\n".join(lines[:40]))
