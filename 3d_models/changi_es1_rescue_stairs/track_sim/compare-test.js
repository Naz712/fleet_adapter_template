#!/usr/bin/env node
// Head-to-head run of the two-section vehicle and the one with its front half split in
// two, both with the balancing seat arm, at all three height settings and both ways.
// Writes compare-results.js for compare.html; the case-by-case stress results come
// from stress-test.js (stress-results.js).
//
//   node compare-test.js
const fs = require('fs');
const path = require('path');
const TM = require('./track-model.js');

const DESIGNS = [
  { id: 'frontSplit', name: 'Front half split', opts: { mastMode: 'balance', sections: [0.7, 0.35, 0.35], mainJoint: 1 } },
  { id: 'two', name: 'Two sections', opts: { mastMode: 'balance' } },
];
const keep = ['minTipAngleDeg', 'tipAngleAt', 'tipAngleDir', 'maxTipDrop', 'maxSeatTiltDeg', 'minClearance', 'minTrackClearance', 'maxHingeDeg', 'maxOtherHingeDeg', 'maxPitchChangePer10cmDeg'];
const pick = (s) => Object.fromEntries(keep.map((k) => [k, s[k]]));

const rows = [];
for (const h of [3.2, 5.8, 8.4]) {
  const row = { height: h };
  for (const d of DESIGNS) {
    const r = TM.simulate(Object.assign({ height: h, oneTrack: false }, d.opts));
    row[d.id] = { up: pick(r.summary.up), down: pick(r.summary.down) };
    console.log(`${h} m  ${d.name.padEnd(17)} lean up ${r.summary.up.minTipAngleDeg.toFixed(1).padStart(5)}°  down ${r.summary.down.minTipAngleDeg.toFixed(1).padStart(5)}°`);
  }
  rows.push(row);
}
const an = Object.fromEntries(DESIGNS.map((d) => [d.id, TM.analyse(d.opts)]));
const out = {
  generated: new Date().toISOString().slice(0, 10),
  designs: DESIGNS.map(({ id, name, opts }) => ({ id, name, opts, totalMass: an[id].totalMass, totalLength: an[id].totalLength })),
  heights: rows,
};
fs.writeFileSync(path.join(__dirname, 'compare-results.js'),
  '// Written by compare-test.js; do not edit by hand.\nwindow.COMPARE_RESULTS = ' + JSON.stringify(out, null, 1) + ';\n');
