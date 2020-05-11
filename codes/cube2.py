# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 19:07:05 2019

@author: prateekspawar
"""

import numpy as np
import cv2
import openpyscad as ops
def detect(c):
    shape=[]
    approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
    
    if ((len(approx) > 10)):
        shape = "circle"
		# return the name of the shape
    return shape
def vertices( threshf ):
    contours, hierarchy = cv2.findContours(threshf,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(threshf,contours,-1,(0,255,0),3)
    
    block=[]
    circle=[]
    for i in range(1,len(contours)):
        if( detect(contours[i])!="circle" and len(contours[i])==4): 
            block.append(contours[i])
        if(detect(contours[i])=="circle"):
            circle.append(contours[i])
                
    vertexf=[]
 
    for i in range(0,len(block)):
        vertexf.append([])
        for j in range(0,4):
            vertexf[i].append([])
            vertexf[i][j].append(block[i][j][0][0])
            vertexf[i][j].append(block[i][j][0][1])
#    print("vertexes",vertexf)
    for i in range(0,len(vertexf)):
        for l in range(0,len(vertexf)):
                     
            for j in range(0,len(vertexf[i])):
                for k in range(0,len(vertexf[i])):
                    
                    if( abs(vertexf[i][j][0]-vertexf[l][k][0])<=5):
                        vertexf[i][j][0]=vertexf[l][k][0]=(vertexf[i][j][0]+vertexf[l][k][0])/2
                    if( abs(vertexf[i][j][1]-vertexf[l][k][1])<=5):
                        vertexf[i][j][1]=vertexf[l][k][1]=(vertexf[i][j][1]+vertexf[l][k][1])/2
    circlef=[]
    M=[]
    cx=[]
    cy=[]
    area=[]
    for i in range(0,len(circle)):
        circlef.append([])
        M[i] = cv2.moments(circle[i])
        cx[i] = int(M[i]['m10']/M[i]['m00'])
        cy[i] = int(M[i]['m01']/M[i]['m00'])
        area[i] = cv2.contourArea(circle[i])
        circlef[i].append(cx[i])
        circlef[i].append(cy[i])
        circlef[i].append(area[i])
        
    return(vertexf,circlef)
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

img=cv2.imread('drawings/cube2.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,127,255,0)
h,w=thresh.shape
threshf=thresh[0:int(h/2),0:int(w/2)]
thresht=thresh[int(h/2):h,0:int(w/2)]
threshs=thresh[0:int(h/2),int(w/2):w]
vertexf,circlef=vertices(threshf)
vertext,circlet=vertices(thresht)
vertexs,circles=vertices(threshs)
print("front",vertexf)
print("Top",vertext)
print("Side",vertexs) 
xdifff=[];ydifff=[];xdifft=[];ydifft=[];xdiffs=[];ydiffs=[]

for i in range(0,len(vertexf)):
    xdifff.append([])
    ydifff.append([])
    xdifff[i],ydifff[i]=diff(vertexf[i])
for i in range(0,len(vertext)):
    xdifft.append([])
    ydifft.append([])
    xdifft[i],ydifft[i]=diff(vertext[i])   
for i in range(0,len(vertexs)):
    xdiffs.append([])
    ydiffs.append([])
    xdiffs[i],ydiffs[i]=diff(vertexs[i])
#print("front",xdifff,ydifff)
#print("top",xdifft,ydifft)
#print("side",xdiffs,ydiffs)

xfsa1=[];xfsa2=[];yfsa1=[];yfsa2=[]

for i  in range(0,len(vertexf)):
    xfsa1.append([])
    xfsa2.append([])
    c=0
    for j in range(1,4):
        if(vertexf[i][0][0]==vertexf[i][j][0]):
            if((j==1 and vertexf[i][2][0]==vertexf[i][3][0]) or (j==2 and vertexf[i][1][0]==vertexf[i][3][0]) or (j==3 and vertexf[i][1][0]==vertexf[i][2][0])):
                c=1
                break
    if(c==1):
        xfsa1[i]=vertexf[i][0][1]
        xfsa2[i]=vertexf[i][j][1]
    else:
         xfsa1[i]=-1
         xfsa2[i]=-1
        
for i  in range(0,len(vertexf)):
    yfsa1.append([])
    yfsa2.append([])
    c=0
    for j in range(1,4):
        if(vertexf[i][0][1]==vertexf[i][j][1]):
            if((j==1 and vertexf[i][2][1]==vertexf[i][3][1]) or (j==2 and vertexf[i][1][1]==vertexf[i][3][1]) or (j==3 and vertexf[i][1][1]==vertexf[i][2][1])):
                c=1
                break
    if(c==1):
        yfsa1[i]=vertexf[i][0][0]
        yfsa2[i]=vertexf[i][j][0]
    else:
         yfsa1[i]=-1
         yfsa2[i]=-1
xtsa1=[];xtsa2=[];ytsa1=[];ytsa2=[]
for i  in range(0,len(vertext)):
    xtsa1.append([])
    xtsa2.append([])
    c=0
    for j in range(1,4):
        if(vertext[i][0][0]==vertext[i][j][0]):
            if((j==1 and vertext[i][2][0]==vertext[i][3][0]) or (j==2 and vertext[i][1][0]==vertext[i][3][0]) or (j==3 and vertext[i][1][0]==vertext[i][2][0])):
                c=1
                break
    if(c==1):
        xtsa1[i]=vertext[i][0][1]
        xtsa2[i]=vertext[i][j][1]
    else:
         xtsa1[i]=-1
         xtsa2[i]=-1
            
                
for i  in range(0,len(vertext)):
    ytsa1.append([])
    ytsa2.append([])
    c=0
    for j in range(1,4):
        if(vertext[i][0][1]==vertext[i][j][1]):
            if((j==1 and vertext[i][2][1]==vertext[i][3][1]) or (j==2 and vertext[i][1][1]==vertext[i][3][1]) or (j==3 and vertext[i][1][1]==vertext[i][2][1])):
                c=1
                break
    if(c==1):
        ytsa1[i]=vertext[i][0][0]
        ytsa2[i]=vertext[i][j][0]
    else:
         ytsa1[i]=-1
         ytsa2[i]=-1 
         
xssa1=[];xssa2=[];yssa1=[];yssa2=[]
for i  in range(0,len(vertexs)):
    xssa1.append([])
    xssa2.append([])
    c=0
    for j in range(1,4):
        if(vertexs[i][0][0]==vertexs[i][j][0]):
            if((j==1 and vertexs[i][2][0]==vertexs[i][3][0]) or (j==2 and vertexs[i][1][0]==vertexs[i][3][0]) or (j==3 and vertexs[i][1][0]==vertexs[i][2][0])):
                c=1
                break
    if(c==1):
        xssa1[i]=vertexs[i][0][1]
        xssa2[i]=vertexs[i][j][1]
    else:
         xssa1[i]=-1
         xssa2[i]=-1
            
                
for i  in range(0,len(vertexs)):
    yssa1.append([])
    yssa2.append([])
    c=0
    for j in range(1,4):
        if(vertexs[i][0][1]==vertexs[i][j][1]):
            if((j==1 and vertexs[i][2][1]==vertexs[i][3][1]) or (j==2 and vertexs[i][1][1]==vertexs[i][3][1]) or (j==3 and vertexs[i][1][1]==vertexs[i][2][1])):
                c=1
                break
    if(c==1):
        yssa1[i]=vertexs[i][0][0]
        yssa2[i]=vertexs[i][j][0]
    else:
         yssa1[i]=-1
         yssa2[i]=-1 
         
#print("xfsa1",xfsa1,"xfsa2",xfsa2)
#print("yfsa1",yfsa1,"yfsa2",yfsa2)      
#print("xtsa1",xtsa1,"xtsa2",xtsa2)
#print("ytsa1",ytsa1,"ytsa2",ytsa2) 
#print("xssa1",xssa1,"xssa2",xssa2)
#print("yssa1",yssa1,"yssa2",yssa2)     
cuboid=[]
u=0
for i in range(0,len(vertexf)):
    for j in range(0,len(vertext)):
        for k in range(0,len(vertexs)):

            if(((abs(xfsa1[i]-xssa1[k])<5 and abs(xfsa2[i]-xssa2[k])<5) or (abs(xfsa1[i]-xssa2[k])<5 and abs(xfsa2[i]-xssa1[k])<5)) and \
               ((abs(yfsa1[i]-ytsa1[j])<5 and abs(yfsa2[i]-ytsa2[j])<5) or (abs(yfsa1[i]-ytsa2[j])<5 and abs(yfsa2[i]-ytsa1[j])<5))): 
               
                cuboid.append([])
                print("i=",i,"j=",j,"k=",k)
                l=(xdifff[i][0]+xdifft[j][0])/2
                b=(ydifff[i][0]+ydiffs[k][0])/2
                h=(ydifft[j][0]+xdiffs[k][0])/2
                cuboid[u].append(l);cuboid[u].append(b);cuboid[u].append(h)
                cx=[];cy=[];cz=[]
                
                
#                print(l,b,h)
                if(yfsa1[i]>yfsa2[i]):
                    
                    cx=(yfsa2[i])+l/2
                else:
                    cx=(yfsa1[i])+l/2
                if(xfsa1[i]>xfsa2[i]):
                    cy=int(xfsa2[i])+b/2
                else:
                    cy=int(xfsa1[i])+b/2   
                if(xtsa1[j]>xtsa2[j]):
                    cz=int(xtsa2[j])+h/2
                else:
                    cz=int(xtsa1[j])+h/2  
                cuboid[u].append(cx);cuboid[u].append(cy);cuboid[u].append(cz)
                u=u+1

i=0;j=0
while(i<len(cuboid)):
    while(j<len(cuboid)):
#        print("i is:",i,"j is:",j)
        if(i!=j and cuboid[i]==cuboid[j]):
            cuboid.pop(j)
#            print(j,"is popped")
            j=j-1
        
        j=j+1
    i=i+1
    j=0
print(cuboid)  



ct=ops.Cube([0,0,0])
for i in range(0,len(cuboid)):
   
    l=cuboid[i][0];b=cuboid[i][1];h=cuboid[i][2]
    cgx=cuboid[i][3];cgy=cuboid[i][4];cgz=cuboid[i][5]
    c1 = ops.Cube([l,h,b]).translate([-l/2,-h/2,-b/2]).translate([cgx,cgz,-cgy])  
    
    ct=ct+c1
ct.write("cube2.scad")

cv2.waitKey(0)
cv2.destroyAllWindows()

