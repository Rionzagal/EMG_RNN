import os
import argparse
import numpy as np                                              #pip install numpy
import pandas as pd                                             #pip install pandas
from scipy.io import loadmat                                    #pip install scipy
from tensorflow import keras                                    #pip install tensorflow, tensorboard, keras (Si tienes GPU revisa la instalación de CUDA Toolkit 11.0 para que funcione de la mejor manera.)
from matplotlib import pyplot as plt                            #pip install matplotlib
from sklearn.model_selection import train_test_split            #pip install sklearn
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM

#Program input params
parse = argparse.ArgumentParser('dnn_ea04.py')
parse.add_argument('--epochs', type = int, default = 5)
parse.add_argument('--samp_size', type = int, default = 100)
parse.add_argument('--samp_freq', type = int, default = 1000)
parse.add_argument('--n_channels', type = int, default = 2)
parse.add_argument('--base_dir', type = str, default = r'{}\Data'.format(os.getcwd()))
parse.add_argument('--train_dir', type = str, default = r'{}\Training'.format(os.getcwd()))
parse.add_argument('--model_filename', type = str, default = 'EMG_model.h5')
args = parse.parse_args()

class EMG(object):
    #EMG signals object
    def __init__(self, source = args.base_dir, fs = args.samp_freq, n_channels = args.n_channels):
        #Constructor
        self.fs = fs
        self.channels = dict()
        _, _, filenames = next(os.walk(source))
        for c in range(n_channels): self.channels[f'ch_{c}'] = list()
        for file in filenames:
            try:
                fhand = loadmat(f'{source}\\{file}')
                data = np.array(fhand['data'])
                for c in range(n_channels): self.channels[f'ch_{c}'].append(data[:, c])
            except:
                continue

    def pre_process(self, window = 50, max_amp = 1.):
        #Signal pre-processing by rectification and filtration
        for channel in self.channels.keys():
            for signal in self.channels[channel]:
                f_signal = list()
                for t in range(len(signal)): signal[t] = signal[t]**2
                signal *= (0xFFFF/(np.max(signal)))
                for t in range(len(signal)):
                    if signal.shape[0] < t + window: break
                    f_signal.append(np.mean(signal[t: t + window]))
                signal = np.array(f_signal, np.uint16)

    def separate(self, npoints = 4500, separation = 5000, classes = 5):
        #Separation by class method
        self.classes = dict()
        for channel in self.channels.keys():
            self.classes[channel] = dict()
            for c in range(classes):
                self.classes[channel][str(c)] = list()
                start = separation*c
                stop = start + npoints
                for signal in self.channels[channel]: self.classes[channel][str(c)].append(signal[start: stop])

    def get_samples(self, size = args.samp_size):
        #Sample generation
        self.samples = dict()
        for channel in self.classes.keys():
            self.samples[channel] = dict()
            for label in self.classes[channel].keys():
                self.samples[channel][label] = list()
                for signal in self.classes[channel][label]:
                    for t in range(len(signal)):
                        if len(signal) < t + size: break
                        self.samples[channel][label].append(signal[t: t+size])

    def get_features(self):
        #Feature extraction from samples
        data = list()
        features = dict()
        targets = dict()
        for channel in self.classes.keys():
            features[channel] = {
                'RMS': list(),
                'mean': list(),
                'std': list()
            }
            targets[channel] = list()
        for channel in self.samples.keys():
            for label in self.samples[channel].keys():
                for sample in self.samples[channel][label]:
                    features[channel]['RMS'].append(np.sqrt(sum(sample**2)/sample.shape[0]))
                    features[channel]['mean'].append(np.mean(sample))
                    features[channel]['std'].append(np.std(sample))
                    targets[channel].append(int(label))
            data.append(pd.DataFrame(features[channel]))
        targets = np.array(targets[channel])
        return data, targets

class RNN(object):
    def __init__(self, input_shape, add_Dropout = False, Drop = 0.2):
        self.model = Sequential()
        self.opt = None
        self.compiled = False

        self.model.add(LSTM(128, input_shape = input_shape, return_sequences = True))
        if add_Dropout: self.model.add(Dropout(Drop))
        self.model.add(LSTM(128))
        if add_Dropout: self.model.add(Dropout(Drop))
        self.model.add(Dense(32))
        if add_Dropout: self.model.add(Dropout(0.5*Drop))
        self.model.add(Dense(5, activation = 'softmax'))

    def set_Adam_optim(self, learning_rate = 1e-3, decay = None):
        if decay is None:
            self.opt = keras.optimizers.Adam(lr = learning_rate)
        else:
            self.opt = keras.optimizers.Adam(lr = learning_rate, decay = decay)

    def compile(self, loss = 'mean_squared_error', metrics = ['accuracy']):
        if self.opt is None:
            print("Optimizer not set! Please set an optimizer.")
        else:
            self.model.compile(loss = loss, optimizer = self.opt, metrics = metrics)
            self.compiled = True

    def train_model(self, x_train, y_train, x_val, y_val, epochs = 10):
        if self.compiled:
            history = self.model.fit(x_train, y_train, epochs = epochs, validation_data = (x_val, y_val))
            print(f"Model successfuly trianed in {epochs} epochs!\nRetrieved metrics and values: {history.history.keys()}")
        else:
            print("Model not ready to trian! Be sure that the layers, optimizer and compilations are all set!")
            history = None
        return history

    def load_model(self, filename, source):
        try:
            file = f"{source}\\{filename}"
            self.model = keras.models.load_model(filepath = file, custom_objects = None, compile = True, options = None)
            print(f"Model successfuly extracted from {source} as {filename}.")
            print(self.model.summary())
        except:
            print("Could not create a model from filename!\nPlease create a new model.")

def main():
    signals = EMG(source = args.base_dir, fs = args.samp_freq)
    signals.pre_process(window = 50, max_amp = 1.)
    signals.separate(npoints = 4500, separation = 5000, classes = 5)
    signals.get_samples(size = 200)
    channel_features, targets = signals.get_features()
    for c in range(len(channel_features)): print(f"Channel {c} features:\n{channel_features[c].head()}")
    features = np.zeros((channel_features[0].shape[0], channel_features[0].shape[1], len(channel_features)))
    for c in range(len(channel_features)): features[:, :, c] = channel_features[c].to_numpy()
    x_train, x_val, y_train, y_val = train_test_split(features, targets, test_size = 0.4, random_state = 0)

    net = RNN(input_shape = (x_train.shape[1:]), add_Dropout = False)
    net.load_model(filename = args.model_filename, source = args.train_dir)
    net.set_Adam_optim(learning_rate = 1e-3, decay = 1e-6)
    net.compile(loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
    try:
        history = net.train_model(x_train = x_train, y_train = y_train, x_val = x_val, y_val = y_val, epochs = 100)
    except KeyboardInterrupt:
        print("Model training interrupted. Terminating now.")
        quit()
    if history is not None:
        # summarize history for accuracy
        plt.figure()
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc = 'upper left')
        plt.savefig(f"{os.getcwd()}\\Results\\model_accuracy.png")
        # summarize history for loss
        plt.figure()
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc = 'upper left')
        plt.savefig(f"{os.getcwd()}\\Results\\model_loss.png")
        plt.show()
    net.model.save(filepath = f"{args.train_dir}\\{args.model_filename}", overwrite = True, include_optimizer = True)
if __name__ == '__main__':
    main()
