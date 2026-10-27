from pt import *
from scipy import ndimage as ndi
NAVY=hexc('#1a2350')
yy,xx=YY,XX
r=np.random.default_rng(12)
c=vgrad([(0,'#b8f3f2'),(0.12,'#79dbe6'),(0.4,'#38a9d1'),(0.66,'#2a86c0')])
# surface shimmer band
wv=np.sin(xx/60+np.sin(xx/23)*1.5)*8+np.sin(xx/17)*3
band=np.exp(-((yy-30-wv)/16)**2)+0.6*np.exp(-((yy-62-wv*0.7)/10)**2)
sh=blur(noise(10,2,seed=2),2)
c=add(c,hexc('#ffffff'),blur(band*(0.5+sh),2),0.35)
c=add(c,hexc('#ffffff'),np.clip(1-yy/70,0,1),0.25)
# god rays
for i in range(9):
    x0=120+i*165+r.random()*60;wid=30+r.random()*60;ang=0.18+r.random()*0.08
    pts=[(x0,-10),(x0+wid,-10),(x0+wid+ang*900+wid*1.5,900),(x0+ang*900-wid*0.5,900)]
    m=blur(poly(pts),18)*np.clip(1-yy/850,0,1)
    c=screen(c,hexc('#fbfff0'),m,0.22+r.random()*0.12)
# distant reef silhouettes
def ridge(y0,amp,seed,smooth,n=60):
    rr=np.random.default_rng(seed);p=[(0,H)];v=0
    for i in range(n+1):
        v=v*smooth+(rr.random()-0.5)*amp;p.append((i*W/n,y0+v-abs(np.sin(i*0.7))*amp*0.6))
    return p+[(W,H)]
m=poly(ridge(560,70,3,0.6),1.2);c=over(c,hexc('#4f9fcc'),m,0.7)
m=poly(ridge(620,60,8,0.5),0.8);c=over(c,hexc('#5aa6c9'),m,0.85)
# small far fish school silhouettes
for i in range(26):
    x=900+r.random()*420+np.sin(i)*30;y=230+r.random()*120
    fm=ellipse(x,y,7,3)+poly([(x-6,y),(x-12,y-4),(x-12,y+4)])
    c=over(c,hexc('#2f7fb3'),np.clip(fm,0,1),0.55)
# sand floor
sy=660
sand_top=[(0,sy+10)]+[(x,sy+12*np.sin(x/180)+6*np.sin(x/57)) for x in range(0,W+1,24)]+[(W,H),(0,H)]
sm=poly(sand_top,0.6)
sand=vgrad([(0.62,'#cfe0d6'),(0.72,'#f0e4c4'),(1,'#f6e9cb')])
c=over(c,sand,sm)
# caustics on sand (perspective-compressed)
py=np.clip((yy-sy)/(H-sy),0.001,1)
u=xx/ (40+60*py); v=(yy-sy)/(14+30*py)
cau=np.abs(np.sin(u+1.7*np.sin(v*0.9+u*0.3))+np.sin(v*1.3+1.4*np.sin(u*0.8)))
cau=np.exp(-cau*3.2)
c=add(c,hexc('#ffffff'),cau*sm*(0.2+0.35*py),0.38)
c=add(c,hexc('#ffffff'),np.exp(-((yy-sy-8)/10)**2)*sm,0.1)
# sand ripples & pebbles
pb=circles([(r.random()*W,sy+40+r.random()**0.7*(H-sy-40),2+r.random()*4) for i in range(60)])
c=over(c,hexc('#c9b48e'),pb,0.6)
# blue haze above sand
c=over(c,hexc('#58acd2'),np.exp(-((yy-sy+10)/26)**2),0.25)
# coral helpers
def branch_coral(c,x,y,scale,col,dark,seed):
    rr=np.random.default_rng(seed);segs=[]
    def br(x,y,a,L,d,w):
        x2=x+np.cos(a)*L;y2=y+np.sin(a)*L
        segs.append(([(x,y),((x+x2)/2+rr.random()*6-3,(y+y2)/2),(x2,y2)],w))
        if d>0:
            for k in range(2+(rr.random()<0.35)):
                br(x2,y2,a+(k-0.5)*0.7+(rr.random()-0.5)*0.4,L*(0.68+rr.random()*0.15),d-1,w*0.78)
    for k in range(3):br(x+(k-1)*12*scale,y,-np.pi/2+(k-1)*0.45,62*scale,3,18*scale)
    m=np.zeros((H,W),np.float32)
    for pts,w in segs:m=np.maximum(m,lines([pts],w))
    c=over(c,hexc(col),m)
    # shading: darker on right/bottom using shifted mask
    sh=np.clip(m-np.roll(np.roll(m,-4,1),4,0),0,1)
    c=over(c,hexc(dark),sh,0.6)
    hl=np.clip(m-np.roll(np.roll(m,3,1),-3,0),0,1)
    c=add(c,hexc('#ffffff'),hl,0.25)
    # polyps dots
    dots=[]
    for pts,w in segs[::2]:
        x2,y2=pts[-1];dots.append((x2,y2,w*0.28,0.9))
    c=add(c,hexc('#fff3f6'),np.clip(gauss_dots(dots,0),0,1)*m,0.5)
    c=over(c,NAVY,outline(m,2.4),0.9)
    return c
