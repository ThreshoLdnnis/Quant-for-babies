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
// Fixed SIMULATED evaluation data, embedded in the HTML. No network or model fitting.
const evaluationDemo=JSON.parse(document.querySelector('#evaluation-demo-data').textContent);
let activeFactor='mom20';
let scatterMode='score';
const factorColors={mom20:'#087e83',vol20:'#78649c',turn20:'#a67735'};
function svgElement(name, attrs={}, text='') {
  const e=document.createElementNS('http://www.w3.org/2000/svg',name);
  for(const [key,value] of Object.entries(attrs))e.setAttribute(key,value);
  if(text)e.textContent=text;
  return e;
}
function averageRanks(values) {
  const sorted=values.map((v,i)=>({v,i})).sort((a,b)=>a.v-b.v);
  const ranks=Array(values.length);
  for(let i=0;i<sorted.length;){let j=i+1;while(j<sorted.length&&sorted[j].v===sorted[i].v)j++;const rank=(i+1+j)/2;for(let k=i;k<j;k++)ranks[sorted[k].i]=rank;i=j;}
  return ranks;
}
function scatterDomain(values,rankMode) {
  if(rankMode)return [.6,values.length+.4];
  let low=Math.min(0,...values),high=Math.max(0,...values);
  const padding=(high-low||1)*.12;
  return [low-padding,high+padding];
}
function renderScatter() {
  const points=evaluationDemo.snapshot;
  const rawX=points.map(p=>p[`${activeFactor}_score`]);
  const rawY=points.map(p=>100*p.future_return_20);
  const rankMode=scatterMode==='rank';
  const xs=rankMode?averageRanks(rawX):rawX, ys=rankMode?averageRanks(rawY):rawY;
  const [xmin,xmax]=scatterDomain(xs,rankMode),[ymin,ymax]=scatterDomain(ys,rankMode);
  const x=v=>65+(v-xmin)/(xmax-xmin)*570,y=v=>265-(v-ymin)/(ymax-ymin)*225;
  const layer=document.querySelector('#scatter-chart .plot');layer.replaceChildren();
  for(let tick=0;tick<=4;tick++){
    const xv=xmin+(xmax-xmin)*tick/4,yv=ymin+(ymax-ymin)*tick/4;
    layer.append(svgElement('line',{x1:65,y1:y(yv),x2:635,y2:y(yv),stroke:'#dfe7e3'}),svgElement('text',{x:54,y:y(yv)+4,'text-anchor':'end',fill:'#526a79','font-size':11},`${yv.toFixed(rankMode?1:1)}${rankMode?'':'%'}`),svgElement('text',{x:x(xv),y:285,'text-anchor':'middle',fill:'#526a79','font-size':11},xv.toFixed(1)));
  }
  if(ymin<0&&ymax>0)layer.append(svgElement('line',{x1:65,y1:y(0),x2:635,y2:y(0),stroke:'#8ea8a2','stroke-dasharray':'4 4'}));
  points.forEach((p,i)=>{
    const circle=svgElement('circle',{cx:x(xs[i]),cy:y(ys[i]),r:5,fill:factorColors[activeFactor]});
    circle.append(svgElement('title',{},`${p.symbol}: ${rawX[i].toFixed(4)}, forward20=${rawY[i].toFixed(3)}%`));
    layer.append(circle,svgElement('text',{x:x(xs[i])+8,y:y(ys[i])-7,fill:'#314f5e','font-size':11},p.symbol.replace('SIM','S')));
  });
  layer.append(svgElement('text',{x:350,y:315,'text-anchor':'middle',fill:'#526a79','font-size':12},rankMode?'当期因子平均秩':'固定方向后的因子得分（Z刻度）'));
  const ic=evaluationDemo.ic_series.find(r=>r.factor===activeFactor&&r.trade_date===evaluationDemo.snapshot_date);
  document.querySelector('#scatter-status').textContent=`${activeFactor.toUpperCase()}，${evaluationDemo.snapshot_date}，同一组${points.length}只虚构股票，Rank IC=${Number(ic.rank_ic).toFixed(4)}。当前${rankMode?'显示平均秩；并列取相同平均位置':'横轴为得分，纵轴为未来20期价格收益（%）'}。`;
  document.querySelector('#scatter-desc').textContent=`模拟${points.length}股票，${activeFactor.toUpperCase()}与未来20期价格收益，Spearman相关${Number(ic.rank_ic).toFixed(4)}，${rankMode?'平均秩坐标':'得分和收益坐标'}。`;
  document.querySelectorAll('[data-scatter-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.scatterMode===scatterMode)));
}
function renderIc() {
  const rows=evaluationDemo.ic_series.filter(r=>r.factor===activeFactor);
  const x=i=>55+i*600/(rows.length-1),y=v=>135-v*98;
  const layer=document.querySelector('#ic-chart .plot');layer.replaceChildren();
  layer.append(svgElement('rect',{x:55,y:25,width:x(20)-55,height:210,fill:'#f0f3f0'}),svgElement('rect',{x:x(60),y:25,width:655-x(60),height:210,fill:'#f0f3f0'}));
  [-1,-.5,0,.5,1].forEach(v=>layer.append(svgElement('line',{x1:55,y1:y(v),x2:655,y2:y(v),stroke:v===0?'#8ea8a2':'#dfe7e3','stroke-dasharray':v===0?'4 3':'0'}),svgElement('text',{x:42,y:y(v)+4,'text-anchor':'end',fill:'#526a79','font-size':11},v.toFixed(1))));
  let segment=[];
  function flush(){if(segment.length)layer.append(svgElement('polyline',{points:segment.join(' '),fill:'none',stroke:factorColors[activeFactor],'stroke-width':2.2}));segment=[];}
  rows.forEach((r,i)=>{if(Number.isFinite(r.rank_ic)){segment.push(`${x(i)},${y(r.rank_ic)}`);layer.append(svgElement('circle',{cx:x(i),cy:y(r.rank_ic),r:2,fill:factorColors[activeFactor]}));}else flush();});flush();
  [0,20,40,60,79].filter(i=>i<rows.length).forEach(i=>layer.append(svgElement('text',{x:x(i),y:262,'text-anchor':'middle',fill:'#526a79','font-size':11},rows[i].trade_date.slice(5))));
  layer.append(svgElement('text',{x:350,y:287,'text-anchor':'middle',fill:'#526a79','font-size':12},'2024年模拟工作日（不是交易所日历）'));
  const s=evaluationDemo.ic_summary.find(r=>r.factor===activeFactor), valid=rows.filter(r=>Number.isFinite(r.rank_ic));
  document.querySelector('#ic-periods').textContent=s.n_periods;
  document.querySelector('#ic-mean').textContent=s.mean_ic.toFixed(3);
  document.querySelector('#ic-ir').textContent=s.icir.toFixed(3);
  document.querySelector('#ic-status').textContent=`${activeFactor.toUpperCase()}：${s.n_periods}个有效评价日，每日配对股票数${Math.min(...valid.map(r=>r.n))}–${Math.max(...valid.map(r=>r.n))}。前后空白保留；ICIR使用样本SD，未年化，未假定日期独立。`;
}
function renderQuintiles() {
  const all=evaluationDemo.quintile_mean_common;
  const rows=all.filter(r=>r.factor===activeFactor).sort((a,b)=>a.quintile-b.quintile);
  const maximum=Math.max(.02,...all.map(r=>Math.abs(r.mean_forward_return_20)))*1.2;
  const y=v=>145-v/maximum*105,x=i=>90+i*116;
  const layer=document.querySelector('#quintile-chart .plot');layer.replaceChildren();
  [-maximum,0,maximum].forEach(v=>layer.append(svgElement('line',{x1:55,y1:y(v),x2:655,y2:y(v),stroke:v===0?'#8ea8a2':'#dfe7e3'}),svgElement('text',{x:44,y:y(v)+4,'text-anchor':'end',fill:'#526a79','font-size':11},`${(v*100).toFixed(1)}%`)));
  rows.forEach((r,i)=>{const value=r.mean_forward_return_20,top=Math.min(y(value),y(0));layer.append(svgElement('rect',{x:x(i),y:top,width:60,height:Math.max(1,Math.abs(y(value)-y(0))),rx:2,fill:value>=0?'#087e83':'#a45b45'}),svgElement('text',{x:x(i)+30,y:y(value)+(value>=0?-9:17),'text-anchor':'middle',fill:'#193346','font-size':13},`${(value*100).toFixed(2)}%`),svgElement('text',{x:x(i)+30,y:280,'text-anchor':'middle',fill:'#526a79','font-size':12},`Q${r.quintile}`));});
  document.querySelector('#quintile-days').textContent=rows[0]?.n_periods||0;
  document.querySelector('#quintile-status').textContent=`${activeFactor.toUpperCase()}，共同有效${rows[0]?.n_periods||0}个评价日；各组平均人数：${rows.map(r=>`Q${r.quintile}=${r.mean_n_stocks.toFixed(2)}`).join('，')}。这是组内按股、跨期按日期等权的20期未来收益均值。`;
  document.querySelector('#quintile-desc').textContent=`模拟${activeFactor.toUpperCase()}共同日期五组未来20期价格收益均值：${rows.map(r=>`Q${r.quintile} ${(r.mean_forward_return_20*100).toFixed(2)}%`).join('；')}。不是策略日收益。`;
}
function renderFactor() {
  document.querySelectorAll('[data-factor]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.factor===activeFactor)));
  renderScatter();renderIc();renderQuintiles();
}
document.querySelectorAll('[data-factor]').forEach(b=>b.addEventListener('click',()=>{activeFactor=b.dataset.factor;renderFactor();}));
document.querySelectorAll('[data-scatter-mode]').forEach(b=>b.addEventListener('click',()=>{scatterMode=b.dataset.scatterMode;renderScatter();}));
document.querySelectorAll('.snapshot-date').forEach(e=>e.textContent=evaluationDemo.snapshot_date);
function renderStability() {
  const layer=document.querySelector('#stability-chart .plot'),x=i=>75+i*140,y=v=>215-(v+.12)/.34*175;
  [-.1,0,.1,.2].forEach(v=>layer.append(svgElement('line',{x1:55,y1:y(v),x2:655,y2:y(v),stroke:'#dfe7e3'}),svgElement('text',{x:43,y:y(v)+4,'text-anchor':'end',fill:'#526a79','font-size':11},v.toFixed(2))));
  layer.append(svgElement('line',{x1:55,y1:y(.04),x2:655,y2:y(.04),stroke:'#78918a','stroke-dasharray':'5 4'}));
  ['A','B'].forEach((factor,index)=>{const rows=evaluationDemo.stability.series.filter(r=>r.factor===factor),color=index?'#a67735':'#087e83';layer.append(svgElement('polyline',{points:rows.map((r,i)=>`${x(i)},${y(r.rank_ic)}`).join(' '),fill:'none',stroke:color,'stroke-width':2.5}));rows.forEach((r,i)=>layer.append(svgElement('circle',{cx:x(i),cy:y(r.rank_ic),r:4,fill:color})));});
  [0,1,2,3,4].forEach(i=>layer.append(svgElement('text',{x:x(i),y:248,'text-anchor':'middle',fill:'#526a79','font-size':12},`第${i+1}期`)));
}
renderFactor();renderStability();
