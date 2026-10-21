import html
import os
SP = os.path.dirname(os.path.abspath(__file__))   # run: python3 build.py && node topdf.mjs "$PWD"

from svgs import svg_shaft, svg_tensioner

CSS = '''
@page { size: A4; margin: 11mm 11mm 11mm 11mm }
@page land { size: A4 landscape; margin: 8mm 10mm 8mm 10mm }
.land { page: land } .land figure img { max-height: 186mm; width: auto; max-width: 100%; margin: 0 auto }
html, body { margin: 0; padding: 0 }
body { font: 9.4pt/1.32 "Helvetica Neue", Arial, "Liberation Sans", sans-serif; color: #111 }
h1 { font-size: 19pt; margin: 0 0 2mm; letter-spacing: -0.01em; padding-bottom: 1.5mm; border-bottom: 1.4px solid #c85d1a }
h2 { font-size: 12.5pt; margin: 5mm 0 1.5mm; color: #c85d1a; text-transform: uppercase; letter-spacing: 0.05em; break-after: avoid }
h3 { font-size: 10.2pt; margin: 3.5mm 0 1mm; break-after: avoid }
p { margin: 0 0 1.8mm } ul, ol { margin: 0 0 1.8mm; padding-left: 4.5mm } li { margin: 0 0 1mm }
b { font-weight: 700 }
.lead { font-size: 10pt }
figure { margin: 2mm 0 3mm; break-inside: avoid } figure img { display: block; width: 100%; border: 0.5px solid #cfcac0 }
figcaption { font-size: 8.3pt; color: #222; margin-top: 1mm; line-height: 1.3 }
.two { display: flex; gap: 4mm; align-items: flex-start } .two > * { flex: 1 1 0; min-width: 0 }
.box { border: 0.6px solid #c9c4ba; border-radius: 1.5mm; padding: 2mm 2.5mm; background: #faf8f3; margin: 1.5mm 0 3mm; break-inside: avoid }
.box b.t { display: block; color: #c85d1a; text-transform: uppercase; letter-spacing: 0.05em; font-size: 8.6pt; margin-bottom: 1mm }
table { border-collapse: collapse; width: 100%; font-size: 8.6pt; margin: 1mm 0 3mm } th { text-align: left; color: #c85d1a; border-bottom: 0.8px solid #c85d1a; padding: 0.8mm 1.5mm 0.8mm 0; font-size: 8.2pt; text-transform: uppercase; letter-spacing: 0.04em }
td { vertical-align: top; padding: 0.9mm 1.5mm 0.9mm 0; border-bottom: 0.4px solid #e2ddd3 } tr { break-inside: avoid }
.page { page-break-before: always } .apx h2 { margin-top: 0 }
.warn { border-left: 2.5px solid #c85d1a; padding-left: 2.5mm; margin: 2mm 0 3mm }
.small { font-size: 8.4pt; color: #333 }
'''

def fig(src, cap, cls=""):
    return f'<figure class="{cls}"><img src="img/{src}.jpg"><figcaption>{cap}</figcaption></figure>'
def sheet(src, title):
    return f'<div class="apx land"><h2>{title}</h2><figure><img src="img/{src}.jpg"></figure></div>\n'

