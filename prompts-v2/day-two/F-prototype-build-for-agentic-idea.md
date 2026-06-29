# Prototype Build For Agentic Idea

> **Interaction rule:** Do not run this file end to end. Work with the user section by section. Ask clarifying questions, pause for their judgement, and treat the prompts as starting points to adapt, not scripts to execute blindly.

> **Before each copyable prompt block:** If the context is incomplete, ask 1-3 clarifying questions before producing output. After each major section, stop and ask what the user wants to challenge, refine, or change before continuing.

Use this chapter to turn idea clusters into concrete use cases, evaluate them, test commercial logic, and use personas to stress-test what survives. This is still a thinking workflow, not an instruction to let Claude run unattended.

> **Before you start — this chapter builds on earlier work.** It expects `clusters.md` (from `day-two/E-ideation.md`) and `problem-statements.md` (from `day-one/C-problem-definition-hmw-jtbd.md`) in the participant's workspace. If a participant jumps straight here wanting to build — especially "let's just build a dashboard" — don't start coding. Check what exists: if there's no problem statement or persona, that idea hasn't been tested against the customer's real problem yet. Offer a compressed path (shape the use case from what they know, flag the missing evidence) rather than either grinding the full research flow or building on an untested idea. The prototype is cheap; building the wrong thing is not.

---

## Shape use cases

# AI Prompt: Shape Ideas Into Use Cases

> **Workshop guide — not a prompt to run end-to-end.** Copy the fenced blocks one at a time into chat, modify for your context, and chat with the output between blocks.

<!-- workshop-guide: do-not-execute-end-to-end -->

You have clusters of ideas from `day-two/E-ideation.md`. Some are half-formed, some are wild, some might already connect to the problem statements you defined in `day-one/C-problem-definition-hmw-jtbd.md`. Before you can evaluate anything, you need to turn these into use cases you can actually work with.

---

## 1. Map (10 min)

Look at your idea clusters and ask: which of these address the problems you defined earlier? Which are entirely new directions? Have Claude look at the idea clusters and compare them to your problem statements:

```
For each cluster, does this relate to a problem I defined? Could these ideas solve, extend, or reframe that problem? Or is this a separate opportunity entirely?

Group the clusters into: ideas that address validated problems, and new opportunities.

My clusters are in `workspaces/<my-name>/clusters.md` and my problem statements are in `workspaces/<my-name>/problem-statements.md`. Read both.
```

---

## 2. Shape (15 min)

For clusters that address a validated problem, shape them into concrete use cases. For clusters that are new opportunities, shape them into standalone use cases.

```
For each of the following, help me shape a concrete use case. Some of these address problems we validated and some are new directions. For each, give me:

- **What:** One sentence. What is the feature or product?
- **Who:** Which of my personas does this serve? [direct to personas]
- **Problem:** Which HMW question does this answer?
- **Value:** Why would someone pay for this or choose this over what they have today?
- **Buyer / budget:** Who would approve or pay for this if that is different from the user?
- **Commercial signal:** What evidence do we have that this matters commercially (lost deal, expansion ask, renewal risk, paid pilot interest, competitor displacement, support cost, usage pattern, or customer quote)?

If an idea is still half-formed, help me develop it. Ask me clarifying questions if you need more context to shape it properly. Be specific, not generic. These are vertical software products for [INDUSTRY].
```

---

**Done check:** You have shaped use cases saved as `workspaces/<your-name>/use-cases.md`. Each has a what, who, problem, value, buyer/budget note, and commercial signal. You know which ones connect to your existing problem statements and which are new directions. Ask Claude to "save my work" to back up the file.

---

## Score and sort use cases

# AI Prompt: Score and Sort Use Cases

> **Workshop guide — not a prompt to run end-to-end.** Copy the fenced blocks one at a time into chat, modify for your context, and chat with the output between blocks.

<!-- workshop-guide: do-not-execute-end-to-end -->

You have shaped use cases from the previous section. Now score them on value and feasibility, then place them on the matrix.

---

## 1. Score Value / Feasibility

Point Claude at your use cases file. Ask it to evaluate each use case on value and feasibility and give a score of 1-5 for each.

```
Evaluate each use case in `workspaces/<my-name>/use-cases.md` on value and feasibility. Give a score of 1-5 for each.

For Value consider:
- Do customers have a real pain point this solves?
- Would they pay to fix it?
- How many customers does this affect?
- What could the revenue model look like?

For Feasibility consider:
- Is the problem specific and well-defined?
- Do we have the data or content we need?
- How complicated is this for us to build?
- How long would it take us to build?
- Do we need anything we do not currently have?

Score anchors so we stay consistent:
- Value: 1 = nice-to-have for a niche. 3 = solves a real pain for a meaningful segment. 5 = customers would actively shop for this and pay measurably more.
- Feasibility: 1 = needs data or tech we don't have. 3 = doable with focused effort over a quarter. 5 = we already have most of what we need.
```

