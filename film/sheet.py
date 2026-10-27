import sys,glob
from PIL import Image
files=sys.argv[2:];out=sys.argv[1]
ims=[Image.open(f) for f in files];w,h=ims[0].size
cols=3 if w>h else 4;sc=640/w if w>h else 360/w
tw,th=int(w*sc),int(h*sc);rows=(len(ims)+cols-1)//cols
o=Image.new('RGB',(cols*tw,rows*th))
for i,im in enumerate(ims):o.paste(im.resize((tw,th)),((i%cols)*tw,(i//cols)*th))
o.save(out,quality=88)
