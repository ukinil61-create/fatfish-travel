from pt import *
from scipy import ndimage as ndi
NAVY=hexc('#2a2a5a')
yy,xx=YY,XX
r=np.random.default_rng(21)
c=vgrad([(0,'#9fc0f2'),(0.35,'#c9d4f7'),(0.6,'#f6d2e4'),(0.75,'#ffe4d6')])
c=add(c,hexc('#fff3dd'),radial(1060,520,520,1.6),0.45)
c=add(c,hexc('#ffffff'),radial(1060,520,120,1.2),0.5)
# tiny stars in upper sky
pts=[(r.random()*W,r.random()*300,0.8+r.random(),0.5) for i in range(40)]
c=add(c,hexc('#ffffff'),np.clip(gauss_dots(pts,0),0,1),0.6)
def cloud(c,cx,cy,w,h,seed,light='#ffffff',mid='#f3eafa',shadow='#cbbfe8',line='#a99cd6',outline_a=0.6,nb=14):
    rr=np.random.default_rng(seed)
    balls=[]
    for k in range(nb):
        t=k/(nb-1)
        bx=cx-w/2+t*w+(rr.random()-0.5)*w*0.08
        top=np.sin(t*np.pi)**0.7
        br=h*(0.35+0.45*top)*(0.75+rr.random()*0.4)
        by=cy-top*h*0.35+rr.random()*h*0.1
        balls.append((bx,by,br))
    base=poly([(cx-w/2-h*0.3,cy+h*0.05),(cx+w/2+h*0.3,cy+h*0.05),(cx+w/2,cy+h*0.4),(cx-w/2,cy+h*0.4)])
    m=np.clip(circles(balls)+base,0,1)
    m=m*(yy<cy+h*0.42)
    c=over(c,hexc(mid),m)
    # per-ball highlight
    # draw balls back-to-front: each ball lit top-left, shaded at its bottom, thin crease line
    order=sorted(balls,key=lambda b:-b[2])
    for bx,by,br in order:
        bm=circles([(bx,by,br)])*m
        c=over(c,hexc(mid),bm)
        c=over(c,hexc(light),circles([(bx-br*0.1,by-br*0.2,br*0.88)],6)*bm,0.95)
        c=over(c,hexc(shadow),bm*np.clip((yy-by-br*0.35)/(br*0.8),0,1),0.3)
        c=over(c,hexc(line),blur(outline(bm,1.6),0.8)*(yy<by)*(yy>by-br),0.12)
    sh=np.clip((yy-(cy+h*0.05))/(h*0.35),0,1)*m
    c=over(c,hexc(shadow),sh,0.6)
    c=over(c,hexc(line),outline(m,2.2),outline_a)
    return c,m
# far clouds (pinkish, low contrast)
for i,(x,y,w,h) in enumerate([(200,420,380,90),(700,380,300,70),(1350,430,420,100),(1000,300,220,50),(380,250,200,46)]):
    c,_=cloud(c,x,y,w,h,i+40,light='#fff6fb',mid='#f7e4f1',shadow='#e6cde6',line='#d7bfe0',outline_a=0.35,nb=10)
# bookshelf helper
BOOKC=['#e98a8a','#7fa7e0','#f2c25b','#8cc59a','#b48bd6','#f5a3c7','#6fc3c9','#f09a5a']
def shelf(c,x,y,w,h,rows,angle_seed,tilt=0.0):
    rr=np.random.default_rng(angle_seed)
    # frame
    def rot(px,py):
        ca,sa=np.cos(tilt),np.sin(tilt);dx,dy=px-x,py-y
        return (x+dx*ca-dy*sa,y+dx*sa+dy*ca)
    def rpoly(pts):return poly([rot(*p) for p in pts])
    outer=rpoly([(x-w/2,y-h),(x+w/2,y-h),(x+w/2,y),(x-w/2,y)])
    top=rpoly([(x-w/2-10,y-h-14),(x+w/2+10,y-h-14),(x+w/2+10,y-h),(x-w/2-10,y-h)])
    c=over(c,hexc('#8a5a44'),outer)
    inner_h=(h-16)/rows
    allm=np.clip(outer+top,0,1)
    for k in range(rows):
        iy=y-h+8+k*inner_h
        back=rpoly([(x-w/2+9,iy),(x+w/2-9,iy),(x+w/2-9,iy+inner_h-8),(x-w/2+9,iy+inner_h-8)])
        c=over(c,hexc('#5c3a30'),back)
        bx=x-w/2+11
        while bx<x+w/2-20:
            bw=8+rr.random()*9;bh=(inner_h-8)*(0.62+rr.random()*0.36)
            if rr.random()<0.12:  # leaning book
                bpts=[(bx,iy+inner_h-8),(bx+bw,iy+inner_h-8),(bx+bw+bh*0.35,iy+inner_h-8-bh*0.95),(bx+bh*0.35,iy+inner_h-8-bh)]
            else:
                bpts=[(bx,iy+inner_h-8-bh),(bx+bw,iy+inner_h-8-bh),(bx+bw,iy+inner_h-8),(bx,iy+inner_h-8)]
            bm=rpoly(bpts)
            col=BOOKC[int(rr.random()*len(BOOKC))]
            c=over(c,hexc(col),bm)
            band=rpoly([(bx,iy+inner_h-8-bh*0.75),(bx+bw,iy+inner_h-8-bh*0.75),(bx+bw,iy+inner_h-8-bh*0.68),(bx,iy+inner_h-8-bh*0.68)])
            c=over(c,hexc('#fff3d0'),band*bm,0.8)
            c=over(c,NAVY,outline(bm,1.2),0.6)
            bx+=bw+1+(bh*0.35 if len(bpts) and bpts[2][0]>bx+bw+1 else 0)
        board=rpoly([(x-w/2,iy+inner_h-8),(x+w/2,iy+inner_h-8),(x+w/2,iy+inner_h),(x-w/2,iy+inner_h)])
        c=over(c,hexc('#a8714f'),board);c=add(c,hexc('#ffffff'),board*(np.roll(board,3,0)<0.5),0.25)
    c=over(c,hexc('#a8714f'),top);c=add(c,hexc('#ffe0c0'),top*(np.roll(top,4,0)<0.5),0.4)
    c=over(c,NAVY,outline(allm,2.4),0.9)
    return c
