from libs import *
from RNN import *

feature_data = pd.read_csv("./datasets/training_features.csv")
print(feature_data.head())

feature_channels = feature_data['channel'].to_numpy()
print(feature_channels)

n_channels = np.max(feature_channels) + 1
channel_features = list()
feat_targets = pd.DataFrame()

for ch in range(n_channels):
    mask = feature_data['channel'] == ch
    curr_channel_feats = feature_data[mask]
    feat_targets[f"ch_{ch}"] = curr_channel_feats['target']
    channel_features.append(curr_channel_feats.drop(columns=['channel', 'target']))

tar = feat_targets.to_numpy()

targets = np.uint8(tar[:,0])
features = np.zeros(shape=(channel_features[ch].shape[0], channel_features[ch].shape[1], n_channels))

for ch in range(n_channels):
    features[:, :, ch] = channel_features[ch].to_numpy()

training_length = round(0.7*features.shape[0])
# x_train = features[:training_length, :, :]
# x_val = features[training_length:, :, :]
# y_train = targets[:training_length]
# y_val = targets[training_length:]

x_train, x_val, y_train, y_val = train_test_split(features, targets, test_size = 0.4, random_state = 0)

try:
    model = load_model("LSTM_model.h5","./Models")
except:
    model = LSTM_RNN(input_shape=(3,2), output_classes = 5, LSTM_layers = 2, LSTM_units = 128, Dense_layers = 2, Dense_units = 64, DropOut = 0.2)
    model = compile(model=model, loss='sparse_categorical_crossentropy', metrics=['accuracy'], learning_rate=1e-2, decay=1e-6)

train_model(model, x_train, y_train, x_val, y_val, epochs = 50)