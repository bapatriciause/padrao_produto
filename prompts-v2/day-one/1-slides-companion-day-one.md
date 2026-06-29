# Day 1 Slides Companion

Use this alongside the v2 prompt chapters. It is not a full slide transcript. It keeps the exercise titles, key slide language, examples, done checks, and facilitator reminders that participants are likely to need while Claude Code is guiding them.

Source: the Palm Beach Product Track facilitation deck (Day 1), plus the set-up / Git walkthrough.

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

- Day 1 Orientation
- Confirm Set-Up
- Multiple Sessions And Delegation
- Spotting AI Opportunities
- Personas
- Problem Statements, Stack Rank, And HMWs
- Practising Customer Interviews
- Demo To Content

---

## Day 1 Orientation

**Related prompts:** `prompts-v2/00-onboarding.md`, `prompts-v2/day-one/A-market-research.md`

**Day 1 agenda:**

- Product set-up, intro, and housekeeping
- Rapid Market and User Research
- Problem Definition, How Might We Questions, and Jobs To Be Done
- Practical Product Management with AI
- Wrap-up
- Daily Debrief with GM

**Goals for today:**

- "Weeks of research and analysis, done in a day."
- Orientation: where product fits in AI-first development
- Research: AI-analysed market and personas
- Define: sharp problems, HMW, and jobs to be done
- Interview: practising the art of customer conversations
- Outcome: a validated problem, ready to build on

**Participant framing:**

- You will be working, not watching.

### Pick Your Disruption

Pick the lane where the team will create the most value, chosen on honest strengths, not what is easiest to start Monday.

Disrupt your customer:

- The play: a booked customer demo driving this week's build, with real revenue on the line.
- What we want to see: speed and pivot.
- Watch out: the same idea you walked in with. Show how far you pushed it and what you built in four days.

Disrupt your company:

- The play: a big chunk of real backlog cleared in two days, in your own codebase.
- What we want to see: quantity and quality of execution, showing what the AI-SDLC unlocks.
- Watch out: a pile of cleared tickets with no framing. Show it passes security scans and works.

Disrupt your product:

- The play: a narrow but deep, multi-step agentic flow.
- What we want to see: reasoning and explainability, not production-ready polish.
- Make the reasoning visible.
- Watch out: conventional flows dressed up as agentic.

---

## Product Thinking Today

The opening framing for why this week is different.

**Product thinking today is slow:**

- Few ideas make it through the pipeline — costly to test concepts, so few use cases get explored.
- Customer feedback comes late — prototypes need heavy up-front effort before anyone reacts.
- Market research and data synthesis is time-consuming — interviews and competitive analysis eat time.

**AI-driven product thinking:**

- Every aspect of product management gets quicker — discovery, analysis, ideation, and validation all compress.
- More experimentation and proof of concepts — a problem description becomes a working prototype, fast.
- Stronger data synthesis and decision making — synthesize large data to challenge bias and inform decisions.

**The key line:**

- With AI we can experiment faster, and the bottleneck is no longer building — it's knowing what to build.

---

## What Is An Agentic Tool?

**Related prompts:** `prompts-v2/00-onboarding.md`, `prompts-v2/day-one/D-practical-product-management-with-ai.md`

Most AI tools answer questions. The tools used this week take actions.

You are not prompting a chatbot. You are directing an AI that works through multi-step tasks inside your own data.

**Chat AI:**

- You ask a question and get a response.
- Output is text in a chat window.
- You copy and paste results into other tools.
- It is usually single turn.

**Agentic AI:**

- You describe a task and the AI works through it.
- Output can be files, code, analysis, or prototypes.
- The AI reads your data, writes to your repo, and iterates.
- It is multi-step: plans, executes, adjusts.

**Tools this week:**

- Claude Code is the primary workspace. It reads files, writes analysis, and builds prototypes.
- Claude.ai is for research and quick questions with web access.
- Claude Cowork is a collaborative workspace where multiple people can work with Claude together in real time.

**Facilitator reminder:**

- Frame this as shared setup, not a basic AI lecture.
- The skill is not technical. The skill is clear direction.

---

## Connect Your Tools

**Related prompt:** `prompts-v2/00-onboarding.md`

Read-only access is plenty.

Useful access includes:

