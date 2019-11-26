
import urllib
import os
import io,gzip
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import numpy as np
import sklearn.cluster  as skc
from sklearn import metrics
from sklearn.cluster import KMeans
import http
import http.cookiejar
import time

headers = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'),
    ('Accept-Language', 'zh-CN'),
    ('Accept', 'text/html, application/xhtml+xml, */*'),
    ('Connection', 'keep-alive')
    ]
def getOpener(cookieName=str(time.time())):
    cookie = http.cookiejar.MozillaCookieJar('data/cookies/'+cookieName+'.txt')
    try:
        cookie.load(ignore_discard=True, ignore_expires=True)
        pass
    except Exception as e:
        #print(e)
        pass
    cookieHandle = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cookieHandle)
    return (opener,cookie)


def splitImg(img): #分割验证码图片
    img=img.convert("RGB") 
    x=[]
    colors=[]
    for x1 in range(img.width):
        for x2 in range(img.height):
            (r,g,b)=img.getpixel((x1,x2))  
            if r<255 and g<255 and b<255:
                colors.append([r,g,b])
                x.append([x1,x2])
    db_color=skc.DBSCAN(min_samples=10).fit(colors)#适配数据集X,返回dbscan的实例
    labels_color=db_color.labels_#每个元素的簇序号，-1为噪音点
    
    colors_df=pd.DataFrame(colors,columns=list('rgb'))
    x_df=pd.DataFrame(x,columns=['x1','x2'])
    x_df['color_cluster']=labels_color
    db_pic=skc.DBSCAN(eps=2.5,min_samples=10).fit(x_df)#适配数据集X,返回dbscan的实例
    x_df['label']=db_pic.labels_
    nCluster_list=[]
    print(set(x_df['color_cluster']))
    for i in set(x_df['color_cluster']):
        d=x_df[x_df['color_cluster']==i]
        c=skc.DBSCAN(eps=2.5,min_samples=1).fit(d[['x1','x2']])
        nCluster_list.append(len(set(c.labels_)))
    noisy=nCluster_list.index(max(nCluster_list))
    
    imgs=[]
    for k in set(x_df['color_cluster']):
        if k!=noisy:
            df=x_df[x_df['color_cluster']==k]
            #im=Image.new('RGB',(img.width/4,img.height),(255,255,255))
            im=Image.new('RGB',(df['x1'].max()-df['x1'].min()+7,df['x2'].max()-df['x2'].min()+7),(255,255,255))
            for i in range(len(df)):
                try:
                    im.putpixel((df.iloc[i]['x1']-df['x1'].min()+3,df.iloc[i]['x2']-df['x2'].min()+3),(0,0,0))
                except Exception as e:
                    return False
            imgs.append(im)
    return imgs

def getCaptcha(opener,cookie,url='https://cmcoins.boc.cn/CoinSeller/ImageValidation/validation1512712177016.gif'):#获取验证码，返回图片
    opener.addheaders = headers
    try:
        response = opener.open(url,timeout=5)
        print(response)
        cookie.save(ignore_discard=True, ignore_expires=True)
        responseData = response.read()
        data_stream = io.BytesIO(responseData)  
        img=Image.open(data_stream)
    except Exception as e:
        print( e)
        return False
    return img
#验证码获取

for i in range(3):
    try:
        opener,cookie=getOpener()
        img=getCaptcha(opener,cookie)
        imgs =splitImg(img)
        for j,im in enumerate(imgs):
            name=str(time.time())[-12:-1]
            im.save('data/captcha/img_'+name+'_.png')
#             plt.subplot(1,6,j+1)
#             plt.imshow(im)
#         plt.show()
        time.sleep(1)
    except:
        time.sleep(1)
