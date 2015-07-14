# Authors: Praveen Sripad <praveen.sripad@rwth-aachen.de>
#          Alexandre Gramfort <alexandre.gramfort@telecom-paristech.fr>
#
# License: BSD (3-clause)

import numpy as np
from scipy import stats
from scipy.signal import hilbert
from nose.tools import assert_true, assert_raises
from mne.utils import check_random_state, run_tests_if_main
from mne.connectivity.cfc import (modulation_index, shuffle_data,
                                  cross_frequency_coupling,
                                  generate_pac_signal)


def test_generate_pac_data():
    """ Test generation of phase amplitude coupled data. """
    assert_raises(RuntimeError, generate_pac_signal, 1000., 1, 1, 8., 60.)
    assert_raises(ValueError, generate_pac_signal, 1000., 1, 10, 8., 60.,
                  sigma=0)


def test_phase_amplitude_coupling():
    """ Test phase amplitdue coupling. """

    fs, times, trials = 100., 1, 10
    times = np.linspace(0, times, fs * times)

    rng = check_random_state(42)
    white_noise = rng.normal(0, 0.2, len(times))

    phase_series_fp = np.angle(hilbert(white_noise)) + np.pi
    bin_size = 2 * np.pi / 18  # for 18 bins
    phase_bins = np.arange(phase_series_fp.min(),
                           phase_series_fp.max() + bin_size, bin_size)
    assert_true(len(phase_bins) - 1 == 18)

    amplitude_bin_means = np.zeros((trials, 18))
    amplitude_bin_means[:, rng.randint(0, 19)] = 1
    for i in range(trials):
        assert_true(modulation_index(amplitude_bin_means)[i] == 1.)


def test_modulation_index():
    """ Test computation of normalized modulation index. """

    rng = check_random_state(42)
    trials = 10
    amplitude_dist = np.zeros((trials, 0))
    assert_raises(ValueError, modulation_index, amplitude_dist)
    amplitude_dist = np.zeros((trials, 18))
    amplitude_dist[:, rng.randint(0, 19)] = 2
    assert_raises(ValueError, modulation_index, amplitude_dist)
    dist = rng.rand(1, 18)
    dist /= dist.sum()
    mi = 1. - (stats.entropy(dist[0]) / np.log(len(dist[0])))
    assert_true(0. <= mi <= 1.)


def test_shuffle_data():
    """ Test generation of surrogate data. """

    times = np.linspace(0, 1, 100. * 1 * 10)
    data = np.reshape(times, (10, 100))
    surr_data = shuffle_data(data)
    assert_true(data.shape == surr_data.shape)


def test_cross_frequency_coupling():
    """ Test cross frequency coupling. """

    data = np.ones((1, 100))
    assert_raises(ValueError, cross_frequency_coupling,
                  data,
                  1000., 8., 5, 60., 80., 20)

run_tests_if_main()
