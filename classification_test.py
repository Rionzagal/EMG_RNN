from matplotlib.pyplot import subplots
from libs import *
from RNN import *
from EMG_signal import *

_, _, files = next(os.walk("./datasets/Biopac"))

r_index = np.random.randint(low=0, high=len(files))

active_filename = files[r_index]
print(f"Active file for evaluation: {active_filename}")

emg = signal(f"./datasets/Biopac/{active_filename}")
emg.pre_process(window=100)

plt.figure()
plt.plot(emg.envelopes['t'], emg.envelopes['ch_0'], label='pre_processed ch_0')
plt.plot(emg.envelopes['t'], emg.envelopes['ch_1'], label='pre_processed ch_1')
plt.legend()

emg.get_samples()
emg.sample_features()

for n in range(len(emg.features)):
    print(emg.features[n].head())

net_input = np.zeros(shape=(emg.features[n].shape[0], emg.features[n].shape[1], len(emg.features)), dtype=np.float16)

for n in range(len(emg.features)): net_input[:,:,n] = emg.features[n].to_numpy()

print(net_input.shape)

try:
    net = load_model("LSTM_model.h5","./Models")
except UnboundLocalError:
    warnings.warn("Neural Network model not found! Insert a valid filename and source or create a new model.")
    quit()

results = net.predict(net_input)
print(results.shape)

fig, axs = plt.subplots(nrows=results.shape[1], sharex='col')

for index in range(axs.size):
    axs[index].plot(results[:,index], label=f'class {index}')

fig.legend()

plt.show()
