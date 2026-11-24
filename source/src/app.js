(function(){
// Every typed answer in Study Plan 1, in the order they get assembled.
const FIELDS=[
 ['Lesson 1: Fast digestion',[
  ['l1_project','Project that gets the style block first'],
  ['l1_secs','Seconds to find what my last report needed from me (before)'],
  ['l1_need','1. Needs you'],
  ['l1_goal','2. Goal met?'],
  ['l1_path','3. Short path'],
  ['l1_err','4. Errors and why']]],
 ['Lesson 2: The manager brief',[
  ['l2_job','Full job'],
  ['l2_why','Why'],
  ['l2_guard','Guardrails'],
  ['l2_done','Done looks like'],
  ['l2_task','First real task this brief goes to']]]
];
const P='sp1:';
const S={get:k=>{try{return localStorage.getItem(P+k)}catch(e){return null}},
 set:(k,v)=>{try{localStorage.setItem(P+k,v)}catch(e){}},
 clear:()=>{try{Object.keys(localStorage).filter(k=>k.startsWith(P)).forEach(k=>localStorage.removeItem(k))}catch(e){}}};

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

function assemble(){
 const out=['Study Plan 1: my answers',''];
 FIELDS.forEach(([lesson,fs])=>{
  out.push(lesson);
  fs.forEach(([id,label])=>{const v=(S.get('f:'+id)||'').trim();out.push(label+': '+(v||'(not answered yet)'))});
  out.push('');
 });
 return out.join('\n').trim();
}

document.addEventListener('DOMContentLoaded',()=>{
 if('scrollRestoration' in history)history.scrollRestoration='manual';
 window.scrollTo(0,0);

 // copy buttons for templates
 document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>{
  copyText(document.getElementById(b.dataset.copy).textContent,b)}));

 // quizzes
 document.querySelectorAll('.quiz').forEach(qz=>{
  const id=qz.dataset.quiz,ans=qz.dataset.answer,fb=qz.querySelector('.fb'),st=qz.querySelector('.st');
  const bs=[...qz.querySelectorAll('.choice')];
  const win=(b,silent)=>{
   qz.dataset.ok='1';qz.classList.add('done');b.classList.add('right');
   bs.forEach(x=>x.setAttribute('aria-disabled','true'));
   fb.className='fb yes';fb.textContent='Right. '+b.dataset.why;st.textContent='Passed';
   if(!silent){S.set('q:'+id,'ok');update()}
  };
  bs.forEach(b=>b.addEventListener('click',()=>{
   if(qz.dataset.ok)return;
   if(b.dataset.k===ans){win(b)}
   else{b.classList.add('wrong');fb.className='fb no';fb.textContent='Not this one. '+b.dataset.why+' Try again.'}
  }));
  if(S.get('q:'+id)==='ok'){const b=bs.find(x=>x.dataset.k===ans);if(b)win(b,true)}
 });

 // typed answers
 document.querySelectorAll('[data-save]').forEach(el=>{
  const id=el.dataset.save,min=+(el.dataset.min||1),wrap=el.closest('.field'),st=wrap.querySelector('.frow span');
  const v=S.get('f:'+id);if(v!==null)el.value=v;
  const check=()=>{const ok=el.value.trim().length>=min;wrap.classList.toggle('ok',ok);el.dataset.ok=ok?'1':'';
   st.textContent=ok?'Saved on this phone':(el.value.trim()?'Saved, keep going':'Not answered yet');return ok};
  el.addEventListener('input',()=>{S.set('f:'+id,el.value);check();update()});
  wrap.querySelector('button').addEventListener('click',e=>copyText(el.value.trim()?el.value:'(empty)',e.currentTarget));
  check();
 });

 // cards, meter, unlock
 const ds=[...document.querySelectorAll('#locks details')];
 const done=c=>{const qs=[...c.querySelectorAll('.quiz')],fs=[...c.querySelectorAll('[data-save][data-min]')];
  return qs.every(q=>q.dataset.ok)&&fs.every(f=>f.dataset.ok)};
 function update(){
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
  const sv=document.getElementById('allanswers');if(sv)sv.textContent=assemble();
 }
 window.SP1update=update;

 // assembled answers (any page that shows them)
 const sv=document.getElementById('allanswers');
 if(sv){sv.textContent=assemble();document.getElementById('copyall').addEventListener('click',e=>copyText(assemble(),e.currentTarget))}

 // progress on the start page
 document.querySelectorAll('[data-passed]').forEach(el=>{if(S.get('pass:'+el.dataset.passed))el.textContent='Passed'});

 // two-tap reset
 const rs=document.getElementById('reset');
 if(rs)rs.addEventListener('click',()=>{
  if(rs.dataset.armed){S.clear();location.href='index.html'}
  else{rs.dataset.armed='1';rs.textContent='Tap again to erase every answer';setTimeout(()=>{delete rs.dataset.armed;rs.textContent='Start over'},4000)}
 });

 update();
});
})();
