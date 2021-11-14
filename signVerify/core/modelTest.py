#importPackages

import os
import cv2
import glob
import logging
import numpy as np 
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

logging.info(f'Modules Imported')

#Model Testing Function

def modelTesting(inputFile,modelName,Project):
    
    logging.info(f'Model Evaluation Started')

    #width,height size
    size = 224

    #Image Preprocess

    img = cv2.imread(str(inputFile))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (size,size))

    test= np.array(img)/255.0
    test= test.reshape(-1, size,size, 3)

    # load and evaluate a saved model

    from keras.models import load_model
    
    logging.info(f'load and evaluate a saved model')

    # load model
    models = load_model(str(modelName))

    # summarize model.
    models.summary()

    #Prediction

    predictions = models.predict(test)

    listOutputAcc = predictions.tolist()

    #Accuracy Score

    accuracy = max(listOutputAcc[0])*100

    listOutput = predictions.round().tolist()
    output=listOutput[0]

    out=[]
    if output==[1.0, 0.0]:
        out.append("Genuine")

    elif output==[0.0, 1.0]:
        out.append("Forged")

    verification=out[0]

    return [verification, accuracy]
