const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();
for(const mode of ['h','v']){const W=mode==='h'?1920:1080,H=mode==='h'?1080:1920;const p=await b.newPage({viewport:{width:W,height:H}});
 await p.goto(`http://127.0.0.1:8765/film/film.html?mode=${mode}`);await p.evaluate(()=>window.filmReady);
 const u=await p.evaluate(()=>renderCover());fs.writeFileSync(`cover_${mode}_full.jpg`,Buffer.from(u.split(',')[1],'base64'));await p.close()}
await b.close()})();
