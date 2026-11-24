from build import quiz, field, typed, card, nextblock, E
from pages.common import mine, head, credit
TITLE = 'Lesson 2 Manager Brief'
LESSON = 'l2'

TICKET = '''<style>
.ticket{background:var(--paper);color:#0a2540;border-radius:10px;padding:clamp(16px,3vw,28px);box-shadow:0 2px 0 #06192c,0 18px 0 -8px #0d3159;position:relative}
.thead{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;border-bottom:2px solid #0a2540;padding-bottom:10px;margin-bottom:6px}
.thead b{font-size:clamp(18px,2.4vw,24px);letter-spacing:-.01em}
.thead span{font-size:14px;color:#3c5a78}
.tf{display:grid;grid-template-columns:150px minmax(0,1fr);gap:14px;padding:12px 0;border-bottom:1px dashed #9fb4c9}
.tf:last-of-type{border-bottom:0}
.tl{font-weight:800;font-size:15px;display:flex;gap:8px;align-items:baseline}
.tl em{font-style:normal;display:inline-grid;place-items:center;width:26px;height:26px;border-radius:50%;background:#0a2540;color:#fff;font-size:13px;flex:none}
.tf:nth-of-type(4) .tl em{background:var(--pink);color:var(--pink2)}
.tv{font-size:16px}
.stamp{position:absolute;right:clamp(12px,3vw,28px);bottom:clamp(12px,3vw,24px);border:3px solid var(--pink);color:var(--pink);font-weight:800;font-size:14px;padding:4px 10px;border-radius:6px;transform:rotate(-6deg);background:rgba(255,92,138,.06)}
@media(max-width:600px){.tf{grid-template-columns:minmax(0,1fr);gap:4px}.stamp{position:static;display:inline-block;margin-top:10px}}
</style>
<div class="ticket" role="img" aria-label="Example work order with four fields">
<div class="thead"><b>Work order: bakery website</b><span>Agent: website builder</span></div>
<div class="tf"><div class="tl"><em>1</em>Full job</div><div class="tv">Build a one-page site where customers order a custom cake. Copy, layout, order form and publishing, all of it.</div></div>
<div class="tf"><div class="tl"><em>2</em>Why</div><div class="tv">Phone orders get lost. An order that arrives in writing is the only result that matters.</div></div>
<div class="tf"><div class="tl"><em>3</em>Guardrails</div><div class="tv">Free tools only. No prices on the page until I approve them. If something needs paying for, stop and ask.</div></div>
<div class="tf"><div class="tl"><em>4</em>Done looks like</div><div class="tv">Loads on a phone in under 3 seconds and a test order reaches my inbox. Run these checks yourself before reporting.</div></div>
<div class="stamp">Plan first, then hand off</div>
</div>'''

INTERVIEW = 'Before doing anything, interview me so you can write a full brief for this job. Ask me questions until you can cover the full job, why it matters, the guardrails, and what done looks like with checks you can run yourself. Then show me the brief in four parts and wait for my go.'

TMPL = '''Full job: [the whole outcome, not a step]
Why: [what this is for, and the one result that matters]
Guardrails: [a few plain limits; what to do if one is hit]
Done looks like: [testable checks]. Run these checks yourself and show me the results before you report back.'''

