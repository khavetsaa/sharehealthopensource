"""Uterine fatigue from abdominal electrohysterography (EHG).

SHARE's abdominal sensors record the uterus's electrical activity. Research on
uterine electromyography suggests that as the uterine muscle tires, the median
frequency of its electrical bursts shifts lower. This module measures that shift.
"""
from __future__ import annotations

import numpy as np

EHG_BAND_HZ = (0.2, 4.0)


def median_frequency(signal: np.ndarray, fs: float, band: tuple[float, float] = EHG_BAND_HZ) -> float:
    """Median frequency (Hz) of the power spectrum inside the EHG band."""
    x = np.asarray(signal, dtype=float)
    if x.ndim != 1 or x.size < 8:
        raise ValueError("Signal must be a 1-D array with at least 8 samples")
    if fs <= 0:
        raise ValueError("Sampling rate must be positive")
    x = x - x.mean()
    window = np.hanning(x.size)
    power = np.abs(np.fft.rfft(x * window)) ** 2
    freqs = np.fft.rfftfreq(x.size, d=1.0 / fs)
    mask = (freqs >= band[0]) & (freqs <= band[1])
    if not mask.any() or power[mask].sum() == 0:
        raise ValueError("No signal power inside the EHG band")
    p, f = power[mask], freqs[mask]
    cumulative = np.cumsum(p)
    return float(f[np.searchsorted(cumulative, cumulative[-1] / 2)])


def fatigue_index(median_freqs: list[float], baseline_windows: int = 3) -> float:
    """Relative drop in median frequency against the start of labour.

    0.0 = no change; 0.2 = median frequency 20% below baseline.
    """
    if len(median_freqs) <= baseline_windows:
        return 0.0
    baseline = float(np.mean(median_freqs[:baseline_windows]))
    recent = float(np.mean(median_freqs[-baseline_windows:]))
    if baseline <= 0:
        raise ValueError("Baseline median frequency must be positive")
    return round(max(0.0, (baseline - recent) / baseline), 3)
