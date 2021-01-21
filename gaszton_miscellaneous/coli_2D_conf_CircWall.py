speed=100.
xyres=0.25
zres=2*xyres

NlinesXY=11
#height=1.4  #original height
height=1.6
z0=-3.+mod(height,zres)

R=60.
funR=7.5
#gap=2*funR+6.
gap=2*funR+7.
sideL=R-15-gap
y0=R*cos(pi/6)

#side wall:
lineE=array([[-sideL/2,y0,z0],[sideL/2,y0,z0]])
nl=array([NlinesXY,(height-z0)/zres+1])

sideE=mStr.lineReplicate3D(lineE,nl,[xyres,zres],[1,2])
sideE[-1,3:5]=[0,speed]

cflower=mStr.MicroStr(sideE)

#make the entry funnel:
funTheta=120./180.*pi
Np=round(funR*funTheta) #1um resolution for the circle arc
phivec=linspace(0,funTheta,Np,endpoint=True)+(pi/2-funTheta)-pi/2

funlayer=empty((0,3))
r=funR
for i in range(NlinesXY):
    
    funE=array([sin(phivec)*r-sideL/2-xyres,cos(phivec)*r+y0-funR,phivec*0]).transpose()

    #add an extra point the make the funnel sharp:
    dr=diff(funE[:2,:],axis=0)
    dr=dr/sqrt(sum(dr*dr))
    xp=array([funE[0,:].copy()])
    xp-=(i+1)*dr*xyres
    funE=append(xp,funE,0)

    if(mod(i,2)==1):
        funE=flipud(funE)

    funlayer=append(funlayer,funE,0)

    r+=xyres

funlayer[:,2]=z0

#replicate the layer along Z:
Nz=(height-z0)/zres+1
funnel=mStr.lineReplicate2D(funlayer,Nz,zres,2)
funnel[-1,3:5]=[0,speed]

cflower.addStr(mStr.MicroStr(funnel))
funnel[:,0]*=-1
cflower.addStr(mStr.MicroStr(funnel))

#add an outer straight line to funnel in 
#bacteria swimming along the walls outer side
funL=15. 
xoff=-(NlinesXY/2-0.5)*xyres
lineE=array([[xoff,0,z0],[xoff,-funL,z0]])
nl=array([NlinesXY,(height-z0)/zres+1])

funLine=mStr.lineReplicate3D(lineE,nl,[xyres,zres],[0,2])
funLine[-1,3:5]=[0,speed]

#dx=-2. 
#dy=funL-2.5-xyres

dx=2.
dy=funL-2.5

funnel=mStr.MicroStr(funLine)
funnel.rotate(15,'z')
funnel.shift([sideL/2+funR,y0,0])
funnel.shift([dx,dy,0])

cflower.addStr(funnel)

funnel=mStr.MicroStr(funLine)
funnel.rotate(-15,'z')
funnel.shift([-sideL/2-funR,y0,0])
funnel.shift([-dx,dy,0])

cflower.addStr(funnel)

#add an inner circular wall:
wallLayer=empty((0,3))
#r=sqrt(3)/2*R-(NlinesXY-4)*xyres
r=R-(NlinesXY-4)*xyres-11.4

for i in range(NlinesXY):
       
    phioff=-9.5/r
    phirange=2*pi/6+phioff
    phivec=array([linspace(0,phirange,60)]).transpose()+2*pi/6-phioff/2

    lineE=concatenate((cos(phivec)*r,sin(phivec)*r,0*phivec+z0),axis=1)
    if (mod(i,2)==1):
        lineE=flipud(lineE)

    wallLayer=append(wallLayer,lineE,0)

    r-=xyres

#replicate the layer along Z:
Nz=(height-z0)/zres+1
wall=mStr.lineReplicate2D(wallLayer,Nz,zres,2)
wall[-1,3:5]=[0,speed]
cflower.addStr(mStr.MicroStr(wall))

#rotate and add 5 times
temp=deepcopy(cflower)
for i in range(5):
    temp.rotate(60,'z')
    cflower.addStr(temp)

cflower.rotate(90,'z')

#add a central support column for the roof:
nl=(height+3)/zres+1
scol=mStr.diskStr(0,0,-2,1.5,speed,xyres,zres,nl)
#scol=mStr.diskStr(0,0,-2,2.5,speed,xyres,zres,nl)

#make the central support column to be fabricated first:
temp=deepcopy(cflower)
cflower=scol
cflower.addStr(temp)

#add radial lines:
x0=8.
x1=R-22.
nly=5
yoff=-(nly/2.-0.5)*xyres

lineE=array([[x0,yoff,z0],[x1,yoff,z0]])
nl=array([nly,(height-z0)/zres+1])

rLine=mStr.lineReplicate3D(lineE,nl,[xyres,zres],[1,2])
rLine[-1,3:5]=[0,speed]
rLine=mStr.MicroStr(rLine)
#rLine.rotate(30,'z')

Nlines=6
for i in range(Nlines):
    cflower.addStr(rLine)
    rLine.rotate(360/Nlines,'z')


#add a roof:
zoffset=0.5
rstart=remainder(R+NlinesXY*xyres,0.5)+xyres
roof=mStr.diskStr(0,0,height+zoffset,R+NlinesXY*xyres,speed,2*xyres,2*zres,1,phires=60,ipstep=0.15)

#zres=0.75

for i in range(1,6):
    if mod(i,2)==1:
        roofE=mStr.diskStr(0,0,height+zoffset+i*2*zres,R+NlinesXY*xyres,speed,2*xyres,2*zres,1,phires=60,ipstep=0.15,Rmin=rstart)
    else:
        roofE=mStr.diskStr(0,0,height+zoffset+i*2*zres,R+NlinesXY*xyres,speed,2*xyres,2*zres,1,phires=60,ipstep=0.15)

    roof.addStr(roofE)

##add an extra wall on the top of the roof (it will hold the norland filling):
#z0=height+zoffset+(i+1)*2*zres
#rstart=R
#Nlz=10/(2*zres)+1
#roofE=mStr.diskStr(0,0,z0,R+NlinesXY*xyres,speed,2*xyres,2*zres,Nlz,phires=60,ipstep=0.15,Rmin=rstart,scanmode=1)
#roof.addStr(roofE)

roof.rotate(30,'z')

cflower.plot(1)

#single beam hologram:
traps=holo.trap(-10,10,0)
h=holo.holo(traps,1,isRand=True)


#compensate for the glass tilt:
#y direction:
dx=250.
dz=-0.3  #usually -
phi=arctan2(dz,dx)/pi*180
cflower.rotate(phi,'x')
roof.rotate(phi,'x')

#x direction:
dx=250.
dz=-0.15
phi=-arctan2(dz,dx)/pi*180
cflower.rotate(phi,'y')
roof.rotate(phi,'y')


