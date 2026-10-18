import sys, re, math, json
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.XCAFApp import XCAFApp_Application
from OCP.TDF import TDF_LabelSequence, TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.TopLoc import TopLoc_Location
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.BRep import BRep_Tool
from OCP.TopoDS import TopoDS
import numpy as np
path = sys.argv[1]
app = XCAFApp_Application.GetApplication_s(); doc = TDocStd_Document(TCollection_ExtendedString("MDTV-XCAF")); app.NewDocument(TCollection_ExtendedString("MDTV-XCAF"), doc)
rd = STEPCAFControl_Reader(); rd.SetNameMode(True); rd.SetColorMode(True); rd.ReadFile(path); rd.Transfer(doc)
tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
def name_of(label):
    n = TDataStd_Name(); return n.Get().ToExtString() if label.FindAttribute(TDataStd_Name.GetID_s(), n) else ""
parts = []
def walk(label, loc, inst):
    if tool.IsAssembly_s(label):
        comps = TDF_LabelSequence(); tool.GetComponents_s(label, comps)
        for i in range(1, comps.Length() + 1):
            c = comps.Value(i); ref = TDF_Label()
            if tool.GetReferredShape_s(c, ref): walk(ref, loc.Multiplied(tool.GetLocation_s(c)), name_of(c) or name_of(ref))
    else: parts.append((inst or name_of(label), tool.GetShape_s(label).Moved(loc)))
free = TDF_LabelSequence(); tool.GetFreeShapes(free)
for i in range(1, free.Length() + 1): walk(free.Value(i), TopLoc_Location(), name_of(free.Value(i)))
print("parts in STEP:", len(parts))
def bb(s): b = Bnd_Box(); BRepBndLib.Add_s(s, b, True); return b.Get()
def vol(s): g = GProp_GProps(); BRepGProp.VolumeProperties_s(s, g); return g.Mass()
boxes = [bb(s) for n, s in parts]
def overlap(a, b, tol=-0.05): return all(a[i] < b[i+3] + tol and b[i] < a[i+3] + tol for i in range(3))
changed = [i for i, (n, s) in enumerate(parts) if "[" in n]
hits = []
for i in changed:
    for j, (n2, s2) in enumerate(parts):
        if j == i or (j in changed and j < i): continue
        if "belt" in n2 or "belt" in parts[i][0]: continue
        if not overlap(boxes[i], boxes[j]): continue
        try: v = vol(BRepAlgoAPI_Common(parts[i][1], s2).Shape())
        except Exception as e: v = -1
        if v > 0.05: hits.append((v, parts[i][0][:60], n2[:60]))
hits.sort(reverse=True)
print("interferences (> 0.05 mm3):", len(hits))
for v, a, b in hits[:25]: print(f"  {v:8.2f} mm3  {a}  <->  {b}")
# ---- render
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
def tris(shape, defl=0.6):
    BRepMesh_IncrementalMesh(shape, defl, False, 0.5, True)
    out = []; ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face_s(ex.Current()); loc = TopLoc_Location(); t = BRep_Tool.Triangulation_s(f, loc)
        if t is not None:
            tr = loc.Transformation(); nn = t.NbNodes()
            pts = np.array([(lambda p: [p.X(), p.Y(), p.Z()])(t.Node(k).Transformed(tr)) for k in range(1, nn + 1)])
            for k in range(1, t.NbTriangles() + 1):
                a, b, c = t.Triangle(k).Get(); out.append(pts[[a - 1, b - 1, c - 1]])
        ex.Next()
    return out
def render(fname, view, clip=None, elev=22, azim=-55, title=""):
    fig = plt.figure(figsize=(11, 7), dpi=110); ax = fig.add_subplot(111, projection="3d")
    for n, s in parts:
        b = bb(s)
        if clip and not overlap(b, clip, tol=0): continue
        T = tris(s, 0.8 if "belt" in n else 0.4)
        if not T: continue
        col = (0.86, 0.45, 0.16) if "[new]" in n else (0.35, 0.55, 0.85) if "[reviewed]" in n or "[trimmed" in n or "[moved" in n else (0.25, 0.26, 0.3) if "belt" in n else (0.78, 0.8, 0.83)
        pc = Poly3DCollection(T, facecolor=col, edgecolor="none", alpha=1.0); pc.set_sort_zpos(0); ax.add_collection3d(pc)
    lo = clip if clip else view
    ax.set_xlim(lo[0], lo[3]); ax.set_ylim(lo[2], lo[5]); ax.set_zlim(lo[1], lo[4])
    ax.view_init(elev=elev, azim=azim); ax.set_box_aspect((lo[3]-lo[0], lo[5]-lo[2], lo[4]-lo[1])); ax.set_axis_off(); ax.set_title(title, fontsize=10)
    fig.tight_layout(); fig.savefig(fname); plt.close(fig); print("saved", fname)
render("r_all.png", (-250, -30, -50, 250, 30, 170), title="track unit, reviewed: orange = new, blue = changed")
render("r_nose.png", None, clip=(195, -16, -30, 245, 16, 30), elev=28, azim=-120, title="nose A: idler, slider with foot, tab, jack screw, carrier ends")
render("r_hinge.png", None, clip=(-25, -20, -50, 25, 20, 40), elev=25, azim=-60, title="hinge A: shaft, pins, pulleys, shim, P17")
