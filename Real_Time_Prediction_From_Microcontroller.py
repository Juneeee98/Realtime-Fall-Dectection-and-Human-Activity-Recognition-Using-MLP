import socket
import msvcrt
import csv
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


Label = { 'STD':0, 'WAL':1, 'JOG':2 , 'JUM':3, 'FALL':4 , 'LYI':5,'RA':6} #, 'JUM':3, 'LYI':4, 'FOL':5, 'FKL':5, 'BSC':5, 'SDL':5, 'STU':6, 'STN':7, 'SCH':8, 'SIT':9, 'CHU':10, 'CSI':11, 'CSO':12}
class_names = { 0:'STD', 1:'WAL', 2:'JOG' , 3:'JUM', 4:'FALL', 5:'LYI',6:'RA'}#, 3:'JUM', 4:'LYI', 5:'Falling', 6:'STU', 7:'STN', 8:'SCH', 9:'SIT', 10:'CHU', 11:'CSI', 12:'CSO'}

inputSensor = []
model = tf.keras.models.load_model('./model_4/')

model.summary()


l = []
packet = []
p = ""
tp = []
s = socket.socket()         
 
s.bind(('0.0.0.0', 80 ))
s.listen(0)    
i = 0      

record = input("Press R to start recording...")
if record == 'r' :
        

    # while True:
    
    client, addr = s.accept()
    #     x = kbfunc()

    carry = ''   
    try:
        while True:
            content = client.recv(1)
            

            if len(content) ==0:
                # print("heree?")
                break

            else:
                #print(len(content))
              
                temp = ''
                content = content.decode("utf-8")

                if content == '!':
                    
                    tp =[]
                    p = ''

                
                elif content == '@':
                    tp.append(float(p))
                    # print(type(tp[0]))
                    p = ''
                    inputSensor.append(tp)
                    if len(inputSensor) > STEP_SIZE:
                        inputSensor.pop(0)
                    if len(inputSensor) == STEP_SIZE:
                        temp = np.array(inputSensor).reshape(-1, STEP_SIZE, SENSOR_NUM)
                        #print(temp)
                        pred = model.predict(temp)
                        results = np.argmax(pred, axis=1)
                        print("prediction: ", class_names[results[i]])
                        # inputSensor = []
                    


                elif content ==',':
                    p = float(p)
                    p = p
                    tp.append(p)
                    p = ''

                else:
                    p += content

    except KeyboardInterrupt:
        pass   
    
 