- API access to the support system
- Read access to product repos
- Access to product docs, tickets, customer research, support exports, or usage data

Once tools are connected, participants can ask things like:

- I want to write product specs and docs.
- I want to do product research.
- I want a spec for devs that understands our codebase.

If access is missing:

- Request it urgently.
- If blocked, talk to the GM in a break.
- Get everything connected ahead of Day 2 where possible.

---

## Confirm Set-Up

**Related prompt:** `prompts-v2/00-onboarding.md`

**Exercise:** Confirm Set-up

**Time:** 15 mins

The slide asks participants to confirm they have:

- Claude Code open and running
- Repo linked to their folder
- Tools connected where possible
- Pre-work files uploaded
- The repository available, because full step-by-step instructions live there
- the day-specific slides companion open so they can follow along on their own screen

**Sample prompt to try:**

```text
Read the files in the repo and give me a summary of what you've found. What am I attending? What looks most useful? What's missing?
```

**Useful setup framing:**

- GitHub is cloud storage in reverse.
- You copy the whole project down to your computer.
- That local copy is your repo.
- You edit files locally, then push the update back.
- Git tracks versions.
- GitHub is where the team's shared copy lives.
- Clone means copy down.
- Push means send changes up.
- Pull means get the latest.

**Why you even care about Git (the unlock):**

- Right now your devs are often the gatekeepers — good ideas stall in the dev queue: bug tickets, ROMs/estimates, prototypes, scripts, debugging all wait their turn.
- This week you get the keys: build it yourself with Claude Code, then hand dev a clean repo to take further, together.

**Git matters because (the three payoffs):**

- It is the safety net for the Product track. A commit is a checkpoint; participants just tell Claude "save my work." The agent runs the commands — no need to memorise them.
- **Experiment without fear:** every exercise is reversible — rewind a bad idea in seconds. Removing the risk of being wrong is how AI-first teams move faster.
- **Your agent's work is traceable:** Git records what changed, when, and why — a full audit trail, so handoff to development becomes a conversation, not a guess.
- **The team stays in sync:** insights, personas, problem statements — everyone sees the same version. The repo is the team's shared brain for the week.

**Facilitator reminder:**

- The skill is not technical Git fluency. The skill is knowing that the work is safe, traceable, and shareable.
- If setup fails, the fallback is to generate files in another AI application, download them, and upload them manually to the Git workspace.

---

## Multiple Sessions And Delegation

**Related prompt:** `prompts-v2/00-onboarding.md`

**Purpose:** teach participants that they do not need to sit idle while one Claude response is running.

**Key message:**

- Multiple sessions are optional.
- Claude cannot open extra sessions for the participant.
- The participant opens a new Claude Code session or window themselves.
- Claude can tell them when parallel work would help and what to paste in each session.
- Parallel sessions are useful for independent research or analysis.
- One focused session is better for judgement-heavy decisions.

**Good use of multiple sessions:**

- One session researches market trends.
- One session analyses customer or internal data.
- One session reviews competitors.
- Outputs come back together in `insights.md`.

**Better kept in one focused session:**

- Choosing problem statements
- Refining personas
- Selecting use cases
- Responsible AI fit
- Revenue-signal review

**Facilitator reminder:**

- Do not pressure everyone to use multiple sessions.
- Do stop people from waiting unnecessarily if they are comfortable moving faster.

---

## Build A Dashboard (morning foil)

**→ Prompt:** `prompts-v2/day-one/C-problem-definition-hmw-jtbd.md` — Morning Warm-Up: Build A Dashboard.

Right after set-up, build something real in ~15 minutes: pick a report or metric someone in your business has asked for and have Claude build a working, clickable dashboard.

**This is a deliberate foil, not your answer.** You'll pull it apart this afternoon to find the real job underneath — *the dashboard is the receipt, the job is the product.* Don't over-invest; ship something you can open and click, then move on.

**Done check:** a working dashboard saved to your repo, plus a one-line note of who would open it, how often, and what they would do next.

---

## Opportunity To Capture Customers' Operational Spend

The strategic "why" behind the opportunity hunt (source: Menlo — "Software Finally Gets to Work: The Opportunity in Vertical AI").

