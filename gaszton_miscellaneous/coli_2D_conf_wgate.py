def roofReshape(roofE,phi):

    roofE=deepcopy(roofE)
    s=roofE.Strokes[0]

    roofE.rotate(-phi,'z')
    coors1=s.coors.copy()

    roofE.rotate(2*phi,'z')
    coors2=s.coors.copy()

    #interlace the coordinates:
    coors=append(coors1,coors2,1)
    N=len(coors)
    coors=coors.reshape((2*N,3))

    return coors

speed=100.
xyres=0.25
zres=2*xyres

NlinesXY=11
#height=1.4  #original height
height=1.8
z0=-3.+mod(height,zres)

R=100.
funR=7.5
gap=2*funR+6.
#gap=2*funR+7.
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

#dx=-2.  #2before
#dy=funL-2.5-xyres

funnelshift=0.5

dx=2.+cos(pi/3.)*funnelshift
dy=funL-2.5+sin(pi/3.)*funnelshift

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

#rotate and add 5 times
temp=deepcopy(cflower)
for i in range(5):
    temp.rotate(60,'z')
    cflower.addStr(temp)

cflower.rotate(90,'z')

#add a central support column for the roof:
nl=(height+3)/zres+1
scol=mStr.diskStr(0,0,-2,1.5,speed,xyres,zres,nl)
#cflower.addStr(scol)

scol.shift([0,R*0.6,0])
Ncol=6
for i in range(Ncol):
    cflower.addStr(scol)
    scol.rotate(360./Ncol,'z')


#add the gate:
gheight=9.
nlz=(gheight--2)/zres+1
gateR=1.5
gateRingR0=gateR+2.5
gateRingR1=gateRingR0+1.

gate=mStr.diskStr(0,0,-2,gateR,speed,xyres,zres,nlz)

plate=mStr.diskStr(0,0,0,gateRingR0+2.,speed,xyres,zres,3,Rmin=gateR)
gate.addStr(plate)
plate=mStr.diskStr(0,0,gheight,gateRingR0+1.,speed,xyres,zres,2,Rmin=gateR)
gate.addStr(plate)

#ring of the lever:
leverAngle=25./180*pi
nlz=4
z0=gheight/2.
lever=mStr.diskStr(0,0,z0,gateRingR1,speed,xyres,zres,nlz,Rmin=gateRingR0)
leverL1=25
leverL2=10.


nly=1./xyres+1
y0=-(nly/2.-0.5)*xyres
x1=cos(leverAngle)*leverL2
y1=sin(leverAngle)*leverL2
lineE=array([[gateRingR1,y0,z0],
             [leverL1,y0,z0],
             [leverL1+x1,y0+y1,z0]])
arm=mStr.lineReplicate3D(lineE,[nly,nlz],[xyres,zres],[1,2])
arm[-1,3:5]=[0,speed]
lever.addStr(mStr.MicroStr(arm))

#add a spherical handle on the lever:
sphHandleL=8.
nly=1./xyres+1
y0=-(nly/2.-0.5)*xyres
x1=cos(leverAngle)*leverL2
y1=sin(leverAngle)*leverL2
lineE=array([[-gateRingR1,y0,z0],
             [-(sphHandleL+gateRingR1),y0,z0]])
arm=mStr.lineReplicate3D(lineE,[nly,nlz],[xyres,zres],[1,2])
arm[-1,3:5]=[0,speed]
lever.addStr(mStr.MicroStr(arm))
#sphere:
sphR=1.5
sph=mStr.sphereStr(0,0,0,sphR,speed,xyres,1,1)
sph.shift([-(sphHandleL+gateRingR1)-sphR,0,z0+(nlz/2.-0.5)*zres])
lever.addStr(sph)

nlz+=2
z0-=nlz*zres
lineE=array([[leverL1,y0,z0],
             [leverL1+x1,y0+y1,z0]])
arm=mStr.lineReplicate3D(lineE,[nly,nlz],[xyres,zres],[1,2])
arm[-1,3:5]=[0,speed]
lever.addStr(mStr.MicroStr(arm))


#lever.rotate(-leverAngle/pi*180,'z')
lever.rotate(-140,'z')

gate.addStr(lever)

dx=-(leverL2/2.+cos(leverAngle)*leverL1)+0.5
dy=sin(leverAngle)*leverL1-6.
gate.shift([dx,R+dy,0])

#gate.plot(1)

Ngate=6
for i in range(Ngate):
    cflower.addStr(gate)
    gate.rotate(360./Ngate,'z')

#add a roof:
R-=9.
phi=(16./R)/pi*180

zoffset=0.5
zres=0.75
rstart=remainder(R+NlinesXY*xyres,0.5)+xyres
roof=mStr.diskStr(0,0,height+zoffset,R+NlinesXY*xyres-xyres,speed,2*xyres,2*zres,1,phires=60,ipstep=0.15,Rmin=rstart-xyres)
newcoors=roofReshape(roof,phi)
roof.Strokes[0].coors=newcoors

for i in range(1,6):
    if mod(i,2)==1:
        roofE=mStr.diskStr(0,0,height+zoffset+i*2*zres,R+NlinesXY*xyres,speed,2*xyres,2*zres,1,phires=60,ipstep=0.15,Rmin=rstart)        
    else:
        roofE=mStr.diskStr(0,0,height+zoffset+i*2*zres,R+NlinesXY*xyres-xyres,speed,2*xyres,2*zres,1,phires=60,ipstep=0.15,Rmin=rstart-xyres)


    newcoors=roofReshape(roofE,phi)
    roofE.Strokes[0].coors=newcoors
    roof.addStr(roofE)

roof.rotate(30,'z')

cflower.shift([R,R,0])
roof.shift([R,R,0])

temp=deepcopy(cflower)
temp.addStr(roof)
temp.plot2D(plotmode=1)

#cflower.plot2D(plotmode=1)
#roof.plot2D(plotmode=1)
#grid()
#single beam hologram:
traps=holo.trap(-10,10,0)
h=holo.holo(traps,1,isRand=True)


#compensate for the glass tilt:
#y direction:
dx=250.
dz=0.2
phi=arctan2(dz,dx)/pi*180
cflower.rotate(phi,'x')
roof.rotate(phi,'x')

#x direction:
dx=250.
dz=-0.5
phi=-arctan2(dz,dx)/pi*180
cflower.rotate(phi,'y')
roof.rotate(phi,'y')