H = []
H.append(f'<!doctype html><html><head><meta charset="utf-8"><title>Track unit assembly, in detail</title><style>{CSS}</style></head><body>')
H.append('''<h1>Track unit assembly, in detail</h1>
<p class="lead">Only the track side of the RB4107 1:5 carrier: the toothed wheels, how each one is fixed to its shaft, how the shaft is held in place, the idler wheels on their shoulder screws, the tensioner, and how the track loop goes on and is set. The frame, deck, drive train and electronics are left out; they are in the full plan. Everything here is for one side; the other side is the same, mirrored. Dimensions are in millimetres and come from the shared 3D model (Nhien's Rev B with the track added, reviewed 16 to 18 October 2026).</p>
<div class="two">''' + fig("cat_hinge_shaft", "<b>Fig. 1a</b> The hinge shaft of one side with its three toothed parts: rear hinge wheel outside the rear plate, front hinge wheel in the lane between the plates, stage-2 pulley inboard of the P17 support. This shaft is the drive shaft: the stage-2 belt turns it, the two wheels drive the two track loops.") + fig("zoom_nose", "<b>Fig. 1b</b> The nose end: idler wheel on its shoulder screw in the plate slot, the tensioner tab and slider, the rail ending short of the wheel.") + '''</div>
<h2>What is in one side's track unit</h2>
<table><tr><th>Part</th><th>Qty per side</th><th>What it does</th><th>How it is fixed</th></tr>
<tr><td>Hinge wheels, HTD 5M 20T for 15 mm belt, flanged, bore reamed 8 H7 (TS-06)</td><td>2</td><td>Drive the front and the rear track loops; the front one also locates the shaft</td><td>Ø2.5 spring pin through hub and shaft, at mid-face, flush</td></tr>
<tr><td>Stage-2 pulley M3 (MISUMI HTD 5M, 9 wide, with hub), bore 8</td><td>1</td><td>Brings the drive from the motor belt onto the shaft</td><td>Two cone-point set screws, each in a seat drilled 1 mm into the shaft, Loctite 243 (section 1.3)</td></tr>
<tr><td>Hinge shaft P20, Ø8 h7 plain round, A 82.3 / B 77.3</td><td>1</td><td>Carries the three parts above, turns in three 688 bearings</td><td>Held along its axis by the pinned front wheel between the P1 and P2 bearings; nothing else</td></tr>
<tr><td>Bearings 688-2RS (8 x 16 x 5) in P2, P1 and P17</td><td>3</td><td>The shaft turns in them</td><td>Pressed into seats laser-cut 15.8 and reamed 16 H7, Loctite 641</td></tr>
<tr><td>Shims 8 x 11: 0.5 (front wheel) and 1.0 (stage-2 pulley)</td><td>1 + 1</td><td>Keep the wheel and pulley faces off the bearings' outer rings</td><td>Trapped between the pinned part and the bearing's inner ring</td></tr>
<tr><td>Idler wheels, same HTD 5M 20T, bored 16 H7 for two 688s with an 8 x 10 x 9 sleeve</td><td>2 (nose, rear)</td><td>Free-running far wheel of each loop; the tensioner moves it</td><td>On an ISO 7379 Ø8 x 25 M6 shoulder screw through the plate slot</td></tr>
<tr><td>Shoulder screw set: head washer 8 x 11 x 1, 0.5 shim, slider TS-09, M6 nyloc</td><td>2 sets</td><td>The stub axle of the idler and its clamp</td><td>Nyloc 7 N·m once tensioned; slider replaces the washer under the nut</td></tr>
<tr><td>Tensioner tab TS-09 with M3 x 6 and M4 x 20 jack screw</td><td>2</td><td>Pushes the idler out along the slot and holds that position while the nut is tightened</td><td>M3 into the plate's new tapped hole at (±223, +11), Loctite 243</td></tr>
<tr><td>Track loops: bought HTD 550-5M-15 belt with 22 bonded cleats, 5 high (TS-01B; chosen 19 Oct). Fallback: printed TPU loop (TS-01)</td><td>2</td><td>The track</td><td>Teeth in the wheel grooves; tension only</td></tr>
<tr><td>Slide rails P3 to P6 (UHMW 186 x 20 x 5) on carrier angles TS-10</td><td>2 + 2 per segment</td><td>The runs slide on them so the loop stays straight under load</td><td>Carrier angle M3 x 6 into the plate (3 off), rail 3 x 5 thread-forming into the angle</td></tr>
</table>''')