Software today owns the **system of record** — workflows, processes, approvals. But that's only about **$1** of a customer's operational spend. The other **~$6** sits in the layers above the software:

- **Workflows & processes** — repeatable tasks, approvals, compliance steps.
- **Service & labour** — people executing, interpreting, responding.
- **Knowledge & judgment** — domain expertise, pattern recognition, decisions.

These upper layers are where AI lets us break in. Four reasons we can:

1. We can do it **faster** than before, with AI-first development.
2. We can do it **better** than others, due to our proprietary domain data and vertical expertise.
3. We can make it **valuable** for customers, leveraging our customer intimacy to target real pain points.
4. We can **scale** it through existing distribution — our software is already embedded in the workflow.

(This same model reappears on Day 2 as the System-of-Record → System-of-Understanding ladder.)

---

## Spotting AI Opportunities

**Related prompt:** `prompts-v2/day-one/A-market-research.md`

The goal of this block:

Where could AI create new value or revenue in your business?

Use two lenses:

- External lens: what is changing around us?
- Internal lens: what do we already have that could become new value?

Why both lenses matter:

- Some teams chase external trends and ignore what they are sitting on.
- Some teams stay heads-down inside the product and miss what is shifting outside.
- The point is to cover both angles.

### Exercise: Getting Started On Rapid Market Research

**→ Prompt:** `prompts-v2/day-one/A-market-research.md` — run the market, customer, and competitor scans, then distil to `insights.md`.

**Time:** 20 mins

**Key questions:**

- What is changing in our industry that creates new opportunity?
- What pressures are our customers facing that we could help solve?
- What are our competitors building that we are not?
- Where is demand heading?
- Where might we be exposed?

**Prompting reminder:**

- Define the role.
- Provide context.
- State the goal.
- Describe what good output looks like.

**Parallel-working reminder:**

- The three main prompts can run in parallel if the participant opens separate Claude Code sessions.
- Claude should tell the participant what to paste into each session.
- Running one chat at a time is fine.
- Bring findings together at the end.

**Done check:**

- A markdown file is saved to the repo with market research findings and key insights.
- Each insight is specific and connects to product direction.
- Insights should not be general industry statements.

### What A Good Insight Looks Like

A good insight connects a specific finding to something that could inform product direction. It should signal where demand is heading, where the business is exposed, or where there is an unmet need.

**Weaker examples:**

- "Our market is moving toward agentic AI and automation."
- "Our NPS is strong and customers seem satisfied with the current feature set."

**Why they are weak:**

- They are too generic.
- They sound like headlines.
- They do not say what changed, who is affected, or what the product team should do differently.

**Stronger examples:**

- "Three competitors now offer predictive features and customers are asking about it in sales calls."
- "40% of accounts export data to spreadsheets for analysis our platform could handle natively."

**Speed is not validation.** Producing insights fast with AI does not make them true. Treat the insight that only confirms what you already hoped or believed as the one to distrust most — label its confidence and note the disconfirming evidence you'd need to check it. "Our NPS is strong" feels reassuring precisely because it asks nothing of you.

**Why they are stronger:**

- They are specific.
- They connect evidence to product direction.
- They show demand, exposure, or unmet need.

**Role-specific evidence note:**

- Product may bring roadmap and discovery notes.
- Sales may bring lost deals, demo objections, pricing pushback, and competitor battlecards.
- Customer Success may bring renewal risk and adoption patterns.
- Support may bring ticket themes.
- Engineering or Implementation may bring feasibility and workflow constraints.
- Label confidence clearly: repeated customer signal, role-specific observation, one-off anecdote, or confirmed by usage/support/revenue data.

### Exercise: Analyze Your Data

**→ Prompt:** `prompts-v2/day-one/A-market-research.md` — the internal-data / customer-analytics scan.

**Time:** 25 mins

**Key questions:**

- What insights are hiding in customer interviews, existing data, tickets, and feedback?
- What do we already have in our product and data that we are not using to create value?
- What recurring behaviours and patterns show up in how different users engage with the system?
- Are there distinct groups of users doing fundamentally different things with the product?

**Slide guidance:**

- Turn to the data you have access to.
- Use support tickets, customer feedback, usage data, interview transcripts, and anything else in the repo.
- Ask Claude what customers are telling you they need.
- Ask what you can infer from how customers actually behave.
- Ask whether the product could surface insights instead of just storing them.

