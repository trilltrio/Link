from build import quiz, field, typed, card, nextblock, E, LATER
from pages.common import mine, head, credit
TITLE = 'Lesson 1 Fast Digestion'
LESSON = 'l1'

PLATE = '''<style>
.plate{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,.8fr) minmax(0,1.4fr);gap:clamp(14px,3vw,36px);align-items:end;background:#0c2a49;border:1px solid var(--line);border-radius:10px;padding:clamp(16px,3vw,28px)}
.col{display:flex;flex-direction:column}
.txt{width:100%;border-radius:4px;background:repeating-linear-gradient(to bottom,var(--line) 0 6px,transparent 6px 13px);transform-origin:bottom;animation:grow 1.2s ease-out both}
.txt.big{background:repeating-linear-gradient(to bottom,#3a6a98 0 6px,transparent 6px 13px)}
@keyframes grow{from{transform:scaleY(.05)}to{transform:scaleY(1)}}
.fn{font-weight:300;font-size:clamp(30px,4.5vw,50px);line-height:1;margin-top:10px;white-space:nowrap}
.fl{color:var(--mute);font-size:14px}
.stack{display:grid;gap:8px}
.slot{border-radius:6px;padding:11px 14px;background:#123a63;border:1px solid var(--line)}
.slot b{display:block;font-size:17px}
.slot span{color:var(--mute);font-size:14px}
.slot.p1{background:var(--pink);border-color:var(--pink);color:var(--pink2)}
.slot.p1 span{color:#4a0d20}
@media(max-width:760px){.plate{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.plate .col:last-child{grid-column:1/-1}}
</style>
<div class="plate" role="img" aria-label="A 600-word answer beside a 3,200-word answer, and the 4-part stack that replaces them">
<div class="col"><div class="txt" style="height:calc(min(40vw,320px)*600/3200)"></div><div class="fn">600</div><div class="fl">words, typical answer</div></div>
<div class="col"><div class="txt big" style="height:min(40vw,320px)"></div><div class="fn">3,200</div><div class="fl">words, top user's answer</div></div>
<div class="col"><div class="stack">
<div class="slot p1"><b>1. Needs you</b><span>Stop here if that's all you need</span></div>
<div class="slot"><b>2. Goal met?</b><span>Yes, partly or no, with proof</span></div>
<div class="slot"><b>3. Short path</b><span>Next 1 to 3 moves</span></div>
<div class="slot"><b>4. Errors and why</b><span>What broke, what's a guess</span></div>
</div><div class="fl" style="margin-top:10px">Same work, read top-down</div></div>
</div>'''

MESSY = ('I went through the bakery site and fixed the menu layout, which took a while because the photos were huge, so I shrank them. '
         'The menu page should load faster now. I also noticed the order form doesn\'t send anywhere yet, and I wasn\'t sure which email '
         'you want orders to go to. I\'m not fully sure the shrinking didn\'t blur the cake photos.')
GOOD = ('1. Needs you: which email should orders go to?\n2. Goal met? Partly. The menu loads faster; the order form doesn\'t send yet.\n'
        '3. Short path: you send the email, I connect the form, then test one order.\n4. Errors and why: the cake photos may look blurry after shrinking. Not checked yet.')

VIS = ['One-page HTML page', 'Docs', 'Dashboards', 'Whiteboards', 'Sheets', 'Slides', 'Motion (short animated explainers)']

def opt(kind, name, value, label):
    return f'<label class="opt2"><input type="{kind}" name="{name}" value="{E(value)}"><span>{E(label)}</span></label>'

