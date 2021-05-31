from libs import *

def get_absolute_envelope(data, window = 20):
    abs_data = np.abs(data)
    envelope = list()
    for t in range(data.size):
        if data.size < t + window: break
        envelope.append(np.mean(abs_data[t: t+window]))
    return np.array(envelope)

class signal(object):
    def __init__(self, source, fs = 1000, n_channels = 2, n_data = 0):
        #Constructor
        self.fs = fs
        channels = dict()
        try:
            fhand = loadmat(source)
            data = np.array(fhand['data'])
        except:
            warnings.warn("Source file could not be extracted correctly or not found. Please specify a valid source file.")
            return -1
        if 0 < n_data:
            channels['t'] = np.linspace(0, n_data/fs, n_data)
        else:
            channels['t'] = np.linspace(0, data.shape[0]/fs, data.shape[0])
        for c in range(n_channels): channels[f'ch_{c}'] = data[:n_data, c] if 0 < n_data else data[:, c]
        self.channels = pd.DataFrame(channels)

    def pre_process(self, max_value = 1., window = 20):
        envelopes = {'t': np.linspace(0, np.max(self.channels['t']), self.channels['t'].size-window+1)}
        for key in self.channels.keys():
            if 't' != key:
                signal = get_absolute_envelope(np.array(self.channels[key]), window)
                envelopes[key] = signal*(max_value/np.max(signal))
        self.envelopes = pd.DataFrame(envelopes)
        return self.envelopes

    def get_queue(self, window = 100):
        #Sample generation
        samples = dict()
        for key in self.channels.keys():
            if 't' != key:
                samples[key] = list()
                for t in range(self.channels[key].size):
                    if self.channels[key].size < t+window: break
                    samples[key].append(np.array(self.channels[key][t: t+window]))
        self.samples = pd.DataFrame(samples)

    def get_features(self):
        pass