**Done check:**

- A markdown file is saved to the repo with internal data findings and key insights.

### Exercise: Bringing It Together

**→ Prompt:** `prompts-v2/day-one/A-market-research.md` — cross-reference the findings and distil the sharpest insights into `insights.md`.

**Time:** 25 mins

Prompt items to include:

- Compare market research findings with internal data analysis.
- Where do they align?
- Where do they contradict?
- Identify opportunities at the intersection of external trends and internal strengths.
- Based on everything analysed, what assumptions are probably unsupported?
- Where might we be wrong?

**Keep in mind:**

- If you had to brief leadership on the three most important findings from the morning, what would they be?
- Which findings should influence what you build?

**Done check:**

- A markdown file is saved to the repo that cross-references market findings with internal data.
- Key insights are called out.
- The participant can name the three most important insights from the morning.

### Optional Exercise: Recurring Market Research Agent

**→ Prompt:** `prompts-v2/day-one/A-market-research.md` — the optional recurring-agent section (after the core flow).

**Time:** 10 mins

Set up a weekly agent that does market research on a cadence and delivers a brief you can act on.

Personalize the agent with:

- Three to five specific competitors to watch
- Sources you trust: publications, analysts, newsletters
- Customer segments: company size, geography, vertical, buyer type
- Internal context: current strategic bets, roadmap themes, investment areas
- What "useful" looks like: pricing moves, AI launches, regulatory shifts, feature adoption trends, M&A

**Facilitator reminder:**

- This is optional. It is useful after the core research flow, but should not distract from creating `insights.md`.

### Market Research Map

The deck now summarises this as a four-phase block, about 70 minutes end to end:

- Research your market: scan industry shifts, customer pressures, and competitor moves.
- Analyse your data: point Claude at tickets, feedback, usage, and interview transcripts.
- Bring it together: cross-reference market findings against internal data and challenge assumptions.
- Set up a recurring agent: schedule a weekly brief that reruns the research and delivers signals the team can act on.

Outputs:

- A market-findings file with product-tied insights
- An internal-findings file
- A cross-referenced file naming the three sharpest insights
- A personalised weekly brief, if the recurring agent is set up

---

## Personas

**Related prompt:** `prompts-v2/day-one/B-user-personas.md`

**Key message:**

AI can generate personas quickly. Quick does not mean correct.

With AI, personas change in three practical ways:

- You can build personas from real data.
- AI can evaluate personas and show where assumptions are unsupported.
- Once grounded, a persona can become a thinking partner for testing ideas.

Getting personas right matters because every later exercise depends on their quality. Generic personas produce generic ideas, bias, and low-value use cases.

### What Makes A Good Persona

A good persona includes:

- Role and relationship to the problem the product solves
- The realities they navigate day to day, not just inside the software
- What they are trying to accomplish
- How they use the product
- How often and how deeply they use it
- What workarounds they rely on
- Pain points grounded in real data
- Decision patterns and motivations

Distinct personas should reflect genuinely different behaviours and motivations, not just unique job titles.

**Weaker examples:**

- "Sarah, 42, Operations Manager at a mid-size company. Tech-savvy. Uses our platform daily. Wants better dashboards and faster reporting."
- "Enterprise customer. 500+ employees. Needs advanced features and integrations."

Stronger example:

- "Regional operations manager overseeing 15 sites. Accountable for incident rates but has no real-time visibility. Relies on weekly spreadsheets from site managers. Finds out about problems last."

**Role-specific evidence note:**

- Do not confuse buyer segments, admin roles, internal teams, or implementation stakeholders with personas.
- They may matter, but product work also needs the day-to-day user whose workflow changes.
- Buyer ≠ user. "The CFO who signs the contract" is the buyer; "the AP clerk who lives in the system every day" is the user. Build personas for the people who do the work, not just the people who pay.

### Exercise: Build Your Personas

**→ Prompt:** `prompts-v2/day-one/B-user-personas.md` — build personas from your evidence, then critique them.

**Time:** 20 mins

Start with the insights from the morning. Market research and user data analysis should already have surfaced patterns. Now go deeper into who the users actually are.

Build personas. For each one, include:

