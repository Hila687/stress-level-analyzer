# --- Add project root to Python path ---
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# import statements
import numpy as np
import pytest
from HeartRateAnalyzer import HeartRateAnalyzer  # adjust import path if needed


def test_compute_bpm_on_sine_wave():
    """
    Test that compute_bpm correctly detects BPM from a synthetic sine wave signal.
    """

    fs = 30  # Sampling frequency (frames per second)
    duration = 10  # seconds
    true_bpm = 90
    true_freq = true_bpm / 60.0  # Hz

    # Create a time array and generate a clean sine wave at the target frequency
    t = np.arange(0, duration, 1 / fs)
    clean_signal = np.sin(2 * np.pi * true_freq * t)

    # Add small random noise to simulate real-world signal variation
    # noisy_signal = clean_signal + 0.05 * np.random.randn(len(t))

    # Add realistic noise components
    illumination_drift = 0.3 * np.sin(2 * np.pi * 0.1 * t)
    motion_noise = np.zeros_like(t)
    indices = np.random.choice(len(t), size=int(0.05 * len(t)), replace=False)
    motion_noise[indices] = np.random.uniform(-1, 1, size=len(indices))

    noisy_signal = clean_signal + illumination_drift + motion_noise + 0.1 * np.random.randn(len(t))


    analyzer = HeartRateAnalyzer(fs=fs)
    estimated_bpm = analyzer.compute_bpm(noisy_signal)

    # The estimated BPM should be reasonably close to the true BPM (±5 BPM tolerance)
    assert abs(estimated_bpm - true_bpm) < 5, f"Expected around {true_bpm}, got {estimated_bpm}"
    print(f"True BPM: {true_bpm}, Estimated BPM: {estimated_bpm}")


def test_compute_bpm_on_constant_signal():
    """
    Test that compute_bpm returns a low or valid BPM for a constant (flat) signal.
    """

    fs = 30
    constant_signal = np.ones(300)  # Flat signal (10 seconds at 30 fps)
    analyzer = HeartRateAnalyzer(fs=fs)
    bpm = analyzer.compute_bpm(constant_signal)

    # Since there is no frequency component, BPM should fall within the valid range but not extreme
    assert 40 <= bpm <= 240, f"BPM {bpm} is outside expected range for a flat signal"
