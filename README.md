# EMG signal classification using RNN (_Recurrent Neural Network_)

Remote control algorithms and schema is always changing in order to be even more practical and precise than its past evolution. As the gesture recognition algorithms based on EMG evolve, more gestures can be obtained by the usage of Artificial Neural Networks (_ANN_). These algorithms are designed to identify a certain position or movement in a specified region, which makes them useful for diagnostics. In this study we focus on the dynamic classification of five different possitions of the forearm based on EMG, and the possibility to embed this system into a micro-controller unit (_MCU_). In order to provide a solution to this project, an EMG classification system is proposed, using **2 EMG channels located on the forearm** (_CH\_0 located in flexor group and CH\_1 located in extensor group_) and a classifier algorithm based on Recurrent Neural Network (_RNN_) to classify the combined input signals from each channel and provide a group of commands based on the possition of the forearm and the activity of each muscular group.

## EMG signal obtention and pre-processing

In order to successfuly register EMG signals, we used the [_Myoware_](https://dynamoelectronics.com/tienda/myoware-muscle-sensor/) system, which registers, amplifies and rectifies the EMG signal produced between its two muscle electrodes and its reference electrode. It then sends the amplified and rectified signal through the output signal _SIG_ pin. The MCU then registers the signal in a dequeue vector, indicating a 100 ms time window, and extracting its relevant features, such as the **_mean_**, **_standard deviation_** and **_RMS value_**.  These relevant features were considered for evaluation mainly because they provide high-value information regarding the overall _contraction_ and _relaxation_ of the selected muscular group while being features of fast computing due to them being **statistical values**, enabling the MCU to compute the equations of each channel and extract the features without letting the next dequeue iteration to stack and lose information.

<img src="https://user-images.githubusercontent.com/82832934/160168841-5c11b237-05b2-4466-8fa3-0168c6151abf.png" alt="Myoware sensor" width="500" />
<img src="https://user-images.githubusercontent.com/82832934/160174668-21d10585-5325-4755-b5be-22385738cf40.png" alt="EMG envelope signal" width="500" />

## RNN model configuration and training

Once the signal has been successfuly registered and its relevant features extracted, the extracted features can now be assembled as an imput matrix for the proposed dynamic RNN model. The proposed model is configured as a Long-Short-Term-Memory Recurrent Neural Network (_LSTM RNN_), which is used in Deep Learning (_DL_) to track long sequences of data (such as continuous signal), and process it aided by feedback connections.

### Proposed dynamic model architecture

The proposed model is presented in the following image, which presents the interconnected layers of the dynamic model, with an input layer representing the features extracted per channel by the number of channels (_for this project: `number of features` x `number of channels`_) and an output layer representing the different possitions considered in the project (_labeled from 0 to N_). The hidden layers in the model are composed by 2 LSTM layers activated using a _tanh_ function and  containing 128 nodes each, and 2 DENSE layers, the first activated by a _tanh_ function and containing 128 nodes, while the second is activated using a _softmax_ function and containing nodes equal to the end number of classes (_in this case, 5_).

![Proposed dynamic LSTM model][Proposed LSTM model]

### Model training and configuration

In order to train the proposed model, a set of 81 dual-channel EMG signals, retrieved from 27 subjects aged 19 and 23 years of age, is used for supervised training of the model. Each signal is recorded using the _Biopac_ system, at a 1 kHz frequency, which matches the sampling rate of the project. Each signal contains each of the considered forearm positions, diferentiated by the combined behavior of the EMG channels and separated on 5-second intervals. 

![Raw EMG signal][Raw EMG sample]

Considering that the raw signal obtained in the datasets contains positive and negative voltage values based on the reference point, differing from the Myoware aquisition system, a pre-processing of the signal is needed in order to assimilate it to the Myoware signal. The sample pre-processing consists of a signal square value rectification, followed by a moving average filter. The raw signal is segmented to obtain a regular signal vectors containing only the desired raw signal label. Once the signal is segmented into separate, regular vectors, it is then processed using the method mentioned earlier.

![Segmented raw signal][Segmented raw EEG sample]
![Processed sample segment][Processed sample segment]

The processed sample is then separated in a similar dequeue fashion in order to assimilate the 100 ms window for feature extraction. The features are then arranged in a feature matrix (_m x n x l_), which contains _`m: feature values`_, _`n: number of channels`_ and _`l: target label`_. The resultant feature matrix is then scrambled, manaining the features with its correspondent label, and then applied to the model in training. The model is trained using a train/test separation rate of 70/30 and the Adam optimizer. The training of the model is determined in 100 epochs, resulting in the training chart below.

![Model training chart][Model training result by epochs]

***

# Issues and Tasks

Here is a section for possible tasks and future actions for this project, even if it is already published.

## TO DO
Here is a list of things to do in order to complete/repair issues within the app or modules that could be added or upgraded.

- [ ] Generate a live-connection to a secondary MCU and apply the control mechanism to perform an end-action
- [ ] Migrate the dynamic classifier and MCU programs to a more powerful embedded system (_eg. Teensy or Raspberry_) compatible with _TensorFlow_ or _TensorFlow Lite_
- [ ] Generate an electrode mechanism to implement EMG detection while ensuring wearability of the EMG module of the project
- [ ] Generate the schematics for the hardware modules of the project
- [ ] Upgrade the number of channels applied to the project in order to enable real-time classification

## Would be nice to...
Here is a list of upgrades that could make a better experience for the end-user, but do not affect functionality.

- [ ] Upgrade the dynamic classifier model in order to use Neural Ordinary Differential Equations (_NODE_) models, as proposed by (Chen et al., 2018)
- [ ] Generate an available database with the desired EMG signals in order to use as training set for the dynamic model
- [ ] Generate a GUI app for control settings and customization

[Myoware]: https://user-images.githubusercontent.com/82832934/160168841-5c11b237-05b2-4466-8fa3-0168c6151abf.png "Myoware connections and components"
[Mean value]: https://user-images.githubusercontent.com/82832934/160171426-c1131ffa-527a-474c-bc0f-05d8156dce3e.png "Mean value of a vector"
[STD value]: https://user-images.githubusercontent.com/82832934/160172990-38caf8ce-d9f0-47a4-9db0-a2c981fa9ae8.png "Standard Deviation Value"
[RMS value]: https://user-images.githubusercontent.com/82832934/160173774-c1b1a705-73ee-4038-a22d-9033c8a413da.png "RMS Value"
[Dequeue EMG signal]: https://user-images.githubusercontent.com/82832934/160174668-21d10585-5325-4755-b5be-22385738cf40.png "EMG envelope signal"
[Proposed LSTM model]: https://user-images.githubusercontent.com/82832934/160183041-2b0ea36b-6698-4c4f-a048-7ac1a11a37ba.png "Dynamic LSTM model"
[Raw EMG sample]: https://user-images.githubusercontent.com/82832934/160202491-41fda927-a60b-43e8-98d9-f946db0cd19d.png "Raw EMG sample from datasets"
[Segmented raw EEG sample]: https://user-images.githubusercontent.com/82832934/160207665-fc9ceffe-4d97-4828-9c51-5844adf5e561.png "Segmented raw EEG sample"
[Processed sample segment]: https://user-images.githubusercontent.com/82832934/160207811-35aac9f2-8196-4bad-9fe3-dd960281ba16.png "Processed sample segment"
[Model training result by epochs]: https://user-images.githubusercontent.com/82832934/160209351-a1c3041c-947f-47a6-a09f-54e1377b2b19.png "Model training results after 100 epochs"
