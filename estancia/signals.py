import os
import numpy as np
from scipy.io import loadmat
from matplotlib import pyplot as plt

_, _, files = next(os.walk(f"{os.getcwd()}\\Data"))
fhand = loadmat(f'{os.getcwd()}\\Data\\{files[0]}')

fig, axs = plt.subplots(2, 1, sharex='col')
t = np.arange(start=0, stop=25, step=0.001)
axs[0].plot(t, np.array(fhand['data'])[:25000, 0])
axs[0].grid()
axs[1].plot(t, np.array(fhand['data'])[:25000, 1])
axs[1].grid()

axs[0].set(ylabel = 'voltage (V)', title = 'EMG channel 1')
axs[1].set(xlabel = 'time (s)', ylabel = 'voltage (V)', title = 'EMG channel 2')


ch1 = np.array(fhand['data'])[:4500, 0]
ch1square = ch1**2
t = np.linspace(0., ch1.shape[0]/1000, ch1.shape[0])

movmean = list()
for n in range(len(ch1square)):
    if ch1square.shape[0] < n + 20: break
    movmean.append(np.mean(ch1square[n: n + 20]))
movmean = np.array(movmean)
tmm = np.linspace(0., ch1.shape[0]/1000, movmean.shape[0])

fig, ax = plt.subplots()
ax.plot(t, ch1)
ax.set(xlabel='time (s)', ylabel='voltage (V)',
       title='Raw EMG signal')
ax.grid()

fig, axs = plt.subplots(3, 1, sharex = 'col')
axs[0].plot(t, ch1, 'r')
axs[0].grid()
axs[0].set(ylabel = 'voltage (V)', title = 'A')
axs[1].plot(t, ch1square, 'g')
axs[1].grid()
axs[1].set(ylabel = 'voltage (V)', title = 'B')
axs[2].plot(tmm, movmean, 'b')
axs[2].grid()
axs[2].set(xlabel = 'time (s)', ylabel = 'voltage (V)', title = 'C')

plt.figure()
plt.plot(tmm[:100], movmean[:100])
plt.grid(True)
plt.title('EMG envelope signal')
plt.xlabel('time (s)')
plt.ylabel('voltage (V)')

plt.show()
