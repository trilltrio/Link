TITLE = 'Study Plan 1'
LESSON = 'home'

def body():
    row = lambda n, href, t, s, k: f'''<a href="{href}" style="display:grid;grid-template-columns:44px minmax(0,1fr) auto;gap:12px;align-items:center;padding:16px;border:1px solid var(--line);border-radius:8px;background:#0c2a49;color:var(--ink);text-decoration:none;margin-bottom:10px">
<span style="font-weight:300;font-size:32px;color:var(--sky);line-height:1">{n}</span><span><b>{t}</b><br><span class="src">{s}</span></span><span class="src" data-passed="{k}">Open</span></a>'''
    return f'''<section class="band">
<div class="wrap" style="max-width:640px">
<div class="crumb">Silerio Solutions</div>
<h1>Study Plan 1</h1>
<p style="margin-top:14px">Two lessons. Pass each card's Try it now to unlock the next lesson. What you type is saved on this phone and can be copied at the end.</p>
<div style="margin-top:20px">
{row(1, 'lesson1.html', 'Fast digestion', 'Read your agents in under a minute', 'l1')}
{row(2, 'lesson2.html', 'The manager brief', 'Job, why, guardrails, done', 'l2')}
</div>
<a class="nextbtn open" href="lesson1.html" style="margin-top:14px">Start Lesson 1 →</a>
</div>
</section>'''
