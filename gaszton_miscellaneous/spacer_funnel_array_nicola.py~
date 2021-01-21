def rotateZ(coors,phi):
    rotmat=array([[cos(phi),-sin(phi),0],
                 [sin(phi),cos(phi),0],
                 [0,0,1]])

    npoints=size(coors,0)
    for i in range(npoints):
        tmp=coors[i,0:3].copy()
        tmp=dot(rotmat,tmp)
        coors[i,0:3]=tmp.copy()
    return coors

def makeholo(spacing,Nfocus,phi):
    #hologram calculation:
    xoff=-10
    yoff=10
    xy0=(Nfocus/2-0.5)*spacing

    xc=linspace(-xy0,xy0,Nfocus)
    yc=0*xc
    zc=yc*0
    tcoors=array([xc,yc,zc]).transpose()

    tcoors=rotateZ(tcoors,phi/180.*pi)
    tcoors[:,0]+=xoff
    tcoors[:,1]+=yoff

    traps=[]
    for i in range(len(yc)):
        traps+=[holo.trap(tcoors[i,0],tcoors[i,1],tcoors[i,2])]

    h=holo.holo(traps,60,isRand=False)
    holo.calc_performance(h,traps)

    return h

speed=100
gridD=220.

entryR=20.

Nfocus=5
spacing=1.

#funnel parameters:
funAngle=45/180.*pi
funL=((gridD/2)-entryR)/sin(funAngle)

fx0=gridD/2.-funL*cos(funAngle)-10
funL+=2

holo_y=makeholo(spacing,Nfocus,90)
holo_x=makeholo(spacing,Nfocus,0)
holo_m45=makeholo(spacing,Nfocus,-45)
holo_p45=makeholo(spacing,Nfocus,45)

xyres=0.25
z0=0.

Nlines=int(spacing/xyres)
xyoff=-(Nlines/2.-0.5)*xyres
x0=gridD/2-Nfocus*spacing/2.
y0=gridD/2-xyoff


#x-direction sides:
lineE=array([[-x0,-y0,z0],[fx0,-y0,z0]])

hline=mStr.lineReplicate2D(lineE,Nlines,xyres,1)
hline[-1,3:5]=[0,speed]
temp=deepcopy(hline)
temp[:,1]+=gridD
hline=append(hline,temp,0)

spgrid=mStr.MicroStr(hline,holo=holo_y)

#y-direction sides:
lineE=array([[-y0,-x0,z0],[-y0,-entryR,z0]])

vline=mStr.lineReplicate2D(lineE,Nlines,xyres,0)
vline[-1,3:5]=[0,speed]

temp=deepcopy(vline)
temp[:,1]*=-1
vline=append(vline,temp,0)

spgrid.addStr(mStr.MicroStr(vline,holo=holo_x))


#add funnels:
lineE=array([[-funL,xyoff,z0],[0,xyoff,z0]])
fline=mStr.lineReplicate2D(lineE,Nlines,xyres,1)
fline[-1,3:5]=[0,speed]

funnel=mStr.MicroStr(fline,holo=holo_m45)
funnel.rotate(45,'z')
funnel.shift([gridD/2.-5,-entryR,0])

f2=mStr.MicroStr(fline,holo=holo_p45)
f2.rotate(-45,'z')
f2.shift([gridD/2.-5,entryR,0])
funnel.addStr(f2)

spgrid.addStr(funnel)

spgrid.plot2D()
axis("equal")
grid()
draw()

#compensate for the glass tilt:
#y direction:
dx=250.
dz=-0.15
phi=arctan2(dz,dx)/pi*180
spgrid.rotate(phi,'x')

#x direction:
dx=250.
dz=-0.0
phi=arctan2(dz,dx)/pi*180
spgrid.rotate(phi,'y')



