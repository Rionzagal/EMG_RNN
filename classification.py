from libs import *
from EMG_signal import *
from RNN import *

biopac_source = f"./datasets/Biopac/11_1.mat"

emg = signal(biopac_source, 1000, 2, 25000)
print(emg.channels.head())

envelope_signals = emg.pre_process(1.)
print(envelope_signals.head())

classes = separate(envelope_signals, npoints=4500, separation=5000, n_classes=5)

for index in range(len(classes)):
    print(f"Movement class: {index}")
    print(classes[index].head())
    samples = get_queue(signal_df=classes[index], window=100)

    features = get_features(samples)
    
    for feature in features:
        print(feature.head())
