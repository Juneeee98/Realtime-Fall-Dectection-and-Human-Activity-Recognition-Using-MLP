import pandas as pd 
import tensorflow as tf 
import matplotlib as plt
import glob
import numpy as np 
from tensorflow import keras
from keras import Sequential
from sklearn.utils import shuffle
import sklearn.model_selection


STEP_SIZE = 20
SENSOR_NUM = 6
NUM_CLASSESS = 7

df = pd.concat([pd.read_csv(f) for f in glob.glob('./train_new/*.csv')], ignore_index = True)
print(df)

Label = { 'STD':0, 'WAL':1, 'JOG':2 , 'JUM':3, 'FALL':4 , 'LYI':5,'RA':6} 
class_names = { 0:'STD', 1:'WAL', 2:'JOG' , 3:'JUM', 4:'FALL', 5:'LYI',6:'RA'}

dataSet = df[["acc_x", "acc_y", "acc_z", "gyro_x","gyro_y","gyro_z",  "label"]]

dataSet.label = [Label[item] for item in dataSet.label]


print(dataSet)

x = np.array(dataSet.drop(["label"],1))
y = np.array(dataSet["label"])

modDataset = []
modTruth =[]

for i in range(len(x)-STEP_SIZE):
    temp = []
    for j in range(i, i+STEP_SIZE):
        temp.append(x[j])
    modDataset.append(temp)

for i in range(len(y)-STEP_SIZE):
    temp = []
    for j in range(i, i+STEP_SIZE):
        temp.append(y[j])
    
    most_common_item = max(temp, key = temp.count)

    modTruth.append(most_common_item)

print(len(modDataset))
print(len(modTruth))

print(len(modDataset[0]))
print(modDataset[1])

modDataset = np.array(modDataset).reshape(-1, STEP_SIZE, SENSOR_NUM)

print(modDataset)



y = np.array(modTruth)
x = modDataset

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x,y,test_size = 0.3)

print(x_train)
print(y_train)

model = Sequential()
model.add(keras.layers.Flatten(input_shape=(STEP_SIZE, SENSOR_NUM)))
model.add(keras.layers.Dense(128, activation='relu'))
model.add(keras.layers.Dropout(0.3))
model.add(keras.layers.Dense(128, activation='relu'))
model.add(keras.layers.Dropout(0.3))
model.add(keras.layers.Dense(NUM_CLASSESS, activation='softmax'))   

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]) 
model.summary()

model.fit(x_train,y_train, epochs=30, validation_split =0.1)

model.save('./model_x/')

pred = model.predict(x_test)
results = np.argmax(pred, axis=1)

for i in range(50) :
    if class_names[y_test[i]] == class_names[results[i]]:
        print("prediction: ", class_names[results[i]], "    actual: ", class_names[y_test[i]], "prediction: Correct!!!" )
    else:
        print("prediction: ", class_names[results[i]], "    actual: ", class_names[y_test[i]], "prediction: Wrong :( " )