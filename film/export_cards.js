const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:430,height:900}});
await p.goto('file:///home/user/work/dist/fatfish-travel.html');await p.waitForTimeout(1500);
const specs=[['beach','pack',null,11],['lighthouse','look','gull',22],['shrine','back',null,31],['coral','look','seal',41],['forest','sleep','crab',52],['onsen','eat','gull',61],['station','read',null,77],['library','read','seal',83],['fjord','back',null,95]];
const out=await p.evaluate(async specs=>{await ready;return specs.map(([d,pose,f,seed])=>paintCard({dest:d,seed,date:'26.10.27',pose,friend:f}))},specs);
out.forEach((u,i)=>fs.writeFileSync(`cards/card_${i}_${specs[i][0]}.jpg`,Buffer.from(u.split(',')[1],'base64')));
await b.close()})();
