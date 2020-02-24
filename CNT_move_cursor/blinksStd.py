# -*- coding: utf-8 -*-
"""
Estimate Relaxation from Band Powers

This example shows how to buffer, epoch, and transform EEG data from a single
electrode into values for each of the classic frequencies (e.g. alpha, beta, theta)
Furthermore, it shows how ratios of the band powers can be used to estimate
mental state for neurofeedback.

The neurofeedback protocols described here are inspired by
*Neurofeedback: A Comprehensive Review on System Design, Methodology and Clinical Applications* by Marzbani et. al

Adapted from https://github.com/NeuroTechX/bci-workshop
"""

import numpy as np  # Module that simplifies computations on matrices
import matplotlib.pyplot as plt  # Module used for plotting
import matplotlib.animation as animation
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import utils  # Our own utility functions
from blinkFilter import filt
from scipy import signal
import pyautogui # for spacebar
import datetime
import MoveCursor as m
import time
import _thread
from mne.filter import create_filter
from scipy.signal import lfilter, lfilter_zi
# Handy little enum to make code more readable

#pyautogui.PAUSE = 0.01                      # Make sure there is no delay between consecutive values when the autogui library is used

class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3

class Buffers:
    timestamp_buffer = None
    eeg_buffer = {}
    filter_state = None


""" EXPERIMENTAL PARAMETERS """
# Modify these to change aspects of the signal processing

# Length of the EEG data buffer (in seconds)
# This buffer will hold last n seconds of data and be used for calculations
BUFFER_LENGTH = 5

# Length of the epochs used to compute the FFT (in seconds)
EPOCH_LENGTH = 0.2

# Amount of overlap between two consecutive epochs (in seconds)
OVERLAP_LENGTH = 0.1

# Amount to 'shift' the start of each next consecutive epoch
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

# Index of the channel(s) (electrodes) to be used
# 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
INDEX_CHANNEL_LEFT = [1]
INDEX_CHANNEL_RIGHT = [2]

def input_thread(flag):
    input()
    flag.append(True)

def get_average_blink(eye_index):
    eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
    filter_state = None
    eye = "left" if eye_index == INDEX_CHANNEL_LEFT else "right"
    print("Please blink your " + eye + " eye. Press enter when done.")
    maxMatches = []
    stop_flag = []
    _thread.start_new_thread(input_thread, (stop_flag,))
    i = 10 # number of times to run after user presses enter
    while i > 0:
        if stop_flag:
            i = i - 1
        eeg_data, timestamp = inlet.pull_chunk(
            timeout=1, max_samples=int(SHIFT_LENGTH * fs))

        # Only keep the channel we're interested in
        ch_data = np.array(eeg_data)[:, eye_index]

        # Update EEG buffer with the new data
        eeg_buffer, filter_state = utils.update_buffer(
            eeg_buffer, ch_data, notch=True,
            filter_state=filter_state)

        """ 3.2 COMPUTE BAND POWERS """
        # Get newest samples from the buffer
        data_epoch = utils.get_last_data(eeg_buffer,
                int(EPOCH_LENGTH * fs))
        matchFilt = signal.hilbert(filt)
        matches = signal.correlate(matchFilt,data_epoch[:,0])
        matchesAbs = np.abs(matches[:])
        maxMatches.append((np.max(matchesAbs)/1e5).astype(int))

    maxMatchesIdx = np.argmax(maxMatches)
    idx = maxMatchesIdx
    peakValues = []
    stop_flag = 1
    check_right_side = False
    while True:
        if idx > 0 and idx < len(maxMatches) - 1:
            idx = idx + (1 if stop_flag == 2 else -1)
            possPeak = maxMatches[idx]
            if maxMatches[maxMatchesIdx]*0.6 < possPeak:
                peakValues.append(possPeak)
            elif stop_flag == 2:
                break
            else:
                check_right_side = True
        elif stop_flag == 2:
            break
        else:
            check_right_side = True
        if check_right_side:
            idx = maxMatchesIdx
            stop_flag = 2
            check_right_side = False

    return peakValues


def calibrate(rep):
    maxMatches = np.zeros((2, rep))
    maxMatchesLength = np.zeros((2, rep))
    for eye in [0 , 1]: # left = 0, right = 1
        for i in range(rep):
            temp = get_average_blink(
                INDEX_CHANNEL_LEFT if eye == 0 else INDEX_CHANNEL_RIGHT)
            maxMatches[eye, i] = np.average(temp)
            maxMatchesLength[eye, i] = len(temp)

    return np.average(maxMatches[0, :]), \
            np.average(maxMatches[1, :]), \
            np.average(maxMatchesLength[0, :]), \
            np.average(maxMatchesLength[1, :])

