from libs import *

def get_absolute_envelope(data, window = 20):
    abs_data = np.abs(data)
    envelope = list()
    for t in range(data.size):
        if data.size < t + window: break
        envelope.append(np.mean(abs_data[t: t+window]))
    return np.array(envelope)

def separate(data, npoints = 4500, separation = 5000, n_classes = 5):
    #Separation by class method
    classes = list()
    for c in range(n_classes):
        sep_data = pd.DataFrame()
        start = separation*c
        stop = start + npoints
        for channel in data.keys():
            if 't' == channel: continue
            sep_data[channel] = data[channel][start: stop]
        classes.append(sep_data)
    return classes

def get_queue(signal_df, window = 100):
    """
    Queue sampling method over a defined signal stored in the object. Signal can be either a raw Data variable or the 'envelopes' variable.
    window [uint] = amount of data points used for the dequeue storage over the sampling data.
    Returns a pandas DataFrame containing the sample queue vectors with length 'window' of each channel found in the sampling data.
    """
    #Data asign for queue process
    if ("<class 'pandas.core.frame.DataFrame'>" != str(signal_df.__class__)) and ("<class 'dict'>" != str(signal_df.__class__)):
        data = None
    else:
        data = pd.DataFrame(signal_df)
    if data is None:
        warnings.warn("Error. The needed argument must be either a raw signal or an envelope signal. Terminating now.")
        return False
        
    #Sample generation
    samples = dict()
    for key in data.keys():
        if ('t' != key):
            samples[key] = list()
            for t in range(data[key].size):
                if data[key].size < t+window: break
                samples[key].append(np.array(data[key][t: t+window]))
    samples_df = pd.DataFrame(samples)
    return samples_df

def get_features(samples):
    """
    Feature calcualtion method from sampling queue DataFrame.
    sample_array [pd.DataFrame] or [dict] = Sample DataFrame used for feature calculation. The sample data must be a DataFrame containing queue vectors in each of its values.
    Returns a list containing a pandas Dataframe with features 'RMS', 'mean' and 'standard deviation' for each channel found in the sample data.
    """
    #Data sample inspection
    if samples is None:
        warnings.warn("Sample data not found. Features cannot be calculated!")
        return False
    elif ("<class 'pandas.core.frame.DataFrame'>" != str(samples.__class__)) and ("<class 'dict'>" != str(samples.__class__)):
        warnings.warn(f"Sample data not valid. Sample data must be a pandas DataFrame or a dictionary, but is {str(samples.__class__)}. Features cannot be calculated!")
        return False
    if samples.__class__ == 'dict': samples = pd.DataFrame(samples)
    values = samples.values
    if 2 != values.shape.__len__():
        warnings.warn("Sample data not valid. Sample values must be numpy arrays or lists as vectors. Features cannot be calculated!")
        return False

    #Channel data frames generation for feature packaging
    data = list()
    for channel in samples.keys():
        channel_features = {
            'RMS': list(),
            'mean': list(),
            'std': list()
        }
    #Data features fill in Data Frame for each sample
        for sample in samples[channel]:
            channel_features['RMS'].append(np.sqrt(sum(sample**2)/sample.shape[0]))
            channel_features['mean'].append(np.mean(sample))
            channel_features['std'].append(np.std(sample))
        data.append(pd.DataFrame(channel_features))
    return data

class signal(object):
    channels = None
    envelopes = None
    samples = None
    features = None
    Error_outcome = False

    def pre_process(self, max_value = 1., window = 20):
        """
        Pre processing method over the signals stored in the object 'channels' variable.
        max_value [ufloat] or [uint] = Maximum value used for processed data normalization
        window [uint] = Amount of data points found in the signal used to generate the envelope by a moving average method
        Returns a pandas DataFrame containing the pre-processed channel signals and a time vector for reference.
        """
        #Envelope time vector generation
        envelopes = {'t': np.linspace(0, np.max(self.channels['t']), self.channels['t'].size-window+1)}

        #Envelope signal data appending
        for key in self.channels.keys():
            if 't' != key:
                signal = get_absolute_envelope(np.array(self.channels[key]), window)
                envelopes[key] = signal*(max_value/np.max(signal))
        self.envelopes = pd.DataFrame(envelopes)
        return self.envelopes

    def get_samples(self):
        self.samples = get_queue(signal_df=self.envelopes, window=100)

    def sample_features(self):
        self.features = get_features(sample_data=self.samples)

    def __init__(self, source, fs = 1000, n_channels = 2, n_data = 0):
        """
        Object describes the EMG needed signal to be processed in an MCU.
        The accepted source is either a .mat file, .log file, .txt file or a .csv file.
        source [str] = Data directory
        fs [uint] = Sampling frequency in Hz
        n_channels [uint] = Amount of channels to be evaluated in the file
        n_data [uint] = Amount of data points to be evaluated in each channel. 0 is to evaluate all of the present data in the file.
        """
        #Constructor
        self.fs = fs
        channels = dict()

        #File reading and data extraction
        if '.mat' in source:
            try:
                fhand = loadmat(source)
                data = np.array(fhand['data'])
            except:
                warnings.warn("Source file could not be extracted correctly or not found. Please specify a valid source file.")
                return self.Error_outcome
        elif ('.log' in source) or ('.txt' in source):
            try:
                fhand = open(source, 'r')
                lines = fhand.read().splitlines()
                fhand.close()
                data = np.empty((1, n_channels))
                for line in lines[1:]:
                    columns = [col.strip() for col in line.split(',') if col]
                    try:
                        columns = [float(col.strip()) for col in line.split(',') if col]
                        np.append(data, columns, axis = 0)
                    except:
                        continue
            except:
                warnings.warn("Source file could not be extracted correctly or not found. Please specify a valid source file.")
                return self.Error_outcome

        #Time vector generation and channels DataFrame packaging
        if 0 < n_data:
            channels['t'] = np.linspace(0, n_data/fs, n_data)
        else:
            channels['t'] = np.linspace(0, data.shape[0]/fs, data.shape[0])
        for c in range(n_channels): channels[f'ch_{c}'] = data[:n_data, c] if 0 < n_data else data[:, c]
        self.channels = pd.DataFrame(channels)
