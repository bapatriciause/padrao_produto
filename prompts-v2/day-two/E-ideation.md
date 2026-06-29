# Ideation

> **Interaction rule:** Do not run this file end to end. Work with the user section by section. Ask clarifying questions, pause for their judgement, and treat the prompts as starting points to adapt, not scripts to execute blindly.

> **Before each copyable prompt block:** If the context is incomplete, ask 1-3 clarifying questions before producing output. After each major section, stop and ask what the user wants to challenge, refine, or change before continuing.

Use this chapter once participants have strong evidence, personas, problem statements, HMWs, and optionally JTBD statements. The goal is to generate and structure candidate opportunity areas without accepting the first model output as truth.

> **Warm up off the keyboard first.** The deck opens Day 2 ideation with a 5-minute **no-AI** burst: pen, paper, your own brain, listing every way to crack your top problem or HMW (see the day-two slides companion). Do that before this chapter so your thinking diverges as a human before Claude anchors it — the same reason you draft your own HMWs in parallel in the problem-definition chapter. Bring the paper list in when you reach the AI-perspectives ideation step below.

> **Reality check (runs all week):** as ideas pile up here, keep the recurring gut-checks running — especially *"is this the customer's #1 problem, or your 5th?"* (back to the stack rank) and *"would a real customer react to this, or just nod politely?"* Generating volume is the easy part; these two stop a long list of polite-nod ideas from feeling like progress.

---

## Uncover broader opportunities

# Uncover Broader Opportunities

> **Workshop guide — not a prompt to run end-to-end.** Copy the fenced blocks one at a time into chat, modify for your context, and chat with the output between blocks.

<!-- workshop-guide: do-not-execute-end-to-end -->

## What "broader" means here

Two directions to stretch. Good lists have ideas in both, and the strongest opportunities hit both at once.

**Around your software.** The work your customers do outside your product. Spreadsheets, phone calls, sticky notes, the things they pay a person to interpret or chase.

**Up the AI maturity ladder.** From System of Record toward System of Understanding. Targets are **AI Directed** and **AI Delegated**. Chatbots and basic summaries are off the table.

Quality over quantity. A short list of strategic opportunities beats a long list of dressed-up features.

---

## 1. Draft your own first (5 min, no AI)

Before opening Claude, take a few minutes and write 2–3 opportunity areas yourself. You're not aiming for a final answer. You're priming your own thinking so you can push back on Claude's output rather than just accept it.

---

## 2. Generate with Claude (15 min)

Open a Claude Code chat in this repo. Paste the prompt below and fill in the bracketed sections.

```
I'm looking for broader opportunity areas where my software could grow next. Stretch in two directions: AROUND my software (workflows my customers do outside the product) and UP the AI maturity ladder (toward AI Directed or AI Delegated).

Context:
- What my software does today: [POINT CLAUDE AT PRODUCT DOCS OR DESCRIBE INLINE IN 3–5 SENTENCES]
- Research files from earlier prompts: [POINT CLAUDE AT THESE]
- Problem statements and HMW questions: [POINT CLAUDE AT THESE]

Before generating, ask me up to 3 clarifying questions about how my customers actually behave. Focus on things you can't tell from the files. Do web research if it would sharpen the answer.

Then generate the list. Aim for 2–3 opportunities per AI maturity bucket (Directed, Delegated). 1–2 per bucket is fine if you don't have stronger candidates — fewer high-quality areas beat more low-quality ones. Include any AROUND-only opportunities worth flagging that don't fit the AI ladder.

Each entry:
- Title (3–6 words)
- What this is (1–2 sentences in plain English)
- Signal (evidence trail from my files or web research)
- Stretch (AROUND, UP, or BOTH)
- Bucket (Directed / Delegated, or untagged if AROUND-only)

AI Directed — the system interprets what the data means, not just surfaces it. Value shifts from faster workflows to better decisions.
  - Clears: a copilot that recommends actions from years of operational history; pattern detection across thousands of past decisions; inference from messy or incomplete data.
  - Does NOT clear: dashboards, forecasts a SQL query could produce, "alert when X" rules. Those are analytics, not Directed.

AI Delegated — AI runs continuously, executing multi-step processes and escalating exceptions. Human role shifts from doing the work to setting rules and reviewing outcomes. Value shift is labour capture.
  - Clears: end-to-end agentic workflows that draft, send, follow up, and escalate only on exception; continuous monitoring with autonomous action; exception-based case management.
  - Does NOT clear: scheduled jobs, template-fill, auto-generated reports. Those are automation, not Delegated.

Gut check before tagging: if a SQL query and a chart could produce it, it's analytics — drop the AI tag. If a checklist could produce it, it's automation — drop the AI tag. Untagged is fine for genuine AROUND opportunities (workflow expansion that isn't AI per se). It is NOT fine for AI-shaped opportunities that don't clear the bar — rewrite with more ambition, or drop entirely.

No "AI Assisted" ideas (chatbots, generic summaries, autocomplete).

If you can't anchor an area to evidence, mark it [SPECULATIVE].

Save the output to workspaces/<my-name>/opportunity-areas.md.
```