# ---------- Section 1
H.append('''<div class="page"><h2>1. The hinge shaft and what is fixed to it</h2>
<p>Each side has one shaft. It is also the drive shaft, so three toothed parts turn with it: the rear hinge wheel (outside the rear plate P2), the front hinge wheel (in the 20 mm lane between P2 and the front plate P1) and the stage-2 pulley (inboard of the P17 support). The shaft runs in three 688 bearings, one in each of P2, P1 and P17. Fig. 2 shows the whole stack.</p>''')
H.append(svg_shaft())
H.append('''<h3>1.1 How each wheel and pulley is fixed to the shaft: the cross pin</h3>
<p>One ISO 8752 spring pin through the hub and the shaft (2.5 x 24 in the hinge wheels; the stage-2 pulley uses set screws instead, 1.3) at the middle of the toothed face, driven flush on both sides. The pin does two jobs at once: it makes the part turn with the shaft (torque goes through the pin in double shear, which carries many times the 60 N this drive puts on it), and it stops the part sliding along the shaft, because the pin is in the shaft too. Nothing else holds the wheels: no grub screw, no flat on the shaft, no E-clip groove.</p>
<p><b>Why not a set screw on the wheels.</b> The hinge wheels fill the 20 mm lane at 19 mm over their flanges with 0.5 mm each side, so they have no hub boss. A set screw would have to go through the toothed rim, under the track, with no way to reach it once the track is on. And on a plain round shaft a set screw holds only by friction: an M3 or M4 cup point gives about 1 to 1.5 N·m against 0.25 N·m running and 0.75 N·m in a shock, it works loose when the drive reverses, and its burr stops the shaft pulling back out through the bearings. The reviewer's set screw is right where there is a hub for it; that is the stage-2 pulley, in 1.3.</p>
<p><b>Why not a D-flat or an E-clip.</b> A flat fixes rotation but not position along the shaft, so the clips come back; a 70 mm milled flat weakens the shaft; an E-clip groove cuts the Ø8 shaft to Ø6 where it bends most. The pin hole sits beside a bearing where bending is small: an Ø8 shaft with a Ø2.5 hole keeps about half its section modulus and runs at about 40 MPa against a yield above 350 MPa.</p>
<h3>1.2 How the shaft is held in place along its axis</h3>
<p>The front hinge wheel is pinned first, sitting in the lane with its 0.5 mm shim against the P1 bearing's inner ring and a 0.3 to 0.5 mm feeler gap to the P2 bearing. Once that pin is in, the shaft cannot move more than the feeler gap in either direction, because the wheel is trapped between the two plate bearings and the shaft is pinned to the wheel. That is the whole axial location. The rear wheel and the stage-2 pulley are then pinned where they stand, each with its own small gap or shim to the bearing beside it, and the shaft ends stand 1.5 mm proud of the outer faces. The rear wheel is the part at the very end of the shaft: its pin is what keeps it there; nothing can walk off because nothing is free on the shaft.</p>
<p>Check after pinning: push and pull the front wheel; it moves only by the feeler gap. A strip of paper passes between every wheel face and the bearing's outer ring next to it; if it does not, the face rubs the ring and the bearing drags.</p>
<h3>1.3 The stage-2 pulley: set screws in seats (chosen 20 Oct)</h3>
<p>The stage-2 pulley is a bought MISUMI economy HTD 5M pulley for the 9 mm belt, with a hub, bore Ø8 and two tapped holes in the hub. Drilling a cross pin through its small toothed part was judged too fiddly, so the hub's set screws hold it instead. On a plain round shaft a set screw holds by friction only and slips when the drive reverses, so each screw gets a seat:</p>
<ul>
<li>Push the pulley and its 1 mm shim against the P17 bearing's inner ring.</li>
<li>Through each tapped hole, spot-drill the shaft about 1 mm deep with a drill that just passes the thread (Ø2.5 for M3, Ø3.3 for M4), in place.</li>
<li>Fit cone-point set screws with Loctite 243, about 1 N·m. The cone sits in the seat, so the screw takes the torque in bearing and holds the pulley along the shaft.</li>
</ul>
<p>The hub sticks out past the teeth, so the shaft has to run under it: the hub length is still to be confirmed with Nhien, and the shaft lengths (82.3 / 77.3) grow by it.</p>
<p>A screw right through the hub and the shaft (M3 x 30 with a nyloc through a Ø3.2 hole) also works and is removable with tools, as long as the head and the nut clear the belt and the P17 support as the pulley turns.</p>''')
H.append('''<div class="page"><h3>1.4 Procedure: pinning the three parts to the shaft (2 hours for both sides)</h3>
<p><b>What you are doing.</b> The pin hole through the shaft is drilled with the parts in place, because the wheels sit between the plates and the shaft only ever goes in through the bearings. The hole in each hub was drilled on the drill press beforehand (when the bore was reamed: Ø2.5 through both walls at mid-face, 9.5 from a flange face, centre-punched first) and now serves as the drill guide. That is what keeps a hand-drilled hole straight.</p>
<p><b>Tools.</b> Cordless drill with a sharp long-series Ø2.5 HSS bit (two new ones in the kit), cutting fluid, 2.5 mm pin punch and a small hammer, feeler gauges 0.3 and 0.5, the shims, two G-clamps, a marker, a strip of paper.</p>
<ol>
<li>The frame sits on the bench with its plates clamped down, no deck yet, so every hub hole is reachable from above. Mark each hub hole with the marker so you can find it when the wheel is in the lane.</li>
<li>Put the shaft in from outside, chamfered end first: through the rear wheel, the P2 bearing, the front wheel with its 0.5 shim on the P1 side, the P1 bearing, the P17 bearing, the 1 mm shim and the stage-2 pulley. Push until the outer end stands 1.5 mm proud of the rear wheel's outer face.</li>
<li><b>Front wheel first</b>, because it locates the whole shaft. Push the wheel and its shim gently against the P1 bearing. Slide the 0.3 feeler between the wheel's other face and the P2 bearing: it must go in with a light drag. The 0.5 must not. If the 0.5 goes in, the lane is too wide (check the bars); if the 0.3 will not, the lane is too narrow.</li>
<li>Turn the wheel so its hub hole points straight up. Hold it there by its flange; the shaft is free to turn, so make sure the hub hole and nothing else is what the drill meets.</li>
<li>Oil on the bit. Put the bit into the hub hole, sight along the plate so the drill is square to the shaft, and drill with steady pressure. You feel it cut aluminium for a moment, then steel; keep the speed moderate and let it cut. When it breaks through the far side of the shaft it enters the far hub hole: ease off. Pull out, clear the chips, blow out the hole.</li>
<li>Start a spring pin with the hammer, then drive it with the punch until it sits the same depth both sides, about 3 mm below the tooth roots. It must not stand up into a tooth space on either side, or the track will click over it.</li>
<li>Check: the shaft turns freely by hand with the wheel; pushing and pulling the wheel moves it only by the feeler gap; the strip of paper passes between the wheel face and the bearing's outer ring on both sides.</li>
<li><b>Rear wheel.</b> Slide it so the 0.3 feeler passes between its inner face and the P2 bearing and the 0.5 does not. Hub hole up, drill, pin, check.</li>
<li><b>Stage-2 pulley.</b> Push it and its 1 mm shim against the P17 bearing's inner ring. Through each tapped hole, spot-drill the shaft about 1 mm deep (1.3), then the two set screws with Loctite 243, about 1 N·m. Check.</li>
<li>Other side the same. Final check for the side: the shaft turns freely with its three parts; runout over the wheel teeth under 0.1 mm against a fixed pointer; the front frame still swings 0 to 35°.</li>
</ol>
<div class="warn"><p><b>Mistakes to avoid.</b> Drilling without the hub hole as a guide (the hole wanders, the pin is loose, the wheel knocks under load). Forgetting a shim before the shaft goes in (everything comes out again). Driving the pin too far (it pokes into the tooth space on the far side). A dull bit: a 2.5 mm drill that is not cutting steel within a few seconds is blunt; change it before it snaps.</p>
<p><b>If a pin ends up loose.</b> Drill a second pair of hub holes at 90° to the first on the drill press, with the wheel off on a spare piece of shaft, and pin again. On the assembled machine that means the shaft comes out, which is why the practice run on scrap (a spare wheel and 100 mm of spare shaft are in the order) is worth the hour.</p></div>
<div class="two">''' + fig("cat_pulley", "<b>Fig. 3</b> The hinge wheel as bought (MISUMI HTD 5M 20T for 15 mm belt, flanged), with the bore reamed 8 H7 and the Ø2.5 hub hole at mid-face.") + fig("r_hinge", "<b>Fig. 4</b> Solid-model check at the hinge: plates, bearings, wheels, shims and the pinned shaft, nothing touching that should not.") + '</div></div>')

