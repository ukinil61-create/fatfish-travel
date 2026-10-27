from pt import *
NAVY=hexc('#141a3a')
yy,xx=YY,XX
r=np.random.default_rng(3)
c=vgrad([(0,'#060b24'),(0.25,'#0e1c49'),(0.5,'#21407a'),(0.6,'#3a6aa2')])
# stars
pts=[]
for i in range(480):
    b=r.random()**3;pts.append((r.random()*W,(r.random()**1.3)*H*0.62,0.6+b*1.5,0.35+b))
c=add(c,hexc('#f2f6ff'),np.clip(gauss_dots(pts,0),0,1.4),0.9)
for i in range(16):
    x,y=r.random()*W,r.random()*H*0.45;L=8+r.random()*14
    cr=np.exp(-np.abs(yy-y)/0.9)*np.exp(-np.abs(xx-x)/L)+np.exp(-np.abs(xx-x)/0.9)*np.exp(-np.abs(yy-y)/L)
    c=add(c,hexc('#fff8e0'),cr,0.65)
# aurora
def curtain(base,amp,freq,phase,L,col_lo,col_hi,strength,seed):
    global c
    bx=base+amp*np.sin(xx[0]/freq+phase)+amp*0.45*np.sin(xx[0]/(freq*0.37)+phase*2.1)
    rn=np.random.default_rng(seed).random(W//3+2)
    rays=np.interp(np.arange(W)/3,np.arange(len(rn)),rn)
    from scipy import ndimage as ndi
    rays=ndi.gaussian_filter1d(rays,2.5);rays=(rays-rays.min())/(rays.max()-rays.min())
    rays=0.55+0.7*rays
    fold=0.6+0.4*np.sin(xx[0]/55+phase*3)**2
    d=(bx[None,:]-yy)
    up=np.exp(-np.clip(d,0,None)/L)*(d>0)
    down=np.exp(-np.clip(-d,0,None)/6)*(d<=0)
    I=blur((up+down)*(rays*fold)[None,:],1.6)
    t=np.clip(d/(L*1.5),0,1)[...,None]
    col=hexc(col_lo)*(1-t)+hexc(col_hi)*t
    c=1-(1-c)*(1-np.clip(col*I[...,None]*strength,0,1))
curtain(335,50,200,0.3,150,'#7dffc8','#a07cff',0.72,1)
curtain(245,30,150,2.2,110,'#8affd9','#c890ff',0.42,2)
curtain(400,26,270,4.0,90,'#6ff2b8','#6a90ff',0.3,3)
c=add(c,hexc('#5d8fd0'),np.exp(-((yy-600)/80)**2),0.22)
# distant mountains (2 layers)
def ridge(y0,amp,seed,smooth,n=48):
    rr=np.random.default_rng(seed);p=[(0,H)];v=0
    for i in range(n+1):
        v=v*smooth+(rr.random()-0.5)*amp;p.append((i*W/n,y0+v))
    return p+[(W,H)]
m=poly(ridge(520,90,4,0.75),0.6)
c=over(c,vgrad([(0.45,'#2a4878'),(0.62,'#3f6699')]),m,0.9)
c=add(c,hexc('#9ff0dd'),outline(m,4)*(yy<600),0.18)
m=poly(ridge(585,40,9,0.6),0.6)
c=over(c,vgrad([(0.5,'#30558a'),(0.62,'#4c78ad')]),m)
# mist band
c=add(c,hexc('#9dc4ea'),np.exp(-((yy-612)/18)**2),0.18)
# cliffs
L=[(0,120),(40,138),(90,175),(150,250),(205,330),(240,410),(285,500),(320,575),(352,630),(0,640)]
R=[(W,100),(W-40,126),(W-100,175),(W-160,260),(W-210,350),(W-250,440),(W-290,530),(W-330,610),(W,640)]
c,m1=rock(c,chaikin(L,2),'#14234a','#22396a','#0c1733',NAVY,seed=1,rim=np.clip(1-yy/700,0,1),rimcol='#86f0cf',facets=9)
c,m2=rock(c,chaikin(R,2),'#14234a','#22396a','#0c1733',NAVY,seed=2,rim=np.clip(1-yy/700,0,1),rimcol='#86f0cf',facets=9)
import sys
NOTAIL='notail' in sys.argv
c_pre=c.copy()
# whale tail
cx,wy=780,630
half=[(-34,8),(-30,-60),(-24,-130),(-20,-190),(-30,-214),(-80,-236),(-150,-264),(-212,-300),(-250,-334),(-266,-354),(-240,-362),(-196,-356),(-148,-345),(-98,-332),(-52,-318),(-16,-306),(0,-292)]
right=[(-x*1.02,y+(-6 if y<-250 else 0)) for x,y in reversed(half[:-1])]
tail=[(cx+x,wy+y) for x,y in half+right]
tail=chaikin(tail,3)
tm=poly(tail)
body=vgrad([(0.25,'#86a6d4'),(0.34,'#6d8fc4'),(0.5,'#46699f'),(0.62,'#2b4b7e')])
c=over(c,body,tm)
# darker trailing edge band & spots
tb=poly(chaikin([(cx+x,wy+y+18) for x,y in half[9:]]+[(cx-x,wy+y+12) for x,y in reversed(half[9:])],2))
c=over(c,hexc('#355a8f'),blur(tb,3)*tm,0.0)
spots=circles([(cx-150,wy-318,8),(cx-196,wy-336,6),(cx-110,wy-302,5),(cx+140,wy-326,7),(cx+96,wy-306,5),(cx+190,wy-346,5),(cx-4,wy-160,5),(cx+10,wy-100,4),(cx-12,wy-60,3)])
c=over(c,hexc('#3d5f95'),spots*tm,0.55)
# aurora rim on top edge
c=add(c,hexc('#c5fff0'),outline(tm,8)*np.clip((wy-200-yy)/120,0,1),0.45)
c=over(c,NAVY,outline(tm,2.8),0.95)
if NOTAIL:
    from PIL import Image as _I
    al=np.clip(tm+outline(tm,2.8),0,1)
    ys_,xs_=np.where(al>0.01);x0_,x1_,y0_,y1_=xs_.min()-2,xs_.max()+3,ys_.min()-2,ys_.max()+3
    rgba=np.dstack([np.clip(c,0,1),al])[y0_:y1_,x0_:x1_]
    _I.fromarray((rgba*255+.5).astype(np.uint8),'RGBA').save('fjord_tail.png')
    import json;json.dump({'x0':int(x0_),'y0':int(y0_),'w':int(x1_-x0_),'h':int(y1_-y0_),'wy':wy,'cx':cx},open('fjord_tail.json','w'))
    c=c_pre
# reflection: mirror everything above water
src=np.clip(2*wy-yy.astype(int),0,H-1)
from scipy import ndimage as ndi
disp=(np.sin(yy/3.2+np.sin(xx/90)*2)*2.5+ (noise(10,2,seed=21)-0.5)*10)*np.clip((yy-wy)/120,0,1)
sx=np.clip(xx+disp,0,W-1).astype(int)
refl=c[src,sx]
refl=blur(refl,1.8)
water=vgrad([(0.6,'#1f4679'),(0.8,'#132f5c'),(1,'#081733')])
fade=np.clip((yy-wy)/420,0,1)[...,None]
w=refl*(0.62-0.35*fade)+water*(0.38+0.35*fade)
streak=noise(4,2,seed=5)
streak=ndi.gaussian_filter(streak,(0.6,20))
w=add(w,hexc('#b5dcff'),np.clip((streak-0.55)*4,0,1)*np.clip((yy-wy)/200,0.2,1),0.08)
wm=(yy>=wy).astype(np.float32)
c=c*(1-wm[...,None])+w*wm[...,None]
c=add(c,hexc('#cfeeff'),np.exp(-((yy-wy)/2)**2)*np.exp(-((xx-cx)/500)**2),0.3)
if not NOTAIL:
    # water sheets dripping from flukes
    segs=[]
    for (x0,y0) in [(cx-236,wy-352),(cx-190,wy-346),(cx-140,wy-336),(cx-96,wy-322),(cx+100,wy-330),(cx+150,wy-342),(cx+200,wy-356),(cx+238,wy-362)]:
        Ls=60+r.random()*140;sw=r.random()*6-3
        segs.append([(x0+sw*np.sin(k/40)+k*0.08*np.sign(x0-cx),y0+k) for k in np.linspace(0,Ls,16)])
    sm=lines(segs,1.6,0.4)
    gradfade=np.clip(1-(yy-(wy-360))/260,0,1)
    c=screen(c,hexc('#e6f9ff'),sm*gradfade,0.65)
    drops=[]
    for s_ in segs:
        for k in range(3):
            x,y=s_[-1];drops.append((x+r.random()*4-2,y+18+k*22+r.random()*10,1.2+r.random(),0.8))
    # spray & droplets
    for i in range(150):
        a=r.random()*np.pi;rad=r.random()**0.7*230
        drops.append((cx+np.cos(a)*rad*1.2,wy-np.sin(a)*rad*0.5-r.random()*20,0.7+r.random()*2,0.7+r.random()*0.4))
    dm=np.clip(gauss_dots(drops,0),0,1)
    mist=blur(ellipse(cx,wy-18,200,48),22)
    c=screen(c,hexc('#cdeeff'),mist,0.32)
    c=screen(c,hexc('#f0fcff'),dm,0.95)
    c=add(c,hexc('#8fe6ff'),blur(dm,7),0.45)
    # foam ring
    foam=np.zeros((H,W),np.float32)
    for rx,a in ((70,1),(120,0.7),(190,0.45),(290,0.3),(420,0.18)):
        e=np.sqrt(((xx-cx)/rx)**2+((yy-wy-6)/(rx*0.11))**2)
        foam+=a*np.exp(-((e-1)*rx/2.6)**2)*(yy>wy-2)
    c=add(c,hexc('#d6f2ff'),np.clip(foam,0,1),0.45)
    c=screen(c,hexc('#ffffff'),blur(ellipse(cx,wy+2,46,7),2),0.6)
# glints
gl=[(cx+(r.random()-0.5)*900,wy+12+r.random()**1.5*300,1.0,0.6*r.random()) for i in range(120)]
gm=np.clip(gauss_dots(gl,0),0,1);gm=ndi.gaussian_filter(gm,(0.4,4))*4
c=add(c,hexc('#d8f2ff'),np.clip(gm,0,1),0.5)
# foreground ledge
ledge=[(-10,792),(60,778),(150,770),(250,774),(340,784),(410,800),(452,826),(486,872),(520,940),(548,1034),(-10,1034)]
c,lm=rock(c,chaikin(ledge,2),'#1a2a4d','#2a4373','#101c38',NAVY,seed=7,rim=np.clip((850-yy)/60,0,1),rimcol='#8ff0d0',facets=5)
# flat top highlight
top=poly(chaikin([(10,790),(150,776),(300,782),(400,800),(380,812),(250,800),(120,800),(20,808)],2))
c=over(c,hexc('#30507f'),top*lm,0.6)
# moss tufts & tiny glowing flowers
tufts=[(30+i*37+r.random()*12,792+np.interp(30+i*37,[0,150,300,450],[0,-16,-8,30])+r.random()*4) for i in range(12)]
blades=[]
for x,y in tufts:
    for k in range(5):
        h=8+r.random()*14;dx=(r.random()-0.5)*10
        blades.append([(x+k*2-4,y+2),(x+k*2-4+dx*0.5,y-h*0.5),(x+k*2-4+dx,y-h)])
bm=lines(blades,1.6,0.2)
c=over(c,hexc('#1f4f57'),bm,0.95);c=add(c,hexc('#7fe0c0'),bm*np.clip((800-yy)/30,0,1),0.35)
fl=[(x+r.random()*10-5,y-10-r.random()*6,1.5,1.0) for x,y in tufts[::2]]
fm_=np.clip(gauss_dots(fl,0),0,1)
c=add(c,hexc('#e9fff6'),fm_,0.9);c=add(c,hexc('#7affd0'),blur(fm_,5),0.9)
# vignette
v=np.clip(1-((xx/W-0.5)**2*0.9+(yy/H-0.45)**2*1.1),0,1)
c=c*(0.7+0.3*v[...,None])
save(c,'bg_fjord_notail.png' if NOTAIL else 'bg_fjord.png')
