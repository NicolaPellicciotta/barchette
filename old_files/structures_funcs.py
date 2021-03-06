from copy import deepcopy

# ciao=arrange_disks(radius=5.,Dx=50,Dy=50,height=3.,height_standing=1.,size_standing=1.)
#ciao=arrange_disks(radius=10.,Dx=75,Dy=50)


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


execfile("lineposgenerator.py")



# to make disks and dumbbell around 10 and 35 um in diameter
def arrange_disks(radius=5.,height=3.,Dx=45,Dy=45,height_standing=1.,size_standing=1.):

    speed=100.
    xyres=0.25
    zres=xyres*2
    z_below =-2
    
    Nx = ceil(200./ Dx)
    Ny = 4
#    scaling = array([1.,0.7,0.5,0.3,0.2])
    if Ny*Dy>250:
        print('distanza tra strutture deve essere inferiore')
        return
#    Ny_max= ceil(200./Dy)
    Xc,Yc=placeReplicas(Nx,Ny,Dx,Dy,direction=1,shift=False)
    mic_structures=None

    for i in arange(len(Xc)):
        kk=int(floor(i/Nx))
        if kk==0 or kk==1:
            temp=create_dumbbell_disk(radius=radius,height=height,height_standing=height_standing,size_standing=size_standing, plot_visible=0,speed=speed,xyres=xyres)
        else:
            nl= int((height-z_below)/zres +1)
            temp=mStr.diskStr(0,0,0,radius,speed,xyres,zres,nl,Rmin= 0.75)

        temp.shift([Xc[i],Yc[i],z_below])
        if mic_structures is None:
            mic_structures=deepcopy(temp)
        else:
            mic_structures.addStr(temp)

    figure();mic_structures.plot2D(plotmode=1)
    figure();mic_structures.plot2D([1,2]);

    return mic_structures  





# to make disks and dumbbell around 10 and 35 um in diameter
def arrange_large_disks(radius=20.,height=3.,Dx=60,Dy=60,height_standing=1.,size_standing=2.):

    speed=100.
    xyres=0.25
    zres=xyres*2
    z_below =-2
    
    Nx = ceil(200./ Dx)
    Ny = 2
#    scaling = array([1.,0.7,0.5,0.3,0.2])
    if Ny*Dy>250:
        print('distanza tra strutture deve essere inferiore')
#    Ny_max= ceil(200./Dy)
    Xc,Yc=placeReplicas(Nx,Ny,Dx,Dy,direction=1,shift=False)
    mic_structures=None

    for i in arange(len(Xc)):
        kk=int(floor(i/Nx))
        if kk==0:
            temp=create_dumbbell_disk(radius=radius,height=height,height_standing=height_standing,size_standing=size_standing, plot_visible=0,speed=speed,xyres=xyres)
        else:
            nl= int((height-z_below)/zres +1)
            temp=mStr.diskStr(0,0,0,radius,speed,xyres,zres,nl,Rmin= 0.75)

        temp.shift([Xc[i],Yc[i],z_below])
        if mic_structures is None:
            mic_structures=deepcopy(temp)
        else:
            mic_structures.addStr(temp)

    figure();mic_structures.plot2D(plotmode=1)
    figure();mic_structures.plot2D([1,2]);

    return mic_structures  




# to make disks and dumbbell around 10 and 35 um in diameter
def arrange_funnels_disks(radius=5.,height=8.,angle_funnel=45.,spacing=1.5,L_funnel=4., Dx=45,Dy=45):

    speed=100.
    xyres=0.25
    zres=xyres*2
    z_below =-2
    height_standing=3.5
    
    Nx = ceil(200./ Dx)
    Ny = ceil(200./ Dy)
#    scaling = array([1.,0.7,0.5,0.3,0.2])
    if Ny*Dy>250:
        print('distanza tra strutture deve essere inferiore')