H.append(sheet("TS-11", "Sheet TS-11: where every part sits along the hinge shaft and the idler screw, with the fits"))
H.append(sheet("EX-11", "How to read TS-11"))
H.append(sheet("TS-06", "Sheet TS-06: the toothed wheel, reamed bore and cross pin"))
H.append(sheet("EX-06", "How to read TS-06"))

# ---------- Section 2
H.append('''<div class="page"><h2>2. The idler wheels on their shoulder screws</h2>
<p>The far wheel of each loop (at the nose for the front segment, at the tail for the rear one) is an idler: it carries no drive, it only guides the loop and takes the tension. It turns on two 688 bearings on an ISO 7379 shoulder screw, Ø8 x 25 with an M6 thread, which passes through the slot in the plate. The screw is the idler's stub axle; the slot lets the axle move 9.6 mm along the plate for tensioning.</p>
<h3>2.1 The stack on the shoulder screw, from the head</h3>
<table><tr><th>Order</th><th>Part</th><th>Thickness</th><th>Why it is there</th></tr>
<tr><td>1</td><td>Head washer 8 x 11 x 1</td><td>1</td><td>Keeps the screw head off the bearing's outer ring; it bears on the inner ring only</td></tr>
<tr><td>2</td><td>Bearing 688-2RS, outer</td><td>5</td><td>Pressed in the wheel (bore 16 H7, light press)</td></tr>
<tr><td>3</td><td>Sleeve 8 x 10 x 9, aluminium</td><td>9</td><td>Between the two inner rings, so the nut can clamp them without squeezing the wheel</td></tr>
<tr><td>4</td><td>Bearing 688-2RS, inner</td><td>5</td><td>Second bearing: the wheel runs on two, no rock</td></tr>
<tr><td>5</td><td>Shim 8 x 11 x 0.5</td><td>0.5</td><td>Keeps the wheel's inner flange off the plate and the rail's carrier</td></tr>
<tr><td>6</td><td>Plate P1 or P2, through the slot 8.1 x 20.3</td><td>5</td><td>The Ø8 shank sits in the 8.1 slot with 0.1 to 0.15 clearance</td></tr>
<tr><td>7</td><td>Slider TS-09 (Ø6.4 hole on the thread)</td><td>3</td><td>Replaces the plain M6 washer; its foot is what the jack screw pushes</td></tr>
<tr><td>8</td><td>M6 nyloc nut</td><td>5</td><td>Clamps plate, shim and the two inner rings against the head at 7 N·m; the outer rings and the wheel stay free</td></tr>
</table>
<p>The stack on the 25 mm shoulder is 1 + 5 + 9 + 5 + 0.5 = 20.5, plus the 5 mm plate: the shoulder ends 0.5 mm inside the plate, so the nut tightens the inner-ring stack solid against the head and never pinches the wheel. With the 3 mm slider in place of the 1.6 mm washer, 1.5 mm of thread still shows past the nut. The wheel must spin free with the nut tight; if it does not, a bearing is seated crooked or the sleeve is missing.</p>
<h3>2.2 Where the idler can sit</h3>
<p>The slot runs from x 220.4 to 232.6 (screw centres, measured from the hinge axis). The rail ends at 207 and its carrier angle at 204, and the wheel's flange reaches 16 mm inboard of the screw centre, so the idler must never sit closer to the hinge than x 223 or the flange hits the rail end. The usable travel is therefore 223 to 232.6: 9.6 mm of axle movement, which takes up 19 mm of loop. Measured from the plate's nose end at x 240.2, that is 17.2 mm down to 7.6 mm.</p>
<div class="two">''' + fig("cat_shoulder", "<b>Fig. 5a</b> The idler set: shoulder screw, head washer, the two bearings with the sleeve between them, the 0.5 shim, the slider and the nyloc.") + fig("cat_tensioner", "<b>Fig. 5b</b> The tensioner set that goes with it: the tab with its ear and the jack screw, and the slider with its foot.") + '</div></div>')

