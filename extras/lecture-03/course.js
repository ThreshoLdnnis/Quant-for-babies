'use strict';
// All chart observations are synthetic teaching values, never market observations.
const progressBar = document.querySelector('.progress-bar');
const progressLabel = document.querySelector('.progress-label');
let scheduled = false;
function updateProgress() {
  const extent = document.documentElement.scrollHeight - window.innerHeight;
  const progress = extent > 0 ? Math.min(100, Math.max(0, window.scrollY / extent * 100)) : 100;
  progressBar.style.width = `${progress}%`;
  progressLabel.textContent = `已阅读 ${Math.round(progress)}%`;
  scheduled = false;
}
window.addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(updateProgress); } }, { passive: true });
window.addEventListener('resize', updateProgress);
updateProgress();
const chapters = [...document.querySelectorAll('main section[id]')];
const tocLinks = [...document.querySelectorAll('.toc a')];
const observer = new IntersectionObserver(entries => {
  const visible = entries.filter(e => e.isIntersecting).sort((a,b) => a.boundingClientRect.top - b.boundingClientRect.top);
  if (!visible.length) return;
  tocLinks.forEach(a => { if (a.hash === `#${visible[0].target.id}`) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
}, {rootMargin:'-90px 0px -65% 0px', threshold:0});
chapters.forEach(s => observer.observe(s));
async function copyCodeText(content) {
  if (navigator.clipboard?.writeText && window.isSecureContext) {
    try { await navigator.clipboard.writeText(content); return; }
    catch { /* Local-file clipboard access can be denied; try selection below. */ }
  }
  const area = document.createElement('textarea');
  area.value = content; area.style.position = 'fixed'; area.style.opacity = '0';
  document.body.append(area);
  try { area.select(); if (!document.execCommand('copy')) throw new Error('copy unavailable'); }
  finally { area.remove(); }
}
document.querySelectorAll('pre').forEach((pre, index) => {
  const wrapper = document.createElement('div'); wrapper.className = 'codebox';
  pre.parentNode.insertBefore(wrapper, pre);
  const header = document.createElement('div'); header.className = 'code-head';
  const label = document.createElement('span'); label.textContent = pre.dataset.label || (pre.querySelector('code')?.className.replace('language-', '').toUpperCase() || 'CODE');
  const button = document.createElement('button'); button.className = 'copy-btn'; button.type = 'button'; button.textContent = '复制代码'; button.setAttribute('aria-label', `复制第 ${index + 1} 段代码`);
  header.append(label, button); wrapper.append(header,pre);
  button.addEventListener('click', async () => {
    const content = pre.textContent;
    try {
      await copyCodeText(content);
      button.textContent = '已复制 ✓';
    } catch { button.textContent = '请选中代码复制'; }
    setTimeout(() => { button.textContent = '复制代码'; }, 2400);
  });
});
document.querySelector('.to-top').addEventListener('click', () => window.scrollTo({top:0, behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'}));
// Controlled synthetic examples, separate from real security data.
function svgElement(name, attrs={}, text='') {
  const e=document.createElementNS('http://www.w3.org/2000/svg',name);
  for(const [key,value] of Object.entries(attrs)) e.setAttribute(key,value);
  if(text) e.textContent=text;
  return e;
}
const demoPrices=Array.from({length:41},(_,i)=>10+0.05*i+0.18*Math.sin(Math.PI*i/10));
function renderMomentum() {
  const end=Number(document.querySelector('#momentum-end').value), start=end-20;
  const x=i=>55+i*600/end, y=v=>220-(v-9.5)*65;
  const layer=document.querySelector('#momentum-chart .plot'); layer.replaceChildren();
  layer.append(svgElement('rect',{x:x(start),y:20,width:x(end)-x(start),height:205,fill:'#edf5ef'}));
  [10,11,12].forEach(v=>layer.append(svgElement('line',{x1:55,y1:y(v),x2:655,y2:y(v),stroke:'#dbe7e2'}),svgElement('text',{x:40,y:y(v)+4,'text-anchor':'end',fill:'#526a79','font-size':12},String(v))));
  layer.append(svgElement('polyline',{points:demoPrices.slice(0,end+1).map((v,i)=>`${x(i)},${y(v)}`).join(' '),fill:'none',stroke:'#a6bdb7','stroke-width':2}));
  layer.append(svgElement('polyline',{points:demoPrices.slice(start,end+1).map((v,i)=>`${x(i+start)},${y(v)}`).join(' '),fill:'none',stroke:'#087e83','stroke-width':3}));
  [start,end].forEach(i=>layer.append(svgElement('circle',{cx:x(i),cy:y(demoPrices[i]),r:5,fill:'#a67735'})));
  [...new Set([0,start,end])].forEach(i=>layer.append(svgElement('text',{x:x(i),y:249,'text-anchor':'middle',fill:'#526a79','font-size':12},`第${i}期`)));
  const change=demoPrices[end]/demoPrices[start]-1;
  document.querySelector('#momentum-end-label').textContent=end;
  document.querySelector('#momentum-start-price').textContent=demoPrices[start].toFixed(2);
  document.querySelector('#momentum-end-price').textContent=demoPrices[end].toFixed(2);
  document.querySelector('#momentum-value').textContent=`${(change*100).toFixed(2)}%`;
  document.querySelector('#momentum-status').textContent=`第${start}期至第${end}期，20个间隔、21个价格。只用当前及以前记录计算，动量${(change*100).toFixed(2)}%。`;
  document.querySelector('#momentum-desc').textContent=`模拟价格，第${start}期${demoPrices[start].toFixed(2)}，第${end}期${demoPrices[end].toFixed(2)}，20期动量${(change*100).toFixed(2)}%。`;
}
document.querySelector('#momentum-end').addEventListener('input',renderMomentum);
renderMomentum();
const baseReturns=Array.from({length:20},(_,i)=>[.01,-.01,.02,-.02][i%4]);
function sampleStd(values) { const mean=values.reduce((a,b)=>a+b,0)/values.length; return Math.sqrt(values.reduce((sum,v)=>sum+(v-mean)**2,0)/(values.length-1)); }
const volLayer=document.querySelector('#volatility-chart .plot');
const volX=[140,320,500];
const volY=value=>218-value*3300;
for(let tick=0;tick<=5;tick++) {
  volLayer.append(svgElement('line',{x1:60,y1:volY(tick/100),x2:650,y2:volY(tick/100),stroke:'#dfe7e3'}),svgElement('text',{x:45,y:volY(tick/100)+4,'text-anchor':'end',fill:'#526a79','font-size':12},`${tick}%`));
}
[1,3,.5].forEach((scale,i)=>{
  const std=sampleStd(baseReturns.map(v=>v*scale));
  volLayer.append(svgElement('rect',{x:volX[i],y:volY(std),width:70,height:218-volY(std),fill:i===1?'#a67735':'#087e83',rx:3}),svgElement('text',{x:volX[i]+35,y:volY(std)-10,'text-anchor':'middle',fill:'#193346','font-size':14},`${(std*100).toFixed(4)}%`),svgElement('text',{x:volX[i]+35,y:243,'text-anchor':'middle',fill:'#526a79','font-size':13},`模拟${['A','B','C'][i]}`));
});
let madView='clipped';
function renderMad() {
  const extreme=Number(document.querySelector('#mad-outlier').value);
  const raw=[1,2,2,3,extreme], clipped=raw.map(v=>Math.max(-1,Math.min(5,v)));
  const values=madView==='raw'?raw:clipped;
  const maximum=madView==='raw'?Math.ceil(extreme/20)*20:6;
  const x=i=>90+i*120, y=v=>212-v/maximum*165;
  const layer=document.querySelector('#mad-chart .plot'); layer.replaceChildren();
  [0,maximum/2,maximum].forEach(v=>layer.append(svgElement('line',{x1:55,y1:y(v),x2:655,y2:y(v),stroke:'#dfe7e3'}),svgElement('text',{x:43,y:y(v)+4,'text-anchor':'end',fill:'#526a79','font-size':12},String(v))));
  values.forEach((v,i)=>layer.append(svgElement('rect',{x:x(i),y:y(v),width:50,height:212-y(v),fill:madView==='raw'?'#a67735':'#087e83',rx:2}),svgElement('text',{x:x(i)+25,y:y(v)-8,'text-anchor':'middle',fill:'#193346','font-size':14},String(v)),svgElement('text',{x:x(i)+25,y:240,'text-anchor':'middle',fill:'#526a79','font-size':12},['A','B','C','D','E'][i])));
  document.querySelector('#mad-outlier-value').textContent=extreme;
  document.querySelector('#mad-raw-values').textContent=raw.join('、');
  document.querySelector('#mad-clipped-values').textContent=clipped.join('、');
  document.querySelector('#mad-chart-status').textContent=`当前显示${madView==='raw'?'原始':'裁剪后'}截面，中位数2、MAD=1、边界[-1,5]。纵轴上限${maximum}个模拟因子点；切换时纵轴会重算。`;
  document.querySelector('#mad-desc').textContent=`模拟五股票，原值${raw.join('、')}，裁剪后${clipped.join('、')}，中位数2，MAD1，边界负1至5。当前显示${madView==='raw'?'原始':'裁剪后'}数据。`;
  document.querySelectorAll('[data-mad-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.madView===madView)));
}
document.querySelectorAll('[data-mad-view]').forEach(b=>b.addEventListener('click',()=>{madView=b.dataset.madView;renderMad();}));
document.querySelector('#mad-outlier').addEventListener('input',renderMad);
renderMad();
