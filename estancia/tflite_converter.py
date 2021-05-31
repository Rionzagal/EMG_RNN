import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow import lite as tflite
from matplotlib import pyplot as plt
from hex_to_c import hex_to_c_array

database = f"{os.getcwd()}\\JD señales"

_, _, files = next(os.walk(database))

signals = dict()

for file in files:

    print(file)

    fhand = open(f"{database}\\{file}")
    lines = fhand.read().splitlines()
    fhand.close()

    ch1 = list()
    ch2 = list()

    for line in lines[1:]:
        columns = [col.strip() for col in line.split(',') if col]
        try:
            ch1.append(float(columns[0]))
            ch2.append(float(columns[1]))
        except:
            continue

    ch1 = np.array(ch1)
    ch2 = np.array(ch2)

    for index in range(ch1.size):
        ch1[index] = ch1[index] if (ch1[index] < (np.mean(ch1) + 3*np.std(ch1))) and  (0.1*np.mean(ch1) < ch1[index]) else np.mean(ch1)
        ch2[index] = ch2[index] if (ch2[index] < (np.mean(ch2) + 3*np.std(ch2)))  and (0.1*np.mean(ch2) < ch2[index]) else np.mean(ch2)

    signals[file.split('_')[1]] = ch2

    figure, axs = plt.subplots(2,1,sharex=True)
    axs[0].plot(ch1, 'r')
    axs[1].plot(ch2, 'b')

print(signals.keys())

figure, axs = plt.subplots(2,1, sharex=True)
axs[0].plot(signals['extensor'], 'r')
axs[1].plot(signals['flexor'],'b')

plt.show()

_, _, model_files = next(os.walk(f"{os.getcwd()}\\Training"))


model = keras.models.load_model(filepath = f"{os.getcwd()}\\Training\\EMG_model.h5", custom_objects = None, compile = True, options = None)

interpreter = tflite.Interpreter(model_content = model)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


converter = tf.lite.TFLiteConverter.from_keras_model(model)
lite_model = converter.convert()
c_model_name = "EMG_RNN"

try:
    with open(f"{os.getcwd()}\\Training\\EMG_lite.tflite", "wb") as fhand:
        fhand.write(lite_model)
    print(f"File has been saved in dir: Training as EMG_lite.tflite")
except:
    print(f"File could not be saved! :c")

# Write TFLite model to a C source (or header) file
with open(c_model_name + '.h', 'w') as file:
  file.write(hex_to_c_array(lite_model, c_model_name))