#    Ny_max= ceil(200./Dy)
    Xc,Yc=placeReplicas(Nx,Ny,Dx,Dy,direction=1,shift=False)
    mic_structures=None
    
    dumbbell_funnel= create_dumbbell_funnel(radius=radius,height=height,height_standing=height_standing,angle_funnel=angle_funnel,spacing=spacing, plot_visible=0,speed=speed,xyres=xyres,L_funnel=L_funnel)
    for i in arange(len(Xc)):
        temp=deepcopy(dumbbell_funnel)
        temp.shift([Xc[i],Yc[i],0])
        if mic_structures is None:
            mic_structures=deepcopy(temp)
        else:
            mic_structures.addStr(temp)

    figure();mic_structures.plot2D(plotmode=1)
    figure();mic_structures.plot2D([1,2]);

    return mic_structures  





def create_square(height=5.,size=10.,plot_visible=0):

    speed=100.
    power= 8 # Mw 
    #(nicola) with 8Mw structure either detach or do ot polymerise, use 10Mw instead

    xyres=0.25
    zres=2*xyres;    
    z_below =-2
    square_x=  size
    square_y= size
    nl=(square_x)/(2*xyres)+1
    lineE=array([[-square_x/2,-square_y/2,z_below],[-square_x/2,+square_y/2,z_below]])
    fillcol=mStr.lineReplicate2D(lineE,nl,zres,0)
    fillcol[-1,3:5]=array([0,speed])
    square_mst=mStr.MicroStr(fillcol)


    height_eff = height-z_below
    nl= int((height_eff)/(zres)+1)

    for i in range(1,nl):
#        square_x+=i*zres+2*xyres   #this is for making the square with growing size 
#        square_y+=i*zres+2*xyres
        nl=(square_x)/(2*xyres)+1
        lineE=array([[-square_x/2,-square_y/2,z_below+ i*zres],[-square_x/2,+square_y/2,z_below+i*zres]])
        fillcol=mStr.lineReplicate2D(lineE,nl,zres,0)
        fillcol[-1,3:5]=array([0,speed])
        square_mst.addStr(mStr.MicroStr(fillcol))

    if plot_visible!=0:
        figure();square_mst.plot2D(plotmode=1)
        figure(); square_mst.plot2D([1,2]);

    return square_mst



def arrange_squares(Dx=40,Dy=40):
    
    
    Nx = ceil(200./ Dx)
    Ny = 4
    scaling = array([1.,0.7,0.5,0.3,0.2])
    if Ny*Dy>250:
        print('distanza tra strutture deve essere inferiore')
#    Ny_max= ceil(200./Dy)
    Xc,Yc=placeReplicas(Nx,Ny,Dx,Dy,direction=1,shift=False)
    mic_structures=None
    for i in arange(len(Xc)):
        kk=int(floor(i/Nx))
        square_mst =create_square(height=(5*scaling[kk]),size=(10*scaling[kk]),plot_visible=0)
        print(scaling[kk])
        temp=deepcopy(square_mst)
    #    temp.rotate(theta[i]/pi*180,'z')
        temp.shift([Xc[i],Yc[i],0])
        if mic_structures is None:
            mic_structures=deepcopy(temp)
        else:
            mic_structures.addStr(temp)

    figure();mic_structures.plot2D(plotmode=1)
    figure();mic_structures.plot2D([1,2]);

    return mic_structures    


def create_dumbbell_disk(radius=10,height=5,height_standing=1.5,size_standing=1.5, plot_visible=0,speed=100,xyres=0.25):
    '''
        --               --
        -------------------
        --               --
    '''

    zres=2*xyres;    
    z_below =-2

### create the base (sligltly higher for glass attachemnt)

    nl=((height_standing-z_below)/zres+1)
    disco_base=mStr.diskStr(0,0,0,radius,speed,xyres,zres,nl,Rmin= radius-size_standing)
    dumbbell= deepcopy(disco_base)

### create the central disk
    height_disk= height-2*height_standing
    nl=((height_disk)/zres+1)
    disco=mStr.diskStr(0,0,0,radius,speed,xyres,zres,nl,Rmin= 0.75)
    disco.shift([0,0,dumbbell.Strokes[0].coors[:,2].max()])    
    dumbbell.addStr(disco)

### create top 

    nl=((height_standing)/zres+1)
    disco_top=mStr.diskStr(0,0,0,radius,speed,xyres,zres,nl,Rmin= radius-size_standing)
    disco_top.shift([0,0,dumbbell.Strokes[1].coors[:,2].max()])    
    dumbbell.addStr(disco_top)

    if plot_visible!=0:
        figure(1);dumbbell.plot2D(plotmode=1)
        figure(2); dumbbell.plot2D([1,2]);
    

    return dumbbell




