"""Vital-sign calculations used by SHARE.

All functions are pure and unit-tested. Thresholds follow the WHO 2025
postpartum haemorrhage (PPH) guideline's list of abnormal signs.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Vitals:
    """One set of maternal observations."""

    heart_rate: float  # beats per minute
    systolic: float  # mmHg
    diastolic: float  # mmHg
    temperature: float | None = None  # degrees Celsius

    def __post_init__(self) -> None:
        if self.heart_rate <= 0 or self.systolic <= 0 or self.diastolic <= 0:
            raise ValueError("Heart rate and blood pressure must be positive")
        if self.diastolic >= self.systolic:
            raise ValueError("Diastolic pressure must be below systolic pressure")


def shock_index(v: Vitals) -> float:
    """Shock index = heart rate / systolic blood pressure."""
    return round(v.heart_rate / v.systolic, 2)


def mean_arterial_pressure(v: Vitals) -> float:
    """Mean arterial pressure (MAP) = (systolic + 2 x diastolic) / 3, in mmHg."""
    return round((v.systolic + 2 * v.diastolic) / 3, 1)


def abnormal_signs(v: Vitals) -> list[str]:
    """Return the WHO 2025 abnormal signs present in this set of vitals.

    WHO lists: pulse above 100, systolic below 100, diastolic below 60,
    or shock index above 1.
    """
    signs: list[str] = []
    if v.heart_rate > 100:
        signs.append(f"heart rate {v.heart_rate:.0f} > 100")
    if v.systolic < 100:
        signs.append(f"systolic {v.systolic:.0f} < 100")
    if v.diastolic < 60:
        signs.append(f"diastolic {v.diastolic:.0f} < 60")
    si = shock_index(v)
    if si > 1:
        signs.append(f"shock index {si:.2f} > 1")
    return signs
