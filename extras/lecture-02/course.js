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
const syntheticClose = Array.from({length:30},(_,i) => Math.round((20+i*.16+Math.sin(i*.65)*.8)*100)/100);
function svgElement(name, attrs={}, text='') { const e=document.createElementNS('http://www.w3.org/2000/svg',name); for(const [k,v] of Object.entries(attrs)) e.setAttribute(k,v); if(text)e.textContent=text;return e; }
function renderRolling(windowSize) {
  const svg=document.querySelector('#rolling-chart'); const layer=svg.querySelector('.plot'); layer.replaceChildren();
  const x=i=>53+i*20.7, y=v=>210-(v-18)*23;
  for(let tick=18;tick<=26;tick+=2){layer.append(svgElement('line',{x1:53,y1:y(tick),x2:660,y2:y(tick),stroke:'#e0e8e4'}),svgElement('text',{x:38,y:y(tick)+4,'text-anchor':'end',fill:'#526a79','font-size':11},String(tick)));}
  layer.append(svgElement('polyline',{points:syntheticClose.map((v,i)=>`${x(i)},${y(v)}`).join(' '),fill:'none',stroke:'#087e83','stroke-width':2.5}));
  const means=syntheticClose.map((_,i)=>i<windowSize-1?null:syntheticClose.slice(i-windowSize+1,i+1).reduce((a,b)=>a+b,0)/windowSize);
  layer.append(svgElement('polyline',{points:means.map((v,i)=>v===null?null:`${x(i)},${y(v)}`).filter(Boolean).join(' '),fill:'none',stroke:'#a67735','stroke-width':2.5}));
  [0,9,19,29].forEach(i=>layer.append(svgElement('text',{x:x(i),y:238,'text-anchor':'middle',fill:'#526a79','font-size':11},`第${i+1}条`)));
  document.querySelector('#ma-window').textContent=windowSize;
  document.querySelector('#ma-last').textContent=means.at(-1).toFixed(2);
  document.querySelector('#ma-first').textContent=`第 ${windowSize} 条`;
  document.querySelector('#chart-status').textContent=`当前为 ${windowSize} 条观察均线。前 ${windowSize-1} 条没有完整窗口，均线留空。`;
  document.querySelectorAll('[data-window]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.window)===windowSize)));
  document.querySelector('#rolling-chart-desc').textContent=`虚构股票30条模拟收盘价，最后收盘价${syntheticClose.at(-1).toFixed(2)}，${windowSize}条均线最后数值${means.at(-1).toFixed(2)}。前${windowSize-1}条均线为空。`;
}
document.querySelectorAll('[data-window]').forEach(b=>b.addEventListener('click',()=>renderRolling(Number(b.dataset.window))));
renderRolling(5);