def create_funnel(angle_funnel=45.,L=4.,height=1.,speed=100,xyres=0.25):

    zres=xyres*2

    nl=(height)/zres+1

    cos_L= -L*cos(angle_funnel*pi/180)
    sin_L = L*sin(angle_funnel*pi/180)
    lineE=array([[cos_L,sin_L,0],[0,0,0],[cos_L,-sin_L,0]]) 
    lineE2= concatenate((lineE,lineE[::-1]+[xyres,0,0])) #,lineE+[2*xyres,0,0]))
    funnel=mStr.lineReplicate2D(lineE2,nl,zres,2)
    funnel[-1,3:5]=array([0,speed])
    funnel=mStr.MicroStr(funnel)

    return funnel


#### displace funnels in a circle
def displace_funnel_circle(radius=10.,angle_funnel=45.,height_funnel=1.5,L_funnel=4.,spacing=1.5, plot_visible=0,speed=100,xyres=0.25):

#    spacing = 1.5
   
    L_openedge= 2.*L_funnel*sin(angle_funnel*pi/180.)
    L_altezza = L_funnel*cos(angle_funnel*pi/180.)
    r = radius -L_altezza

    N_funnel = floor( 2*pi*r/(L_openedge+spacing) )  
    delta_angle = 2*pi/N_funnel

    funnel_disk=None
    for i in arange(N_funnel):
        temp = create_funnel(angle_funnel=angle_funnel,L=L_funnel,height=height_funnel,speed=speed,xyres=xyres)
        temp_angle = i*delta_angle
        temp.rotate(temp_angle*180/pi ,'z')
        temp.shift([radius*cos(temp_angle) , radius*sin(temp_angle) , 0 ]) 

        if funnel_disk ==None:
            funnel_disk=deepcopy(temp)
            funnel_disk.addStr(temp)

        else:
            funnel_disk.addStr(temp)
        

    if plot_visible!=0:
        figure(1);funnel_disk.plot2D(plotmode=1)
        figure(2); funnel_disk.plot2D([1,2]);
    
    

    return funnel_disk
    ### create all funnels with thi angle on a circonferenza radius



    return funnels




def create_dumbbell_funnel(radius=10.,height=5.,height_standing=1.5,L_funnel=4., angle_funnel=45.,spacing=1.5,plot_visible=0,speed=100,xyres=0.25):
    '''
        --               --
        -------------------
        --               --
    '''

    zres=2*xyres;    
    z_below =-2
#    angle_funnel=45.

### create the base (sligltly higher for glass attachemnt)

    nl=((height_standing-z_below)/zres+1)
    disco_base=displace_funnel_circle(radius=radius,angle_funnel=angle_funnel,height_funnel=(height_standing-z_below),L_funnel=L_funnel,spacing=spacing, plot_visible=0,speed=speed,xyres=xyres)
    disco_base.shift([0,0,z_below])
    dumbbell= deepcopy(disco_base)

### create the central disk
    height_disk= height-2*height_standing
    nl=((height_disk)/zres+1)
    disco=mStr.diskStr(0,0,0,radius,speed,xyres,zres,nl,Rmin= 0.75)
    disco.shift([0,0,dumbbell.Strokes[1].coors[:,2].max()+zres])    
    dumbbell.addStr(disco)

### create top 

    nl=((height_standing)/zres+1)
    disco_top=displace_funnel_circle(radius=radius,angle_funnel=angle_funnel,height_funnel=(height_standing),L_funnel=L_funnel,spacing=spacing, plot_visible=0,speed=speed,xyres=xyres)
    disco_top.shift([0,0,dumbbell.Strokes[-1].coors[:,2].max()+zres])    
    dumbbell.addStr(disco_top)

    if plot_visible!=0:
        figure(1);dumbbell.plot2D(plotmode=1)
        figure(2); dumbbell.plot2D([1,2]);
    

    return dumbbell

def create_channels(height=2.,first_layer=2.7, letter='0'):

    speed=100.
    power= 8 # Mw 
    #(nicola) with 8Mw structure either detach or do ot polymerise, use 10Mw instead

    xyres=0.25
    zres=2*xyres;