def prefs(v):
    f = ('<fieldset><legend>1. How should answers be built?</legend>' +
         opt('radio', 'structure', 'four', 'Top-down in four parts: needs me, goal met?, short path, errors and why') +
         opt('radio', 'structure', 'concise', 'Just keep it concise') + '</fieldset>'
         '<fieldset><legend>2. Which visuals do you want instead of long prose? Pick any.</legend>' +
         ''.join(opt('checkbox', 'vis', x, x) for x in VIS) + '</fieldset>')
    if v == 'didier':
        f += mine(v,
            '<fieldset><legend>3. How do you read?</legend>' +
            opt('radio', 'speed', 'fast', 'Fast. I skim.') + opt('radio', 'speed', 'slow', 'I take my time.') + '</fieldset>'
            '<fieldset><legend>4. Words or visuals first?</legend>' +
            opt('radio', 'lead', 'visual', 'Visual first') + opt('radio', 'lead', 'words', 'Words first') + opt('radio', 'lead', 'both', 'Both, side by side') + '</fieldset>'
            '<fieldset><legend>5. Match the visual to the job? Pick any.</legend>' +
            opt('checkbox', 'map', 'num', 'Numbers I track go on a dashboard') + opt('checkbox', 'map', 'walk', 'Walkthroughs go on slides') + '</fieldset>'
            '<fieldset><legend>6. Anything that makes reading harder?</legend>' +
            opt('radio', 'read', 'none', 'No') + opt('radio', 'read', 'dys', 'Dyslexia') + opt('radio', 'read', 'other', 'Something else') +
            '<input type="text" name="read_other" placeholder="Tell your agent in a few words" autocomplete="off"></fieldset>')
    return f'<form id="prefs" class="prefs" onsubmit="return false">{f}</form>'

