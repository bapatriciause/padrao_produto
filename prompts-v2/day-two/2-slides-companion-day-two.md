# Day 2 Slides Companion

Use this alongside the Day 2 v2 prompt chapters. It is not a full slide transcript. It keeps the exercise titles, key slide language, examples, done checks, and facilitator reminders that participants are likely to need while Claude Code is guiding them.

Source: the Palm Beach Product Track facilitation deck (Day 2).

This file is designed to be readable in plain markdown.

## How To Use This

Before starting an exercise, open the matching section here and the matching prompt chapter.

After Claude gives an output, ask:

- Is this specific enough to act on?
- Is it grounded in evidence?
- Does it avoid smuggling in a solution too early?
- Would this change a product decision?
- Can the team explain why this matters commercially?

Claude should not run an entire chapter at once. It should coach one exercise at a time, check whether the output is deep enough, and ask whether the participant is ready or the facilitator has moved the room on.

## Quick Navigation

- Day 2 Orientation
- Agentic Vocabulary
- Ideation
- Prototype Build For Agentic Idea
- Responsible AI
- PoC Build For Handoff

---
## Day 2 Orientation

**Related prompts:** `prompts-v2/day-two/E-ideation.md`, `prompts-v2/day-two/F-prototype-build-for-agentic-idea.md`, `prompts-v2/day-two/G-responsible-ai.md`

**Day 2 agenda:**

- Ideation and Refinement: use-case brainstorming
- Prototype build for agentic idea
- Responsible AI
- Refine initial PoC: vibe-code a PoC for handoff
- Wrap-up
- Daily Debrief

**Goals for today:**

- "We know what to build — and we can defend why."
- Ideate: an agentic use case from your research
- Prototype: a first working proof-of-concept
- Revisit: weigh it against the ideas you came in with
- Commit: push the agentic build, or refine another track

Key reminder:

- The prototype is disposable. The decision is not.

**Watch-outs for today** (now called out on the Day 2 goals slide):

- Push past your existing backlog and ideas.
- Keep the customer, the problem, the insights, and the value in focus.
- Do not build a dashboard by default.
- Your Day 1 prototype was a learning tool, not a commitment.
- Be ready to throw it away.

---

## Day 2 Warm-Up: Rapid Ideation (no AI)

**Related prompt:** `prompts-v2/day-two/E-ideation.md`

### Exercise: First Burst Of Ideas

**→ Prompt:** no-AI warm-up (pen & paper). Do it *before* `prompts-v2/day-two/E-ideation.md`; bring the paper list in at the AI-perspectives step.

**Time:** 5 mins (about 3 minutes of listing)

This one is deliberately **off the keyboard. No AI — pen, paper, your own brain.** Take your top problem or HMW and list every way you can think of to crack it, with no constraints. Diverging as a human first keeps your thinking from anchoring to Claude's before the AI ideation starts.

**Ground rules:**

- No AI — pen, paper, your own brain.
- Think big; wild ideas welcome.
- Quantity over quality.
- Unlimited budget, no barriers.

Example HMW to riff on:

```text
How might we help our users get the answers they need from their data without waiting for a report?
```

Go wild — answers that explain themselves out loud, a weekly podcast recap of the business, even "delivered by carrier pigeon." A daft idea on paper is fine; this is divergence, not judgement.

**Done check:**

- A list of ideas **on paper**, one per line. You bring these into Claude later, at the AI-perspectives step — don't save them to the repo yet.
- Do not filter or evaluate yet.

---

## Agentic Product Framing

**Related prompts:** `prompts-v2/day-two/E-ideation.md`, `prompts-v2/day-two/F-prototype-build-for-agentic-idea.md`, `prompts-v2/day-two/G-responsible-ai.md`

The Day 2 framing asks participants to park the ideas they arrived with and see the work through an agentic lens.

The shift — from system of record to system of understanding — and what each stage unlocks:

- From system of record → AI assisted → AI directed → AI delegated → AI domain intelligence → toward a system of understanding.
- Proprietary data begins building the next moat; deep expertise makes you irreplaceable; the software expands into the work above it.

Three opportunity anchors:

- Data advantage: proprietary data strengthens the core product.
- Services expansion: agentic workflows create new value around the product.
- Market advantage: deep vertical expertise makes the product harder to replace.

This is the same opportunity as Day 1's operating-spend model — the ~$6 of customer operating spend that sits above the $1 of system-of-record. The ladder is how you climb into that spend.

The deck uses LegacyCo (property-management software for operators of 50–500+ units; product "RentBase") to make the progression concrete:

