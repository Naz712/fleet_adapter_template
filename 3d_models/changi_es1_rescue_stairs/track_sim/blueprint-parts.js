// Parts, build steps and guides for blueprint.html. The links were found by web search
// on 2026-09-29 and not opened; stock and prices were not checked.
(function () {
  const SG = true;
  const L = (shop, url, sg, where) => ({ shop, url, sg: !!sg, where });

  // pulleys by tooth count
  const PULLEY = {
    16: [L('Cytron SG, 16T 5 mm bore', 'https://sg.cytron.io/c-3d-modeling/c-3d-accessories/p-2gt-timing-belt-16-teeth-5mm-pulley', SG)],
    20: [L('Cytron SG, 20T 5 mm bore', 'https://sg.cytron.io/p-2gt-timing-belt-20-teeth-5mm-pulley', SG),
      L('SGBotic, 20T 5 mm bore', 'https://www.sgbotic.com/index.php?dispatch=products.view&product_id=2623', SG),
      L('Amazon SG, WINSINN 5-pack', 'https://www.amazon.sg/WINSINN-Pulley-Timing-Aluminum-Printer/dp/B077GNZK3J', SG)],
    25: [L('eBay, 25T 5–8 mm bore', 'https://www.ebay.com/itm/326343330035', false, 'ships from overseas'),
      L('AliExpress, POWGE 25T', 'https://www.aliexpress.com/item/1005003273419587.html', false, 'ships from overseas')],
    28: [L('Amazon US, 28T 4 mm bore', 'https://www.amazon.com/Timing-Pulley-Synchronous-Printer-NO-1052/dp/B0F23NCVVQ', false, 'ships from overseas'),
      L('eBay, 28T 4–8 mm bore', 'https://www.ebay.com/itm/155659793449', false, 'ships from overseas')],
    30: [L('SGBotic, 30T 5 mm bore', 'https://www.sgbotic.com/index.php?dispatch=products.view&product_id=2624', SG)],
    36: [L('RobotDigg, 36T 5 mm bore', 'https://www.robotdigg.com/product/24/GT2-Pulley-36-Teeth-5mm-Bore', false, 'ships from China'),
      L('Adafruit, 36T 5 mm bore', 'https://www.adafruit.com/product/1253', false, 'ships from the US')],
  };
  // closed GT2 loops, 6 mm wide, by length
  const RD100 = L('RobotDigg, 96–102 mm', 'https://www.robotdigg.com/product/38/96mm,-98mm,-100mm-or-102mm-2GT-closed-loop-belt', false, 'ships from China');
  const RD110 = L('RobotDigg, 110–116 mm', 'https://www.robotdigg.com/product/279/110mm-112mm-114mm-116mm-2GT-endless-belt', false, 'ships from China');
  const RD120 = L('RobotDigg, 120–130 mm', 'https://www.robotdigg.com/product/203/120mm,-122mm,-124mm,-126mm,-128mm-or-130mm-2GT-endless-belt', false, 'ships from China');
  const RD140 = L('RobotDigg, 140–156 mm', 'https://www.robotdigg.com/product/88/140/142/144/146/150/152/154-156mm-long-2GT-endless-belt', false, 'ships from China');
  const loopLinks = (l) => {
    if (l === 100) return [L('Amazon SG, Gates 100 mm', 'https://www.amazon.sg/Gates-Powergrip%C3%822GT-Belt-100mm-M-BELT-LL-GT2-6/dp/B07TXJC1TX', SG), RD100];
    if (l === 102) return [RD100];
    if (l === 110) return [L('Cytron SG, 110 mm', 'https://sg.cytron.io/p-3d-printer-closed-loop-timing-belt-2gt-110mm', SG), RD110];
    if (l === 112) return [L('SGBotic, 112 mm', 'https://www.sgbotic.com/index.php?dispatch=products.view&product_id=2630', SG), RD110];
    if (l <= 116) return [RD110];
    if (l === 126) return [RD120, L('eBay, 126 mm 10-pack', 'https://www.ebay.com/itm/384954048599', false, 'ships from overseas')];
    if (l <= 130) return [RD120];
    if (l === 158) return [L('Cytron SG, 158 mm', 'https://sg.cytron.io/ampp-3d-printer-closed-loop-timing-belt-2gt-158mm', SG)];
    return [RD140];
  };

  window.BLUEPRINT_PARTS = {
    note: 'Quantities are for the whole model. SG marks a shop in Singapore. The links came from a web search and were not opened, so check stock and prices before you go.',
    groups: [
      { name: 'Tracks and drive', items: [
        { ref: 'P', part: (P) => `GT2 pulley, ${P.teeth} teeth, 5 mm bore, for 6 mm belt`, qty: '16',
          links: (P) => PULLEY[P.teeth] || [], fit: (P) => `Two per section: 12 at the three joints, 4 at the ends. Pitch Ø${(P.teeth * 2 / Math.PI).toFixed(1)} mm.` },
        { ref: 'B', part: (P) => `GT2 closed belt loop, ${P.loop} mm, 6 mm wide`, qty: '8 (+2 spare)',
          links: (P) => loopLinks(P.loop), fit: (P) => `One per section, 2 lanes per side. Axles ${P.C.toFixed(1)} mm apart.` },
        { ref: 'X', part: '5 mm silver steel rod', qty: '5 axles', links: [
          L('Kuriosity, motor shaft 2–8 mm', 'https://kuriosity.sg/products/motor-shaft-4mm-6mm-8mm', SG),
          L('MISUMI SG, cut-to-length shaft', 'https://sg.misumi-ec.com/vona2/detail/110302490360/', SG)],
          fit: (P) => `Cut each to about ${Math.round(P.W + 10)} mm.` },
        { ref: 'BR', part: 'Ball bearing MR105ZZ, 5 × 10 × 4 mm', qty: '16', links: [
          L('MISUMI SG, MR105ZZ', 'https://sg.misumi-ec.com/vona2/detail/221000531116/?HissuCode=MR105ZZ', SG)],
          fit: 'Four per tray, in the knuckles. Printed bushes also work at this speed.' },
        { ref: 'C', part: 'Shaft collar, 5 mm, set screw', qty: '10', links: [
          L('RS Singapore, steel', 'https://sg.rs-online.com/web/p/shaft-collars/8236935', SG),
          L('Kuriosity, flange 4–8 mm', 'https://kuriosity.sg/products/flange-4mm-5mm-6mm-8mm', SG)],
          fit: 'Two per axle, on the ends.' },
        { ref: 'M', part: 'N20 gear motor with encoder, 6 V, 100–150 rpm', qty: '1', links: [
          L('Kuriosity, N20 with encoder', 'https://kuriosity.sg/products/n20-high-torque-motor-with-encoder', SG, 'pick the 100–150 rpm variant'),
          L('Cytron SG, 6 V 85 rpm (no encoder)', 'https://sg.cytron.io/p-6v-85rpm-dc-micro-metal-gearmotor', SG),
          L('DFRobot, 6 V 105 rpm with encoder', 'https://www.dfrobot.com/product-1434.html', false, 'ships from China')],
          fit: (P) => `Drives the H2 axle through two printed gears, and every belt through the shared axles: ${Math.round(P.speed)} mm/s at ${P.rpm} rpm.` },
      ] },
      { name: 'Grip covering', items: [
        { ref: 'G', part: 'Neoprene rubber sheet, 1 mm, Shore 60A', qty: '1 sheet', links: [
          L('Shopee SG', 'https://shopee.sg/Neoprene-Rubber-Sheet-1mm-thick-Black-Color-hardness-60-shoreA-i.203737814.29403577492', SG, 'seller location not checked')],
          fit: (P) => `Cut 8 strips ${P.bw} mm wide and ${P.loop} mm long, and glue one to the back of each belt.` },
        { ref: 'GL', part: 'Selleys Kwik Grip contact adhesive', qty: '1', links: [
          L('Horme', 'https://www.horme.com.sg/product.aspx?id=3708', SG), L('Selffix', 'https://www.selffix.com/selleys-kwik-grip-15ml/', SG)],
          fit: 'Bonds neoprene to the rubber of the belts.' },
        { ref: 'G2', part: 'Cheaper or quicker grip, instead of G', qty: '–', links: [
          L('Decathlon, 16" bicycle inner tube', 'https://www.decathlon.sg/p/bicycle-inner-tube-16-x-1-5-1-9-inch-schrader-black-decathlon-8602104.html', SG, 'cut rings and stretch them over the belts'),
          L('Daiso, 15 mm non-slip tape', 'https://shop.daisosingapore.com.sg/products/4580707591163', SG, 'gritty; may crack round small pulleys'),
          L('Maker Supplies, eSUN TPU 95A', 'https://makersupplies.sg/products/esun-etpu-95a-1-75mm-1kg-3d-printer-filament', SG, 'print tread strips with ridges')],
          fit: 'Whatever you use must not slide on your stair material tilted to 37°.' },
      ] },
      { name: 'Hinges and seat', items: [
        { ref: 'S1–S3', part: 'MG90S metal-gear micro servo, 180°', qty: '3', links: [
          L('Cytron SG, MG90S', 'https://sg.cytron.io/p-mg90s-metal-gear-micro-servo', SG),
          L('Kuriosity, MG90S / SG92R', 'https://kuriosity.sg/products/servo-motor-sg92r-180-360-sg90-upgrade', SG, 'choose 180°, not 360°')],
          fit: 'The three hinges. About 2.8 kg·cm at 6 V; keep the whole model under about 300 g.' },
        { ref: 'S4–S5', part: 'SG90 micro servo', qty: '2', links: [L('Cytron SG, SG90', 'https://sg.cytron.io/p-sg90-micro-servo', SG)],
          fit: 'Arm lean (S4) and seat tilt (S5).' },
      ] },
      { name: 'Control and power', items: [
        { ref: 'U', part: 'Arduino Nano V3 (CH340)', qty: '1', links: [
          L('Kuriosity, Nano V3', 'https://kuriosity.sg/products/nano-v3-0-oem-ch340-usb-driver', SG),
          L('Cytron SG, Raspberry Pi Pico', 'https://sg.cytron.io/c-3d-accessories/c-featured/p-raspberry-pi-pico', SG, 'instead of the Nano, 3.3 V logic')],
          fit: 'Enough pins for 5 servos, the motor driver, the encoder and the tilt sensor.' },
        { ref: 'D', part: 'TB6612FNG motor driver', qty: '1', links: [
          L('Cytron SG', 'https://sg.cytron.io/p-tb6612fng-dual-channel-1p2a-motor-driver-presoldered-header', SG),
          L('SGBotic (SparkFun)', 'https://www.sgbotic.com/index.php?dispatch=products.view&product_id=2562', SG)],
          fit: 'One channel drives the N20.' },
        { ref: 'IMU', part: 'MPU-6050 tilt sensor (GY-521)', qty: '1', links: [
          L('Cytron SG, GY-521', 'https://sg.cytron.io/p-gy-521-mpu6050-6dof-accelerometer-plus-gyro', SG),
          L('Kuriosity, MPU-6050', 'https://kuriosity.sg/products/6dof-6-axis-accelerometer-gyroscope-sensor-mpu-6050', SG)],
          fit: 'On the seat cradle, to keep the seat level.' },
        { ref: 'BAT', part: '2S LiPo, 7.4 V, 450–900 mAh, and a 2S balance charger', qty: '1 + 1', links: [
          L('Cytron SG, LiPo batteries and chargers', 'https://sg.cytron.io/c-lipo-rechargeable-battery-and-charger', SG),
          L('Cytron SG, 2S USB balance charger', 'https://sg.cytron.io/p-2s-7.4v-lipo-battery-usb-5v-1a-fast-balance-charger', SG),
          L('Kuriosity, 2 × 18650 holder with switch', 'https://kuriosity.sg/products/2x-18650-battery-holder-with-switch', SG, 'heavier option, with 18650 cells')],
          fit: 'On the seat cradle with the Nano: together they stand in for the person\'s weight.' },
        { ref: 'V', part: 'Step-down converter to 5–6 V, 3 A or more', qty: '1', links: [
          L('Kuriosity, 5 V 3 A buck', 'https://kuriosity.sg/products/dc-dc-step-down-buck-converter-3-3v-5v-12v-3a', SG),
          L('Cytron SG, XL4005 5 A adjustable', 'https://sg.cytron.io/p-xl4005-smps-adjustable-5a-buck-converter', SG, 'set to 5.5–6 V')],
          fit: 'Powers the five servos and the motor driver.' },
      ] },
      { name: 'Hardware and printing', items: [
        { ref: 'H', part: 'M2 and M3 screw kits, brass heat-set inserts', qty: '1 each', links: [
          L('Kuriosity, M2/M2.5 kit', 'https://kuriosity.sg/products/screw-m2-m2-5-kit', SG),
          L('Kuriosity, M3/M4/M5 kit', 'https://kuriosity.sg/products/screw-nut-m3-m4-m5-kit', SG),
          L('Kuriosity, heat-set inserts', 'https://kuriosity.sg/products/brass-inserts-m2-m3-m4-m5-185pcs', SG)],
          fit: 'Servos, trays, arm and cradle.' },
        { ref: 'PR', part: 'Printed parts: trays T1–T4, arm, cradle, chair, two gears, three levers', qty: '1 set', links: [
          L('3D Print Singapore', 'https://3dprintsingapore.com/', SG, 'PLA, PETG and TPU'),
          L('ZELTA3D', 'https://www.zelta3d.com/', SG)],
          fit: 'PLA or PETG. Or print them yourself.' },
      ] },
      { name: 'Test stairs', items: [
        { ref: 'ST', part: '3 mm MDF or plywood, laser cut', qty: '1 set', links: [
          L('Build & Cut, laser cutting (DXF)', 'https://www.buildandcut.com/products/laser-cutting-service-3-5-9mm-dxf-required', SG),
          L('GPG Printing, laser cutting', 'https://www.gpgprinting.com.sg/laser-cutting-service', SG),
          L('NLB MakeIT at libraries', 'https://www.nlb.gov.sg/main/services/MakeIT-at-Libraries', SG, 'free laser cutter after a starter session'),
          L('Build & Cut, plywood cut to size', 'https://www.buildandcut.com/products/standard-plywood', SG)],
          fit: (P) => `Two stringers with the step profile, and ${P.steps} treads and risers, ${P.rise.toFixed(1)} × ${P.going.toFixed(1)} mm.` },
      ] },
    ],
    steps: [
      ['Choose your belt and pulley.', 'Set them under Your parts. Every size on this page follows from them. 20 teeth with 110 mm loops, both sold in Singapore, gives exactly 1:10.'],
      ['Print the parts.', (P) => `Four section trays T1 to T4 with bearing knuckles ${P.C.toFixed(1)} mm apart, the seat arm, the seat cradle and chair, two drive gears and three hinge levers, in PLA or PETG.`],
      ['Make the tracks.', (P) => `Glue a ${P.bw} mm strip of neoprene to the smooth back of each belt. First check the grip: a strip laid on your stair material must not slide when the board is tilted to 37°. If it slides, add small ridges every 6 to 8 mm.`],
      ['Build the chain.', 'Press the bearings into the tray knuckles, slide the five axles through, then fit the pulleys: lane A on the outside, lane B inside. Tighten the grub screws and fit collars on the axle ends. Each tray must swing freely on its axles.'],
      ['Fit the belts.', 'T1 and T3 run in lane A, T2 and T4 in lane B, on both sides. Neighbouring belts then share an axle, so one axle turns them all.'],
      ['Fit the drive.', 'Mount the N20 on T2 so its gear meshes with the gear on the H2 axle. Turn it by hand: all eight belts should move together.'],
      ['Fit the hinge servos.', 'S1 goes on T1 for hinge H1, S2 on T3 for H2, S3 on T4 for H3. Centre each servo with the chain straight, then join its link to the lever on the next tray. Check that each hinge swings ±55° without binding.'],
      ['Build the seat.', 'Mount S4 on a bracket on T2, above the motor, and fix the arm to its horn. S5 at the top of the arm tilts the seat cradle. Put the chair, the Nano, the motor driver, the tilt sensor and the battery on the cradle.'],
      ['Wire it.', 'Follow sheet D. Test each servo and the drive motor on their own, at low speed.'],
      ['Program it.', 'Drive slowly and zero the encoder at the start mark. For each distance, set the servos from the hinge program above, and trim the seat level with the tilt sensor.'],
      ['Build the test stairs and try it.', 'Build them to sheet E. Run it up and down with a hand ready to catch it.'],
    ],
    guides: [
      { title: 'Making robot tank treads from timing belts', url: 'https://www.instructables.com/Making-Timing-Belts-Robot-Tank-Treads-Using-Scarf-/', note: 'Instructables' },
      { title: 'Printed TPU tank tracks', url: 'https://www.printables.com/model/253130-tpu-tank-tracks', note: 'Printables, a model to adapt' },
      { title: 'Arduino PackBot-style robot with flippers', url: 'https://www.instructables.com/PACKBOT-ROBOT-ARDUINO-BASED/', note: 'Instructables, climbs a few steps' },
      { title: 'Stair climbing of a tracked robot with flipper arms', url: 'https://www.researchgate.net/publication/272000912_Stair_Climbing_of_a_Track-Driven_Mobile_Robot_with_Flipper_Arm', note: 'research paper' },
      { title: 'TB6612FNG hookup guide', url: 'https://learn.sparkfun.com/tutorials/tb6612fng-hookup-guide/all', note: 'SparkFun' },
      { title: 'N20 encoder motor with Arduino', url: 'https://electricdiylab.com/controlling-n20-encoder-micro-gear-motor-with-arduino/', note: 'reading distance' },
      { title: 'Servo motors with Arduino', url: 'https://docs.arduino.cc/learn/electronics/servo-motors', note: 'Arduino docs' },
      { title: 'MPU-6050 with Arduino', url: 'https://howtomechatronics.com/tutorials/arduino/arduino-and-mpu6050-accelerometer-and-gyroscope-tutorial/', note: 'HowToMechatronics' },
      { title: 'Getting started with the GY-521', url: 'https://sg.cytron.io/tutorial/getting-started-gy-521-mpu6050-arduino-maker-uno', note: 'Cytron SG' },
    ],
    guidesNote: 'None of these builds this exact vehicle; together they cover the tracks, the flippers, the motor, the servos and the tilt sensor.',
  };
})();
