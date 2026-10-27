// node render.js mode workers  -> frames_<mode>/%05d.jpg at 30fps
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const mode=process.argv[2]||'h',NW=+(process.argv[3]||4),FPS=30;
const W=mode==='h'?1920:1080,H=mode==='h'?1080:1920;
const OUT=path.join(__dirname,'frames_'+mode);fs.mkdirSync(OUT,{recursive:true});
(async()=>{
  const b=await chromium.launch();
  const dur=await (async()=>{const p=await b.newPage({viewport:{width:W,height:H}});await p.goto(`http://127.0.0.1:8765/film/film.html?mode=${mode}`);await p.evaluate(()=>window.filmReady);const d=await p.evaluate(()=>window.DUR);await p.close();return d})();
  const N=Math.round(dur*FPS);const t0=Date.now();let done=0;
  const todo=[];for(let i=0;i<N;i++){if(!fs.existsSync(path.join(OUT,`${String(i).padStart(5,'0')}.jpg`)))todo.push(i)}
  console.log('frames',N,'todo',todo.length);
  const chunk=Math.ceil(todo.length/NW);
  await Promise.all(Array.from({length:NW},async(_,w)=>{
    const mine=todo.slice(w*chunk,(w+1)*chunk);if(!mine.length)return;
    const p=await b.newPage({viewport:{width:W,height:H}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
    await p.goto(`http://127.0.0.1:8765/film/film.html?mode=${mode}`);await p.evaluate(()=>window.filmReady);
    for(const i of mine){const u=await p.evaluate(t=>grab(t,.94),i/FPS);fs.writeFileSync(path.join(OUT,`${String(i).padStart(5,'0')}.jpg`),Buffer.from(u.split(',')[1],'base64'));
      if(++done%150===0)console.log(done,'/',todo.length,((Date.now()-t0)/done).toFixed(0),'ms/frame avg');}
    if(errs.length)console.log('worker',w,'errors',errs.slice(0,3));await p.close()}));
  console.log('done in',((Date.now()-t0)/1000).toFixed(0),'s');await b.close()})().catch(e=>{console.error(e);process.exit(1)});
