// Small exact teaching models. No network access or quantum hardware connection.
export function groverState(N, k, extraOracle=false) {
  if (![4,16,64].includes(N) || !Number.isInteger(k) || k<0 || k>12) throw new RangeError('Teaching model bounds');
  let amplitudes=Array(N).fill(1/Math.sqrt(N));
  for (let step=0; step<k; step++) {
    amplitudes[0]*=-1;
    const mean=amplitudes.reduce((a,b)=>a+b,0)/N;
    amplitudes=amplitudes.map(value=>2*mean-value);
  }
  if(extraOracle) amplitudes[0]*=-1;
  return {amplitudes, probabilities:amplitudes.map(value=>value*value)};
}
const gcd=(a,b)=>b?gcd(b,a%b):a;
export function shorSample(c) {
  if (![0,64,128,192].includes(c)) throw new RangeError('Fixed ideal phase samples only');
  const d=gcd(c,256), numerator=c/d, denominator=256/d;
  if(c===0)return {c,numerator,denominator,status:'uninformative',factors:[]};
  if((2**denominator)%15!==1)return {c,numerator,denominator,status:'retry',factors:[]};
  const x=(2**(denominator/2))%15;
  return {c,numerator,denominator,status:'factors',factors:[gcd(x-1,15),gcd(x+1,15)]};
}
if(typeof document!=='undefined') {
  const zh=document.documentElement.lang.startsWith('zh');
  const t=(en,cn)=>zh?cn:en;
  const shorOutput=document.getElementById('shor-result');
  if(shorOutput) {
    const buttons=[...document.querySelectorAll('[data-shor-sample]')];
    function showSample(c) {
      const sample=shorSample(c);
      buttons.forEach(button=>button.setAttribute('aria-pressed',String(Number(button.dataset.shorSample)===c)));
      let detail;
      if(sample.status==='uninformative') detail=t('Zero phase gives no order information. Take another sample.','零相位不提供阶信息，需要另取样本。');
      else if(sample.status==='retry') detail=t('Candidate r=2 fails: 2² mod 15=4, not 1. This reduced denominator is a divisor of the true order; obtain more samples.','候选 r=2 未通过校验：2² mod 15=4，不是 1。约分后分母只是实际阶的因子，需要更多样本。');
      else detail=t('Candidate r=4 passes: 2⁴ mod 15=1. Half-power x=4 gives gcd(3,15)=3 and gcd(5,15)=5.','候选 r=4 通过：2⁴ mod 15=1。半阶幂 x=4，得到 gcd(3,15)=3、gcd(5,15)=5。');
      shorOutput.textContent=`c=${c}: ${c}/256 = ${sample.numerator}/${sample.denominator}. ${detail}`;
    }
    buttons.forEach(button=>button.addEventListener('click',()=>showSample(Number(button.dataset.shorSample))));
    showSample(64);
  }
  const size=document.getElementById('grover-size');
  if(size) {
    const iterations=document.getElementById('grover-iterations');
    const oracle=document.getElementById('grover-oracle');
    const percent=value=>`${(value*100).toFixed(2)}%`;
    function render() {
      const N=Number(size.value), k=Number(iterations.value);
      const state=groverState(N,k,oracle.checked);
      const theta=Math.asin(1/Math.sqrt(N));
      const suggested=Math.round(Math.PI/(4*theta)-0.5);
      document.getElementById('grover-k').textContent=String(k);
      document.getElementById('grover-summary').textContent=t(
        `N=${N}, M=1, k=${k} · target probability ${percent(state.probabilities[0])} · first-peak choice k=${suggested}`,
        `N=${N}、M=1、k=${k} · 目标概率 ${percent(state.probabilities[0])} · 首峰附近选择 k=${suggested}`);
      const body=document.getElementById('grover-amplitudes');
      body.replaceChildren();
      const tbl=document.createElement('table');
      const head=document.createElement('tr');
      [t('State','状态'),t('Amplitude (signed)','振幅（含符号）'),t('Probability','概率')].forEach(label=>{const th=document.createElement('th');th.scope='col';th.textContent=label;head.append(th);});
      const thead=document.createElement('thead');thead.append(head);tbl.append(thead);
      const tbody=document.createElement('tbody');
      [[t('Marked x=0','标记态 x=0'),state.amplitudes[0],state.probabilities[0]],
       [t(`Each of ${N-1} unmarked states`,`其余 ${N-1} 态中的每一态`),state.amplitudes[1],state.probabilities[1]]].forEach(([label,amp,prob])=>{
        const row=document.createElement('tr');
        [label,Math.abs(amp)<1e-12?'0':amp.toFixed(6),percent(prob)].forEach((text,index)=>{const cell=document.createElement(index===0?'th':'td');if(index===0)cell.scope='row';cell.textContent=text;row.append(cell);});tbody.append(row);
      });
      tbl.append(tbody);body.append(tbl);
      const svg=document.getElementById('grover-curve');
      svg.replaceChildren();
      const ns='http://www.w3.org/2000/svg';
      const add=(tag,attrs,text)=>{const el=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([key,value])=>el.setAttribute(key,String(value)));if(text!==undefined)el.textContent=text;svg.append(el);return el;};
      for(const value of [0,0.5,1]) {
        const y=175-145*value;
        add('line',{x1:55,x2:745,y1:y,y2:y,stroke:'#d2dcd8'});
        add('text',{x:45,y:y+5,'text-anchor':'end',class:'svg-small'},`${value*100}%`);
      }
      const points=Array.from({length:13},(_,i)=>[55+i*57.5,175-145*Math.sin((2*i+1)*theta)**2]);
      add('polyline',{points:points.map(p=>p.join(',')).join(' '),fill:'none',stroke:'#376b76','stroke-width':2});
      points.forEach(([x,y],i)=>{
        add('circle',{cx:x,cy:y,r:i===k?7:4,fill:i===k?'#af4c2b':'#376b76'});
        add('text',{x,y:198,'text-anchor':'middle',class:'svg-small'},i);
      });
      add('text',{x:400,y:225,'text-anchor':'middle',class:'svg-small'},t('Complete Grover iterations k','完整 Grover 迭代数 k'));
    }
    [size,iterations,oracle].forEach(input=>input.addEventListener('input',render));
    document.getElementById('grover-optimum').addEventListener('click',()=>{
      iterations.value=String(Math.round(Math.PI/(4*Math.asin(1/Math.sqrt(Number(size.value))))-0.5));oracle.checked=false;render();
    });
    render();
  }
}
