import numpy as np, json
from PIL import Image
SRC='/home/user/assets_raw/src/'
poses={'read':'read_fixed.png','sleep':SRC+'xixi_sleep.png','eat':SRC+'xixi_eat.png','sew':SRC+'xixi_sew.png','write':SRC+'xixi_write.png',
 'clean':SRC+'xixi_clean.png','pack':SRC+'xixi_pack.png','back':SRC+'xixi_back.png','look':SRC+'xixi_travel_photo.png'}
meta={}
for k,f in poses.items():
    im=np.array(Image.open(f).convert('RGBA')).astype(np.float32)
    a=im[...,3]
    a=np.where(a<6,0,a); a=np.where(a>=236,255,a)
    im[...,3]=a
    ys,xs=np.where(a>8)
    x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
    pad=6
    x0=max(0,x0-pad);y0=max(0,y0-pad);x1=min(im.shape[1],x1+pad);y1=min(im.shape[0],y1+pad)
    crop=Image.fromarray(im[y0:y1,x0:x1].astype(np.uint8),'RGBA')
    crop.save(f'art/fish_{k}.png')
    # feet anchor: lowest opaque rows -> center x of bottom 3% band
    sub=a[y0:y1,x0:x1]
    h=sub.shape[0]; band=sub[int(h*0.9):]>128
    bx=np.where(band.any(0))[0]
    meta[k]={'x0':int(x0),'y0':int(y0),'w':int(x1-x0),'h':int(y1-y0),'cx':float((bx.min()+bx.max())/2/(x1-x0))}
    print(k,meta[k])
json.dump(meta,open('art/pose_meta.json','w'),indent=1)
