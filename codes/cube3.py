# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 19:07:05 2019

@author: prateekspawar
"""

import numpy as np
import cv2
import openpyscad as ops
def detect(c):
    perimeter = cv2.arcLength(c,True)
    area = cv2.contourArea(c)
    if (abs(perimeter*perimeter/area-4*np.pi)<50):
        shape = "circle"
		# return the name of the shape
    return shape
def vertices( threshf ):
    contours, hierarchy = cv2.findContours(threshf,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(threshf,contours,1,(0,255,0),3)
#    print((contours[1]))
    circle=[]
    for i in range(1,len(contours)):
        if(detect(contours[i])=="circle"):
            circle.append(contours[i])
    circlef=[]
    M=[]
    cx=[]
    cy=[]
    area=[]
    for i in range(0,len(circle)):
        circlef.append([])
        M = cv2.moments(circle[i])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        area = cv2.contourArea(circle[i])
        circlef[i].append(cx)
        circlef[i].append(cy)
        circlef[i].append(area)
    
    i=0;j=0;k=0
    while(i<len(contours)):
        while(j<len(contours[i])):
            while(k<len(contours[i])):
                clist=contours[i].tolist()
                if(j!=k and abs(clist[j][0][0]-clist[k][0][0])<5 and abs(clist[j][0][1]-clist[k][0][1])<5):
                    clist[j][0][0]=(clist[j][0][0]+clist[k][0][0])/2
                    clist[j][0][1]=(clist[j][0][1]+clist[k][0][1])/2
                    clist.pop(k)
                    contours[i]=np.asarray(clist)
                    k=k-1
                k=k+1
            j=j+1;k=0
        i=i+1;j=0
#    print((contours[1]))               
                    
        
        
    block=[]
    
  
    for i in range(1,len(contours)):
        
        if( len(contours[i])==4): 
            block.append(contours[i])
        
                
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
    
#    print("one")  
    i=0;l=0
    while(i<len(vertexf)):
        while(l<len(vertexf)):
            a=0;b=0;c=0;d=0
            if(i!=l):         
                for j in range(0,4):
                    if(vertexf[i][0]==vertexf[l][j]):
                        a=1
                    if(vertexf[i][1]==vertexf[l][j]):
                        b=1
                    if(vertexf[i][2]==vertexf[l][j]):
                        c=1
                    if(vertexf[i][3]==vertexf[l][j]):
                        d=1
            if(a==1 and b==1 and c==1 and d==1):
                vertexf.pop(l)
                l=l-1
            l=l+1
        i=i+1;l=0
                    
                    
                        
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

img=cv2.imread('codes\drawings\cube3.jpg')

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
                cuboid[u].append(i);cuboid[u].append(j);cuboid[u].append(k)
                if(u==0):
                    cuboid[u].append('a')
                else:
                    cuboid[u].append('a')
                    i=0
                    h=0
                    while(i<u):
                        a=cuboid[u][6];b=cuboid[u][7];c=cuboid[u][8]
                        x=cuboid[i][6];y=cuboid[i][7];z=cuboid[i][8]
                        print("a=",a,"b=",b,"c=",c,"x=",x,"y=",y,"z=",z)
                        for j in range(0,4):
#                            print("j=",j,(vertexf[a][j][0]-yfsa1[x])*(vertexf[a][j][0]-yfsa2[x]),(vertexf[a][j][1]-xfsa1[x])*(vertexf[a][j][1]-xfsa2[x]))
                            if(((vertexf[a][j][0]-yfsa1[x])*(vertexf[a][j][0]-yfsa2[x])<=0) and ((vertexf[a][j][1]-xfsa1[x])*(vertexf[a][j][1]-xfsa2[x])<=0)\
                               and ((vertext[b][j][0]-ytsa1[y])*(vertext[b][j][0]-ytsa2[y])<=0) and ((vertext[b][j][1]-xtsa1[y])*(vertext[b][j][1]-xtsa2[y])<=0) \
                               and ((vertexs[c][j][0]-yssa1[z])*(vertexs[c][j][0]-yssa2[z])<=0) and ((vertexs[c][j][1]-xssa1[z])*(vertexs[c][j][1]-xssa2[z])<=0)):
                                h=1
                            else:
                                h=0
                        if(h==1):
                            cuboid[u][9]='d'
                            break
                        i=i+1
                                
                    
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
    if(cuboid[i][9]=='a'):
        ct=ct+c1
    if(cuboid[i][9]=='d'):
        ct=ct-c1
ct.write("cube3.scad")
#cv2.imshow('front',threshf)
#cv2.imshow('side',threshs)
cv2.waitKey(0)
cv2.destroyAllWindows()