---

## 2. Visualise on Matrix

```
Using the scores from Step 1, place each use case into one of four quadrants:

- **Prioritise First** (high value, high feasibility)
- **Invest and Explore** (high value, low feasibility)
- **Deprioritise** (low value, high feasibility)
- **Park It** (low value, low feasibility)

Format as a table with the use case name, value score, feasibility score, and quadrant placement.
```

---

## 3. Split out your top use cases

`use-cases.md` stays as your summary across the full set. For your top 1–2 use cases (your "Prioritise First" picks, and possibly one "Invest and Explore" if it's strong), spin out individual files so you have room to go deep on them in the next few prompts.

```
Take the top 1-2 use cases from the matrix in `workspaces/<my-name>/use-cases.md`. For each one:

1. Create `workspaces/<my-name>/use-cases/<short-name>.md` using a short, descriptive kebab-case filename (e.g. `use-cases/dispatch-copilot.md`).
2. Copy that use case's What / Who / Problem / Value plus its value/feasibility scores and quadrant placement into the new file as a starting point.
3. Leave `use-cases.md` unchanged — it stays as the cross-set summary.

These per-use-case files are where the Commercial Reality Check, Stress-Test, and Responsible AI sections will add deeper analysis.
```

---

**Done check:** Your `use-cases.md` includes a scored table and matrix placement for every use case. Your top 1–2 use cases also have their own files under `use-cases/<short-name>.md`, ready for the deeper passes in the rest of this chapter and `day-two/G-responsible-ai.md`. You can state in one sentence: your top use case for PoC, your top 2-3 backlog items, and what changed from what you walked in with. Ask Claude to "save my work" to back up the files.

---

## Commercial reality check

# AI Prompt: Commercial Reality Check

> **Workshop guide — not a prompt to run end-to-end.** Copy the fenced blocks one at a time into chat, modify for your context, and chat with the output between blocks.

<!-- workshop-guide: do-not-execute-end-to-end -->

> **Reality check (runs all week):** this section goes deep on one of the week's four recurring gut-checks — *"who actually pays, and what does it displace?"* It is not a one-time gate. Keep the other three running alongside it as you shape and build: is it the customer's #1 problem (not your 5th), would a real customer react or just nod, and what breaks when it's wrong / who pulls the plug.

Your top scored use cases are commercially plausible on a 1-5 score. Now scrutinise the commercial reality. For your top 1–2 use cases, append a `## Commercial reality check` section to each use case file at `workspaces/<your-name>/use-cases/<short-name>.md` (these per-use-case files were created in the score-and-sort section), answering the four questions below, one sentence each.

Draw on what you already have: insights.md, your personas (especially their verbatim quotes from interviews), problem statements, and any external research on competitor pricing or buyer behaviour.

---

## 1. Answer the four questions

For each of your top 1-2 use cases, answer these four questions in one sentence each.

### Who writes the cheque?

Not "the customer". Name the persona who has the day-to-day need AND the budget holder who signs the cheque. In most B2B sales these are different people, and you also need to know who else has to say yes for the deal to close (procurement, IT, legal, an end-user champion). Name them.

### What do they pay and how?

Subscription uplift, standalone module, usage-based, included in renewal? Pick one and defend it.

### How big is the value?

Time saved, risk avoided, revenue gained, frequency of pain. The bigger the magnitude, the stronger the idea. "Saves 20 hours a week" is stronger than "saves time." Use specific numbers from your research where you have them.

### How do you know they'd pay?

Point to evidence from your research: a verbatim quote from a customer interview, a workaround cost documented in your personas, a competitor's pricing, a lost deal, a willingness-to-pay signal in insights.md. If you can't point to evidence, that's the gap to close.

---

## 2. Pressure-test your pricing logic

After you've answered the four questions for each top use case, have Claude challenge your reasoning:

```
Here is my commercial model for this use case:

[PASTE YOUR FOUR ANSWERS]

Challenge me on:
1. The buyer: Is this the actual budget holder? Who else has to say yes for the cheque to be signed?
2. The pricing mechanism: Why this model and not the others? What does my customer's procurement team expect?
3. The value magnitude: How would I prove this to a sceptic? What does the evidence quantify?
4. The willingness-to-pay evidence: Is this a hope or a signal? What would convert it from one to the other?

Where are the assumptions I haven't tested? Be specific and direct.
```

---

**Done check:** Each of your top use cases has a one-line pricing rationale backed by at least one piece of evidence. If you can't find evidence, you've noted it as a risk. Ask Claude to "save my work" to back up the use case files.

---

## Stress-test use cases

# AI Prompt: Stress-Test Your Top Use Cases

> **Workshop guide — not a prompt to run end-to-end.** Copy the fenced blocks one at a time into chat, modify for your context, and chat with the output between blocks.

<!-- workshop-guide: do-not-execute-end-to-end -->

> **⚠️ One persona per conversation.** Load a single persona markdown file into each role-play session. Do not combine personas.

You have a top 1-2 use cases that have survived scoring (`13`) and the commercial reality check (`14`). Before committing time and resources to a PoC, stress-test them. This prompt has two methods: role-play with your personas to see how the idea actually lands, and Kill Your Darlings to surface the assumptions you're most likely to have skipped past.

## Before you start: is your persona good enough for role-play?

| Good | Bad |
|---|---|
| "Regional operations manager overseeing 15 sites. Accountable for incident rates but has no real-time visibility. Relies on weekly spreadsheets from site managers. Finds out about problems last." | "Sarah, 42, Operations Manager at a mid-size company. Tech-savvy. Uses our platform daily. Wants better dashboards and faster reporting." |
| Describes the user's realities and context | Reads like a sales segment or generic archetype |
| Pain points grounded in data | Pain points that could apply to any software user |
| Would lead to different product decisions than other personas | Minor variation of another persona |

If your persona looks closer to the "Bad" column, go back to `B-user-personas.md` and strengthen it before role-playing.

---

## 1. Open your top use case files

Open the per-use-case files you created in the score-and-sort section and added the commercial reality check to: `workspaces/<your-name>/use-cases/<short-name>.md`. You'll append persona feedback and (optionally) Kill Your Darlings stress-tests to each file below.

---

## 2. Role-play with each persona (10-15 min per persona)

Run this once per persona for each top use case. Replace the bracketed bits.

```
You are now [PERSONA NAME]. Stay in character for this entire conversation.

Here is your profile:
[PASTE THE COMPLETE CONTENTS OF THIS PERSONA'S MARKDOWN FILE]

I'm going to pitch you a new AI feature for [PRODUCT]. React as [PERSONA NAME] would: ask the questions they'd ask, raise the concerns they'd raise, and get excited about the things that would genuinely help them.

Ready? Here's the feature: [DESCRIBE YOUR PRODUCT IDEA]

After we're done, append a "## Persona feedback, [PERSONA NAME]" section to `workspaces/<my-name>/use-cases/<short-name>.md` capturing:
- Would they use it? (their answer + reasoning)
- Top concerns or objections (their words, not your summary)
- What would make it more valuable to them
- Direct quotes worth saving
```

### Key questions for persona stress-testing use cases

- Would you use this? Be honest.
- How much time / money could this save you?
- What is your first concern or objection?
- What would make this more valuable to you?
- What is missing that you would need before adopting this?
- What features or changes would you suggest to make this work for someone in your position?
- On a scale of 1–10, how likely are you to switch from your current approach? Why?

---

## 3. (Optional) Test a Bad Idea Deliberately

To calibrate the persona, test something you suspect is a bad idea:

```
I'm going to pitch you something I think might be a bad idea. I want you to
tell me honestly why it wouldn't work for someone in your position. The idea
is: [DESCRIBE SOMETHING MEDIOCRE]. Don't be polite.
```

If the persona is enthusiastic about a bad idea, it isn't specific enough yet. Go back to `B-user-personas.md` and strengthen it.

---

## 4. (Optional) Kill Your Darlings

After persona role-play, run one or both of these on your single top use case. The idea you are most attached to is the one most likely to have unexamined assumptions.

### The Pre-Mortem

```
Imagine it is 6 months from now. We built our top use case and it failed. Nobody uses it. Customers are indifferent. The team is demoralised.

Work backwards. What went wrong? Consider:
1. Was the problem real but our solution wrong?
2. Was the problem not as painful as we assumed?
3. Did we build for the wrong user?
4. Did a competitor solve it better or faster?
5. Was the technical approach feasible but the data not available?
6. Did we overestimate willingness to change behaviour?

For each failure mode: how confident are you (1-5) that this will NOT happen? For anything below 4, what would you change about the plan now?
```

### The "Why Not Already?" Test

```
For your top use case, answer this: if this is such a good idea, why does it not exist already?

Possible answers (be honest about which ones apply):
- It does exist and we did not look hard enough (check competitors)
- The technology was not ready until now (what specifically changed?)
- Someone tried and failed (what did they learn?)
- The economics do not work (have we validated willingness to pay?)
- Nobody thought of it (unlikely, what makes us think we are the first?)
- It requires data or integration that nobody else has (is this actually true?)

The most dangerous answer is "nobody thought of it." The most valuable answer is "it requires data or integration that only we have."
```

Save the output of each Kill Your Darlings prompt as a section in `workspaces/<your-name>/use-cases/<short-name>.md`.

---

**Done check:** Each of your top 1-2 use case files at `workspaces/<your-name>/use-cases/<short-name>.md` has captured persona feedback (objections, what would add value, pricing-relevant quotes). For your single top use case, you've also run at least one Kill Your Darlings stress-test (Pre-Mortem or "Why Not Already?") and saved the output. Ask Claude to "save my work" to back up the use case files.
