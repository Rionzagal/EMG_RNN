from libs import *
from EMG_signal import *

biopac_source = f"./datasets/Biopac/11_1.mat"

emg = signal(biopac_source, 1000, 2, 25000)
envelope_signals = emg.pre_process(1.)
emg.get_queue()

print(emg.channels.head())

print(envelope_signals.head())
