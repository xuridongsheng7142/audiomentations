import os
import random
#from pathlib import Path

import numpy as np
import time
from scipy.io import wavfile

import sys
sys.path.append("./")
from audiomentations import (
    AddGaussianNoise,
    TimeStretch,
    PitchShift,
    Shift,
    Normalize,
    FrequencyMask,
    TimeMask,
    AddGaussianSNR,
    Gain,
)
#from audiomentations.augmentations.transforms import (
#    LowPassFilter,
#    HighPassFilter,
#    BandPassFilter,
#    ApplyImpulseResponse,
#    Reverse,
#)
from audiomentations.core.audio_loading_utils import load_sound_file
#from audiomentations.core.transforms_interface import (
#    MultichannelAudioNotSupportedException,
#)

exit ()
augmenter = AddGaussianSNR(min_snr_in_db=10, max_snr_in_db=30, p=1.0)
augmenter = TimeStretch(min_rate=0.9, max_rate=1.1, leave_length_unchanged=False, p=1.0)
augmenter = Gain(min_gain_in_db=-6, max_gain_in_db=6, p=1.0)
augmenter = FrequencyMask(min_frequency_band=0.5, max_frequency_band=0.6, p=1.0)
####augmenter = PitchShift(min_semitones=-4, max_semitones=4, p=1.0)
augmenter = Shift(min_fraction=-0.5, max_fraction=0.5, rollover=False, fade=True, fade_duration=0.3, p=1.0)
augmenter = Normalize(p=1.0)

sound_file_path = "/home/xudong.wang/xdwang/corpus/LR_2021/dev_train/../dev_train_fix/L001-train-039.wav"
output_file_path = "a.wav"

samples, sample_rate = load_sound_file(
    sound_file_path, sample_rate=None, mono=False
)

augmented_samples = augmenter(
    samples=samples, sample_rate=sample_rate
)

fix_data = np.asarray(augmented_samples * 32768, dtype=np.int16)

print(fix_data)
wavfile.write(
    output_file_path, rate=sample_rate, data=fix_data
)
