// render selected times to jpgs for inspection: node probe.js mode t1 t2 ...
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [mode,...ts]=process.argv.slice(2);const b=await chromium.launch();const W=mode==='h'?1920:1080,H=mode==='h'?1080:1920;
const p=await b.newPage({viewport:{width:W,height:H}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto(`http://127.0.0.1:8765/film/film.html?mode=${mode}`);await p.evaluate(()=>window.filmReady);
const OUT='/tmp/claude-0/-home-user/b4ca9f1e-7b56-5731-96d6-f91b64ef4651/scratchpad/probe/';fs.mkdirSync(OUT,{recursive:true});
for(const t of ts){const t0=Date.now();const u=await p.evaluate(t=>grab(+t,.9),t);fs.writeFileSync(OUT+`${mode}_${String(t).padStart(6,'0')}.jpg`,Buffer.from(u.split(',')[1],'base64'));console.log(t,Date.now()-t0,'ms')}
console.log('errors',errs);await b.close()})();
