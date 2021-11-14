#importPackages

import os
import cv2
import glob
import logging
import numpy as np 
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

logging.info(f'Modules Imported')

#Model Training Function

def modelTraining(trainDir,testDir,project):

    #width,height size
    size = 224

    #Stored Training Data into List
    
    trainData = []
    trainLabels = []

    for per in os.listdir(trainDir+'/'):
        for data in glob.glob(trainDir+'/'+per+'/*.*'):
            img = cv2.imread(data)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (size,size))
            trainData.append([img])
            if per[-1]=='g':
                trainLabels.append(np.array(1))
            else:
                trainLabels.append(np.array(0))

    trainData = np.array(trainData)/255.0
    trainLabels = np.array(trainLabels)
    
    logging.info(f'Stored Training Data into List')

    #Stored Testing Data into List

    testData = []
    testLabels = []

    for per in os.listdir(testDir+'/'):  
        for data in glob.glob(testDir+'/'+per+'/*.*'):
            img = cv2.imread(data)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (size,size))
            testData.append([img])
            if per[-1]=='g':
                testLabels.append(np.array(1))
            else:
                testLabels.append(np.array(0))

    testData = np.array(testData)/255.0
    testLabels = np.array(testLabels)

    logging.info(f'Stored Testing Data into List')
 
    #Convert to Categorical features

    from tensorflow.keras.utils import to_categorical
    trainLabels = to_categorical(trainLabels)

    logging.info(f'Converted Categorical features')

    #Reshaping_data

    trainData = trainData.reshape(-1, size,size, 3)
    testData = testData.reshape(-1, size,size, 3)

    #Shuffle the data

    from sklearn.utils import shuffle
    trainData,trainLabels = shuffle(trainData,trainLabels)
    testData,testLabels = shuffle(testData,testLabels)

    #Transfer learning VGG16 Algorithm implementation
    
    logging.info(f'Transfer learning VGG16 Algorithm implementation')

    import tensorflow 
    from tensorflow import keras
    from keras import optimizers
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.applications.vgg16 import VGG16
    from tensorflow.keras.layers import Dropout, Flatten, Dense
    from tensorflow.keras.models import Sequential, Model, load_model
    
    base_model =VGG16(weights='imagenet', include_top=False, input_shape=(224,224,3))
    base_model.summary()

    add_model = Sequential()
    add_model.add(Flatten(input_shape=base_model.output_shape[1:]))
    add_model.add(Dense(256, activation='relu'))
    add_model.add(Dense(2, activation='softmax'))

    model = Model(inputs=base_model.input, outputs=add_model(base_model.output))

    model.compile(loss='binary_crossentropy', optimizer=Adam(lr=1e-4),
                metrics=['accuracy'])
    model.summary()

    #Traning Process

    from keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping, ReduceLROnPlateau, TensorBoard

    earlyStopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=3,verbose=1)

    earlyStop=[earlyStopping]

    epoch = 20

    batchSize = 64
    
    history = model.fit(trainData,trainLabels, batch_size=batchSize,epochs=epoch, callbacks=earlyStop,validation_split=.3)

    #Save the Model
    modelFile = "signVerifyModel.h5"
    model.save(modelFile)

    logging.info(f'VGG Model Saved into h5')

    logging.info(f'Training Session Completed')

    return modelFile
