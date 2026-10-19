import html, math
def svg_shaft():
    sx = 6.5; x0 = 30; cy = 150; sy = 2.0
    X = lambda z: x0 + (z + 48) * sx
    def rect(z0, z1, h, fill, stroke="#333"):
        return f'<rect x="{X(z0):.1f}" y="{cy - h*sy/2:.1f}" width="{(z1-z0)*sx:.1f}" height="{h*sy:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="0.8"/>'
    s = []
    s.append(rect(-25, -20, 110, "#dbe6f0", "#7a8ea3")); s.append(rect(0, 5, 110, "#dbe6f0", "#7a8ea3")); s.append(rect(19, 24, 60, "#dbe6f0", "#7a8ea3"))
    s.append(rect(-46, 36.3, 8, "#7d8186"))
    s.append(rect(-44.5, -25.5, 35.7, "#c9ccd1")); s.append(rect(-19.5, -0.5, 35.7, "#c9ccd1")); s.append(rect(25, 34.8, 40, "#c9ccd1"))
    for z0, z1 in ((-25, -20), (0, 5), (19, 24)): s.append(rect(z0, z1, 16, "#9aa0a6"))
    s.append(rect(-0.5, 0, 11, "#e07a2e", "#9a4a10")); s.append(rect(24, 25, 11, "#e07a2e", "#9a4a10"))
    for zc in (-35, -10, 29.9): s.append(rect(zc-1.25, zc+1.25, 24, "#c85d1a", "#7a3a0e"))
    def lab(x, y, text, anchor="middle", col="#111", size=10.5):
        return f'<text x="{x:.1f}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{col}">{html.escape(text)}</text>'
    def lead(z, y1, y2): return f'<line x1="{X(z):.1f}" y1="{y1}" x2="{X(z):.1f}" y2="{y2}" stroke="#555" stroke-width="0.7"/>'
    wt = cy - 35.7; pt = cy - 55; wb = cy + 35.7
    s.append(f'<line x1="{X(-25)}" y1="14" x2="{X(5)}" y2="14" stroke="#c85d1a" stroke-width="0.9" marker-start="url(#a)" marker-end="url(#a)"/>')
    s.append(lab(X(-10), 10, "lane 20.0 between the plate faces = wheel 19 + shim 0.5 + gap 0.5", "middle", "#c85d1a", 10))
    s += [lead(-10, wt-1, 34), lab(X(-10), 30, "Front hinge wheel, pinned FIRST: it locates the shaft"),
          lead(-35, wt-1, 50), lab(X(-35), 46, "Rear hinge wheel, pinned"),
          lead(29.9, cy-40, 50), lab(X(29.9), 46, "Stage-2 pulley, 2 set screws in seats"),
          lead(-22.5, pt-1, 68), lab(X(-22.5), 64, "P2 plate, 688 bearing"),
          lead(2.5, pt-1, 68), lab(X(2.5), 64, "P1 plate, 688"),
          lead(21.5, cy-30, 68), lab(X(21.5), 64, "P17 support, 688"),
          lead(-25.25, wb+1, cy+58), lab(X(-25.25)+4, cy+62, "0.3 to 0.5 gap, rear wheel to the P2 bearing", "start"),
          lead(-19.75, wb+1, cy+76), lab(X(-19.75)+4, cy+80, "0.3 to 0.5 feeler gap, front wheel to the P2 bearing", "start"),
          lead(-0.25, cy+11, cy+94), lab(X(-0.25)-4, cy+98, "0.5 shim against the P1 bearing", "end"),
          lead(24.5, cy+11, cy+94), lab(X(24.5)+4, cy+98, "1 mm shim against the P17 bearing", "start"),
          lab(X(-46), cy+118, "shaft end 1.5 mm proud of the wheel face", "start"), lab(X(36.3), cy+118, "1.5 mm proud of the pulley face", "end"),
          lab(X(-5), cy+138, "Plain round shaft Ø8 h7, 82.3 long (side A; side B is 77.3).", "middle"),
          lab(X(-5), cy+152, "Three Ø2.5 spring pins at mid-face, driven flush. No flats, no grooves, no E-clips.", "middle"),
          lab(X(-48), cy+172, "OUTSIDE the machine", "start", "#555"), lab(X(37), cy+172, "INBOARD, towards the middle", "end", "#555")]
    body = "\n".join(s)
    return f'''<figure><svg viewBox="0 0 740 330" role="img" aria-label="What sits on the hinge shaft, in order, with the shims, gaps and pins" style="width:100%;height:auto"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0,3 L6,0 L6,6 z" fill="#c85d1a"/></marker></defs>{body}</svg>
<figcaption><b>Fig. 2</b> One hinge shaft seen from above, side A, drawn to scale along the shaft. Everything that must not move is pinned to the shaft; the shaft itself is held by the pinned front wheel sitting between the P1 and P2 bearings.</figcaption></figure>'''

