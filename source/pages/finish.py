from pages.common import mine, credit
TITLE = 'Your Take-Home Kit'
LESSON = 'kit'

def body(v, vname):
    return f'''<section class="band">
<div class="wrap" style="max-width:820px">
<div class="crumb">{vname} · Study Plan 1 · <a href="../index.html" style="color:var(--mute)">switch version</a></div>
<h1>What you built</h1>
<p style="margin-top:14px">Every block from the lessons, ready to copy. This is what you take home.</p>
{mine(v, '<p style="margin:4px 0 0">This take-home page, collecting every block in one place.</p>')}
<button type="button" id="copyall" class="groupcopy">Copy all</button>
<div class="kit" id="kit"></div>
<div class="kitem empty" style="margin-top:16px"><b>More blocks coming</b><p class="src" style="margin:6px 0 0">Lessons 3 and up add their blocks here.</p></div>
<p class="src" style="margin-top:18px">Saved on this phone only. Copy everything before you clear your browser.</p>
<p style="margin-top:18px"><a href="lesson1.html" style="color:var(--sky)">Lesson 1</a> · <a href="lesson2.html" style="color:var(--sky)">Lesson 2</a></p>
<p style="margin-top:22px"><button type="button" id="reset">Start over</button></p>
{credit()}
</div>
</section>'''
