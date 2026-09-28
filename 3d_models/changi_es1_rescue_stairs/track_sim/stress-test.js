#!/usr/bin/env node
// Stress test for the two-track stair climber. Runs the vehicle through harder
// conditions than its default design, at all three height settings and in both
// directions, and reports what holds and what does not. It also sizes the parts of
// the seat support at twice the worst load.
//
//   node stress-test.js      prints the results and writes stress-results.js for the page
const fs = require('fs');
const path = require('path');
const TM = require('./track-model.js');

const G = 9.81;
// A hard stop: from walking pace (0.25 m/s) to rest in 0.2 s. It leans the weight by
// atan(deceleration / g); the vehicle must take that anywhere without falling.
const HARD_STOP_DEG = TM.deg(Math.atan(0.25 / 0.2 / G));

const SCENARIOS = [
  { group: 'Baseline', name: 'Default design', what: '120 kg person, half lying, seat 0.5 m up, balance arm', opts: {} },
  { group: 'Baseline', name: 'Arm without its drive', what: 'held halfway between the units, the earlier design', opts: { mastMode: 'average' } },
  { group: 'Load', name: '200 kg person', what: 'two thirds more than planned', opts: { personMass: 200 } },
  { group: 'Load', name: '40 kg person', what: 'a child or a small adult', opts: { personMass: 40 } },
  { group: 'Load', name: 'Slides 10 cm towards the feet', what: 'held by the harness and foot stop', opts: { comOffset: -0.1 } },
  { group: 'Load', name: 'Slides 10 cm towards the head', what: 'held by the harness', opts: { comOffset: 0.1 } },
  { group: 'Load', name: 'Slides 25 cm towards the feet', what: 'no harness or foot stop', opts: { comOffset: -0.25 } },
  { group: 'Posture', name: 'Sitting up', what: '15° recline', opts: { reclineDeg: 15 } },
  { group: 'Posture', name: 'Lying flat', what: '90° recline', opts: { reclineDeg: 90 } },
  { group: 'Posture', name: 'Lying flat and slides 10 cm towards the feet', what: 'the case a single post looks worst for', opts: { reclineDeg: 90, comOffset: -0.1 } },
  { group: 'Stairs', name: 'Steeper stairs', what: '250 mm treads, 34.2°', opts: { going: 0.25 } },
  { group: 'Stairs', name: 'Steepest stairs', what: '180 mm rise, 250 mm treads, 35.8°', opts: { rise: 0.18, going: 0.25 } },
  { group: 'Motors', name: 'Hinge motor at three-quarter speed', what: '90°/m, or driving a third faster', opts: { hingeRateDegPerM: 90 } },
  { group: 'Motors', name: 'Hinge motor at half speed', what: '60°/m, or driving twice as fast', opts: { hingeRateDegPerM: 60 } },
  { group: 'Motors', name: 'Seat drive at half speed', what: '75°/m', opts: { levelRateDegPerM: 75 } },
  { group: 'Motors', name: 'Hinge range cut to ±45°', what: 'a smaller hinge motor', opts: { hingeLimitDeg: 45 } },
  { group: 'Failures', name: 'Arm drive seizes in the middle', what: 'then keeps going', opts: { armLockDeg: 0 } },
  { group: 'Failures', name: 'Arm drive seizes leaning 20° uphill', what: 'then keeps going', opts: { armLockDeg: -20 } },
  { group: 'Failures', name: 'Arm drive seizes leaning 20° downhill', what: 'then keeps going', opts: { armLockDeg: 20 } },
  { group: 'Failures', name: 'Seat drive stuck level', what: 'fails on the flat; the arm takes over levelling', opts: { levelLockDeg: 0 } },
  { group: 'Failures', name: 'Seat drive stuck on a flight', what: 'fails at 31.6°; the arm takes over levelling', opts: { levelLockDeg: 31.6 } },
  { group: 'Combined', name: 'Heavy, half lying, steepest stairs', what: '200 kg, 45°, slid 10 cm to the feet, 35.8° stairs', opts: { personMass: 200, comOffset: -0.1, rise: 0.18, going: 0.25 } },
  { group: 'Combined', name: 'Heavy, lying flat, steepest stairs', what: '200 kg, 90°, slid 10 cm to the feet, 35.8° stairs', opts: { personMass: 200, reclineDeg: 90, comOffset: -0.1, rise: 0.18, going: 0.25 } },
];

