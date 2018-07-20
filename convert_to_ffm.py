# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 18:03:59 2018

@author: wk.wu
"""
import pandas as pd

def convert_to_ffm(df,type,numerics,categories,muti_cat,features,sep):
    currentcode=len(numerics)
    catdict={}
    catcodes={}#记录类别特征的feat_index
    for x in numerics:#前currentcode个表示的是连续特征
        catdict[x]=0
    for x in categories:
        catdict[x]=1
    for x in muti_cat:
        catdict[x]=2
    nrows=df.shape[0]
    with open(str(type)+"_ffm.txt","w") as text_file:
        for n,r in enumerate(range(nrows)):
            datastring=""
            datarow=df.iloc[r].to_dict()#将第r条样本转换成dict，{'a':1,'b':2}
            datastring+=str(int(datarow['label']))#添加label
            for i,x in enumerate(catdict.keys()):#catdict记录特征是否为类别特征，i为特征的field_index,更具前面的
                if(catdict[x]==0):#连续特征
                    if datarow[x]==-1:
                        continue
                    datastring=datastring+' '+'{}:{}:{}'.format(i,i,datarow[x])
                elif catdict[x]==1:#类别特征
                    if datarow[x]==-1:
                        continue
                    if(x not in catcodes):#x特征第一次出现
                        catcodes[x]={}
                        catcodes[x][datarow[x]]=currentcode
                        currentcode+=1
                    elif datarow[x] not in catcodes[x]:
                        catcodes[x][datarow[x]]=currentcode
                        currentcode+=1
                    code=catcodes[x][datarow[x]]
                    datastring=datastring+' '+'{}:{}:{}'.format(i,code,1)
                    #datastring=datastring+" "+str(i)+":"+str(int(code))+":1"
                else:#多值离散特征的处理
                    if datarow[x]==-1:
                        continue
                    s=datarow[x].split(sep)
                    for ss in s:
                        if x not in catcodes:
                            catcodes[x]={}
                        if ss not in catcodes[x]:
                            catcodes[x][ss]=currentcode
                            currentcode+=1
                        code=catcodes[x][ss]
                        datastring=datastring+' '+'{}:{}:{}'.format(i,code,1)
            datastring+='\n'
            text_file.write(datastring)
