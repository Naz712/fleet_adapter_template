import sys, json, collections
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
from OCP.TopAbs import TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer

path = sys.argv[1]
app = XCAFApp_Application.GetApplication_s()
doc = TDocStd_Document(TCollection_ExtendedString("MDTV-XCAF")); app.NewDocument(TCollection_ExtendedString("MDTV-XCAF"), doc)
rd = STEPCAFControl_Reader(); rd.SetNameMode(True); rd.SetColorMode(True)
st = rd.ReadFile(path); rd.Transfer(doc)
tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
def name_of(label):
    n = TDataStd_Name()
    return n.Get().ToExtString() if label.FindAttribute(TDataStd_Name.GetID_s(), n) else ""
rows = []
def walk(label, loc, path, inst):
    if tool.IsAssembly_s(label):
        comps = TDF_LabelSequence(); tool.GetComponents_s(label, comps)
        for i in range(1, comps.Length() + 1):
            c = comps.Value(i); ref = TDF_Label()
            if tool.GetReferredShape_s(c, ref):
                walk(ref, loc.Multiplied(tool.GetLocation_s(c)), path + [name_of(label)], name_of(c))
    else:
        shape = tool.GetShape_s(label).Moved(loc)
        box = Bnd_Box(); BRepBndLib.Add_s(shape, box, True)
        xmin, ymin, zmin, xmax, ymax, zmax = box.Get()
        ns = 0; ex = TopExp_Explorer(shape, TopAbs_SOLID)
        while ex.More(): ns += 1; ex.Next()
        rows.append({"proto": name_of(label), "inst": inst, "path": path[1:], "bbox": [round(v, 2) for v in (xmin, ymin, zmin, xmax, ymax, zmax)], "solids": ns})
free = TDF_LabelSequence(); tool.GetFreeShapes(free)
for i in range(1, free.Length() + 1):
    walk(free.Value(i), TopLoc_Location(), [], name_of(free.Value(i)))
json.dump(rows, open("parts_index.json", "w"), indent=0)
print("parts:", len(rows), "status", st)
by = collections.defaultdict(list)
for r in rows: by[" / ".join(r["path"])].append(r)
for k, v in by.items():
    print(f"\n== {k} ({len(v)})")
    cnt = collections.Counter(r["proto"] for r in v)
    for n, c in sorted(cnt.items()): print(f"  {c:3d} x {n}")
