"""Run a simulated labour through the SHARE engine: python -m share.cli"""
from __future__ import annotations

from .ehg import fatigue_index, median_frequency
from .risk import LabourState, assess
from .simulate import FS_HZ, labour
from .thresholds import Mother, personal_trigger_ml, should_start_emotive
from .vitals import Vitals, mean_arterial_pressure, shock_index


def main() -> None:
    mother = Mother(weight_kg=58, haemoglobin_g_dl=9.2)
    print("SHARE Health simulation (synthetic data, not for clinical use)")
    print(f"Mother: {mother.weight_kg} kg, haemoglobin {mother.haemoglobin_g_dl} g/dL\n")
    mfs: list[float] = []
    result = None
    for hour, window in enumerate(labour(hours=12, fatigue=True), start=1):
        mfs.append(median_frequency(window, FS_HZ))
        state = LabourState(
            fatigue_index=fatigue_index(mfs),
            oxytocin_hours=max(0, hour - 4),
            haemoglobin_g_dl=mother.haemoglobin_g_dl,
            labour_hours=hour,
        )
        result = assess(state)
        print(f"Hour {hour:2d}  median freq {mfs[-1]:.2f} Hz  risk {result.score:.2f} {result.level.upper():5s}  {', '.join(result.reasons)}")

    high_risk = result is not None and result.level in ("amber", "red")
    trigger = personal_trigger_ml(mother, high_risk=high_risk)
    print(f"\nPersonal E-MOTIVE trigger: {trigger} ml (WHO: 300 ml + abnormal sign, or 500 ml)\n")

    vitals = Vitals(heart_rate=96, systolic=104, diastolic=66)
    print(f"Vitals: shock index {shock_index(vitals)}, MAP {mean_arterial_pressure(vitals)} mmHg")
    for loss in (100, 150, 200, 250, 300):
        start, reason = should_start_emotive(loss, vitals, trigger)
        print(f"Drape reading {loss:3d} ml -> {'START E-MOTIVE' if start else 'monitor':14s} {reason}")


if __name__ == "__main__":
    main()
