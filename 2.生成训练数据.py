import pandas as pd
import os
import re
from PIL import Image
import numpy as np
li=[]
for dirpath,dirname,filenames in os.walk('data/dataset/'):
    if len(filenames)==0:
        continue
    for filename in filenames:
        if len(re.findall('\.png$',filename))==1:
            filepath=dirpath+filename
            img=Image.open(filepath)
            im=img.resize((30,30))
            pix=np.asarray(im)[:,:,0]
            pix_30=pix.flatten()
            li.append(pix_30.tolist()+[filename[-5]])
            
df=pd.DataFrame(li)
df.to_hdf('./data/train.h5',key='train')