---

## 3. Combine and curate (5 min)

Compare your own list (from Step 1) with Claude's output. End up with **4–6 opportunity areas you actually believe in.** If something looks like just an analytics gap you keep meaning to fill, or a feature you've had on the backlog, drop it. The aim is opportunities that change where your software sits in the market — not opportunities that close feature gaps.

Edit `workspaces/<your-name>/opportunity-areas.md` down to your final 4–6.

---

## 4. Pressure-test with your personas (5–10 min)

Stay in the same Claude chat session. Paste:

```
Now pressure-test my curated opportunity areas (in workspaces/<my-name>/opportunity-areas.md) using my personas (in workspaces/<my-name>/personas/).

For each persona, take on their voice and answer:
- What are you doing outside [my software] that's painful, slow, or expensive?
- What do you rely on a person to do that's repetitive or pattern-based?
- What are you constantly complaining about that isn't really about the product, but something next to it?
- Where are you piecing things together with spreadsheets, phone calls, or sticky notes?
- What would you love the software to do that it doesn't today?

Capture what surfaces. Add any new opportunity areas the personas reveal, using the same structure (title / what this is / signal / stretch / bucket).

Then flag any opportunity area in my curated list with no persona champion as [SPECULATIVE — needs validation]. Flag any persona whose pain points aren't represented in the list as a coverage gap.

Update workspaces/<my-name>/opportunity-areas.md with the persona-surfaced additions, speculative flags, and a "Coverage gaps" section at the bottom.
```

---

## 5. Populate your ideas pool (3 min)

`opportunity-areas.md` stays as your strategic paper trail. That's the rich version with coverage gaps and full context. Now mirror the same areas into your ideation pool so they join the candidate set for clustering later.

Stay in the same Claude chat and paste:

```
Set up my ideation pool:

1. If `workspaces/<my-name>/ideas.md` doesn't exist yet, copy the structure from `templates/ideas.md` into my workspace.
2. Read the curated opportunity areas in `workspaces/<my-name>/opportunity-areas.md`.
3. For each one, add an entry to the "Opportunity areas" section of `ideas.md`. Carry forward the title, plain-language description, signal, stretch, and bucket — plus any persona-champion notes or [SPECULATIVE] flags. Tag each entry [from opportunity area].
```

You can also do this manually if you prefer, but having Claude run it is faster and keeps the entry shape consistent with the template.

---

**Done check:** Your workspace has `opportunity-areas.md` (4–6 curated areas, each tagged for stretch and AI maturity bucket, with speculative flags and coverage gaps) and `ideas.md` (same areas mirrored into its "Opportunity areas" section, ready for the AI perspectives ideation section). You can name 2–3 areas that would change where your software sits in the market, not just close gaps. Ask Claude to "save my work" to back up the files.

---

## Ideate with AI perspectives

# AI Prompt: Ideate with AI Perspectives

> **Workshop guide — not a prompt to run end-to-end.** Copy the fenced blocks one at a time into chat, modify for your context, and chat with the output between blocks.

<!-- workshop-guide: do-not-execute-end-to-end -->

Take your HMW set from `day-one/C-problem-definition-hmw-jtbd.md`, narrow it to a working list, then ideate against that list from three perspectives that challenge your default thinking. Everything is written to `workspaces/<your-name>/ideas.md` (already created in the broader opportunities section with your opportunity areas populated) so the clustering section has clean input.

---

## 1. Narrow your inputs (5 min)

