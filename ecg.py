
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, iirnotch

def ecg_filter(ecg_signal, fs):
      # Remove baseline wander using a 0.5 Hz high-pass filter
      high_cutoff = 0.5
      b_high, a_high = butter(4, high_cutoff / (fs / 2), btype="highpass")
      ecg_highpassed = filtfilt(b_high, a_high, ecg_signal)

      # Remove high-frequency noise using a 40 Hz low-pass filter
      low_cutoff = 40
      b_low, a_low = butter(4, low_cutoff / (fs / 2), btype="lowpass")
      ecg_bandpassed = filtfilt(b_low, a_low, ecg_highpassed)

      # Remove 50 Hz powerline interference using a notch filter
      notch_freq = 50
      quality_factor = 30
      b_notch, a_notch = iirnotch(notch_freq / (fs / 2), quality_factor)
      ecg_cleaned = filtfilt(b_notch, a_notch, ecg_bandpassed)

      return ecg_cleaned

  # Example sampling frequency
fs = 250

  # Example time axis: 5 seconds of data
t = np.arange(0, 5, 1 / fs)

  # Example noisy ECG-like signal for testing
ecg_raw = (
    1.0 * np.sin(2 * np.pi * 1.2 * t)
    + 0.3 * np.sin(2 * np.pi * 50 * t)
    + 0.2 * np.sin(2 * np.pi * 0.2 * t)
    + 0.1 * np.random.randn(len(t))
)

  # Apply ECG filter
ecg_clean = ecg_filter(ecg_raw, fs)

  # Plot raw and filtered ECG
plt.figure(figsize=(10, 5))

plt.subplot(2, 1, 1)
plt.plot(t, ecg_raw)
plt.title("Raw ECG Signal")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")

plt.subplot(2, 1, 2)
plt.plot(t, ecg_clean)
plt.title("Filtered ECG Signal")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()


