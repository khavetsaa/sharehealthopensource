"""Explainable PPH risk score shown to midwives as green, amber or red.

This is a transparent logistic score so every alert can be explained. The
weights below are illustrative placeholders chosen from published risk factors.
They will be replaced by a model trained, validated and then locked on data
from SHARE's silent study in Kenyan hospitals. Not for clinical use.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

INTERCEPT = -3.0
WEIGHTS = {
    "fatigue_index": 9.0,  # per unit drop in EHG median frequency
    "oxytocin_hours": 0.15,  # long oxytocin augmentation
    "anaemia": 0.8,  # haemoglobin below 11 g/dL
    "previous_pph": 1.2,
    "labour_hours_over_12": 0.6,
}
AMBER_AT = 0.30
RED_AT = 0.60


@dataclass(frozen=True)
class LabourState:
    fatigue_index: float
    oxytocin_hours: float = 0.0
    haemoglobin_g_dl: float = 12.0
    previous_pph: bool = False
    labour_hours: float = 0.0


@dataclass(frozen=True)
class RiskResult:
    score: float
    level: str  # "green", "amber" or "red"
    reasons: list[str] = field(default_factory=list)


def assess(state: LabourState) -> RiskResult:
    features = {
        "fatigue_index": state.fatigue_index,
        "oxytocin_hours": state.oxytocin_hours,
        "anaemia": 1.0 if state.haemoglobin_g_dl < 11 else 0.0,
        "previous_pph": 1.0 if state.previous_pph else 0.0,
        "labour_hours_over_12": 1.0 if state.labour_hours > 12 else 0.0,
    }
    contributions = {k: WEIGHTS[k] * v for k, v in features.items()}
    z = INTERCEPT + sum(contributions.values())
    score = round(1 / (1 + math.exp(-z)), 3)
    level = "red" if score >= RED_AT else "amber" if score >= AMBER_AT else "green"
    labels = {
        "fatigue_index": f"uterine signal slowed {state.fatigue_index:.0%}",
        "oxytocin_hours": f"oxytocin for {state.oxytocin_hours:.1f} h",
        "anaemia": f"haemoglobin {state.haemoglobin_g_dl:.1f} g/dL",
        "previous_pph": "previous PPH",
        "labour_hours_over_12": f"labour {state.labour_hours:.0f} h",
    }
    reasons = [labels[k] for k, c in sorted(contributions.items(), key=lambda kv: -kv[1]) if c > 0.3]
    return RiskResult(score=score, level=level, reasons=reasons)
