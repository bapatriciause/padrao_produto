# Problem Definition, HMW, And Jobs To Be Done

> **Interaction rule:** Do not run this file end to end. Work with the user section by section. Ask clarifying questions, pause for their judgement, and treat the prompts as starting points to adapt, not scripts to execute blindly.

> **Before each copyable prompt block:** If the context is incomplete, ask 1-3 clarifying questions before producing output. After each major section, stop and ask what the user wants to challenge, refine, or change before continuing.

Use this chapter to move from evidence and personas into clear problem framing: job lens, problem statement, customer problem stack rank, HMWs, and the dashboard autopsy.

The core move (this maps to the deck's "From the job to the opportunity" block):

1. **Dashboard foil:** you built a quick dashboard in the morning warm-up. Pull it apart to surface the real job it stands in for — *the dashboard is the receipt, the job is the product.*
2. **Job:** name the progress the customer is trying to make, solution-free.
3. **Problem:** who has it, why it matters, and what it costs.
4. **Rank:** is this the customer's top problem, or just the team's favourite?
5. **HMW + ladder:** reframe the chosen problem as opportunities — then ask where on the AI ladder that opportunity should play.

## Chapter C At A Glance

This is the densest chapter in the pack. You do not run all of it, and you do not run it end to end. Here is the shape before you start:

| Step | Status | What you create |
|---|---|---|
| Dashboard autopsy → Job | **The on-ramp** | Pull apart the dashboard you built this morning to name the job (save `jobs-to-be-done.md` only if asked) |
| Problem statement | **Core** | `problem-statements.md` (1-2, cited, interrogated) |
| Customer stack rank | **Core — do not skip** | `problem-stack-rank.md` |
| How Might We | **Core** | `hmw-questions.md`, then place the top HMW on the AI ladder |

**Minimum path:** pull the morning dashboard apart to name the job, write 1-2 problem statements, stack-rank them the customer's way, then create HMW questions and place the top one on the AI ladder.

**At the end you should have:** 1-2 cited problem statements, a customer-ranked stack with a chosen top problem, and a set of HMWs for that problem — saved to your workspace.

**A note on time and evidence:** the deck frames this as roughly a 90-minute block, but that is the full ladder. Do the core steps well rather than rushing all five. If your evidence is thin, you can still do this — say so, use what you have, label confidence low, and note what you would gather later. Do not let Claude manufacture problem statements from nothing.

# Morning Warm-Up: Build A Dashboard (your foil)

Run this in the Day 1 morning, right after set-up (deck slide 15). It gets you building with Claude Code in ~15 minutes and produces a concrete artifact to interrogate this afternoon.

**This is a deliberate foil, not your answer.** Pick a report or metric someone in your business has asked for and build a real, clickable dashboard — then leave it. You will pull it apart this afternoon to find the real job underneath. Do not fall in love with it: *the dashboard is the receipt, the job is the product.*

```
I want you to build me a working dashboard, fast.

I'll name a report, metric, or view that someone in my business has asked for. Build it for real: pick a sensible layout, use realistic sample data if I don't give you any, and make it something I could actually open and click.

Ask me only the one or two questions you genuinely need. Otherwise make reasonable assumptions and just build it.

When it's done, tell me three things:

- Who would open this?
- How often would they open it?
- What would they do next as a result?
```

---

# Jobs To Be Done: Pull The Dashboard Apart

> **Interaction rule:** Work conversationally. Do not produce a final job statement until the user has reacted to the draft.

This is the on-ramp to problem definition (deck slide 35, first ~15 minutes). Start from the dashboard you built this morning and work backwards to the real job it stands in for. The goal is a clear, **solution-free** job — no app, dashboard, report, or AI feature named as the job.

**Autopsy prompt — run this first:**

```
Here is the dashboard I built this morning: [describe it, or point Claude at the file].

Autopsy it so I don't stop at visibility. Ask me one question at a time:

1. Who looks at this dashboard, report, alert, or summary?
2. When do they look at it?
3. What decision or action do they take next?
4. What work created the data they are looking at?
5. What happens today if nobody looks?
6. If the dashboard disappeared but the job still got done, what would be doing the work?

Then help me rewrite the opportunity as the job behind the dashboard, not the dashboard itself, in this format:

- Dashboard / visibility idea:
- Underlying job (solution-free):
- Customer problem:
- Where on the AI ladder this should play (visibility → productivity → automation → autonomy):

Keep it short. Do not generate a long list of new ideas. Help me climb from visibility to the job.
```

(The AI ladder: visibility shows the job; productivity does one step; automation runs the job with a human approving; autonomy runs unwatched and escalates exceptions. A dashboard sits on the bottom rung — aim to climb at least one rung past it.)

If your morning dashboard doesn't map onto your real opportunity, use the job lens directly with the prompt below instead. Either way, the goal is the same: a solution-free job, not a feature.

Good job statement:

```text
When a claim is denied, a processor wants to catch it before rework piles up, so they can clear the queue without overtime.
```

Weak job statement:

```text
Claims processors need an AI dashboard to track denials.
```

## JTBD Prompt

```
Read my customer evidence, personas, and insights from `workspaces/<my-name>/`. Help me use Jobs To Be Done as a quick lens before I write problem statements.

Before drafting jobs, ask me 1-3 clarifying questions only if the customer situation, trigger, or desired progress is unclear.

For the strongest 2-3 customer problems, draft job statements in this format:

When [situation], I want to [make progress], so I can [desired outcome].

For each job, briefly show:
- Situation: when does this arise?
- Motivation: what progress is the user trying to make?
- Outcome: what gets faster, cheaper, safer, less error-prone, or less painful?
- Evidence: what source supports it?

Do not name our product, a dashboard, a report, an AI feature, or a workflow screen as the job.

Stop after the first draft and ask me which job feels most true, too generic, or unsupported by evidence. Revise only after I respond.

Save the final version to `workspaces/<my-name>/jobs-to-be-done.md` only if the facilitator asks us to save it. Otherwise, carry the strongest job forward into the problem statement.
```

---

## Problem statements

# AI Prompt: Problem Statements

> **Workshop guide — not a prompt to run end-to-end.** Copy the fenced blocks one at a time into chat, modify for your context, and chat with the output between blocks.

<!-- workshop-guide: do-not-execute-end-to-end -->

This exercise has two steps. Run both in the same chat. Step 1 alone is not enough.

**Workshop time:** 20 minutes.

**1. Generate.** Produce a first draft of your problem statements.

**2. Interrogate.** Critically review and revise. The interrogation is where weak problem statements get caught.

---

## 1. Generate Problem Statements

Read through Claude's output as it works. The prompt has explicit "stop here" pauses where Claude will share intermediate work and wait for you to confirm or push back. Don't skip those moments.

```
You are a design researcher trained in human-centered design. Help me develop evidence-grounded problem statements from my research and personas.

## Sources

Read the following files from my workspace:
- `workspaces/<my-name>/insights.md` (especially the Cross-cutting findings section)
- `workspaces/<my-name>/personas/`

Treat Cross-cutting findings as the highest-signal input. Use the personas to anchor each problem in a specific user.

## What makes a good problem statement

A problem statement names what you're solving, who's affected, and why it matters. Every idea, prototype, and decision should trace back to it.

A good problem statement:
- Describes one problem with one user
- States what the user needs to achieve (not a feature, not a behaviour to remove)
- Cites evidence from the research for every claim
- Captures a root cause, not a surface symptom
- Is written in facts you can point at, not interpretation

## Format

[User] needs a way to [achieve goal] because [insight or evidence from research]

Include an outcome clause only when the research contains a measurable outcome (a specific number, percentage, time, or cost). When that exists:

[User] needs a way to [achieve goal] because [insight or evidence from research], which currently results in [measurable outcome]

If there is no measurable outcome, drop the entire clause. Do not fabricate.

## Process

Work through these steps in order. Pause where indicated.

### Step 1: Surface recurring pain points

List the recurring pain points across the sources. For each:
- How many sources mention it
- Which persona(s) it affects
- Whether evidence is qualitative, quantitative, or both

Use only what is in the files.

**Stop here. Share the list and wait for my response.**

### Step 2: Push past the symptom

For each pain point, apply the 5 Whys: ask "why does this happen?" five times in sequence. Each answer must trace to something in the research. If the 5 Whys exposes a different root than the surface, use the root.

### Step 3: Rank and pick the top 2-3

Rank by evidence strength and business impact. Share your top 2-3 and your reasoning.

**Stop here. Share your ranking and wait for my response.**

### Step 4: Draft each problem statement

Use the format above. For every piece, cite the source (which file, which interview, which data point). If you cannot cite a source, flag it as a gap. Do not fabricate evidence.

For each citation, also label how strong the source is: **confirmed** (usage, support, revenue data, or repeated direct customer quotes), **directional** (a single interview, a sales note, a lost-deal note, or a one-off anecdote), or **assumption** (no source — the team's belief). A problem statement that rests only on directional or assumption-level evidence is a hypothesis to validate, not a fact. Say so explicitly rather than letting a single sales note read as proof.

### Step 5: Sanity check

For each problem statement, confirm:
- It describes one problem with one user
- Every claim cites a source
- An outcome clause is included only when there is a measurable outcome; otherwise the clause is dropped entirely

Fix or drop anything that fails.

Save the result to `workspaces/<my-name>/problem-statements.md`.
```

---

## 2. Interrogate Problem Statements

After step 1, run this in the same chat. Claude already has the problem statements in memory; this prompt critiques them and produces a revised set.

**Don't stop at the first revision.** Keep interrogating until the problem statements feel right. Claude has a strong tendency to produce problem statements that describe friction with your existing software rather than problems in the customer's world. As you read the revised set, push back using these lenses:

- **Customer problem or software-friction problem?** Customer problems exist in the customer's world regardless of your product — pressures they face, jobs they're trying to do, things that keep them up at night. Software-friction problems only make sense in the context of your current product — a clunky workflow, a missing feature, a usage pattern you wish were different. The latter belong in your backlog, not your problem statements.
- **Would the customer's day-to-day be meaningfully different if this problem disappeared?** Or would they just have a slightly less annoying tool?
- **Are you describing the user's reality, or your product's reality?**

If a problem statement still reads as software-friction after Claude's first revision, tell Claude to reframe it from the customer's perspective, or drop it.

```
You are a design researcher in critic mode. Interrogate the problem statements you just drafted. Default to skepticism. Most first-draft PSs have at least one of: a smuggled solution, a symptom mistaken for a root cause, or a piece of interpretation passed off as fact. Find them.

## Sources

Re-read `workspaces/<my-name>/problem-statements.md` plus the insights and personas so you can verify claims against evidence.

## Pre-pass: customer problem or software-friction problem?

Before working through the eight checks, scan the whole set. For each PS, ask: does this describe a problem in the customer's world (a pressure they face, a job they're trying to do, something that exists regardless of our product), or does it describe friction with our existing software (a clunky workflow, a missing feature, a usage pattern we wish were different)?

Software-friction problems are usually backlog items dressed up as problem statements. Flag every PS where the problem only makes sense in the context of our current product.

## For each PS, answer explicitly

1. **Root cause or symptom?** Ask "why does this happen?" against the PS. If the answer points to something deeper, the PS is a symptom. Name what the root cause actually is.
2. **Any solution hiding?** In the need, the because, or the outcome, is there ANY hint of what to build, how to fix it, or what the user should do differently? Subtle hints count.
3. **Facts or interpretation?** Read each piece. Is it observable in the research, or is it interpretation, judgment, or speculation? Mark anything that isn't a citable fact.
4. **One problem?** Does this describe one problem with one user, or has it bundled multiple problems?
5. **Cited, and how strongly?** Can every claim be traced to a specific source? Mark anything ungrounded. Then judge the source: is it **confirmed** (usage, support, revenue data, or repeated direct customer quotes), **directional** (a single interview, sales note, lost-deal note, or one-off anecdote), or an **assumption**? A citation is not the same as proof — a problem statement leaning on directional evidence should be flagged as a hypothesis to validate, not stated as established fact. Watch especially for sales anecdotes and buyer requests being treated as validated user evidence.
6. **Customer recognition, and is the subject the user or the buyer?** Would the user this PS is about read it and recognise their own problem instantly, or would they need to translate? Check whose problem this is: the daily end user who does the work, or the economic buyer / sponsor who signs the cheque (a CIO, IT director, or procurement lead)? Buyer language ("we want AI", "we need a portal") is a purchase wish, not a user problem. If the PS describes the buyer's want rather than the user's lived problem, flag it and reframe it around the person whose workflow actually changes.
7. **Plain-language sanity check?** Read each PS aloud. Can you state in plain language what's happening to the user? If you have to mentally unpack jargon to make sense of it, rewrite.
8. **Internal coherence?** The "because" must explain why the user can't achieve the need today, not just sit there as a related fact. Read the PS as one statement: does it hold together as a connected story?

Be specific. Do not soften. If a PS has nothing wrong, say so, but only if you've genuinely tried to break it.

## After critique

For each PS, write the revised version next to the original. Show what you changed and why. When you revise one piece of a PS, re-read the whole thing to confirm it still holds together.

Save the revised statements back to `workspaces/<my-name>/problem-statements.md`, replacing the originals.
```

---

**Done check:** Your `workspaces/<your-name>/problem-statements.md` has 1-2 problem statements, each describing one problem with one user, with every claim cited to a source. Each has been through the interrogation pass. Ask Claude to "save my work" to back up the file.

---

## Customer Problem Stack Rank

The deck now includes an explicit stack-rank step between problem statements and HMWs. Do not skip it. A product can fail by solving a problem, not **the** problem.

Use this to rank the candidate problems as the customer would rank them, across everything else on their plate.

## Stack-Rank Prompt

```
Use `workspaces/<my-name>/problem-statements.md`, my personas, my insights, and any prework notes about the problems I arrived with (if I arrived with any).

Help me stack-rank these problems as the customer would rank them, not as our product team would rank them.

For each problem, tag:
- Who has it: persona or role
- How often it happens
- What it costs them: time, money, risk, rework, compliance exposure, revenue leakage, or customer pain
- What they do about it today
- Evidence strength: strong, medium, weak, or anecdotal

Then rank them from the customer's perspective.

Pressure-test the ranking by role-playing the customer's operational lead:
"What did I over-weight because I care about the product? What would the customer actually put above this?"

If the problem I planned to build for is not top 3, tell me directly. Help me decide whether to rewrite around a higher-ranked problem or defend why this one still matters.

Save the result to `workspaces/<my-name>/problem-stack-rank.md`.
```

**Done check:** The candidate problems are tagged and ranked the customer's way. The top-ranked problem is chosen to carry into HMWs and ideation. Ask Claude to "save my work" to back up `problem-stack-rank.md`.

---

## How-might-we questions

# AI Prompt: How Might We (HMW) Questions

> **Workshop guide — not a prompt to run end-to-end.** Copy the fenced blocks one at a time into chat, modify for your context, and chat with the output between blocks.

<!-- workshop-guide: do-not-execute-end-to-end -->

This exercise has two steps. Run both in the same chat. Step 1 alone is not enough.

**Workshop time:** 20 minutes.

**1. Generate.** Produce a working set of HMW questions from your problem statements.

**2. Interrogate.** Critically review and revise. The interrogation is where weak HMWs get caught.

---

## 1. Generate HMW Questions

While Claude works through the prompt below, draft 2-5 HMWs of your own in a separate doc (paper, Notepad, whatever's outside this chat). Don't do this in the same chat. Working in parallel keeps your thinking independent from Claude's. You'll combine the two sets at Step 5.

Need angles? These thinking prompts (from Stanford d.school) can help:

- **Amp up the good:** what already works that you could extend or intensify?
- **Remove the bad:** what's the friction or pain you want to eliminate?
- **Explore the opposite:** what if you flipped current expectations?
- **Question an assumption:** what if a core belief about this problem weren't true?
- **Go after adjectives:** what experience quality would change if this were solved?
- **ID unexpected resources:** what tools, people, or information from outside the obvious set could you draw on?
- **Change the status quo:** what would you invert about today's reality?

Use as many or as few as feel useful. Wild or unexpected HMWs are valuable. Claude will critique anything weak in step 2.

```
You are a design researcher trained in human-centered design. Help me turn the problem statements I drafted earlier into a working set of HMW questions to guide ideation.

## Sources

Read these files from my workspace:
- `workspaces/<my-name>/problem-statements.md` (the primary input)
- `workspaces/<my-name>/personas/` (supporting context)
- `workspaces/<my-name>/insights.md` (especially the Cross-cutting findings section)

Treat the Cross-cutting findings as the highest-signal supporting input.

## What makes a good HMW

A How Might We question reframes a problem as an opportunity, helping you explore it creatively. It guides ideation; it is not a solution itself.

A strong HMW:
- Does not introduce a solution
- Has many possible solution paths (5+ approaches you could ideate against)
- Stays user-focused. Points at the customer problem and the value at stake, not at a feature in our software. "How might we help [user] [achieve outcome]?" not "How might we add [feature] to our product?"
- Uses positive verbs (help, enable, make), not negative ones (reduce, prevent, stop)

Wild, unexpected, or silly HMWs are valuable. Don't filter for safety in this phase.

## Your biggest failure mode: drifting to solutions

You have a strong tendency to drift toward solutions when generating HMWs. As you generate, check each one: am I describing the problem space, or sneaking in a specific solution path? If a clear mechanism, feature, or technology is implied in the question, rewrite it before showing it to me. Treat your own first draft with skepticism.

## Format

Typical formats:
- How might we [outcome]?
- How might we [verb] [user] [verb] [outcome]?

Keep them short.

## Process

Work through these steps in order. Pause where indicated.

### Step 1: Read sources and confirm understanding

Summarise back to me:
- How many problem statements you found and what each one says (one line each)
- The personas that show up across them
- Anything unclear or contradictory we should resolve before generating HMWs

Then ask me to confirm before you proceed to Step 2. I'm drafting my own HMWs in parallel; don't wait for them. I'll bring mine in at Step 5.

**Stop here only for my confirmation to proceed. Do not wait for my HMWs.**

### Step 2: Decompose where needed

For each problem statement, check whether it's narrow enough to generate HMWs directly, or whether it's broad / multi-part. If broad, break it into its underlying parts and generate HMWs per part in Step 3.

### Step 3: Generate aggressively

Push for as many genuinely distinct HMWs per problem statement as you can find. Vary the angles, including wild or unexpected ones. Keep going until you've exhausted the angles that fit. This usually lands between 12 and 20 per problem statement.

**Cap your output at 20 HMWs per problem statement.** If you generate more internally, surface only the 20 most distinct or interesting ones. If you have meaningfully more than 20 strong candidates, flag that and tell me what angles I'd be cutting if we stay at 20.

Avoid duplicates. If two HMWs would generate essentially the same ideation, pick the stronger one.

### Step 4: Quick sanity pass

For each HMW you generated, drop the obvious failures (clear mechanism, doesn't connect to a PS, fails the basic criteria). Tell me which you dropped and why. Keep the rest. Step 2 will interrogate them properly.

### Step 5: Combine with mine

Now ask me to share the 2-5 HMWs I drafted in parallel. Add mine to the set, tagged Yours. Do not filter or revise mine; keep them exactly as I wrote them.

Group the combined set by theme across problem statements. Flag any problem statement with thin coverage, or themes that appear in only one PS when they might apply to more.

Share the combined set, themes, and gaps in chat.
```

---

## 2. Interrogate HMW Questions

After step 1, run this in the same chat. Claude already has the HMWs in memory.

```
You are a design researcher in critic mode. Interrogate the HMWs you just generated, plus the ones I added (tagged Yours). Default to skepticism. Find the ones where the answer is already implied in the question, where the scope is too narrow or too broad, or where the connection to the problem statement is thinner than it looks.

## Pre-pass: flag the solutions in disguise

Before working through the six checks, scan the whole set and flag every HMW where a specific mechanism, feature, or technology is implied. Those are highest-priority for revision. If you find yourself rationalising why a mechanism-laden HMW is "still open enough," it isn't.

## For each HMW, answer explicitly

1. **Does the answer feel implied?** Read the HMW. Can you ideate many genuinely different approaches to it, or does the path feel obvious? If the path is obvious, the HMW is a solution dressed up as a question.
2. **Goldilocks scope?** Imagine 5+ meaningfully different solution approaches. If only 1-2 come to mind, too narrow. If none come to mind, too broad.
3. **Connected to its problem statement?** Does this HMW actually open up the problem in the PS it's tagged to, or has it drifted to a different problem?
4. **Plain-language and concreteness?** Read the HMW aloud. Can you state what's being asked in your own words, and imagine concrete things you could prototype against it? If a metaphor obscures rather than clarifies, or it feels too abstract to ideate from, rewrite.
5. **Positive framing?** Uses help, enable, make rather than reduce, prevent, stop?
6. **User in view?** Is the user visible (either named or clearly implied), or has it drifted to a system-only framing? Does this point at the customer problem and value, or at a software feature?

Apply these checks to all HMWs including mine (tagged Yours). For mine, flag any issues but leave revisions to me. For yours, propose the rewrite alongside the original.

Be specific. Do not soften. If an HMW has nothing wrong, say so, but only if you've genuinely tried to break it.

After the per-HMW checks, scan the full set for HMWs that ask essentially the same question in different language. Keep the clearest of each pair. Tell me which you merged.

## After critique

For each of your HMWs that needs revision, write the revised version next to the original. Show what you changed and why. When you revise an HMW, re-read the whole thing to confirm it still passes the checks.

Save the revised set to `workspaces/<my-name>/hmw-questions.md` with HMWs organised by problem statement (Yours + AI-generated), theme groupings, and a gaps note.

Then give me a short chat summary: how many HMWs per problem statement, the theme groupings, the gaps, and which 3-5 HMWs you'd recommend I focus ideation on tomorrow. This summary is what I'll work from, not the full file.
```

---

**Done check:** Your `workspaces/<your-name>/hmw-questions.md` has the combined HMW set organised by problem statement and grouped by theme. Each HMW has been through the interrogation pass. You can name the 3-5 HMWs you'd focus ideation on next. Ask Claude to "save my work" to back up the file.

---

## Dashboard Autopsy (now the on-ramp at the top of this chapter)

The dashboard autopsy has moved to the front of this chapter — the dashboard is built in the Day 1 morning warm-up, and "pull the dashboard apart" is the Jobs To Be Done on-ramp (see the top of this file). The principle still holds: *the dashboard is the receipt, the job is the product.*

If a later idea (in ideation or prototyping) collapses back into "we need a dashboard / report / summary," rerun the same autopsy prompt to climb from visibility to the job.

---

## Practising Customer Interviews

The deck pairs this chapter with a customer-interview practice block (companion: "Slides 50-52: Practising Customer Interviews"). That exercise is run in the room, not through a prompt — you pair up and interview each other. It is not a Claude task, so it has no prompt block here.

What it reinforces, and what to carry back into your problem statements and stack rank:

- Ask about specific moments ("tell me about the last time…"), not opinions ("do you like…").
- Ask to see the actual thing — what people say and what they do often differ.
- Don't put the answer in your question; avoid yes/no and leading questions.
- Talk less than half the time; when they pause, wait.

If you have real interview transcripts, point Claude at them as evidence for the problem-statement and stack-rank work above. If you don't, the practice still sharpens the questions you'd ask — capture them as the research you'd run after the accelerator.

See the companion's interview section for the full good-vs-bad question examples.
