from build import quiz, field, typed, card, nextblock
TITLE = 'Lesson 1 Fast Digestion'
LESSON = 'l1'

STYLE = '''Answer top-down in four parts, in this order:
1. Needs you: decisions or inputs only I can give. Write "None" if none.
2. Goal met?: Yes, Partly or No in one line, with the evidence.
3. Short path: the next 1 to 3 actions, one line each.
4. Errors and why: what failed or is uncertain, and the reason. Label facts vs guesses.
Keep parts 1 to 3 under 150 words. Put detail only in part 4.
When the answer is numbers, steps or structure, deliver it as a visual (a one-page HTML page, dashboard, sheet, slides or whiteboard) instead of long prose. Lead with the visual, then four short bars, then the detail.'''

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
<div class="col"><div class="txt big" style="height:min(40vw,320px)"></div><div class="fn">3,200</div><div class="fl">words, heavy user's answer</div></div>
<div class="col"><div class="stack">
<div class="slot p1"><b>1. Needs you</b><span>Stop here if that's all you need</span></div>
<div class="slot"><b>2. Goal met?</b><span>Yes, partly or no, with proof</span></div>
<div class="slot"><b>3. Short path</b><span>Next 1 to 3 moves</span></div>
<div class="slot"><b>4. Errors and why</b><span>What broke, what's a guess</span></div>
</div><div class="fl" style="margin-top:10px">Same work, read top-down</div></div>
</div>'''

def body():
    c1 = card(1, 'Where the numbers come from', '''
