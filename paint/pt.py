# tiny painting toolkit: float RGB canvases, AA masks via 3x supersampled PIL drawing
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
W,H=1536,1024
SS=3
rng=np.random.default_rng(7)
def hexc(h):
    h=h.lstrip('#');return np.array([int(h[i:i+2],16) for i in (0,2,4)],np.float32)/255
def vgrad(stops,h=H,w=W):
    ys=np.linspace(0,1,h)
    pos=[p for p,_ in stops];cols=[hexc(c) for _,c in stops]
    out=np.zeros((h,3),np.float32)
    for k in range(3):out[:,k]=np.interp(ys,pos,[c[k] for c in cols])
    return np.repeat(out[:,None,:],w,1)
def newmask():
    im=Image.new('L',(W*SS,H*SS),0);return im,ImageDraw.Draw(im)
def fin(im,blur=0):
    m=im.resize((W,H),Image.LANCZOS)
    if blur:m=m.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(m,np.float32)/255
def S(pts):return [(x*SS,y*SS) for x,y in pts]
def poly(pts,blur=0):
    im,d=newmask();d.polygon(S(pts),fill=255);return fin(im,blur)
def ellipse(cx,cy,rx,ry,blur=0):
    im,d=newmask();d.ellipse([(cx-rx)*SS,(cy-ry)*SS,(cx+rx)*SS,(cy+ry)*SS],fill=255);return fin(im,blur)
def circles(lst,blur=0):
    im,d=newmask()
    for cx,cy,r in lst:d.ellipse([(cx-r)*SS,(cy-r)*SS,(cx+r)*SS,(cy+r)*SS],fill=255)
    return fin(im,blur)
def lines(segs,width,blur=0):
    im,d=newmask()
    for pts in segs:
        d.line(S(pts),fill=255,width=int(width*SS),joint='curve')
        r=width*SS/2
        for x,y in (pts[0],pts[-1]):d.ellipse([x*SS-r,y*SS-r,x*SS+r,y*SS+r],fill=255)
    return fin(im,blur)
def over(c,col,m,a=1.0):
    col=np.asarray(col,np.float32)
    if col.ndim==1:col=col[None,None,:]
    m=(m*a)[...,None];return c*(1-m)+col*m
def add(c,col,m,a=1.0):
    col=np.asarray(col,np.float32)
    if col.ndim==1:col=col[None,None,:]
    return c+col*(m*a)[...,None]
def screen(c,col,m,a=1.0):
    col=np.asarray(col,np.float32)
    if col.ndim==1:col=col[None,None,:]
    s=1-(1-c)*(1-col*(m*a)[...,None]);return s
def outline(m,width=2.2,blur=0.4):
    # ring just outside/at edge of mask
    from scipy import ndimage as ndi
    b=m>0.5
    d_out=ndi.distance_transform_edt(~b);d_in=ndi.distance_transform_edt(b)
    sd=np.where(b,-d_in,d_out)
    ring=np.clip(1-np.abs(sd+width*0.3)/(width*0.6+0.5),0,1)
    return ring
def radial(cx,cy,r,power=2.0):
    y,x=np.mgrid[0:H,0:W].astype(np.float32)
    d=np.sqrt((x-cx)**2+(y-cy)**2)/r
    return np.clip(1-d,0,1)**power
def blur(m,s):
    from scipy import ndimage as ndi
    if m.ndim==3:return np.stack([ndi.gaussian_filter(m[...,k],s) for k in range(m.shape[2])],2)
    return ndi.gaussian_filter(m,s)
def noise(scale,octaves=4,seed=0):
    r=np.random.default_rng(seed);out=np.zeros((H,W),np.float32);amp=1;tot=0
    for o in range(octaves):
        s=max(1,int(scale/(2**o)))
        g=r.random((H//s+2,W//s+2)).astype(np.float32)
        im=Image.fromarray((g*255).astype(np.uint8)).resize(((W//s+2)*s,(H//s+2)*s),Image.BICUBIC)
        out+=amp*np.asarray(im,np.float32)[:H,:W]/255;tot+=amp;amp*=0.5
    return out/tot
def save(c,path):
    Image.fromarray((np.clip(c,0,1)*255+0.5).astype(np.uint8)).save(path)
def chaikin(p,n=3,closed=True):
    for _ in range(n):
        q=[];m=len(p)
        rngi=range(m) if closed else range(m-1)
        for i in rngi:
            (x0,y0),(x1,y1)=p[i],p[(i+1)%m];q+=[(0.75*x0+0.25*x1,0.75*y0+0.25*y1),(0.25*x0+0.75*x1,0.25*y0+0.75*y1)]
        p=q if closed else [p[0]]+q+[p[-1]]
    return p
YY,XX=np.mgrid[0:H,0:W].astype(np.float32)
def gauss_dots(pts,col_sz):
    m=np.zeros((H,W),np.float32)
    for x,y,s,a in pts:
        x0,x1=int(max(0,x-4*s)),int(min(W,x+4*s+1));y0,y1=int(max(0,y-4*s)),int(min(H,y+4*s+1))
        if x0>=x1 or y0>=y1:continue
        m[y0:y1,x0:x1]+=a*np.exp(-((XX[y0:y1,x0:x1]-x)**2+(YY[y0:y1,x0:x1]-y)**2)/(2*s*s))
    return m
def rock(c,pts,base,light,dark,NAVY,seed=0,rim=None,rimcol=None,facets=6,lw=2.6):
    rr=np.random.default_rng(seed)
    m=poly(pts)
    c=over(c,hexc(base),m)
    xs=[p[0] for p in pts];ys=[p[1] for p in pts]
    x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
    for i in range(facets):
        cx=x0+rr.random()*(x1-x0);cy=y0+rr.random()*(y1-y0)*0.7
        w=(x1-x0)*(0.12+rr.random()*0.2);h=(y1-y0)*(0.1+rr.random()*0.2)
        f=[(cx-w,cy+h*0.2),(cx-w*0.3,cy-h),(cx+w*0.6,cy-h*0.8),(cx+w,cy+h*0.3),(cx+w*0.2,cy+h)]
        fm=poly(f)*m
        c=over(c,hexc(light if rr.random()<0.6 else dark),fm,0.55)
        c=over(c,NAVY,outline(fm,1.4)*m,0.35)
    if rim is not None:
        c=add(c,hexc(rimcol),outline(m,7)*rim,0.5)
    c=over(c,NAVY,outline(m,lw),0.95)
    return c,m