def brain_coral(c,x,y,rx,ry,col,dark):
    rr=np.random.default_rng(int(x))
    balls=[]
    for k in range(int(rx/7)):
        a=rr.random()*np.pi;d=rr.random()**0.6
        bx=x+np.cos(a)*rx*d*0.85;by=y-np.sin(a)*ry*d*0.9;br=rx*(0.16+rr.random()*0.12)
        balls.append((bx,by,br))
    balls.sort(key=lambda b:b[1])
    allm=np.zeros((H,W),np.float32)
    for bx,by,br in balls:
        m=circles([(bx,by,br)])
        c=over(c,hexc(col),m)
        c=over(c,hexc(dark),m*np.clip(((yy-by)/br+0.2),0,1),0.5)
        c=add(c,hexc('#ffffff'),circles([(bx-br*0.35,by-br*0.4,br*0.28)],1),0.55)
        c=over(c,NAVY,outline(m,1.8),0.75)
        allm=np.maximum(allm,m)
    c=over(c,NAVY,outline(allm,2.4),0.9)
    return c
def fan_coral(c,x,y,s,col,seed):
    rr=np.random.default_rng(seed);segs=[]
    for k in range(14):
        a=-np.pi/2+(k-6.5)*0.13
        pts=[(x,y)];px,py_=x,y
        for j in range(6):
            px+=np.cos(a+(rr.random()-0.5)*0.4)*22*s;py_+=np.sin(a)*22*s;pts.append((px,py_))
        segs.append(pts)
    m=lines(segs,3.2*s)
    # lattice fill
    fill=np.clip(blur(m,7*s)*3,0,1)
    c=over(c,hexc(col),fill,0.35)
    c=over(c,hexc(col),m,0.95)
    c=over(c,NAVY,outline(m,1.6),0.6)
    return c
def anemone(c,x,y,s,col,tip):
    segs=[]
    for k in range(16):
        a=-np.pi/2+(k-7.5)*0.16
        L=46*s*(0.8+0.2*np.cos(k))
        pts=[(x,y)]+[(x+np.cos(a)*L*t+np.sin(t*3+k)*5*s,y+np.sin(a)*L*t) for t in (0.35,0.7,1.0)]
        segs.append(pts)
    m=lines(segs,7*s)
    c=over(c,hexc(col),m)
    tips=[(p[-1][0],p[-1][1],4*s,1) for p in segs]
    tm=np.clip(gauss_dots(tips,0)*2,0,1)
    c=over(c,hexc(tip),tm,0.9)
    base=ellipse(x,y+4*s,24*s,12*s);c=over(c,hexc('#7a4fa0'),base);c=over(c,NAVY,outline(np.clip(m+base,0,1),2.2),0.9)
    return c
def kelp(c,x,y,h,seed):
    rr=np.random.default_rng(seed);segs=[]
    for k in range(3):
        pts=[(x+k*14+np.sin(t/40+k)*12,y-t) for t in np.linspace(0,h*(0.7+0.3*rr.random()),20)]
        segs.append(pts)
    m=lines(segs,9)
    c=over(c,hexc('#3f9b7a'),m);c=add(c,hexc('#b5ffd9'),np.clip(m-np.roll(m,3,1),0,1),0.3);c=over(c,NAVY,outline(m,2),0.8)
    return c
# back layer corals (smaller, hazier) at mid depth
for x,col,dk,s in [(170,'#f39ab0','#c66a8a',0.7),(1360,'#f7b07a','#c97c4f',0.75),(520,'#c58ad6','#8f5aa8',0.55)]:
    c=branch_coral(c,x,sy+8,s,col,dk,int(x))