# ---------- Section 3
H.append('''<div class="page"><h2>3. The tensioner: how it works</h2>
<p>The track loop is tight when the idler is pushed out along its slot. Rev B relied on the nut's friction alone to hold the idler wherever a hand had put it, which is why the reviewer said the track would be loose: nothing set the tension and nothing kept it. TS-09 adds a pusher and a lock at each idler, four sets per machine.</p>''')
H.append(svg_tensioner())
H.append('''<h3>3.1 The three parts</h3>
<ul>
<li><b>The tab.</b> A 30 mm length of 20 x 20 x 3 aluminium angle. One leg is cut back to a 7.5 x 8 ear that lies on the plate's inboard face and is screwed to it with an M3 x 6 into the new tapped hole at (±223, +11), Loctite 243, 1.0 N·m. The other leg, leg B, stands off the plate at right angles, 1.5 mm on the hinge side of the slot end, so the nut's corners never touch it as the idler travels. Leg B carries an M4 tapped hole at the height of the slider's foot (6 mm off the plate face, 11 mm below the slot centreline).</li>
<li><b>The slider.</b> An 8 mm wide slice of the same angle. Its 19 mm leg lies on the plate over the slot with a Ø6.4 hole 13 mm from its bottom, so it sits on the shoulder screw's M6 thread under the nut, in place of the plain washer. Its short leg, 8 mm, is bent inboard at the bottom: the foot.</li>
<li><b>The jack screw.</b> An M4 x 20 socket head screw through the tapped hole in leg B, tip against the foot, turned with a 3 mm key from the hinge side, under the bar.</li>
</ul>
<h3>3.2 What happens when you turn it</h3>
<p>The tab cannot move: it is screwed to the plate. The jack screw advances through leg B by 0.7 mm per turn (the M4 pitch), so each half turn pushes the foot, and with it the slider, the shoulder screw and the idler wheel, 0.35 mm outward along the slot. The loop passes over the idler, so pushing the idler out stretches the loop: 1 mm of idler travel takes up 2 mm of loop. When the deflection is right, the nyloc is tightened to 7 N·m with the screw head held by its 4 mm key: now the nut and the clamped stack hold the idler, by far more force than the belt pull. The jack screw is then backed off a quarter turn so that it carries no load, and stays there as the stop for the next re-tension.</p>
<h3>3.3 How tight is right, and how to measure it</h3>
<p>The rails sit directly under both runs of the loop, so pushing a run inward moves nothing and tells you nothing. Pull a run away from its rail instead: with the machine on blocks, hook a cleat of the lower run at mid-span (about 110 mm from either wheel) with a bent wire on a small spring scale and pull it away from the machine with 4 N, about 400 g, reading the movement against a steel rule held beside it. The printed TPU track should give 2 to 3 mm; the stiffer belt of option B, 1.5 to 2.5 mm. Less than that loads the bearings and makes a TPU loop creep faster; more than that and the teeth ride up under load and skip.</p>
<div class="two">''' + fig("tens3d", "<b>Fig. 7</b> The tensioner on the solid model, nose A, from inboard: tab standing off the plate (orange), jack screw on the slider's foot, shoulder screw and nut in the slot, carrier angle below.") + fig("ts09plan", "<b>Fig. 8</b> The same corner as drawn on TS-09, plan from inboard: slot, shoulder screw and nut, slider, tab with its ear and M3, jack screw on the foot, and the rail and carrier ending short of the wheel.") + '''</div>
<div class="box"><b class="t">Numbers to remember</b>Idler travel 223 to 232.6 (9.6 mm, 19 mm of loop). Half a turn of the jack screw = 0.35 mm. Deflection 2 to 3 mm (TPU) or 1.5 to 2.5 mm (belt) at 4 N on the lower run at mid-span. Nyloc 7 N·m with the screw head held. Jack screw backed off a quarter turn after locking. A TPU loop settles 1 to 2 % in its first days: re-check after the first run and after a day.</div></div>''')
H.append(sheet("TS-09", "Sheet TS-09: idler tensioner, tab, slider and jack screw"))
H.append(sheet("EX-09", "How to read TS-09"))

