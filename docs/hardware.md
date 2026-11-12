# Hardware concept

Prototype in design with our engineering partner Medevice (target: January 2027). Design files will be published here under CERN-OHL-P-2.0.

## Modular kit
- **Hub:** battery, microcontroller, alarm, pump; all computation offline.
- **Five snap-in sensors** on a soft abdominal band. None optical.

| Sensor | Position | Reads | Used for |
| --- | --- | --- | --- |
| 1 Fundal | Top of uterus | Electrical activity + firmness (tone) | Contraction strength; tone checks after birth; feedback for compression |
| 2 Upper left | Upper uterus | Electrical activity | Fatigue (median frequency shift) |
| 3 Upper right | Upper uterus | Electrical activity | Fatigue; how contractions spread |
| 4 Lower left | Lower uterus | Electrical activity | Upper vs lower comparison; maternal heart rate |
| 5 Lower right | Lower uterus | Electrical activity + reference | Clean signal reference |

- **Vital signs:** blood pressure via cuff or link to the ward monitor (for shock index and mean arterial pressure); temperature.
- **Compression pad:** inflates in cycles inside a single-use sleeve; pressure capped.
- **Display:** screen with green, amber and red alerts and the personal E-MOTIVE trigger.

## Open questions for the prototype
- Fetal heart rate from the same abdominal electrodes (feasibility, Phase 2)
- Signal quality across body types
- Cleaning validation and fluid-ingress testing