def live_plot(i, buff, ax, channel, update=False):
    if update:
        eeg_data, timestamp = inlet.pull_chunk(
            timeout=1, max_samples=int(SHIFT_LENGTH * fs))

        ch_data_left = np.array(eeg_data)[:, INDEX_CHANNEL_LEFT]
        ch_data_right = np.array(eeg_data)[:, INDEX_CHANNEL_RIGHT]
        timestamp = np.reshape(timestamp, (len(timestamp), 1))


        buff.eeg_buffer[str(INDEX_CHANNEL_LEFT)], filter_state = utils.update_buffer(
            buff.eeg_buffer[str(INDEX_CHANNEL_LEFT)], ch_data_left)
        buff.eeg_buffer[str(INDEX_CHANNEL_RIGHT)], filter_state = utils.update_buffer(
            buff.eeg_buffer[str(INDEX_CHANNEL_RIGHT)], ch_data_right)
        buff.timestamp_buffer, _ = utils.update_buffer(
            buff.timestamp_buffer, timestamp)

    xs = (buff.timestamp_buffer)
    ys = (buff.eeg_buffer[str(channel)])

    xs = xs[-500:]
    ys = ys[-500:]

    ax.clear()
    ax.set_ylim(-3000, 3000)
    ax.plot(xs, ys)

    plt.subplots_adjust(bottom=0.30)

def plot():
    buff = Buffers()

    buff.eeg_buffer[str(INDEX_CHANNEL_LEFT)] = np.zeros((int(fs * BUFFER_LENGTH), 1))
    buff.eeg_buffer[str(INDEX_CHANNEL_RIGHT)] = np.zeros((int(fs * BUFFER_LENGTH), 1))
    buff.timestamp_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
    buff.filter_state = None

    fig = plt.figure(1)
    ax = fig.add_subplot(1, 1, 1)

    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(1, 1, 1)

    animL = animation.FuncAnimation(fig, live_plot,
            fargs=(buff, ax, INDEX_CHANNEL_LEFT,True,), interval=1)
#    animR = animation.FuncAnimation(fig2, live_plot,
#           fargs=(buff, ax2, INDEX_CHANNEL_RIGHT,), interval=1)
    plt.show()

def on_timer(   ):
        """Add some data at the end of each signal (real-time signals)."""

        samples, timestamps = inlet.pull_chunk(timeout=0.0, max_samples=100)
        if timestamps:
            samples = np.array(samples)[:, ::-1]

            data = np.vstack([data, samples])
            data = data[-n_samples :]
            filt_samples, filt_state = lfilter(
                bf, af, samples, axis=0, zi=filt_state
            )
            data_f = np.vstack([data_f, filt_samples])
            data_f = data_f[-n_samples :]

            if filt:
                plot_data = data_f / scale
            elif not filt:
                plot_data = (data - data.mean(axis=0)) / scale

            sd = np.std(plot_data[-int(sfreq) :], axis=0)[::-1] * scale
            co = np.int32(np.tanh((sd - 30) / 15) * 5 + 5)


            for ii in range(n_chans):
                quality[ii].text = "%.2f" % (sd[ii])
                quality[ii].color = quality_colors[co[ii]]
                quality[ii].font_size = 3 + co[ii]

                names[ii].font_size = 3 + co[ii]
                names[ii].color = quality_colors[co[ii]]

            program["a_position"].set_data(plot_data.T.ravel().astype(np.float32))
            update()

