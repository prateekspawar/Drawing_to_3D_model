# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 19:07:05 2019

@author: prateekspawar
"""

import numpy as np
import cv2
import openpyscad as ops
def vertices( threshf ):
    minLineLength = 30
    maxLineGap = 5
    edgesf = cv2.Canny(threshf,50,150,apertureSize = 3)
    linesf = cv2.HoughLinesP(edgesf,1,np.pi/180,100,minLineLength,maxLineGap)
    print(len(linesf))
    vertexf=[]
    
    for i in range (0,len(linesf)):
        for x1,y1,x2,y2 in linesf[i]:
            vertexf.append([x1,y1])
            vertexf.append([x2,y2])
#    print(vertexf)
    i=0
    j=0
    while(i<len(vertexf)):
        while(j<len(vertexf)):
    #        print("i=",i,"j=",j)
            if (i!=j):
                if((abs(vertexf[i][0]-vertexf[j][0])<=5)and(abs(vertexf[i][1]-vertexf[j][1])<=5)):
                    x=(vertexf[i][0]+vertexf[j][0])/2
                    y=(vertexf[i][1]+vertexf[j][1])/2
                    vertexf[i][0]=x
                    vertexf[i][1]=y
                    vertexf.pop(j)
            j=j+1  
        i=i+1
        j=0
#    print(vertexf)   
    vertexfs=[]
    for i in range(0,len(vertexf)):
        vertexfs.append(vertexf[i][0])
        vertexfs.append(vertexf[i][1])
#    print(vertexfs)            
    i=0
    j=0
    while(i<len(vertexfs)):
        while(j<len(vertexfs)):
    #        print("i=",i,"j=",j)
            if(abs(vertexfs[i]-vertexfs[j])<=5):
                vertexfs[i]=vertexfs[j]=(vertexfs[i]+vertexfs[j])/2
            j=j+1
        i=i+1
        j=0
#    print(vertexfs) 
    i=0
    j=0
    while(i<len(vertexfs)):
        while(j<len(vertexfs)):
    #        print("i=",i,"j=",j)
            if(abs(vertexfs[i]-vertexfs[j])<=5):
                vertexfs[i]=vertexfs[j]=(vertexfs[i]+vertexfs[j])/2
            j=j+1
        i=i+1
        j=0
#    print(vertexfs) 
    i=0
    j=0
    while(i<len(vertexfs)):
        while(j<len(vertexfs)):
    #        print("i=",i,"j=",j)
            if(abs(vertexfs[i]-vertexfs[j])<=5):
                vertexfs[i]=vertexfs[j]=(vertexfs[i]+vertexfs[j])/2
            j=j+1
        i=i+1
        j=0
#    print(vertexfs)        
    for i in range(0,len(vertexfs)):
        vertexfs[i]=round(vertexfs[i])
#    print(vertexfs)    
    for i in range(0,len(vertexf)):
        vertexf[i][0]=vertexfs[i*2]
        vertexf[i][1]=vertexfs[i*2+1]
#    print(vertexf)  
    return(vertexf)
    
def diff(vertex):
#    print("in diff")
    xdiff=[]
    ydiff=[]
    for i in range(0,len(vertex)):
        j=0
        for j in range(0,len(vertex)):
            if(vertex[i][0]-vertex[j][0]!=0):
               xdiff.append(abs(vertex[i][0]-vertex[j][0]))
            if(vertex[i][1]-vertex[j][1]!=0):
                ydiff.append(abs(vertex[i][1]-vertex[j][1]))
#    print(xdiff)
#    print(ydiff)
    i=0            
    while(i<len(xdiff)):
        j=0
        while(j<len(xdiff)):
            if(i!=j):
                if(xdiff[i]==xdiff[j]):
                    xdiff.pop(j)
#                    print(j,"is poped")
                    j=j-1
                    
            j=j+1
        i=i+1
    i=0            
    while(i<len(ydiff)):
        j=0
        while(j<len(ydiff)):
            if(i!=j):
                if(ydiff[i]==ydiff[j]):
                    ydiff.pop(j)
                    j=j-1
            j=j+1
        i=i+1
#    print(xdiff)
#    print(ydiff)
    return(xdiff,ydiff)

img=cv2.imread('drawings/cube1.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,127,255,0)
h,w=thresh.shape
threshf=thresh[0:int(h/2),0:int(w/2)]
thresht=thresh[int(h/2):h,0:int(w/2)]
threshs=thresh[0:int(h/2),int(w/2):w]

vertexf=vertices(threshf)
vertext=vertices(thresht)
vertexs=vertices(threshs)
print("front",vertexf)
print("Top",vertext)
print("Side",vertexs)    
xdifff,ydifff=diff(vertexf)
xdifft,ydifft=diff(vertext)
xdiffs,ydiffs=diff(vertexs)
print("front",xdifff,ydifff)
print("top",xdifft,ydifft)
print("side",xdiffs,ydiffs)
if((len(xdifff)==1)and(len(ydifff)==1)and(len(xdifft)==1)and(len(ydifft)==1)and(len(xdiffs)==1)and(len(ydiffs)==1)):
    print("one body")
    if(abs(xdifff[0]-xdifft[0])<5 and abs(ydifff[0]-ydiffs[0])<5 and abs(ydifft[0]-xdiffs[0])<5):
        
        l=abs((xdifff[0]+xdifft[0])/2)
        b=abs(ydifff[0]+ydiffs[0])/2
        h=abs(ydifft[0]+xdiffs[0])/2
        print("Cuboid","l=",l,"b=",b,"h=",h)
        vertexa=[]
        for i in range(0,len(vertexf)):
            vertexa.append(vertexf[i][:])
            vertexa.append(vertexf[i][:])
#        print(vertexa)
#        print(vertexf)
        i=0
        while(i<len(vertexf)):
           vertexa[i*2].append(vertexs[2][0])
           vertexa[i*2+1].append(vertexs[0][0])
           i=i+1
        print(vertexa)
        cgx=vertexa[0][0]+l/2
        cgy=vertexa[0][1]-b/2
        cgz=vertexa[0][2]-h/2
        print("cgx=",cgx,"cgy=",cgy,"cgz=",cgz)
        c1 = ops.Cube([l, b, h])    
        c1.translate([cgx,cgy,cgz])
        (c1).write("cube1.scad")
    
#
#cv2.imshow('front',threshf)
#cv2.imshow('top',thresht)
#cv2.imshow('side',threshs)
cv2.waitKey(0)
cv2.destroyAllWindows()

