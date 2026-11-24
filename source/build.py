import html, pathlib, importlib, sys
ROOT = pathlib.Path(__file__).parent
CSS = (ROOT/'src/style.css').read_text()
JS = (ROOT/'src/app.js').read_text()
E = html.escape
VERSIONS = {'creator': ('Creator version', 'sp1c'), 'didier': ("Didier's version", 'sp1d')}
LATER = '<p class="later">Finish the lesson. Everything you write is waiting for you at the end.</p>'

def quiz(qid, q, answer, choices, head='Try it now'):
    bs = ''.join(f'<button type="button" class="choice" data-k="{c[0]}" data-why="{E(c[2])}"' +
                 (f' data-back="{c[3]}"' if len(c) > 3 else '') + f'>{E(c[1])}</button>' for c in choices)
    return (f'<div class="try quiz" data-quiz="{qid}" data-answer="{answer}"><div class="tryhead">{head}<span class="st">Pick one</span></div>'
            f'<p class="q">{E(q)}</p><div class="choices">{bs}</div><p class="fb" aria-live="polite"></p></div>')

def field(fid, label, sub='', minlen=3, big=True, ph=''):
    inp = (f'<textarea id="{fid}" data-save="{fid}" data-min="{minlen}" placeholder="{E(ph)}"></textarea>' if big else
           f'<input type="text" id="{fid}" data-save="{fid}" data-min="{minlen}" placeholder="{E(ph)}" autocomplete="off">')
    s = f'<small>{E(sub)}</small>' if sub else ''
    return (f'<div class="field"><label for="{fid}">{E(label)}{s}</label>{inp}'
            f'<div class="frow"><span>Not answered yet</span><button type="button">Copy</button></div></div>')

def typed(intro, *fields, head='Try it now', extra=''):
    return (f'<div class="try typed"><div class="tryhead">{head}<span class="st">Saved as you type</span></div>'
            f'<p class="q">{E(intro)}</p>{LATER}{"".join(fields)}{extra}</div>')

def card(n, title, learn, test):
    return (f'<details><summary><span class="lk">{n}</span>{E(title)}</summary><div class="body">'
            f'<div class="learn">{learn}</div><div class="testdiv">Test</div><div class="test">{test}</div></div></details>')

def nextblock(href, label, plat):
    return (f'<div class="plat" id="plat">{E(plat)}</div>'
            f'<div class="next"><a id="nextbtn" class="nextbtn locked" href="{href}" aria-disabled="true" tabindex="-1">'
            f'<span>{E(label)}</span><span class="ico" aria-hidden="true">🔒</span></a><p class="nextnote" id="nextnote"></p></div>')

def page(title, lesson, body, prefix=''):
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
<body data-lesson="{lesson}" data-prefix="{prefix}" id="top">
{body}
<script>
{JS}</script>
</body>
</html>
'''

REDIRECT = '<!DOCTYPE html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=index.html"><title>Study Plan 1</title><a href="index.html">Study Plan 1</a>'

def build():
    out = ROOT/'site'; out.mkdir(exist_ok=True)
    idx = importlib.import_module('pages.index')
    (out/'index.html').write_text(page(idx.TITLE, 'home', idx.body()))
    for v, (vname, prefix) in VERSIONS.items():
        d = out/v; d.mkdir(exist_ok=True)
        for name in ['lesson1', 'lesson2', 'finish']:
            mod = importlib.import_module('pages.'+name)
            (d/f'{name}.html').write_text(page(mod.TITLE, mod.LESSON, mod.body(v, vname), prefix))
    for old in ['lesson1', 'lesson2', 'lesson3']:  # old v1 addresses
        (out/f'{old}.html').write_text(REDIRECT)
    (out/'.nojekyll').write_text('')
    print('built')

if __name__ == '__main__':
    sys.path.insert(0, str(ROOT)); sys.modules['build'] = sys.modules['__main__']; build()
