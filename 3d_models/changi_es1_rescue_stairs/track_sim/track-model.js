// Quasi-static model of a two-part (hinged) track and a one-piece track on the
// Changi AES "ES1" rescue stairs, carrying a casualty in a reclining seat. For every
// position along the stairs it works out how the track units rest on the real step
// nosings, then checks support, clearance, hinge angle, seat tilt and tipping.
// Units: metres, kilograms and radians.
//
// Works in Node (module.exports) and in the browser (window.TrackModel).
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.TrackModel = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const STAIRS = { rise: 0.17, going: 0.28, lowerTreads: 18, landing: 1.0, topPlatform: 2.8 };

  const DEFAULTS = {
    height: 8.4, // top platform setting, m
    rise: 0.17, // step rise, m
    going: 0.28, // step going (tread depth), m
    unitLength: 0.7, // sprocket centre to sprocket centre, per unit
    sprocketRadius: 0.09,
    unitMass: 25,
    personMass: 120,
    chairMass: 25, // stretcher-chair, levelling drive and mast
    reclineDeg: 45, // backrest from vertical: about 15 sitting up, 90 lying flat
    seatHeight: 0.5, // levelling pivot above the hinge axle (mast length)
    vehicleWidth: 0.75, // across the outer edges of the left and right tracks
    levelSeat: true, // a driven pivot keeps the seat level
    levelLimitDeg: 40,
    levelRateDegPerM: 150, // how fast the pivot can re-level, per metre travelled
    hingeLimitDeg: 55,
    hingeRateDegPerM: 120, // how fast the hinge actuator can bend, per metre travelled
    // 'moving': the hinges bend while the vehicle drives, each only so fast per metre travelled.
    // 'stopGo': the vehicle stops wherever the hinges (or the levelling) need to move, so they reach
    // any shape on the spot; a hinge then moves towards the shape that keeps every section on the
    // stairs only as far as leaves the vehicle a safe lean, and otherwise holds its bend until more
    // track is on the stairs.
    bendMode: 'moving',
    stopGoSafeDeg: 10, // stopGo: a hinge move must leave at least this lean (or no less than holding still)
    // stopGo: a laser at the leading end of the track looks straight down. While a platform edge lies
    // between the seat's hinge and that end, the vehicle drives on with its hinges held until the
    // laser sees the stairs this many risers lower than usual; then it stops and bends. null: no laser.
    laserRisers: null,
    // How the hinges reach for the stairs at an edge. 'lift': a hinge may lift the vehicle so a track
    // end reaches the stairs early (both ends down, the middle up). 'lie': every section lies on the
    // stairs about its inner hinge and no hinge is lifted off them; a section past an edge stays
    // straight until its hinge is near enough the edge to bend it down onto the steps. 'touch' (a stiff
    // main track and an arm on its leading axle): the main track rests on the stairs by its own weight
    // and the arm swings, down or up, until it just touches the stairs ahead.
    reach: 'lift',
    maxLift: 0, // reach 'lie': the most a hinge may lift the vehicle off the stairs to put a track end down, m
    armUpDeg: null, // reach 'touch': how far the arm can swing up before the platform is in the way (null: hingeLimitDeg)
    dirs: null, // only these directions, e.g. ['up'] (null: both)
    speed: 0.25, // m/s: only used to turn rates per metre into rates per second
    comOffset: 0, // person shifted along the seat, m (+ towards the head)
    seatBias: 0.15, // the seat's load centre set this far towards the head from the post, m
    mastMode: 'balance', // 'balance': a drive at the arm's foot leans it to keep the weight
    // furthest from tipping; 'average': arm held halfway between the units; 'upright': kept vertical;
    // 'base': no arm, the seat's levelling pivot sits on top of the centre box (seatHeight above the
    // hinge axle), square to the section the box is bolted to
    armLimitDeg: 50, // balance arm: lean either way from halfway between the units
    armRateDegPerM: 60, // balance arm: how fast its drive turns, per metre travelled
    armLockDeg: null, // balance arm drive seized at this lean from halfway (a failure), or null
    // mastMode 'twoArm': an arm on each track unit carries a level cradle between them
    twoArmBase: 0.25, // each arm's foot, this far from the hinge along its unit, m
    twoArmBaseUp: 0.12, // and this far above the unit's axle line (on its frame), m
    twoArmLen: 0.55, // arm length, foot pivot to cradle pin, m
    twoArmSlide: 0.4, // the front pin slides this far either way along the cradle, m
    twoArmRateDegPerM: 90, // how fast each arm drive turns, per metre travelled
    twoArmLock: null, // 'rear' or 'front': that arm's drive has seized (a failure)
    // More sections: one half kept whole and the other split in two, for example.
    sections: null, // section lengths rear to front; null = two sections of unitLength
    mainJoint: 1, // the hinge that carries the seat, counted from the rear
    extraHingeMass: 6, // kg of motor at each extra hinge
    // centre box for the battery and drive motor, bolted to the section just behind the seat's hinge (both
    // halves split): m from the seat's hinge axle, along that section and square to it. It clears the stairs,
    // the seat, the person and the other sections at every pose of the four-section chain (blueprint sheet C).
    box: { back: 0.29, front: 0.21, floor: 0.04, top: 0.29, width: 0.3 },
    boxMass: 0, // kg in the centre box
    boxCom: [-0.04, 0.165], // m from the seat's hinge axle to the box's centre of mass, along and square to that section
    extraHingeRateDegPerM: null, // how fast the extra hinges bend; null = the main hinge's rate scaled up for a shorter section (twice as fast for half the length)
    extraHingeSeized: false, // the extra hinges have seized straight (a failure)
    mainHingeSeized: false, // the seat's hinge has seized straight, the others still work (a failure)
    trailMode: 'wrap', // a split trailing half: 'wrap' (bends over edges, may be held straight while the seat's hinge is lifted), 'settle', 'straight' or 'nearest' (whichever the hinges reach sooner)
    leadMode: 'droop', // a split leading half: 'droop' (held in line as one unit, except that its end section is let down onto the stairs about its own hinge to keep contact), 'straight' (held in line) or 'split' (its end section folds first, lifting the section inside it)
    hingeControl: 'lead', // several hinges: 'lead' (the seat's hinge leads, the others keep up), 'together' or 'own'
    // mastMode 'vArms': two arms rising from the hinge in a V, feet on the averaging post
    vArmFoot: 0.06, // each foot this far fore or aft of the hinge, m
    vArmLen: 0.5, // arm length, m
    vArmPins: 0.25, // cradle pins nominally twice this apart, m
    vArmSlide: 0.2, // the front pin slides this far either way, m
    levelLockDeg: null, // levelling drive frozen at this angle (a failure), or null
  };

  // the stairs: ES1 by default; lowerTreads (and topPlatform) can be set for other stairs,
  // e.g. one flight of lowerTreads + 1 risers with height (lowerTreads + 1) x rise
  const stairsOf = (o) => Object.assign({}, STAIRS, { rise: o.rise, going: o.going },
    o.lowerTreads != null ? { lowerTreads: o.lowerTreads } : {}, o.topPlatform != null ? { topPlatform: o.topPlatform } : {});
  const deg = (r) => (r * 180) / Math.PI;
  const rad = (d) => (d * Math.PI) / 180;
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const G = 9.81;

  // ------------------------------------------------------------ casualty seat
  // A reclining stretcher-chair on a levelling pivot at the top of a mast over the
  // hinge. Seat frame: u forward (uphill, towards the head), v up, origin at the
  // pivot. The person lies back with the head uphill and the feet downhill, the way
  // casualties are carried on stairs. Body: a 1.80 m adult, segment masses from
  // standard anthropometric tables. Every part is a capsule (a segment grown by r).
  const SEAT = { board: 0.03, bracket: 0.05, thigh: 0.48, shank: 0.5, torso: 0.5 };
  function seatModel(o) {
    const key = `${o.reclineDeg}|${o.personMass}|${o.chairMass}|${o.comOffset}|${o.seatBias}`;
    if (o._seat && o._seat.key === key) return o._seat;
    const al = rad(o.reclineDeg);
    const sg = rad(10 * clamp((90 - o.reclineDeg) / 30, 0, 1)); // thighs a little raised, flat when lying
    const gm = rad(clamp(80 - 1.2 * o.reclineDeg, 0, 70)); // lower legs hang down when sitting up
    const V = (u, v) => ({ u, v });
    const at = (A, d, k, n, j = 0) => V(A.u + d.u * k + (n ? n.u * j : 0), A.v + d.v * k + (n ? n.v * j : 0));
    const dot = (a, b) => a.u * b.u + a.v * b.v;
    const b = V(Math.sin(al), Math.cos(al)), bn = V(-Math.cos(al), Math.sin(al)); // backrest, towards the chest
    const t = V(-Math.cos(sg), Math.sin(sg)), tn = V(Math.sin(sg), Math.cos(sg)); // seat, up
    const l = V(-Math.cos(gm), -Math.sin(gm)), ln = V(-Math.sin(gm), Math.cos(gm)); // leg rest, towards the shins
    const w = SEAT.board, rT = 0.13, rH = 0.1, rTh = 0.085, rS = 0.06, rF = 0.045;
    const C = V(0, 0), K = at(C, t, SEAT.thigh);
    const sT = (w + rTh) * dot(tn, b); // torso starts level with the top of the thigh
    const sS = (w + rTh) * dot(tn, l); // shank starts level with the end of the thigh
    const ankle = at(K, l, 0.46, ln, w + rS);
    const parts = [
      { kind: 'chair', name: 'backrest', a: C, b: at(C, b, sT + SEAT.torso + 0.3), r: w },
      { kind: 'chair', name: 'seat', a: C, b: K, r: w },
      { kind: 'chair', name: 'leg rest', a: K, b: at(K, l, SEAT.shank), r: w },
      { kind: 'body', name: 'thigh', a: at(C, t, 0, tn, w + rTh), b: at(K, t, 0, tn, w + rTh), r: rTh },
      { kind: 'body', name: 'shank', a: at(K, l, sS, ln, w + rS), b: ankle, r: rS },
      { kind: 'body', name: 'foot', a: ankle, b: at(ankle, ln, 0.16), r: rF },
      { kind: 'body', name: 'torso', a: at(C, b, sT, bn, w + rT), b: at(C, b, sT + SEAT.torso, bn, w + rT), r: rT },
    ];
    const hc = at(C, b, sT + SEAT.torso + 0.17, bn, w + rH);
    parts.push({ kind: 'body', name: 'head', a: hc, b: hc, r: rH });
    const pt = (name, k) => { const q = parts.find((x) => x.name === name); return V(q.a.u + (q.b.u - q.a.u) * k, q.a.v + (q.b.v - q.a.v) * k); };
    const mp = o.personMass, mc = o.chairMass;
    const boards = parts.filter((q) => q.kind === 'chair');
    const lens = boards.map((q) => Math.hypot(q.b.u - q.a.u, q.b.v - q.a.v));
    const lsum = lens.reduce((x, y) => x + y, 0);
    const masses = [
      { p: pt('head', 0), m: 0.081 * mp }, { p: pt('torso', 0.45), m: 0.597 * mp }, { p: pt('thigh', 0.5), m: 0.2 * mp },
      { p: pt('shank', 0.45), m: 0.093 * mp }, { p: pt('foot', 0.5), m: 0.029 * mp },
      ...boards.map((q, i) => ({ p: V((q.a.u + q.b.u) / 2, (q.a.v + q.b.v) / 2), m: (0.6 * mc * lens[i]) / lsum })),
    ];
    // Place the chair so its centre of mass sits straight above the pivot, with the
    // seat board a bracket's height above it. The drive and mast (40 %) sit at the pivot.
    let mu = 0, su = 0, sv = 0;
    for (const q of masses) { mu += q.m; su += q.m * q.p.u; sv += q.m * q.p.v; }
    const du = -su / mu + (o.seatBias || 0), dv = w + SEAT.bracket, off = o.comOffset || 0;
    const mv = (p, k) => V(p.u + du + k, p.v + dv);
    for (const q of parts) { const k = q.kind === 'body' ? off : 0; q.a = mv(q.a, k); q.b = mv(q.b, k); }
    masses.forEach((q, i) => { q.p = mv(q.p, i < 5 ? off : 0); }); // the first five are the person
    masses.push({ p: V(0, 0), m: 0.4 * mc });
    let M = 0, cu = 0, cv = 0;
    for (const q of masses) { M += q.m; cu += q.m * q.p.u; cv += q.m * q.p.v; }
    const out = { key, parts, masses, mass: M, com: V(cu / M, cv / M), person: mp,
      recline: o.reclineDeg, thighDeg: deg(sg), legDeg: deg(gm) };
    o._seat = out;
    return out;
  }

  // Seat parts in world coordinates for pose p (pivot p.P, seat tilted by p.phi).
  function placeSeat(o, p) {
    const s = seatModel(o), c = Math.cos(p.phi), sn = Math.sin(p.phi);
    const W = (q) => ({ x: p.P.x + q.u * c - q.v * sn, z: p.P.z + q.u * sn + q.v * c });
    return s.parts.map((q) => { const A = W(q.a), B = W(q.b); return { kind: q.kind, name: q.name, r: q.r, ax: A.x, az: A.z, bx: B.x, bz: B.z }; });
  }

  // ---------------------------------------------------------------- stairs
  function stairProfile(height, st = STAIRS) {
    const { rise: r, going: g, lowerTreads: n, landing } = st;
    const zL = (n + 1) * r;
    const xL0 = n * g;
    const xL1 = xL0 + landing;
    const nUp = Math.max(0, Math.round((height - zL) / r));
    const rUp = nUp ? (height - zL) / nUp : 0;
    const H = zL + nUp * rUp;
    const xP0 = xL1 + Math.max(nUp - 1, 0) * g;
    const xP1 = xP0 + st.topPlatform;
    const pts = [[-6, 0], [0, 0]];
    for (let i = 1; i <= n; i++) pts.push([(i - 1) * g, i * r], [i * g, i * r]);
    pts.push([xL0, zL], [xL1, zL]);
    for (let j = 1; j <= nUp; j++) {
      const x = xL1 + (j - 1) * g;
      pts.push([x, zL + j * rUp]);
      if (j < nUp) pts.push([x + g, zL + j * rUp]);
    }
    pts.push([xP1 + 6, H]);
    const clean = [];
    for (const p of pts) {
      const q = clean[clean.length - 1];
      if (!q || Math.hypot(p[0] - q[0], p[1] - q[1]) > 1e-9) clean.push(p);
    }
    // A track at least two nosings long rides on the line from nosing to nosing and
    // bridges the gaps between steps.
    // pitch: that line carried down to the floor at the foot of each flight (the path
    //        of the hinge, which cuts the corner between floor and first step);
    // ride:  the same line but with the real floor and first riser (the path of the
    //        outer track ends, which cannot rest on thin air in front of a riser).
    const pitch = [[-6, 0], [-g, 0], [xL0, zL]];
    const ride = [[-6, 0], [0, 0], [0, r], [xL0, zL], [xL1, zL]];
    if (nUp) { pitch.push([xL1 - g, zL], [xP0, H]); ride.push([xL1, zL + rUp], [xP0, H]); }
    pitch.push([xP1 + 6, H]);
    ride.push([xP1 + 6, H]);
    return {
      pts: clean, pitch, ride, H, zL, xL0, xL1, xP0, xP1, nUp, rUp,
      pitchLower: Math.atan2(r, g), pitchUpper: nUp ? Math.atan2(rUp, g) : 0,
      edges: [
        // convex corners where the slope flattens (the risky "crest" points)
        { x: xL0, z: zL, kind: 'crest', name: 'mid platform edge' },
        ...(nUp ? [{ x: xP0, z: H, kind: 'crest', name: 'top platform edge' }] : []),
      ],
    };
  }

  // Terrain helper: vertices + edges with outward normals, sorted by x, plus a mirror copy.
  function buildTerrain(pts) {
    const V = pts.map((p) => ({ x: p[0], z: p[1], convex: false }));
    for (let i = 1; i < V.length - 1; i++) {
      const ax = V[i].x - V[i - 1].x, az = V[i].z - V[i - 1].z;
      const bx = V[i + 1].x - V[i].x, bz = V[i + 1].z - V[i].z;
      V[i].convex = ax * bz - az * bx < -1e-12; // right turn = outside corner (a nosing)
    }
    const E = [];
    for (let i = 0; i < V.length - 1; i++) {
      const A = V[i], B = V[i + 1];
      const ex = B.x - A.x, ez = B.z - A.z, len = Math.hypot(ex, ez);
      E.push({ A, B, ex, ez, len2: ex * ex + ez * ez, nx: -ez / len, nz: ex / len,
        x0: Math.min(A.x, B.x), x1: Math.max(A.x, B.x) });
    }
    return { V, E };
  }

  function makeTerrain(profile) {
    const t = buildTerrain(profile.pts);
    const mirrored = buildTerrain(profile.pts.map((p) => [-p[0], p[1]]).reverse());
    t.mirror = mirrored;
    return t;
  }

  // Highest ground level at x (risers count as their top).
  function groundZ(T, x) {
    let z = -Infinity;
    for (const e of T.E) {
      if (x < e.x0 - 1e-12 || x > e.x1 + 1e-12) continue;
      if (Math.abs(e.ex) < 1e-12) z = Math.max(z, e.A.z, e.B.z);
      else z = Math.max(z, e.A.z + ((x - e.A.x) / e.ex) * e.ez);
    }
    return z;
  }

  // Lowest height at x where a sprocket of radius rho clears the stairs.
  function clearanceZ(T, x, rho) {
    let z = -Infinity;
    for (const v of T.V) {
      const dx = v.x - x;
      if (Math.abs(dx) < rho) z = Math.max(z, v.z + Math.sqrt(rho * rho - dx * dx));
    }
    for (const e of T.E) {
      if (e.nz <= 0.5) continue; // vertical faces are covered by their end points
      // the clearance line sits rho along the normal, so it is shifted sideways too
      const ox = rho * e.nx, oz = rho * e.nz;
      const xa = Math.min(e.A.x, e.B.x) + ox, xb = Math.max(e.A.x, e.B.x) + ox;
      if (x >= xa && x <= xb) z = Math.max(z, e.A.z + oz + ((x - (e.A.x + ox)) / e.ex) * e.ez);
    }
    return z;
  }

  // A unit hinged at J points forward (+x). Rotate it down from vertical until its
  // track (the axle segment grown by rho) first touches the stairs. Returns that angle.
  function restAngle(T, jx, jz, L, rho) {
    let best = -Math.PI / 2 + 1e-4;
    const xmin = jx - rho, xmax = jx + L + rho;
    for (const v of T.V) {
      if (v.x < xmin || v.x > xmax) continue;
      const wx = v.x - jx, wz = v.z - jz;
      const d = Math.hypot(wx, wz);
      if (d < 1e-9) continue;
      const phi = Math.atan2(wz, wx);
      const dd = Math.max(d, rho);
      if (Math.sqrt(dd * dd - rho * rho) <= L) {
        const th = phi + Math.asin(Math.min(1, rho / dd));
        if (th < Math.PI / 2 && th > best) best = th;
      }
      if (d >= L - rho && d <= L + rho) {
        const k = (L * L + d * d - rho * rho) / (2 * L * d);
        if (k >= -1 && k <= 1) {
          const th = phi + Math.acos(k);
          if (th < Math.PI / 2 && th > best) best = th;
        }
      }
    }
    for (const e of T.E) {
      if (e.x1 < xmin || e.x0 > xmax) continue;
      const k = (rho - (e.nx * (jx - e.A.x) + e.nz * (jz - e.A.z))) / L;
      if (k < -1 || k > 1) continue;
      const psi = Math.atan2(e.nz, e.nx), ac = Math.acos(k);
      for (let th of [psi + ac, psi - ac]) {
        while (th > Math.PI) th -= 2 * Math.PI;
        while (th <= -Math.PI) th += 2 * Math.PI;
        if (th <= -Math.PI / 2 || th >= Math.PI / 2 || th <= best) continue;
        const Ex = jx + L * Math.cos(th), Ez = jz + L * Math.sin(th);
        const s = ((Ex - e.A.x) * e.ex + (Ez - e.A.z) * e.ez) / e.len2;
        if (s >= 0 && s <= 1) best = th;
      }
    }
    return best;
  }

  // Rest angle of a unit pointing backward (-x), via the mirrored stairs.
  // Returned as the mirrored angle: the far end sits at (jx - L cos, jz + L sin).
  const restAngleBack = (T, jx, jz, L, rho) => restAngle(T.mirror, -jx, jz, L, rho);

  // Shortest distance from segment A-B to the terrain polyline.
  function segTerrainDist(T, ax, az, bx, bz) {
    let d = Infinity;
    const lo = Math.min(ax, bx), hi = Math.max(ax, bx);
    for (const e of T.E) {
      if (e.x1 < lo - 1 || e.x0 > hi + 1) continue;
      d = Math.min(d, segSegDist(ax, az, bx, bz, e.A.x, e.A.z, e.B.x, e.B.z));
    }
    return d;
  }

  function segSegDist(ax, az, bx, bz, cx, cz, dx, dz) {
    const cross = (px, pz, qx, qz, rx, rz) => (qx - px) * (rz - pz) - (qz - pz) * (rx - px);
    const d1 = cross(ax, az, bx, bz, cx, cz), d2 = cross(ax, az, bx, bz, dx, dz);
    const d3 = cross(cx, cz, dx, dz, ax, az), d4 = cross(cx, cz, dx, dz, bx, bz);
    if (((d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0)) && ((d3 > 0 && d4 < 0) || (d3 < 0 && d4 > 0))) return 0;
    return Math.min(
      segPointDist(ax, az, bx, bz, cx, cz).d, segPointDist(ax, az, bx, bz, dx, dz).d,
      segPointDist(cx, cz, dx, dz, ax, az).d, segPointDist(cx, cz, dx, dz, bx, bz).d,
    );
  }

  // ------------------------------------------------------------ pose solvers
  // The path of a sprocket centre riding over the stairs (the surface grown by rho),
  // sampled as a dense polyline.
  function sprocketPath(T, rho, x0, x1, dx = 0.002) {
    const n = Math.ceil((x1 - x0) / dx) + 1;
    const X = new Float64Array(n), Z = new Float64Array(n);
    for (let i = 0; i < n; i++) { X[i] = x0 + i * dx; Z[i] = clearanceZ(T, X[i], rho); }
    return { X, Z, x0, dx, n };
  }
  // Where a hinge axle sits when the track is folded over the stairs: the pitch line moved up by the
  // pulley radius with its corners kept sharp. Over a crest a single pulley rolls round the corner a
  // little lower than this, and the sections either side of a hinge held that low would cut the corner.
  function mitreZ(prof, rho, x) {
    if (!prof._mitre || prof._mitre.rho !== rho) {
      const pts = prof.pitch, off = [];
      for (let i = 1; i < pts.length; i++) {
        const [x0, z0] = pts[i - 1], [x1, z1] = pts[i], l = Math.hypot(x1 - x0, z1 - z0);
        if (l < 1e-9) continue;
        const nx = -(z1 - z0) / l, nz = (x1 - x0) / l;
        off.push([x0 + nx * rho, z0 + nz * rho, x1 + nx * rho, z1 + nz * rho]);
      }
      const V = [[off[0][0], off[0][1]]];
      for (let i = 1; i < off.length; i++) {
        const [ax, az, bx, bz] = off[i - 1], [cx, cz, dx, dz] = off[i];
        const den = (bx - ax) * (dz - cz) - (bz - az) * (dx - cx);
        const t = Math.abs(den) < 1e-12 ? 1 : ((cx - ax) * (dz - cz) - (cz - az) * (dx - cx)) / den;
        V.push([ax + t * (bx - ax), az + t * (bz - az)]);
      }
      V.push([off[off.length - 1][2], off[off.length - 1][3]]);
      prof._mitre = { rho, V };
    }
    const V = prof._mitre.V;
    if (x <= V[0][0]) return V[0][1];
    for (let i = 1; i < V.length; i++) if (x <= V[i][0]) { const [x0, z0] = V[i - 1], [x1, z1] = V[i]; return z0 + ((z1 - z0) * (x - x0)) / Math.max(1e-12, x1 - x0); }
    return V[V.length - 1][1];
  }
  function pathZ(Q, x) {
    const f = (x - Q.x0) / Q.dx, i = Math.max(0, Math.min(Q.n - 2, Math.floor(f))), t = f - i;
    return Q.Z[i] + (Q.Z[i + 1] - Q.Z[i]) * t;
  }
  // Points on the path at distance r from (cx, cz), ahead of xMin.
  function circleOnPath(Q, cx, cz, r, xMin) {
    const out = [];
    const i0 = Math.max(0, Math.floor((Math.max(xMin, cx - r) - Q.x0) / Q.dx));
    const i1 = Math.min(Q.n - 2, Math.ceil((cx + r - Q.x0) / Q.dx));
    for (let i = i0; i <= i1; i++) {
      const ax = Q.X[i], az = Q.Z[i], bx = Q.X[i + 1], bz = Q.Z[i + 1];
      const ex = bx - ax, ez = bz - az, fx = ax - cx, fz = az - cz;
      const a = ex * ex + ez * ez, b = 2 * (fx * ex + fz * ez), c = fx * fx + fz * fz - r * r;
      const disc = b * b - 4 * a * c;
      if (disc < 0) continue;
      const sq = Math.sqrt(disc);
      for (const t of [(-b - sq) / (2 * a), (-b + sq) / (2 * a)]) {
        if (t < 0 || t > 1) continue;
        const x = ax + t * ex;
        if (x > xMin) out.push({ x, z: az + t * ez });
      }
    }
    return out;
  }

  // Chain of two units with a fixed bend `beta` (0 for one rigid track), hinge point
  // at x = jx. Lift the hinge from jz0 until the chain fits, resting on the stairs.
  function solveBent(T, jx, jz0, beta, o, prevA1) {
    const L = o.unitLength, rho = o.sprocketRadius;
    const ang = (z) => ({ tf: restAngle(T, jx, z, L, rho), tb: restAngleBack(T, jx, z, L, rho) });
    const fits = (a) => a.tf - beta <= -a.tb + 1e-9;
    let z = jz0, a = ang(z);
    if (!fits(a)) {
      let lo = jz0, hi = jz0 + 1.5 * L;
      for (let k = 0; k < 44; k++) {
        const m = (lo + hi) / 2;
        if (fits(ang(m))) hi = m; else lo = m;
      }
      z = hi; a = ang(hi);
    }
    // Allowed rear-unit angles: [tf - beta, -tb]. With room to rock, the chain settles
    // under gravity onto whichever side keeps its centre of mass supported.
    const lo = a.tf - beta, hi = -a.tb;
    if (hi - lo < 1e-6) return pose(o, jx, z, hi, hi + beta);
    const cands = [pose(o, jx, z, hi, hi + beta), pose(o, jx, z, lo, lo + beta)];
    if (prevA1 !== undefined) cands.push(pose(o, jx, z, Math.min(Math.max(prevA1, lo), hi), Math.min(Math.max(prevA1, lo), hi) + beta));
    let best = cands[0], bm = -Infinity;
    for (const c of cands) {
      const m = supportMargin(T, o, c);
      if (m > bm + 1e-6) { bm = m; best = c; }
    }
    return best;
  }

  // Horizontal distance from the centre of mass to the nearest edge of support.
  const LINK_ARM = 0.15; // averaging-link arm fixed to each unit, m
  const SETTLE = 0.03; // a track within 3 cm of the surface settles onto it
  const FALL = 0.05; // tipping further than this onto a track end counts as a fall

  function supportMargin(T, o, p) {
    const rho = o.sprocketRadius, tol = SETTLE;
    const cs = contactsOf(T, p, rho, tol);
    if (!cs.length) return -1;
    const com = centreOfMass(o, p);
    let minX = Infinity, maxX = -Infinity;
    for (const c of cs) { minX = Math.min(minX, c.x); maxX = Math.max(maxX, c.x); }
    return Math.min(com.x - minX, maxX - com.x);
  }

  function centreOfMass(o, p) {
    const s = seatModel(o), m = s.mass;
    const c = Math.cos(p.phi), sn = Math.sin(p.phi);
    const lx = p.P.x + s.com.u * c - s.com.v * sn, lz = p.P.z + s.com.u * sn + s.com.v * c;
    // the tracks weigh 2 x unitMass in all, shared out by section length
    const us = unitsOf(p);
    let Ltot = 0;
    for (const [A, B] of us) Ltot += Math.hypot(B.x - A.x, B.z - A.z);
    let M = m, sx = m * lx, sz = m * lz;
    for (const [A, B] of us) {
      const mk = (2 * o.unitMass * Math.hypot(B.x - A.x, B.z - A.z)) / Ltot;
      M += mk; sx += (mk * (A.x + B.x)) / 2; sz += (mk * (A.z + B.z)) / 2;
    }
    if (p.pts) for (let j = 1; j < p.pts.length - 1; j++) if (j !== o.mainJoint) { M += o.extraHingeMass; sx += o.extraHingeMass * p.pts[j].x; sz += o.extraHingeMass * p.pts[j].z; }
    if (o.boxMass) {
      const a = p.angles ? p.angles[o.mainJoint - 1] : p.a1, [u, v] = o.boxCom;
      M += o.boxMass; sx += o.boxMass * (p.J.x + u * Math.cos(a) - v * Math.sin(a)); sz += o.boxMass * (p.J.z + u * Math.sin(a) + v * Math.cos(a));
    }
    return { x: sx / M, z: sz / M, load: { x: lx, z: lz } };
  }

  // Where the seat pivot sits. 'average': at the top of a post that leans with the
  // average pitch, the drive levelling the seat on top. 'upright': the drive sits at
  // the foot of the post and tilts the whole post, so the pivot stays over the hinge
  // and leans only by the seat tilt the drive has not yet taken out.
  function placePivot(o, p) {
    if (o.mastMode === 'twoArm' || o.mastMode === 'vArms') {
      if (!p.arms) { const off = o._twoArmOff || { dx: 0, dz: o.seatHeight }; p.P = { x: p.J.x + off.dx, z: p.J.z + off.dz }; }
      return;
    }
    const a = o.mastMode === 'upright' ? p.phi : o.mastMode === 'balance' ? p.pitch + (p.psiRel || 0) : o.mastMode === 'base' ? p.a1 : p.pitch;
    p.P = { x: p.J.x - o.seatHeight * Math.sin(a), z: p.J.z + o.seatHeight * Math.cos(a) };
  }

  // The levelling pivot turns the seat back towards level, but only so fast.
  function level(o, p, prevLam, ds) {
    if (o.mastMode === 'twoArm' || o.mastMode === 'vArms') { p.lam = 0; return; } // the two arms level the cradle themselves
    const lean = (o.mastMode === 'base' ? p.a1 : p.pitch) + (p.psiRel || 0); // what the arm leans, which the seat drive cancels
    if (o.levelLockDeg != null) { p.lam = rad(o.levelLockDeg); p.phi = lean - p.lam; placePivot(o, p); return; }
    if (!o.levelSeat) { p.lam = 0; p.phi = lean; placePivot(o, p); return; }
    const lim = rad(o.levelLimitDeg), target = clamp(lean, -lim, lim);
    let lam = target;
    if (prevLam !== null) { const mx = rad(o.levelRateDegPerM) * ds; lam = prevLam + clamp(target - prevLam, -mx, mx); }
    p.lam = lam;
    p.phi = lean - lam;
    placePivot(o, p);
  }

  // Two arms, one standing on each track unit, carry a cradle between them like a bed
  // on two legs: a pin at the rear arm, a pin that slides along the cradle at the front.
  // Each arm has its own drive. They keep the cradle level (tips at the same height)
  // and, like the balance arm, move it fore and aft to keep the weight furthest from
  // tipping, within their range and speed and without coming within 3 cm of anything.
  // If a drive cannot turn far enough in time, the cradle tilts.
  function armFeet(o, p) {
    const e = o.twoArmBaseUp;
    if (o.mastMode === 'vArms') {
      // both feet on the averaging post, just fore and aft of the hinge
      const f = o.vArmFoot, a = p.pitch, tx = Math.cos(a), tz = Math.sin(a), nx = -Math.sin(a), nz = Math.cos(a);
      return [
        { x: p.J.x - f * tx + e * nx, z: p.J.z - f * tz + e * nz, ref: a },
        { x: p.J.x + f * tx + e * nx, z: p.J.z + f * tz + e * nz, ref: a },
      ];
    }
    const d = o.twoArmBase;
    return [
      { x: p.J.x - d * Math.cos(p.a1) - e * Math.sin(p.a1), z: p.J.z - d * Math.sin(p.a1) + e * Math.cos(p.a1), ref: p.a1 },
      { x: p.J.x + d * Math.cos(p.a2) - e * Math.sin(p.a2), z: p.J.z + d * Math.sin(p.a2) + e * Math.cos(p.a2), ref: p.a2 },
    ];
  }
  function twoArms(T, TR, o, p, prev, ds) {
    const v = o.mastMode === 'vArms';
    const l = v ? o.vArmLen : o.twoArmLen, c = v ? o.vArmPins : o.twoArmBase, slide = v ? o.vArmSlide : o.twoArmSlide;
    const rho = o.sprocketRadius;
    const [B1, B2] = armFeet(o, p);
    const ref1 = B1.ref, ref2 = B2.ref;
    const lo = rad(15), hi = rad(165); // each arm stays above its own unit
    const stepMax = prev ? rad(o.twoArmRateDegPerM) * ds : Infinity;
    const tip = (B, g) => ({ x: B.x + l * Math.cos(g), z: B.z + l * Math.sin(g) });
    const wide = contactsOf(TR, p, rho, FALL);
    let cLo = null, cHi = null;
    for (const q of wide) { if (!cLo || q.x < cLo.x) cLo = q; if (!cHi || q.x > cHi.x) cHi = q; }
    const lean = (com) => (!cLo ? -1 : Math.min(Math.atan2(com.x - cLo.x, Math.max(1e-6, com.z - cLo.z)), Math.atan2(cHi.x - com.x, Math.max(1e-6, com.z - cHi.z))));
    // the arm angles, measured against their own units, carry over from the last step
    const rel1 = prev ? prev.g1 - prev.ref1 : null, rel2 = prev ? prev.g2 - prev.ref2 : null;
    let r0 = lo, r1 = hi;
    if (prev) { r0 = Math.max(lo, rel1 - stepMax); r1 = Math.min(hi, rel1 + stepMax); }
    if (o.twoArmLock === 'rear' && prev) { r0 = r1 = rel1; }
    const N = prev ? 12 : 90;
    const cands = [];
    for (let i = 0; i <= N; i++) {
      const g1 = ref1 + r0 + ((r1 - r0) * i) / N, T1 = tip(B1, g1);
      // front arm: tip level with the rear one, on the branch that keeps the pins about 2c apart
      const sn = (T1.z - B2.z) / l;
      const want = Math.abs(sn) <= 1 ? [Math.asin(sn), Math.PI - Math.asin(sn)] : [sn > 0 ? Math.PI / 2 : -Math.PI / 2];
      for (const gw of want) {
        let rel = gw - ref2;
        while (rel > Math.PI) rel -= 2 * Math.PI;
        while (rel < -Math.PI) rel += 2 * Math.PI;
        rel = clamp(rel, lo, hi);
        if (prev) rel = o.twoArmLock === 'front' ? rel2 : rel2 + clamp(rel - rel2, -stepMax, stepMax);
        const g2 = ref2 + rel, T2 = tip(B2, g2);
        const span = Math.hypot(T2.x - T1.x, T2.z - T1.z);
        if (T2.x <= T1.x || Math.abs(span - 2 * c) > slide) continue;
        const phi = Math.atan2(T2.z - T1.z, T2.x - T1.x);
        p.phi = phi; p.P = { x: T1.x + c * Math.cos(phi), z: T1.z + c * Math.sin(phi) };
        p.arms = { B1, B2, T1, T2, g1, g2, ref1, ref2 };
        const t = lean(centreOfMass(o, p));
        const move = prev ? Math.abs(g1 - ref1 - rel1) + Math.abs(rel - rel2) : 0;
        cands.push({ arms: p.arms, P: p.P, phi, score: Math.min(t, rad(25)) - 2 * Math.abs(phi) - 1e-3 * move });
      }
    }
    if (!cands.length) {
      // nothing reachable keeps the pins in their slide: hold the last arm angles
      const g1 = prev ? ref1 + rel1 : ref1 + Math.PI / 2, g2 = prev ? ref2 + rel2 : ref2 + Math.PI / 2;
      const T1 = tip(B1, g1), T2 = tip(B2, g2), phi = Math.atan2(T2.z - T1.z, T2.x - T1.x);
      cands.push({ arms: { B1, B2, T1, T2, g1, g2, ref1, ref2 }, P: { x: T1.x + c * Math.cos(phi), z: T1.z + c * Math.sin(phi) }, phi, score: -Infinity });
    }
    cands.sort((u, v) => v.score - u.score);
    let pick = cands[0];
    for (const cd of cands.slice(0, 8)) {
      p.arms = cd.arms; p.P = cd.P; p.phi = cd.phi;
      let gap = Infinity;
      for (const q of placeSeat(o, p)) {
        gap = Math.min(gap, segTerrainDist(T, q.ax, q.az, q.bx, q.bz) - q.r);
        for (const [A, B] of unitsOf(p)) gap = Math.min(gap, segSegDist(q.ax, q.az, q.bx, q.bz, A.x, A.z, B.x, B.z) - q.r - rho);
      }
      for (const [F, Tp, others] of [[cd.arms.B1, cd.arms.T1, v ? unitsOf(p) : [[p.J, p.F]]], [cd.arms.B2, cd.arms.T2, v ? unitsOf(p) : [[p.R, p.J]]]]) {
        gap = Math.min(gap, segTerrainDist(T, F.x, F.z, Tp.x, Tp.z) - 0.03);
        // an arm must not come down onto a track: stay 3 cm clear once past its own foot
        for (const [A, B] of others) {
          const q = { x: F.x + (Tp.x - F.x) * 0.25, z: F.z + (Tp.z - F.z) * 0.25 };
          gap = Math.min(gap, segSegDist(q.x, q.z, Tp.x, Tp.z, A.x, A.z, B.x, B.z) - 0.03 - rho);
        }
      }
      if (gap >= 0.03) { pick = cd; break; }
    }
    p.arms = pick.arms; p.P = pick.P; p.phi = pick.phi;
  }

  // Balance arm: with the vehicle pose settled, lean the arm (within its range and
  // speed) to where the weight can take the biggest push before the vehicle falls,
  // without bringing the seat within 3 cm of the steps or tracks.
  function balanceArm(T, TR, o, p, prevRel, ds) {
    if (o.armLockDeg != null) { p.psiRel = rad(o.armLockDeg); placePivot(o, p); return; }
    const rho = o.sprocketRadius, lim = rad(o.armLimitDeg), stepMax = rad(o.armRateDegPerM) * ds;
    if (o.levelLockDeg != null) {
      // the seat drive has stuck: the arm takes over levelling the seat as far as it can
      const want = clamp(rad(o.levelLockDeg) - p.pitch, -lim, lim);
      p.psiRel = prevRel == null ? want : prevRel + clamp(want - prevRel, -stepMax, stepMax);
      placePivot(o, p);
      return;
    }
    const wide = contactsOf(TR, p, rho, FALL);
    let lo = null, hi = null;
    for (const c of wide) { if (!lo || c.x < lo.x) lo = c; if (!hi || c.x > hi.x) hi = c; }
    if (!lo) return;
    const a = prevRel == null ? -lim : Math.max(-lim, prevRel - stepMax);
    const b = prevRel == null ? lim : Math.min(lim, prevRel + stepMax);
    const cands = [];
    for (let i = 0; i <= 16; i++) {
      p.psiRel = a + ((b - a) * i) / 16;
      p.phi = 0; // the seat drive keeps up (its lag is applied afterwards)
      placePivot(o, p);
      const c = centreOfMass(o, p);
      const t = Math.min(Math.atan2(c.x - lo.x, Math.max(1e-6, c.z - lo.z)), Math.atan2(hi.x - c.x, Math.max(1e-6, c.z - hi.z)));
      // beyond 25 degrees of margin there is nothing to gain; then move as little as possible
      cands.push({ rel: p.psiRel, score: Math.min(t, rad(25)) - 1e-3 * Math.abs(p.psiRel - (prevRel == null ? 0 : prevRel)) });
    }
    cands.sort((u, v) => v.score - u.score);
    let pick = cands[0];
    for (const c of cands) {
      p.psiRel = c.rel; placePivot(o, p);
      let gap = Infinity;
      for (const q of placeSeat(o, p)) {
        gap = Math.min(gap, segTerrainDist(T, q.ax, q.az, q.bx, q.bz) - q.r);
        for (const [A, B] of unitsOf(p)) gap = Math.min(gap, segSegDist(q.ax, q.az, q.bx, q.bz, A.x, A.z, B.x, B.z) - q.r - rho);
      }
      if (gap >= 0.03) { pick = c; break; }
    }
    p.psiRel = pick.rel;
    placePivot(o, p);
  }

  // Lift the hinge above (jx, jz0) until both outer track ends can touch the stairs.
  function solveTent(T, QE, jx, jz0, o) {
    const L = o.unitLength, rho = o.sprocketRadius, lim = rad(o.hingeLimitDeg);
    const clear = (A, B) => segTerrainDist(T, A.x, A.z, B.x, B.z) >= rho - 6e-4;
    const at = (dz) => {
      const J = { x: jx, z: jz0 + dz };
      const Rs = circleOnPath(QE, J.x, J.z, L, -Infinity).filter((q) => q.x < J.x - 1e-6);
      const Fs = circleOnPath(QE, J.x, J.z, L, J.x + 1e-6);
      for (const R of Rs) for (const F of Fs) {
        const a1 = Math.atan2(J.z - R.z, J.x - R.x), a2 = Math.atan2(F.z - J.z, F.x - J.x);
        if (Math.abs(a2 - a1) > lim + 1e-9) continue;
        if (clear(R, J) && clear(J, F)) return pose(o, J.x, J.z, a1, a2);
      }
      return null;
    };
    let prevDz = 0;
    for (let dz = 0; dz <= 0.5; dz += 0.01) {
      const p = at(dz);
      if (p) { // refine the lowest lift between the last miss and this hit
        let lo = prevDz, hi = dz, best = p;
        for (let k = 0; k < 12; k++) {
          const m = (lo + hi) / 2, q = at(m);
          if (q) { hi = m; best = q; } else lo = m;
        }
        return best;
      }
      prevDz = dz;
    }
    return null;
  }

  // Two units with a driven hinge, at hinge position J0 on the hinge path.
  // Target shape: each unit settles onto the stairs (a bend past the limit locks at
  // the limit); when the leading unit sticks out past a platform edge it is folded
  // down onto the next surface (hinge lifted just enough for both track ends to
  // touch). It stays folded until the centre of mass is HOLD past the edge, so the
  // trailing unit keeps its end on the stairs; then the trailing unit straightens.
  const HOLD = 0.05;
  function targetHinged(T, QE, J0, o, prof, dir, state) {
    const L = o.unitLength, rho = o.sprocketRadius, lim = rad(o.hingeLimitDeg);
    const tf = restAngle(T, J0.x, J0.z, L, rho), tb = restAngleBack(T, J0.x, J0.z, L, rho);
    let p = pose(o, J0.x, J0.z, -tb, tf);
    if (Math.abs(p.beta) > lim) p = solveBent(T, J0.x, J0.z, Math.sign(p.beta) * lim, o);
    if (o.reach === 'lie') {
      // only a small lift: fold the leading half down past the edge if the hinge rises no more than maxLift
      const lead = dir === 'up' ? p.F : p.R, sgn = dir === 'up' ? 1 : -1;
      const edge = prof.edges.find((c) => sgn * (c.x - p.J.x) > 0 && sgn * (lead.x - c.x) > rho);
      if (edge && o.maxLift > 0 && lead.z - pathZ(QE, lead.x) > 0.02) {
        const t = solveTent(T, QE, p.J.x, p.J.z, o);
        if (t && t.J.z - p.J.z <= o.maxLift) { t.folded = true; return t; }
      }
      return p;
    }
    const lead = dir === 'up' ? p.F : p.R;
    const sgn = dir === 'up' ? 1 : -1;
    // the edge the leading unit is reaching over (hinge before it, leading end past it)
    const edge = prof.edges.find((c) => sgn * (c.x - p.J.x) > 0 && sgn * (lead.x - c.x) > rho);
    if (edge && (state.folding === edge || lead.z - pathZ(QE, lead.x) > 0.02)) {
      const t = solveTent(T, QE, p.J.x, p.J.z, o);
      if (t) { t.folded = true; state.folding = edge; return t; }
    }
    if (!edge && state.folding) {
      const t = solveTent(T, QE, p.J.x, p.J.z, o);
      if (t && sgn * (centreOfMass(o, t).x - state.folding.x) < HOLD) { t.folded = true; return t; }
    }
    if (!edge) state.folding = null;
    return p;
  }

  // How far the vehicle could lean before it tips (the same measure as evaluate's tipAngle).
  function leanMargin(T, o, p) {
    const wide = contactsOf(T, p, o.sprocketRadius, FALL), com = centreOfMass(o, p);
    let lo = null, hi = null;
    for (const c of wide) { if (!lo || c.x < lo.x) lo = c; if (!hi || c.x > hi.x) hi = c; }
    if (!lo) return -Math.PI / 2;
    return Math.min(Math.atan2(com.x - lo.x, Math.max(1e-6, com.z - lo.z)), Math.atan2(hi.x - com.x, Math.max(1e-6, com.z - hi.z)));
  }
  // stopGo: makers of candidate shapes from the target (first) back to holding the last bends
  // (last), each made only when needed. Take the one furthest towards the target that leaves a
  // safe lean, or at least as much as holding.
  function guardedMove(T, o, makers) {
    const safe = rad(o.stopGoSafeDeg), qs = [], ms = [];
    const get = (i) => { if (!(i in qs)) { qs[i] = makers[i]() || null; ms[i] = qs[i] ? leanMargin(T, o, qs[i]) : null; } return qs[i]; };
    if (get(0) && ms[0] >= safe - 1e-9) return qs[0];
    let h = makers.length - 1;
    while (h > 0 && !get(h)) h--;
    const need = Math.min(safe, ms[h]) - 1e-9;
    for (let i = 0; i < h; i++) if (get(i) && ms[i] >= need) { if (i) qs[i].held = true; return qs[i]; }
    if (h) qs[h].held = true;
    return qs[h];
  }

  // The leading-end laser: how much lower than usual it sees the stairs, m, looking straight down
  // from the end axle (on flat ground it reads the axle height).
  function laserDrop(Treal, o, p, dir) {
    const lead = dir === 'up' ? p.F : p.R;
    return lead.z - groundZ(Treal, lead.x) - o.sprocketRadius;
  }
  // stopGo with a laser: hold the hinges while an edge lies between the seat's hinge and the leading
  // end, until the laser sees the drop. Returns true while the vehicle should drive on, held.
  // Once it has seen the drop, the pose is marked edgeSeen until that edge is behind the hinge.
  function laserWait(o, prof, dir, p, state) {
    if (o.laserRisers == null) return false;
    const sgn = dir === 'up' ? 1 : -1, lead = dir === 'up' ? p.F : p.R;
    const edge = prof.edges.find((c) => sgn * (c.x - p.J.x) > 0 && sgn * (lead.x - c.x) > 0);
    p.laser = laserDrop(state.T, o, p, dir);
    if (!edge) { state.laser = null; return false; }
    if (state.laser === edge) { p.edgeSeen = true; return false; }
    if (p.laser >= o.laserRisers * o.rise - 0.005) { state.laser = edge; p.laserFired = p.edgeSeen = true; return false; }
    return true;
  }

  // Follow the target, but the hinge can only bend so fast per metre travelled.
  function solveHinged(T, QE, J0, o, prof, dir, prev, ds, state) {
    if (o.bendMode === 'stopGo' && prev) {
      const hold = solveBent(T, J0.x, J0.z, prev.beta, o, prev.a1);
      hold.folded = prev.folded;
      if (laserWait(o, prof, dir, hold, state)) { hold.held = true; hold.waiting = true; return hold; }
      const target = targetHinged(T, QE, J0, o, prof, dir, state);
      const toward = (t) => () => {
        const q = solveBent(T, J0.x, J0.z, prev.beta + t * (target.beta - prev.beta), o, prev.a1);
        q.folded = target.folded;
        return q;
      };
      const q = guardedMove(T, o, [() => target, toward(0.75), toward(0.5), toward(0.25), () => hold]);
      if (hold.laserFired) q.laserFired = true;
      if (hold.edgeSeen) q.edgeSeen = true;
      q.laser = hold.laser;
      return q;
    }
    const target = targetHinged(T, QE, J0, o, prof, dir, state);
    if (!prev) return target;
    const maxStep = rad(o.hingeRateDegPerM) * ds;
    const dBeta = target.beta - prev.beta;
    if (Math.abs(dBeta) <= maxStep + 1e-9) return target;
    const p = solveBent(T, J0.x, J0.z, prev.beta + Math.sign(dBeta) * maxStep, o, prev.a1);
    p.rateLimited = true;
    p.folded = target.folded;
    return p;
  }

  // ------------------------------------------------- more than two sections
  // A chain of track sections joined by driven hinges, rear to front. The hinge that
  // carries the seat (o.mainJoint) rides the hinge path like the two-section vehicle's
  // hinge, and the same rules apply, section by section:
  //  - each section settles onto the stairs about its inner end (the end nearer the
  //    seat's hinge); an outer hinge stops at its limit and leaves its section hanging;
  //  - working out from the seat's hinge, the first section reaching out past a
  //    platform edge with its end in the air is folded down onto the next surface by
  //    lifting its inner end as little as possible: the seat's hinge (keeping the far
  //    track end on the stairs, as the two-section tent) or the hinge inside it, by
  //    turning the section inside it up;
  //  - once over an edge, the seat's hinge stays lifted with both track ends on the
  //    stairs until the centre of mass is HOLD past the edge;
  //  - a split half that is trailing (or not folding) either settles or is held in
  //    line as one piece, whichever shape the hinges reach sooner (o.trailMode);
  //  - every hinge bends only so fast; the seat's hinge goes as fast as it can and the
  //    others keep up with it (o.hingeControl).
  // With two sections this gives exactly the same poses as solveHinged.
  function chainPoints(L, m, M, a) {
    const N = L.length, P = new Array(N + 1);
    P[m] = { x: M.x, z: M.z };
    for (let k = m; k < N; k++) P[k + 1] = { x: P[k].x + L[k] * Math.cos(a[k]), z: P[k].z + L[k] * Math.sin(a[k]) };
    for (let k = m - 1; k >= 0; k--) P[k] = { x: P[k + 1].x - L[k] * Math.cos(a[k]), z: P[k + 1].z - L[k] * Math.sin(a[k]) };
    return P;
  }
  // section angles from the bends (bend j sits between sections j-1 and j) and the
  // angle of the section just ahead of the seat's hinge
  function chainAngles(betas, m, N, th) {
    const a = new Array(N);
    a[m] = th;
    for (let k = m + 1; k < N; k++) a[k] = a[k - 1] + betas[k - 1];
    for (let k = m - 1; k >= 0; k--) a[k] = a[k + 1] - betas[k];
    return a;
  }
  function makeChainPose(o, M, a) {
    const L = o.sections, m = o.mainJoint, N = L.length;
    const pts = chainPoints(L, m, M, a);
    const units = [], bends = [];
    for (let k = 0; k < N; k++) units.push([pts[k], pts[k + 1]]);
    for (let j = 1; j < N; j++) bends.push(a[j] - a[j - 1]);
    return finishPose(o, { J: pts[m], R: pts[0], F: pts[N], a1: a[m - 1], a2: a[m], beta: a[m] - a[m - 1], units, pts, m, angles: a.slice(), bends });
  }
  const bendsOk = (o, a) => a.every((v, k) => k === 0 || Math.abs(v - a[k - 1]) <= rad(o.hingeLimitDeg) + 1e-9);
  // Settle section k0 and the sections beyond it (away from the seat's hinge) onto the
  // stairs, each about its inner end. An outer hinge bends down no further than its
  // limit, leaving its section hanging.
  function settle(T, o, M, a, k0) {
    const L = o.sections, m = o.mainJoint, N = L.length, rho = o.sprocketRadius, lim = rad(o.hingeLimitDeg);
    const aa = a.slice();
    if (k0 >= m) {
      let P = chainPoints(L, m, M, aa)[k0];
      for (let k = k0; k < N; k++) {
        let th = restAngle(T, P.x, P.z, L[k], rho);
        if (k > m) th = Math.max(th, aa[k - 1] - lim);
        aa[k] = th;
        P = { x: P.x + L[k] * Math.cos(th), z: P.z + L[k] * Math.sin(th) };
      }
    } else {
      let P = chainPoints(L, m, M, aa)[k0 + 1];
      for (let k = k0; k >= 0; k--) {
        let th = -restAngleBack(T, P.x, P.z, L[k], rho);
        if (k < m - 1) th = Math.min(th, aa[k + 1] + lim);
        aa[k] = th;
        P = { x: P.x - L[k] * Math.cos(th), z: P.z - L[k] * Math.sin(th) };
      }
    }
    return aa;
  }
  function drapeChain(T, o, M) {
    const a = settle(T, o, M, new Array(o.sections.length).fill(0), o.mainJoint);
    return settle(T, o, M, a, o.mainJoint - 1);
  }
  // With every bend fixed, the angles the chain can take at hinge height z without
  // any section cutting into the stairs (an interval of the section-ahead angle).
  function chainInterval(T, o, x, z, betas) {
    const L = o.sections, m = o.mainJoint, N = L.length, rho = o.sprocketRadius, M = { x, z };
    const angles = (th) => chainAngles(betas, m, N, th);
    let lo = restAngle(T, x, z, L[m], rho);
    let hi = -restAngleBack(T, x, z, L[m - 1], rho) + betas[m - 1];
    if (hi < lo - 1e-9) return null;
    // outer sections ahead clear more easily as the chain turns up, those behind as it turns down
    const okFwd = (th) => { const a = angles(th), P = chainPoints(L, m, M, a); for (let k = m + 1; k < N; k++) if (a[k] < restAngle(T, P[k].x, P[k].z, L[k], rho) - 1e-7) return false; return true; };
    const okBack = (th) => { const a = angles(th), P = chainPoints(L, m, M, a); for (let k = m - 2; k >= 0; k--) if (a[k] > -restAngleBack(T, P[k + 1].x, P[k + 1].z, L[k], rho) + 1e-7) return false; return true; };
    if (m + 1 < N) {
      if (!okFwd(hi)) return null;
      if (!okFwd(lo)) { let u = lo, v = hi; for (let i = 0; i < 30; i++) { const w = (u + v) / 2; if (okFwd(w)) v = w; else u = w; } lo = v; }
    }
    if (m > 1) {
      if (!okBack(lo)) return null;
      if (!okBack(hi)) { let u = lo, v = hi; for (let i = 0; i < 30; i++) { const w = (u + v) / 2; if (okBack(w)) u = w; else v = w; } hi = u; }
    }
    return hi >= lo - 1e-9 ? { lo, hi: Math.max(lo, hi), angles } : null;
  }
  // Chain with fixed bends: lift the seat's hinge from z0 until it fits, then let it
  // settle onto whichever side keeps the centre of mass supported (as solveBent).
  function solveChainBent(T, o, x, z0, betas, prevTh) {
    const Ltot = o.sections.reduce((u, v) => u + v, 0);
    let z = z0, iv = chainInterval(T, o, x, z, betas);
    if (!iv) {
      let lo = z0, hi = z0 + Ltot;
      if (!chainInterval(T, o, x, hi, betas)) return null;
      for (let k = 0; k < 40; k++) { const mid = (lo + hi) / 2; if (chainInterval(T, o, x, mid, betas)) hi = mid; else lo = mid; }
      z = hi; iv = chainInterval(T, o, x, z, betas);
      if (!iv) return null;
    }
    const M = { x, z }, cands = [iv.hi, iv.lo];
    if (prevTh !== undefined && prevTh !== null) cands.push(clamp(prevTh, iv.lo, iv.hi));
    let best = null, bm = -Infinity;
    for (const th of cands) { const q = makeChainPose(o, M, iv.angles(th)); const mg = supportMargin(T, o, q); if (mg > bm + 1e-6) { bm = mg; best = q; } }
    return best;
  }
  // Where section k can put its outer end down on the stairs from its inner end Pj
  // without cutting into them: a list of angle sets, nearest spot first.
  function endSpots(T, QE, o, a, k, Pj, ahead) {
    const L = o.sections, rho = o.sprocketRadius;
    let cs = ahead ? circleOnPath(QE, Pj.x, Pj.z, L[k], Pj.x + 1e-6) : circleOnPath(QE, Pj.x, Pj.z, L[k], -Infinity).filter((q) => q.x < Pj.x - 1e-6);
    cs = cs.sort((u, v) => (ahead ? u.x - v.x : v.x - u.x));
    const out = [];
    for (const q of cs) {
      if (segTerrainDist(T, Pj.x, Pj.z, q.x, q.z) < rho - 6e-4) continue;
      const aa = a.slice();
      aa[k] = ahead ? Math.atan2(q.z - Pj.z, q.x - Pj.x) : Math.atan2(Pj.z - q.z, Pj.x - q.x);
      out.push(aa);
    }
    return out;
  }
  // Put section k's outer end down on the stairs, if it fits within the hinge limits.
  function placeEnd(T, QE, o, a, k, Pj, ahead) {
    return endSpots(T, QE, o, a, k, Pj, ahead).find((aa) => bendsOk(o, aa)) || null;
  }
  // Scan a lift upwards in 1 cm (or 0.5 degree) steps, then refine the first hit.
  function firstFit(at, step, max) {
    let prev = 0;
    for (let d = 0; d <= max + 1e-9; d += step) {
      const hit = at(d);
      if (hit) {
        let lo = prev, hi = d, best = hit;
        for (let k = 0; k < 12; k++) { const mid = (lo + hi) / 2, q = at(mid); if (q) { hi = mid; best = q; } else lo = mid; }
        return best;
      }
      prev = d;
    }
    return null;
  }
  // The sections on one side of the seat's hinge (side +1 ahead of it, -1 behind).
  function sideSections(o, side) {
    const m = o.mainJoint, N = o.sections.length, ks = [];
    for (let k = side > 0 ? m : m - 1; side > 0 ? k < N : k >= 0; k += side) ks.push(k);
    return ks;
  }
  // The shapes one side of the seat's hinge can take from a lifted hinge Mz with its
  // far track end on the stairs, of one kind: 'fold' (section `first`, next to the
  // hinge, puts its end down and the ones beyond it settle), 'settle' (the sections
  // settle, the last one letting its end down if it hangs) or 'straight' (the sections
  // held in line as one piece, its far end on the stairs).
  function sideShapes(T, QE, o, Mz, side, kind, first) {
    const L = o.sections, m = o.mainJoint, N = L.length, lim = rad(o.hingeLimitDeg), rho = o.sprocketRadius;
    const ks = sideSections(o, side), k0 = ks[0], kEnd = ks[ks.length - 1];
    const inside = (aa) => ks.every((k) => k === k0 || Math.abs(aa[k] - aa[k - side]) <= lim + 1e-9);
    const zero = new Array(N).fill(0);
    if (kind === 'fold') {
      return endSpots(T, QE, o, zero, first, Mz, side > 0)
        .map((aa) => (first === kEnd ? aa : settle(T, o, Mz, aa, first + side)))
        .filter(inside);
    }
    if (kind === 'settle') {
      const aa = settle(T, o, Mz, zero, k0), P = chainPoints(L, m, Mz, aa), E = side > 0 ? P[N] : P[0];
      if (Math.abs(E.z - pathZ(QE, E.x)) <= 1e-3) return [aa];
      return endSpots(T, QE, o, aa, kEnd, side > 0 ? P[N - 1] : P[1], side > 0).filter(inside);
    }
    const Ls = ks.reduce((u, k) => u + L[k], 0), out = [];
    let cs = side > 0 ? circleOnPath(QE, Mz.x, Mz.z, Ls, Mz.x + 1e-6) : circleOnPath(QE, Mz.x, Mz.z, Ls, -Infinity).filter((q) => q.x < Mz.x - 1e-6);
    cs = cs.sort((u, v) => (side > 0 ? u.x - v.x : v.x - u.x));
    for (const q of cs) {
      if (segTerrainDist(T, Mz.x, Mz.z, q.x, q.z) < rho - 6e-4) continue;
      const th = side > 0 ? Math.atan2(q.z - Mz.z, q.x - Mz.x) : Math.atan2(Mz.z - q.z, Mz.x - q.x);
      const bb = zero.slice();
      for (const k of ks) bb[k] = th;
      out.push(bb);
    }
    return out;
  }
  // Of several candidate shapes, the one the hinges can reach soonest from the last
  // pose (smallest largest bend change); the first one if there is no last pose.
  function nearest(cands, prev) {
    if (!prev || cands.length < 2) return cands[0] || null;
    let best = cands[0], bs = Infinity;
    for (const c of cands) {
      let d = 0;
      for (let j = 1; j < c.a.length; j++) d = Math.max(d, Math.abs(c.a[j] - c.a[j - 1] - prev.bends[j - 1]));
      if (d < bs - 1e-6) { bs = d; best = c; }
    }
    return best;
  }
  // Lift the seat's hinge as little as possible until both outer track ends rest on
  // the stairs (with two sections, the tent of solveTent). With `first` given, that
  // section (next to the hinge) is the one folding down past an edge. A split half may
  // settle or be held straight; of those, the shape nearest the last pose is used.
  function chainLift(T, QE, o, M, first, prev, trail) {
    const m = o.mainJoint, lim = rad(o.hingeLimitDeg);
    const fSide = first == null ? 0 : first >= m ? 1 : -1;
    const kinds = (side) => (side === fSide ? ['fold'] : sideSections(o, side).length < 2 ? ['settle'] : trail === side && (o.trailMode === 'settle' || o.trailMode === 'straight') ? [o.trailMode] : ['settle', 'straight']);
    const cands = [];
    for (const kb of kinds(-1)) for (const kf of kinds(1)) {
      const t = firstFit((dz) => {
        const Mz = { x: M.x, z: M.z + dz };
        const behind = sideShapes(T, QE, o, Mz, -1, kb, first);
        if (!behind.length) return null;
        for (const f of sideShapes(T, QE, o, Mz, 1, kf, first)) for (const r of behind) {
          if (Math.abs(f[m] - r[m - 1]) <= lim + 1e-9) return { M: Mz, a: r.slice(0, m).concat(f.slice(m)) };
        }
        return null;
      }, 0.01, 0.5);
      if (t) cands.push(t);
    }
    return nearest(cands, prev);
  }
  // Fold section k (ahead of the seat's hinge in the direction of travel) down past an
  // edge: lift its inner end as little as possible until its outer end reaches the
  // stairs, then let the sections beyond it settle.
  function foldSection(T, QE, o, M, a, k, dir, prev) {
    const L = o.sections, m = o.mainJoint, N = L.length, rho = o.sprocketRadius, up = dir === 'up';
    if (k === (up ? m : m - 1)) return chainLift(T, QE, o, M, k, prev, up ? -1 : 1);
    const parent = up ? k - 1 : k + 1, beyond = up ? k + 1 : k - 1;
    return firstFit((d) => {
      const aa = a.slice();
      aa[parent] = a[parent] + (up ? d : -d); // turn the section inside it up
      const P = chainPoints(L, m, M, aa), A = P[parent], B = P[parent + 1];
      if (segTerrainDist(T, A.x, A.z, B.x, B.z) < rho - 6e-4) return null;
      let out = placeEnd(T, QE, o, aa, k, up ? P[k] : P[k + 1], up);
      if (out && beyond >= 0 && beyond < N) out = settle(T, o, M, out, beyond);
      return out && bendsOk(o, out) ? { M, a: out } : null;
    }, rad(0.5), rad(60));
  }
  function targetChain(T, QE, J0, o, prof, dir, state, prev) {
    const N = o.sections.length, m = o.mainJoint, rho = o.sprocketRadius, lim = rad(o.hingeLimitDeg);
    const up = dir === 'up', sgn = up ? 1 : -1;
    if (o.reach === 'touch' && N > 2) {
      // A stiff main track (every section but the leading one, its hinges straight, the seat's hinge in
      // its middle) and an arm on its leading axle. The main track rests on the stairs by its own weight,
      // then the arm swings (down or up) until it just touches the stairs ahead: it can catch the vehicle,
      // but never props it up.
      const armK = up ? N - 1 : 0, main = up ? o.sections.slice(0, N - 1) : o.sections.slice(1);
      const om = Object.assign({}, o, { sections: main, mainJoint: up ? m : m - 1 });
      const body = solveChainBent(T, om, J0.x, J0.z, main.slice(1).map(() => 0), prev ? prev.angles[m] : undefined);
      if (body) {
        const ang = up ? body.angles.concat([0]) : [0].concat(body.angles);
        const P = body.pts[up ? main.length : 0], inner = ang[up ? armK - 1 : armK + 1];
        const arm = up ? restAngle(T, P.x, P.z, o.sections[armK], rho) : -restAngleBack(T, P.x, P.z, o.sections[armK], rho);
        const lift = up ? arm - inner : inner - arm, upMax = o.armUpDeg != null ? rad(o.armUpDeg) : lim; // + is the arm up
        if (lift <= upMax) {
          const b = Math.max(-lim, lift);
          ang[armK] = up ? inner + b : inner - b;
          return makeChainPose(o, body.J, ang);
        }
        // the arm can't swing up that far (the platform is in the way): it climbs the step at its limit
        const q = solveChainBent(T, o, J0.x, J0.z, o.sections.slice(1).map((_, j) => (j === (up ? N - 2 : 0) ? upMax : 0)), prev ? prev.angles[m] : undefined);
        if (q) return q;
      }
    }
    if (o.reach === 'lie') {
      // every section rests on the stairs about its inner hinge, the seat's hinge where a folded track puts it
      const J = { x: J0.x, z: Math.max(J0.z, mitreZ(prof, rho, J0.x)) };
      let p = makeChainPose(o, J, drapeChain(T, o, J));
      if (!bendsOk(o, p.angles)) p = solveChainBent(T, o, J.x, J.z, p.bends.map((b) => clamp(b, -lim, lim))) || p;
      // working out from the seat's hinge, the first section reaching out past an edge with its
      // end in the air folds down onto the stairs, if that lifts no hinge more than maxLift
      if (o.maxLift > 0) for (let k = up ? m : m - 1; up ? k < N : k >= 0; k += sgn) {
        const A = p.pts[up ? k : k + 1], B = p.pts[up ? k + 1 : k];
        const edge = prof.edges.find((c) => sgn * (c.x - A.x) > 0 && sgn * (B.x - c.x) > rho);
        if (!edge) continue;
        if (B.z - pathZ(QE, B.x) <= 0.02) break;
        const t = foldSection(T, QE, o, p.J, p.angles, k, dir, prev);
        if (t) {
          const q = makeChainPose(o, t.M, t.a);
          if (Math.max(...q.pts.slice(1, -1).map((v, i) => v.z - p.pts[i + 1].z)) <= o.maxLift) { q.folded = true; return q; }
        }
        break;
      }
      return p;
    }
    // a split half that leads is held in line: work the target out with it as one unit
    const lead = sideSections(o, sgn);
    if ((o.leadMode === 'straight' || o.leadMode === 'droop') && lead.length > 1) {
      const Lm = lead.reduce((u, k) => u + o.sections[k], 0);
      const om = Object.assign({}, o, up ? { sections: o.sections.slice(0, m).concat([Lm]) } : { sections: [Lm].concat(o.sections.slice(m)), mainJoint: 1 });
      const toMerged = (a) => (up ? a.slice(0, m + 1) : a.slice(m - 1));
      const fromMerged = (a) => (up ? a.slice(0, m).concat(lead.map(() => a[m])) : lead.map(() => a[0]).concat(a.slice(1)));
      const mp = prev && (() => { const a = toMerged(prev.angles); return { angles: a, bends: a.slice(1).map((v, j) => v - a[j]) }; })();
      const t = targetChain(T, QE, J0, om, prof, dir, state.merged || (state.merged = {}), mp);
      const q = makeChainPose(o, t.J, fromMerged(t.angles));
      q.folded = t.folded;
      return q;
    }
    let a0 = drapeChain(T, o, J0);
    // a split trailing half settles, or stays in line as one piece if the hinges reach that sooner
    const ks = sideSections(o, -sgn);
    if (ks.length > 1 && (o.trailMode === 'nearest' || o.trailMode === 'straight') && (prev || o.trailMode === 'straight')) {
      const Ls = ks.reduce((u, k) => u + o.sections[k], 0);
      const th = up ? -restAngleBack(T, J0.x, J0.z, Ls, rho) : restAngle(T, J0.x, J0.z, Ls, rho);
      const b = a0.slice();
      for (const k of ks) b[k] = th;
      a0 = o.trailMode === 'straight' ? b : nearest([{ a: a0 }, { a: b }], prev).a;
    }
    let p = makeChainPose(o, J0, a0);
    // a bend past its limit locks at the limit
    if (!bendsOk(o, p.angles)) {
      const q = solveChainBent(T, o, J0.x, J0.z, p.bends.map((b) => clamp(b, -lim, lim)));
      if (q) p = q;
    }
    const folding = state.chainFolding || (state.chainFolding = {});
    // working out from the seat's hinge, fold the first section that reaches out past
    // an edge with its end in the air (or is already folding over it)
    for (let k = up ? m : m - 1; up ? k < N : k >= 0; k += sgn) {
      const A = p.pts[up ? k : k + 1], B = p.pts[up ? k + 1 : k];
      const edge = prof.edges.find((c) => sgn * (c.x - A.x) > 0 && sgn * (B.x - c.x) > rho);
      if (!edge) { delete folding[k]; continue; }
      if (folding[k] === edge || B.z - pathZ(QE, B.x) > 0.02) {
        const t = foldSection(T, QE, o, p.J, p.angles, k, dir, prev);
        if (t) {
          for (let j = k + sgn; j >= 0 && j < N; j += sgn) delete folding[j];
          folding[k] = edge;
          const q = makeChainPose(o, t.M, t.a);
          q.folded = true;
          return q;
        }
      }
    }
    // once the seat's hinge is over an edge, it stays lifted with both track ends on
    // the stairs until the weight is HOLD past the edge
    const trailEnd = up ? p.R : p.F;
    const tEdge = prof.edges.find((c) => sgn * (p.J.x - c.x) > 0 && sgn * (c.x - trailEnd.x) > 0);
    if (tEdge) {
      const h = chainLift(T, QE, o, J0, null, prev, -sgn);
      if (h) {
        const q = makeChainPose(o, h.M, h.a);
        if (sgn * (centreOfMass(o, q).x - tEdge.x) < HOLD) { q.folded = true; return q; }
      }
    }
    return p;
  }
  // A split leading half keeps its end on the stairs where it can (o.leadMode 'droop'):
  // its outer section is let down onto the stairs about its own hinge, as far as that
  // hinge turns in one step, without lifting the rest of the vehicle.
  function droopLead(T, o, dir, J0, p, prev, ds, rate) {
    const m = o.mainJoint, up = dir === 'up', lead = sideSections(o, up ? 1 : -1);
    if (lead.length < 2) return p;
    const d = settle(T, o, p.J, p.angles, up ? m + 1 : m - 2);
    // the bend between each outer section and the one inside it
    const joints = lead.slice(1).map((k) => (up ? k - 1 : k));
    const betas = p.bends.slice(), maxStep = rad(rate) * ds;
    let changed = false;
    for (const j of joints) {
      let b = d[j + 1] - d[j];
      if (prev) b = prev.bends[j] + clamp(b - prev.bends[j], -maxStep, maxStep);
      if (Math.abs(b - betas[j]) > 1e-9) { betas[j] = b; changed = true; }
    }
    if (!changed) return p;
    const q = solveChainBent(T, o, J0.x, J0.z, betas, p.angles[m]);
    if (!q) return p;
    q.rateLimited = p.rateLimited;
    q.folded = p.folded;
    return q;
  }
  function solveChainStep(T, QE, J0, o, prof, dir, prev, ds, state) {
    let seen = false;
    if (o.bendMode === 'stopGo' && prev && !o.mainHingeSeized && o.laserRisers != null) {
      const hold = solveChainBent(T, o, J0.x, J0.z, prev.bends, prev.angles[o.mainJoint - 1]);
      if (hold) { hold.folded = prev.folded; if (laserWait(o, prof, dir, hold, state)) { hold.held = true; hold.waiting = true; return hold; } seen = !!hold.edgeSeen; }
    }
    const target = targetChain(T, QE, J0, o, prof, dir, state, prev);
    const m = o.mainJoint, stuck = o.mainHingeSeized;
    const extraRate = o.extraHingeRateDegPerM == null ? (o.hingeRateDegPerM * o.unitLength) / Math.min(...o.sections) : o.extraHingeRateDegPerM;
    const done = (p) => (o.leadMode === 'droop' && o.reach === 'lift' ? droopLead(T, o, dir, J0, p, prev, ds, extraRate) : p);
    if (!prev && !stuck) return done(target);
    if (o.bendMode === 'stopGo' && !stuck) {
      const full = done(target);
      const toward = (t) => () => {
        const betas = prev.bends.map((b, j) => b + t * (full.bends[j] - b));
        const q = solveChainBent(T, o, J0.x, J0.z, betas, prev.angles[m - 1] + betas[m - 1]);
        if (q) q.folded = target.folded;
        return q;
      };
      const q = guardedMove(T, o, [() => full, toward(0.75), toward(0.5), toward(0.25), toward(0)]);
      if (o.laserRisers != null) q.laser = laserDrop(state.T, o, q, dir);
      if (seen) q.edgeSeen = true;
      return q;
    }
    // a seized seat's hinge stays straight; the others still go for their targets
    const want = stuck ? target.bends.map((b, j) => (j === m - 1 ? 0 : b)) : target.bends;
    // How far each hinge gets towards its target this step, as a share of the way.
    // 'lead': the seat's hinge goes as fast as it can and the others keep up with it,
    // never getting further along than it; 'together': all cover the same share, as
    // much as the slowest allows; 'own': each as fast as it can.
    const own = want.map((b, j) => {
      const maxStep = rad(j === m - 1 ? o.hingeRateDegPerM : extraRate) * ds, d = prev ? Math.abs(b - prev.bends[j]) : 0;
      return d > maxStep + 1e-9 ? maxStep / d : 1;
    });
    const shares = o.hingeControl === 'own' ? own
      : o.hingeControl === 'together' ? own.map(() => Math.min(...own))
      : own.map((sh, j) => (j === m - 1 ? sh : Math.min(sh, own[m - 1])));
    const share = Math.min(...shares);
    if (share >= 1 && !stuck) return done(target);
    const betas = prev ? want.map((b, j) => prev.bends[j] + shares[j] * (b - prev.bends[j])) : want;
    // with room to rock, it may stay where the section behind the seat's hinge was
    const q = solveChainBent(T, o, J0.x, J0.z, betas, prev ? prev.angles[m - 1] + betas[m - 1] : undefined);
    if (!q) return done(target);
    q.rateLimited = share < 1;
    q.folded = target.folded;
    return done(q);
  }

  // One rigid track the same overall length as the two units.
  function solveRigid(T, J0, o, prev) {
    return solveBent(T, J0.x, J0.z, 0, o, prev ? prev.a1 : undefined);
  }

  function pose(o, xJ, zJ, a1, a2) {
    const L = o.unitLength;
    const J = { x: xJ, z: zJ };
    const R = { x: xJ - L * Math.cos(a1), z: zJ - L * Math.sin(a1) };
    const F = { x: xJ + L * Math.cos(a2), z: zJ + L * Math.sin(a2) };
    return finishPose(o, { J, R, F, a1, a2, beta: a2 - a1 });
  }
  // Seat attitude and pivot for a vehicle pose; a1 and a2 are the sections either side
  // of the hinge that carries the seat.
  function finishPose(o, p) {
    const avg = (p.a1 + p.a2) / 2; // pitch-averaging mast
    // seat tilt if the levelling drive keeps up (the travel loop applies its speed limit)
    const psiRel = o.mastMode === 'balance' ? o._psiRel || 0 : 0; // balance arm: its last lean
    const lean = (o.mastMode === 'base' ? p.a1 : avg) + psiRel;
    const lam = o.levelLockDeg != null ? rad(o.levelLockDeg) : o.levelSeat ? clamp(lean, -rad(o.levelLimitDeg), rad(o.levelLimitDeg)) : 0;
    Object.assign(p, { pitch: avg, psiRel, lam, phi: lean - lam });
    placePivot(o, p);
    return p;
  }
  const unitsOf = (p) => p.units || [[p.R, p.J], [p.J, p.F]];

  // --------------------------------------------------------------- checks
  function segPointDist(ax, az, bx, bz, px, pz) {
    const ex = bx - ax, ez = bz - az, l2 = ex * ex + ez * ez;
    let t = l2 > 1e-18 ? ((px - ax) * ex + (pz - az) * ez) / l2 : 0;
    t = Math.max(0, Math.min(1, t));
    const cx = ax + t * ex, cz = az + t * ez;
    return { d: Math.hypot(px - cx, pz - cz), cx, cz };
  }

  // Closest points between segments P1-P2 and Q1-Q2.
  function closestSegSeg(p1x, p1z, p2x, p2z, q1x, q1z, q2x, q2z) {
    const dx = p2x - p1x, dz = p2z - p1z, ex = q2x - q1x, ez = q2z - q1z;
    const rx = p1x - q1x, rz = p1z - q1z;
    const a = dx * dx + dz * dz, e = ex * ex + ez * ez, f = ex * rx + ez * rz;
    const c = dx * rx + dz * rz, b = dx * ex + dz * ez, den = a * e - b * b;
    let s = den > 1e-12 ? Math.min(1, Math.max(0, (b * f - c * e) / den)) : 0;
    let t = (b * s + f) / e;
    if (t < 0) { t = 0; s = Math.min(1, Math.max(0, -c / a)); }
    else if (t > 1) { t = 1; s = Math.min(1, Math.max(0, (b - c) / a)); }
    const px = p1x + dx * s, pz = p1z + dz * s, qx = q1x + ex * t, qz = q1z + ez * t;
    return { d: Math.hypot(px - qx, pz - qz), qx, qz, t };
  }

  // Where one unit (axle segment A-B grown by rho) touches the real stairs.
  // Where a stretch of track touches the stairs, or comes within tol of them. The
  // stretch runs through the points P; P[0] and P[last] are its end sprockets. Hinges
  // inside it are held by their drives: in a straight run they count as track, not as
  // ends, and where the run bends they count as ends only if they actually touch.
  function trackContacts(T, P, rho, tol) {
    const out = [];
    let lo = Infinity, hi = -Infinity;
    for (const Q of P) { lo = Math.min(lo, Q.x); hi = Math.max(hi, Q.x); }
    lo -= rho + tol; hi += rho + tol;
    const add = (x, z, v) => out.push({ x, z, nosing: !!(v && v.convex) });
    const ends = [P[0], P[P.length - 1]];
    const kinks = [];
    for (let k = 1; k + 1 < P.length; k++) {
      const a1 = Math.atan2(P[k].z - P[k - 1].z, P[k].x - P[k - 1].x), a2 = Math.atan2(P[k + 1].z - P[k].z, P[k + 1].x - P[k].x);
      if (Math.abs(a2 - a1) > rad(1)) kinks.push(P[k]);
    }
    for (const e of T.E) {
      if (e.x1 < lo || e.x0 > hi) continue;
      let c = null;
      for (let k = 0; k + 1 < P.length; k++) {
        const q = closestSegSeg(P[k].x, P[k].z, P[k + 1].x, P[k + 1].z, e.A.x, e.A.z, e.B.x, e.B.z);
        if (!c || q.d < c.d) c = q;
      }
      if (c.d > rho + tol) continue;
      add(c.qx, c.qz, c.t < 1e-6 ? e.A : c.t > 1 - 1e-6 ? e.B : null);
      // a track lying along an edge touches it over a stretch: record both ends of it
      for (const Q of ends) {
        const q = segPointDist(e.A.x, e.A.z, e.B.x, e.B.z, Q.x, Q.z);
        if (q.d <= rho + tol) add(q.cx, q.cz, null);
      }
      for (const Q of kinks) {
        const q = segPointDist(e.A.x, e.A.z, e.B.x, e.B.z, Q.x, Q.z);
        if (q.d <= rho + Math.min(tol, SETTLE)) add(q.cx, q.cz, null);
      }
      for (const v of [e.A, e.B]) {
        for (let k = 0; k + 1 < P.length; k++) if (segPointDist(P[k].x, P[k].z, P[k + 1].x, P[k + 1].z, v.x, v.z).d <= rho + tol) { add(v.x, v.z, v); break; }
      }
    }
    // de-duplicate vertices shared by two edges
    return out.filter((q, i) => out.findIndex((r) => Math.hypot(r.x - q.x, r.z - q.z) < 1e-6) === i);
  }
  const unitContacts = (T, A, B, rho, tol) => trackContacts(T, [A, B], rho, tol);
  // The track behind the seat's hinge and the track ahead of it, as lines of points.
  const halvesOf = (p) => (p.pts ? [p.pts.slice(0, p.m + 1), p.pts.slice(p.m)] : [[p.R, p.J], [p.J, p.F]]);
  const contactsOf = (T, p, rho, tol) => halvesOf(p).flatMap((P) => trackContacts(T, P, rho, tol));

  // T: real steps. TR: nosing line the tracks ride on (support and stability).
  // The centre box's outline in the world: bolted to the section just behind the seat's hinge.
  function boxCorners(o, p) {
    const b = o.box, a = p.a1, c = Math.cos(a), s = Math.sin(a);
    return [[-b.back, b.floor], [b.front, b.floor], [b.front, b.top], [-b.back, b.top]].map(([u, v]) => ({ x: p.J.x + u * c - v * s, z: p.J.z + u * s + v * c }));
  }

  function evaluate(T, TR, o, p) {
    const rho = o.sprocketRadius, tol = 0.004;
    const us = unitsOf(p), N = us.length, [hr, hf] = halvesOf(p);
    const rear = trackContacts(TR, hr, rho, SETTLE), front = trackContacts(TR, hf, rho, SETTLE);
    const all = rear.concat(front);
    const realNosings = (A, B) => T.V.filter((v) => v.convex && segPointDist(A.x, A.z, B.x, B.z, v.x, v.z).d <= rho + tol).length;
    const com = centreOfMass(o, p);
    let minX = Infinity, maxX = -Infinity;
    for (const c of all) { minX = Math.min(minX, c.x); maxX = Math.max(maxX, c.x); }
    const margin = all.length ? Math.min(com.x - minX, maxX - com.x) : -1;
    // If the centre of mass is past the support, the vehicle rocks over the outermost
    // contact until its end on that side lands: that fall is the tip drop.
    let tipDrop = 0;
    if (margin < 0) {
      const end = com.x < minX ? (p.R.x < p.F.x ? p.R : p.F) : (p.R.x < p.F.x ? p.F : p.R);
      tipDrop = Math.max(0, end.z - clearanceZ(TR, end.x, rho));
    }
    // How far the weight's line of action can lean (a push, a hard stop, a bump)
    // before the vehicle falls. Rocking onto a track end within FALL of the stairs
    // only settles it, so those ends count as support here.
    const wide = contactsOf(TR, p, rho, FALL);
    let cLo = null, cHi = null;
    for (const c of wide) { if (!cLo || c.x < cLo.x) cLo = c; if (!cHi || c.x > cHi.x) cHi = c; }
    const leanDown = cLo ? Math.atan2(com.x - cLo.x, Math.max(1e-6, com.z - cLo.z)) : -Math.PI / 2;
    const leanUp = cHi ? Math.atan2(cHi.x - com.x, Math.max(1e-6, com.z - cHi.z)) : -Math.PI / 2;
    const tipAngle = Math.min(leanDown, leanUp), tipDir = leanDown < leanUp ? 'downhill' : 'uphill';
    // seat and casualty: gap to the steps, and to the vehicle's own tracks
    let clearance = Infinity, trackClearance = Infinity, hit = null, trackHit = null;
    for (const q of placeSeat(o, p)) {
      const d = segTerrainDist(T, q.ax, q.az, q.bx, q.bz) - q.r;
      if (d < clearance) { clearance = d; hit = q.name; }
      for (let k = 0; k < N; k++) {
        const [A, B] = us[k], unit = k === 0 ? 'rear' : k === N - 1 ? 'front' : 'middle';
        const dt = segSegDist(q.ax, q.az, q.bx, q.bz, A.x, A.z, B.x, B.z) - q.r - rho;
        if (dt < trackClearance) { trackClearance = dt; trackHit = { part: q.name, unit }; }
      }
    }
    // centre box: gap to the steps, and to the seat and casualty above it
    let boxClearance = null, boxSeat = null;
    if (o.box) {
      const bc = boxCorners(o, p), seat = placeSeat(o, p);
      boxClearance = Infinity; boxSeat = Infinity;
      for (let k = 0; k < 4; k++) {
        const A = bc[k], B = bc[(k + 1) % 4];
        boxClearance = Math.min(boxClearance, segTerrainDist(T, A.x, A.z, B.x, B.z));
        for (const q of seat) boxSeat = Math.min(boxSeat, segSegDist(q.ax, q.az, q.bx, q.bz, A.x, A.z, B.x, B.z) - q.r);
      }
    }
    return {
      rear, front, boxClearance, boxSeat,
      rearNosings: p.units ? null : realNosings(p.R, p.J),
      frontNosings: p.units ? null : realNosings(p.J, p.F),
      com, support: [minX, maxX], margin, tipDrop, clearance, closest: hit, trackClearance, trackHit, tipAngle, tipDir,
      // bending the seat's weight puts on the mast at the hinge axle, and on the levelling drive
      mastMoment: seatModel(o).mass * G * (com.load.x - p.J.x),
      levelMoment: seatModel(o).mass * G * (com.load.x - p.P.x),
      armTorques: p.arms ? (() => {
        const W = seatModel(o).mass * G, A = p.arms;
        const span = Math.max(1e-6, A.T2.x - A.T1.x);
        const f2 = clamp((W * (com.load.x - A.T1.x)) / span, -3 * W, 3 * W), f1 = W - f2; // vertical loads on the two pins
        return [f1 * (A.T1.x - A.B1.x), f2 * (A.T2.x - A.B2.x)];
      })() : null,
    };
  }

  // ----------------------------------------------------------- whole trip
  function simulate(opts, step = 0.01) {
    const o = Object.assign({}, DEFAULTS, opts);
    // stopGo: the vehicle waits while the hinges and the levelling move, so per metre they are
    // unlimited. A track that can't bend has nothing to stop for: it rocks over the edges as it
    // drives, so its levelling keeps the rate it has on the move.
    let oOne = o;
    if (o.bendMode === 'stopGo') {
      oOne = Object.assign({}, o);
      Object.assign(o, { hingeRateDegPerM: 1e6, extraHingeRateDegPerM: 1e6, levelRateDegPerM: 1e6 });
    }
    const prof = stairProfile(o.height, stairsOf(o));
    const T = makeTerrain(prof); // the real steps: payload clearance, nosing count
    const TR = makeTerrain({ pts: prof.ride }); // nosing line with real floors and first risers
    const L = o.unitLength, rho = o.sprocketRadius;
    const xa = -(1.2 + L + rho), xb = prof.xP0 + L + rho + 0.5;
    const Q = sprocketPath(makeTerrain({ pts: prof.pitch }), rho, xa - L - 1, xb + L + 1); // hinge path
    const QE = sprocketPath(TR, rho, xa - L - 1, xb + L + 1); // outer track ends
    // hinge path from xa to xb, resampled every `step` metres of travel
    const i0 = Math.round((xa - Q.x0) / Q.dx), i1 = Math.round((xb - Q.x0) / Q.dx);
    const path = [];
    let sAcc = 0, next = 0;
    for (let i = i0; i <= i1; i++) {
      if (i > i0) sAcc += Math.hypot(Q.X[i] - Q.X[i - 1], Q.Z[i] - Q.Z[i - 1]);
      if (sAcc >= next - 1e-12) { path.push({ s: sAcc, x: Q.X[i], z: Q.Z[i] }); next += step; }
    }
    const out = { opts: o, profile: prof, terrain: T, path, seat: seatModel(o), up: [], down: [], rigidUp: [], rigidDown: [] };
    const sum = (ls) => ls.reduce((u, v) => u + v, 0);
    const seized = o.sections && o.extraHingeSeized ? Object.assign({}, o, { sections: [sum(o.sections.slice(0, o.mainJoint)), sum(o.sections.slice(o.mainJoint))], mainJoint: 1 }) : null;
    const withOne = o.oneTrack !== false; // oneTrack: false skips the one-long-track comparison
    const rigid = [];
    let prev = null;
    if (withOne) for (const J0 of path) {
      const r = solveRigid(TR, J0, o, prev);
      r.s = J0.s;
      prev = r;
      rigid.push(r);
    }
    for (const dir of o.dirs || ['up', 'down']) {
      const seq = dir === 'up' ? path.map((_, i) => i) : path.map((_, i) => path.length - 1 - i);
      const res = new Array(path.length);
      const state = { folding: null, T };
      let last = null, lam = null, psi = null, arms = null;
      o._psiRel = 0; o._twoArmOff = null;
      for (const i of seq) {
        let h;
        if (!o.sections) h = solveHinged(TR, QE, path[i], o, prof, dir, last, step, state);
        else if (!seized) h = solveChainStep(TR, QE, path[i], o, prof, dir, last, step, state);
        else { // each split half moves as one piece
          Object.assign(seized, { _psiRel: o._psiRel, _twoArmOff: o._twoArmOff });
          const g = solveChainStep(TR, QE, path[i], seized, prof, dir, last && last.merged, step, state);
          const a = o.sections.map((_, k) => (k < o.mainJoint ? g.a1 : g.a2));
          h = Object.assign(makeChainPose(o, g.J, a), { merged: g, folded: g.folded, rateLimited: g.rateLimited });
        }
        h.s = path[i].s;
        if (o.mastMode === 'balance') { balanceArm(T, TR, o, h, psi, step); psi = o._psiRel = h.psiRel; }
        if (o.mastMode === 'twoArm' || o.mastMode === 'vArms') { twoArms(T, TR, o, h, arms, step); arms = h.arms; o._twoArmOff = { dx: h.P.x - h.J.x, dz: h.P.z - h.J.z }; }
        level(o, h, lam, step);
        lam = h.lam;
        res[i] = Object.assign(h, { ev: evaluate(T, TR, o, h) });
        last = h;
      }
      out[dir] = res;
      if (!withOne) continue;
      // one long track: the same poses either way, but the seat levelling lags behind
      // in the direction of travel
      const one = new Array(path.length);
      lam = null; psi = null; arms = null;
      for (const i of seq) {
        const q = Object.assign({}, rigid[i]);
        delete q.arms;
        if (o.mastMode === 'balance') { balanceArm(T, TR, o, q, psi, step); psi = q.psiRel; }
        if (o.mastMode === 'twoArm' || o.mastMode === 'vArms') { twoArms(T, TR, o, q, arms, step); arms = q.arms; }
        level(oOne, q, lam, step);
        lam = q.lam;
        q.ev = evaluate(T, TR, o, q);
        one[i] = q;
      }
      out[dir === 'up' ? 'rigidUp' : 'rigidDown'] = one;
    }
    const sm = (ps) => summarise(ps, o, prof, step);
    if (o.dirs) { // one direction only
      out.summary = {};
      for (const dir of o.dirs) out.summary[dir] = sm(out[dir]);
      return out;
    }
    out.summary = { up: sm(out.up), down: sm(out.down) };
    out.summary.two = worstOf(out.summary.up, out.summary.down);
    if (withOne) {
      Object.assign(out.summary, { rigidUp: sm(out.rigidUp), rigidDown: sm(out.rigidDown) });
      out.summary.rigid = worstOf(out.summary.rigidUp, out.summary.rigidDown);
    }
    return out;
  }

  function summarise(poses, o, prof, step = 0.01) {
    let maxHinge = 0, maxPitch = 0, minMargin = Infinity, minClear = Infinity, maxJump = 0, jumpAt = null, minNosings = Infinity;
    let maxDrop = 0, dropAt = null, maxTilt = 0, maxTiltJump = 0, maxLevel = 0, minTrack = Infinity, closest = null, trackHit = null;
    let maxMast = 0, maxLevelM = 0, minTip = Infinity, tipAt = null, tipDir = null, maxLink = 0, maxArmT = 0, maxOther = 0;
    let minBox = Infinity, minBoxSeat = Infinity;
    const win = Math.max(1, Math.round(0.1 / step)); // samples in 10 cm of travel
    for (let i = 0; i < poses.length; i++) {
      const p = poses[i];
      maxHinge = Math.max(maxHinge, Math.abs(p.beta));
      maxPitch = Math.max(maxPitch, Math.abs(p.pitch));
      minMargin = Math.min(minMargin, p.ev.margin);
      if (p.ev.tipDrop > maxDrop) { maxDrop = p.ev.tipDrop; dropAt = p.s; }
      if (p.ev.clearance < minClear) { minClear = p.ev.clearance; closest = p.ev.closest; }
      if (p.ev.trackClearance < minTrack) { minTrack = p.ev.trackClearance; trackHit = p.ev.trackHit; }
      maxTilt = Math.max(maxTilt, Math.abs(p.phi));
      maxMast = Math.max(maxMast, Math.abs(p.ev.mastMoment));
      if (p.ev.boxClearance != null) { minBox = Math.min(minBox, p.ev.boxClearance); minBoxSeat = Math.min(minBoxSeat, p.ev.boxSeat); }
      if (p.bends) p.bends.forEach((b, j) => { if (j !== o.mainJoint - 1) maxOther = Math.max(maxOther, Math.abs(b)); });
      if (p.ev.armTorques) maxArmT = Math.max(maxArmT, Math.abs(p.ev.armTorques[0]), Math.abs(p.ev.armTorques[1]));
      // the averaging diamond opens to 90 degrees minus the bend: link force M / (2 arm cos(bend))
      maxLink = Math.max(maxLink, Math.abs(p.ev.mastMoment) / (2 * LINK_ARM * Math.max(0.2, Math.cos(p.beta))));
      if (p.ev.tipAngle < minTip) { minTip = p.ev.tipAngle; tipAt = p.s; tipDir = p.ev.tipDir; }
      maxLevelM = Math.max(maxLevelM, Math.abs(p.ev.levelMoment));
      maxLevel = Math.max(maxLevel, Math.abs(p.lam));
      if (i >= win) {
        const jmp = Math.abs(p.pitch - poses[i - win].pitch);
        if (jmp > maxJump) { maxJump = jmp; jumpAt = p.s; }
        maxTiltJump = Math.max(maxTiltJump, Math.abs(p.phi - poses[i - win].phi));
      }
      // A unit lying along a flight should always sit on two or more nosings.
      const rho = o.sprocketRadius;
      const within = (a, b) => [[0, prof.xL0], [prof.xL1, prof.xP0]].some(([lo, hi]) => a - rho >= lo && b + rho <= hi);
      const pitchAt = (x) => (x < prof.xL1 ? prof.pitchLower : prof.pitchUpper);
      const straight = Math.abs(p.beta) < rad(0.5);
      if (!p.units && straight && within(p.R.x, p.J.x) && Math.abs(p.a1 - pitchAt(p.R.x)) < rad(0.5)) minNosings = Math.min(minNosings, p.ev.rearNosings);
      if (!p.units && straight && within(p.J.x, p.F.x) && Math.abs(p.a2 - pitchAt(p.F.x)) < rad(0.5)) minNosings = Math.min(minNosings, p.ev.frontNosings);
    }
    return {
      maxHingeDeg: deg(maxHinge), maxPitchDeg: deg(maxPitch),
      minMargin, minClearance: minClear, closestPart: closest, minTrackClearance: minTrack, trackHit,
      maxTipDrop: maxDrop, tipDropAt: dropAt,
      maxPitchChangePer10cmDeg: deg(maxJump), worstAt: jumpAt,
      maxSeatTiltDeg: deg(maxTilt), maxSeatTiltChangePer10cmDeg: deg(maxTiltJump), maxLevelDeg: deg(maxLevel),
      maxMastMoment: maxMast, maxLevelMoment: maxLevelM,
      minTipAngleDeg: deg(minTip), tipAngleAt: tipAt, tipAngleDir: tipDir, maxLinkForce: maxLink, maxArmTorque: maxArmT, maxOtherHingeDeg: deg(maxOther),
      minNosingsOnFlight: minNosings === Infinity ? null : minNosings,
      minBoxClearance: minBox === Infinity ? null : minBox, minBoxSeat: minBoxSeat === Infinity ? null : minBoxSeat,
    };
  }

  // Worst case of two summaries (for example up and down).
  function worstOf(a, b) {
    const out = {};
    for (const k of Object.keys(a)) {
      const x = a[k], y = b[k];
      if (typeof x !== 'number' || typeof y !== 'number') { out[k] = x; continue; }
      out[k] = /^min/.test(k) ? Math.min(x, y) : Math.max(x, y);
    }
    out.closestPart = a.minClearance <= b.minClearance ? a.closestPart : b.closestPart;
    out.trackHit = a.minTrackClearance <= b.minTrackClearance ? a.trackHit : b.trackHit;
    out.tipAngleDir = a.minTipAngleDeg <= b.minTipAngleDeg ? a.tipAngleDir : b.tipAngleDir;
    return out;
  }

  // Hand-calculation stresses in the seat support ("column and cradle") at twice the
  // worst steady load, to allow for bumps. Steel S355: yield 355 MPa, shear 205 MPa.
  // sm: a run summary (worst of up and down) for these options.
  const SUPPORT = { dyn: 2, fy: 355e6, fs: 205e6, col: [0.05, 0.004], colGap: 0.4, rod: 0.012,
    rail: [0.04, 0.003], hingeAxle: 0.04, hingeAxleArm: 0.08, tiltAxle: 0.03 };
  function structure(opts, sm) {
    const o = Object.assign({}, DEFAULTS, opts), S = SUPPORT, seat = seatModel(o), W = seat.mass * G;
    const boxZ = ([b, t]) => (b ** 4 - (b - 2 * t) ** 4) / 12 / (b / 2);
    const Mcol = S.dyn * sm.maxMastMoment;
    const link = (S.dyn * sm.maxLinkForce) / 2; // two diamonds, one each side
    // cradle: each half of the load cantilevers from the tilt axle
    let head = 0, feet = 0;
    for (const q of seat.masses) { const m = q.m * G * q.p.u; if (m > 0) head += m; else feet -= m; }
    const Mrail = S.dyn * Math.max(head, feet);
    const Mhinge = S.dyn * ((W + o.unitMass * G) / 2) * S.hingeAxleArm;
    const members = [
      { part: 'Columns', size: '2 × 50 × 50 × 4 mm box tube, 0.4 m apart', load: `${Mcol.toFixed(0)} N·m bend`, stress: Mcol / (2 * boxZ(S.col)), limit: S.fy },
      { part: 'Averaging links', size: '12 mm rods, a diamond each side', load: `${(link / 1000).toFixed(1)} kN each`, stress: link / (Math.PI * S.rod ** 2 / 4), limit: S.fy },
      { part: 'Cradle rails', size: '2 × 40 × 40 × 3 mm box tube', load: `${Mrail.toFixed(0)} N·m bend`, stress: Mrail / (2 * boxZ(S.rail)), limit: S.fy },
      { part: 'Hinge axle', size: '40 mm solid bar', load: `${Mhinge.toFixed(0)} N·m bend`, stress: Mhinge / (Math.PI * S.hingeAxle ** 3 / 32), limit: S.fy },
      { part: 'Tilt axle', size: '30 mm bar, double shear', load: `${(S.dyn * W / 1000).toFixed(1)} kN`, stress: (S.dyn * W) / (2 * Math.PI * S.tiltAxle ** 2 / 4), limit: S.fs },
    ];
    if (o.mastMode === 'twoArm' || o.mastMode === 'vArms') {
      // each arm is a pair of box tubes (left and right); its drive holds the arm's moment
      const Marm = S.dyn * sm.maxArmTorque;
      members.splice(0, 2,
        { part: 'Arms', size: '2 pairs of 40 × 40 × 4 mm box tube', load: `${Marm.toFixed(0)} N·m bend`, stress: Marm / (2 * boxZ([0.04, 0.004])), limit: S.fy });
      members.splice(members.findIndex((m) => m.part === 'Tilt axle'), 1,
        { part: 'Cradle pins', size: '25 mm bars, double shear', load: `${(S.dyn * W / 1000).toFixed(1)} kN`, stress: (S.dyn * W) / (2 * Math.PI * 0.025 ** 2 / 4), limit: S.fs });
    }
    for (const m of members) m.factor = m.limit / m.stress;
    const an = analyse(o);
    if (o.mastMode === 'twoArm' || o.mastMode === 'vArms') {
      return { members, drives: [
        { part: 'Hinge motor', need: `${(S.dyn * an.hingeTorque).toFixed(0)} N·m`, note: 'self-locking; holds a fold with the power off' },
        { part: 'Arm drives', need: `${(S.dyn * sm.maxArmTorque).toFixed(0)} N·m each`, note: 'two, self-locking; they level the cradle and move it fore and aft' },
        { part: 'Track drives', need: `${an.sprocketTorque.toFixed(0)} N·m, ${an.drivePower.toFixed(0)} W`, note: 'per unit and in total, at 0.25 m/s; spring brakes' },
      ] };
    }
    const drives = [
      { part: 'Hinge motor', need: `${(S.dyn * an.hingeTorque).toFixed(0)} N·m`, note: 'self-locking; holds a fold with the power off' },
      ...(o.mastMode === 'balance' ? [{ part: 'Arm drive', need: `${(S.dyn * sm.maxMastMoment).toFixed(0)} N·m`, note: 'self-locking; leans the arm to keep the weight away from the edges' }] : []),
      { part: 'Seat tilt drives', need: `${Math.max(S.dyn * sm.maxLevelMoment, an.levelTorque).toFixed(0)} N·m each`, note: 'two, self-locking; either one holds the seat alone' },
      { part: 'Track drives', need: `${an.sprocketTorque.toFixed(0)} N·m, ${an.drivePower.toFixed(0)} W`, note: 'per unit and in total, at 0.25 m/s; spring brakes' },
    ];
    return { members, drives };
  }

  // Closed-form checks from the stair and track dimensions.
  function analyse(opts) {
    const o = Object.assign({}, DEFAULTS, opts);
    const st = stairsOf(o), s = stairProfile(o.height, st);
    const g = st.going;
    const nosing = Math.max(Math.hypot(g, st.rise), s.nUp ? Math.hypot(g, s.rUp) : 0);
    const pitch = Math.max(s.pitchLower, s.pitchUpper);
    const L = o.unitLength, rho = o.sprocketRadius;
    const seat = seatModel(o);
    const extraMass = o.sections ? (o.sections.length - 2) * o.extraHingeMass : 0; // motors at the extra hinges
    const M = seat.mass + 2 * o.unitMass + extraMass + (o.boxMass || 0);
    // On a slope the centre of mass slides downhill by (its height above the track) x
    // sin(pitch). A level seat keeps its own centre of mass over the pivot, so only the
    // mast height counts; a fixed seat leans with the vehicle and its full height counts.
    const loadLever = o.seatHeight + (o.levelSeat ? 0 : seat.com.v);
    const comAboveTrack = rho + (seat.mass * loadLever) / M;
    const tipRatio = L / comAboveTrack; // CoM over the hinge, rear contact one unit behind
    const minRate = deg(pitch) / L; // fold the full pitch within one unit length of travel
    const traction = M * G * Math.sin(pitch); // N the tracks push (or brake) on the slope
    return {
      nosingSpacing: nosing,
      pitchDeg: deg(pitch),
      minUnitLength: 2 * nosing,
      unitOverall: (o.sections ? Math.max(...o.sections) : L) + 2 * rho,
      shortestSection: o.sections ? Math.min(...o.sections) : L,
      totalLength: (o.sections ? o.sections.reduce((u, v) => u + v, 0) : 2 * L) + 2 * rho,
      extraMass,
      loadMass: seat.mass,
      totalMass: M,
      seatComAbovePivot: seat.com.v,
      comAboveTrack,
      tipRatio,
      tipNeed: 1.5 * Math.tan(pitch),
      maxComAboveTrack: L / (1.5 * Math.tan(pitch)),
      minRate,
      traction,
      drivePower: traction * o.speed, // W at the tracks
      sprocketTorque: (traction / 2) * rho, // N m per unit
      // Folded over an edge the vehicle stands on its two outer track ends and the hinge
      // holds up the middle: seat plus half of each unit, at half a unit length.
      hingeTorque: (seat.mass + o.unitMass) * G * (L / 2),
      // The seat's centre of mass sits above its pivot, so a seat left tilted by the full
      // pitch pulls on the levelling drive with this torque.
      levelTorque: seat.mass * G * seat.com.v * Math.sin(pitch),
      // Side to side: the vehicle stands on its left and right tracks. It tips sideways
      // once a side tilt carries the centre of mass past the outer track edge.
      comHeight: rho + (seat.mass * (o.seatHeight + seat.com.v)) / M,
      sideTipDeg: deg(Math.atan(o.vehicleWidth / 2 / (rho + (seat.mass * (o.seatHeight + seat.com.v)) / M))),
      friction: Math.tan(pitch),
      checks: [
        { id: 'support', ok: L >= 2 * nosing },
        { id: 'landing', ok: L + 2 * rho <= STAIRS.landing },
        { id: 'hinge', ok: o.hingeLimitDeg >= 45 },
        { id: 'rate', ok: o.hingeRateDegPerM >= 1.5 * minRate },
        { id: 'tip', ok: tipRatio >= 1.5 * Math.tan(pitch) },
      ],
    };
  }

  return { STAIRS, DEFAULTS, SUPPORT, LINK_ARM, armFeet, boxCorners, stairProfile, makeTerrain, groundZ, clearanceZ, restAngle, restAngleBack,
    sprocketPath, solveHinged, solveRigid, evaluate, simulate, analyse, structure, seatModel, placeSeat, deg, rad };
});
