from matplotlib import path

def genpositions_circle(l,R,N,d):
    d2 = d**2
    R2 = R**2

    n=0

    sgs = []
    sgs2 = []
    while (n<N):
        #print "attempts = "+str(k) +"/"+str(kmx)+" succesfull = "+str(n)+"\r",
        a = rand()*2*pi
        x0 = 2*(rand()-0.5)*R
        y0 = 2*(rand()-0.5)*R
        x1 = cos(a)*l/2. + x0
        y1 = sin(a)*l/2. + y0
        x2 = -cos(a)*l/2. + x0
        y2 = -sin(a)*l/2. + y0
        sgt = array([x1,y1,x2,y2])
        ov = 0
        for j in arange(0,len(sgs)):
            dt = myssd(sgt,sgs[j])
            if dt<d2:
                ov += 1
                break
        
        if chkcir(sgt,R2)==0:
            continue

        if ov==0:
            sgs += [sgt]
            sgs2 += [array([x0,y0,a])]
            n += 1

    X,Y,theta=array(sgs2).transpose()
    return X,Y,theta

def genpositions_square(l,R,N,d):
    d2 = d**2
    R2 = R**2  
    n = 0
    sgs = []
    sgs2 = []
    while (n<N):
        print(n)
        #print "attempts = "+str(k) +"/"+str(kmx)+" succesfull = "+str(n)+"\r",
        a = rand()*2*pi
        x0 = 2*(rand()-0.5)*R
        y0 = 2*(rand()-0.5)*R
        x1 = cos(a)*l/2. + x0
        y1 = sin(a)*l/2. + y0
        x2 = -cos(a)*l/2. + x0
        y2 = -sin(a)*l/2. + y0
        sgt = array([x1,y1,x2,y2])
        ov = 0
        for j in arange(0,len(sgs)):
            dt = myssd(sgt,sgs[j])
            if dt<d2:
                ov += 1
                break
        if ov==0:
            sgs += [sgt]
            sgs2 += [array([x0,y0,a])]
            n += 1

    X,Y,theta=array(sgs2).transpose()
    return X,Y,theta

def genpositions_tri(l,R,N,d):
    d2 = d**2
    R2 = R**2
    n = 0
    sgs = []
    sgs2 = []

    phivec=linspace(0,2*pi,4)
    tripol=array([cos(phivec)*R,sin(phivec)*R]).T
    P=path.Path(tripol)

    while (n<N):
        #print "attempts = "+str(k) +"/"+str(kmx)+" succesfull = "+str(n)+"\r",
        a = rand()*2*pi
        x0 = 2*(rand()-0.5)*R
        y0 = 2*(rand()-0.5)*R
        x1 = cos(a)*l/2. + x0
        y1 = sin(a)*l/2. + y0
        x2 = -cos(a)*l/2. + x0
        y2 = -sin(a)*l/2. + y0
        sgt = array([x1,y1,x2,y2])
        ov = 0
        for j in arange(0,len(sgs)):
            dt = myssd(sgt,sgs[j])
            if dt<d2:
                ov += 1
                break

        if chktri(sgt,P)==0:
            continue

        if ov==0:
            sgs += [sgt]
            sgs2 += [array([x0,y0,a])]
            n += 1


    X,Y,theta=array(sgs2).transpose()
    return X,Y,theta

def chkcir(sg,R2):
    x1,y1,x2,y2 = sg
    return (x1**2+y1**2<R2)*(x2**2+y2**2<R2)

def chktri(sg,P):
    return P.contains_point(sg[0:2])*P.contains_point(sg[2:4])


def chksquare(sg,R):
    mask=prod(abs(sg)<R)
    return mask
    

def pltseg(sa):
    x1a,y1a,x2a,y2a = sa
    plot([x1a,x2a],[y1a,y2a],'-',lw=2)
       

def myssd(sa,sb):
    x1a,y1a,x2a,y2a = sa
    x1b,y1b,x2b,y2b = sb
    d2 = segseg(x1a,y1a,x2a,y2a,x1b,y1b,x2b,y2b)
    return d2

def segseg(x1a,y1a,x2a,y2a,x1b,y1b,x2b,y2b):
    ds = []
    ds += [ segseg1(x1a,y1a,x2a,y2a,x1b,y1b,x2b,y2b)]
    ds += [ ptseg(x1a,y1a,x1b,y1b,x2b,y2b) ]
    ds += [ ptseg(x2a,y2a,x1b,y1b,x2b,y2b) ]
    ds += [ ptseg(x1b,y1b,x1a,y1a,x2a,y2a) ]
    ds += [ ptseg(x2b,y2b,x1a,y1a,x2a,y2a) ]
    ds = array(ds)
    return ds.min()




def ptseg(X,Y,x1,y1,x2,y2):
    t = -(((X - x1)*(x1 - x2) + (Y - y1)*(y1 - y2))/(Power(x1 - x2,2) + Power(y1 - y2,2)))
    if t<0:
        t=0
    if t>1:
        t=1
    xxt = (x2-x1)*t + x1
    yyt = (y2-y1)*t + y1
    d2 = (X-xxt)**2 + (Y-yyt)**2
    return d2



def segseg1(x1a,y1a,x2a,y2a,x1b,y1b,x2b,y2b):
    t=(x2b*(y1a - y1b) + x1a*(y1b - y2b) + x1b*(-y1a + y2b))/(-((x1b - x2b)*(y1a - y2a)) + (x1a - x2a)*(y1b - y2b))
    if t<0:
        t = 0
    if t>1:
        t=1
    s=(x2a*(-y1a + y1b) + x1b*(y1a - y2a) + x1a*(-y1b + y2a))/((x1b - x2b)*(y1a - y2a) - (x1a - x2a)*(y1b - y2b))
    if s<0:
        s = 0
    if s>1:
        s=1
    xat = (x2a-x1a)*t + x1a
    yat = (y2a-y1a)*t + y1a
    xbs = (x2b-x1b)*s + x1b
    ybs = (y2b-y1b)*s + y1b
    d2 = (xat-xbs)**2 + (yat-ybs)**2
    return d2

def Power(x,n):
    return x**n