c=over(c,hexc('#5fb3d6'),np.ones((H,W),np.float32)*(yy<sy+40),0.12)
# kelp sides
c=kelp(c,40,H,520,1);c=kelp(c,1460,H,560,2)
# foreground coral clusters left & right (leave center open)
c=fan_coral(c,120,820,1.3,'#b26fd0',3)
c=branch_coral(c,250,870,1.25,'#ff8fa6','#d0607e',5)
c=brain_coral(c,90,900,110,70,'#f6a25c','#c7743a')
c=anemone(c,380,930,1.7,'#ff9eb8','#fff0b0')
c=branch_coral(c,1320,860,1.3,'#ff9b6b','#cf6a3f',9)
c=fan_coral(c,1450,830,1.2,'#e07ab8',4)
c=brain_coral(c,1420,940,120,66,'#c58ad6','#9058ad')
c=anemone(c,1180,950,1.4,'#7fd0ff','#fffbd0')
c=brain_coral(c,620,980,70,40,'#f7c66a','#c99a3d')
# star fish & shells on sand
def starfish(c,x,y,s,col):
    pts=[]
    for k in range(10):
        a=-np.pi/2+k*np.pi/5;rad=(22 if k%2==0 else 9)*s
        pts.append((x+np.cos(a)*rad,y+np.sin(a)*rad*0.7))
    m=poly(chaikin(pts,1));c=over(c,hexc(col),m);c=add(c,hexc('#ffffff'),np.clip(gauss_dots([(x+p[0]*0,y,0,0) for p in []],0),0,1));c=over(c,NAVY,outline(m,2),0.9);return c
c=starfish(c,860,930,1.2,'#ff8a6b');c=starfish(c,1010,1000,0.9,'#ffc75a')
# fish
def fish(c,x,y,s,body,stripe,d=1):
    m=ellipse(x,y,26*s,15*s);t=poly([(x-20*s*d,y),(x-40*s*d,y-14*s),(x-40*s*d,y+14*s)])
    fin=poly([(x-4*s*d,y-12*s),(x+8*s*d,y-22*s),(x+12*s*d,y-12*s)])
    allm=np.clip(m+t+fin,0,1)
    c=over(c,hexc(body),allm)
    st=m*np.clip(1-np.abs(xx-(x+4*s*d))/(4*s),0,1)
    c=over(c,hexc(stripe),st,0.9)
    c=add(c,hexc('#ffffff'),m*np.clip(1-((xx-x)**2/(26*s)**2+(yy-y+7*s)**2/(6*s)**2),0,1),0.4)
    c=over(c,NAVY,outline(allm,2),0.9)
    e=circles([(x+14*s*d,y-3*s,3.2*s)]);c=over(c,hexc('#1a2350'),e);c=add(c,hexc('#ffffff'),circles([(x+15*s*d,y-4*s,1.1*s)]),1)
    return c
for x,y,s,b,st_,d in [(430,330,1.0,'#ffd34d','#ffffff',1),(500,370,0.8,'#ffd34d','#ffffff',1),(1080,260,1.1,'#ff9248','#ffffff',-1),(1150,300,0.8,'#ff9248','#ffffff',-1),(760,180,0.7,'#7fd8ff','#2b6fd0',1),(300,520,0.75,'#ff8fb1','#ffffff',1),(1250,480,0.9,'#b6f06a','#2b8a4a',-1)]:
    c=fish(c,x,y,s,b,st_,d)
# bubbles
bm=np.zeros((H,W),np.float32);hl=np.zeros((H,W),np.float32)
for i in range(46):
    x=r.random()*W;y=r.random()*700;rad=3+r.random()**2*14
    ring=np.exp(-((np.sqrt((xx-x)**2+(yy-y)**2)-rad)/1.1)**2) if False else None
    bm+=circles([(x,y,rad)])-circles([(x,y,rad-1.6)])
    hl+=circles([(x-rad*0.35,y-rad*0.35,rad*0.25)])
c=screen(c,hexc('#ffffff'),np.clip(bm,0,1),0.75);c=screen(c,hexc('#ffffff'),np.clip(hl,0,1),0.9)
# vignette + slight blue tint at bottom corners
v=np.clip(1-((xx/W-0.5)**2*0.8+(yy/H-0.4)**2*0.9),0,1)
c=c*(0.78+0.22*v[...,None])
save(c,'bg_coral.png')