if __name__ == "__main__":

    """ 1. CONNECT TO EEG STREAM """

    # Search for active LSL streams
    new_cursor = m.MoveCursor()
    new_cursor.draw(3)
    print('Looking for an EEG stream...')
    streams = resolve_byprop('type', 'EEG', timeout=2)
    if len(streams) == 0:
        raise RuntimeError('Can\'t find EEG stream.')

    # Set active EEG stream to inlet and apply time correction
    print("Start acquiring data")
    inlet = StreamInlet(streams[0], max_chunklen=12)
    eeg_time_correction = inlet.time_correction()

    # Get the stream info and description
    info = inlet.info()
    description = info.desc()

    # Get the sampling frequency
    # This is an important value that represents how many EEG data points are
    # collected in a second. This influences our frequency band calculation.
    # for the Muse 2016, this should always be 256
    fs = int(info.nominal_srate())

    """ 2. INITIALIZE BUFFERS """

    # Initialize raw EEG data buffer
    eeg_buffer_left = np.zeros((int(fs * BUFFER_LENGTH), 1))
    eeg_buffer_right = np.zeros((int(fs * BUFFER_LENGTH), 1))
    filter_state_left = None  # for use with the notch filter
    filter_state_right = None  # for use with the notch filter

    # plot()

    # Compute the number of epochs in "buffer_length"
    n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) /
                              SHIFT_LENGTH + 1))

    # Initialize the band power buffer (for plotting)
    # bands will be ordered: [delta, theta, alpha, beta]
    band_buffer = np.zeros((n_win_test, 4))

    """ 3. GET DATA """

    # The try/except structure allows to quit the while loop by aborting the
    # script with <Ctrl-C>
    print('Press Ctrl-C in the console to break the while loop.')
    oldTimeL = datetime.datetime.now() # initialize time delta
    oldTimeR = datetime.datetime.now() # initialize time delta

    """

    #calibrate
    left_thresh, right_thresh, left_delay, right_delay = calibrate(3)

    #normalize delay
    left_delay = left_delay * 40 + 100
    right_delay = right_delay * 30 + 70

    print("left_thresh: %d   right_thresh: %d" % (left_thresh, right_thresh))
    print("left_delay: %d   right_delay: %d" % (left_delay, right_delay))
    input()

    """

    n_samples = int(fs * 10) #10 is window size
    data_fLeft = np.zeros((n_samples, 1))
    data_fRight = np.zeros((n_samples, 1))
    af = [1.0]
    bf = create_filter(data_fLeft.T, fs, 3, 40.0, method = "fir") #do
    zi = lfilter_zi(bf, af)
    dataLeft = np.zeros((n_samples, 1))
    dataRight = np.zeros((n_samples, 1))
    filt_stateLeft = np.tile(zi, (1, 1)).transpose()
    filt_stateRight = np.tile(zi, (1, 1)).transpose()
    oldTimeL = datetime.datetime.now() # initialize time delta
    oldTimeR = datetime.datetime.now() # initialize time delta

    try:
        # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
        while True:
            """Add some data at the end of each signal (real-time signals)."""
            samples, timestamps = inlet.pull_chunk(timeout=0.0, max_samples=100)
            new_cursor.check_direction()
            if timestamps:
                samplesLeft = np.array(samples)[:, INDEX_CHANNEL_LEFT]
                dataLeft = np.vstack([dataLeft, samplesLeft])
                dataLeft = dataLeft[-n_samples :]
                filt_samples, filt_stateLeft = lfilter(
                    bf, af, samplesLeft, axis=0, zi=filt_stateLeft)
                data_fLeft = np.vstack([data_fLeft, filt_samples])
                data_fLeft = data_fLeft[-n_samples :]
                plot_data = data_fLeft / 500
                

                sd = np.std(plot_data[-int(fs) :], axis=0)[::-1] * 500 # 500 = scale
                co = np.int32(np.tanh((sd - 30) / 15) * 5 + 5)
        

                if(co > 1):
                    #print("Left eye blink" + str(sd))
                    newTime = datetime.datetime.now()
                    if (newTime - oldTimeL).total_seconds()*1000 > 150:
                        new_cursor.movement = False
                        new_cursor.start_action("L")
                    oldTimeL = newTime

                # ----------------------

                samplesRight = np.array(samples)[:, INDEX_CHANNEL_RIGHT]
                dataRight = np.vstack([dataRight, samplesRight])
                dataRight = dataRight[-n_samples :]
                filt_samples, filt_stateRight = lfilter(
                    bf, af, samplesRight, axis=0, zi=filt_stateRight)
                data_fRight = np.vstack([data_fRight, filt_samples])
                data_fRight = data_fRight[-n_samples :]
                plot_data = data_fRight / 500
                

                sd = np.std(plot_data[-int(fs) :], axis=0)[::-1] * 500 # 500 = scale
                co = np.int32(np.tanh((sd - 30) / 15) * 5 + 5)
        

                if(co > 1):
                    #print("Right eye blink" + str(sd))
                    newTime = datetime.datetime.now()
                    if (newTime - oldTimeR).total_seconds()*1000 > 100:
                        new_cursor.movement = True if not new_cursor.movement else False
                        new_cursor.start_action("R")
                    oldTimeR = newTime
                
     
    except KeyboardInterrupt:
        print('Closing!')



