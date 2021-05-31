import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from scipy.io import loadmat 
from matplotlib import pyplot as plt


class signal(object):
    def __init__(self, source, fs = 2000, n_channels = 2):
        self.fs = fs
        self.channels = dict()
        #for c in range(n_channels): self.channels[f'ch_{c}'] = list()
        try:
            fhand = loadmat(source)
            data = np.array(fhand['data'])
            for c in range(n_channels): self.channels[f'ch_{c}'] = data[:, c]
        except:
            print("F")
    
    def pre_process(self, window = 50):
        #Signal pre-processing by rectification and filtration
        for channel in self.channels.keys():
            f_signal = list()
            for t in range(self.channels[channel].size): self.channels[channel][t] = self.channels[channel][t]**2
            self.channels[channel] *= (0xFFFF/(np.max(self.channels[channel])))
            for t in range(self.channels[channel].size):
                if self.channels[channel].shape[0] < t + window: break
                f_signal.append(np.mean(self.channels[channel][t: t + window]))
            self.channels[channel] = np.array(f_signal, dtype=np.uint16)

    def generate_samples(self, window = 100):
        self.samples = dict()
        for channel in self.channels.keys():
            self.samples[channel] = list()
            for t in range(self.channels[channel].size):
                if self.channels[channel].size < t + window: break
                self.samples[channel].append(np.array(self.channels[channel][t: t + window]))

    def get_features(self):
        data = list()
        for channel in self.samples.keys():
            channel_features = {
                'RMS': list(),
                'mean': list(),
                'std': list()
            }
            for sample in self.samples[channel]:
                channel_features['RMS'].append(np.sqrt(sum(sample**2)/sample.shape[0]))
                channel_features['mean'].append(np.mean(sample))
                channel_features['std'].append(np.std(sample))
            data.append(pd.DataFrame(channel_features))
        return data

model = keras.models.load_model(r"{}\Training\EMG_model.h5".format(os.getcwd()), compile=True)

_, _, files = next(os.walk(f"{os.getcwd()}\\Data"))

current_file = files[np.random.randint(low=0, high=len(files)-1)]
fhand = loadmat(f'{os.getcwd()}\\Data\\{current_file}')

ch1 = fhand['data'][:25000, 0]
ch2 = fhand['data'][:25000, 1]

t = np.linspace(start=0, stop=25, num=ch1.size)

fig, (ax0, ax1) = plt.subplots(2,1, sharex='col')
ax0.plot(t, ch1, color='r', label='Extensor muscle signal')
ax1.plot(t, ch2, color='b', label='Flexor muscle signal')

for ax in [ax1, ax0]:
    ax.set_ylabel('voltage [V]')
    ax.grid()

ax1.set_xlabel('time [s]')
fig.legend(loc='upper left')

channels = [ch1, ch2]
f_signals = [list(), list()]

for c in range(2):
    for i in range(t.size): channels[c][i] = (channels[c][i]**2)
    for i in range(t.size):
        if channels[c].shape[0] < i + 50: break
        f_signals[c].append(np.mean(channels[c][i: i + 50]))

fig, (ax0, ax1) = plt.subplots(2, 1, sharex='col')

t_proc = np.linspace(0, 25, len(f_signals[c]))

ax0.plot(t_proc, f_signals[0], color='r', label='Processed extensor signal')
ax1.plot(t_proc, f_signals[1], color='b', label='Processed flexor signal')

for ax in [ax1, ax0]:
    ax.set_ylabel('Amplitude')
    ax.grid()

ax1.set_xlabel('time [s]')
fig.legend(loc='upper left')

emg = signal(fs = 1000, n_channels = 2, source = f'{os.getcwd()}\\Data\\{current_file}')
emg.pre_process()
emg.generate_samples(window = 100)
features = emg.get_features()
input = np.zeros((features[0].shape[0], features[0].shape[1], len(features)))
for c in range(len(features)):
    print(f"Some of the features extracted in channel {c} are:\n{features[c].head()}")
    input[:, :, c] = features[c].to_numpy()
print(f"Input generated as a {input.shape} tensor.")

prediction = model.predict(input)

fig, ax = plt.subplots(nrows=prediction.shape[1], ncols=1, sharex=True, sharey=False)
for c in range(prediction.shape[1]):
    ax[c].plot(prediction[:, c])
    ax[c].set_title(f"Prediction for class {c} movement")

plt.show()
