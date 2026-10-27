// friend critters as SVG strings (viewBox 0 0 120 110), navy lineart style
const FR_SVG={
crab:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 110"><g stroke="#1f3468" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">
<path d="M30 92 l-8 10 M40 95 l-4 11 M80 95 l4 11 M90 92 l8 10" fill="none"/>
<path d="M60 22c22 0 40 16 40 38 0 20-14 34-40 34S20 80 20 60c0-22 18-38 40-38z" fill="#f6c3b4"/>
<path d="M60 30c16 0 28 11 28 26 0 13-10 22-26 22-12 0-20-7-20-17 0-9 7-15 16-15 7 0 12 4 12 10 0 5-4 8-8 8" fill="none" stroke="#d98e7d"/>
<path d="M60 22c22 0 40 16 40 38 0 20-14 34-40 34S20 80 20 60c0-22 18-38 40-38z" fill="none"/>
<path d="M24 84c4-10 14-14 22-12l-2 18c-8 2-16 0-20-6z" fill="#ee7f6a"/>
<path d="M18 70c-8-2-14 2-14 9 0 6 6 9 11 7l5-5c-4 0-7-2-6-5 1-3 5-3 7-1z" fill="#ee7f6a"/>
<path d="M34 72 l-4-20 M44 70 l2-20" fill="none"/>
<ellipse cx="30" cy="50" rx="6.5" ry="7.5" fill="#fff"/><ellipse cx="46" cy="48" rx="6.5" ry="7.5" fill="#fff"/></g>
<ellipse cx="31" cy="51" rx="3.2" ry="4.2" fill="#1f3468"/><ellipse cx="47" cy="49" rx="3.2" ry="4.2" fill="#1f3468"/>
<circle cx="32.3" cy="49" r="1.3" fill="#fff"/><circle cx="48.3" cy="47" r="1.3" fill="#fff"/>
<ellipse cx="34" cy="84" rx="4" ry="2.4" fill="#ffb3c0" opacity=".9"/>
<path d="M36 80q3 3 6 0" stroke="#1f3468" stroke-width="2.2" fill="none" stroke-linecap="round"/>
<path d="M70 38q6-4 12 0" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/></svg>`,
gull:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 110"><g stroke="#1f3468" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">
<path d="M50 96v8h-7M68 96v8h7" fill="none" stroke="#e8962f"/>
<path d="M90 56c14 2 22 14 20 26-10-2-18-8-22-16z" fill="#c9d3e3"/>
<path d="M60 18c22 0 36 18 36 42 0 22-14 38-36 38S24 82 24 60c0-24 14-42 36-42z" fill="#fff"/>
<path d="M30 56c-14 2-22 14-20 26 10-2 18-8 22-16z" fill="#c9d3e3"/>
<path d="M30 70q30 14 60 0" fill="none" stroke="#1f3468" stroke-width="7"/>
<path d="M72 74l10 14 6-12z" fill="#1f3468"/>
<path d="M51 49q9-6 18 0q-9 11-18 0z" fill="#f6c24a"/></g>
<path d="M32 70q28 12 56 0" fill="none" stroke="#3f63a8" stroke-width="3"/>
<circle cx="46" cy="40" r="4.4" fill="#1f3468"/><circle cx="74" cy="40" r="4.4" fill="#1f3468"/>
<circle cx="47.5" cy="38.5" r="1.5" fill="#fff"/><circle cx="75.5" cy="38.5" r="1.5" fill="#fff"/>
<circle cx="64" cy="52" r="1.7" fill="#e05050"/>
<ellipse cx="37" cy="52" rx="5" ry="3" fill="#ffb3c0" opacity=".9"/><ellipse cx="83" cy="52" rx="5" ry="3" fill="#ffb3c0" opacity=".9"/>
<path d="M54 18c2-8 10-10 12-4" stroke="#1f3468" stroke-width="3" fill="none" stroke-linecap="round"/></svg>`,
seal:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 110"><g stroke="#1f3468" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">
<path d="M96 86c10-2 18 4 20 12-8 2-16 0-22-6z" fill="#e9eef7"/>
<path d="M60 26c26 0 44 18 44 42 0 22-18 34-44 34S16 90 16 68c0-24 18-42 44-42z" fill="#f7f9fd"/>
<path d="M30 84c-8 2-14 10-12 16 8 0 14-4 18-10z" fill="#e9eef7"/>
<path d="M84 84c8 2 14 10 12 16-8 0-14-4-18-10z" fill="#e9eef7"/></g>
<circle cx="80" cy="40" r="3" fill="#c9d3e3"/><circle cx="88" cy="50" r="2.2" fill="#c9d3e3"/><circle cx="30" cy="44" r="2.4" fill="#c9d3e3"/>
<ellipse cx="45" cy="58" rx="6.5" ry="8" fill="#1f3468"/><ellipse cx="75" cy="58" rx="6.5" ry="8" fill="#1f3468"/>
<circle cx="47.5" cy="54.5" r="2.4" fill="#fff"/><circle cx="77.5" cy="54.5" r="2.4" fill="#fff"/><circle cx="43.5" cy="61" r="1.1" fill="#fff"/><circle cx="73.5" cy="61" r="1.1" fill="#fff"/>
<ellipse cx="60" cy="68" rx="4.5" ry="3.2" fill="#1f3468"/>
<path d="M55 73q5 5 10 0" stroke="#1f3468" stroke-width="2.4" fill="none" stroke-linecap="round"/>
<path d="M50 69h-14M50 72l-13 4M70 69h14M70 72l13 4" stroke="#9aa6bf" stroke-width="1.6" stroke-linecap="round"/>
<ellipse cx="36" cy="72" rx="6" ry="3.4" fill="#ffb3c0" opacity=".9"/><ellipse cx="84" cy="72" rx="6" ry="3.4" fill="#ffb3c0" opacity=".9"/>
<path d="M44 34q8-6 16-2" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/></svg>`
};
if(typeof module!=='undefined')module.exports=FR_SVG;
