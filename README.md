# Filtering of Noise-Corrupted ECG Signals Using Digital Filters

## Overview

This project demonstrates the use of digital signal processing techniques to reduce noise from ECG signals.

A real ECG signal from the MIT-BIH Arrhythmia Database is corrupted with 50 Hz powerline interference and white Gaussian noise. The noisy signal is then processed using FIR and IIR digital filters and analyzed in both time and frequency domains.

## Objectives

* Process a real ECG signal using Python
* Introduce controlled noise into the ECG
* Design and apply FIR and IIR digital filters
* Analyze the signal using FFT
* Compare filtering performance using SNR and group delay

## Methodology

```text
MIT-BIH ECG
     ↓
Add Noise
     ↓
Noisy ECG
     ↓
 ┌───────────────┐
 │               │
FIR Filter    IIR Filter
 │               │
 └───────┬───────┘
         ↓
Time & Frequency Domain Analysis
         ↓
SNR & Group Delay Comparison
```

## Filters Used

### FIR Filter

* 101-tap FIR notch filter
* Hamming window
* 50 Hz notch
* Applied using `lfilter()`

### IIR Filter

* 4th-order Butterworth bandpass filter
* Passband: 0.5 to 40 Hz
* Applied using `filtfilt()`

## Dataset

**MIT-BIH Arrhythmia Database**

* Record: 100
* Sampling frequency: 360 Hz
* Samples used: 3000
* Accessed using the WFDB Python library

## Technologies

* Python
* NumPy
* SciPy
* Matplotlib
* WFDB

## Results

The project provides:

* Original and noisy ECG waveforms
* FIR and IIR filtered ECG waveforms
* Frequency spectrum comparison using FFT
* SNR comparison
* Group delay comparison

## Project Structure

```text
ECG-Noise-Filter-Using-Digital-Filters/
├── index.py
├── ecg.py
└── README.md
```

## Installation

```bash
pip install numpy scipy matplotlib wfdb
```

## Run

```bash
python index.py
```

## Authors

**Sanjay Sivaprasad**
**Navaneeth P**
**Yash Kiran VP**

B.Tech Electronics and Communication Engineering
Vimal Jyothi Engineering College
(2026)
