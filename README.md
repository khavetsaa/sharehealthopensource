# SHARE Health

**Open-source early warning and response for postpartum haemorrhage (PPH) in low-resource maternity wards.**

In Kenya, about 5,000 women die each year from pregnancy complications, and severe bleeding after birth (PPH) causes 37% of those deaths. Bleeding is often caught late because midwives in understaffed wards check mothers by hand and only periodically.

SHARE is a wearable belt plus this software engine. It supports two steps of **E-MOTIVE**, the WHO-recommended PPH care bundle:

1. **Early detection, before birth.** Five non-optical abdominal sensors record the uterus's electrical activity (electrohysterography, EHG) during labour. As the muscle tires, the median frequency of its signal drops. SHARE combines this fatigue signal with the mother's haemoglobin, oxytocin exposure and vital signs to show a **green, amber or red** risk level and a **personal blood-loss trigger** for starting E-MOTIVE.
2. **Uterine massage, during PPH.** When staff confirm PPH and the uterus is soft, the same belt inflates a pad in cycles to massage the uterus, freeing the midwife's hands.

> **Status: research prototype.** This repository runs on synthetic data only. It is not a medical device, has not been clinically validated, and must not be used to make clinical decisions.

## What works today

| Module | What it does | File |
| --- | --- | --- |
| Vital signs | Shock index, mean arterial pressure, WHO 2025 abnormal signs | `share/vitals.py` |
| Thresholds | WHO 2025 E-MOTIVE rule and a personal trigger that is **never later than WHO** | `share/thresholds.py` |
| Uterine fatigue | Median frequency of EHG bursts and a fatigue index | `share/ehg.py` |
| Risk score | Explainable green/amber/red score with the reasons behind each alert | `share/risk.py` |
| Compression safety | Interlocks: staff start only, soft uterus only, pressure cap, deflate on fault | `share/compression.py` |
| Simulator | Synthetic labour EHG for tests and demos | `share/simulate.py` |
| Demo dashboard | Browser demo of the midwife screen | `demo/index.html` |

## Quick start

```bash
pip install numpy pytest
pytest -q                # 45 tests
python -m share.cli      # run a simulated labour
```

Example output (synthetic):

```
Hour 10  median freq 0.49 Hz  risk 0.70 RED  uterine signal slowed 24%, oxytocin for 6.0 h, haemoglobin 9.2 g/dL
Personal E-MOTIVE trigger: 200 ml (WHO: 300 ml + abnormal sign, or 500 ml)
Drape reading 200 ml -> START E-MOTIVE Personal trigger reached (200 ml)
```

Open `demo/index.html` in any browser to see the midwife dashboard.

## Design principles

- **Decision support, not diagnosis.** SHARE flags risk and prompts preparation. Clinicians diagnose PPH, measure blood loss with the E-MOTIVE calibrated drape, and start and stop every action.
- **Earlier, never later.** The personal trigger is capped at the WHO threshold, and the WHO rule always applies.
- **Fair across skin tones.** No optical sensors: they read less accurately on darker skin.
- **Explainable.** Every alert lists the factors behind it.
- **Offline first.** All computation runs on the device; wards often lack reliable internet.
- **Privacy by design.** Consent, anonymisation and data kept in Kenya. See [docs/safety-and-privacy.md](docs/safety-and-privacy.md).

## Repository map

```
share/        Python engine (risk, thresholds, EHG, vitals, compression interlocks, simulator)
tests/        Automated tests (pytest)
demo/         Browser demo of the midwife dashboard
docs/         Intended use, safety and privacy, hardware, roadmap, model card
```

## Roadmap

See [docs/roadmap.md](docs/roadmap.md). Next: belt prototype with our engineering partner Medevice (January 2027), a silent data study in Kenyan hospitals, and a risk model trained and locked on Kenyan data.

## Licences

- Software: [Apache 2.0](LICENSE)
- Hardware design files (when published): CERN Open Hardware Licence v2, Permissive
- Documentation: Creative Commons Attribution 4.0

## Contributing

Clinicians, engineers and data scientists are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Team

SHARE Health, Kenya. Founder and CEO: Yvone Khavetsa.
