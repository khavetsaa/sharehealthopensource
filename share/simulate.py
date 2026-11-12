"""Synthetic labour data for testing and demos. No real patient data is used."""
from __future__ import annotations

import numpy as np

FS_HZ = 20.0
WINDOW_S = 120


def ehg_window(dominant_hz: float, seconds: int = WINDOW_S, fs: float = FS_HZ, seed: int = 0) -> np.ndarray:
    """One window of synthetic EHG: a contraction burst at dominant_hz plus noise."""
    rng = np.random.default_rng(seed)
    t = np.arange(int(seconds * fs)) / fs
    envelope = np.exp(-((t - seconds / 2) ** 2) / (2 * (seconds / 6) ** 2))
    burst = envelope * np.sin(2 * np.pi * dominant_hz * t)
    return burst + 0.05 * rng.standard_normal(t.size)


def labour(hours: int = 12, fatigue: bool = True, seed: int = 1) -> list[np.ndarray]:
    """Hourly EHG windows. With fatigue, the dominant frequency drifts lower."""
    start, end = 0.70, (0.45 if fatigue else 0.68)
    freqs = np.linspace(start, end, hours)
    return [ehg_window(f, seed=seed + i) for i, f in enumerate(freqs)]
