import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import wfdb

# -----------------------------
# 1. Load ECG from PhysioNet
# -----------------------------
record = wfdb.rdrecord('100', pn_dir='mitdb', sampto=3000)
ecg = record.p_signal[:, 0]
fs = record.fs

t = np.arange(len(ecg)) / fs

# -----------------------------
# 2. Add Noise (Powerline + White)
# -----------------------------
noise_powerline = 0.5 * np.sin(2 * np.pi * 50 * t)
noise_white = 0.2 * np.random.randn(len(ecg))
noisy_ecg = ecg + noise_powerline + noise_white

# -----------------------------
# 3. FIR Notch Filter (Hamming)
# -----------------------------
notch_freq = 50
bw = 2
numtaps = 101

fir_coeff = signal.firwin(
    numtaps,
    [notch_freq - bw, notch_freq + bw],
    fs=fs,
    pass_zero=True,
    window='hamming'
)

ecg_fir = signal.lfilter(fir_coeff, 1.0, noisy_ecg)

# -----------------------------
# 4. IIR Butterworth Filter
# -----------------------------
lowcut = 0.5
highcut = 40

b, a = signal.butter(4, [lowcut, highcut], btype='band', fs=fs)
ecg_iir = signal.filtfilt(b, a, noisy_ecg)

# -----------------------------
# 5. DFT Function
# -----------------------------
def compute_fft(sig):
    fft_vals = np.fft.fft(sig)
    fft_vals = np.abs(fft_vals)[:len(sig)//2]
    freqs = np.fft.fftfreq(len(sig), 1/fs)[:len(sig)//2]
    return freqs, fft_vals

f1, X_noisy = compute_fft(noisy_ecg)
f2, X_fir = compute_fft(ecg_fir)
f3, X_iir = compute_fft(ecg_iir)

# -----------------------------
# 6. SNR Calculation
# -----------------------------
def snr(clean, noisy):
    noise = noisy - clean
    return 10 * np.log10(np.sum(clean**2) / np.sum(noise**2))

snr_fir = snr(ecg, ecg_fir)
snr_iir = snr(ecg, ecg_iir)

print("SNR FIR:", snr_fir)
print("SNR IIR:", snr_iir)

# -----------------------------
# 7. Group Delay
# -----------------------------
w_fir, gd_fir = signal.group_delay((fir_coeff, 1))
w_iir, gd_iir = signal.group_delay((b, a))

# -----------------------------
# 8. Plot Time Domain
# -----------------------------
plt.figure(figsize=(12, 8))

plt.subplot(3,1,1)
plt.plot(t, noisy_ecg)
plt.title("Noisy ECG")

plt.subplot(3,1,2)
plt.plot(t, ecg_fir)
plt.title("FIR Filtered ECG")

plt.subplot(3,1,3)
plt.plot(t, ecg_iir)
plt.title("IIR Filtered ECG")

plt.tight_layout()
plt.show()

# -----------------------------
# 9. Plot Frequency Domain
# -----------------------------
plt.figure(figsize=(12, 8))

plt.subplot(3,1,1)
plt.plot(f1, X_noisy)
plt.title("Noisy Spectrum")

plt.subplot(3,1,2)
plt.plot(f2, X_fir)
plt.title("FIR Spectrum")

plt.subplot(3,1,3)
plt.plot(f3, X_iir)
plt.title("IIR Spectrum")

plt.tight_layout()
plt.show()

# -----------------------------
# 10. Group Delay Plot
# -----------------------------
plt.figure()
plt.plot(w_fir, gd_fir, label='FIR')
plt.plot(w_iir, gd_iir, label='IIR')
plt.legend()
plt.title("Group Delay Comparison")
plt.show()