function runScenario(sc) {
  const w = { tipUp: Infinity, tipDown: Infinity, drop: 0, tilt: 0, steps: Infinity, stepsPart: '', tracks: Infinity, tracksHit: null, hinge: 0, one: null, sm: null };
  for (const h of [3.2, 5.8, 8.4]) {
    const r = TM.simulate(Object.assign({ height: h }, sc.opts));
    const u = r.summary.up, d = r.summary.down, t = r.summary.two;
    w.tipUp = Math.min(w.tipUp, u.minTipAngleDeg);
    w.tipDown = Math.min(w.tipDown, d.minTipAngleDeg);
    w.drop = Math.max(w.drop, t.maxTipDrop);
    w.tilt = Math.max(w.tilt, t.maxSeatTiltDeg);
    w.hinge = Math.max(w.hinge, t.maxHingeDeg);
    if (t.minClearance < w.steps) { w.steps = t.minClearance; w.stepsPart = t.closestPart; }
    if (t.minTrackClearance < w.tracks) { w.tracks = t.minTrackClearance; w.tracksHit = t.trackHit; }
    // keep the worst loads for the structure check
    if (!w.sm) w.sm = Object.assign({}, t);
    else for (const k of ['maxMastMoment', 'maxLevelMoment', 'maxLinkForce']) w.sm[k] = Math.max(w.sm[k], t[k]);
    const g = r.summary.rigid;
    if (!w.one || g.maxTipDrop > w.one.drop) w.one = { drop: g.maxTipDrop, tilt: g.maxSeatTiltDeg, tip: g.minTipAngleDeg };
  }
  const tip = Math.min(w.tipUp, w.tipDown), gap = Math.min(w.steps, w.tracks);
  let level = 'pass', why = `takes a ${tip.toFixed(1)}° lean anywhere; a hard stop needs ${HARD_STOP_DEG.toFixed(1)}°`;
  if (w.drop > 0.01 || tip < 0) { level = 'fail'; why = `rocks over and drops ${Math.round(w.drop * 100)} cm`; }
  else if (gap < 0) { level = 'fail'; why = 'the seat or person hits the tracks or steps'; }
  else if (tip < HARD_STOP_DEG) { level = 'warn'; why = `a hard stop at the wrong moment could rock it (takes ${tip.toFixed(1)}°, needs ${HARD_STOP_DEG.toFixed(1)}°)`; }
  else if (w.tilt > 20) { level = 'warn'; why = `stays up, but the person tilts ${w.tilt.toFixed(0)}°`; }
  else if (gap < 0.03) { level = 'warn'; why = `fits with only ${Math.round(gap * 100)} cm to spare`; }
  return { tipUp: w.tipUp, tipDown: w.tipDown, drop: w.drop, tilt: w.tilt, steps: w.steps, stepsPart: w.stepsPart,
    tracks: w.tracks, tracksHit: w.tracksHit, hinge: w.hinge, one: w.one, level, why, sm: w.sm };
}

const t0 = Date.now();
const results = SCENARIOS.map((sc) => Object.assign({ group: sc.group, name: sc.name, what: sc.what, opts: sc.opts }, runScenario(sc)));
const base = results[0];
// A seized hinge motor: if the tracks keep driving, it is one long track.
results.push({ group: 'Failures', name: 'Hinge motor seizes straight', what: 'and the tracks keep driving', opts: {},
  tipUp: base.one.tip, tipDown: base.one.tip, drop: base.one.drop, tilt: base.one.tilt, steps: base.steps, stepsPart: base.stepsPart,
  tracks: base.tracks, tracksHit: base.tracksHit, hinge: 0, level: 'fail',
  why: `behaves like one long track and drops ${Math.round(base.one.drop * 100)} cm at an edge, so the tracks must stop if the hinge stops` });

// Grip on the treads: to hold on the slope, and to stop hard going down.
const pitch = Math.atan(TM.DEFAULTS.rise / TM.DEFAULTS.going);
const aStop = 0.25 / 0.2;
const grip = { hold: Math.tan(pitch), stop: Math.tan(pitch) + aStop / (G * Math.cos(pitch)), pitchDeg: TM.deg(pitch) };

// Structure of the column-and-cradle support at twice the worst load, 120 kg and 200 kg.
const heavy = results.find((r) => r.name === '200 kg person');
const structure = {
  normal: TM.structure({}, base.sm),
  heavy: TM.structure({ personMass: 200 }, heavy.sm),
};

const out = { hardStopDeg: HARD_STOP_DEG, grip, structure, generated: new Date().toISOString().slice(0, 10),
  results: results.map(({ sm, ...r }) => r) };
fs.writeFileSync(path.join(__dirname, 'stress-results.js'),
  '// Written by stress-test.js; do not edit by hand.\nwindow.STRESS_RESULTS = ' + JSON.stringify(out, null, 1) + ';\n');

const pad = (s, n) => String(s).padEnd(n);
console.log(`Hard stop from 0.25 m/s in 0.2 s leans the weight ${HARD_STOP_DEG.toFixed(1)}°.\n`);
for (const r of out.results) {
  console.log(`${pad(r.level.toUpperCase(), 5)} ${pad(r.group, 9)} ${pad(r.name, 46)} lean up ${r.tipUp.toFixed(1).padStart(5)}° down ${r.tipDown.toFixed(1).padStart(5)}°  drop ${String(Math.round(r.drop * 100)).padStart(2)} cm  tilt ${r.tilt.toFixed(0).padStart(2)}°  gaps ${Math.round(r.steps * 100)}/${Math.round(r.tracks * 100)} cm  - ${r.why}`);
}
console.log(`\nGrip needed on ${grip.pitchDeg.toFixed(1)}° stairs: ${grip.hold.toFixed(2)} to hold, ${grip.stop.toFixed(2)} for a hard stop going down.`);
for (const [k, s] of Object.entries(structure)) {
  console.log(`\nSupport at twice the worst load (${k === 'normal' ? '120' : '200'} kg):`);
  for (const m of s.members) console.log(`  ${pad(m.part, 16)} ${pad(m.size, 40)} ${pad(m.load, 16)} ${(m.stress / 1e6).toFixed(0).padStart(4)} MPa  (${m.factor.toFixed(1)}x under the limit)`);
  for (const d of s.drives) console.log(`  ${pad(d.part, 16)} needs ${d.need} - ${d.note}`);
}
console.log(`\n${((Date.now() - t0) / 1000).toFixed(0)} s`);
