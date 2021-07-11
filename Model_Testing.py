import pandas as pd 
import tensorflow as tf 
import matplotlib as plt
import glob
import numpy as np 
from tensorflow import keras
from sklearn.utils import shuffle
import sklearn.model_selection
from sklearn.metrics import confusion_matrix, accuracy_score
STEP_SIZE = 20
SENSOR_NUM = 6

df = pd.concat([pd.read_csv(f) for f in glob.glob('./test/*.csv')], ignore_index = True)
print(df)

Label = { 'STD':0, 'WAL':1, 'JOG':2 , 'JUM':3, 'FALL':4 , 'LYI':5,'RA':6} 
class_names = { 0:'STD', 1:'WAL', 2:'JOG' , 3:'JUM', 4:'FALL', 5:'LYI',6:'RA'}

dataSet = df[["acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z", "label"]]
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


modDataset = np.array(modDataset).reshape(-1, STEP_SIZE, SENSOR_NUM)


print(modDataset)
print(modDataset.shape)
model = tf.keras.models.load_model('./model/model_4')
model.summary()

pred = model.predict(modDataset)
results = np.argmax(pred, axis=1)

count = 0
correct = 0
for i in range(len(modDataset)) :
    if class_names[y[i]] == class_names[results[i]]:
        print("prediction: ", class_names[results[i]], "    actual: ", class_names[modTruth[i]], "prediction: Correct!!!" )
        count += 1
        correct += 1
    else:
        print("prediction: ", class_names[results[i]], "    actual: ", class_names[modTruth[i]], "prediction: Wrong :( " )
        count += 1

import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score
print("success rate: ", correct/count*100)
cm = confusion_matrix(modTruth, results)
print(cm)

df_cm = pd.DataFrame(cm, index=['STD', 'WAL', 'JOG', 'JUM', 'FALL' , 'LYI','RA'], 
columns=['STD', 'WAL', 'JOG', 'JUM', 'FALL' , 'LYI','RA']) 
# plt.figure(figsize=(10,7))
sn.set(font_scale=1) # for label size
sn.heatmap(df_cm, annot=True, annot_kws={"size": 10}) # font size

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report

print(classification_report(modTruth, results, target_names=['STD', 'WAL', 'JOG', 'JUM', 'FALL' , 'LYI','RA']))


plt.show()