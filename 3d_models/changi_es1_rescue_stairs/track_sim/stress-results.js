// Written by stress-test.js; do not edit by hand.
window.STRESS_RESULTS = {
 "hardStopDeg": 7.261554383523292,
 "grip": {
  "hold": 0.6071428571428571,
  "stop": 0.7562103115821974,
  "pitchDeg": 31.263731694377427
 },
 "structure": {
  "normal": {
   "members": [
    {
     "part": "Columns",
     "size": "2 × 50 × 50 × 4 mm box tube, 0.4 m apart",
     "load": "996 N·m bend",
     "stress": 47606515.6841471,
     "limit": 355000000,
     "factor": 7.456962453528488
    },
    {
     "part": "Averaging links",
     "size": "12 mm rods, a diamond each side",
     "load": "1.7 kN each",
     "stress": 14712109.201456862,
     "limit": 355000000,
     "factor": 24.12978282983695
    },
    {
     "part": "Cradle rails",
     "size": "2 × 40 × 40 × 3 mm box tube",
     "load": "613 N·m bend",
     "stress": 60071370.95185361,
     "limit": 355000000,
     "factor": 5.909637059632411
    },
    {
     "part": "Hinge axle",
     "size": "40 mm solid bar",
     "load": "133 N·m bend",
     "stress": 21233815.887548305,
     "limit": 355000000,
     "factor": 16.71861533885556
    },
    {
     "part": "Tilt axle",
     "size": "30 mm bar, double shear",
     "load": "2.8 kN",
     "stress": 2012355.1004539249,
     "limit": 205000000,
     "factor": 101.87068870387655
    }
   ],
   "drives": [
    {
     "part": "Hinge motor",
     "need": "1167 N·m",
     "note": "self-locking; holds a fold with the power off"
    },
    {
     "part": "Seat tilt drives",
     "need": "479 N·m each",
     "note": "two, self-locking; either one holds the seat alone"
    },
    {
     "part": "Track drives",
     "need": "45 N·m, 251 W",
     "note": "per unit and in total, at 0.25 m/s; spring brakes"
    }
   ]
  },
  "heavy": {
   "members": [
    {
     "part": "Columns",
     "size": "2 × 50 × 50 × 4 mm box tube, 0.4 m apart",
     "load": "1730 N·m bend",
     "stress": 82682242.5244043,
     "limit": 355000000,
     "factor": 4.293545858957793
    },
    {
     "part": "Averaging links",
     "size": "12 mm rods, a diamond each side",
     "load": "2.9 kN each",
     "stress": 25551758.274244927,
     "limit": 355000000,
     "factor": 13.8933687533286
    },
    {
     "part": "Cradle rails",
     "size": "2 × 40 × 40 × 3 mm box tube",
     "load": "966 N·m bend",
     "stress": 94748848.62813194,
     "limit": 355000000,
     "factor": 3.7467473762482926
    },
    {
     "part": "Hinge axle",
     "size": "40 mm solid bar",
     "load": "196 N·m bend",
     "stress": 31226199.834629864,
     "limit": 355000000,
     "factor": 11.36865843042178
    },
    {
     "part": "Tilt axle",
     "size": "30 mm bar, double shear",
     "load": "4.4 kN",
     "stress": 3122619.9834629865,
     "limit": 205000000,
     "factor": 65.64999938694267
    }
   ],
   "drives": [
    {
     "part": "Hinge motor",
     "need": "1717 N·m",
     "note": "self-locking; holds a fold with the power off"
    },
    {
     "part": "Seat tilt drives",
     "need": "765 N·m each",
     "note": "two, self-locking; either one holds the seat alone"
    },
    {
     "part": "Track drives",
     "need": "64 N·m, 354 W",
     "note": "per unit and in total, at 0.25 m/s; spring brakes"
    }
   ]
  }
 },
 "generated": "2026-09-28",
 "results": [
  {
   "group": "Baseline",
   "name": "Default design",
   "what": "120 kg person, half lying, seat 0.5 m up, balance arm",
   "opts": {},
   "tipUp": 10.689655910312414,
   "tipDown": 8.287734256456702,
   "drop": 0,
   "tilt": 5.033555710202661,
   "steps": 0.4467728952543756,
   "stepsPart": "backrest",
   "tracks": 0.25451488795117805,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.22818618387216283,
    "tilt": 25.49038332841601,
    "tip": -12.651588743991969
   },
   "level": "pass",
   "why": "takes a 8.3° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Baseline",
   "name": "Arm without its drive",
   "what": "held halfway between the units, the earlier design",
   "opts": {
    "mastMode": "average"
   },
   "tipUp": 8.036321449565781,
   "tipDown": 8.177099304990376,
   "drop": 0,
   "tilt": 5.053139651111426,
   "steps": 0.4859118180271377,
   "stepsPart": "leg rest",
   "tracks": 0.3033538723102307,
   "tracksHit": {
    "part": "leg rest",
    "unit": "rear"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.23633325290796003,
    "tilt": 22.490383328416005,
    "tip": -15.437476410629898
   },
   "level": "pass",
   "why": "takes a 8.0° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Load",
   "name": "200 kg person",
   "what": "two thirds more than planned",
   "opts": {
    "personMass": 200
   },
   "tipUp": 12.413258092690905,
   "tipDown": 7.8460429522386,
   "drop": 0,
   "tilt": 5.033555710202659,
   "steps": 0.4194059099116304,
   "stepsPart": "backrest",
   "tracks": 0.23019759908342438,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.22818618387216283,
    "tilt": 25.490383328416016,
    "tip": -15.272791037525746
   },
   "level": "pass",
   "why": "takes a 7.8° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Load",
   "name": "40 kg person",
   "what": "a child or a small adult",
   "opts": {
    "personMass": 40
   },
   "tipUp": 10.859084268868624,
   "tipDown": 11.501145133013376,
   "drop": 0,
   "tilt": 5.034839444947756,
   "steps": 0.4832020016167473,
   "stepsPart": "leg rest",
   "tracks": 0.29488130137012136,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.23633325290796003,
    "tilt": 24.663731694378527,
    "tip": -10.931041927041855
   },
   "level": "pass",
   "why": "takes a 10.9° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Load",
   "name": "Slides 10 cm towards the feet",
   "what": "held by the harness and foot stop",
   "opts": {
    "comOffset": -0.1
   },
   "tipUp": 11.13052242765377,
   "tipDown": 8.426983070291726,
   "drop": 0,
   "tilt": 5.033555710202661,
   "steps": 0.3796505903679209,
   "stepsPart": "backrest",
   "tracks": 0.19527865352899007,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.23633325290796003,
    "tilt": 24.663731694378534,
    "tip": -11.241276863320062
   },
   "level": "pass",
   "why": "takes a 8.4° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Load",
   "name": "Slides 10 cm towards the head",
   "what": "held by the harness",
   "opts": {
    "comOffset": 0.1
   },
   "tipUp": 11.952498805255264,
   "tipDown": 8.421714733207063,
   "drop": 0,
   "tilt": 5.033555710202661,
   "steps": 0.46497216583265083,
   "stepsPart": "thigh",
   "tracks": 0.28291964048517493,
   "tracksHit": {
    "part": "thigh",
    "unit": "front"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.22818618387216283,
    "tilt": 25.490383328416,
    "tip": -11.06264535240602
   },
   "level": "pass",
   "why": "takes a 8.4° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Load",
   "name": "Slides 25 cm towards the feet",
   "what": "no harness or foot stop",
   "opts": {
    "comOffset": -0.25
   },
   "tipUp": 11.047112454462127,
   "tipDown": 9.580557228053992,
   "drop": 0,
   "tilt": 7.401493882070308,
   "steps": 0.27454173230253864,
   "stepsPart": "backrest",
   "tracks": 0.09420034108483805,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.3085405800942862,
    "tilt": 24.66373169437853,
    "tip": -15.861174106285004
   },
   "level": "pass",
   "why": "takes a 9.6° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Posture",
   "name": "Sitting up",
   "what": "15° recline",
   "opts": {
    "reclineDeg": 15
   },
   "tipUp": 10.96820939547283,
   "tipDown": 8.513939305052384,
   "drop": 0,
   "tilt": 5.033555710202661,
   "steps": 0.24505952078822205,
   "stepsPart": "leg rest",
   "tracks": 0.05768182478077047,
   "tracksHit": {
    "part": "leg rest",
    "unit": "rear"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.22818618387216283,
    "tilt": 25.490383328416016,
    "tip": -12.906361188278828
   },
   "level": "pass",
   "why": "takes a 8.5° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Posture",
   "name": "Lying flat",
   "what": "90° recline",
   "opts": {
    "reclineDeg": 90
   },
   "tipUp": 11.04796732404588,
   "tipDown": 10.038487283440555,
   "drop": 0,
   "tilt": 5.033555710202661,
   "steps": 0.1090574446401652,
   "stepsPart": "backrest",
   "tracks": 0.01627637007092997,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.22818618387216283,
    "tilt": 24.290383328416002,
    "tip": -12.485471172342972
   },
   "level": "warn",
   "why": "fits with only 2 cm to spare"
  },
  {
   "group": "Posture",
   "name": "Lying flat and slides 10 cm towards the feet",
   "what": "the case a single post looks worst for",
   "opts": {
    "reclineDeg": 90,
    "comOffset": -0.1
   },
   "tipUp": 9.602722374113233,
   "tipDown": 8.735122440909144,
   "drop": 0,
   "tilt": 5.033555710202661,
   "steps": 0.05986148738828488,
   "stepsPart": "backrest",
   "tracks": 0.03010393344776252,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.23633325290796003,
    "tilt": 24.663731694378534,
    "tip": -12.943858464718398
   },
   "level": "pass",
   "why": "takes a 8.7° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Stairs",
   "name": "Steeper stairs",
   "what": "250 mm treads, 34.2°",
   "opts": {
    "going": 0.25
   },
   "tipUp": 10.860306508159884,
   "tipDown": 8.459537434545942,
   "drop": 0,
   "tilt": 5.049735551747864,
   "steps": 0.37912284188961387,
   "stepsPart": "backrest",
   "tracks": 0.19807766760080467,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 42.32299297198413,
   "one": {
    "drop": 0.25777511106843587,
    "tilt": 27.542354049517492,
    "tip": -15.538675815731052
   },
   "level": "pass",
   "why": "takes a 8.5° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Stairs",
   "name": "Steepest stairs",
   "what": "180 mm rise, 250 mm treads, 35.8°",
   "opts": {
    "rise": 0.18,
    "going": 0.25
   },
   "tipUp": 9.120351883349674,
   "tipDown": 8.276760908103379,
   "drop": 0,
   "tilt": 4.208255895352068,
   "steps": 0.3316815366218189,
   "stepsPart": "backrest",
   "tracks": 0.15158620396179057,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 45.47105683981243,
   "one": {
    "drop": 0.28218728012645045,
    "tilt": 30.353887254436774,
    "tip": -18.2710332780266
   },
   "level": "pass",
   "why": "takes a 8.3° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Motors",
   "name": "Hinge motor at three-quarter speed",
   "what": "90°/m, or driving a third faster",
   "opts": {
    "hingeRateDegPerM": 90
   },
   "tipUp": 8.531730330909497,
   "tipDown": 9.17707088561966,
   "drop": 0,
   "tilt": 5.101710315470173,
   "steps": 0.42820590414492,
   "stepsPart": "backrest",
   "tracks": 0.23806407616193578,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 39.00888917306952,
   "one": {
    "drop": 0.22818618387216283,
    "tilt": 25.49038332841601,
    "tip": -12.651588743991969
   },
   "level": "pass",
   "why": "takes a 8.5° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Motors",
   "name": "Hinge motor at half speed",
   "what": "60°/m, or driving twice as fast",
   "opts": {
    "hingeRateDegPerM": 60
   },
   "tipUp": 9.433458309529785,
   "tipDown": -10.713544800005598,
   "drop": 0.16516683448794822,
   "tilt": 16.467680724969995,
   "steps": 0.4475573868945574,
   "stepsPart": "backrest",
   "tracks": 0.23911032377721717,
   "tracksHit": {
    "part": "leg rest",
    "unit": "rear"
   },
   "hinge": 35.399999999999984,
   "one": {
    "drop": 0.22818618387216283,
    "tilt": 25.49038332841601,
    "tip": -12.651588743991969
   },
   "level": "fail",
   "why": "rocks over and drops 17 cm"
  },
  {
   "group": "Motors",
   "name": "Seat drive at half speed",
   "what": "75°/m",
   "opts": {
    "levelRateDegPerM": 75
   },
   "tipUp": 11.106649177758342,
   "tipDown": 8.536469176354883,
   "drop": 0,
   "tilt": 6.512893973253578,
   "steps": 0.4467728952543756,
   "stepsPart": "backrest",
   "tracks": 0.25451488795117805,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.22818618387216283,
    "tilt": 29.362662239355462,
    "tip": -12.373889768232564
   },
   "level": "pass",
   "why": "takes a 8.5° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Motors",
   "name": "Hinge range cut to ±45°",
   "what": "a smaller hinge motor",
   "opts": {
    "hingeLimitDeg": 45
   },
   "tipUp": 7.2807102868010425,
   "tipDown": 8.31951779172826,
   "drop": 0,
   "tilt": 5.033555710202661,
   "steps": 0.445029070002278,
   "stepsPart": "backrest",
   "tracks": 0.25296028965093054,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 37.56173960800786,
   "one": {
    "drop": 0.22818618387216283,
    "tilt": 25.49038332841601,
    "tip": -12.651588743991969
   },
   "level": "pass",
   "why": "takes a 7.3° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Failures",
   "name": "Arm drive seizes in the middle",
   "what": "then keeps going",
   "opts": {
    "armLockDeg": 0
   },
   "tipUp": 8.036321449565781,
   "tipDown": 8.177099304990376,
   "drop": 0,
   "tilt": 5.053139651111426,
   "steps": 0.4859118180271377,
   "stepsPart": "leg rest",
   "tracks": 0.3033538723102307,
   "tracksHit": {
    "part": "leg rest",
    "unit": "rear"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.23633325290796003,
    "tilt": 22.490383328416005,
    "tip": -15.437476410629898
   },
   "level": "pass",
   "why": "takes a 8.0° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Failures",
   "name": "Arm drive seizes leaning 20° uphill",
   "what": "then keeps going",
   "opts": {
    "armLockDeg": -20
   },
   "tipUp": 14.487840265234283,
   "tipDown": 9.368399023587969,
   "drop": 0,
   "tilt": 5.033555710202663,
   "steps": 0.44941718904246997,
   "stepsPart": "backrest",
   "tracks": 0.256168534779713,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.31626574206000946,
    "tilt": 22.611307757636457,
    "tip": -20.164944243615594
   },
   "level": "pass",
   "why": "takes a 9.4° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Failures",
   "name": "Arm drive seizes leaning 20° downhill",
   "what": "then keeps going",
   "opts": {
    "armLockDeg": 20
   },
   "tipUp": 9.054332568506059,
   "tipDown": 4.1951913284165006,
   "drop": 0,
   "tilt": 11.611307757635084,
   "steps": 0.41107354660014594,
   "stepsPart": "leg rest",
   "tracks": 0.33257199460650777,
   "tracksHit": {
    "part": "leg rest",
    "unit": "rear"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.41145997362521847,
    "tilt": 22.61130775763646,
    "tip": -25.769195166382975
   },
   "level": "warn",
   "why": "a hard stop at the wrong moment could rock it (takes 4.2°, needs 7.3°)"
  },
  {
   "group": "Failures",
   "name": "Seat drive stuck level",
   "what": "fails on the flat; the arm takes over levelling",
   "opts": {
    "levelLockDeg": 0
   },
   "tipUp": 11.546895257402378,
   "tipDown": 7.43867848807365,
   "drop": 0,
   "tilt": 5.933555710202662,
   "steps": 0.4560296661362757,
   "stepsPart": "backrest",
   "tracks": 0.2760293849718851,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.3518144864260613,
    "tilt": 28.011307757636455,
    "tip": -26.142165322291472
   },
   "level": "pass",
   "why": "takes a 7.4° lean anywhere; a hard stop needs 7.3°"
  },
  {
   "group": "Failures",
   "name": "Seat drive stuck on a flight",
   "what": "fails at 31.6°; the arm takes over levelling",
   "opts": {
    "levelLockDeg": 31.6
   },
   "tipUp": 7.795478850127304,
   "tipDown": 3.3385428800398707,
   "drop": 0,
   "tilt": 5.933555710202662,
   "steps": 0.40756837229133647,
   "stepsPart": "leg rest",
   "tracks": 0.34290637558400006,
   "tracksHit": {
    "part": "leg rest",
    "unit": "rear"
   },
   "hinge": 39.853504194990855,
   "one": {
    "drop": 0.41145997362521847,
    "tilt": 28.011307757636455,
    "tip": -31.703001700346334
   },
   "level": "warn",
   "why": "a hard stop at the wrong moment could rock it (takes 3.3°, needs 7.3°)"
  },
  {
   "group": "Combined",
   "name": "Heavy, half lying, steepest stairs",
   "what": "200 kg, 45°, slid 10 cm to the feet, 35.8° stairs",
   "opts": {
    "personMass": 200,
    "comOffset": -0.1,
    "rise": 0.18,
    "going": 0.25
   },
   "tipUp": 7.281593182021343,
   "tipDown": 6.169784814222091,
   "drop": 0,
   "tilt": 9.429127947676063,
   "steps": 0.23343612407927986,
   "stepsPart": "backrest",
   "tracks": 0.04685242065112244,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 47.01802136752427,
   "one": {
    "drop": 0.28713986777303013,
    "tilt": 27.629133819911843,
    "tip": -21.85010555131527
   },
   "level": "warn",
   "why": "a hard stop at the wrong moment could rock it (takes 6.2°, needs 7.3°)"
  },
  {
   "group": "Combined",
   "name": "Heavy, lying flat, steepest stairs",
   "what": "200 kg, 90°, slid 10 cm to the feet, 35.8° stairs",
   "opts": {
    "personMass": 200,
    "reclineDeg": 90,
    "comOffset": -0.1,
    "rise": 0.18,
    "going": 0.25
   },
   "tipUp": 9.958358971737699,
   "tipDown": 5.42931288236834,
   "drop": 0,
   "tilt": 3.938590348460652,
   "steps": -0.03,
   "stepsPart": "backrest",
   "tracks": -0.025441259585770704,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 44.69963321697183,
   "one": {
    "drop": 0.2871398677730297,
    "tilt": 30.35388725443676,
    "tip": -20.861689712441297
   },
   "level": "fail",
   "why": "the seat or person hits the tracks or steps"
  },
  {
   "group": "Failures",
   "name": "Hinge motor seizes straight",
   "what": "and the tracks keep driving",
   "opts": {},
   "tipUp": -12.651588743991969,
   "tipDown": -12.651588743991969,
   "drop": 0.22818618387216283,
   "tilt": 25.49038332841601,
   "steps": 0.4467728952543756,
   "stepsPart": "backrest",
   "tracks": 0.25451488795117805,
   "tracksHit": {
    "part": "backrest",
    "unit": "front"
   },
   "hinge": 0,
   "level": "fail",
   "why": "behaves like one long track and drops 23 cm at an edge, so the tracks must stop if the hinge stops"
  }
 ]
};
