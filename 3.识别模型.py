from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score  
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import Callback
from tensorflow.keras import regularizers
from sklearn.metrics import confusion_matrix
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
import os
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import time
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Convolution1D,MaxPooling1D,Activation,Flatten,Dropout

one_hot_list=['2', '3', '4', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
       'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'T', 'U', 'V', 'W', 'X',
       'Y', 'Z']


FILE_PATH="model2.h5"#模型进行存储和读取的地方
IMAGE_SIZE=30
# imgs,labels,counter=read_file(PATH,IMAGE_SIZE)
dataset=pd.read_hdf('./data/train.h5',key='train')
dataset_x=dataset.iloc[:,0:900].values
dataset_x=dataset_x.reshape(dataset_x.shape[0],IMAGE_SIZE,IMAGE_SIZE)/255.0
dataset_y=pd.get_dummies(dataset.iloc[:,900]).values
x_train,x_test,y_train,y_test=train_test_split(dataset_x,dataset_y,test_size=0.2,random_state=0)
model=Sequential()
model.add(Convolution1D(filters=32,kernel_size=3,padding='same',input_shape=x_train.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=2,strides=2,padding='same'))
model.add(Convolution1D(filters=64,kernel_size=3,padding='same'))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=2,strides=2,padding='same'))
model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(dataset_y.shape[1]))
model.add(Activation('softmax'))
model.summary()
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
model.fit(x_train,y_train,epochs=20,batch_size=16)
loss,accuracy=model.evaluate(x_test,y_test)
print('testloss:',loss)
print('testaccuracy:',accuracy)
model.save(FILE_PATH)

