# Interactive assembly viewer

`index.html` + `parts.bin` + `parts.json`: a three.js page (libraries from the jsDelivr CDN) showing
Nhien's Rev B assembly with the printed track: orbit, explode the near side, bend the hinge, step
through the build order, click any part for what it does, how it is fastened and where it comes from.
Open it from a web server (not file://), e.g. `python3 -m http.server` in this folder, or use the
published artifact link in the chat. `parts.bin` holds every solid as quantised 16-bit vertices;
`parts.json` is the index (name, class, bounding box, position, across-width tier).
