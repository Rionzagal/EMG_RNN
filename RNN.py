from libs import *

def LSTM_RNN(input_shape, output_classes = 5, LSTM_layers = 2, LSTM_units = 128, Dense_layers = 1, Dense_units = 32, DropOut = 0):
    """
    LSTM network creation method using only LSTM and Dense layers.
    input_shape [tuple] = The input model shape, which will create an array input for data evaluation
    output_classes [uint] = The amount of desired output classes in the model. Model is a classifier, so the output function will be 'softmax'.
    LSTM_layers [uint] = Amount of LSTM layers in the network.
    LSTM_units [uint] = Amount of LSTM units in each LSTM layer.
    Dense_layers [uint] = Amount of Dense layers in the network.
    Desne_units [uint] = Amount of Dense units en each Dense layer.
    DropOut [float] = The amount of data dropout between 0 and 1 between each hidden LSTM layer in the network.
    Returns the keras model created in this method.
    """
    model = Sequential()
    #Input layer generation
    model.add(LSTM(LSTM_units, input_shape = input_shape, return_sequences = True))
    #Hidden LSTM layer generation
    if 0 < DropOut: model.add(Dropout(DropOut))
    for l in range(LSTM_layers - 1):
        model.add(LSTM(LSTM_units))
        if 0 < DropOut: model.add(Dropout(DropOut))
    #Hidden Dense layer generation
    for l in range(Dense_layers): model.add(Dense(Dense_units))
    #Output layer generation
    model.add(Dense(output_classes, activation = 'softmax'))

    return model

def compile(model, loss = 'mean_squared_error', metrics = ['accuracy'], learning_rate = 1e-3, decay = None):
    """
    Keras model optimization and compolation method using a determined loss and metrics using Adam optimizer.
    model [keras model] = Initialized model to be optimized.
    loss [str] = Model compilation loss to be compared.
    metrics [str array] = Model metrics to be compiled and measured.
    learning_rate [ufloat] = Model optimization learning rate.
    decay [ufloat] = Model optimization decay. Default as 'None' for no optimization decay.
    Returns compiled model.
    """
    if decay is None:
        optimizer = keras.optimizers.Adam(lr = learning_rate)
    else:
        optimizer = keras.optimizers.Adam(lr = learning_rate, decay = decay)
    model.compile(loss = loss, optimizer = optimizer, metrics = metrics)
    return model
        

def train_model(model, x_train, y_train, x_val, y_val, epochs = 10):
    try:
        history = model.fit(x_train, y_train, epochs = epochs, validation_data = (x_val, y_val))
        print(f"Model successfuly trianed in {epochs} epochs!\nRetrieved metrics and values: {history.history.keys()}")
        #Summarize history for accuracy
        plt.figure()
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('LSTM_model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc = 'upper left')
        plt.savefig("./models/LSTM_model_accuracy.png")
        #Summarize history for loss
        plt.figure()
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('LSTM_model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc = 'upper right')
        plt.savefig("./models/LSTM_model_loss.png")
        plt.show()
        model.save(filepath = f"./models/LSTM_model.h5", overwrite = True, include_optimizer = True)
        print("Trained model saved in filepath: 'models/LSTM_model.h5'.")
    except Exception:
        warnings.warn("Model could not be trained! Please input a valid model.")

def load_model(filename, source):
    try:
        file = f"{source}\\{filename}"
        model = keras.models.load_model(filepath = file, compile = True)
        print(f"Model successfuly extracted from {source} as {filename}.")
        print(model.summary())
    except:
        warnings.warn("Could not create a model from filename!\nPlease create a new model.")

    return model