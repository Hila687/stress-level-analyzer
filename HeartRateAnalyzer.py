import numpy as np
from typing import List

class HeartRateAnalyzer:

    def __init__(self, fs=30):
        self.fs = fs  # Sampling frequency (frames per second)

    def compute_bpm(self, signal: List[float], min_hr=40, max_hr=240) -> float:
        """
        Computes BPM from a filtered rPPG signal using FFT.
        Returns the dominant frequency in beats per minute.
        """

        # Remove mean to center the signal (DC removal)
        signal = signal - np.mean(signal)

        # Compute FFT and corresponding frequency bins
        n = len(signal)
        fft_result = np.fft.rfft(signal)  # real-valued FFT (positive frequencies only)
        freqs = np.fft.rfftfreq(n, d=1.0 / self.fs)  # frequency bins in Hz

        # Convert frequency range of interest to Hz
        min_hz = min_hr / 60
        max_hz = max_hr / 60

        # Focus only on relevant frequencies (typically 0.7–4Hz)
        valid_range = (freqs >= min_hz) & (freqs <= max_hz)
        valid_freqs = freqs[valid_range]
        valid_amplitudes = np.abs(fft_result)[valid_range]

        # Find the frequency with the highest amplitude (dominant frequency)
        peak_freq = valid_freqs[np.argmax(valid_amplitudes)]

        # Convert to BPM
        bpm = peak_freq * 60.0
        return bpm