- **System of record (today):** structured data — leases, maintenance, inspections, financials. Value = data integrity (a single source of truth) and operational efficiency.
- **AI directed:** copilots interpret tenant/property data to recommend actions. *Average example:* renewal term recommendations (review payment history, suggest adjustments). *Good example:* portfolio-aware rent optimization (per-unit adjustments, flag who to prioritise for renewal). RentBase does the interpretation work of experienced staff.
- **AI delegated:** agentic workflows act, with governance and audit trails. *Average example:* AI-drafted renewal offers, sent with manager approval. *Good example:* end-to-end renewal management — drafts, sends, follows up, escalates only on dispute. Impact: one leasing manager covers the renewal volume that used to take three.

### What Agentic Actually Means

Responsible AI means every step is visible.

Every agentic step must show:

- Multi-step behaviour
- Reasoning
- Explainability
- Traceability
- Human-in-the-loop

How an agent works in a product:

- Signal or trigger
- Reason
- Use a tool
- Check the result
- Act, with human approval where needed
- Repeat until the goal is met

**What is not agentic:**

- Invoice goes in, it scans it, data comes out: one step.
- A single model call dressed up with a nice UI.
- Waiting for a human to click "generate."
- Voice input or document parsing standing in for thinking.

**What is agentic:**

- Multi-step: uses tools and takes several actions to reach a goal.
- Reasons across the steps and shows its work.
- Always running, watching for an event a human would miss.
- Delivers the plan; it does not wait to be asked.

**The tell:**

- An agent is always on, catches the signal you would miss, and hands you the plan before anyone clicks a button.

---

### Agentic Vocabulary, Four Rungs

AP invoices, four ways:

- Enabler: AP aging dashboard. Makes the job visible. Does none of it. Sells nothing by itself.
- AI feature: OCR auto-code. Speeds up one step for an invoice you uploaded. Sells as an upsell.
- Product: AP module. Captures, codes, approves, and posts. Owns the system of record. Sells the module.
- Agentic product: inbox to posted. Reads the inbox, finds invoices, pulls, codes, routes, and leaves humans to handle exceptions. Sells the work itself.

**Test:**

- Turn it off. Does work pile up, or does a screen just go blank?

### Reality Checks

**Run these all week — not one session. Recurring gut-checks woven through every block, every concept, every day.**

- Who actually pays for this, and what does it displace?
- Is this the customer's number one problem, or the team's fifth? (Back to the stack rank.)
- Would a real customer react to this, or just nod politely?
- What breaks when it is wrong, and who pulls the plug?

They should resurface in every Day 2 block — ideation, prototyping, Responsible AI, and PoC build — not only in the commercial reality check.

---

## Ideation

**Related prompt:** `prompts-v2/day-two/E-ideation.md`

### Exercise: Look Beyond Where You're At Today

**→ Prompt:** `prompts-v2/day-two/E-ideation.md` — Uncover Broader Opportunities.

**Time:** 30 mins

Check your list with your personas. Where do they think opportunities are?

**Done check:**

- A list of opportunity areas is saved to the repo.
- The participant can name a few that feel like real expansion territory, not just bigger versions of what the product already does.

### Ideation: Turn Problems Into Ideas

You spent yesterday doing research, building personas, and defining problems. Now interpret what you learned and turn those insights into tangible ideas.

Generate many ideas before filtering. Ideas that seem impractical at first can lead to the most interesting directions.

### Exercise: Ideate With AI

**→ Prompt:** `prompts-v2/day-two/E-ideation.md` — Ideate with AI Perspectives (startup / adjacent industry / personas), then Cluster Ideas.

**Time:** 20 mins

Hand your HMW questions to AI and have it answer from perspectives that challenge your default thinking. Run each perspective as a separate prompt.

Use perspectives such as:

- A well-funded startup entering the market with no legacy constraints
- A product team from another industry that solved a similar problem
- Each persona from your user research

**Done check:**

- Idea lists exist for the three perspectives: startup, adjacent industry, and personas.
- The participant has identified which ideas came up across multiple perspectives.

---

## Refine Ideas And Stress-Test Use Cases

**Related prompt:** `prompts-v2/day-two/F-prototype-build-for-agentic-idea.md`

### Value And Feasibility

**Value questions:**

- Do customers have a real pain point this solves?
- Would they pay to fix it?
- How many customers does this affect?
- What could the revenue model look like?

**Feasibility questions:**

- Is the problem specific and well-defined?
- Do we have the data or content we need?
- How complicated is this to build?
- How long would it take?
- Do we need anything we do not currently have?

**Placement language:**

- Prioritize First: feasible to build, strong value case
- Invest & Explore: clear value, but lower confidence in feasibility
- Deprioritize: feasible to build, but value is not clear
- Park It: feasibility and value are low or not yet understood

**Commercial signals can include:**

- Lost deals
- Expansion asks
- Paid pilot interest
- Renewal risk
- Competitor displacement
- Measurable support cost
- Usage patterns
- Direct customer quotes