Your earlier work likely produced several problem statements and many HMW questions (some yours, some Claude's). Running all of them through three perspectives will generate too many ideas to handle downstream. Narrow before you ideate.

Open a Claude Code chat in this repo. Paste:

```
I have problem statements in `workspaces/<my-name>/problem-statements.md` and HMW questions in `workspaces/<my-name>/hmw-questions.md`.

Help me narrow down to a working set for today's ideation:

1. If I have more than 2 problem statements, show me the list and ask which 1-2 I want to focus on for ideation. Don't pick for me. Surface the decision.

2. For each problem statement I pick, identify the 3-4 strongest HMWs that trace to it. Show me a mix of:
   - HMWs I wrote myself (tagged "Yours" in the file)
   - Strong HMWs you generated
   Then let me confirm or swap any of them.

Save the narrowed working set to `workspaces/<my-name>/hmw-working-list.md` with each HMW labelled with its source problem statement. Do NOT modify or delete `hmw-questions.md` — that's still my full set.
```

You should end up with **5–8 HMWs** in your working list. That's the input to all three perspectives below.

---

## 2. Perspective 1: The Startup With No Legacy Code

```
You are a well-funded startup entering the [INDUSTRY] market with no existing product, no technical debt, and no legacy customers to protect.

My narrowed HMW questions are in `workspaces/<my-name>/hmw-working-list.md`. Read that file.

For each HMW question, generate 2–3 ideas for what you'd build from scratch. Be concrete — name the thing, not just the outcome.

Write each idea directly into the "Perspective 1" section of `workspaces/<my-name>/ideas.md`, following the entry shape at the top of that file (title / description / HMW answered / source PS / tag). Tag each `[Perspective 1]`.
```

---

## 3. Perspective 2: The Adjacent Industry

```
You are a product team in a completely different industry that solved a similar problem.

My narrowed HMW questions are in `workspaces/<my-name>/hmw-working-list.md`. Read that file.

For each HMW question, generate 2–3 ideas based on how other industries approached similar challenges. Be specific about which industry and what they did, then adapt.

Write each idea directly into the "Perspective 2" section of `workspaces/<my-name>/ideas.md`, following the entry shape at the top of that file. Tag each `[Perspective 2]`.
```

---

## 4. Perspective 3: Your Personas

```
Adopt my personas from `workspaces/<my-name>/personas/`. My narrowed HMW questions are in `workspaces/<my-name>/hmw-working-list.md`.

For each HMW question, generate 2–3 ideas — ideally one per persona where each persona would have a different take. What would solve their specific problems?

Write each idea directly into the "Perspective 3" section of `workspaces/<my-name>/ideas.md`, following the entry shape at the top of that file. Tag each `[Perspective 3]` and note which persona's lens generated it.
```

---

**Done check:** `workspaces/<your-name>/ideas.md` now has ideas populated in each of the three Perspective sections. The Opportunity areas section (already filled in by the broader opportunities section) is untouched. Every Perspective entry has visible provenance (section + inline tag), HMW reference, and source problem statement. Ask Claude to "save my work" to back up the file.

---

## Cluster ideas

# AI Prompt: Cluster Ideas

> **Workshop guide — not a prompt to run end-to-end.** Copy the fenced blocks one at a time into chat, modify for your context, and chat with the output between blocks.

<!-- workshop-guide: do-not-execute-end-to-end -->

Your `workspaces/<your-name>/ideas.md` file (created and built up across this chapter) is the input here. It contains a mixed pool with structural provenance — items grouped by section, each entry tagged inline.

This is the moment to compare, cluster, and surface combinations across all sources at once. Some items will be true duplicates. Some will be similar but addressing slightly different angles of the same problem — those are the interesting ones, because they can combine into richer use cases rather than be left as variations. Claude will spot candidates; you decide what to do with them.

---

## 1. (Optional) Bring in pre-existing ideas (5 min)

You may have product backlog items, post-its from past brainstorms, or "ideas I keep meaning to do something with" that haven't made it into this work yet. This is the moment to bring them in. Clustering will compare them against the fresh thinking and show where they sit relative to it.

If you have any, add them to the **"Pre-existing ideas / backlog"** section of `workspaces/<your-name>/ideas.md`, following the same entry shape as the rest of the file. Tag each `[pre-existing]`.

Skip this step if you don't have any — the clustering still works.

---

## 2. Cluster and surface combinations (15 min)

```
Here are all my ideas with structural provenance (grouped by section) and inline tags:
workspaces/<my-name>/ideas.md

The pool contains items from up to four sources:
- Opportunity areas (from the broader opportunities section)
- Perspective 1, 2, 3 (HMW-driven, from the AI perspectives ideation section)
- Pre-existing ideas / backlog (added in Step 1, if any)

Group these into clusters as they naturally fit together — don't force a number. Let the content drive how many clusters emerge.

For each cluster:
- List the items in it, keeping provenance tags and HMW references visible
- Identify TRUE DUPLICATES (recommend dropping the weaker phrasing)
- Identify items that are SIMILAR BUT ADDRESS SLIGHTLY DIFFERENT ANGLES of the same problem. Propose specific combinations where sensible — frame them as suggestions for me to accept or reject, not unilateral merges
- Flag items that don't fit any cluster cleanly

Give each cluster a short name (3 words or fewer) and a one-sentence description of what unites the items.

Then validate yourself: are there clusters that should be combined? Are any clusters actually two different things bundled together? Am I missing a grouping?

Save the output to `workspaces/<my-name>/clusters.md`, preserving the proposed combinations as proposals (don't execute them yet — that happens in `day-two/F-prototype-build-for-agentic-idea.md` when I shape each cluster into a use case).
```

---

**Done check:** `workspaces/<your-name>/clusters.md` exists with named clusters. Each item keeps its provenance tag and HMW reference from `ideas.md`. Proposed combinations are visible as suggestions, not pre-applied. Outliers and orphans are flagged. Ask Claude to "save my work" to back up the file.