- Role and relationship to your product
- Realities they are navigating
- Core motivations
- Key pain points
- How they make decisions

Consider:

- What are they trying to accomplish in their role and world?
- What pressures or constraints shape their decisions?
- What are their primary goals when using your product?
- How do they interact with your product?
- What workarounds do they use?
- What do they care about most: price, speed, quality, support?
- Where does what users say contradict what they do?

Support material:

- Ask AI to create two to three personas from your data.
- Then challenge them: "What assumptions are you making that are not supported by the data?"
- Use the empathy map format: Says, Thinks, Feels, Does.
- If your data is thin, ask: "What are the three most important questions I should be asking my users?"
- Describe each persona from their perspective, not yours.
- Aim for two to four personas.

**Done check:**

- At least two personas are generated and critiqued.
- The participant can name at least one assumption that was challenged by the data.

### Exercise: Pressure-Test And Strengthen Your Personas

**→ Prompt:** `prompts-v2/day-one/B-user-personas.md` — score and refine the personas; fill gaps from the data.

**Time:** 10 mins

**Steps:**

- Run the scoring prompt with your personas.
- Note where each persona scored lowest.
- Go back into your data immediately.
- Use tickets, feedback, and usage data to fill gaps.
- If two personas are too similar, merge them.
- Rescore.
- If a persona still cannot improve, note what data you need after the accelerator.

Scoring criteria:

- User-driven: is this persona defined by who the user actually is?
- Specificity: could this only have been written if you had seen the data?
- Distinctiveness: would this persona lead to different product decisions?
- Actionability: could a product team use it to decide what to build next?
- Data grounding: is this built from evidence or intuition?

Score skeptically. Most personas built from thin data sit in the low-to-mid teens out of 25 — a total above 20 usually means Claude is being too generous, so push inflated scores back down against the evidence. If a persona has little or no interview data behind it, mark it provisional and write a one-line DATA GAP note rather than inventing detail to lift the score.

**Done check:**

- Updated personas are saved to the repo with improved scores.
- The participant can name at least one assumption challenged and one gap filled from the data.

---

## Job, Problem, Stack Rank, HMWs, And Dashboard Autopsy

**Related prompt:** `prompts-v2/day-one/C-problem-definition-hmw-jtbd.md`

### From Job To Problem To Opportunity

The job is the lens that reveals the real problem, not necessarily the one the team walked in with. The afternoon block ("From the job to the opportunity", ~75 min) runs:

- **Jobs to be done (~15 min):** pull apart the dashboard you built this morning until you can name the real job it serves — solution-free.
- **Problem statements (~20 min):** turn your research into 1-2 problem statements, citing every field.
- **Rank the problems (~20 min):** rank as the customer would — by what it costs them, not what excites you.
- **Generate HMWs (~20 min):** reframe the top problem as opportunities — then ask where on the AI ladder that opportunity should play.

The slide language to hold onto:

- The job is the lens that reveals the real problem; the dashboard is the receipt, the job is the product.
- Define it, prioritise it, reframe it as opportunities — then place the top one on the AI ladder.
- Tomorrow, ideate and prototype the strongest one.

### How AI Pushes The Job

AI creates value by doing more of the customer's job:

- Visibility / enabler: shows the job through a dashboard, alert, or summary.
- Productivity / utility: does one step such as drafts, codes, extracts, or reconciles.
- Automation / workflow: runs the whole job, with the human approving.
- Autonomy / multi-step: runs unwatched and escalates exceptions.

**Test:**

- Turn it off. Does work pile up, or does a screen just go blank?
- You sell the doing, not the displaying.

### What A Good Job Looks Like

A job is the progress a customer is trying to make. Write it solution-free: no app, dashboard, or "AI."

**Format:**

```text
When [situation], I want to [motivation], so I can [outcome].
```

**Stronger example:**

- "When a claim is denied, a processor wants to catch it before rework piles up, so they clear the queue without overtime."

**Weaker example:**

- "Claims processors need an AI dashboard to track denials."

**Why the stronger example works:**

- It is situation-based.
- It is measurable.
- It names no solution.

### Building A Problem Statement

A problem statement names what you are solving, who has the problem, and why it matters. It anchors ideas, prototypes, and what eventually ships.

**Format:**