def flying_book(c,x,y,s,col,flap,seed):
    # open book: two page wings + cover
    wl=[(x,y),(x-34*s,y-18*s*flap),(x-38*s,y-4*s*flap+6*s),(x-4*s,y+12*s)]
    wr=[(x,y),(x+34*s,y-18*s*flap),(x+38*s,y-4*s*flap+6*s),(x+4*s,y+12*s)]
    cov_l=[(x,y+4*s),(x-38*s,y-12*s*flap+4*s),(x-42*s,y+2*s),(x-2*s,y+16*s)]
    cov_r=[(p[0]*-1+2*x,p[1]) for p in cov_l]
    m=np.clip(poly(cov_l)+poly(cov_r),0,1);c=over(c,hexc(col),m)
    p=np.clip(poly(wl)+poly(wr),0,1);c=over(c,hexc('#fffaf0'),p)
    c=over(c,hexc('#d9cfe6'),p*np.clip(1-np.abs(xx-x)/(6*s),0,1),0.6)
    al=np.clip(m+p,0,1);c=over(c,NAVY,outline(al,1.6),0.85)
    return c
# floating shelves on small clouds
c,_=cloud(c,300,610,260,60,3)
c=shelf(c,300,590,190,250,3,1,-0.05)
c,_=cloud(c,1240,560,240,58,4)
c=shelf(c,1240,540,170,220,3,2,0.06)
c,_=cloud(c,770,420,200,46,5)
c=shelf(c,770,404,250,120,1,3,0.0)
c,_=cloud(c,520,250,150,36,6)
c=shelf(c,520,238,140,90,1,4,-0.1)
c,_=cloud(c,1030,200,150,36,7)
c=shelf(c,1030,186,120,100,1,5,0.12)
# flying books
for i,(x,y,s,f) in enumerate([(640,120,1.6,1),(740,175,1.0,-0.4),(1330,240,1.4,0.8),(130,290,1.3,-0.7),(950,330,0.9,1),(1450,130,1.1,0.2),(430,430,1.0,0.9),(880,80,0.8,-0.6)]):
    c=flying_book(c,x,y,s,BOOKC[i%len(BOOKC)],f,i)
# sparkles around books
sp=[]
for i in range(60):sp.append((r.random()*W,r.random()*600,0.9+r.random()*1.4,0.8))
spm=np.clip(gauss_dots(sp,0),0,1);c=add(c,hexc('#fffbe8'),spm,0.8);c=add(c,hexc('#ffe7f5'),blur(spm,4),0.6)
# ground cloud surface (big, layered)
c,_=cloud(c,260,820,700,170,11,nb=16)
c,_=cloud(c,1250,800,760,180,12,nb=16)
c,_=cloud(c,760,860,900,190,13,nb=18)
# flat-ish fill to bottom
bot=(yy>900).astype(np.float32)
c=over(c,vgrad([(0.85,'#f7f0fb'),(1,'#ece2f7')]),blur(bot,6))
c,_=cloud(c,180,1010,520,120,14,nb=12)
c,_=cloud(c,1380,1020,560,120,15,nb=12)
# soft glow overall
v=np.clip(1-((xx/W-0.5)**2*0.7+(yy/H-0.45)**2*0.7),0,1)
c=c*(0.9+0.1*v[...,None])
save(c,'bg_library.png')