#    height=2.5
    channel_distance = 6.  ###  um

    channel_length = 120. ### um 
    channel_space = 100. ### um 

    #make the channels
    zoffset = 3.

    nl=(height+zoffset)/zres+1
#    first_layer = 8.2 
    channel_zoffset = -zoffset +first_layer # the second number is the height of the first su8 layer
    lineE=array([[0,-channel_length/2,channel_zoffset],[0,channel_length/2,channel_zoffset]]) # single line
    fillcol=mStr.lineReplicate2D(lineE,nl,zres,2)
    fillcol[-1,3:5]=array([0,speed])
    fillcol=mStr.MicroStr(fillcol)


    #Dx=0; Dy=channel_width+xyres; #per makePillar
    #max_x =2*channel_length; max_y=channel_space
    #Ny = floor(max_y/ Dy)
    Dx=channel_distance+xyres; Dy=0; #per makePillar
    max_y =2*channel_length; max_x=channel_space
    Nx = floor(max_x/ Dx)

    if Dy==0:
        Ny=1
    else:
        Ny = floor(max_x/ Dx)
    Xc,Yc=placeReplicas(Nx,Ny,Dx,Dy,direction=1,shift=False)
    #Xc= Xc- array(max_x/2)
    #Yc= Yc- array(max_y/2)



    #replicate to fill obstacle:
    obstacles=None
    for i in range(len(Xc)):
        temp=deepcopy(fillcol)
    #    temp.rotate(theta[i]/pi*180,'z')
        temp.shift([Xc[i],Yc[i],0])
        if obstacles is None:
            obstacles=deepcopy(temp)
        else:
            obstacles.addStr(temp)

    ## from 5.6.20
    obstacles.rotate(90,'z')
    obstacles.shift([0 ,-channel_space/2,0])

    # add a number as identifier
    let_y = 0.
    let_x = 0.
    let_size = 10.

    if letter==0:
        letter2add=  mStr.letter0(let_size,let_y,let_x,speed)

    if letter==1:
        letter2add=  mStr.letter1(let_size,let_y,let_x,speed)

    if letter==2:
        letter2add=  mStr.letter2(let_size,let_y,let_x,speed)

    if letter==3:
        letter2add=  mStr.letter3(let_size,let_y,let_x,speed)

    if letter==4:
        letter2add=  mStr.letter4(let_size,let_y,let_x,speed)

    if letter==5:
        letter2add=  mStr.letter5(let_size,let_y,let_x,speed)

    if letter==6:
        letter2add=  mStr.letter6(let_size,let_y,let_x,speed)

    if letter==7:
        letter2add=  mStr.letter7(let_size,let_y,let_x,speed)

    if letter==8:
        letter2add=  mStr.letter8(let_size,let_y,let_x,speed)

    if letter==9:
        letter2add=  mStr.letter9(let_size,let_y,let_x,speed)

    letter_coords = letter2add.Strokes[0].coors
    letter_replicated = mStr.lineReplicate2D(letter_coords,nl,zres,2)
    letter_replicated[-1,3:5]= array([0,speed])
    letter2add = mStr.MicroStr(letter_replicated)
    let_pos_y = 60.
    let_pos_x = 50.   # real tpp image is mirrored
    letter2add.shift([let_pos_y,let_pos_x,channel_zoffset])
    obstacles.addStr(letter2add)


    figure();obstacles.plot2D(plotmode=1)
    figure(); obstacles.plot2D([1,2]);



#    traps=holo.trap(10,10,0)
#    h=holo.holo(traps,1,isRand=True)
#    slm.show(h)

    return obstacles

    #invchamber.shift([0,RR+30,0])
    #invchamber.shift([-30,RR,0])  #for the triangles


    ''' 
    # da rimettere
    #single beam hologram:



    #compensate for the glass tilt:
    #y direction:
    dx=250.
    dz=0.5  #usually -
    phi=arctan2(dz,dx)/pi*180
    invchamber.rotate(phi,'x')

    #x direction:
    dx=250.
    dz=-0.4
    phi=-arctan2(dz,dx)/pi*180
    invchamber.rotate(phi,'y')
    '''
