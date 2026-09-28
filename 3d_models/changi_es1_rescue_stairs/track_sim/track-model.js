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
    speed: 0.25, // m/s: only used to turn rates per metre into rates per second
  };

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
    const key = `${o.reclineDeg}|${o.personMass}|${o.chairMass}`;
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
    const du = -su / mu, dv = w + SEAT.bracket;
    const mv = (p) => V(p.u + du, p.v + dv);
    for (const q of parts) { q.a = mv(q.a); q.b = mv(q.b); }
    for (const q of masses) q.p = mv(q.p);
    masses.push({ p: V(0, 0), m: 0.4 * mc });
    const M = mu + 0.4 * mc;
    const out = { key, parts, masses, mass: M, com: V(0, (sv + mu * dv) / M), person: mp,
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
  function stairProfile(height) {
    const { rise: r, going: g, lowerTreads: n, landing } = STAIRS;
    const zL = (n + 1) * r;
    const xL0 = n * g;
    const xL1 = xL0 + landing;
    const nUp = Math.max(0, Math.round((height - zL) / r));
    const rUp = nUp ? (height - zL) / nUp : 0;
    const H = zL + nUp * rUp;
    const xP0 = xL1 + Math.max(nUp - 1, 0) * g;
    const xP1 = xP0 + STAIRS.topPlatform;
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
  const SETTLE = 0.03; // a track within 3 cm of the surface settles onto it

  function supportMargin(T, o, p) {
    const rho = o.sprocketRadius, tol = SETTLE;
    const cs = unitContacts(T, p.R, p.J, rho, tol).concat(unitContacts(T, p.J, p.F, rho, tol));
    if (!cs.length) return -1;
    const com = centreOfMass(o, p);
    let minX = Infinity, maxX = -Infinity;
    for (const c of cs) { minX = Math.min(minX, c.x); maxX = Math.max(maxX, c.x); }
    return Math.min(com.x - minX, maxX - com.x);
  }

  function centreOfMass(o, p) {
    const s = seatModel(o), m = s.mass, mu = o.unitMass, M = m + 2 * mu;
    const c = Math.cos(p.phi), sn = Math.sin(p.phi);
    const lx = p.P.x + s.com.u * c - s.com.v * sn, lz = p.P.z + s.com.u * sn + s.com.v * c;
    return {
      x: (m * lx + mu * (p.R.x + p.J.x) / 2 + mu * (p.J.x + p.F.x) / 2) / M,
      z: (m * lz + mu * (p.R.z + p.J.z) / 2 + mu * (p.J.z + p.F.z) / 2) / M,
      load: { x: lx, z: lz },
    };
  }

  // The levelling pivot turns the seat back towards level, but only so fast.
  function level(o, p, prevLam, ds) {
    if (!o.levelSeat) { p.lam = 0; p.phi = p.pitch; return; }
    const lim = rad(o.levelLimitDeg), target = clamp(p.pitch, -lim, lim);
    let lam = target;
    if (prevLam !== null) { const mx = rad(o.levelRateDegPerM) * ds; lam = prevLam + clamp(target - prevLam, -mx, mx); }
    p.lam = lam;
    p.phi = p.pitch - lam;
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

  // Follow the target, but the hinge can only bend so fast per metre travelled.
  function solveHinged(T, QE, J0, o, prof, dir, prev, ds, state) {
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

  // One rigid track the same overall length as the two units.
  function solveRigid(T, J0, o, prev) {
    return solveBent(T, J0.x, J0.z, 0, o, prev ? prev.a1 : undefined);
  }

  function pose(o, xJ, zJ, a1, a2) {
    const L = o.unitLength;
    const J = { x: xJ, z: zJ };
    const R = { x: xJ - L * Math.cos(a1), z: zJ - L * Math.sin(a1) };
    const F = { x: xJ + L * Math.cos(a2), z: zJ + L * Math.sin(a2) };
    const avg = (a1 + a2) / 2; // pitch-averaging mast
    const P = { x: xJ - o.seatHeight * Math.sin(avg), z: zJ + o.seatHeight * Math.cos(avg) };
    // seat tilt if the levelling pivot keeps up (the travel loop applies its speed limit)
    const lam = o.levelSeat ? clamp(avg, -rad(o.levelLimitDeg), rad(o.levelLimitDeg)) : 0;
    return { J, R, F, a1, a2, beta: a2 - a1, pitch: avg, P, lam, phi: avg - lam };
  }

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
  function unitContacts(T, A, B, rho, tol) {
    const out = [];
    const lo = Math.min(A.x, B.x) - rho - tol, hi = Math.max(A.x, B.x) + rho + tol;
    const add = (x, z, v) => out.push({ x, z, nosing: !!(v && v.convex) });
    for (const e of T.E) {
      if (e.x1 < lo || e.x0 > hi) continue;
      const c = closestSegSeg(A.x, A.z, B.x, B.z, e.A.x, e.A.z, e.B.x, e.B.z);
      if (c.d > rho + tol) continue;
      add(c.qx, c.qz, c.t < 1e-6 ? e.A : c.t > 1 - 1e-6 ? e.B : null);
      // a track lying along an edge touches it over a stretch: record both ends of it
      for (const P of [A, B]) {
        const q = segPointDist(e.A.x, e.A.z, e.B.x, e.B.z, P.x, P.z);
        if (q.d <= rho + tol) add(q.cx, q.cz, null);
      }
      for (const v of [e.A, e.B]) {
        if (segPointDist(A.x, A.z, B.x, B.z, v.x, v.z).d <= rho + tol) add(v.x, v.z, v);
      }
    }
    // de-duplicate vertices shared by two edges
    return out.filter((q, i) => out.findIndex((r) => Math.hypot(r.x - q.x, r.z - q.z) < 1e-6) === i);
  }

  // T: real steps. TR: nosing line the tracks ride on (support and stability).
  function evaluate(T, TR, o, p) {
    const rho = o.sprocketRadius, tol = 0.004;
    const rear = unitContacts(TR, p.R, p.J, rho, SETTLE);
    const front = unitContacts(TR, p.J, p.F, rho, SETTLE);
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
    // seat and casualty: gap to the steps, and to the vehicle's own tracks
    let clearance = Infinity, trackClearance = Infinity, hit = null, trackHit = null;
    for (const q of placeSeat(o, p)) {
      const d = segTerrainDist(T, q.ax, q.az, q.bx, q.bz) - q.r;
      if (d < clearance) { clearance = d; hit = q.name; }
      for (const [A, B, unit] of [[p.R, p.J, 'rear'], [p.J, p.F, 'front']]) {
        const dt = segSegDist(q.ax, q.az, q.bx, q.bz, A.x, A.z, B.x, B.z) - q.r - rho;
        if (dt < trackClearance) { trackClearance = dt; trackHit = { part: q.name, unit }; }
      }
    }
    return {
      rear, front,
      rearNosings: realNosings(p.R, p.J),
      frontNosings: realNosings(p.J, p.F),
      com, support: [minX, maxX], margin, tipDrop, clearance, closest: hit, trackClearance, trackHit,
      // bending the seat's weight puts on the mast at the hinge axle, and on the levelling drive
      mastMoment: seatModel(o).mass * G * (com.load.x - p.J.x),
      levelMoment: seatModel(o).mass * G * (com.load.x - p.P.x),
    };
  }

  // ----------------------------------------------------------- whole trip
  function simulate(opts, step = 0.01) {
    const o = Object.assign({}, DEFAULTS, opts);
    const prof = stairProfile(o.height);
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
    const withOne = o.oneTrack !== false; // oneTrack: false skips the one-long-track comparison
    const rigid = [];
    let prev = null;
    if (withOne) for (const J0 of path) {
      const r = solveRigid(TR, J0, o, prev);
      r.s = J0.s;
      prev = r;
      rigid.push(r);
    }
    for (const dir of ['up', 'down']) {
      const seq = dir === 'up' ? path.map((_, i) => i) : path.map((_, i) => path.length - 1 - i);
      const res = new Array(path.length);
      const state = { folding: null };
      let last = null, lam = null;
      for (const i of seq) {
        const h = solveHinged(TR, QE, path[i], o, prof, dir, last, step, state);
        h.s = path[i].s;
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
      lam = null;
      for (const i of seq) {
        const q = Object.assign({}, rigid[i]);
        level(o, q, lam, step);
        lam = q.lam;
        q.ev = evaluate(T, TR, o, q);
        one[i] = q;
      }
      out[dir === 'up' ? 'rigidUp' : 'rigidDown'] = one;
    }
    const sm = (ps) => summarise(ps, o, prof, step);
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
    let maxMast = 0, maxLevelM = 0;
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
      if (straight && within(p.R.x, p.J.x) && Math.abs(p.a1 - pitchAt(p.R.x)) < rad(0.5)) minNosings = Math.min(minNosings, p.ev.rearNosings);
      if (straight && within(p.J.x, p.F.x) && Math.abs(p.a2 - pitchAt(p.F.x)) < rad(0.5)) minNosings = Math.min(minNosings, p.ev.frontNosings);
    }
    return {
      maxHingeDeg: deg(maxHinge), maxPitchDeg: deg(maxPitch),
      minMargin, minClearance: minClear, closestPart: closest, minTrackClearance: minTrack, trackHit,
      maxTipDrop: maxDrop, tipDropAt: dropAt,
      maxPitchChangePer10cmDeg: deg(maxJump), worstAt: jumpAt,
      maxSeatTiltDeg: deg(maxTilt), maxSeatTiltChangePer10cmDeg: deg(maxTiltJump), maxLevelDeg: deg(maxLevel),
      maxMastMoment: maxMast, maxLevelMoment: maxLevelM,
      minNosingsOnFlight: minNosings === Infinity ? null : minNosings,
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
    return out;
  }

  // Closed-form checks from the stair and track dimensions.
  function analyse(opts) {
    const o = Object.assign({}, DEFAULTS, opts);
    const s = stairProfile(o.height);
    const g = STAIRS.going;
    const nosing = Math.max(Math.hypot(g, STAIRS.rise), s.nUp ? Math.hypot(g, s.rUp) : 0);
    const pitch = Math.max(s.pitchLower, s.pitchUpper);
    const L = o.unitLength, rho = o.sprocketRadius;
    const seat = seatModel(o);
    const M = seat.mass + 2 * o.unitMass;
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
      unitOverall: L + 2 * rho,
      totalLength: 2 * L + 2 * rho,
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

  return { STAIRS, DEFAULTS, stairProfile, makeTerrain, groundZ, clearanceZ, restAngle, restAngleBack,
    sprocketPath, solveHinged, solveRigid, evaluate, simulate, analyse, seatModel, placeSeat, deg, rad };
});