<p>Ben AI's video cites two Anthropic studies. Heavy users get answers of about 3,200 words versus about 600. Staff spend about half their week reviewing agent output, while agents sit idle about 80% of the time.</p>
<p class="src">These are the video's numbers and were not checked against the raw studies.</p>''' +
        quiz('l1q1', 'Per the video, where does the time actually go when you work with agents?', 'b', [
            ('a', 'The agent doing the work', 'Per the video, agents sit idle about 80% of the time.'),
            ('b', 'You reading and reviewing what it wrote', 'Staff spend about half their week reviewing. Reading is the slow part.'),
            ('c', 'Writing the prompt', 'The prompt matters (that is Lesson 2), but here the slow part is review.'),
            ('d', 'Waiting for the model to answer', 'The video never names waiting as the problem. Review is.')]))

    c2 = card(2, 'The style block, ready to paste', f'''
<p>Same report, two ways. The left one makes you read everything to find the one thing it needs from you.</p>
<div class="vs"><div class="bad"><b>Wrong: prose dump</b>I started by reviewing the files, then I updated the header, then I tried the form, which mostly worked, and along the way I noticed a few things you may want to decide on, like whether the site should...</div>
<div class="good"><b>Right: top-down</b>1. Needs you: pick the booking email.<br>2. Goal met? Partly, form works, email not set.<br>3. Short path: set email, then deploy.<br>4. Errors: none.</div></div>
<p>Written calmly on purpose. The brief notes that ALL-CAPS "CRITICAL" wording makes models overreact. The 150-word cap and the visual line are additions for your setup.</p>
<div class="copyhead"><b>Output style block</b><button type="button" data-copy="style">Copy</button></div>
<pre id="style">{STYLE}</pre>''' +
        quiz('l1q2', 'An agent report opens with three paragraphs about what it did. What belongs on top instead?', 'b', [
            ('a', 'Errors and why', 'Errors go last. You only read them when you need the detail.'),
            ('b', 'Needs you', 'If nothing needs you, you can stop after line one.'),
            ('c', 'Goal met?', 'That is second. First you need to know if you are blocking anything.'),
            ('d', 'A full list of the steps it took', 'That is the 3,200-word problem. Steps belong in part 4 at most.')]))

    c3 = card(3, 'Which visual to ask for', '''
<div class="scroll"><table>
<thead><tr><th>If the output is</th><th>Ask for</th></tr></thead>
<tbody>
<tr><td>Numbers you watch</td><td>Dashboard</td></tr>
<tr><td>Rows to sort or fill</td><td>Sheet</td></tr>
<tr><td>A plan or decision to keep</td><td>Doc</td></tr>
<tr><td>A process or architecture</td><td>Whiteboard</td></tr>
<tr><td>A walkthrough or pitch</td><td>Slides</td></tr>
<tr><td>A one-off report or lesson</td><td>One-page HTML, like this one</td></tr>
</tbody></table></div>''' +
        quiz('l1q3', "You want to watch Silerio's weekly revenue and hours. What do you ask for?", 'a', [
            ('a', 'Dashboard', 'Numbers you watch go on a dashboard.'),
            ('b', 'Doc', 'A doc is for a plan you keep, not numbers you check every week.'),
            ('c', 'Slides', 'Slides walk someone through a story. You need a glance.'),
            ('d', 'Whiteboard', 'A whiteboard shows a process, not numbers.')]))

    c4 = card(4, 'Three ways to install it, all $0', '''
<div class="opts">
<div class="opt"><span class="tag">Option A · Permanent Fix</span><br>Paste the block into each Claude project's instructions and each agent's CLAUDE.md. That covers every chat, at about two minutes per project.</div>
<div class="opt"><span class="tag">Option B · Permanent Fix</span><br>Save it as a Claude Code output style. This covers terminal agents only; check that /output-style exists in your installed version first.</div>
<div class="opt"><span class="tag w">Wildcard · Strategic Alternative</span><br>Reorder your PIGEON goodnight report template into the 4 parts, so every handoff arrives already sorted. To test it, run one night of reports.</div>
</div>
<p style="margin-top:10px"><b>Call:</b> do A now and the Wildcard next. Use B only if terminal agents ignore A.</p>''' +
        quiz('l1q4', 'You want every chat inside one Claude project to answer in 4 parts. Which option does that?', 'a', [
            ('a', 'Option A: project instructions', 'Project instructions apply to every chat in that project.'),
            ('b', 'Option B: Claude Code output style', 'An output style only covers terminal agents, not project chats.')], head='Try it now (1 of 2)') +
        typed('Now install it for real. Paste the block into one project.',
              field('l1_project', 'Which project got the style block first?', 'Name it exactly as it shows in Claude.', 2, big=False, ph='e.g. Construct')))

    c5 = card(5, 'Drill: time yourself', '''
<ol>
<li>Open your last real agent handoff report.</li>
<li>Time how long it takes to find what it needs from you.</li>
<li>After the block is installed, run your next real task and time the same thing.</li>
</ol>
<div class="pass"><div class="ok"><b>Pass</b><br>Under 60 seconds, and faster than before.</div><div class="no"><b>Fail</b><br>Still scrolling. Cut the cap to 100 words and rerun.</div></div>''' +
        typed('Your before time. This is the number you beat.',
              field('l1_secs', 'Seconds to find what your last report needed from you', 'A guess is fine if you did not time it.', 1, big=False, ph='e.g. 140')))

    c6 = card(6, 'Rewrite one real answer', '''
<p>Take that same last report and rewrite it in the four parts, one line each. This is your first piece of finished work. It gets assembled with your Lesson 2 answers at the end.</p>''' +
        typed('Fill all four lines from your real report.',
              field('l1_need', '1. Needs you', 'What only you can decide or give. "None" counts.', 3, ph='e.g. Pick the booking email'),
              field('l1_goal', '2. Goal met?', 'Yes, Partly or No, with the proof.', 3, ph='e.g. Partly: form works, email not set'),
              field('l1_path', '3. Short path', 'Next 1 to 3 moves.', 3, ph='e.g. Set email, deploy, test on phone'),
              field('l1_err', '4. Errors and why', 'What broke or is a guess.', 3, ph='e.g. None')))

    return f'''<section class="band">
<div class="wrap">
<div class="crumb">Study Plan 1 · Lesson 1 of 2</div>
<div class="top">
<h1>Lesson 1: read your agents in under a minute</h1>
<div class="trophy" id="trophy"><span id="tcount">0 / 6</span><div class="meter"><i id="tbar"></i></div></div>
</div>
{PLATE}
<div class="bars">
<div class="bar"><small>What it is</small><div>Every agent answer comes in 4 parts, with what needs you on top.</div></div>
<div class="bar"><small>Why it matters</small><div>Reading the output is the slow part, not the agent's work.</div></div>
<div class="bar"><small>What to do</small><div>Paste the style block into your project instructions. Ask for visuals, not prose.</div></div>
<div class="bar"><small>How you know</small><div>You find what needs you in under 60 seconds.</div></div>
</div>
</div>
</section>
<section class="band alt">
<div class="wrap">
<h2>Unlock the lesson</h2>
<p class="hint">Open each card and pass its Try it now. Pass all six for platinum and Lesson 2. Your answers save on this phone as you type.</p>
<div class="locks" id="locks">
{c1}{c2}{c3}{c4}{c5}{c6}
</div>
{nextblock('lesson2.html', 'Go to Lesson 2: the manager brief', 'Platinum: Lesson 1 complete.')}
</div>
</section>'''
