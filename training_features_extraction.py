from libs import *
from EMG_signal import *
from RNN import *

_, _, files = next(os.walk("./datasets/Biopac"))
for file in files:
    try:
        if not os.path.exists("./datasets/evaluated_files.txt"):
            fhand = open("./datasets/evaluated_files.txt", 'x')
        else:
            try:
                fhand = open("./datasets/evaluated_files.txt", 'r')
            except OSError:
                cont = input("Files cannot be indexed. Type 'y' if you want to continue.")
                if 'y' == cont:
                    fhand = None
                else:
                    quit()
        
        flag = False
        for line in fhand:
            if file in line: flag = True
        fhand.close()
        if flag: continue

        print(f"Evaluating {file}.")

        emg = signal(f"./datasets/Biopac/{file}", 1000, 2, 25000)

        envelope_signals = emg.pre_process(window = 200)
        classes = separate(envelope_signals, npoints=4500, separation=5000, n_classes=5)

        for index in range(len(classes)):
            print(f"Movement class: {index}")
            samples = get_queue(signal_df=classes[index], window=500)
            features = get_features(samples)
    
            for channel in range(len(features)):
                train_features = features[channel]
                train_features['channel'] = channel*np.ones(train_features.shape[0], dtype=np.uint8)
                train_features['target'] = index*np.ones(train_features.shape[0], dtype=np.uint8)

                if os.path.exists("./datasets/training_features.csv"):
                    mode = 'a'
                    head_flag = False
                else:
                    mode = 'w'
                    head_flag = True

                try:
                    train_features.to_csv("./datasets/training_features.csv", index=False, mode=mode, header=head_flag)
                except Exception:
                    warnings.warn(f"Cannot save the channel {channel} training features from {file} to file!")
    
        try: 
            fhand = open("./datasets/evaluated_files.txt", 'a')
            fhand.write(f"{file}\n")
            fhand.close()
        except OSError:
            warnings.warn("Evaluated file cannot be registered!")
    
    except Exception:
        warnings.warn("Error encountered. Data adquisition terminated.")

print("All of the files have been evaluated!")