def body(v, vname):
    c1 = card(1, 'Where the numbers come from',
        '<p>The video cites two Anthropic studies. Top users get answers of about 3,200 words versus about 600 for everyone else. '
        'Anthropic staff spend about half their week reviewing agent output, while their agents sit idle about 80% of the time.</p>'
        '<p>So the slow part is not the agent working. It is you reading.</p>',
        quiz('l1q1', 'Per the video, where does the time actually go when you work with agents?', 'b', [
            ('a', 'The agent doing the work', 'Per the video, agents sit idle about 80% of the time.'),
            ('b', 'You reading and reviewing what it wrote', 'Staff spend about half their week reviewing. Reading is the slow part.'),
            ('c', 'Writing the prompt', 'The prompt matters (that is Lesson 2), but here the slow part is review.'),
            ('d', 'Waiting for the model to answer', 'The video never names waiting as the problem. Review is.')]))

    c2 = card(2, 'Four parts, top-down',
        '<p>The video\'s fix is an answer style with four parts, in this order:</p>'
        '<ol><li><b>Needs you:</b> what only you can decide or give.</li><li><b>Goal met?</b> Yes, partly or no.</li>'
        '<li><b>Short path:</b> the next few steps.</li><li><b>Errors and why:</b> what went wrong and the reason.</li></ol>'
        '<p>If nothing needs you, you can stop after line one. The video also mentions Claude Code\'s built-in concise output style as the simpler option.</p>'
        '<div class="vs"><div class="bad"><b>Wrong: a story</b>I started by reviewing the files, then I updated the header, then I tried the form, which mostly worked, and along the way I noticed...</div>'
        '<div class="good"><b>Right: top-down</b>1. Needs you: pick the order email.<br>2. Goal met? Partly.<br>3. Short path: set email, publish.<br>4. Errors: none.</div></div>',
        f'<div class="sample"><b>An agent sends you this</b>{E(MESSY)}</div>' +
        quiz('l1q2', 'Rebuilt top-down, what goes on the very first line?', 'b', [
            ('a', 'The photos may be blurry', 'That is an error. Errors go last.'),
            ('b', 'Which email should orders go to?', 'It is the one thing only you can answer, so it goes first.'),
            ('c', 'The menu loads faster now', 'That is progress on the goal. It comes second.'),
            ('d', 'It fixed the menu layout', 'That is a step it took. Steps are the long part you want to skip.')]))

    c3 = card(3, 'Ask for visuals, not prose',
        '<p>The second fix in the video: when an answer is big, get it as a visual you can read at a glance. '
        'The formats it names are a one-page HTML page (like this lesson), Docs, Dashboards, Whiteboards, Sheets, Slides and Motion.</p>' +
        mine(v, '<p style="margin:6px 0">Which visual for which job:</p><div class="scroll"><table><tbody>'
             '<tr><td>Numbers you watch</td><td>Dashboard</td></tr><tr><td>Rows to sort or fill</td><td>Sheet</td></tr>'
             '<tr><td>A plan to keep</td><td>Doc</td></tr><tr><td>A process</td><td>Whiteboard</td></tr>'
             '<tr><td>A walkthrough</td><td>Slides</td></tr><tr><td>A one-off report or lesson</td><td>One-page HTML</td></tr></tbody></table></div>'),
        '<div class="sample"><b>The situation</b>You ask your agent to compare prices from five flour suppliers. It sends back 900 words.</div>' +
        quiz('l1q3', 'Per the video, what should you ask for instead?', 'c', [
            ('a', 'A longer, more careful explanation', 'More words is the problem, not the fix.'),
            ('b', 'The same text with key words in bold', 'Still 900 words to read.'),
            ('c', 'A visual, like a sheet or a one-page page', 'You see all five suppliers side by side at a glance.'),
            ('d', 'Nothing, just read it slower', 'Reading is already the slow part.')]))

    c4 = card(4, 'Build your answer-style block',
        '<p>Your agent can\'t guess how you like to read. Answer the questions below and this page writes the block for you. '
        'You give that block to your agent once, as a standing instruction, and every answer after that follows it.</p>',
        '<div class="try"><div class="tryhead">Try it now<span class="st">Answer all</span></div>' + LATER + prefs(v) +
        '<div class="copyhead"><b>Your block</b><button type="button" data-copy="prefblock">Copy</button></div>'
        '<pre id="prefblock" class="tmpl"></pre></div>')

    c5 = card(5, 'Test your block',
        '<ol><li>Copy your block from card 4.</li>'
        '<li>Paste it where your agent keeps standing instructions (project instructions, custom instructions, or a CLAUDE.md file).</li>'
        '<li>Ask it to redo one answer it already gave you, then put the old and new answers side by side.</li></ol>',
        quiz('l1q5', 'Did you notice the difference?', 'yes', [
            ('yes', 'Yes', 'Your block works. Leave it on.'),
            ('no', 'No', 'Then your block needs fixing. Go back to card 4, change your answers, paste the new block and try again.', 4)],
            head='Try it now (yes or no)'))

    c6 = card(6, 'Rewrite one answer by hand',
        '<p>Your agent will do this for you from now on. Doing it once by hand trains your eye, so you can tell a good answer from a long one in seconds.</p>',
        f'<div class="sample"><b>Rewrite this answer</b>{E(MESSY)}</div>' +
        typed('Put it in the four parts, one line each.',
              field('l1_need', '1. Needs you', 'What only you can decide or give.', 3),
              field('l1_goal', '2. Goal met?', 'Yes, partly or no.', 3),
              field('l1_path', '3. Short path', 'The next few steps.', 3),
              field('l1_err', '4. Errors and why', 'What went wrong or is a guess.', 3),
              extra=f'<details class="peek"><summary>Compare with one good version</summary><div class="body" style="padding-left:16px"><pre class="tmpl">{E(GOOD)}</pre></div></details>'))

    top = head(v, vname, 1, 'Lesson 1: read your agents in under a minute', 6, PLATE, [
        ('What it is', 'Agent answers built the way you read: top-down, with visuals.'),
        ('Why it matters', "Reading the output is the slow part, not the agent's work."),
        ('What to do', 'Build your answer-style block and give it to your agent.'),
        ('How you know', 'You notice the difference on the very next answer.')])
    return top + f'''<section class="band alt">
<div class="wrap">
<h2>Unlock the lesson</h2>
<p class="hint">Each card has a learning part, then a test. Pass all six to unlock Lesson 2.</p>
<div class="locks" id="locks">
{c1}{c2}{c3}{c4}{c5}{c6}
</div>
{nextblock('lesson2.html', 'Go to Lesson 2: the manager brief', 'Platinum: Lesson 1 complete.')}
{credit()}
</div>
</section>'''
