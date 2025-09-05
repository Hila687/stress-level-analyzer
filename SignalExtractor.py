from typing import List
import numpy as np
import cv2 as cv
from scipy.signal import butter, filtfilt

class SignalExtractor: 

    # Constructor to initialize the sampling rate (frames per second)
    def __init__(self, fs=30):
        self.fs = fs

    # Extract the green channel from each frame and calculate the mean brightness
    def extract_raw_signal(self, frames: List[np.ndarray]) -> List[float]:
        raw_signal = []
        for frame in frames:
            green = frame[:, :, 1]  # Index 1 corresponds to the green channel in BGR format
            mean_val = np.mean(green)  # Average brightness of green pixels
            raw_signal.append(mean_val)
        return raw_signal  

    # Apply a bandpass Butterworth filter to remove noise and keep only pulse-relevant frequencies
    def bandpass_filter(self, signal: List[float], lowcut=0.7, highcut=4.0, order=4) -> List[float]:
        nyquist = 0.5 * self.fs  # Nyquist frequency is half the sampling rate
        low = lowcut / nyquist  # Normalize low cutoff frequency
        high = highcut / nyquist  # Normalize high cutoff frequency
        b, a = butter(order, [low, high], btype='band')  # Design bandpass filter
        filtered = filtfilt(b, a, signal)  # Apply filter forward and backward (no phase shift)
        return filtered  # Returns the filtered signal (cleaned rPPG)

    # Full pipeline: extract the raw signal and apply filtering
    def extract_rppg(self, frames: List[np.ndarray]) -> List[float]:
        raw = self.extract_raw_signal(frames)  
        filtered = self.bandpass_filter(raw)   
        return filtered  
