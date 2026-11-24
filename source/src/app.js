(function(){
const P=(document.body.dataset.prefix||'sp1x')+':';
const S={get:k=>{try{return localStorage.getItem(P+k)}catch(e){return null}},
 set:(k,v)=>{try{localStorage.setItem(P+k,v)}catch(e){}},
 del:k=>{try{localStorage.removeItem(P+k)}catch(e){}},
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

/* ---------- sound (only on pages with a sound switch) ---------- */
const soundOn=()=>!!document.getElementById('soundtoggle')&&S.get('sound')!=='off';
let AC=null;
function tone(ok){
 if(!soundOn())return;
 try{
  AC=AC||new (window.AudioContext||window.webkitAudioContext)();
  if(AC.state==='suspended')AC.resume();
  const t=AC.currentTime,notes=ok?[[880,0],[1318.5,.11]]:[[185,0]];
  notes.forEach(([f,d])=>{
   const o=AC.createOscillator(),g=AC.createGain();
   o.type=ok?'sine':'triangle';o.frequency.value=f;
   const peak=ok?.09:.05,len=ok?.55:.3;
   g.gain.setValueAtTime(.0001,t+d);g.gain.exponentialRampToValueAtTime(peak,t+d+.02);g.gain.exponentialRampToValueAtTime(.0001,t+d+len);
   o.connect(g);g.connect(AC.destination);o.start(t+d);o.stop(t+d+len+.05);
  });
 }catch(e){}
}

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

/* ---------- answer-style block (Lesson 1, card 4) ---------- */
const MATCH_LINE='- Pick the visual by the job: a dashboard for numbers I watch, a sheet for rows to sort or fill, a doc for a plan to keep, a whiteboard for a process, slides for a walkthrough, and a one-page page for a one-off report.';
function prefBlock(f){
 if(!f)return'';
 const g=n=>{const e=f.querySelector(`[name=${n}]:checked`);return e?e.value:''};
 const all=n=>[...f.querySelectorAll(`[name=${n}]:checked`)].map(e=>e.value);
 const L=['How I want your answers:'];
 const STRUCT={four:'- Answer top-down in four parts: 1. Needs me: what only I can decide or give ("None" if nothing). 2. Goal met?: yes, partly or no, with the proof. 3. Short path: the next 1 to 3 steps. 4. Errors and why: what failed or is uncertain, and why.',
  concise:'- Keep every answer concise. Lead with what matters and cut the rest.',
  bottom:'- Give me the bottom line first, in one or two sentences, then the details.',
  qa:'- Answer as questions and answers: each question I would ask, then a short answer to it.'};
 if(STRUCT[g('structure')])L.push(STRUCT[g('structure')]);
 const v=all('vis');
 if(v.length)L.push('- When an answer would be a long block of text, give it to me as a visual instead. Formats I use: '+v.join(', ')+'.');
 L.push(...({fast:['- I read fast. Keep it tight and skip recaps.'],slow:['- I take my time reading. Use short sentences and one idea per line.'],
   both:['- My reading pace changes day to day. Put the key point in the first line so I can stop early, and keep the rest easy to skim.']})[g('speed')]||[]);
 L.push(...({visual:['- Lead with a visual, then the words.'],words:['- Lead with words. Add a visual only when it saves me reading.'],
   both:['- Give me a short visual and short words side by side.'],bullets:['- Use bullet points instead of paragraphs.']})[g('lead')]||[]);
 const m=document.getElementById('match');if(m&&m.dataset.ok)L.push(MATCH_LINE);
 const r=all('read');
 if(r.includes('dys'))L.push('- I have dyslexia. Use short sentences, bullet points and bold key words. No dense paragraphs. Use plain, easy-to-read fonts in anything visual.');
 if(r.includes('color'))L.push('- I am color blind. Never use color alone to show meaning; add labels, icons or patterns, and keep contrast high.');
 if(r.includes('small'))L.push('- Small text is hard for me. Use large text in anything visual.');
 if(r.includes('long'))L.push('- Long paragraphs lose me. Keep each paragraph to two or three lines.');
 const other=(f.querySelector('[name=read_other]')||{}).value||'';
 if(r.includes('other')&&other.trim())L.push('- Reading note: '+other.trim());
 return L.join('\n');
}
function prefOk(f){
 const has=n=>!f.querySelector(`[name=${n}]`)||!!f.querySelector(`[name=${n}]:checked`);
 const other=f.querySelector('[name=read_other]');
 const otherOk=!(f.querySelector('[name=read][value=other]:checked'))||(other&&other.value.trim().length>=3);
 const m=document.getElementById('match');
 return has('structure')&&has('vis')&&has('speed')&&has('lead')&&has('read')&&otherOk&&(!m||!!m.dataset.ok);
}

/* ---------- take-home kit ---------- */
const KIT=[
 ['My answer-style block','Lesson 1. Give this to your agent as a standing instruction.',()=>val('l1_block')],
 ['My answer-style block, Version 1','Lesson 1. Your first try, kept when you retook the questions.',()=>val('l1_block_v1'),true],
 ['My work order','Lesson 2. Your master prompt: paste it at the top of a job.',()=>WO.some(([id])=>val(id))?master():''],
 ['My brief protocol','Lesson 2. A standing rule to build into your setup.',()=>S.get('pass:l2')?PROTOCOL:'']
];

document.addEventListener('DOMContentLoaded',()=>{
 if('scrollRestoration' in history)history.scrollRestoration='manual';
 window.scrollTo(0,0);

 document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>{
  copyText(document.getElementById(b.dataset.copy).textContent,b)}));

 const ds=[...document.querySelectorAll('#locks > details')];

 /* pacing: the test opens only after the lesson part */
 const openTest=d=>{const t=d.querySelector('.test.shut');if(t){t.classList.remove('shut');const b=d.querySelector('.starttest');if(b)b.remove();S.set('open:'+document.body.dataset.lesson+':'+ds.indexOf(d),'1')}};
 ds.forEach((d,i)=>{
  const b=d.querySelector('.starttest');if(!b)return;
  if(S.get('open:'+document.body.dataset.lesson+':'+i))openTest(d);
  b.addEventListener('click',()=>{openTest(d);const t=d.querySelector('.test');if(t)t.scrollIntoView({behavior:'smooth',block:'start'})});
 });

 /* quizzes */
 document.querySelectorAll('.quiz').forEach(qz=>{
  const id=qz.dataset.quiz,ans=qz.dataset.answer,fb=qz.querySelector('.fb'),st=qz.querySelector('.st');
  const bs=[...qz.querySelectorAll('.choice')];
  const win=(b,silent)=>{
   qz.dataset.ok='1';qz.classList.add('done');bs.forEach(x=>x.classList.remove('wrong'));b.classList.add('right');
   fb.className='fb yes';fb.textContent='Right. '+b.dataset.why;st.textContent='Passed';
   const old=qz.querySelector('.backbtn');if(old)old.remove();
   if(!silent){S.set('q:'+id,'ok');tone(true);update()}
  };
  bs.forEach(b=>b.addEventListener('click',()=>{
   if(qz.dataset.ok)return;
   if(b.dataset.k===ans){win(b);return}
   tone(false);
   b.classList.add('wrong');fb.className='fb no';fb.textContent=(b.dataset.back?'':'Not this one. ')+b.dataset.why+(b.dataset.back?'':' Try again.');
   if(b.dataset.back&&!qz.querySelector('.backbtn')){
    const bb=document.createElement('button');bb.type='button';bb.className='backbtn';bb.textContent='Back to card '+b.dataset.back;
    bb.addEventListener('click',()=>{const d=ds[+b.dataset.back-1];d.open=true;openTest(d);d.scrollIntoView({behavior:'smooth'});b.classList.remove('wrong');bb.remove();fb.textContent=''});
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

 /* matching game: tap a job then a visual, or drag a job onto a visual */
 const mg=document.getElementById('match');let sync=()=>{};
 if(mg){
  let done={};try{done=JSON.parse(S.get('match')||'{}')}catch(e){}
  const jobs=[...mg.querySelectorAll('.mjob')],vis=[...mg.querySelectorAll('.mvis')],fb=mg.querySelector('.fb');
  let sel=null;
  const mark=()=>{
   jobs.forEach(j=>{const ok=!!done[j.dataset.m];j.classList.toggle('ok',ok);j.disabled=ok;j.draggable=!ok;
    const s=j.querySelector('small');if(s)s.textContent=ok?'→ '+mg.querySelector(`.mvis[data-v="${j.dataset.m}"] span`).textContent:''});
   vis.forEach(v=>v.classList.toggle('ok',!!done[v.dataset.v]));
   const all=jobs.every(j=>done[j.dataset.m]);mg.dataset.ok=all?'1':'';
   mg.querySelector('.st').textContent=all?'All matched':jobs.filter(j=>done[j.dataset.m]).length+' of '+jobs.length+' matched';
  };
  const pick=j=>{if(done[j.dataset.m])return;sel=j;jobs.forEach(x=>x.classList.toggle('sel',x===j));fb.className='fb';fb.textContent='Now tap the visual for: '+j.dataset.label};
  const tryMatch=(j,v)=>{
   if(!j||done[j.dataset.m])return;
   if(v.dataset.v===j.dataset.m){done[j.dataset.m]=1;S.set('match',JSON.stringify(done));sel=null;jobs.forEach(x=>x.classList.remove('sel'));
    fb.className='fb yes';fb.textContent='Right. '+j.dataset.label+' → '+v.querySelector('span').textContent+'.';tone(true);mark();sync();update()}
   else{tone(false);fb.className='fb no';fb.textContent='Not quite. '+v.querySelector('span').textContent+' is for '+v.dataset.what+'. Try another.';
    [j,v].forEach(x=>{x.classList.add('bad');setTimeout(()=>x.classList.remove('bad'),700)})}
  };
  jobs.forEach(j=>{j.addEventListener('click',()=>pick(j));j.addEventListener('dragstart',e=>{pick(j);try{e.dataTransfer.setData('text/plain',j.dataset.m)}catch(x){}})});
  vis.forEach(v=>{
   v.addEventListener('click',()=>{if(sel)tryMatch(sel,v);else{fb.className='fb';fb.textContent='Tap a job on the left first.'}});
   v.addEventListener('dragover',e=>{e.preventDefault();v.classList.add('drop')});
   v.addEventListener('dragleave',()=>v.classList.remove('drop'));
   v.addEventListener('drop',e=>{e.preventDefault();v.classList.remove('drop');tryMatch(sel,v)});
  });
  mark();
 }

 /* preference questionnaire */
 const pf=document.getElementById('prefs');
 if(pf){
  let saved={};try{saved=JSON.parse(S.get('prefs')||'{}')}catch(e){}
  const load=o=>pf.querySelectorAll('input').forEach(i=>{if(i.type==='text')i.value=o[i.name]||'';else i.checked=!!o[i.name+'='+i.value]});
  load(saved);
  const cmp=document.getElementById('compare');
  sync=()=>{
   const o={};pf.querySelectorAll('input').forEach(i=>{if(i.type==='text')o[i.name]=i.value;else if(i.checked)o[i.name+'='+i.value]=1});
   S.set('prefs',JSON.stringify(o));
   const ok=prefOk(pf),txt=prefBlock(pf);
   pf.dataset.ok=ok?'1':'';
   document.getElementById('prefblock').textContent=ok?txt:'Answer every question above and your block appears here.';
   if(ok)S.set('f:l1_block',txt);
   const tr=pf.closest('.try');tr.classList.toggle('done',ok);tr.querySelector('.st').textContent=ok?'Block built, saved':'Answer all';
   const v1=val('l1_block_v1');
   if(cmp){cmp.classList.toggle('shut',!v1);document.getElementById('v1block').textContent=v1;
    document.getElementById('v2block').textContent=ok?txt:'Answer every question to build Version 2.'}
   const rt=document.getElementById('retake');if(rt)rt.disabled=!ok;
  };
  pf.addEventListener('change',e=>{
   const t=e.target;
   if(t.name==='read'&&t.checked){ // "None" clears the rest, anything else clears "None"
    if(t.value==='none')pf.querySelectorAll('[name=read]').forEach(x=>{if(x!==t)x.checked=false});
    else{const n=pf.querySelector('[name=read][value=none]');if(n)n.checked=false}
   }
   sync();update()});
  pf.addEventListener('input',()=>{sync();update()});
  const rt=document.getElementById('retake');
  if(rt)rt.addEventListener('click',()=>{
   if(!pf.dataset.ok)return;
   S.set('f:l1_block_v1',prefBlock(pf));S.del('f:l1_block');load({});sync();update();
   pf.scrollIntoView({behavior:'smooth',block:'start'});
  });
  sync();
 }

 /* read aloud */
 const tg=document.getElementById('soundtoggle');
 if(tg){
  const canSpeak='speechSynthesis' in window;
  const paint=()=>{const on=soundOn();tg.setAttribute('aria-pressed',on?'true':'false');tg.textContent=on?'Sound: on':'Sound: off';
   document.querySelectorAll('.speakrow').forEach(r=>r.classList.toggle('shut',!on||!canSpeak));
   if(!on&&canSpeak)speechSynthesis.cancel()};
  tg.addEventListener('click',()=>{S.set('sound',soundOn()?'off':'on');paint();if(soundOn())tone(true)});
  ds.forEach(d=>{
   const body=d.querySelector('.body');if(!body)return;
   const row=document.createElement('div');row.className='speakrow';
   const b=document.createElement('button');b.type='button';b.className='speak';b.textContent='🔊 Read aloud';row.appendChild(b);body.prepend(row);
   b.addEventListener('click',()=>{
    if(!canSpeak)return;
    if(speechSynthesis.speaking){speechSynthesis.cancel();document.querySelectorAll('.speak').forEach(x=>x.textContent='🔊 Read aloud');return}
    const c=d.querySelector('.learn').cloneNode(true);c.querySelectorAll('pre,button,.copyhead,.speakrow,svg').forEach(x=>x.remove());
    let txt=d.querySelector('summary').textContent.replace(/^\d+/,'')+'. '+c.innerText.replace(/\s+/g,' ');
    const t=d.querySelector('.test:not(.shut)');
    if(t)t.querySelectorAll('.q,.sample').forEach(q=>{txt+=' '+q.innerText});
    const u=new SpeechSynthesisUtterance(txt);u.lang='en-US';u.rate=1;
    u.onend=u.onerror=()=>{b.textContent='🔊 Read aloud'};
    b.textContent='■ Stop';speechSynthesis.speak(u);
   });
  });
  paint();
 }

 /* group copy (work order) and live blocks */
 document.querySelectorAll('[data-copygroup]').forEach(b=>b.addEventListener('click',()=>copyText(workOrder(),b)));
 const live=()=>{const m=document.getElementById('master');if(m)m.textContent=master();const p=document.getElementById('protocol');if(p)p.textContent=PROTOCOL};

 /* cards, meter, unlock */
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
  const items=KIT.map(([t,s,fn,hide])=>({t,s,v:fn(),hide})).filter(i=>i.v||!i.hide);
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