# ---------- Section 4
H.append('''<div class="page"><h2>4. Fitting the track loop and setting the tension</h2>
<p>This is assembly steps 10 and 11 of the plan, for one loop; four loops per machine, the two of one side set to the same feel. Before this, each belt has come back from the belt maker with its 22 cleats (5 high) and has been fit-checked on two wheels at 223 mm centres. (Fallback, the printed TPU loop: the fit-test slice and then the rings.)</p>
<h3>4.1 Parts for one loop</h3>
<p>The idler wheel with its two bearings and sleeve already pressed in; the shoulder screw, head washer 8 x 11 x 1, shim 8 x 11 x 0.5, slider, M6 nyloc; the tab with its M3 x 6 and M4 x 20 jack screw; the loop. Tools: 4 mm hex key (shoulder screw head), 10 mm spanner (nyloc), 2.5 mm key (M3), 3 mm key (jack screw), the hook and spring scale, a steel rule, Loctite 243.</p>
<h3>4.2 Procedure</h3>
<ol>
<li>Put the idler wheel inside the loop and hang the loop over the hinge wheel, teeth into the grooves, so the idler sits near its slot in the plate.</li>
<li>Build the shoulder screw stack from the head: head washer, through the idler's two bearings and sleeve, the 0.5 shim, through the plate slot, the slider with its foot pointing inboard and down, the nyloc finger-tight only. Push the idler toward the hinge until the screw sits at x 223: that is 17.2 mm from the plate's nose end, and no closer, because the rail ends there.</li>
<li>Fit the tab: ear onto the plate's tapped hole with the M3 x 6 and a drop of 243, 1.0 N·m. Leg B stands 1.5 mm off the slot end on the hinge side. Run the M4 jack screw through the tapped leg until its tip touches the slider's foot.</li>
<li>Turn the jack screw clockwise in half turns. Each half turn moves the idler 0.35 mm outward. After each, pull the lower run with the hook and scale at mid-span and read how far it comes away from the rail. Stop at 2 to 3 mm (TPU) or 1.5 to 2.5 mm (belt).</li>
<li>Lock it: 4 mm key in the shoulder screw head so it cannot turn, 10 mm spanner on the nyloc, 7 N·m (snug plus a quarter turn with the long leg of the key is close). The nut clamps the plate between the slider and the shim.</li>
<li>Back the jack screw off a quarter turn so it carries no load; the nut holds the position now.</li>
<li>Turn the loop one full turn by hand. Listen: no clicks (a click is a tooth riding up or a pin standing proud). Look: the 5 mm cleats clear the deck underside by about 3 mm (no notch), the loop runs centrally between the flanges without walking, the flanges clear the rail end by at least 2 mm and the bar end by 3.7.</li>
<li>Do the other loop of the same side to the same deflection, then the other side.</li>
<li>Re-check the deflection after the first run and again after a day. A new belt settles a little (a TPU loop more); if it reads over 2.5 mm (TPU: 3 mm), loosen the nut, half a turn on the jack screw, tighten again. That is the whole re-tensioning job.</li>
</ol>
<h3>4.3 Checks before the first run</h3>
<ul>
<li>Shoulder screw centre between 223 and 232.6, measured from the plate's nose end as 17.2 down to 7.6 mm.</li>
<li>The idler spins free with the nut tight; the hinge wheel turns the loop by hand with no tight spot once a turn (a tight spot means a pin proud or a bearing crooked).</li>
<li>Each side on blocks under power: no tooth jump when the loop is braked by hand.</li>
</ul>
<div class="two">''' + fig("cat_track", "<b>Fig. 9</b> The loop. Chosen: a bought HTD 550-5M-15 belt with 22 bonded cleats, 5 high. Fallback: the printed TPU track, 110 HTD 5M teeth inside, 45 cleats outside.") + fig("seq85", "<b>Fig. 10</b> Steps 8 to 10 in the interactive model: the idlers go on last, through the plate slots, with the sliders, nuts and tabs.") + '</div></div>')
H.append(sheet("TS-01B", "Sheet TS-01B: the bought belt with 5 mm cleats (chosen)"))