def body(v, vname):
    c1 = card(1, 'The full job, not a step',
        '<p>The video says top users hand over the whole outcome. A step makes the agent wait for you after every move; the whole job lets it plan the order itself.</p>'
        '<div class="vs"><div class="bad"><b>Wrong: a step</b>Make a header for the site.</div><div class="good"><b>Right: the full job</b>Build the whole site that gets customers to order.</div></div>',
        quiz('l2q1', 'Which one is a full job?', 'c', [
            ('a', 'Make a header for the bakery site.', 'That is one step. The agent stops and waits for the next.'),
            ('b', 'Pick some colors for the site.', 'Still a step, and no outcome to aim at.'),
            ('c', 'Build the whole bakery site that gets customers to order a cake.', 'The whole outcome, so the agent can plan the order itself.'),
            ('d', 'Fix the footer.', 'A step. Useful, but the agent cannot plan around it.')]))

    c2 = card(2, 'Why: the intent behind it',
        '<p>The why lets the agent make the calls you didn\'t think of. If it knows orders are the goal, it puts the order button where people see it without being told.</p>'
        '<div class="vs"><div class="bad"><b>Wrong: no why</b>Add an order form.</div><div class="good"><b>Right: with why</b>A written order is the only goal, so the form is the most important thing on the page.</div></div>',
        quiz('l2q2', 'Which line gives the agent the why?', 'c', [
            ('a', 'Add an order form.', 'That is a task with no reason behind it.'),
            ('b', 'Use pink and brown.', 'A style choice, not the intent.'),
            ('c', 'Orders are the only goal, so the order button matters most.', 'Now the agent can make calls you never mentioned, like moving the button up top.'),
            ('d', 'Make it nice.', 'Vague, and still no reason.')]))

    c3 = card(3, 'Guardrails: few, calm, specific',
        '<p>A few hard limits, written plainly. The video warns against ALL-CAPS "CRITICAL" or "MUST" wording, because it makes models overreact.</p>'
        '<div class="vs"><div class="bad"><b>Wrong: shouting</b>CRITICAL: you MUST NEVER use paid tools!!!</div><div class="good"><b>Right: calm</b>Use only free tools. If something needs paying for, stop and ask me.</div></div>',
        quiz('l2q3', 'Which guardrail will an agent follow best?', 'b', [
            ('a', 'CRITICAL: you MUST NEVER use paid tools!!!', 'Shouting makes models overreact near the rule.'),
            ('b', 'Use only free tools. If something needs paying for, stop and ask me.', 'Calm, specific, and it says what to do when the limit is hit.'),
            ('c', 'Be careful with money.', 'Too vague to follow or check.'),
            ('d', "Don't do anything bad.", 'Names no limit at all.')]))

    c4 = card(4, 'Done looks like, plus self-checks',
        '<p>Describe done as things you could test, then tell the agent to run those tests itself before it reports. The video credits this to Boris Cherny, who created Claude Code.</p>'
        '<div class="vs"><div class="bad"><b>Wrong: vague</b>Make it look good.</div><div class="good"><b>Right: testable</b>Loads under 3 seconds on a phone. The test order arrives. Show me the result.</div></div>',
        quiz('l2q4', 'Which "done" can the agent check by itself?', 'c', [
            ('a', 'Make it look good.', 'Nobody can test "good".'),
            ('b', 'Make it professional.', 'Same problem: no check to run.'),
            ('c', 'Loads on a phone in under 3 seconds and the test order reaches my inbox. Run these checks and show me.', 'Two tests the agent can run, plus the order to run them.'),
            ('d', 'Done when you think it is done.', 'That hands the call back to the agent with nothing to measure.')]))

    c5 = card(5, "Can't fill the four? Get interviewed",
        '<p>When the job is still fuzzy, the video\'s move is to flip it: the agent asks, you answer, and it writes the brief.</p>'
        f'<div class="copyhead"><b>Interview prompt</b><button type="button" data-copy="interview">Copy</button></div><pre id="interview" class="tmpl">{E(INTERVIEW)}</pre>',
        quiz('l2q5', "You know you need a site but can't say what done looks like. What now?", 'b', [
            ('a', 'Send the four lines with "Done: TBD"', 'A blank line means the agent guesses, and guesses are what cause redirects.'),
            ('b', 'Paste the interview prompt and answer its questions', 'The agent pulls the missing line out of you.')], head='Try it now (1 of 2)'))

    c6 = card(6, 'The blank work order',
        '<p>Paste this at the top of any agent job and fill the four lines.</p>'
        f'<div class="copyhead"><b>Brief template</b><button type="button" data-copy="tmpl">Copy</button></div><pre id="tmpl" class="tmpl">{E(TMPL)}</pre>',
        typed('Fill the work order for a real job of your own.',
              field('l2_job', 'Full job', 'The whole outcome, not a step.', 8),
              field('l2_why', 'Why', 'What it is for, and the one result that matters.', 8),
              field('l2_guard', 'Guardrails', 'A few calm limits, and what to do if one is hit.', 8),
              field('l2_done', 'Done looks like', 'Checks the agent can run itself.', 8),
              extra='<button type="button" class="groupcopy" data-copygroup="1">Copy all four, with titles</button>'))

    c7 = card(7, 'Drill and pass or fail',
        '<ol><li>Pick a real agent job.</li><li>Send it your filled work order. If a line is still blank, use the interview prompt first.</li><li>Let the agent run without stepping in.</li></ol>'
        '<div class="pass"><div class="ok"><b>Pass</b><br>The first run passes its own checks, and your fixes are small.</div><div class="no"><b>Fail</b><br>You had to redirect it. Find which of the four lines was missing.</div></div>',
        quiz('l2q7', 'Your first run needed redirecting. What is the first move?', 'b', [
            ('a', 'Rewrite the brief in ALL CAPS so it listens', 'Shouting makes it worse, per card 3.'),
            ('b', 'Find which of the four lines was missing or vague, fix it, rerun', 'The fix lives in the brief, not in more pushing.'),
            ('c', 'Give up on agents for this job', 'Per the video, beginners quit about 19% of the time versus 5 to 7% for top users. Fix the brief instead.'),
            ('d', 'Do the job yourself', 'That puts all the planning and the work back on you.')]) +
        typed('Lock in the drill.', field('l2_task', 'Which real job gets this brief first?', '', 3, big=False)))

    split = ('<div class="saved"><h2 style="margin-top:8px">Take these with you</h2>' +
        mine(v, '<p style="margin:4px 0 0">Splitting the lesson into a master prompt and a protocol.</p>') +
        '<div class="copyhead"><b>1. Master prompt: save this</b><button type="button" data-copy="master">Copy</button></div>'
        '<p class="src">Your filled work order. Paste it at the top of the job.</p><pre id="master" class="tmpl"></pre>'
        '<div class="copyhead" style="margin-top:16px"><b>2. Protocol: work this into your setup later</b><button type="button" data-copy="protocol">Copy</button></div>'
        '<p class="src">The lesson as a standing rule your agent follows on every job.</p><pre id="protocol" class="tmpl"></pre></div>')

    top = head(v, vname, 2, 'Lesson 2: brief the agent like a manager', 7, TICKET, [
        ('What it is', 'Four fields before any job: the full job, why, guardrails, what done looks like.'),
        ('Why it matters', 'Per the video, top users make most plan decisions up front, so agents get it right the first time.'),
        ('What to do', 'Fill the work order for a real job. Stuck? Have the agent interview you.'),
        ('How you know', 'The first run passes its own checks and you change nothing big.')])
    return top + f'''<section class="band alt">
<div class="wrap">
<h2>Unlock the lesson</h2>
<p class="hint">Each card has a learning part, then a test. Pass all seven to unlock what you built.</p>
<div class="locks" id="locks">
{c1}{c2}{c3}{c4}{c5}{c6}{c7}
</div>
{split}
{nextblock('finish.html', 'See what you built', 'Platinum: Lesson 2 complete.')}
<p class="src" style="margin-top:22px">The video says top users make about 70% of the plan decisions and 20% of the execution. Not checked against the raw studies.</p>
{credit()}
</div>
</section>'''
