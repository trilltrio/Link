VIDEO = 'https://www.youtube.com/watch?v=81Jg17dQz1A'

def mine(v, html, inline=False):
    if v != 'didier':
        return ''
    return f'<div class="minebox"><span class="mine">Didier\'s addition</span>{html}</div>'

def head(v, vname, n, title, trophy_total, picture, bars):
    return f'''<section class="band">
<div class="wrap">
<div class="crumb">{vname} · Lesson {n} of 2 · <a href="../index.html" style="color:var(--mute)">switch version</a></div>
<div class="top">
<h1>{title}</h1>
<div class="trophy" id="trophy"><span id="tcount">0 / {trophy_total}</span><div class="meter"><i id="tbar"></i></div></div>
</div>
{picture}
<div class="bars">{''.join(f'<div class="bar"><small>{a}</small><div>{b}</div></div>' for a, b in bars)}</div>
</div>
</section>'''

def credit():
    return f'<p class="src" style="margin-top:22px">Built from <a href="{VIDEO}" style="color:var(--sky)">Ben AI\'s video</a> on how top Claude users work. Study numbers are the video\'s and were not checked against the raw studies.</p>'