### Exercise: Refine Ideas

**→ Prompt:** `prompts-v2/day-two/F-prototype-build-for-agentic-idea.md` — Shape Use Cases → Score & Sort → Commercial Reality Check.

**Time:** 75 mins

**Steps:**

- Shape ideas into use cases.
- Group ideas into clusters and validate them against problem statements.
- Ask whether they solve meaningful problems or represent new opportunities.
- Turn clusters into use cases with What, Who, Problem, and Value.
- Examine value and feasibility.
- Prioritize what is worth going after first.
- Run a commercial reality check.
- Get concrete on who writes the cheque, pricing model, size of value, and evidence that customers would pay.

**Done check:**

- The use case markdown file has two to three shaped use cases.
- Each has What, Who, Problem, Value, value/feasibility score, matrix placement, and pricing rationale backed by evidence or noted as a risk.
- The participant can state the top use case for PoC, the top two to three backlog items, and what changed from what they walked in with.

### Exercise: Stress-Test Your Top Use Cases

**→ Prompt:** `prompts-v2/day-two/F-prototype-build-for-agentic-idea.md` — Stress-Test Your Top Use Cases (persona role-play + kill-a-bad-idea).

**Time:** 30 mins

Take your top one to two use cases and stress-test them with personas and assumptions.

Ask personas:

- What would confuse you?
- What would make this valuable?
- What would make you ignore it?
- What would you need to trust it?
- What would you pay for, if anything?

Follow-up:

- Compare how each persona reacted.
- Where do they agree?
- Where do they disagree?
- What specific changes would strengthen the use case?

Optional Kill Your Darlings:

- Run a pre-mortem: it is six months from now and this failed. Why?
- Run a "Why not already?" test.
- Surface the assumptions the team skipped past.

**Done check:**

- The use case markdown file has been updated to incorporate persona feedback.
- Each use case reflects what the personas said, not just what the team started with.

---

## Responsible AI

**Related prompt:** `prompts-v2/day-two/G-responsible-ai.md`

Responsible AI is the practice of designing, developing, and using AI technology to maximize benefits and minimize risks. These dimensions need to be assessed and updated over time as the technology evolves.

Dimensions:

- Privacy and Security: sensitive data, protection, access, storage
- Safety: what happens when AI is wrong
- Transparency: whether users know AI is involved
- Explainability: whether users or support can understand why AI produced an output
- Veracity and Robustness: edge cases, unusual workflows, bad inputs
- Fairness: whether the system works differently for different user groups
- Governance: ownership, policies, oversight
- Controllability: human oversight and ability to intervene, adjust, or shut down

**Facilitator reminder:**

- This is not compliance theatre.
- This is about building AI systems customers can safely and confidently rely on.
- Transparency and explainability should be designed early, especially for agentic workflows.

### Exercise: Responsible AI Fit

**→ Prompt:** `prompts-v2/day-two/G-responsible-ai.md` — Responsible AI Fit (the 15-minute conversation).

**Time:** 15 mins

This is a conversation, not a checklist. The participant should use Claude to ask sharp questions that make them think about the Responsible AI watch-outs that matter most for the idea they are prototyping.

Pick your top use case or one that involves AI. If none involve AI yet, hypothetically add it or work with Claude to do that.

Talk through four lenses:

- Explainability: can you explain why it produced a given answer or decision?
- Transparency: do users know AI is involved, and why it acted?
- Fairness: could it serve some users better than others?
- Safety: what could go wrong if the output is wrong, incomplete, biased, misunderstood, or brittle?

Mapping note:

- For this 15-minute exercise, fold Privacy and Security plus Veracity and Robustness into Safety.
- Sensitive data, model-boundary risk, hallucination, bad inputs, and edge cases belong under Safety if they matter.
- Ownership and accountability should be captured as an open question if unclear, but this is not a governance-mapping exercise.

Starter prompt:

```text
Here's the idea I'm prototyping: [paste].

Act as a Responsible AI facilitator. Ask me short, sharp questions across four lenses: explainability, transparency, fairness, and safety.

Ask one question at a time. After each answer, reflect back the implication in 1-2 sentences, then move on. Skip lenses that are low relevance. Do not solve the risks or produce a checklist.

Start with the lens most likely to matter for my idea. Ask your first question now.
```

**Done check:**

- The participant can name the 1-2 Responsible AI watch-outs that matter most.
- They know whether one design assumption needs to be checked before prototyping.
- They have surfaced watch-outs without trying to solve all of them in the room.

### Optional Deeper Inventory

**→ Prompt:** `prompts-v2/day-two/G-responsible-ai.md` — Optional: Deeper Responsible AI Inventory (facilitator-triggered only).

