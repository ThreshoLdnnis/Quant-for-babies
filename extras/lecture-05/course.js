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
// Every plotted observation comes from a deterministic SIMULATED account run.
const backtestDemo=JSON.parse(document.querySelector('#backtest-demo-data').textContent);
const strategyNames={mom20:'动量单因子',vol20:'波动率单因子',turn20:'换手率单因子',multi:'静态多因子',reference:'8股等权参考'};
const strategyColors={mom20:'#a67735',vol20:'#78649c',turn20:'#5276a0',multi:'#087e83',reference:'#a35369'};
const scenarioNames={zero:'零成本',base:'基础成本',high:'较高成本'};
let activeScenario='base';
const pct=(value,digits=2)=>Number.isFinite(value)?`${(100*value).toFixed(digits)}%`:'不可定义';
function svgEl(name,attrs={},text=''){
  const e=document.createElementNS('http://www.w3.org/2000/svg',name);
  Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));if(text)e.textContent=text;return e;
}
function svgText(g,x,y,text,attrs={}){g.append(svgEl('text',{x,y,fill:'#526a79','font-size':12,...attrs},text));}
function chart(id){const svg=document.getElementById(id);const g=svg.querySelector('.plot');g.replaceChildren();return {svg,g};}
function lineAxes(g,dates,min,max,height,tickFormat){
  const left=66,right=696,top=28,bottom=height-44;
  const x=i=>left+i/Math.max(1,dates.length-1)*(right-left);
  const y=v=>bottom-(v-min)/(max-min)*(bottom-top);
  for(let i=0;i<=4;i++){
    const value=min+(max-min)*i/4;g.append(svgEl('line',{x1:left,x2:right,y1:y(value),y2:y(value),stroke:'#e3ebe8'}));
    svgText(g,left-10,y(value)+4,tickFormat(value),{'text-anchor':'end'});
  }
  [0,Math.floor((dates.length-1)/3),Math.floor(2*(dates.length-1)/3),dates.length-1].forEach(i=>svgText(g,x(i),bottom+25,dates[i].slice(5),{'text-anchor':'middle'}));
  return {x,y,left,right,top,bottom};
}
function drawRanking(){
  const {g}=chart('ranking-chart'),rows=backtestDemo.ranking_snapshot;
  const min=Math.min(0,...rows.map(r=>r.score)),max=Math.max(0,...rows.map(r=>r.score)),span=max-min||1;
  const x=v=>132+(v-min)/span*535,zero=x(0),step=31;
  g.append(svgEl('line',{x1:zero,x2:zero,y1:20,y2:rows.length*step+25,stroke:'#a9bfb9'}));
  rows.forEach((r,i)=>{
    const y=27+i*step,color=r.selected?'#087e83':'#acbbb5';
    svgText(g,115,y+15,`${r.symbol}${r.selected?' ★':''}`,{'text-anchor':'end',fill:r.selected?'#087e83':'#526a79'});
    const rect=svgEl('rect',{x:Math.min(zero,x(r.score)),y,width:Math.max(1,Math.abs(x(r.score)-zero)),height:20,fill:color,rx:2});
    rect.append(svgEl('title',{},`${r.symbol}，排名${r.rank}，合成分${r.score.toFixed(6)}，${r.selected?'目标入选':'未入选'}`));g.append(rect);
    svgText(g,x(r.score)+(r.score>=0?5:-5),y+15,r.score.toFixed(3),{'text-anchor':r.score>=0?'start':'end','font-size':11});
  });
  svgText(g,390,rows.length*step+60,'静态合成得分（无量纲）',{'text-anchor':'middle'});
  document.querySelector('#ranking-status').textContent=`${rows[0].signal_date}收盘信号，共${rows.length}个有效候选；Top3：${rows.filter(r=>r.selected).map(r=>r.symbol).join('、')}。下一开盘才尝试执行。`;
}
function drawWeights(){
  const {g}=chart('weights-chart'),rows=backtestDemo.weight_snapshot;
  const series=[['before_weight','调仓前','#78649c'],['target_weight','目标','#a67735'],['after_weight','执行后','#087e83']];
  const left=65,right=700,bottom=285,top=45,max=Math.max(.4,...rows.flatMap(r=>series.map(([k])=>r[k])))*1.12;
  const y=v=>bottom-v/max*(bottom-top),group=(right-left)/rows.length;
  for(let n=0;n<=4;n++){const v=max*n/4;g.append(svgEl('line',{x1:left,x2:right,y1:y(v),y2:y(v),stroke:'#e3ebe8'}));svgText(g,left-8,y(v)+4,pct(v,0),{'text-anchor':'end'});}
  rows.forEach((r,i)=>{
    series.forEach(([key,name,color],j)=>{const rect=svgEl('rect',{x:left+i*group+group*.12+j*group*.24,y:y(r[key]),width:group*.22,height:bottom-y(r[key]),fill:color});rect.append(svgEl('title',{},`${r.symbol} ${name}: ${pct(r[key])}`));g.append(rect);});
    svgText(g,left+(i+.5)*group,bottom+20,r.symbol==='CASH'?'现金':r.symbol.replace('SIM','S'),{'text-anchor':'middle','font-size':11});
  });
  series.forEach(([,name,color],i)=>{g.append(svgEl('rect',{x:100+i*170,y:13,width:16,height:5,fill:color}));svgText(g,123+i*170,20,name);});
  document.querySelector('#weights-status').textContent=`${rows[0].trade_date}，基础成本多因子；按同一开盘参考价估值，执行前后分母分别为当时权益。卖出受阻可留下旧持仓，交易费用使执行后权益变化。现金保留在权重中。`;
}
function drawNav(){
  const {g}=chart('nav-chart');const rows=backtestDemo.nav_series.filter(r=>r.scenario===activeScenario);
  const dates=rows.filter(r=>r.strategy==='multi').map(r=>r.trade_date),values=[1,...rows.map(r=>r.nav)];
  const low=Math.min(...values),high=Math.max(...values),pad=Math.max(.01,(high-low)*.12);
  const a=lineAxes(g,dates,low-pad,high+pad,350,v=>v.toFixed(2));
  for(const strategy of backtestDemo.strategies){
    const series=rows.filter(r=>r.strategy===strategy);const p=series.map((r,i)=>`${i?'L':'M'}${a.x(i).toFixed(2)} ${a.y(r.nav).toFixed(2)}`).join(' ');
    const path=svgEl('path',{d:p,fill:'none',stroke:strategyColors[strategy],'stroke-width':strategy==='multi'?3:1.7,...(strategy==='reference'?{'stroke-dasharray':'6 4'}:{})});
    path.append(svgEl('title',{},`${strategyNames[strategy]} ${scenarioNames[activeScenario]}期末净值${series.at(-1).nav.toFixed(6)}`));g.append(path);
  }
  document.querySelector('#nav-status').textContent=`${scenarioNames[activeScenario]}，${backtestDemo.start_date}至${backtestDemo.end_date}，80个模拟期间（含初始现金预热），3次执行。每档费用独立运行；参考组合是虚构8股等权，非真实指数。`;
  const legend=document.querySelector('#nav-legend');legend.replaceChildren();
  for(const strategy of backtestDemo.strategies){const span=document.createElement('span');span.style.setProperty('--series-color',strategyColors[strategy]);span.textContent=strategyNames[strategy];legend.append(span);}
  const body=document.querySelector('#metrics-body');body.replaceChildren();
  backtestDemo.metrics.filter(r=>r.scenario===activeScenario).forEach(r=>{const tr=document.createElement('tr');[strategyNames[r.strategy],pct(r.total_return),pct(r.annualized_return),pct(r.annualized_vol),Number.isFinite(r.sharpe)?r.sharpe.toFixed(3):'不可定义',pct(r.max_drawdown)].forEach(value=>{const td=document.createElement('td');td.textContent=value;tr.append(td);});body.append(tr);});
  document.querySelector('#metrics-caption').textContent=`实际模拟输出 · ${scenarioNames[activeScenario]} · 整段80期含现金阶段 · 年化为短样本换算`;
}
function drawDrawdown(){
  const {g}=chart('drawdown-chart');const rows=backtestDemo.nav_series.filter(r=>r.strategy==='multi'&&r.scenario===activeScenario),dates=rows.map(r=>r.trade_date);
  const min=Math.min(-.005,...rows.map(r=>r.drawdown))*1.18,a=lineAxes(g,dates,min,0,260,v=>pct(v,1));
  const d=rows.map((r,i)=>`${i?'L':'M'}${a.x(i)} ${a.y(r.drawdown)}`).join(' ');
  g.append(svgEl('path',{d:`M${a.x(0)} ${a.y(0)} ${d.replace(/^M/,'L')} L${a.x(rows.length-1)} ${a.y(0)} Z`,fill:'#d8eee7'}));
  g.append(svgEl('path',{d,fill:'none',stroke:'#087e83','stroke-width':2}));
  const metric=backtestDemo.metrics.find(r=>r.strategy==='multi'&&r.scenario===activeScenario);
  document.querySelector('#drawdown-status').textContent=`${scenarioNames[activeScenario]}多因子，最大回撤${pct(metric.max_drawdown)}（非正数口径）；只描述所见80期路径，不是未来损失上限。`;
}
function drawSensitivity(){
  const {g}=chart('sensitivity-chart'),rows=backtestDemo.cost_sensitivity;
  const min=Math.min(0,...rows.map(r=>r.total_return)),max=Math.max(.01,...rows.map(r=>r.total_return))*1.2,y=v=>245-(v-min)/(max-min)*195;
  for(let i=0;i<=4;i++){const v=min+(max-min)*i/4;g.append(svgEl('line',{x1:70,x2:695,y1:y(v),y2:y(v),stroke:'#e3ebe8'}));svgText(g,60,y(v)+4,pct(v,1),{'text-anchor':'end'});}
  rows.forEach((r,i)=>{const x=115+i*200;g.append(svgEl('rect',{x,y:Math.min(y(0),y(r.total_return)),width:100,height:Math.max(1,Math.abs(y(r.total_return)-y(0))),fill:r.scenario===activeScenario?'#087e83':'#abc4bb'}));svgText(g,x+50,y(r.total_return)-9,pct(r.total_return),{'text-anchor':'middle',fill:'#193346'});svgText(g,x+50,270,scenarioNames[r.scenario],{'text-anchor':'middle'});});
  document.querySelector('#sensitivity-status').textContent='纵轴为多因子累计收益。每档均重新成交，费用改变现金、可买整手与后续持仓；差额不等于简单把累计费用从零费率净值末端减掉。';
}
function updateScenario(){document.querySelectorAll('[data-scenario]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.scenario===activeScenario)));drawNav();drawDrawdown();drawSensitivity();}
document.querySelectorAll('[data-scenario]').forEach(b=>b.addEventListener('click',()=>{activeScenario=b.dataset.scenario;updateScenario();}));
document.querySelector('#cost-bps').addEventListener('input',e=>{const bps=Number(e.target.value);document.querySelector('#cost-value').textContent=`${bps} bp`;document.querySelector('#cost-percent').textContent=pct(bps/10000);const net=.005-bps/10000;document.querySelector('#cost-net').textContent=(net>0?'+':'')+pct(net);});
drawRanking();drawWeights();updateScenario();
