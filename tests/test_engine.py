import numpy as np
import pytest

from share.compression import MAX_PRESSURE_MMHG, CompressionController
from share.ehg import fatigue_index, median_frequency
from share.risk import LabourState, assess
from share.simulate import FS_HZ, ehg_window, labour
from share.thresholds import Mother, personal_trigger_ml, should_start_emotive, who_rule_met
from share.vitals import Vitals, abnormal_signs, mean_arterial_pressure, shock_index

NORMAL = Vitals(heart_rate=80, systolic=120, diastolic=80)
SHOCKED = Vitals(heart_rate=120, systolic=95, diastolic=55)


# Vitals
def test_shock_index_and_map():
    assert shock_index(NORMAL) == 0.67
    assert mean_arterial_pressure(NORMAL) == 93.3


def test_abnormal_signs_follow_who_2025():
    assert abnormal_signs(NORMAL) == []
    assert len(abnormal_signs(SHOCKED)) == 4


def test_invalid_vitals_rejected():
    with pytest.raises(ValueError):
        Vitals(heart_rate=80, systolic=70, diastolic=90)


# Thresholds: the personal trigger is never later than WHO
def test_who_rule():
    assert not who_rule_met(299, SHOCKED)
    assert who_rule_met(300, SHOCKED)
    assert not who_rule_met(450, NORMAL)
    assert who_rule_met(500, NORMAL)


@pytest.mark.parametrize("weight", [40, 58, 70, 120])
@pytest.mark.parametrize("hb", [6.0, 9.0, 11.0, 14.0])
@pytest.mark.parametrize("high_risk", [False, True])
def test_personal_trigger_never_above_who(weight, hb, high_risk):
    trigger = personal_trigger_ml(Mother(weight, hb), high_risk)
    assert 150 <= trigger <= 300


def test_anaemic_mother_gets_earlier_trigger():
    assert personal_trigger_ml(Mother(58, 9.2), high_risk=True) < personal_trigger_ml(Mother(58, 12.5))


def test_who_rule_always_wins():
    start, reason = should_start_emotive(500, NORMAL, personal_ml=300)
    assert start and reason == "WHO criteria met"


def test_personal_trigger_starts_emotive_early():
    start, reason = should_start_emotive(200, NORMAL, personal_ml=200)
    assert start and "Personal trigger" in reason
    assert not should_start_emotive(150, NORMAL, personal_ml=200)[0]


# EHG fatigue
def test_median_frequency_recovers_dominant_frequency():
    mf = median_frequency(ehg_window(0.6), FS_HZ)
    assert abs(mf - 0.6) < 0.1


def test_fatigue_detected_only_when_signal_slows():
    tired = [median_frequency(w, FS_HZ) for w in labour(fatigue=True)]
    steady = [median_frequency(w, FS_HZ) for w in labour(fatigue=False)]
    assert fatigue_index(tired) > 0.15
    assert fatigue_index(steady) < 0.05


def test_median_frequency_rejects_bad_input():
    with pytest.raises(ValueError):
        median_frequency(np.zeros(4), FS_HZ)


# Risk score
def test_risk_levels():
    assert assess(LabourState(fatigue_index=0.0)).level == "green"
    high = assess(LabourState(fatigue_index=0.3, oxytocin_hours=8, haemoglobin_g_dl=9.0))
    assert high.level == "red"
    assert high.reasons and "uterine signal" in high.reasons[0]


# Compression safety interlocks
def test_compression_needs_staff_confirmation_and_soft_uterus():
    c = CompressionController()
    assert c.start(uterus_soft=True).startswith("Blocked")
    c.confirm_pph()
    assert c.start(uterus_soft=False).startswith("Blocked")
    assert c.start(uterus_soft=True) == "Compression cycles started"


def test_pressure_capped_and_deflates_on_fault():
    c = CompressionController()
    c.confirm_pph()
    c.start(uterus_soft=True)
    assert c.set_pressure(500) == MAX_PRESSURE_MMHG
    c.on_fault("power loss")
    assert c.pressure_mmhg == 0 and not c.running
    assert c.set_pressure(40) == 0
