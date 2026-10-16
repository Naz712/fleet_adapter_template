# Interactive assembly viewer

`index.html` + `parts.b64.txt` + `parts.json`: a three.js page (libraries from the jsDelivr CDN) showing
Nhien's Rev B frame carrying the printed track (Rev B's stock belts are replaced by the track from
`track_running_shape`, placed on the same wheel centres): orbit, drag the Assemble slider to take the
unit apart and put it back together in its 11 build steps, bend the hinge, put it on the ES1 stairs, show
the drive train only or the frame and tracks only, click any part or joint number for what it does, how it
is fastened and where it comes from.

Attached parts ride with the part they are fixed to (bearings with their plate, rails with their plate,
posts, motors and tray with the deck), and each step moves in from the side it is really fitted from, so
parts never pass through each other while the slider moves.

The hinge slider stops where the real parts would touch, from a part-against-part sweep of the Rev B
geometry at 0.1° steps: nose-up at 0° (the front frame rests on the two foam up-stops B18 under the deck,
so Rev B bends nose-down only), and nose-down at 18.8° as drawn, where the top corner of the sector mount
angle P14 meets the nose end of deck slot H. "Deck slot H +3 mm" releases the swing to 40°, which is what
the slot needs. The front group that swings is the front plates, both 2020 bars, the sector gear P11 with
P14 and their screws, the P19 brackets, the rails with their hardware and the nose idlers.

Open it from a web server (not file://), e.g. `python3 -m http.server` in this folder, or use the
published artifact link in the chat. `parts.b64.txt` holds every solid as quantised 16-bit vertices, base64;
`parts.json` is the index (name, class, bounding box, position, across-width tier).