def svg_tensioner():
    sc = 8.0; x0 = 262; y0 = 200
    X = lambda x: x0 + (x - 200) * sc
    Y = lambda y: y0 - y * sc
    def rect(xa, ya, xb, yb, fill, stroke="#333", rx=0):
        return f'<rect x="{X(xa):.1f}" y="{Y(yb):.1f}" width="{(xb-xa)*sc:.1f}" height="{(yb-ya)*sc:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="0.8"/>'
    s = []
    s.append(rect(200, -22, 240.2, 22, "#dbe6f0", "#7a8ea3"))
    s.append(rect(200, -8.3, 207, 8.3, "#eceae3", "#8a877d"))
    s.append(rect(200, 6.8, 204, 8.3, "#e07a2e", "#9a4a10")); s.append(rect(200, -8.3, 204, -6.8, "#e07a2e", "#9a4a10"))
    s.append(rect(216.35, -4.05, 236.65, 4.05, "#fff", "#333", rx=32))
    s.append(rect(219, -13, 227, 6, "#e9a06a", "#9a4a10")); s.append(rect(219, -13, 227, -10, "#c85d1a", "#7a3a0e"))
    pts = " ".join(f"{X(223 + 5.77*math.cos(math.radians(a))):.1f},{Y(5.77*math.sin(math.radians(a))):.1f}" for a in range(0, 360, 60))
    s.append(f'<polygon points="{pts}" fill="#b9bdc2" stroke="#333" stroke-width="0.8"/>')
    s.append(f'<circle cx="{X(223):.1f}" cy="{Y(0):.1f}" r="{3*sc:.1f}" fill="#8d9196" stroke="#333" stroke-width="0.8"/>')
    s.append(rect(215.5, -15, 218.5, 15, "#c85d1a", "#7a3a0e")); s.append(rect(218.5, 7, 226, 15, "#e9a06a", "#9a4a10"))
    s.append(f'<circle cx="{X(223):.1f}" cy="{Y(11):.1f}" r="{1.7*sc:.1f}" fill="#fff" stroke="#333" stroke-width="0.8"/>')
    s.append(rect(211.5, -12.75, 215.5, -9.25, "#7d8186")); s.append(rect(215.5, -12, 219, -10, "#9aa0a6"))
    s.append(f'<line x1="{X(223)}" y1="{Y(18.5)}" x2="{X(232.6)}" y2="{Y(18.5)}" stroke="#c85d1a" stroke-width="1" marker-end="url(#b)"/>')
    s.append(f'<text x="{X(227.8)}" y="{Y(20.3)}" font-size="10" text-anchor="middle" fill="#c85d1a">idler travel 223 to 232.6 = 9.6 mm (19 mm of loop)</text>')
    def lab(x, y, lines, anchor):
        t = f'<text x="{x}" y="{y}" font-size="10.5" fill="#111" text-anchor="{anchor}">'
        t += "".join(f'<tspan x="{x}" dy="{0 if k == 0 else 12.5}">{html.escape(l)}</tspan>' for k, l in enumerate(lines))
        return t + "</text>"
    def lead(xa, ya, xb, yb): return f'<line x1="{X(xa):.1f}" y1="{Y(ya):.1f}" x2="{xb}" y2="{yb}" stroke="#555" stroke-width="0.7"/>'
    L = 250; R = X(241) + 6
    s += [lead(217, 13, L, 62), lab(L-4, 60, ["Leg B of the tab stands off the plate,", "1.5 mm clear of the slot end:", "the nut never touches it"], "end"),
          lead(213.5, -11, L, 150), lab(L-4, 148, ["M4 x 20 jack screw through leg B:", "half a turn = 0.35 mm along the slot"], "end"),
          lead(220, -11.5, L, 222), lab(L-4, 220, ["The slider's foot, bent inboard:", "what the jack screw pushes"], "end"),
          lead(206, 7.5, L, 300), lab(L-4, 298, ["Rail (186) and carrier end at 204 to 207:", "the idler never comes in past 223"], "end"),
          lead(225, 11, R, 60), lab(R+4, 58, ["Ear of the tab on the plate face:", "M3 x 6 into the new tapped hole", "at (223, +11), Loctite 243"], "start"),
          lead(235, 2, R, 140), lab(R+4, 138, ["Slot 8.1 x 20.3 in the plate;", "the Ø8 shank of the shoulder", "screw slides in it"], "start"),
          lead(228, -3, R, 222), lab(R+4, 220, ["M6 nyloc on the shoulder screw:", "finger-tight while tensioning,", "7 N·m to lock"], "start"),
          lead(226, -7.5, R, 300), lab(R+4, 298, ["Slider: an 8 mm slice of angle", "on the screw's thread, in place", "of the M6 washer"], "start")]
    body = "\n".join(s)
    W = R + 250
    return f'''<figure><svg viewBox="0 0 {W:.0f} 390" role="img" aria-label="The tensioner at the nose end seen from inboard: tab, slider with foot, jack screw and the shoulder screw in its slot" style="width:100%;height:auto"><defs><marker id="b" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#c85d1a"/></marker></defs>{body}</svg>
<figcaption><b>Fig. 6</b> How the tensioner works, to scale: the inboard face of plate P1 at the nose end (the shoulder screw head and the idler wheel are on the far side). The tab is fixed to the plate; the jack screw turns in the tab and pushes the slider's foot; the slider sits on the shoulder screw, so the idler moves out along the slot and the loop tightens. The nut then locks the shoulder screw; the jack screw is backed off a quarter turn and carries nothing.</figcaption></figure>'''
