import os
from pathlib import Path

import numpy as np

AUDIO_FILENAME_ENDINGS = (".aiff", ".flac", ".m4a", ".mp3", ".ogg", ".opus", ".wav")


def get_file_paths(
    root_path,
    filename_endings=AUDIO_FILENAME_ENDINGS,
    traverse_subdirectories=True,
    follow_symlinks=True,
):
    """Return a list of paths to all files with the given filename extensions in a directory.
    Also traverses subdirectories by default.
    """
    file_paths = []

    for root, dirs, filenames in os.walk(root_path, followlinks=follow_symlinks):
        filenames = sorted(filenames)
        for filename in filenames:
            input_path = os.path.abspath(root)
            file_path = os.path.join(input_path, filename)

            if filename.lower().endswith(filename_endings):
                file_paths.append(Path(file_path))
        if not traverse_subdirectories:
            # prevent descending into subfolders
            break

    return file_paths


def calculate_rms(samples):
    """Given a numpy array of audio samples, return its Root Mean Square (RMS)."""
    return np.sqrt(np.mean(np.square(samples)))


def calculate_rms_without_silence(samples, sample_rate):
    """
    This function returns the rms of a given noise whose silent periods have been removed. This ensures
    that the rms of the noise is not underestimated. Is most useful for short non-stationary noises.
    """

    window = int(0.025 * sample_rate)

    if samples.shape[-1] < window:
        return calculate_rms(samples)

    rms_all_windows = np.zeros(samples.shape[-1] // window)
    current_time = 0

    while current_time < samples.shape[-1] - window:
        rms_all_windows[current_time // window] += calculate_rms(
            samples[current_time : current_time + window]
        )
        current_time += window

    rms_threshold = np.max(rms_all_windows) / 25

    # The segments with a too low rms are identified and discarded
    rms_all_windows = rms_all_windows[rms_all_windows > rms_threshold]
    # Beware that each window must have the same number of samples so that this calculation of the rms is valid.
    return calculate_rms(rms_all_windows)


def calculate_desired_noise_rms(clean_rms, snr):
    """
    Given the Root Mean Square (RMS) of a clean sound and a desired signal-to-noise ratio (SNR),
    calculate the desired RMS of a noise sound to be mixed in.

    Based on https://github.com/Sato-Kunihiko/audio-SNR/blob/8d2c933b6c0afe6f1203251f4877e7a1068a6130/create_mixed_audio_file.py#L20
    :param clean_rms: Root Mean Square (RMS) - a value between 0.0 and 1.0
    :param snr: Signal-to-Noise (SNR) Ratio in dB - typically somewhere between -20 and 60
    :return:
    """
    a = float(snr) / 20
    noise_rms = clean_rms / (10 ** a)
    return noise_rms


def convert_decibels_to_amplitude_ratio(decibels):
    return 10 ** (decibels / 20)


def is_waveform_multichannel(samples):
    """
    Return bool that answers the question: Is the given ndarray a multichannel waveform or not?

    :param samples: numpy ndarray
    :return:
    """
    return len(samples.shape) > 1


def is_spectrogram_multichannel(spectrogram):
    """
    Return bool that answers the question: Is the given ndarray a multichannel spectrogram?

    :param samples: numpy ndarray
    :return:
    """
    return len(spectrogram.shape) > 2 and spectrogram.shape[-1] > 1


def convert_float_samples_to_int16(y):
    """Convert floating-point numpy array of audio samples to int16."""
    if not issubclass(y.dtype.type, np.floating):
        raise ValueError("input samples not floating-point")
    return (y * np.iinfo(np.int16).max).astype(np.int16)


def convert_int16_samples_to_float(y):
    """Convert int16 numpy array of audio samples to floating-point."""
    if not issubclass(y.dtype.type, np.int16):
        raise ValueError("input samples not int16")
    return (y / np.iinfo(np.int16).max).astype(np.float32)