# ---------- Section 5
H.append('''<div class="page"><h2>5. What the runs slide on: rails and carrier angles</h2>
<p>Between the two wheels of a segment the loop would sag and the teeth would climb under load, so each run slides on a UHMW rail, 186 x 20 x 5, one above and one below, on each plate. The rails sit 13.3 mm from the shaft axis, just under the tooth tips, which is why the tension check pulls a run away from the rail instead of pushing it.</p>
<p>Rev B held each rail with four small clips; the reviewer called the contact area too small. TS-10 replaces them with a full-length 10 x 10 x 1.5 aluminium angle per rail: one leg on the plate face, screwed with three M3 x 6 into new tapped holes at x 40, 105 and 170 (y ±3.5), Loctite 243, 1.0 N·m; the other leg under the upper rail or on top of the lower rail, with the rail screwed to it by three 3 x 5 thread-forming screws into blind pilots 4 deep, at 20, 93 and 166 from the rail's hinge end (x 38, 111, 184) and 7.5 from the plate face: the rail is only 5 mm thick and its far face is what the track slides on, so a longer screw would come out of it. The plate leg is cut down to 6.5 mm so the upper and lower angles do not meet on the plate's centreline. The rails are trimmed from 189 to 186 so the idler's flange clears them at x 223. Do not drill the old clip pilots in the rails: they overlap the new ones at x 38 / 40 and 184 / 185.</p>
''' + fig("cat_carrier", "<b>Fig. 11</b> A rail on its carrier angle on the plate face, from the interactive model.") + '</div>')
H.append(sheet("TS-10", "Sheet TS-10: rail carrier angle"))

