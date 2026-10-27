import numpy as np, sys
from PIL import Image
from scipy import ndimage as ndi
src,dst=sys.argv[1],sys.argv[2]
a=np.array(Image.open(src).convert('RGB')).astype(np.float32)
mx=a.max(2)
dark=mx<22
lab,n=ndi.label(dark)
sizes=ndi.sum(np.ones_like(mx),lab,range(1,n+1))
bg=np.isin(lab,1+np.where(sizes>150)[0])
fg=~bg
fg=ndi.binary_opening(fg,iterations=1)
fg=ndi.binary_fill_holes(fg)|fg  # keep (holes that are bg components already excluded above)
fg=fg&~bg|ndi.binary_closing(fg,iterations=1)&~bg
# signed distance for AA outline
d_out=ndi.distance_transform_edt(~fg)   # distance outside fg
navy=np.array([24,28,66],np.float32)
OUT=2.6
alpha=np.clip(OUT+0.5-d_out,0,1)
alpha[fg]=1
col=a.copy()
# recolor dark edge pixels inside fg to navy to remove speckle
d_in=ndi.distance_transform_edt(fg)
edge_in=(fg)&(d_in<=2.5)
col[edge_in]=col[edge_in]*0.35+navy*0.65
col[~fg]=navy
out=np.dstack([np.clip(col,0,255),alpha*255]).astype(np.uint8)
Image.fromarray(out,'RGBA').save(dst)
