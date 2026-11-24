import html, pathlib
ROOT = pathlib.Path(__file__).parent
CSS = (ROOT/'src/style.css').read_text()
JS = (ROOT/'src/app.js').read_text()
E = html.escape

def quiz(qid, q, answer, choices, head='Try it now'):
    bs = ''.join(f'<button type="button" class="choice" data-k="{k}" data-why="{E(why)}">{E(t)}</button>' for k, t, why in choices)
    return (f'<div class="try quiz" data-quiz="{qid}" data-answer="{answer}"><div class="tryhead">{head}<span class="st">Pick one</span></div>'
            f'<p class="q">{E(q)}</p><div class="choices">{bs}</div><p class="fb" aria-live="polite"></p></div>')

def field(fid, label, sub='', minlen=3, big=True, ph=''):
    inp = (f'<textarea id="{fid}" data-save="{fid}" data-min="{minlen}" placeholder="{E(ph)}"></textarea>' if big else
           f'<input type="text" id="{fid}" data-save="{fid}" data-min="{minlen}" placeholder="{E(ph)}" autocomplete="off">')
    s = f'<small>{E(sub)}</small>' if sub else ''
    return (f'<div class="field"><label for="{fid}">{E(label)}{s}</label>{inp}'
            f'<div class="frow"><span>Not answered yet</span><button type="button">Copy</button></div></div>')

def typed(intro, *fields, head='Try it now'):
    return (f'<div class="try typed"><div class="tryhead">{head}<span class="st">Your real work, saved</span></div>'
            f'<p class="q">{E(intro)}</p>{"".join(fields)}</div>')

def card(n, title, body):
    return f'<details><summary><span class="lk">{n}</span>{E(title)}</summary><div class="body">{body}</div></details>'

def nextblock(href, label, plat):
    return (f'<div class="plat" id="plat">{E(plat)}</div>'
            f'<div class="next"><a id="nextbtn" class="nextbtn locked" href="{href}" aria-disabled="true" tabindex="-1">'
            f'<span>{E(label)}</span><span class="ico" aria-hidden="true">🔒</span></a><p class="nextnote" id="nextnote"></p></div>')

def page(title, lesson, body):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;600;800&display=swap" rel="stylesheet">
<style>
{CSS}</style>
</head>
<body data-lesson="{lesson}" id="top">
{body}
<script>
{JS}</script>
</body>
</html>
'''

def build():
    out = ROOT/'site'; out.mkdir(exist_ok=True)
    for name in ['index', 'lesson1', 'lesson2', 'lesson3']:
        mod = __import__('pages.'+name, fromlist=['x'])
        (out/f'{name}.html').write_text(page(mod.TITLE, mod.LESSON, mod.body()))
    (out/'.nojekyll').write_text('')
    print('built', sorted(p.name for p in out.iterdir()))

if __name__ == '__main__':
    import sys; sys.path.insert(0, str(ROOT)); build()