```text
[User/persona] needs a way to [achieve goal / overcome pain] because [evidence / insight], which currently results in [measurable negative outcome].
```

Key components:

- Specific: could you find this user and interview them?
- Grounded: is the evidence from research, not an assumption?
- Root cause: have you asked why enough to get past the symptom?
- Solution-free: does it describe the problem without smuggling in the answer?

**Weaker examples:**

- "Dispatch teams have a delay problem and need better visibility tools."
- "Claims processors need a denial-prediction tool so they can rework fewer claims each month."

**Stronger examples:**

- "Dispatch coordinators at regional freight carriers miss too many SLAs, finding out about delays only when customers complain, costing 22% of monthly performance."
- "Claims processors at regional health insurers have too many denials, caught only during rework, costing 18% of admin time."

**Facilitator reminder:**

- Claude will often sneak in a solution.
- Ask: is this a real problem, or a feature wearing a problem costume?
- If there are no numbers, do not force numbers into the template.
- Think elevator pitch: one or two sentences on what the customer is actually experiencing.

### Exercise: Phase 1 - Problem Statement

**→ Prompt:** `prompts-v2/day-one/C-problem-definition-hmw-jtbd.md` — Problem Statements (generate, then interrogate).

**Time:** 20 mins

Pull from:

- Market research
- Internal data
- Personas
- Cross-referenced insights

Use Claude to generate candidate problem statements.

Make sure:

- Every field cites a source.
- More than one problem statement is allowed if the research supports it.
- The user is specific enough to identify and interview.
- The statement does not smuggle in a solution like "better visibility tools" or "AI-powered dashboard."
- Each statement traces to research, not inference Claude made.

**Done check:**

- At least one to two problem statements are saved to the repo.

### Exercise: Stack-Rank The Customer's Problems

**→ Prompt:** `prompts-v2/day-one/C-problem-definition-hmw-jtbd.md` — Customer Problem Stack Rank.

**Time:** 20 mins

A product can fail by solving a problem but not the customer's most important problem.

Based on Shreyas Doshi's "Customer Problem Stack Rank" (opinionx.co). Watch the **focusing illusion**: customers over-weight whatever you ask them about, so rank every candidate against everything else on their plate — by what it costs them (time, money, risk), not by what excites you.

Bring forward:

- The candidate problem statements just generated
- The five problems the participant arrived with

For each one, tag:

- Who has it: persona or role
- How often it happens
- What it costs them
- What they do about it today

Then rank the problems as the customer would, across everything on their plate, not by what the product team finds interesting.

Use Claude to pressure-test:

```text
Play my customer's ops lead and re-rank these. What did I over-weight?
```

**Watch out:**

- The problem that is interesting to the team but ranks fifth for the customer.
- If the planned build is not in the customer's top three, rewrite around a higher-ranked problem or clearly defend why not.

**Done check:**

- Problems are tagged and ranked as the customer would rank them.
- The participant has picked the top-ranked problem to carry into HMWs and ideation.

### Evaluating HMWs

How Might We questions reframe a problem as opportunities. They open the solution space for ideation.

**Format:**

```text
How might we [achieve something] for [someone] so that [outcome]?
```

The sweet spot:

- Narrow enough to be actionable
- Broad enough to allow creative solutions

**Weaker examples:**

- "How might we build a denial-prediction model?"
- "How might we use AI to improve our product?"
- "How might we improve the customer experience?"
- "How might we get claims processors to be more careful with data entry?"

**Stronger examples:**

- "How might we help spot at-risk deliveries before customers complain?"
- "How might we help claims processors catch likely denials?"
- "How might we help production schedulers see equipment risk before delays cascade?"

### Exercise: Phase 2 - Generate Your HMWs

**→ Prompt:** `prompts-v2/day-one/C-problem-definition-hmw-jtbd.md` — HMW Questions (generate, then interrogate).

**Time:** 20 mins

Explore your problem statements with HMW questions.

**Keep in mind:**

- HMWs should not be solutions or requirements.
- Stay grounded in the user's needs and context.
- Check whether each HMW solves the root problem or just a symptom.
- Draft your own HMWs in parallel with Claude, not after.
- If Claude sees yours first, its next batch anchors to your language.
- Cap the output. Ask for 20 max per problem statement, or have Claude pick the top 20 worth reading.

