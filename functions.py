import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import mplstereonet

def get_datatype(S1,S2,S3,fault_regime):
    if fault_regime=="Normal Faulting":
      m=np.array([[S3, 0, 0],[0, S2, 0],[0, 0, S1]])
    elif fault_regime=="Thrust Faulting":
      m=np.array([[S2, 0, 0],[0, S1, 0],[0, 0, S3]])
    else:
      m=np.array([[S3, 0, 0],[0, S1, 0],[0, 0, S2]])
    return m

def get_allfaults(S1,S2,S3,w,Pp,C,fa,m):
    pp=math.pi
    cc=(pp/180)
    n1=31
    n2=121
    n3=n1*n2
    k=0
    azk=[0]*n2
    dipz=[0]*n1
    dx=[0]*n3
    dy=[0]*n3
    strk=[0]*n3
    dip=[0]*n3
    X1=[0]*n3
    SS1=[0]*n3
    NN1=[0]*n3
    ff=math.tan(cc*fa)

    for j in range(0,n2):
        azk[j]=cc*(3*j+90)
        for i in range(0,n1):
           dipz[i]=(pp/2)-cc*3*i
           az=(pp/2)-azk[j]
           if az<0:
                az=2*pp+az
           else:
                az=(pp/2)-azk[j]
           radius=math.sqrt(2)*math.cos((pp/4)+(dipz[i]/2))
           dx[k]=radius*math.cos(az)
           dy[k]=radius*math.sin(az)
           strk[k]=3*j
           dip[k]=3*i 
           R=np.array([[math.cos(cc*w), math.sin(cc*w), 0],[-math.sin(cc*w), math.cos(cc*w), 0],[0, 0, 1]])
           RT=R.transpose()
           V1=np.dot(R,m)
           V=np.dot(V1,RT)
           v1=np.array([math.cos(az)*math.cos(dipz[i]),math.sin(az)*math.cos(dipz[i]),math.sin(dipz[i])])
           t=np.dot(V,v1)
           X1[k]=np.dot(v1,t)
           SS1[k]=math.sqrt(np.dot(t,t)-pow(X1[k],2))
           NN1[k]= X1[k]-((SS1[k]-C)/ff)
           k=k+1
    return strk, dip,NN1

def get_discretefaults(S1,S2,S3,w,Pp,C,fa,m,df):
    pp=math.pi
    cc=(pp/180)
    k=0
    n4=len(df)
    dx=[0]*n4
    dy=[0]*n4
    strk2=[0]*n4
    dip2=[0]*n4
    X2=[0]*n4
    SS2=[0]*n4
    NN2=[0]*n4
    dipz=[0]*n4
    ff=math.tan(cc*fa)

    for i in range(0,n4):
       az=cc*(df['az1'][i]+90)
       az=(pp/2)-az
       if az<0:
          az=2*pp+az
       else:
          az=cc*(df['az1'][i]+90)
       dipz[i]=(pp/2)-cc*df['dip'][i]
       radius=math.sqrt(2)*math.cos((pp/4)+(dipz[i]/2))
       dx[k]=radius*math.cos(az)
       dy[k]=radius*math.sin(az)
       strk2[i]=df['az1'][i]
       dip2[i]=df['dip'][i]
       R=np.array([[math.cos(cc*w), math.sin(cc*w), 0],[-math.sin(cc*w), math.cos(cc*w), 0],[0, 0, 1]])
       RT=R.transpose()
       V1=np.dot(R,m)
       V=np.dot(V1,RT)
       v1=np.array([math.cos(az)*math.cos(dipz[i]),math.sin(az)*math.cos(dipz[i]),math.sin(dipz[i])])
       t=np.dot(V,v1)
       X2[k]=np.dot(v1,t)
       SS2[k]=math.sqrt(np.dot(t,t)-pow(X2[k],2))
       NN2[k]= round(X2[k]-((SS2[k]-C)/ff))
       k=k+1
    return strk2, dip2,NN2

def get_visual(df1,df2):
    strike =df2['Strike'].to_numpy()
    dip = df2['Dip'].to_numpy()
    area=df2['Dip'].to_numpy()
    colors = df2.index.to_numpy()

    strike1 =df1['Strike'].to_numpy()
    dip1 = df1['Dip'].to_numpy()
    area1=df1['Pc'].to_numpy()
    colors1 = area1

    fig, ax = mplstereonet.subplots(figsize=(6, 4))

    pole_x, pole_y = mplstereonet.pole(strike, dip)
    pole_x1, pole_y1 = mplstereonet.pole(strike1, dip1)

  
    c1=ax.scatter(pole_x1,pole_y1,c=colors1, s=45,cmap='hsv_r', alpha=0.75)
    
    c=ax.scatter(pole_x,pole_y,c='black', s=45,cmap='hsv_r', alpha=0.75)
    
    fig.colorbar(c1,location='bottom',label="Critical Pressure(psi)")

    ax.set_azimuth_ticks([])
    
    label = np.arange(0,360,45)
    labx= 0.5-0.55*np.cos(np.radians(label+90))
    laby= 0.5+0.55*np.sin(np.radians(label+90))
    for i in range(len(label)):
       ax.text(labx[i],laby[i],str(int(label[i]))+'\N{DEGREE SIGN}',transform=ax.transAxes, ha='center', va='center')
   
    fig.subplots_adjust(top=1.5)

    ax.grid(kind='polar')

    return fig