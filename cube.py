from copy import deepcopy

def randpos(Npos,rangeR,minD,runf=100):

        X=array([0])
        Y=array([0])

        i=0
        while (i<(Npos*runf)) and (len(X)<Npos):
            x=2*(rand()-0.5)*rangeR
            y=2*(rand()-0.5)*rangeR

            #if the new point is outside rangeR we skip it:
            if sqrt(x**2+y**2)>rangeR:
                continue
            rvec=sqrt((X-x)**2+(Y-y)**2)

            #check if the new point is closer to any point than minD
            if not (rvec<minD).any():
                X=append(X,x)
                Y=append(Y,y)
            i+=1

        return X,Y



def placeReplicas(Nx,Ny,Dx,Dy,direction=1,shift=None):
	    if direction==0:
		    a,b=meshgrid(arange(0,Nx)*Dx,arange(0,Ny)*Dy)
		    if shift==True:
			    a[1::2]+=Dx/2.
	    elif direction==1:
		    b,a=meshgrid(arange(0,Ny)*Dy,arange(0,Nx)*Dx)
		    if shift==True:
			    b[1::2]+=Dy/2.
	    xs=list(flatten(a))
	    ys=list(flatten(b))
	    #plot(xs,ys, 'x')
	    return xs,ys



def arrange_cubes(L=10,h=5,Dr=50,speed=100.,xyres=0.25,zres=0.9):


    

    N= floor(200./Dr)
    Xc,Yc=placeReplicas(N,N,Dr,Dr,direction=1,shift=False)
    cubes=None

    for i in arange(len(Xc)):

#        temp=make_barchetta_double(vela_size=vela_size,support_size=support_size,inverted=inverted,R_vela=R_vela,speed=speed,xyres=xyres,zres=zres)
        temp=make_cube(L=L,h=h,speed=speed,xyres=xyres,zres=zres)

        temp.shift([Xc[i],Yc[i],0])
        if cubes is None:
            cubes=deepcopy(temp)
        else:
            cubes.addStr(temp)
    figure();cubes.plot2D([0,1],plotmode=1)
    figure();cubes.plot2D([0,2],plotmode=1)
    figure();cubes.plot2D([1,2],plotmode=1);

    return cubes


def make_cube(L=10.,h=5.,speed=100.,xyres=0.25,zres=0.9):
    zoffset=3
    
    nlz=round((h+zoffset)/zres)
    nlx=round(L/xyres)
    nly=round(L/xyres)


    lineE=array([[-L/2,-L/2,-zoffset],[-L/2,L/2,-zoffset]]) # single line

    fillcol=mStr.lineReplicate2D(lineE,nlx,xyres,0)
    fillcol=mStr.lineReplicate2D(fillcol[:,0:3],nlz,zres,2)
    fillcol[-1,3:5]=array([0,speed])
    cube=mStr.MicroStr(fillcol)
    return cube






