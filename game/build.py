#!/usr/bin/env python3
"""Build the single-file game: inline friend/souvenir SVG modules, pose metadata and webp assets (+ optional bgm)."""
import base64, json, os, re, sys
here=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(here,'src.html'),encoding='utf-8').read()
assets=os.path.join(here,'..','gassets')
def durl(path,mime):
    return f'data:{mime};base64,'+base64.b64encode(open(path,'rb').read()).decode()
fr=open(os.path.join(here,'friends.js'),encoding='utf-8').read().replace("if(typeof module!=='undefined')module.exports=FR_SVG;","")
sv=open(os.path.join(here,'svg_souv.js'),encoding='utf-8').read()
src=src.replace('/*__FRIENDS__*/',fr).replace('/*__SOUV__*/',sv)
meta=json.load(open(os.path.join(here,'..','art','pose_meta.json')))
src=src.replace('__POSE_META__',json.dumps(meta,separators=(',',':')))
for m in set(re.findall(r'__IMG_(\w+?)__',src)):
    src=src.replace(f'__IMG_{m}__',durl(os.path.join(assets,m+'.webp'),'image/webp'))
bgm=os.path.join(assets,'bgm.mp3')
if os.path.exists(bgm):src=src.replace('__BGM__',durl(bgm,'audio/mpeg'))
args=[a for a in sys.argv[1:] if not a.startswith('--')]
if '--artifact' in sys.argv:
    # artifact host wraps the page in its own skeleton: drop document-level tags and our viewport meta
    for tag in ['<!doctype html>\n','<html lang="zh-CN">\n','<head>\n','</head>\n','<body>\n','</body>\n','</html>\n','<meta charset="utf-8">\n','<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n']:
        src=src.replace(tag,'')
out=args[0] if args else os.path.join(here,'..','dist','fatfish-travel.html')
os.makedirs(os.path.dirname(out),exist_ok=True)
open(out,'w',encoding='utf-8').write(src)
print(out,len(src)//1024,'KB')