**Done check:**

- HMWs are organized by problem statement and saved as markdown to the repo.

### Jobs To Be Done: Pull The Dashboard Apart (the on-ramp)

**→ Prompt:** `prompts-v2/day-one/C-problem-definition-hmw-jtbd.md` — Jobs To Be Done: Pull The Dashboard Apart.

You built a dashboard in this morning's warm-up. This is where you pull it apart — it is how the Jobs To Be Done step starts, not a separate intervention at the end.

Work backwards from the dashboard:

- Who looks at it?
- When do they look at it?
- What do they do next?
- Where does the data come from / what job generates it?
- If the dashboard disappeared but the job still got done, what would be doing the work?

Then name the underlying job (solution-free) and where it should sit on the AI ladder (visibility → productivity → automation → autonomy).

**Key line:**

- The dashboard is the receipt. The job is the product.

If a later idea collapses back into "we need a dashboard," rerun the same autopsy to climb from visibility to the job.

---

## Practising Customer Interviews

**Related prompt:** `prompts-v2/day-one/C-problem-definition-hmw-jtbd.md`

How to have a good interview:

- Be curious about them and their world, not just your product.
- Start broad, finish deep.
- Build rapport first, then dig into the specific things they mention.
- Ask about specific moments: "Tell me about the last time..." instead of "Do you like..."
- Ask to see the actual thing. What people say and what they do often differ.
- Do not put the answer in your question.
- Avoid yes/no and leading questions.
- Talk less than half the time.
- When they pause, wait instead of jumping in.

Good vs bad questions:

- Too broad: "What do you think of the product?"
- Better: "Tell me about the last time you used it."
- Leading: "Wouldn't automating this be useful?"
- Better: "What happens right before and right after you do this?"
- Yes/no: "Do you track this somewhere?"
- Better: "Show me how you tracked it this week."

What to listen for:

- What lights them up, and why
- A story or experience that shaped how they think
- Something you would never have guessed
- The thread you would keep pulling on with more time

### Exercise: Get To Know A Stranger

**→ Prompt:** in-room exercise, no Claude prompt. Context: `prompts-v2/day-one/C-problem-definition-hmw-jtbd.md` — Practising Customer Interviews.

**Time:** 40 mins

Pair up with someone you do not know and take turns interviewing each other, ten minutes each.

Keep it off work. Do not talk about your company, your product, or your customers. Spend the time getting to know the person, following whatever thread is interesting, and see where the conversation goes.

**Done check:**

- The participant can name a couple of real insights about their partner, such as what brings them delight or what frustrates them.

---

## Automation And Tooling Examples

**Related prompt:** `prompts-v2/00-onboarding.md`

Every Claude session is a loop:

- Prompt: give Claude context and direction.
- Output: Claude produces work.
- Return: the participant tells Claude what to improve.

The quality comes from the return. Participants should treat feedback to Claude as part of the work, not as a correction after the work is done.

Examples from the deck:

- Jira ticket plus GitHub code to customer-ready setup guide
- Existing importer plus codebase to PoC browser extension and scoped SOW
- Skill output plus sandbox to walkthrough script for customer meeting prep

### Turn A Demo Into Content

**Related prompt:** `prompts-v2/day-one/D-practical-product-management-with-ai.md`

The slide asks participants to turn a 3-5 minute feature walkthrough into useful content.

Inputs:

- Transcript of the walkthrough
- Finished artifacts from the build
- Examples of the participant's normal writing, such as blog posts or LinkedIn posts

Outputs can include:

- Blog post
- LinkedIn post
- Release notes
- Customer email
- Sales enablement note
- Internal update

The core workflow:

- Record the walkthrough.
- Give Claude the transcript, artifacts, and tone examples.
- Have Claude draft from the walkthrough.
- Refine with feedback.
- Turn the process into a reusable skill or prompt if it worked.

**Facilitator reminder:**

- This is not generic marketing copy. Keep it grounded in the demo, the customer problem, what changed, and what claims need verification.
- Strip customer-specific names, private data, and unapproved claims before anything is shared externally.

**Facilitator reminder:**

- Claude is a force multiplier for real work, not a replacement for critical thought.
- The participant remains the person deciding what is worth solving.

---