Use the deeper inventory only if the facilitator asks for it, or if the use case is high-risk enough that the short fit check is insufficient.

The deeper sweep can cover:

- Privacy and Security
- Safety
- Transparency
- Explainability
- Veracity and Robustness
- Fairness
- Governance and Controllability

---

## Lock And Build The PoC

**Related prompts:** `prompts-v2/day-two/F-prototype-build-for-agentic-idea.md`, `prompts-v2/day-two/G-responsible-ai.md`

### Exercise: Lock Your Top Idea

**→ Prompt:** `prompts-v2/day-two/H-poc-build-for-handoff.md` — 1. Lock Your Top Idea.

**Time:** 30 mins

**Questions:**

- Is your top use case still the right one to take into a PoC, or has something shifted?
- What did the use case challenge reveal that your idea does not yet reflect?
- If you showed your idea to your persona right now, what would confuse them?
- What is the strongest version of your idea you can have ready by end of day?

**Useful prompts:**

```text
Here is my problem statement and my use case. Does it solve the problem? Be honest.
```

```text
Write 3 user stories for my persona. Does my use case cover each one fully, partially, or not at all?
```

**Done check:**

- The top use case is locked.
- The participant can pitch it in one sentence: who it is for, what it does, how they will know it works.
- The participant knows the one thing the PoC must show.

### Prototype Mindset

The prototype is an experiment.

- A prototype that proves the idea wrong is just as valuable as one that proves it right.
- A rough prototype is more useful than a blank page because people can react to it.
- The real prototype emerges from the conversation after the first version.
- If no one can tell what it does in a few seconds, fix that first.
- Fake the magic: mock the agentic concept, not working AI. In a mock anything is possible, so push the limits and show the boldest version of the agent doing the job — the agentic move, not another dashboard.
- Make the agent's reasoning visible in the UI and show the human-in-the-loop approval step.

### Exercise: Build Your PoC

**→ Prompt:** `prompts-v2/day-two/H-poc-build-for-handoff.md` — Lock → Commercial gate → Build → Refine → Handoff → Mark Miller.

**Time:** 1.5 hrs (the final Day-2 build runs ~2.5 hrs and adds a dedicated 25-min commercial-check phase).

Bring your locked idea, persona, and problem statement into Claude Code as context.

**Before you build — commercial check: revenue is the gate.** In the agentic lane you sell the work itself, not a screen. No concept advances to build or demo without all three:

- **Who pays?** The budget owner whose labour line shrinks when the agent does the work — name them.
- **What does it displace?** The people-time, tool, or workaround that goes away (anchor to the ~$6 labour : $1 software split).
- **A price that survives a CFO.** A number and model where the value dwarfs the cost of running the agent.

Have Claude play a sceptical CFO and attack your pricing. If you can't answer all three, fix the idea before building. "I don't know yet" is a valid answer — capture it as an open question, not a failure. The gate is here to sharpen the commercial case, not to pass a test.

Confirm scope:

```text
Here is my locked idea and persona. Scope this to a throwaway prototype I can vibe-code — one screen or a few linked flat screens, no backend or database — and tell me the single thing it must get right.
```

**Start:**

```text
Build a working HTML prototype for [your one-sentence scope]. Make it look real enough that a user could react to it.
```

**Pressure-test:**

```text
Critique this prototype against my persona's top three needs. What did I miss?
```

**Done check:**

- The participant can demo the prototype in 60 seconds.
- They can explain the problem it solves.
- They can explain which persona it serves.

**Facilitator reminder:**

- Do not jump straight into building.
- Let Claude interview the participant on the HMW and shape the solution first.
- Bring personas back into the refinement phase.
- Broken PoC is fine. Confusing is not.

### Closing move: pressure-test with Mark Miller

To end Day 2, run the built PoC past **Mark Miller** — the standalone commercial-reviewer prompt at `prompts-v2/day-two/mark-miller-evaluator.md` (Step 5 of the PoC build chapter). It is the last gut-check: can the idea earn revenue, deepen workflow ownership, or defend the moat? Start with the short intake at the top of that file; it is not part of the A–H sequence, so reach for it only once there is a proposal worth stress-testing.

---

## Looking Ahead: The Plan For Day 3

The Day 2 closing slide previews how Day 3 works (this is the build handoff, not the cross-VBU challenge):

- **Reconvene & align:** the whole VBU presents PoCs, discusses, and agrees the idea.
- **Split into tracks:** GM track presents the idea; dev + product become the build team.
- **Spec, then build:** the build team co-creates the spec, then builds. Pick your disruption lane (Customer / Company / Product-agentic) the night before or first thing.
- **Plan hard — it is the build:** spec-driven development lives on the plan. The strongest accelerator builds spent serious time planning the build with Claude before writing code; the product team's job is to help the dev team shape that plan.
