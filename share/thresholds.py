"""When should the E-MOTIVE bundle start?

WHO 2025 rule (applies to every woman):
    measured blood loss >= 300 ml AND any abnormal sign, OR blood loss >= 500 ml.

SHARE's personal trigger (decision support):
    a blood-loss line for this woman, computed from her estimated blood volume,
    haemoglobin and labour risk. The safety rule built into this module is that
    the personal trigger can only bring E-MOTIVE EARLIER than WHO, never later:
    it is capped at 300 ml and the WHO rule always applies as well.

IMPORTANT: the scaling constants below are illustrative placeholders. They are
not clinically validated and must be replaced by values learned and locked on
Kenyan study data before any clinical use.
"""
from __future__ import annotations

from dataclasses import dataclass

from .vitals import Vitals, abnormal_signs

WHO_TRIGGER_WITH_SIGN_ML = 300
WHO_TRIGGER_ALONE_ML = 500

# Illustrative placeholders (see module docstring).
BLOOD_VOLUME_ML_PER_KG = 100  # approximate blood volume at term
BASE_TOLERANCE_FRACTION = 0.045
ANAEMIA_CUTOFF_G_DL = 11.0
HIGH_RISK_FACTOR = 0.85
MIN_TRIGGER_ML = 150
ROUND_TO_ML = 50


@dataclass(frozen=True)
class Mother:
    weight_kg: float
    haemoglobin_g_dl: float

    def __post_init__(self) -> None:
        if not 30 <= self.weight_kg <= 200:
            raise ValueError("Weight must be between 30 and 200 kg")
        if not 3 <= self.haemoglobin_g_dl <= 20:
            raise ValueError("Haemoglobin must be between 3 and 20 g/dL")


def personal_trigger_ml(mother: Mother, high_risk: bool = False) -> int:
    """Blood loss (ml) at which SHARE suggests starting E-MOTIVE for this woman.

    Never above the WHO 300 ml line, never below MIN_TRIGGER_ML.
    """
    fraction = BASE_TOLERANCE_FRACTION
    if mother.haemoglobin_g_dl < ANAEMIA_CUTOFF_G_DL:
        fraction *= mother.haemoglobin_g_dl / ANAEMIA_CUTOFF_G_DL
    if high_risk:
        fraction *= HIGH_RISK_FACTOR
    raw = mother.weight_kg * BLOOD_VOLUME_ML_PER_KG * fraction
    rounded = int(ROUND_TO_ML * round(raw / ROUND_TO_ML))
    return max(MIN_TRIGGER_ML, min(WHO_TRIGGER_WITH_SIGN_ML, rounded))


def who_rule_met(blood_loss_ml: float, vitals: Vitals) -> bool:
    if blood_loss_ml >= WHO_TRIGGER_ALONE_ML:
        return True
    return blood_loss_ml >= WHO_TRIGGER_WITH_SIGN_ML and bool(abnormal_signs(vitals))


def should_start_emotive(
    blood_loss_ml: float, vitals: Vitals, personal_ml: int
) -> tuple[bool, str]:
    """Decide whether to prompt staff to start E-MOTIVE.

    Returns (start, reason). Staff always make the final decision.
    """
    if blood_loss_ml < 0:
        raise ValueError("Blood loss cannot be negative")
    if who_rule_met(blood_loss_ml, vitals):
        return True, "WHO criteria met"
    if blood_loss_ml >= min(personal_ml, WHO_TRIGGER_WITH_SIGN_ML):
        return True, f"Personal trigger reached ({personal_ml} ml)"
    return False, "Below triggers: keep measuring with the calibrated drape"
