// Written by stress-test.js; do not edit by hand.
window.STRESS_RESULTS = {
 "hardStopDeg": 7.261554383523292,
 "grip": {
  "hold": 0.6071428571428571,
  "stop": 0.7562103115821974,
  "pitchDeg": 31.263731694377427
 },
 "generated": "2026-09-28",
 "designs": [
  {
   "id": "balance",
   "name": "One balancing arm",
   "opts": {
    "mastMode": "balance"
   },
   "count": {
    "pass": 16,
    "warn": 4,
    "fail": 3
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
       "part": "Arm drive",
       "need": "996 N·m",
       "note": "self-locking; leans the arm to keep the weight away from the edges"
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
       "part": "Arm drive",
       "need": "1730 N·m",
       "note": "self-locking; leans the arm to keep the weight away from the edges"
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
   "results": [
    {
     "group": "Baseline",
     "name": "Default design",
     "what": "120 kg person, half lying, seat 0.5 m up",
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
  },
  {
   "id": "vArms",
   "name": "Two arms from the hinge",
   "opts": {
    "mastMode": "vArms"
   },
   "count": {
    "pass": 12,
    "warn": 5,
    "fail": 3
   },
   "structure": {
    "normal": {
     "members": [
      {
       "part": "Arms",
       "size": "2 pairs of 40 × 40 × 4 mm box tube",
       "load": "815 N·m bend",
       "stress": 64687857.662179455,
       "limit": 355000000,
       "factor": 5.4878923623336355
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
       "part": "Cradle pins",
       "size": "25 mm bars, double shear",
       "load": "2.8 kN",
       "stress": 2897791.3446536516,
       "limit": 205000000,
       "factor": 70.7435338221365
      }
     ],
     "drives": [
      {
       "part": "Hinge motor",
       "need": "1167 N·m",
       "note": "self-locking; holds a fold with the power off"
      },
      {
       "part": "Arm drives",
       "need": "815 N·m each",
       "note": "two, self-locking; they level the cradle and move it fore and aft"
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
       "part": "Arms",
       "size": "2 pairs of 40 × 40 × 4 mm box tube",
       "load": "1280 N·m bend",
       "stress": 101601378.4066959,
       "limit": 355000000,
       "factor": 3.4940470844695173
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
       "part": "Cradle pins",
       "size": "25 mm bars, double shear",
       "load": "4.4 kN",
       "stress": 4496572.7761867,
       "limit": 205000000,
       "factor": 45.59027735204353
      }
     ],
     "drives": [
      {
       "part": "Hinge motor",
       "need": "1717 N·m",
       "note": "self-locking; holds a fold with the power off"
      },
      {
       "part": "Arm drives",
       "need": "1280 N·m each",
       "note": "two, self-locking; they level the cradle and move it fore and aft"
      },
      {
       "part": "Track drives",
       "need": "64 N·m, 354 W",
       "note": "per unit and in total, at 0.25 m/s; spring brakes"
      }
     ]
    }
   },
   "results": [
    {
     "group": "Baseline",
     "name": "Default design",
     "what": "120 kg person, half lying, seat 0.5 m up",
     "opts": {},
     "tipUp": 9.539141228910507,
     "tipDown": 7.785493596900572,
     "drop": 0,
     "tilt": 5.985206221800444,
     "steps": 0.476735637153078,
     "stepsPart": "backrest",
     "tracks": 0.29672296039253354,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.31626574206000946,
      "tilt": 28.774455359111805,
      "tip": -18.489077711103775
     },
     "level": "pass",
     "why": "takes a 7.8° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "200 kg person",
     "what": "two thirds more than planned",
     "opts": {
      "personMass": 200
     },
     "tipUp": 9.289429600471486,
     "tipDown": 7.038354088768867,
     "drop": 0,
     "tilt": 5.9852062218004605,
     "steps": 0.4622798455010094,
     "stepsPart": "backrest",
     "tracks": 0.2820811253980505,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 40.11786850996207,
     "one": {
      "drop": 0.31626574206000946,
      "tilt": 28.58094196269269,
      "tip": -19.037377165877796
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 7.0°, needs 7.3°)"
    },
    {
     "group": "Load",
     "name": "40 kg person",
     "what": "a child or a small adult",
     "opts": {
      "personMass": 40
     },
     "tipUp": 11.190130677228382,
     "tipDown": 8.602403201089375,
     "drop": 0,
     "tilt": 5.961136909859753,
     "steps": 0.46763243146103484,
     "stepsPart": "backrest",
     "tracks": 0.2874750963619749,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.2577751110684492,
      "tilt": 28.586510431846154,
      "tip": -16.553284732579925
     },
     "level": "pass",
     "why": "takes a 8.6° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 10 cm towards the feet",
     "what": "held by the harness and foot stop",
     "opts": {
      "comOffset": -0.1
     },
     "tipUp": 8.186219838436083,
     "tipDown": 7.552114112430296,
     "drop": 0,
     "tilt": 5.9852062218004605,
     "steps": 0.45889753473724226,
     "stepsPart": "backrest",
     "tracks": 0.2690615241496903,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.2577751110684492,
      "tilt": 28.50879909822226,
      "tip": -15.133310196926882
     },
     "level": "pass",
     "why": "takes a 7.6° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 10 cm towards the head",
     "what": "held by the harness",
     "opts": {
      "comOffset": 0.1
     },
     "tipUp": 12.045875499493832,
     "tipDown": 8.36521737824537,
     "drop": 0,
     "tilt": 5.909464016359643,
     "steps": 0.4898556013828413,
     "stepsPart": "thigh",
     "tracks": 0.3011838057843963,
     "tracksHit": {
      "part": "thigh",
      "unit": "front"
     },
     "hinge": 40.11786850996207,
     "one": {
      "drop": 0.3518144864260613,
      "tilt": 28.61904026984524,
      "tip": -23.50342053855473
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
     "tipUp": 7.436009501736329,
     "tipDown": 7.14376219146787,
     "drop": 0,
     "tilt": 5.985206221800297,
     "steps": 0.42082005239267295,
     "stepsPart": "backrest",
     "tracks": 0.23885190488539973,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.3859889668491423,
      "tilt": 28.35900509704508,
      "tip": -21.743264883405953
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 7.1°, needs 7.3°)"
    },
    {
     "group": "Posture",
     "name": "Sitting up",
     "what": "15° recline",
     "opts": {
      "reclineDeg": 15
     },
     "tipUp": 9.286088968590203,
     "tipDown": 7.671439667181003,
     "drop": 0,
     "tilt": 5.9852062218004605,
     "steps": 0.32936505888135303,
     "stepsPart": "leg rest",
     "tracks": 0.1493650588813532,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.31626574206000946,
      "tilt": 28.73515595012735,
      "tip": -18.52431348738524
     },
     "level": "pass",
     "why": "takes a 7.7° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Posture",
     "name": "Lying flat",
     "what": "90° recline",
     "opts": {
      "reclineDeg": 90
     },
     "tipUp": 10.8594772775756,
     "tipDown": 9.18393644364793,
     "drop": 0,
     "tilt": 5.944874845057304,
     "steps": 0.11168364030327435,
     "stepsPart": "backrest",
     "tracks": 0.09319268366495514,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.30173368859410354,
      "tilt": 28.668659133885367,
      "tip": -18.100163989004404
     },
     "level": "pass",
     "why": "takes a 9.2° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Posture",
     "name": "Lying flat and slides 10 cm towards the feet",
     "what": "the case a single post looks worst for",
     "opts": {
      "reclineDeg": 90,
      "comOffset": -0.1
     },
     "tipUp": 10.665461969729789,
     "tipDown": 8.395702821662075,
     "drop": 0,
     "tilt": 5.9852062218004605,
     "steps": 0.08684537166303846,
     "stepsPart": "backrest",
     "tracks": 0.10298305111322581,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.2430078522681427,
      "tilt": 28.97524383152609,
      "tip": -14.193107852226369
     },
     "level": "pass",
     "why": "takes a 8.4° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Stairs",
     "name": "Steeper stairs",
     "what": "250 mm treads, 34.2°",
     "opts": {
      "going": 0.25
     },
     "tipUp": 8.051754923790956,
     "tipDown": 8.188141793036543,
     "drop": 0,
     "tilt": 6.002416519992195,
     "steps": 0.43190327241010673,
     "stepsPart": "backrest",
     "tracks": 0.24090181150627496,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 43.43373364906162,
     "one": {
      "drop": 0.34513409620101676,
      "tilt": 31.549424592466245,
      "tip": -25.01976583811179
     },
     "level": "pass",
     "why": "takes a 8.1° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Stairs",
     "name": "Steepest stairs",
     "what": "180 mm rise, 250 mm treads, 35.8°",
     "opts": {
      "rise": 0.18,
      "going": 0.25
     },
     "tipUp": 7.882605443654416,
     "tipDown": 8.277925062982995,
     "drop": 0,
     "tilt": 5.8334232422357,
     "steps": 0.3971762439428306,
     "stepsPart": "backrest",
     "tracks": 0.2110553684409013,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 46.21948664070815,
     "one": {
      "drop": 0.38790191513327077,
      "tilt": 32.50158459384505,
      "tip": -25.775034493420172
     },
     "level": "pass",
     "why": "takes a 7.9° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Motors",
     "name": "Hinge motor at three-quarter speed",
     "what": "90°/m, or driving a third faster",
     "opts": {
      "hingeRateDegPerM": 90
     },
     "tipUp": 7.380270702981848,
     "tipDown": 9.712466760858296,
     "drop": 0,
     "tilt": 6.21277592174794,
     "steps": 0.4773488030350942,
     "stepsPart": "backrest",
     "tracks": 0.2973266059423869,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 40.545195381440365,
     "one": {
      "drop": 0.31626574206000946,
      "tilt": 28.774455359111805,
      "tip": -18.489077711103775
     },
     "level": "pass",
     "why": "takes a 7.4° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Motors",
     "name": "Hinge motor at half speed",
     "what": "60°/m, or driving twice as fast",
     "opts": {
      "hingeRateDegPerM": 60
     },
     "tipUp": 5.907312206465943,
     "tipDown": -3.7566821864997246,
     "drop": 0.1078149936603574,
     "tilt": 19.848612334668726,
     "steps": 0.46461123887807465,
     "stepsPart": "backrest",
     "tracks": 0.2742222101681625,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 41.320434831240924,
     "one": {
      "drop": 0.31626574206000946,
      "tilt": 28.774455359111805,
      "tip": -18.489077711103775
     },
     "level": "fail",
     "why": "rocks over and drops 11 cm"
    },
    {
     "group": "Motors",
     "name": "Hinge range cut to ±45°",
     "what": "a smaller hinge motor",
     "opts": {
      "hingeLimitDeg": 45
     },
     "tipUp": 7.035093065388272,
     "tipDown": 8.78277333445392,
     "drop": 0,
     "tilt": 5.985206221800444,
     "steps": 0.47097642218878744,
     "stepsPart": "backrest",
     "tracks": 0.29097283046089395,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 41.320434831240924,
     "one": {
      "drop": 0.31626574206000946,
      "tilt": 28.774455359111805,
      "tip": -18.489077711103775
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 7.0°, needs 7.3°)"
    },
    {
     "group": "Motors",
     "name": "Arm drives at half speed",
     "what": "45°/m",
     "opts": {
      "twoArmRateDegPerM": 45
     },
     "tipUp": 9.298502980883233,
     "tipDown": 10.095428749566064,
     "drop": 0,
     "tilt": 8.273359114873438,
     "steps": 0.44121702233802274,
     "stepsPart": "backrest",
     "tracks": 0.2609311822201249,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 41.752734232198925,
     "one": {
      "drop": 0.31626574206000946,
      "tilt": 29.989907337223276,
      "tip": -21.92700341913677
     },
     "level": "pass",
     "why": "takes a 9.3° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Rear arm drive seizes",
     "what": "then keeps going",
     "opts": {
      "twoArmLock": "rear"
     },
     "tipUp": 8.511908372572828,
     "tipDown": 8.667073147134511,
     "drop": 0,
     "tilt": 11.905196864899017,
     "steps": 0.5310635974241493,
     "stepsPart": "backrest",
     "tracks": 0.3486779912835737,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 29.443787867017,
      "tip": -13.70762840708884
     },
     "level": "pass",
     "why": "takes a 8.5° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Front arm drive seizes",
     "what": "then keeps going",
     "opts": {
      "twoArmLock": "front"
     },
     "tipUp": 4.491765624030169,
     "tipDown": 9.549630266714345,
     "drop": 0,
     "tilt": 30.845664133017127,
     "steps": 0.4363407650485772,
     "stepsPart": "leg rest",
     "tracks": 0.2578472442006745,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 30.498088069759255,
      "tip": -12.907108874575894
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 4.5°, needs 7.3°)"
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
     "tipUp": 8.837103629989778,
     "tipDown": 6.524054528420906,
     "drop": 0,
     "tilt": 5.8334232422357335,
     "steps": 0.3647174510400786,
     "stepsPart": "backrest",
     "tracks": 0.18356941438031235,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 45.04958170002576,
     "one": {
      "drop": 0.36873670839353245,
      "tilt": 32.5015845938451,
      "tip": -21.075726948817397
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 6.5°, needs 7.3°)"
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
     "tipUp": 6.766463337007131,
     "tipDown": 7.588072474269706,
     "drop": 0,
     "tilt": 6.084763124149435,
     "steps": -0.03,
     "stepsPart": "backrest",
     "tracks": 0.04582199205526927,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 44.660231967700255,
     "one": {
      "drop": 0.33847359031651436,
      "tilt": 32.501584593845585,
      "tip": -20.887586446223704
     },
     "level": "fail",
     "why": "the seat or person hits the tracks or steps"
    },
    {
     "group": "Failures",
     "name": "Hinge motor seizes straight",
     "what": "and the tracks keep driving",
     "opts": {},
     "tipUp": -18.489077711103775,
     "tipDown": -18.489077711103775,
     "drop": 0.31626574206000946,
     "tilt": 28.774455359111805,
     "steps": 0.476735637153078,
     "stepsPart": "backrest",
     "tracks": 0.29672296039253354,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 0,
     "level": "fail",
     "why": "behaves like one long track and drops 32 cm at an edge, so the tracks must stop if the hinge stops"
    }
   ]
  },
  {
   "id": "twoArm",
   "name": "Two arms, one on each track",
   "opts": {
    "mastMode": "twoArm"
   },
   "count": {
    "pass": 7,
    "warn": 6,
    "fail": 7
   },
   "structure": {
    "normal": {
     "members": [
      {
       "part": "Arms",
       "size": "2 pairs of 40 × 40 × 4 mm box tube",
       "load": "890 N·m bend",
       "stress": 70631673.04401724,
       "limit": 355000000,
       "factor": 5.026073781075044
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
       "part": "Cradle pins",
       "size": "25 mm bars, double shear",
       "load": "2.8 kN",
       "stress": 2897791.3446536516,
       "limit": 205000000,
       "factor": 70.7435338221365
      }
     ],
     "drives": [
      {
       "part": "Hinge motor",
       "need": "1167 N·m",
       "note": "self-locking; holds a fold with the power off"
      },
      {
       "part": "Arm drives",
       "need": "890 N·m each",
       "note": "two, self-locking; they level the cradle and move it fore and aft"
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
       "part": "Arms",
       "size": "2 pairs of 40 × 40 × 4 mm box tube",
       "load": "1149 N·m bend",
       "stress": 91227678.0689074,
       "limit": 355000000,
       "factor": 3.8913628792772332
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
       "part": "Cradle pins",
       "size": "25 mm bars, double shear",
       "load": "4.4 kN",
       "stress": 4496572.7761867,
       "limit": 205000000,
       "factor": 45.59027735204353
      }
     ],
     "drives": [
      {
       "part": "Hinge motor",
       "need": "1717 N·m",
       "note": "self-locking; holds a fold with the power off"
      },
      {
       "part": "Arm drives",
       "need": "1149 N·m each",
       "note": "two, self-locking; they level the cradle and move it fore and aft"
      },
      {
       "part": "Track drives",
       "need": "64 N·m, 354 W",
       "note": "per unit and in total, at 0.25 m/s; spring brakes"
      }
     ]
    }
   },
   "results": [
    {
     "group": "Baseline",
     "name": "Default design",
     "what": "120 kg person, half lying, seat 0.5 m up",
     "opts": {},
     "tipUp": 16.097172634750056,
     "tipDown": 9.903779083526917,
     "drop": 0,
     "tilt": 8.360748095037671,
     "steps": 0.4425281933184646,
     "stepsPart": "backrest",
     "tracks": 0.26374264832490235,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.30173368859410354,
      "tilt": 25.328270498571094,
      "tip": -17.7263156858548
     },
     "level": "pass",
     "why": "takes a 9.9° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "200 kg person",
     "what": "two thirds more than planned",
     "opts": {
      "personMass": 200
     },
     "tipUp": 12.742460001411732,
     "tipDown": 9.249646962170386,
     "drop": 0,
     "tilt": 8.40835952686954,
     "steps": 0.4690723544352513,
     "stepsPart": "backrest",
     "tracks": 0.2845579128075908,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.30173368859410354,
      "tilt": 26.165373553408788,
      "tip": -18.172424026523533
     },
     "level": "pass",
     "why": "takes a 9.2° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "40 kg person",
     "what": "a child or a small adult",
     "opts": {
      "personMass": 40
     },
     "tipUp": 19.914685002381702,
     "tipDown": 12.08228310877335,
     "drop": 0,
     "tilt": 12.631126849706893,
     "steps": 0.23939925046609742,
     "stepsPart": "backrest",
     "tracks": 0.08651602669197367,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 43.22611328571713,
     "one": {
      "drop": 0.3518144864260613,
      "tilt": 26.14403591428078,
      "tip": -34.08029107751672
     },
     "level": "pass",
     "why": "takes a 12.1° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 10 cm towards the feet",
     "what": "held by the harness and foot stop",
     "opts": {
      "comOffset": -0.1
     },
     "tipUp": 18.076632240951852,
     "tipDown": 8.687471649139388,
     "drop": 0,
     "tilt": 12.631126849706893,
     "steps": 0.24203524065194296,
     "stepsPart": "backrest",
     "tracks": 0.08651602669197367,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 43.57392815969304,
     "one": {
      "drop": 0.3518144864260613,
      "tilt": 26.14403591428078,
      "tip": -30.45336458608403
     },
     "level": "pass",
     "why": "takes a 8.7° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 10 cm towards the head",
     "what": "held by the harness",
     "opts": {
      "comOffset": 0.1
     },
     "tipUp": 10.94292772096103,
     "tipDown": 10.917690875620135,
     "drop": 0,
     "tilt": 11.583003215627206,
     "steps": 0.4661983137690799,
     "stepsPart": "thigh",
     "tracks": 0.29757696373400155,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 40.447490140599974,
     "one": {
      "drop": 0.3494311612459722,
      "tilt": 26.86101057966144,
      "tip": -22.395866263444592
     },
     "level": "pass",
     "why": "takes a 10.9° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 25 cm towards the feet",
     "what": "no harness or foot stop",
     "opts": {
      "comOffset": -0.25
     },
     "tipUp": 15.95585836741358,
     "tipDown": 8.394225838730623,
     "drop": 0,
     "tilt": 12.631126849706893,
     "steps": 0.24203524065194296,
     "stepsPart": "backrest",
     "tracks": 0.08651602669197367,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 40.284730114285125,
     "one": {
      "drop": 0.3518144864260613,
      "tilt": 26.14403591428078,
      "tip": -23.926058128727522
     },
     "level": "pass",
     "why": "takes a 8.4° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Posture",
     "name": "Sitting up",
     "what": "15° recline",
     "opts": {
      "reclineDeg": 15
     },
     "tipUp": 15.878834657939395,
     "tipDown": 9.783569743504728,
     "drop": 0,
     "tilt": 8.33874457221837,
     "steps": 0.2847655161502829,
     "stepsPart": "leg rest",
     "tracks": 0.10118959148565573,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.30173368859410354,
      "tilt": 25.259628002816402,
      "tip": -17.686469636073898
     },
     "level": "pass",
     "why": "takes a 9.8° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Posture",
     "name": "Lying flat",
     "what": "90° recline",
     "opts": {
      "reclineDeg": 90
     },
     "tipUp": 18.442821235177693,
     "tipDown": 10.504970645250634,
     "drop": 0,
     "tilt": 12.631126849706893,
     "steps": -0.03828067681147007,
     "stepsPart": "head",
     "tracks": 0.19503904647705592,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 45.752959985669754,
     "one": {
      "drop": 0.3518144864260613,
      "tilt": 26.14403591428078,
      "tip": -40.29717484420646
     },
     "level": "fail",
     "why": "the seat or person hits the tracks or steps"
    },
    {
     "group": "Posture",
     "name": "Lying flat and slides 10 cm towards the feet",
     "what": "the case a single post looks worst for",
     "opts": {
      "reclineDeg": 90,
      "comOffset": -0.1
     },
     "tipUp": 16.719119427536477,
     "tipDown": 9.767291314968286,
     "drop": 0,
     "tilt": 12.631126849706893,
     "steps": -0.03,
     "stepsPart": "backrest",
     "tracks": 0.19503904647705592,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 43.57392815969304,
     "one": {
      "drop": 0.3518144864260613,
      "tilt": 26.14403591428078,
      "tip": -36.41744353317456
     },
     "level": "fail",
     "why": "the seat or person hits the tracks or steps"
    },
    {
     "group": "Stairs",
     "name": "Steeper stairs",
     "what": "250 mm treads, 34.2°",
     "opts": {
      "going": 0.25
     },
     "tipUp": 6.555578388044917,
     "tipDown": 9.987498249667862,
     "drop": 0,
     "tilt": 15.133441837721799,
     "steps": 0.4255105211995541,
     "stepsPart": "backrest",
     "tracks": 0.25573945032979517,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 41.444524245392586,
     "one": {
      "drop": 0.30173368859409067,
      "tilt": 27.463059329060005,
      "tip": -17.726313278218672
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 6.6°, needs 7.3°)"
    },
    {
     "group": "Stairs",
     "name": "Steepest stairs",
     "what": "180 mm rise, 250 mm treads, 35.8°",
     "opts": {
      "rise": 0.18,
      "going": 0.25
     },
     "tipUp": 1.9073635973178402,
     "tipDown": 8.847310130323422,
     "drop": 0.03007970663443782,
     "tilt": 16.282186948919158,
     "steps": 0.4220082486665322,
     "stepsPart": "backrest",
     "tracks": 0.2546162537206539,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 43.49413143769984,
     "one": {
      "drop": 0.28713986777303013,
      "tilt": 29.72695128116723,
      "tip": -20.288877801225667
     },
     "level": "fail",
     "why": "rocks over and drops 3 cm"
    },
    {
     "group": "Motors",
     "name": "Hinge motor at three-quarter speed",
     "what": "90°/m, or driving a third faster",
     "opts": {
      "hingeRateDegPerM": 90
     },
     "tipUp": 4.923392485157443,
     "tipDown": 9.908988006875058,
     "drop": 0,
     "tilt": 8.360748095037671,
     "steps": 0.4326844867852472,
     "stepsPart": "backrest",
     "tracks": 0.2560546911382636,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 37.70363798712211,
     "one": {
      "drop": 0.30173368859410354,
      "tilt": 25.328270498571094,
      "tip": -17.7263156858548
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 4.9°, needs 7.3°)"
    },
    {
     "group": "Motors",
     "name": "Hinge motor at half speed",
     "what": "60°/m, or driving twice as fast",
     "opts": {
      "hingeRateDegPerM": 60
     },
     "tipUp": -3.019763554980045,
     "tipDown": -8.097784753226259,
     "drop": 0.16516683448794822,
     "tilt": 17.663516797934125,
     "steps": 0.47437222535853274,
     "stepsPart": "backrest",
     "tracks": 0.2832041841938959,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 36.59999999999999,
     "one": {
      "drop": 0.30173368859410354,
      "tilt": 25.328270498571094,
      "tip": -17.7263156858548
     },
     "level": "fail",
     "why": "rocks over and drops 17 cm"
    },
    {
     "group": "Motors",
     "name": "Hinge range cut to ±45°",
     "what": "a smaller hinge motor",
     "opts": {
      "hingeLimitDeg": 45
     },
     "tipUp": -0.9533925747790399,
     "tipDown": 9.909444072450173,
     "drop": 0.06083365613864622,
     "tilt": 8.360748095037662,
     "steps": 0.43332233932212694,
     "stepsPart": "backrest",
     "tracks": 0.25839392322048615,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 37.70363798712211,
     "one": {
      "drop": 0.30173368859410354,
      "tilt": 25.328270498571094,
      "tip": -17.7263156858548
     },
     "level": "fail",
     "why": "rocks over and drops 6 cm"
    },
    {
     "group": "Motors",
     "name": "Arm drives at half speed",
     "what": "45°/m",
     "opts": {
      "twoArmRateDegPerM": 45
     },
     "tipUp": 15.814617661396408,
     "tipDown": 9.710894943345433,
     "drop": 0,
     "tilt": 23.823393266260712,
     "steps": 0.44784325383003487,
     "stepsPart": "backrest",
     "tracks": 0.27060290433358924,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.30173368859410354,
      "tilt": 28.091205929853306,
      "tip": -18.359583358086134
     },
     "level": "warn",
     "why": "stays up, but the person tilts 24°"
    },
    {
     "group": "Failures",
     "name": "Rear arm drive seizes",
     "what": "then keeps going",
     "opts": {
      "twoArmLock": "rear"
     },
     "tipUp": 17.312036671826075,
     "tipDown": 9.237641142070675,
     "drop": 0,
     "tilt": 21.859018985607502,
     "steps": 0.4240101526933687,
     "stepsPart": "backrest",
     "tracks": 0.23846088269324137,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.3518144864260613,
      "tilt": 28.259191524952794,
      "tip": -25.09293772735872
     },
     "level": "warn",
     "why": "stays up, but the person tilts 22°"
    },
    {
     "group": "Failures",
     "name": "Front arm drive seizes",
     "what": "then keeps going",
     "opts": {
      "twoArmLock": "front"
     },
     "tipUp": 9.223953607612955,
     "tipDown": 11.471119233989622,
     "drop": 0,
     "tilt": 24.97225113256611,
     "steps": 0.5443415391318923,
     "stepsPart": "leg rest",
     "tracks": 0.3622345132200646,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.2577751110684492,
      "tilt": 28.547853107351518,
      "tip": -15.849758276804991
     },
     "level": "warn",
     "why": "stays up, but the person tilts 25°"
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
     "tipUp": 4.806211131458122,
     "tipDown": 6.2120110348829725,
     "drop": 0,
     "tilt": 13.080383843689111,
     "steps": 0.413729608598556,
     "stepsPart": "backrest",
     "tracks": 0.2486991841879412,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 40.80000000000017,
     "one": {
      "drop": 0.2724863625092029,
      "tilt": 28.791445653091305,
      "tip": -17.288148880236243
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 4.8°, needs 7.3°)"
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
     "tipUp": 6.153188385340747,
     "tipDown": 8.18185930630448,
     "drop": 0,
     "tilt": 16.767947473906684,
     "steps": -0.03,
     "stepsPart": "backrest",
     "tracks": 0.18791460742846353,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 48.964223902662084,
     "one": {
      "drop": 0.3911912258761001,
      "tilt": 29.89831873581983,
      "tip": -35.03730522674767
     },
     "level": "fail",
     "why": "the seat or person hits the tracks or steps"
    },
    {
     "group": "Failures",
     "name": "Hinge motor seizes straight",
     "what": "and the tracks keep driving",
     "opts": {},
     "tipUp": -17.7263156858548,
     "tipDown": -17.7263156858548,
     "drop": 0.30173368859410354,
     "tilt": 25.328270498571094,
     "steps": 0.4425281933184646,
     "stepsPart": "backrest",
     "tracks": 0.26374264832490235,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 0,
     "level": "fail",
     "why": "behaves like one long track and drops 30 cm at an edge, so the tracks must stop if the hinge stops"
    }
   ]
  },
  {
   "id": "average",
   "name": "One arm without a drive",
   "opts": {
    "mastMode": "average"
   },
   "count": {
    "pass": 7,
    "warn": 8,
    "fail": 5
   },
   "structure": {
    "normal": {
     "members": [
      {
       "part": "Columns",
       "size": "2 × 50 × 50 × 4 mm box tube, 0.4 m apart",
       "load": "495 N·m bend",
       "stress": 23655704.11208518,
       "limit": 355000000,
       "factor": 15.006951317870023
      },
      {
       "part": "Averaging links",
       "size": "12 mm rods, a diamond each side",
       "load": "0.8 kN each",
       "stress": 7310455.241954227,
       "limit": 355000000,
       "factor": 48.560587302782196
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
       "load": "788 N·m bend",
       "stress": 37640125.55055855,
       "limit": 355000000,
       "factor": 9.431424438878686
      },
      {
       "part": "Averaging links",
       "size": "12 mm rods, a diamond each side",
       "load": "1.3 kN each",
       "stress": 11632139.624130636,
       "limit": 355000000,
       "factor": 30.51889088947658
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
   "results": [
    {
     "group": "Baseline",
     "name": "Default design",
     "what": "120 kg person, half lying, seat 0.5 m up",
     "opts": {},
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
     "tipUp": 7.591381887156169,
     "tipDown": 7.4084283432698745,
     "drop": 0,
     "tilt": 5.053139651111426,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.303568226682823,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 22.490383328416005,
      "tip": -15.14658818521759
     },
     "level": "pass",
     "why": "takes a 7.4° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "40 kg person",
     "what": "a child or a small adult",
     "opts": {
      "personMass": 40
     },
     "tipUp": 9.893397917331468,
     "tipDown": 11.00457528750018,
     "drop": 0,
     "tilt": 5.053139651111426,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.3026855770880408,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.3085405800942862,
      "tilt": 22.611307757636457,
      "tip": -16.461831550897273
     },
     "level": "pass",
     "why": "takes a 9.9° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 10 cm towards the feet",
     "what": "held by the harness and foot stop",
     "opts": {
      "comOffset": -0.1
     },
     "tipUp": 8.318777082414123,
     "tipDown": 8.483939161599967,
     "drop": 0,
     "tilt": 5.036276218727477,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.2986372739513491,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.3190647501907171,
      "tilt": 22.490383328416005,
      "tip": -20.425125537035136
     },
     "level": "pass",
     "why": "takes a 8.3° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 10 cm towards the head",
     "what": "held by the harness",
     "opts": {
      "comOffset": 0.1
     },
     "tipUp": 9.344629603414223,
     "tipDown": 8.550220489931682,
     "drop": 0,
     "tilt": 5.033555710202661,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.3033538723102307,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.2577751110684492,
      "tilt": 22.490383328416005,
      "tip": -14.875025394169958
     },
     "level": "pass",
     "why": "takes a 8.6° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 25 cm towards the feet",
     "what": "no harness or foot stop",
     "opts": {
      "comOffset": -0.25
     },
     "tipUp": 8.413911880267834,
     "tipDown": 1.4956860541901666,
     "drop": 0.0420889659050645,
     "tilt": 5.033555710202661,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.3145084673775471,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 40.63000967994316,
     "one": {
      "drop": 0.41145997362521847,
      "tilt": 22.611307757636457,
      "tip": -27.846515256499448
     },
     "level": "fail",
     "why": "rocks over and drops 4 cm"
    },
    {
     "group": "Posture",
     "name": "Sitting up",
     "what": "15° recline",
     "opts": {
      "reclineDeg": 15
     },
     "tipUp": 7.91334029097855,
     "tipDown": 8.040530929584143,
     "drop": 0,
     "tilt": 5.053139651111426,
     "steps": 0.2633040491987477,
     "stepsPart": "leg rest",
     "tracks": 0.0833040491987479,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 22.490383328416005,
      "tip": -15.495616113846735
     },
     "level": "pass",
     "why": "takes a 7.9° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Posture",
     "name": "Lying flat",
     "what": "90° recline",
     "opts": {
      "reclineDeg": 90
     },
     "tipUp": 9.381882905765805,
     "tipDown": 9.696773430027854,
     "drop": 0,
     "tilt": 5.053139651111426,
     "steps": 0.12928408774136785,
     "stepsPart": "backrest",
     "tracks": 0.018903959092688827,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 22.490383328416005,
      "tip": -14.796703774669986
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
     "tipUp": 9.652322548636821,
     "tipDown": 9.841285996835678,
     "drop": 0,
     "tilt": 5.036276218727477,
     "steps": 0.12928408774136785,
     "stepsPart": "backrest",
     "tracks": 0.01890395909268705,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.3190647501907171,
      "tilt": 22.490383328416005,
      "tip": -20.65423223620475
     },
     "level": "warn",
     "why": "fits with only 2 cm to spare"
    },
    {
     "group": "Stairs",
     "name": "Steeper stairs",
     "what": "250 mm treads, 34.2°",
     "opts": {
      "going": 0.25
     },
     "tipUp": 7.739823781907668,
     "tipDown": 5.166142118574268,
     "drop": 0,
     "tilt": 5.0680110716171995,
     "steps": 0.4821775165121127,
     "stepsPart": "leg rest",
     "tracks": 0.3033538723102307,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 41.07205262096803,
     "one": {
      "drop": 0.33807135632481966,
      "tilt": 25.42414045734924,
      "tip": -18.23583826289295
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 5.2°, needs 7.3°)"
    },
    {
     "group": "Stairs",
     "name": "Steepest stairs",
     "what": "180 mm rise, 250 mm treads, 35.8°",
     "opts": {
      "rise": 0.18,
      "going": 0.25
     },
     "tipUp": 7.638781691661554,
     "tipDown": 1.6086081375389905,
     "drop": 0,
     "tilt": 3.930019962447086,
     "steps": 0.4800867055332798,
     "stepsPart": "leg rest",
     "tracks": 0.3035736845260949,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 40.80000000000017,
     "one": {
      "drop": 0.36873670839353245,
      "tilt": 26.753887254436773,
      "tip": -18.23583826289295
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 1.6°, needs 7.3°)"
    },
    {
     "group": "Motors",
     "name": "Hinge motor at three-quarter speed",
     "what": "90°/m, or driving a third faster",
     "opts": {
      "hingeRateDegPerM": 90
     },
     "tipUp": 8.865845951132227,
     "tipDown": 1.9122127995638967,
     "drop": 0,
     "tilt": 5.1344512579086965,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.2863616445060082,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 36.931452237649445,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 22.490383328416005,
      "tip": -15.437476410629898
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 1.9°, needs 7.3°)"
    },
    {
     "group": "Motors",
     "name": "Hinge motor at half speed",
     "what": "60°/m, or driving twice as fast",
     "opts": {
      "hingeRateDegPerM": 60
     },
     "tipUp": 9.5916669943322,
     "tipDown": -7.728156110341011,
     "drop": 0.16782883781080749,
     "tilt": 15.267680724969987,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.26063266137816066,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 34.083928947112405,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 22.490383328416005,
      "tip": -15.437476410629898
     },
     "level": "fail",
     "why": "rocks over and drops 17 cm"
    },
    {
     "group": "Motors",
     "name": "Hinge range cut to ±45°",
     "what": "a smaller hinge motor",
     "opts": {
      "hingeLimitDeg": 45
     },
     "tipUp": 8.036321449565781,
     "tipDown": 1.713112653217235,
     "drop": 0,
     "tilt": 5.053139651111426,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.3033538723102307,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 36.26382605546667,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 22.490383328416005,
      "tip": -15.437476410629898
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 1.7°, needs 7.3°)"
    },
    {
     "group": "Motors",
     "name": "Seat drive at half speed",
     "what": "75°/m",
     "opts": {
      "levelRateDegPerM": 75
     },
     "tipUp": 8.146568332793391,
     "tipDown": 8.294670297492866,
     "drop": 0,
     "tilt": 5.803139651111427,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.32265755364966797,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.3085405800942862,
      "tilt": 27.111307757636457,
      "tip": -16.706995170724607
     },
     "level": "pass",
     "why": "takes a 8.1° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Seat drive stuck level",
     "what": "fails on the flat, then keeps going",
     "opts": {
      "levelLockDeg": 0
     },
     "tipUp": 8.84853212528938,
     "tipDown": 8.84853212528938,
     "drop": 0,
     "tilt": 31.611307757635082,
     "steps": 0.29089084987943803,
     "stepsPart": "leg rest",
     "tracks": 0.14185483678867356,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.3085405800942862,
      "tilt": 31.611307757635082,
      "tip": -18.065355955113283
     },
     "level": "warn",
     "why": "stays up, but the person tilts 32°"
    },
    {
     "group": "Failures",
     "name": "Seat drive stuck on a flight",
     "what": "fails at 31.6°, then keeps going",
     "opts": {
      "levelLockDeg": 31.6
     },
     "tipUp": 11.184388745495795,
     "tipDown": 9.717079648389932,
     "drop": 0,
     "tilt": 33.551493882070275,
     "steps": 0.33173992235789507,
     "stepsPart": "backrest",
     "tracks": 0.2625585340897105,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "one": {
      "drop": 0.18340770650457383,
      "tilt": 31.60000000000146,
      "tip": -11.784881078220366
     },
     "level": "warn",
     "why": "stays up, but the person tilts 34°"
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
     "tipUp": 7.483511343934088,
     "tipDown": -6.983407167328877,
     "drop": 0.1269330865113396,
     "tilt": 6.1466644721648835,
     "steps": 0.4800867055332798,
     "stepsPart": "leg rest",
     "tracks": 0.2976130022051299,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 43.485572493588954,
     "one": {
      "drop": 0.4474500387014997,
      "tilt": 26.753887254436773,
      "tip": -23.2813200197053
     },
     "level": "fail",
     "why": "rocks over and drops 13 cm"
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
     "tipUp": 8.683135003079517,
     "tipDown": -8.254649017342187,
     "drop": 0.1269330865113396,
     "tilt": 6.1466644721648835,
     "steps": 0.06924472041589175,
     "stepsPart": "backrest",
     "tracks": -0.0501780850787944,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 43.485572493588954,
     "one": {
      "drop": 0.41868950757539736,
      "tilt": 26.753887254436773,
      "tip": -25.023111402092823
     },
     "level": "fail",
     "why": "rocks over and drops 13 cm"
    },
    {
     "group": "Failures",
     "name": "Hinge motor seizes straight",
     "what": "and the tracks keep driving",
     "opts": {},
     "tipUp": -15.437476410629898,
     "tipDown": -15.437476410629898,
     "drop": 0.23633325290796003,
     "tilt": 22.490383328416005,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.3033538723102307,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 0,
     "level": "fail",
     "why": "behaves like one long track and drops 24 cm at an edge, so the tracks must stop if the hinge stops"
    }
   ]
  }
 ]
};