# ---------- Section 6
H.append('''<div class="page"><h2>6. Order of work for the track side, and what to have on the bench</h2>
<table><tr><th>When</th><th>Step</th><th>Time</th><th>Go / no-go check</th></tr>
<tr><td>Before build day</td><td>Hinge wheels (bought bored Ø8) with their Ø2.5 holes drilled; stage-2 pulleys bought bored Ø8; 4 idler wheels back from the workshop bored 16 H7. Shaft cut to 82.3 and 77.3, ends chamfered. Tabs, sliders, carrier angles made; rails trimmed and drilled. Loops fit-checked on two wheels at 223 centres.</td><td>workshop 1 to 2 weeks; 4 h of own work</td><td>Shaft slides through every reamed bore with no shake and no stiff spot; a 688 enters the idler bore with a light press and does not fall out</td></tr>
<tr><td>Step 1</td><td>Press the 688s: into P1, P2 and P17 (Loctite 641 on the outer ring), and two into each idler wheel with the sleeve between</td><td>30 min, then cure</td><td>An idler on its bearings spins free with no rock</td></tr>
<tr><td>Steps 3 and 5</td><td>Rails on their carrier angles, angles onto the plates</td><td>30 min each</td><td>Angle lies flat with no rock; rail ends at 207</td></tr>
<tr><td>Step 6</td><td>Hinge wheels and stage-2 pulley held in position with their shims</td><td>20 min</td><td>The bare shaft enters each wheel from the bearing without lifting it</td></tr>
<tr><td>Step 7</td><td>Shafts in, feeler gaps set, three pins per side (section 1.4)</td><td>2 h both sides</td><td>Shaft turns free; axial play = feeler gap only; paper passes at every face</td></tr>
<tr><td>Step 10</td><td>Idlers on their shoulder screws through the slots, sliders, nuts finger-tight, tabs on (section 4.2, 1 to 3)</td><td>40 min for four</td><td>Wheel spins free on the loose screw; jack screw meets the foot squarely</td></tr>
<tr><td>Step 11</td><td>Loops on, tensioned, locked (section 4.2, 4 to 9)</td><td>30 min for four</td><td>Deflection in range; one full turn by hand with no click; nut 7 N·m</td></tr>
</table>
<h3>Fasteners for these joints</h3>
<table><tr><th>Joint</th><th>Fastener</th><th>Qty per machine</th><th>Torque</th><th>Thread-locker</th></tr>
<tr><td>Hinge wheels and stage-2 pulleys to the shafts</td><td>ISO 8752 spring pins 2.5 x 24 (hinge wheels); two cone-point set screws per stage-2 pulley, in seats</td><td>4 pins + 4 screws</td><td>pins driven flush; set screws about 1 N·m</td><td>243 on the set screws</td></tr>
<tr><td>Idlers</td><td>ISO 7379 Ø8 x 25 M6 shoulder screw; 8 x 11 x 1 head washer; 8 x 11 x 0.5 shim; sleeve 8 x 10 x 9; slider; M6 nyloc</td><td>4 sets</td><td>7 N·m</td><td>none</td></tr>
<tr><td>Tensioner tabs</td><td>M3 x 6 SHCS into the plate; M4 x 20 jack screw</td><td>4 + 4</td><td>1.0 N·m / by feel, backed off a quarter turn</td><td>243 on the M3</td></tr>
<tr><td>Rail carriers to plates</td><td>3 x M3 x 6 SHCS per angle</td><td>24</td><td>1.0 N·m</td><td>243</td></tr>
<tr><td>Rails to carriers</td><td>3 x 3 x 5 thread-forming per rail, blind pilots</td><td>24</td><td>seat the head, no more</td><td>none</td></tr>
<tr><td>Bearings in P1, P2, P17</td><td>688-2RS pressed, seat reamed 16 H7</td><td>6</td><td>press</td><td>641 on the outer ring</td></tr>
</table>
<h3>Tools for these steps</h3>
<p>Arbor press or a vice with soft jaws (bearings); cordless drill, long-series Ø2.5 HSS bits x2, cutting fluid, 2.5 pin punch, small hammer; feeler gauges 0.3 and 0.5; hex keys 2.5, 3 and 4; 10 mm spanner; torque screwdriver to 1 N·m and a torque wrench to 7 N·m if available (otherwise the feel described); digital calipers; steel rule; a bent-wire hook and a spring scale reading 4 N; two G-clamps; Loctite 641 and 243; marker; a strip of paper.</p>
<p class="small">Sources: the manufacturing and assembly plan (sections 5.3 to 5.8, 7 steps 6, 7, 10, 11, and procedures 8.2 and 8.3), sheets TS-01, TS-06, TS-09, TS-10 and TS-11 with their explainer pages, and the shared 3D model. Decisions on set screws and the sector gear: plan Appendix C, items 12, 13, 16 and 17.</p></div>''')
H.append('</body></html>')
open(SP + "/index.html", "w").write("\n".join(H)); print("html written")
