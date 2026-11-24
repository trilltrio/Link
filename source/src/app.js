(function(){
const P=(document.body.dataset.prefix||'sp1x')+':';
const S={get:k=>{try{return localStorage.getItem(P+k)}catch(e){return null}},
 set:(k,v)=>{try{localStorage.setItem(P+k,v)}catch(e){}},
 clear:()=>{try{Object.keys(localStorage).filter(k=>k.startsWith(P)).forEach(k=>localStorage.removeItem(k))}catch(e){}}};
const val=id=>(S.get('f:'+id)||'').trim();

const WO=[['l2_job','Full job'],['l2_why','Why'],['l2_guard','Guardrails'],['l2_done','Done looks like']];
const workOrder=()=>WO.map(([id,t])=>t+': '+(val(id)||'[not filled yet]')).join('\n');
const master=()=>workOrder()+'\nRun these checks yourself and show me the results before you report back.';
const PROTOCOL=`Standing protocol for every job I give you:
1. Before you start, make sure the job has a brief in four parts: full job, why, guardrails, and what done looks like.
2. If any part is unclear, interview me first, then show me the brief and wait for my go.
3. Treat the guardrails as firm limits. If one is hit, stop and ask me.
4. Before you report back, run the done checks yourself and show me the results.`;

async function copyText(text,btn){
 const label=btn.dataset.label||btn.textContent;btn.dataset.label=label;
 let ok=false;
 try{await navigator.clipboard.writeText(text);ok=true}catch(e){
  const t=document.createElement('textarea');t.value=text;t.setAttribute('readonly','');t.style.position='fixed';t.style.opacity='0';
  document.body.appendChild(t);t.select();t.setSelectionRange(0,text.length);
  try{ok=document.execCommand('copy')}catch(e2){}
  t.remove();
 }
 btn.textContent=ok?'Copied':'Copy failed, select and copy by hand';
 setTimeout(()=>{btn.textContent=label},2000);
}

/* visual preference block (Lesson 1, card 4) */
function prefBlock(f){
 if(!f)return'';
 const g=n=>{const e=f.querySelector(`[name=${n}]:checked`);return e?e.value:''};
 const all=n=>[...f.querySelectorAll(`[name=${n}]:checked`)].map(e=>e.value);
 const L=['How I want your answers:'];
 const st=g('structure');
 if(st==='four')L.push('- Answer top-down in four parts: 1. Needs me: what only I can decide or give ("None" if nothing). 2. Goal met?: yes, partly or no, with the proof. 3. Short path: the next 1 to 3 steps. 4. Errors and why: what failed or is uncertain, and why.');
 if(st==='concise')L.push('- Keep every answer concise. Lead with what matters and cut the rest.');
 const v=all('vis');
 if(v.length)L.push('- When an answer is more than a few lines, give it to me as a visual instead of long prose. Formats I use: '+v.join(', ')+'.');
 const sp=g('speed');
 if(sp==='fast')L.push('- I read fast. Keep it tight and skip recaps.');
 if(sp==='slow')L.push('- I take my time reading. Use short sentences and one idea per line.');
 const ld=g('lead');
 if(ld==='visual')L.push('- Lead with a visual, then the words.');
 if(ld==='words')L.push('- Lead with words. Add a visual only when it saves me reading.');
 if(ld==='both')L.push('- Give me a short visual and short words side by side.');
 const mp=all('map');
 if(mp.includes('num'))L.push('- When the answer is numbers I track, use a dashboard.');
 if(mp.includes('walk'))L.push('- When you walk me through something, use slides.');
 const d=g('read');
 if(d==='dys')L.push('- I have dyslexia. Use short sentences, bullet points and bold key words. No dense paragraphs. Use plain, easy-to-read fonts in anything visual.');
 const other=(f.querySelector('[name=read_other]')||{}).value||'';
 if(d==='other'&&other.trim())L.push('- Reading note: '+other.trim());
 return L.join('\n');
}
function prefOk(f){
 const has=n=>!f.querySelector(`[name=${n}]`)||!!f.querySelector(`[name=${n}]:checked`);
 const other=f.querySelector('[name=read_other]');
 const otherOk=!(f.querySelector('[name=read][value=other]:checked'))||(other&&other.value.trim().length>=3);
 return has('structure')&&has('vis')&&has('speed')&&has('lead')&&has('read')&&otherOk;
}

/* take-home kit */
const KIT=[
 ['My answer-style block','Lesson 1. Give this to your agent as a standing instruction.',()=>val('l1_block')],
 ['My work order','Lesson 2. Your master prompt: paste it at the top of a job.',()=>WO.some(([id])=>val(id))?master():''],
 ['My brief protocol','Lesson 2. A standing rule to build into your setup.',()=>S.get('pass:l2')?PROTOCOL:'']
];

document.addEventListener('DOMContentLoaded',()=>{
 if('scrollRestoration' in history)history.scrollRestoration='manual';
 window.scrollTo(0,0);

 document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>{
  copyText(document.getElementById(b.dataset.copy).textContent,b)}));

 /* quizzes */
 document.querySelectorAll('.quiz').forEach(qz=>{
  const id=qz.dataset.quiz,ans=qz.dataset.answer,fb=qz.querySelector('.fb'),st=qz.querySelector('.st');
  const bs=[...qz.querySelectorAll('.choice')];
  const win=(b,silent)=>{
   qz.dataset.ok='1';qz.classList.add('done');bs.forEach(x=>x.classList.remove('wrong'));b.classList.add('right');
   fb.className='fb yes';fb.textContent='Right. '+b.dataset.why;st.textContent='Passed';
   const old=qz.querySelector('.backbtn');if(old)old.remove();
   if(!silent){S.set('q:'+id,'ok');update()}
  };
  bs.forEach(b=>b.addEventListener('click',()=>{
   if(qz.dataset.ok)return;
   if(b.dataset.k===ans){win(b);return}
   b.classList.add('wrong');fb.className='fb no';fb.textContent=(b.dataset.back?'':'Not this one. ')+b.dataset.why+(b.dataset.back?'':' Try again.');
   if(b.dataset.back&&!qz.querySelector('.backbtn')){
    const bb=document.createElement('button');bb.type='button';bb.className='backbtn';bb.textContent='Back to card '+b.dataset.back;
    bb.addEventListener('click',()=>{const d=document.querySelectorAll('#locks > details')[+b.dataset.back-1];d.open=true;d.scrollIntoView({behavior:'smooth'});b.classList.remove('wrong');bb.remove();fb.textContent=''});
    fb.after(bb);
   }
  }));
  if(S.get('q:'+id)==='ok'){const b=bs.find(x=>x.dataset.k===ans);if(b)win(b,true)}
 });

 /* typed answers */
 document.querySelectorAll('[data-save]').forEach(el=>{
  const id=el.dataset.save,min=+(el.dataset.min||1),wrap=el.closest('.field'),st=wrap.querySelector('.frow span');
  const v=S.get('f:'+id);if(v!==null)el.value=v;
  const check=()=>{const ok=el.value.trim().length>=min;wrap.classList.toggle('ok',ok);el.dataset.ok=ok?'1':'';
   st.textContent=ok?'Saved on this phone':(el.value.trim()?'Saved, keep going':'Not answered yet');return ok};
  el.addEventListener('input',()=>{S.set('f:'+id,el.value);check();update()});
  wrap.querySelector('button').addEventListener('click',e=>copyText(el.value.trim()?el.value:'(empty)',e.currentTarget));
  check();
 });

 /* preference questionnaire */
 const pf=document.getElementById('prefs');
 if(pf){
  let saved={};try{saved=JSON.parse(S.get('prefs')||'{}')}catch(e){}
  pf.querySelectorAll('input').forEach(i=>{const s=saved[i.name+'='+i.value];if(i.type==='text'){if(saved[i.name])i.value=saved[i.name]}else if(s)i.checked=true});
  const sync=()=>{
   const o={};pf.querySelectorAll('input').forEach(i=>{if(i.type==='text')o[i.name]=i.value;else if(i.checked)o[i.name+'='+i.value]=1});
   S.set('prefs',JSON.stringify(o));
   const ok=prefOk(pf),txt=prefBlock(pf);
   pf.dataset.ok=ok?'1':'';
   document.getElementById('prefblock').textContent=ok?txt:'Answer every question above and your block appears here.';
   if(ok)S.set('f:l1_block',txt);
   pf.closest('.try').classList.toggle('done',ok);
   pf.closest('.try').querySelector('.st').textContent=ok?'Block built, saved':'Answer all';
  };
  pf.addEventListener('change',()=>{sync();update()});pf.addEventListener('input',()=>{sync();update()});
  sync();
 }

 /* group copy (work order) and live blocks */
 document.querySelectorAll('[data-copygroup]').forEach(b=>b.addEventListener('click',()=>copyText(workOrder(),b)));
 const live=()=>{const m=document.getElementById('master');if(m)m.textContent=master();const p=document.getElementById('protocol');if(p)p.textContent=PROTOCOL};

 /* cards, meter, unlock */
 const ds=[...document.querySelectorAll('#locks > details')];
 const done=c=>[...c.querySelectorAll('.quiz,[data-save][data-min],#prefs')].every(x=>x.dataset.ok);
 function update(){
  live();
  if(!ds.length)return;
  let n=0;
  ds.forEach(d=>{
   const ok=done(d);d.classList.toggle('got',ok);if(ok)n++;
   d.querySelectorAll('.try.typed').forEach(t=>t.classList.toggle('done',[...t.querySelectorAll('[data-save][data-min]')].every(f=>f.dataset.ok)));
  });
  const t=ds.length,all=n===t;
  document.getElementById('tcount').textContent=n+' / '+t;
  document.getElementById('tbar').style.width=(n/t*100)+'%';
  document.getElementById('trophy').classList.toggle('plat',all);
  document.getElementById('plat').classList.toggle('on',all);
  const nb=document.getElementById('nextbtn'),nn=document.getElementById('nextnote');
  if(nb){nb.classList.toggle('locked',!all);nb.classList.toggle('open',all);nb.setAttribute('aria-disabled',all?'false':'true');
   nb.tabIndex=all?0:-1;nb.querySelector('.ico').textContent=all?'→':'🔒';
   nn.textContent=all?'Passed. Tap to go on.':'Pass '+(t-n)+' more card'+(t-n===1?'':'s')+' to unlock.'}
  if(all)S.set('pass:'+document.body.dataset.lesson,'1');
 }

 /* kit page */
 const kit=document.getElementById('kit');
 if(kit){
  const items=KIT.map(([t,s,fn],i)=>{const v=fn();return{t,s,v,i}});
  kit.innerHTML='';
  items.forEach(it=>{
   const d=document.createElement('div');d.className='kitem'+(it.v?'':' empty');
   d.innerHTML=`<div class="copyhead"><b></b><button type="button">Copy</button></div><p class="src"></p><pre class="tmpl"></pre>`;
   d.querySelector('b').textContent=it.t;d.querySelector('.src').textContent=it.s;
   d.querySelector('pre').textContent=it.v||'Not built yet. Finish the lesson to fill this in.';
   d.querySelector('button').addEventListener('click',e=>copyText(it.v||'',e.currentTarget));
   kit.appendChild(d);
  });
  document.getElementById('copyall').addEventListener('click',e=>copyText(items.filter(i=>i.v).map(i=>'== '+i.t+' ==\n'+i.v).join('\n\n'),e.currentTarget));
 }

 document.querySelectorAll('[data-passed]').forEach(el=>{if(S.get('pass:'+el.dataset.passed))el.textContent='Passed'});

 const rs=document.getElementById('reset');
 if(rs)rs.addEventListener('click',()=>{
  if(rs.dataset.armed){S.clear();location.href='lesson1.html'}
  else{rs.dataset.armed='1';rs.textContent='Tap again to erase every answer';setTimeout(()=>{delete rs.dataset.armed;rs.textContent='Start over'},4000)}
 });

 update();
});
})();
