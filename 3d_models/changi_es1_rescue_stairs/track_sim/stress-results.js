// Written by stress-test.js; do not edit by hand.
window.STRESS_RESULTS = {
 "hardStopDeg": 7.261554383523292,
 "grip": {
  "hold": 0.6071428571428571,
  "stop": 0.7562103115821974,
  "pitchDeg": 31.263731694377427
 },
 "generated": "2026-09-29",
 "designs": [
  {
   "id": "balance",
   "name": "One balancing arm",
   "opts": {
    "mastMode": "balance"
   },
   "split": false,
   "count": {
    "pass": 17,
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
     "extra": 0,
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
     "extra": 0,
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
     "tipDown": 11.501145133013129,
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
     "extra": 0,
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
     "extra": 0,
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
     "extra": 0,
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
     "tipDown": 9.580557228054136,
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
     "extra": 0,
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
     "tipDown": 8.513939305052531,
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
     "extra": 0,
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
     "extra": 0,
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
     "tipDown": 8.735122440909159,
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
     "extra": 0,
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
     "extra": 0,
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
     "tipDown": 8.27676090810323,
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
     "extra": 0,
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
     "tipUp": 8.531730330909438,
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
     "extra": 0,
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
     "tipUp": 9.43345830952978,
     "tipDown": -10.713544800005659,
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
     "extra": 0,
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
     "tipUp": 7.280710286801184,
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
     "extra": 0,
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
     "name": "Hinge motor half as fast again",
     "what": "180°/m: not a stress, a possible fix",
     "opts": {
      "hingeRateDegPerM": 180
     },
     "tipUp": 13.082882918170625,
     "tipDown": 7.843579600318607,
     "drop": 0,
     "tilt": 4.55518424858783,
     "steps": 0.44495242294169113,
     "stepsPart": "backrest",
     "tracks": 0.2521832321484845,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 43.22611328571713,
     "extra": 0,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 7.8° lean anywhere; a hard stop needs 7.3°"
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
     "extra": 0,
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
     "tipUp": 8.036321449565644,
     "tipDown": 8.177099304990382,
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
     "extra": 0,
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
     "extra": 0,
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
     "extra": 0,
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
     "tipUp": 11.546895257402518,
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
     "extra": 0,
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
     "tipUp": 7.795478850127313,
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
     "extra": 0,
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
     "tipUp": 7.281593182021476,
     "tipDown": 6.169784814222083,
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
     "extra": 0,
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
     "tipUp": 9.958358971737626,
     "tipDown": 5.4293128823683325,
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
     "extra": 0,
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
   "split": false,
   "count": {
    "pass": 12,
    "warn": 6,
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
     "tipUp": 9.539141228910639,
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
     "extra": 0,
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
     "tipUp": 9.289429600471506,
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
     "extra": 0,
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
     "tipUp": 11.190130677228556,
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
     "extra": 0,
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
     "tipUp": 8.18621983843621,
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
     "extra": 0,
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
     "tipDown": 8.365217378245514,
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
     "extra": 0,
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
     "tipUp": 7.4360095017364545,
     "tipDown": 7.143762191467937,
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
     "extra": 0,
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
     "extra": 0,
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
     "tipDown": 9.183936443647939,
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
     "extra": 0,
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
     "tipDown": 8.395702821662006,
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
     "extra": 0,
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
     "tipUp": 8.05175492379107,
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
     "extra": 0,
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
     "tipDown": 8.277925062983124,
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
     "extra": 0,
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
     "tipDown": 9.712466760858435,
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
     "extra": 0,
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
     "extra": 0,
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
     "extra": 0,
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
     "name": "Hinge motor half as fast again",
     "what": "180°/m: not a stress, a possible fix",
     "opts": {
      "hingeRateDegPerM": 180
     },
     "tipUp": 12.374212591555382,
     "tipDown": 5.992575442421654,
     "drop": 0,
     "tilt": 5.209003898933973,
     "steps": 0.4741015515960352,
     "stepsPart": "backrest",
     "tracks": 0.29404308917740396,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 43.22611328571713,
     "extra": 0,
     "one": {
      "drop": 0.31626574206000946,
      "tilt": 28.774455359111805,
      "tip": -18.489077711103775
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 6.0°, needs 7.3°)"
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
     "extra": 0,
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
     "tipUp": 8.511908372572806,
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
     "extra": 0,
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
     "tipUp": 4.49176562403016,
     "tipDown": 9.549630266714352,
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
     "extra": 0,
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
     "tipDown": 6.524054528420976,
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
     "extra": 0,
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
     "tipUp": 6.766463337007139,
     "tipDown": 7.588072474269541,
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
     "extra": 0,
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
   "split": false,
   "count": {
    "pass": 7,
    "warn": 7,
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
     "tipUp": 16.097172634750045,
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
     "extra": 0,
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
     "extra": 0,
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
     "tipUp": 19.914685002381876,
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
     "extra": 0,
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
     "tipDown": 8.687471649139459,
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
     "extra": 0,
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
     "tipUp": 10.942927720961023,
     "tipDown": 10.917690875620192,
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
     "extra": 0,
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
     "extra": 0,
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
     "extra": 0,
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
     "tipUp": 18.44282123517768,
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
     "extra": 0,
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
     "extra": 0,
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
     "tipUp": 6.555578388044925,
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
     "extra": 0,
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
     "tipUp": 1.907363597317682,
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
     "extra": 0,
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
     "tipDown": 9.908988006874983,
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
     "extra": 0,
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
     "extra": 0,
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
     "tipDown": 9.909444072450192,
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
     "extra": 0,
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
     "name": "Hinge motor half as fast again",
     "what": "180°/m: not a stress, a possible fix",
     "opts": {
      "hingeRateDegPerM": 180
     },
     "tipUp": 15.248434807988918,
     "tipDown": 7.799724234526751,
     "drop": 0,
     "tilt": 22.157037994582534,
     "steps": 0.4195255436519455,
     "stepsPart": "backrest",
     "tracks": 0.2502664058984905,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 43.22611328571713,
     "extra": 0,
     "one": {
      "drop": 0.30173368859410354,
      "tilt": 25.328270498571094,
      "tip": -17.7263156858548
     },
     "level": "warn",
     "why": "stays up, but the person tilts 22°"
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
     "extra": 0,
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
     "tipUp": 17.31203667182605,
     "tipDown": 9.237641142070606,
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
     "extra": 0,
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
     "tipUp": 9.223953607613069,
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
     "extra": 0,
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
     "extra": 0,
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
     "tipUp": 6.153188385340738,
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
     "extra": 0,
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
   "split": false,
   "count": {
    "pass": 7,
    "warn": 9,
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
     "tipUp": 8.036321449565644,
     "tipDown": 8.177099304990382,
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
     "extra": 0,
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
     "extra": 0,
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
     "extra": 0,
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
     "tipDown": 8.483939161599961,
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
     "extra": 0,
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
     "extra": 0,
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
     "tipDown": 1.4956860541901658,
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
     "extra": 0,
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
     "tipUp": 7.913340290978397,
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
     "extra": 0,
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
     "tipUp": 9.381882905765618,
     "tipDown": 9.69677343002787,
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
     "extra": 0,
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
     "extra": 0,
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
     "tipDown": 5.1661421185744105,
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
     "extra": 0,
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
     "tipUp": 7.638781691661545,
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
     "extra": 0,
     "one": {
      "drop": 0.36873670839353245,
      "tilt": 26.753887254436773,
      "tip": -18.23583826289277
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
     "tipDown": 1.91221279956397,
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
     "extra": 0,
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
     "tipUp": 9.591666994331955,
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
     "extra": 0,
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
     "tipUp": 8.036321449565644,
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
     "extra": 0,
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
     "name": "Hinge motor half as fast again",
     "what": "180°/m: not a stress, a possible fix",
     "opts": {
      "hingeRateDegPerM": 180
     },
     "tipUp": 7.240142672421078,
     "tipDown": 7.49574080659977,
     "drop": 0,
     "tilt": 4.616759520568562,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.31824035678865137,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 43.22611328571713,
     "extra": 0,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 22.490383328416005,
      "tip": -15.437476410629898
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 7.2°, needs 7.3°)"
    },
    {
     "group": "Motors",
     "name": "Seat drive at half speed",
     "what": "75°/m",
     "opts": {
      "levelRateDegPerM": 75
     },
     "tipUp": 8.146568332793372,
     "tipDown": 8.29467029749279,
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
     "extra": 0,
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
     "tipUp": 8.848532125289328,
     "tipDown": 8.848532125289328,
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
     "extra": 0,
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
     "tipUp": 11.184388745496062,
     "tipDown": 9.717079648389774,
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
     "extra": 0,
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
     "tipUp": 7.483511343934153,
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
     "extra": 0,
     "one": {
      "drop": 0.4474500387014997,
      "tilt": 26.753887254436773,
      "tip": -23.28132001970528
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
     "tipUp": 8.683135003079585,
     "tipDown": -8.254649017342018,
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
     "extra": 0,
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
  },
  {
   "id": "frontSplit",
   "name": "Front half split in two",
   "opts": {
    "mastMode": "balance",
    "sections": [
     0.7,
     0.35,
     0.35
    ],
    "mainJoint": 1
   },
   "split": true,
   "count": {
    "pass": 20,
    "warn": 3,
    "fail": 3
   },
   "structure": {
    "normal": {
     "members": [
      {
       "part": "Columns",
       "size": "2 × 50 × 50 × 4 mm box tube, 0.4 m apart",
       "load": "924 N·m bend",
       "stress": 44166678.91977348,
       "limit": 355000000,
       "factor": 8.03773361915754
      },
      {
       "part": "Averaging links",
       "size": "12 mm rods, a diamond each side",
       "load": "1.5 kN each",
       "stress": 13618094.68003839,
       "limit": 355000000,
       "factor": 26.06825758968796
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
       "need": "924 N·m",
       "note": "self-locking; leans the arm to keep the weight away from the edges"
      },
      {
       "part": "Seat tilt drives",
       "need": "478 N·m each",
       "note": "two, self-locking; either one holds the seat alone"
      },
      {
       "part": "Track drives",
       "need": "47 N·m, 258 W",
       "note": "per unit and in total, at 0.25 m/s; spring brakes"
      }
     ]
    },
    "heavy": {
     "members": [
      {
       "part": "Columns",
       "size": "2 × 50 × 50 × 4 mm box tube, 0.4 m apart",
       "load": "1477 N·m bend",
       "stress": 70590000.95157962,
       "limit": 355000000,
       "factor": 5.029040872849798
      },
      {
       "part": "Averaging links",
       "size": "12 mm rods, a diamond each side",
       "load": "2.5 kN each",
       "stress": 22171031.086441863,
       "limit": 355000000,
       "factor": 16.011884996051958
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
       "need": "1477 N·m",
       "note": "self-locking; leans the arm to keep the weight away from the edges"
      },
      {
       "part": "Seat tilt drives",
       "need": "763 N·m each",
       "note": "two, self-locking; either one holds the seat alone"
      },
      {
       "part": "Track drives",
       "need": "65 N·m, 361 W",
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
     "tipUp": 10.264574512527721,
     "tipDown": 18.71662888044187,
     "drop": 0,
     "tilt": 4.975822237685627,
     "steps": 0.44283000953325935,
     "stepsPart": "backrest",
     "tracks": 0.22387018433466752,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.85350419499082,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 10.3° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "200 kg person",
     "what": "two thirds more than planned",
     "opts": {
      "personMass": 200
     },
     "tipUp": 12.220790799796456,
     "tipDown": 17.953689968536956,
     "drop": 0,
     "tilt": 4.9758222376856285,
     "steps": 0.4140139030908242,
     "stepsPart": "backrest",
     "tracks": 0.2174121776230555,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.85350419499082,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.490383328416016,
      "tip": -15.272791037525746
     },
     "level": "pass",
     "why": "takes a 12.2° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "40 kg person",
     "what": "a child or a small adult",
     "opts": {
      "personMass": 40
     },
     "tipUp": 11.044611548506047,
     "tipDown": 21.59778491632951,
     "drop": 0,
     "tilt": 5.053139626979238,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.3051319392889519,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.85350419499082,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 24.663731694378527,
      "tip": -10.931041927041855
     },
     "level": "pass",
     "why": "takes a 11.0° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 10 cm towards the feet",
     "what": "held by the harness and foot stop",
     "opts": {
      "comOffset": -0.1
     },
     "tipUp": 10.667255985232204,
     "tipDown": 15.699023392149696,
     "drop": 0,
     "tilt": 4.97582223768563,
     "steps": 0.37911483317692296,
     "stepsPart": "backrest",
     "tracks": 0.14895575444339187,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.85350419499082,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 24.663731694378534,
      "tip": -11.241276863320062
     },
     "level": "pass",
     "why": "takes a 10.7° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 10 cm towards the head",
     "what": "held by the harness",
     "opts": {
      "comOffset": 0.1
     },
     "tipUp": 12.388572724737967,
     "tipDown": 21.50599204969762,
     "drop": 0,
     "tilt": 4.9758222376856285,
     "steps": 0.4580072831008371,
     "stepsPart": "thigh",
     "tracks": 0.25685004410000045,
     "tracksHit": {
      "part": "thigh",
      "unit": "front"
     },
     "hinge": 39.85350419499082,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.490383328416,
      "tip": -11.06264535240602
     },
     "level": "pass",
     "why": "takes a 12.4° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 25 cm towards the feet",
     "what": "no harness or foot stop",
     "opts": {
      "comOffset": -0.25
     },
     "tipUp": 10.899572594551723,
     "tipDown": 11.048292577103723,
     "drop": 0,
     "tilt": 5.584909401787958,
     "steps": 0.2753411161679272,
     "stepsPart": "backrest",
     "tracks": 0.030697777844673257,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.85350419499082,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.3085405800942862,
      "tilt": 24.66373169437853,
      "tip": -15.861174106285004
     },
     "level": "pass",
     "why": "takes a 10.9° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Posture",
     "name": "Sitting up",
     "what": "15° recline",
     "opts": {
      "reclineDeg": 15
     },
     "tipUp": 10.290050673928034,
     "tipDown": 18.463681511521678,
     "drop": 0,
     "tilt": 4.975822237685627,
     "steps": 0.24411738536072483,
     "stepsPart": "leg rest",
     "tracks": 0.06203982926879423,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.85350419499082,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.490383328416016,
      "tip": -12.906361188278828
     },
     "level": "pass",
     "why": "takes a 10.3° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Posture",
     "name": "Lying flat",
     "what": "90° recline",
     "opts": {
      "reclineDeg": 90
     },
     "tipUp": 11.677317361743302,
     "tipDown": 20.276863626743232,
     "drop": 0,
     "tilt": 4.975822237685627,
     "steps": 0.11174909805413888,
     "stepsPart": "backrest",
     "tracks": 0.03010393344776252,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.85350419499082,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 24.290383328416002,
      "tip": -12.485471172342972
     },
     "level": "pass",
     "why": "takes a 11.7° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Posture",
     "name": "Lying flat and slides 10 cm towards the feet",
     "what": "the case a single post looks worst for",
     "opts": {
      "reclineDeg": 90,
      "comOffset": -0.1
     },
     "tipUp": 10.711330728451667,
     "tipDown": 17.00021328405529,
     "drop": 0,
     "tilt": 5.034839408771837,
     "steps": 0.05986148738828488,
     "stepsPart": "backrest",
     "tracks": 0.03010393344776252,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.85350419499082,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 24.663731694378534,
      "tip": -12.943858464718398
     },
     "level": "pass",
     "why": "takes a 10.7° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Stairs",
     "name": "Steeper stairs",
     "what": "250 mm treads, 34.2°",
     "opts": {
      "going": 0.25
     },
     "tipUp": 10.550862327728328,
     "tipDown": 11.95326143515921,
     "drop": 0,
     "tilt": 5.032696579584604,
     "steps": 0.3814365009910623,
     "stepsPart": "backrest",
     "tracks": 0.17900229299811918,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 41.583519550744924,
     "extra": 44.82543709050636,
     "one": {
      "drop": 0.25777511106843587,
      "tilt": 27.542354049517492,
      "tip": -15.538675815731052
     },
     "level": "pass",
     "why": "takes a 10.6° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Stairs",
     "name": "Steepest stairs",
     "what": "180 mm rise, 250 mm treads, 35.8°",
     "opts": {
      "rise": 0.18,
      "going": 0.25
     },
     "tipUp": 9.454235345481298,
     "tipDown": 9.394155758071296,
     "drop": 0,
     "tilt": 5.840297669010354,
     "steps": 0.33610782637436154,
     "stepsPart": "backrest",
     "tracks": 0.13945805698394248,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 44.69963321697185,
     "extra": 44.86969151708756,
     "one": {
      "drop": 0.28218728012645045,
      "tilt": 30.353887254436774,
      "tip": -18.2710332780266
     },
     "level": "pass",
     "why": "takes a 9.4° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Motors",
     "name": "Hinge motor at three-quarter speed",
     "what": "90°/m, or driving a third faster",
     "opts": {
      "hingeRateDegPerM": 90
     },
     "tipUp": 9.112457067789672,
     "tipDown": 15.261277576914818,
     "drop": 0,
     "tilt": 5.036656138068298,
     "steps": 0.4210684064150648,
     "stepsPart": "backrest",
     "tracks": 0.21240328258369764,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 38.32748171851321,
     "extra": 37.91371953087075,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 9.1° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Motors",
     "name": "Hinge motor at half speed",
     "what": "60°/m, or driving twice as fast",
     "opts": {
      "hingeRateDegPerM": 60
     },
     "tipUp": 10.44699919979902,
     "tipDown": -11.38702293424007,
     "drop": 0.2269988243016292,
     "tilt": 15.127229431746658,
     "steps": 0.4137870320509154,
     "stepsPart": "leg rest",
     "tracks": 0.16692845664504283,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 35.39999999999998,
     "extra": 28.930071499990383,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "fail",
     "why": "rocks over and drops 23 cm"
    },
    {
     "group": "Motors",
     "name": "Hinge range cut to ±45°",
     "what": "a smaller hinge motor",
     "opts": {
      "hingeLimitDeg": 45
     },
     "tipUp": 9.210271897851518,
     "tipDown": 9.410529940558542,
     "drop": 0,
     "tilt": 4.937071277964386,
     "steps": 0.4383552791487184,
     "stepsPart": "backrest",
     "tracks": 0.2470328579853118,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 37.561739608007876,
     "extra": 41.71656890926383,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 9.2° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Motors",
     "name": "Hinge motor half as fast again",
     "what": "180°/m: not a stress, a possible fix",
     "opts": {
      "hingeRateDegPerM": 180
     },
     "tipUp": 12.451720498631976,
     "tipDown": 21.93294040737171,
     "drop": 0,
     "tilt": 4.555181952547426,
     "steps": 0.45696063302323964,
     "stepsPart": "backrest",
     "tracks": 0.2220685070120287,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 43.22611328571713,
     "extra": 53.65946763486047,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 12.5° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Motors",
     "name": "Seat drive at half speed",
     "what": "75°/m",
     "opts": {
      "levelRateDegPerM": 75
     },
     "tipUp": 10.680122638417412,
     "tipDown": 18.71662888044187,
     "drop": 0,
     "tilt": 6.512896223030973,
     "steps": 0.44283000953325935,
     "stepsPart": "backrest",
     "tracks": 0.22387018433466752,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.85350419499082,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 29.362662239355462,
      "tip": -12.373889768232564
     },
     "level": "pass",
     "why": "takes a 10.7° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Arm drive seizes in the middle",
     "what": "then keeps going",
     "opts": {
      "armLockDeg": 0
     },
     "tipUp": 8.98570603063134,
     "tipDown": 15.544536174802166,
     "drop": 0,
     "tilt": 5.053139626979238,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.3184304227638417,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.85350419499082,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 22.490383328416005,
      "tip": -15.437476410629898
     },
     "level": "pass",
     "why": "takes a 9.0° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Arm drive seizes leaning 20° uphill",
     "what": "then keeps going",
     "opts": {
      "armLockDeg": -20
     },
     "tipUp": 15.295615238453992,
     "tipDown": 23.94683607889266,
     "drop": 0,
     "tilt": 4.9758222376856285,
     "steps": 0.44941718904246997,
     "stepsPart": "backrest",
     "tracks": 0.2349409079570219,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.85350419499082,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.31626574206000946,
      "tilt": 22.611307757636457,
      "tip": -20.164944243615594
     },
     "level": "pass",
     "why": "takes a 15.3° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Arm drive seizes leaning 20° downhill",
     "what": "then keeps going",
     "opts": {
      "armLockDeg": 20
     },
     "tipUp": 10.241370776849632,
     "tipDown": 7.13794842574226,
     "drop": 0,
     "tilt": 12.296306735704615,
     "steps": 0.41107354660014594,
     "stepsPart": "leg rest",
     "tracks": 0.3360457758259686,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.85350419499082,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.41145997362521847,
      "tilt": 22.61130775763646,
      "tip": -25.769195166382975
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 7.1°, needs 7.3°)"
    },
    {
     "group": "Failures",
     "name": "Seat drive stuck level",
     "what": "fails on the flat; the arm takes over levelling",
     "opts": {
      "levelLockDeg": 0
     },
     "tipUp": 12.386117428100249,
     "tipDown": 19.40923099290421,
     "drop": 0,
     "tilt": 5.837071272770488,
     "steps": 0.4560296661362757,
     "stepsPart": "backrest",
     "tracks": 0.2760293849718851,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.85350419499082,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.3518144864260613,
      "tilt": 28.011307757636455,
      "tip": -26.142165322291472
     },
     "level": "pass",
     "why": "takes a 12.4° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Seat drive stuck on a flight",
     "what": "fails at 31.6°; the arm takes over levelling",
     "opts": {
      "levelLockDeg": 31.6
     },
     "tipUp": 9.016313690512694,
     "tipDown": 6.073429354507374,
     "drop": 0,
     "tilt": 5.837071272770488,
     "steps": 0.40756838081531155,
     "stepsPart": "leg rest",
     "tracks": 0.34290637558400006,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.85350419499082,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.41145997362521847,
      "tilt": 28.011307757636455,
      "tip": -31.703001700346334
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 6.1°, needs 7.3°)"
    },
    {
     "group": "Motors",
     "name": "Extra hinge motor at half speed",
     "what": "120°/m instead of 240°/m; the seat's hinge at full speed",
     "opts": {
      "extraHingeRateDegPerM": 120
     },
     "tipUp": 10.264574512527721,
     "tipDown": 9.309175452288397,
     "drop": 0,
     "tilt": 4.975822237685627,
     "steps": 0.4419361899047749,
     "stepsPart": "backrest",
     "tracks": 0.2502132805614351,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.85350419499082,
     "extra": 35.143059653765164,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 9.3° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Extra hinge seizes straight",
     "what": "then keeps going",
     "opts": {
      "extraHingeSeized": true
     },
     "tipUp": 10.26457326929744,
     "tipDown": 7.734035526543588,
     "drop": 0,
     "tilt": 5.0335557102498605,
     "steps": 0.46224930925498375,
     "stepsPart": "backrest",
     "tracks": 0.26836561170396867,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.85350419499082,
     "extra": 0,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 7.7° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Seat's hinge motor seizes straight",
     "what": "the extra hinge still works, the tracks keep driving",
     "opts": {
      "mainHingeSeized": true
     },
     "tipUp": -9.272649949302053,
     "tipDown": -12.375988767699951,
     "drop": 0.2142655869046317,
     "tilt": 25.490383328426827,
     "steps": 0.48695865463770815,
     "stepsPart": "leg rest",
     "tracks": 0.28272162242731136,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 0,
     "extra": 48.11709948175509,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "fail",
     "why": "the long part rocks over edges and drops 21 cm, so the tracks must stop if the hinge stops"
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
     "tipUp": 7.360067130699494,
     "tipDown": 6.275339890918105,
     "drop": 0,
     "tilt": 5.840297669010359,
     "steps": 0.24007591526411945,
     "stepsPart": "backrest",
     "tracks": 0.03354257843474792,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 46.630717287873544,
     "extra": 44.86969151708756,
     "one": {
      "drop": 0.28713986777303013,
      "tilt": 27.629133819911843,
      "tip": -21.85010555131527
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 6.3°, needs 7.3°)"
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
     "tipUp": 9.696437785965186,
     "tipDown": 5.59950299657334,
     "drop": 0,
     "tilt": 5.840297669010355,
     "steps": -0.03,
     "stepsPart": "backrest",
     "tracks": -0.027959100229740574,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 44.31473328088453,
     "extra": 44.86969151708756,
     "one": {
      "drop": 0.2871398677730297,
      "tilt": 30.35388725443676,
      "tip": -20.861689712441297
     },
     "level": "fail",
     "why": "the seat or person hits the tracks or steps"
    }
   ]
  },
  {
   "id": "rearSplit",
   "name": "Rear half split in two",
   "opts": {
    "mastMode": "balance",
    "sections": [
     0.35,
     0.35,
     0.7
    ],
    "mainJoint": 2
   },
   "split": true,
   "count": {
    "pass": 19,
    "warn": 4,
    "fail": 3
   },
   "structure": {
    "normal": {
     "members": [
      {
       "part": "Columns",
       "size": "2 × 50 × 50 × 4 mm box tube, 0.4 m apart",
       "load": "999 N·m bend",
       "stress": 47770598.634597145,
       "limit": 355000000,
       "factor": 7.431349201115025
      },
      {
       "part": "Averaging links",
       "size": "12 mm rods, a diamond each side",
       "load": "1.7 kN each",
       "stress": 14762816.678163087,
       "limit": 355000000,
       "factor": 24.04690160009303
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
       "need": "999 N·m",
       "note": "self-locking; leans the arm to keep the weight away from the edges"
      },
      {
       "part": "Seat tilt drives",
       "need": "479 N·m each",
       "note": "two, self-locking; either one holds the seat alone"
      },
      {
       "part": "Track drives",
       "need": "47 N·m, 258 W",
       "note": "per unit and in total, at 0.25 m/s; spring brakes"
      }
     ]
    },
    "heavy": {
     "members": [
      {
       "part": "Columns",
       "size": "2 × 50 × 50 × 4 mm box tube, 0.4 m apart",
       "load": "1720 N·m bend",
       "stress": 82191385.75257833,
       "limit": 355000000,
       "factor": 4.319187427605376
      },
      {
       "part": "Averaging links",
       "size": "12 mm rods, a diamond each side",
       "load": "2.9 kN each",
       "stress": 25400066.046288345,
       "limit": 355000000,
       "factor": 13.976341610807557
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
       "need": "1720 N·m",
       "note": "self-locking; leans the arm to keep the weight away from the edges"
      },
      {
       "part": "Seat tilt drives",
       "need": "765 N·m each",
       "note": "two, self-locking; either one holds the seat alone"
      },
      {
       "part": "Track drives",
       "need": "65 N·m, 361 W",
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
     "tipUp": 17.89510961248308,
     "tipDown": 9.986459961664403,
     "drop": 0,
     "tilt": 5.0335557102498605,
     "steps": 0.44590125914355194,
     "stepsPart": "backrest",
     "tracks": 0.2537389674652971,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 37.948738558841626,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 10.0° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "200 kg person",
     "what": "two thirds more than planned",
     "opts": {
      "personMass": 200
     },
     "tipUp": 17.71235681359753,
     "tipDown": 8.568561592817446,
     "drop": 0,
     "tilt": 5.0335557102498605,
     "steps": 0.42135615334177245,
     "stepsPart": "backrest",
     "tracks": 0.23191008402308863,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 37.948738558841626,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.490383328416016,
      "tip": -15.272791037525746
     },
     "level": "pass",
     "why": "takes a 8.6° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "40 kg person",
     "what": "a child or a small adult",
     "opts": {
      "personMass": 40
     },
     "tipUp": 22.430310860549653,
     "tipDown": 13.659072392804672,
     "drop": 0,
     "tilt": 5.0335557102498605,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.296808984328657,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "extra": 34.83057387352714,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 24.663731694378527,
      "tip": -10.931041927041855
     },
     "level": "pass",
     "why": "takes a 13.7° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 10 cm towards the feet",
     "what": "held by the harness and foot stop",
     "opts": {
      "comOffset": -0.1
     },
     "tipUp": 16.55963977571101,
     "tipDown": 9.427972420811487,
     "drop": 0,
     "tilt": 5.0335557102498605,
     "steps": 0.37804287902752876,
     "stepsPart": "backrest",
     "tracks": 0.19385048485598352,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 37.948738558841626,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 24.663731694378534,
      "tip": -11.241276863320062
     },
     "level": "pass",
     "why": "takes a 9.4° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 10 cm towards the head",
     "what": "held by the harness",
     "opts": {
      "comOffset": 0.1
     },
     "tipUp": 21.345978877076945,
     "tipDown": 9.725666388516807,
     "drop": 0,
     "tilt": 5.0335557102498605,
     "steps": 0.4623270028858219,
     "stepsPart": "thigh",
     "tracks": 0.2806549400311127,
     "tracksHit": {
      "part": "thigh",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 37.948738558841626,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.490383328416,
      "tip": -11.06264535240602
     },
     "level": "pass",
     "why": "takes a 9.7° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 25 cm towards the feet",
     "what": "no harness or foot stop",
     "opts": {
      "comOffset": -0.25
     },
     "tipUp": 15.824449264978856,
     "tipDown": 10.192952456625486,
     "drop": 0,
     "tilt": 7.4764938820703035,
     "steps": 0.2739852082755002,
     "stepsPart": "backrest",
     "tracks": 0.09362795596193768,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 37.948738558841626,
     "one": {
      "drop": 0.3085405800942862,
      "tilt": 24.66373169437853,
      "tip": -15.861174106285004
     },
     "level": "pass",
     "why": "takes a 10.2° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Posture",
     "name": "Sitting up",
     "what": "15° recline",
     "opts": {
      "reclineDeg": 15
     },
     "tipUp": 17.687139671237503,
     "tipDown": 9.576795098691264,
     "drop": 0,
     "tilt": 5.0335557102498605,
     "steps": 0.24628210528662522,
     "stepsPart": "leg rest",
     "tracks": 0.05813967803528333,
     "tracksHit": {
      "part": "leg rest",
      "unit": "middle"
     },
     "hinge": 39.853504194990855,
     "extra": 37.948738558841626,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.490383328416016,
      "tip": -12.906361188278828
     },
     "level": "pass",
     "why": "takes a 9.6° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Posture",
     "name": "Lying flat",
     "what": "90° recline",
     "opts": {
      "reclineDeg": 90
     },
     "tipUp": 20.440530644910066,
     "tipDown": 11.259617671747614,
     "drop": 0,
     "tilt": 5.0335557102498605,
     "steps": 0.11009202094915899,
     "stepsPart": "backrest",
     "tracks": 0.021130267610286357,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 37.948738558841626,
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
     "tipUp": 16.504390399138877,
     "tipDown": 9.854545629172879,
     "drop": 0,
     "tilt": 5.0335557102498605,
     "steps": 0.058507529695312255,
     "stepsPart": "backrest",
     "tracks": 0.0301039334477623,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 37.948738558841626,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 24.663731694378534,
      "tip": -12.943858464718398
     },
     "level": "pass",
     "why": "takes a 9.9° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Stairs",
     "name": "Steeper stairs",
     "what": "250 mm treads, 34.2°",
     "opts": {
      "going": 0.25
     },
     "tipUp": 14.645386330107653,
     "tipDown": 9.560034027578958,
     "drop": 0,
     "tilt": 5.0497355517036615,
     "steps": 0.37912284188961387,
     "stepsPart": "backrest",
     "tracks": 0.19807766760080467,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 42.32299297198411,
     "extra": 39.86388339774551,
     "one": {
      "drop": 0.25777511106843587,
      "tilt": 27.542354049517492,
      "tip": -15.538675815731052
     },
     "level": "pass",
     "why": "takes a 9.6° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Stairs",
     "name": "Steepest stairs",
     "what": "180 mm rise, 250 mm treads, 35.8°",
     "opts": {
      "rise": 0.18,
      "going": 0.25
     },
     "tipUp": 11.29507986074578,
     "tipDown": 8.33473216114321,
     "drop": 0,
     "tilt": 4.208255895352068,
     "steps": 0.3327006801745538,
     "stepsPart": "backrest",
     "tracks": 0.15260029642714373,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 45.47105683981243,
     "extra": 40.35006057841183,
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
     "tipUp": 17.89510961248308,
     "tipDown": 10.604709621860513,
     "drop": 0,
     "tilt": 5.101710315470173,
     "steps": 0.42632195323959576,
     "stepsPart": "backrest",
     "tracks": 0.23639872007606064,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.0088891730695,
     "extra": 32.90706204301751,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 10.6° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Motors",
     "name": "Hinge motor at half speed",
     "what": "60°/m, or driving twice as fast",
     "opts": {
      "hingeRateDegPerM": 60
     },
     "tipUp": 12.513341860489748,
     "tipDown": -9.906616320929434,
     "drop": 0.1651668351124318,
     "tilt": 16.46768349746362,
     "steps": 0.45056040289294064,
     "stepsPart": "backrest",
     "tracks": 0.24075156862344413,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 35.41172844726432,
     "extra": 26.322542942745148,
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
     "tipUp": 12.431337766550804,
     "tipDown": 8.46355104990774,
     "drop": 0,
     "tilt": 5.0335557102498605,
     "steps": 0.44283000953325935,
     "stepsPart": "backrest",
     "tracks": 0.25100156687316766,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 37.561739608007876,
     "extra": 34.13445835354528,
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
     "name": "Hinge motor half as fast again",
     "what": "180°/m: not a stress, a possible fix",
     "opts": {
      "hingeRateDegPerM": 180
     },
     "tipUp": 17.89510961248308,
     "tipDown": 8.833639676807309,
     "drop": 0,
     "tilt": 4.495115931286631,
     "steps": 0.4642380072063872,
     "stepsPart": "backrest",
     "tracks": 0.27016302584597573,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 43.22611328571713,
     "extra": 44.421123463807376,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 8.8° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Motors",
     "name": "Seat drive at half speed",
     "what": "75°/m",
     "opts": {
      "levelRateDegPerM": 75
     },
     "tipUp": 17.89510961248308,
     "tipDown": 10.238741252785337,
     "drop": 0,
     "tilt": 6.135535916535343,
     "steps": 0.44590125914355194,
     "stepsPart": "backrest",
     "tracks": 0.2537389674652971,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 37.948738558841626,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 29.362662239355462,
      "tip": -12.373889768232564
     },
     "level": "pass",
     "why": "takes a 10.2° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Arm drive seizes in the middle",
     "what": "then keeps going",
     "opts": {
      "armLockDeg": 0
     },
     "tipUp": 17.740505039165814,
     "tipDown": 9.201065556479636,
     "drop": 0,
     "tilt": 5.0335557102498605,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.3033538723102307,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "extra": 33.83416574383092,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 22.490383328416005,
      "tip": -15.437476410629898
     },
     "level": "pass",
     "why": "takes a 9.2° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Arm drive seizes leaning 20° uphill",
     "what": "then keeps going",
     "opts": {
      "armLockDeg": -20
     },
     "tipUp": 17.6519328263708,
     "tipDown": 10.693268310219798,
     "drop": 0,
     "tilt": 5.0335557102498605,
     "steps": 0.44941718904246997,
     "stepsPart": "backrest",
     "tracks": 0.256168534779713,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 37.948738558841626,
     "one": {
      "drop": 0.31626574206000946,
      "tilt": 22.611307757636457,
      "tip": -20.164944243615594
     },
     "level": "pass",
     "why": "takes a 10.7° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Arm drive seizes leaning 20° downhill",
     "what": "then keeps going",
     "opts": {
      "armLockDeg": 20
     },
     "tipUp": 9.639531324628528,
     "tipDown": 3.723430859726047,
     "drop": 0,
     "tilt": 11.611307757635084,
     "steps": 0.3581498910456493,
     "stepsPart": "leg rest",
     "tracks": 0.33257199460650777,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "extra": 31.26785278948997,
     "one": {
      "drop": 0.41145997362521847,
      "tilt": 22.61130775763646,
      "tip": -25.769195166382975
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 3.7°, needs 7.3°)"
    },
    {
     "group": "Failures",
     "name": "Seat drive stuck level",
     "what": "fails on the flat; the arm takes over levelling",
     "opts": {
      "levelLockDeg": 0
     },
     "tipUp": 15.80608071239394,
     "tipDown": 8.72532710315032,
     "drop": 0,
     "tilt": 5.933555710249862,
     "steps": 0.4560296661362757,
     "stepsPart": "backrest",
     "tracks": 0.2760293849718851,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 37.948738558841626,
     "one": {
      "drop": 0.3518144864260613,
      "tilt": 28.011307757636455,
      "tip": -26.142165322291472
     },
     "level": "pass",
     "why": "takes a 8.7° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Seat drive stuck on a flight",
     "what": "fails at 31.6°; the arm takes over levelling",
     "opts": {
      "levelLockDeg": 31.6
     },
     "tipUp": 17.65425125219743,
     "tipDown": 2.861066270623044,
     "drop": 0,
     "tilt": 5.933555710249858,
     "steps": 0.4075683297454653,
     "stepsPart": "leg rest",
     "tracks": 0.34290637558400006,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "extra": 31.26785278948997,
     "one": {
      "drop": 0.41145997362521847,
      "tilt": 28.011307757636455,
      "tip": -31.703001700346334
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 2.9°, needs 7.3°)"
    },
    {
     "group": "Motors",
     "name": "Extra hinge motor at half speed",
     "what": "120°/m instead of 240°/m; the seat's hinge at full speed",
     "opts": {
      "extraHingeRateDegPerM": 120
     },
     "tipUp": 13.331168526626161,
     "tipDown": 9.986459961664403,
     "drop": 0,
     "tilt": 5.0335557102498605,
     "steps": 0.44590125914355194,
     "stepsPart": "backrest",
     "tracks": 0.2537389674652971,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 34.8,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 10.0° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Extra hinge seizes straight",
     "what": "then keeps going",
     "opts": {
      "extraHingeSeized": true
     },
     "tipUp": 10.039711880533174,
     "tipDown": 9.986458630652374,
     "drop": 0,
     "tilt": 5.0335557102498605,
     "steps": 0.44590125914355194,
     "stepsPart": "backrest",
     "tracks": 0.2537389674652971,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.85350419499082,
     "extra": 0,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 10.0° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Seat's hinge motor seizes straight",
     "what": "the extra hinge still works, the tracks keep driving",
     "opts": {
      "mainHingeSeized": true
     },
     "tipUp": -9.328425762158163,
     "tipDown": -12.12190815175627,
     "drop": 0.22818618387216283,
     "tilt": 25.490383328426827,
     "steps": 0.4798956537229191,
     "stepsPart": "leg rest",
     "tracks": 0.2861053181412313,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 0,
     "extra": 42.708495419365434,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "fail",
     "why": "the long part rocks over edges and drops 23 cm, so the tracks must stop if the hinge stops"
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
     "tipUp": 8.178726429275477,
     "tipDown": 5.713511314265542,
     "drop": 0,
     "tilt": 9.279127947676074,
     "steps": 0.2355070640087081,
     "stepsPart": "backrest",
     "tracks": 0.04922307563845485,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 47.018021367524256,
     "extra": 40.35006057841183,
     "one": {
      "drop": 0.28713986777303013,
      "tilt": 27.629133819911843,
      "tip": -21.85010555131527
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 5.7°, needs 7.3°)"
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
     "tipUp": 11.724673352729958,
     "tipDown": 4.889045072919421,
     "drop": 0,
     "tilt": 3.93001996248614,
     "steps": -0.03,
     "stepsPart": "backrest",
     "tracks": -0.04324613736580607,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 44.69963321697185,
     "extra": 40.35006057841183,
     "one": {
      "drop": 0.2871398677730297,
      "tilt": 30.35388725443676,
      "tip": -20.861689712441297
     },
     "level": "fail",
     "why": "the seat or person hits the tracks or steps"
    }
   ]
  },
  {
   "id": "bothSplit",
   "name": "Both halves split in two",
   "opts": {
    "mastMode": "balance",
    "sections": [
     0.35,
     0.35,
     0.35,
     0.35
    ],
    "mainJoint": 2
   },
   "split": true,
   "count": {
    "pass": 20,
    "warn": 3,
    "fail": 3
   },
   "structure": {
    "normal": {
     "members": [
      {
       "part": "Columns",
       "size": "2 × 50 × 50 × 4 mm box tube, 0.4 m apart",
       "load": "924 N·m bend",
       "stress": 44166678.91977348,
       "limit": 355000000,
       "factor": 8.03773361915754
      },
      {
       "part": "Averaging links",
       "size": "12 mm rods, a diamond each side",
       "load": "1.5 kN each",
       "stress": 13618094.68003839,
       "limit": 355000000,
       "factor": 26.06825758968796
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
       "need": "924 N·m",
       "note": "self-locking; leans the arm to keep the weight away from the edges"
      },
      {
       "part": "Seat tilt drives",
       "need": "478 N·m each",
       "note": "two, self-locking; either one holds the seat alone"
      },
      {
       "part": "Track drives",
       "need": "48 N·m, 266 W",
       "note": "per unit and in total, at 0.25 m/s; spring brakes"
      }
     ]
    },
    "heavy": {
     "members": [
      {
       "part": "Columns",
       "size": "2 × 50 × 50 × 4 mm box tube, 0.4 m apart",
       "load": "1511 N·m bend",
       "stress": 72242873.29309776,
       "limit": 355000000,
       "factor": 4.913979522377572
      },
      {
       "part": "Averaging links",
       "size": "12 mm rods, a diamond each side",
       "load": "2.5 kN each",
       "stress": 22274943.74776205,
       "limit": 355000000,
       "factor": 15.937189517511873
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
       "need": "1511 N·m",
       "note": "self-locking; leans the arm to keep the weight away from the edges"
      },
      {
       "part": "Seat tilt drives",
       "need": "763 N·m each",
       "note": "two, self-locking; either one holds the seat alone"
      },
      {
       "part": "Track drives",
       "need": "66 N·m, 369 W",
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
     "tipUp": 18.771717614078593,
     "tipDown": 18.372838082612585,
     "drop": 0,
     "tilt": 4.937071272770486,
     "steps": 0.44283000953325935,
     "stepsPart": "backrest",
     "tracks": 0.22387018433466752,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 18.4° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "200 kg person",
     "what": "two thirds more than planned",
     "opts": {
      "personMass": 200
     },
     "tipUp": 17.546170539701777,
     "tipDown": 17.73141429345868,
     "drop": 0,
     "tilt": 4.937071272770486,
     "steps": 0.41549836428572706,
     "stepsPart": "backrest",
     "tracks": 0.21247599320002528,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.490383328416016,
      "tip": -15.272791037525746
     },
     "level": "pass",
     "why": "takes a 17.5° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "40 kg person",
     "what": "a child or a small adult",
     "opts": {
      "personMass": 40
     },
     "tipUp": 23.943247972389823,
     "tipDown": 21.024285457929988,
     "drop": 0,
     "tilt": 4.9370712727704875,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.3058609972526741,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 24.663731694378527,
      "tip": -10.931041927041855
     },
     "level": "pass",
     "why": "takes a 21.0° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 10 cm towards the feet",
     "what": "held by the harness and foot stop",
     "opts": {
      "comOffset": -0.1
     },
     "tipUp": 16.895618918491262,
     "tipDown": 15.51444353158877,
     "drop": 0,
     "tilt": 4.937071272770486,
     "steps": 0.37804287902752876,
     "stepsPart": "backrest",
     "tracks": 0.14778283612515175,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 24.663731694378534,
      "tip": -11.241276863320062
     },
     "level": "pass",
     "why": "takes a 15.5° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 10 cm towards the head",
     "what": "held by the harness",
     "opts": {
      "comOffset": 0.1
     },
     "tipUp": 21.946181827079982,
     "tipDown": 21.38132831344382,
     "drop": 0,
     "tilt": 4.937071272770486,
     "steps": 0.4583404954177048,
     "stepsPart": "thigh",
     "tracks": 0.2572352906904498,
     "tracksHit": {
      "part": "thigh",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.490383328416,
      "tip": -11.06264535240602
     },
     "level": "pass",
     "why": "takes a 21.4° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Load",
     "name": "Slides 25 cm towards the feet",
     "what": "no harness or foot stop",
     "opts": {
      "comOffset": -0.25
     },
     "tipUp": 15.476876424912962,
     "tipDown": 10.721784207786747,
     "drop": 0,
     "tilt": 5.434909401787955,
     "steps": 0.276476818015712,
     "stepsPart": "backrest",
     "tracks": 0.03239422465030248,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.3085405800942862,
      "tilt": 24.66373169437853,
      "tip": -15.861174106285004
     },
     "level": "pass",
     "why": "takes a 10.7° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Posture",
     "name": "Sitting up",
     "what": "15° recline",
     "opts": {
      "reclineDeg": 15
     },
     "tipUp": 18.55868065496624,
     "tipDown": 18.281909984254447,
     "drop": 0,
     "tilt": 4.937071272770486,
     "steps": 0.24386747478426943,
     "stepsPart": "leg rest",
     "tracks": 0.061795946885154523,
     "tracksHit": {
      "part": "leg rest",
      "unit": "middle"
     },
     "hinge": 39.853504194990855,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.490383328416016,
      "tip": -12.906361188278828
     },
     "level": "pass",
     "why": "takes a 18.3° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Posture",
     "name": "Lying flat",
     "what": "90° recline",
     "opts": {
      "reclineDeg": 90
     },
     "tipUp": 21.345734148147038,
     "tipDown": 20.062189814945572,
     "drop": 0,
     "tilt": 4.937071272770486,
     "steps": 0.11071238043573883,
     "stepsPart": "backrest",
     "tracks": 0.030103933447762188,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 24.290383328416002,
      "tip": -12.485471172342972
     },
     "level": "pass",
     "why": "takes a 20.1° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Posture",
     "name": "Lying flat and slides 10 cm towards the feet",
     "what": "the case a single post looks worst for",
     "opts": {
      "reclineDeg": 90,
      "comOffset": -0.1
     },
     "tipUp": 17.52992572306342,
     "tipDown": 16.596540251188333,
     "drop": 0,
     "tilt": 4.937071272770486,
     "steps": 0.06077344977683216,
     "stepsPart": "backrest",
     "tracks": 0.030103933447762188,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 24.663731694378534,
      "tip": -12.943858464718398
     },
     "level": "pass",
     "why": "takes a 16.6° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Stairs",
     "name": "Steeper stairs",
     "what": "250 mm treads, 34.2°",
     "opts": {
      "going": 0.25
     },
     "tipUp": 15.27212377449954,
     "tipDown": 11.357131874514817,
     "drop": 0,
     "tilt": 4.922451607059491,
     "steps": 0.3824167498727499,
     "stepsPart": "backrest",
     "tracks": 0.1754985235916152,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 41.583519550744924,
     "extra": 44.82543709050636,
     "one": {
      "drop": 0.25777511106843587,
      "tilt": 27.542354049517492,
      "tip": -15.538675815731052
     },
     "level": "pass",
     "why": "takes a 11.4° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Stairs",
     "name": "Steepest stairs",
     "what": "180 mm rise, 250 mm treads, 35.8°",
     "opts": {
      "rise": 0.18,
      "going": 0.25
     },
     "tipUp": 11.89030251408676,
     "tipDown": 8.835460155640776,
     "drop": 0,
     "tilt": 5.736659628956731,
     "steps": 0.3345804785173353,
     "stepsPart": "backrest",
     "tracks": 0.12944885580785395,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 44.69963321697185,
     "extra": 44.86969151708756,
     "one": {
      "drop": 0.28218728012645045,
      "tilt": 30.353887254436774,
      "tip": -18.2710332780266
     },
     "level": "pass",
     "why": "takes a 8.8° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Motors",
     "name": "Hinge motor at three-quarter speed",
     "what": "90°/m, or driving a third faster",
     "opts": {
      "hingeRateDegPerM": 90
     },
     "tipUp": 18.54374351012695,
     "tipDown": 14.764008323688122,
     "drop": 0,
     "tilt": 5.036656138068298,
     "steps": 0.41857254952273415,
     "stepsPart": "backrest",
     "tracks": 0.21082373684278385,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 38.66805170676522,
     "extra": 37.91371953087075,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 14.8° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Motors",
     "name": "Hinge motor at half speed",
     "what": "60°/m, or driving twice as fast",
     "opts": {
      "hingeRateDegPerM": 60
     },
     "tipUp": 11.752010026593684,
     "tipDown": -10.638594048859737,
     "drop": 0.1697947609831112,
     "tilt": 15.127232201750418,
     "steps": 0.4063228162294803,
     "stepsPart": "leg rest",
     "tracks": 0.16273910178038772,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 36.09298458143432,
     "extra": 28.930071499990383,
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
     "tipUp": 12.43031311277663,
     "tipDown": 8.968900347793864,
     "drop": 0,
     "tilt": 4.937071277964386,
     "steps": 0.4383552791487184,
     "stepsPart": "backrest",
     "tracks": 0.2470328579853118,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 37.561739608007876,
     "extra": 41.71656890926383,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 9.0° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Motors",
     "name": "Hinge motor half as fast again",
     "what": "180°/m: not a stress, a possible fix",
     "opts": {
      "hingeRateDegPerM": 180
     },
     "tipUp": 18.771717614078593,
     "tipDown": 21.896024275117085,
     "drop": 0,
     "tilt": 4.283239501513652,
     "steps": 0.4585992714443742,
     "stepsPart": "backrest",
     "tracks": 0.21986331073947304,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 43.22611328571713,
     "extra": 53.65946763486047,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 18.8° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Motors",
     "name": "Seat drive at half speed",
     "what": "75°/m",
     "opts": {
      "levelRateDegPerM": 75
     },
     "tipUp": 18.771717614078593,
     "tipDown": 18.372838082612585,
     "drop": 0,
     "tilt": 5.960590383835963,
     "steps": 0.44283000953325935,
     "stepsPart": "backrest",
     "tracks": 0.22387018433466752,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 29.362662239355462,
      "tip": -12.373889768232564
     },
     "level": "pass",
     "why": "takes a 18.4° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Arm drive seizes in the middle",
     "what": "then keeps going",
     "opts": {
      "armLockDeg": 0
     },
     "tipUp": 18.62320904352771,
     "tipDown": 15.169496526457383,
     "drop": 0,
     "tilt": 4.937071272770486,
     "steps": 0.4859118180271377,
     "stepsPart": "leg rest",
     "tracks": 0.3184304227638417,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.23633325290796003,
      "tilt": 22.490383328416005,
      "tip": -15.437476410629898
     },
     "level": "pass",
     "why": "takes a 15.2° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Arm drive seizes leaning 20° uphill",
     "what": "then keeps going",
     "opts": {
      "armLockDeg": -20
     },
     "tipUp": 17.407985185686808,
     "tipDown": 23.812272109746385,
     "drop": 0,
     "tilt": 4.937071272770486,
     "steps": 0.44941718904246997,
     "stepsPart": "backrest",
     "tracks": 0.2349409079570219,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.31626574206000946,
      "tilt": 22.611307757636457,
      "tip": -20.164944243615594
     },
     "level": "pass",
     "why": "takes a 17.4° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Arm drive seizes leaning 20° downhill",
     "what": "then keeps going",
     "opts": {
      "armLockDeg": 20
     },
     "tipUp": 10.819411924790385,
     "tipDown": 6.724747519165893,
     "drop": 0,
     "tilt": 12.296308632979043,
     "steps": 0.3581498910456493,
     "stepsPart": "leg rest",
     "tracks": 0.3360457758259686,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.41145997362521847,
      "tilt": 22.61130775763646,
      "tip": -25.769195166382975
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 6.7°, needs 7.3°)"
    },
    {
     "group": "Failures",
     "name": "Seat drive stuck level",
     "what": "fails on the flat; the arm takes over levelling",
     "opts": {
      "levelLockDeg": 0
     },
     "tipUp": 15.56643794877315,
     "tipDown": 19.048772124294736,
     "drop": 0,
     "tilt": 5.837071272770488,
     "steps": 0.4560296661362757,
     "stepsPart": "backrest",
     "tracks": 0.2760293849718851,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.3518144864260613,
      "tilt": 28.011307757636455,
      "tip": -26.142165322291472
     },
     "level": "pass",
     "why": "takes a 15.6° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Seat drive stuck on a flight",
     "what": "fails at 31.6°; the arm takes over levelling",
     "opts": {
      "levelLockDeg": 31.6
     },
     "tipUp": 18.54038447799308,
     "tipDown": 5.654596149794953,
     "drop": 0,
     "tilt": 5.837071272770488,
     "steps": 0.4075683384231332,
     "stepsPart": "leg rest",
     "tracks": 0.34290637558400006,
     "tracksHit": {
      "part": "leg rest",
      "unit": "rear"
     },
     "hinge": 39.853504194990855,
     "extra": 44.27159828308214,
     "one": {
      "drop": 0.41145997362521847,
      "tilt": 28.011307757636455,
      "tip": -31.703001700346334
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 5.7°, needs 7.3°)"
    },
    {
     "group": "Motors",
     "name": "Extra hinge motor at half speed",
     "what": "120°/m instead of 240°/m; the seat's hinge at full speed",
     "opts": {
      "extraHingeRateDegPerM": 120
     },
     "tipUp": 13.217142244918902,
     "tipDown": 11.031717406103173,
     "drop": 0,
     "tilt": 4.948722874570999,
     "steps": 0.4423831706691793,
     "stepsPart": "backrest",
     "tracks": 0.25060776570089527,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.853504194990855,
     "extra": 35.143059653765164,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 11.0° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Extra hinge seizes straight",
     "what": "then keeps going",
     "opts": {
      "extraHingeSeized": true
     },
     "tipUp": 9.874726265058651,
     "tipDown": 8.825512380267746,
     "drop": 0,
     "tilt": 5.0335557102498605,
     "steps": 0.4630451861949323,
     "stepsPart": "backrest",
     "tracks": 0.26908672486665197,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 39.85350419499082,
     "extra": 0,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "pass",
     "why": "takes a 8.8° lean anywhere; a hard stop needs 7.3°"
    },
    {
     "group": "Failures",
     "name": "Seat's hinge motor seizes straight",
     "what": "the extra hinge still works, the tracks keep driving",
     "opts": {
      "mainHingeSeized": true
     },
     "tipUp": -8.942978168732258,
     "tipDown": -11.812672890775566,
     "drop": 0.2142655869046317,
     "tilt": 25.490383328426827,
     "steps": 0.4855704151354696,
     "stepsPart": "leg rest",
     "tracks": 0.2783488503147383,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 0,
     "extra": 48.11709948175509,
     "one": {
      "drop": 0.22818618387216283,
      "tilt": 25.49038332841601,
      "tip": -12.651588743991969
     },
     "level": "fail",
     "why": "the long part rocks over edges and drops 21 cm, so the tracks must stop if the hinge stops"
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
     "tipUp": 8.214521428059218,
     "tipDown": 5.808037217393562,
     "drop": 0,
     "tilt": 5.736659628956725,
     "steps": 0.2416318501190817,
     "stepsPart": "backrest",
     "tracks": 0.03354257843474795,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 46.630717287873544,
     "extra": 44.86969151708756,
     "one": {
      "drop": 0.28713986777303013,
      "tilt": 27.629133819911843,
      "tip": -21.85010555131527
     },
     "level": "warn",
     "why": "a hard stop at the wrong moment could rock it (takes 5.8°, needs 7.3°)"
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
     "tipUp": 12.649290931655328,
     "tipDown": 5.166264550665364,
     "drop": 0,
     "tilt": 5.736659628956727,
     "steps": -0.03,
     "stepsPart": "backrest",
     "tracks": -0.04324613736580607,
     "tracksHit": {
      "part": "backrest",
      "unit": "front"
     },
     "hinge": 44.31473328088453,
     "extra": 44.86969151708756,
     "one": {
      "drop": 0.2871398677730297,
      "tilt": 30.35388725443676,
      "tip": -20.861689712441297
     },
     "level": "fail",
     "why": "the seat or person hits the tracks or steps"
    }
   ]
  }
 ]
};
