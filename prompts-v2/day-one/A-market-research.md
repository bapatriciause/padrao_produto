# Market Research

> **Interaction rule:** Do not run this file end to end. Work with the user section by section. Ask clarifying questions, pause for their judgement, and treat the prompts as starting points to adapt, not scripts to execute blindly.

> **Before each copyable prompt block:** If the context is incomplete, ask 1-3 clarifying questions before producing output. After each major section, stop and ask what the user wants to challenge, refine, or change before continuing.

Use this chapter to help participants build evidence before they ideate. The goal is not to paste every prompt mechanically; the goal is to investigate market, customer, competitor, and internal signals, then decide which insights are strong enough to carry forward.

---

## Market research analysis

# Market Research

> **Workshop guide — not a prompt to run end-to-end.** Copy the fenced blocks one at a time into chat, modify for your context, and chat with the output between blocks.

<!-- workshop-guide: do-not-execute-end-to-end -->

Three short prompts, each a different angle on what's happening around your business. This is your first exercise of the day, so take a minute to get oriented before you dive in.

If you are less technical or new to Claude Code, run these one at a time in a single chat. Parallel work is a speed option, not a quality requirement. Claude cannot open extra sessions for you; if you want to work in parallel, open another Claude Code session/window yourself and paste the relevant scan there.

## Exercise (~20 mins, run in parallel)

The three scans (market, customer, competitive) are independent. If you are comfortable in Claude Code, open a separate Claude Code session/window for each prompt yourself and start them all at the same time. Answer clarifying questions as they come back, and you'll move through this exercise faster than running them one at a time. If running three at once feels like a lot, start with one, get a feel for the rhythm, then kick off the other two.

**For each prompt:**

1. Open a new Claude Code session/window yourself, or continue in the same chat if you are running the scans one at a time.
2. Paste the prompt and fill in the bracketed placeholders.
3. Chat with the output and challenge it as you go. Push back, ask for sources, dig deeper on anything that doesn't hold up.
4. When the research feels solid, paste in **Prompt 4** (at the bottom of this file) to distill the findings into a short list of insights. That list is what you save.

By the end you'll have a short, pointed list of insights about **where demand is heading** and **where you might be exposed**. These are the questions to bring forward into personas and ideation.

## What to save to your repo

Your goal is a short, pointed list of insights you can come back to, not pages of research you won't re-read.

- **Default:** keep one running `insights.md` file in your workspace folder (`workspaces/<your-name>/insights.md`). After each scan, ask Claude to update it with the new bullets. By the end of the morning you've got one file with everything worth knowing.
- **If you want more depth:** also save the full research output of each scan as `market-scan.md`, `customer-scan.md`, and `competitive-scan.md`. Useful if you'll come back to the raw research, optional otherwise.
- **Lightest version:** just keep `insights.md` in your workspace folder. Skip the detailed files.

The insights file is the one that matters. That's what feeds the rest of the workshop.

## A few orienting notes

**Tool note.** Use Claude Code for your research. It has web access for external research and can also analyse files in your repo, so it can read anything you've placed in `prework/`.

**If you have prework artifacts** (analyst reports, interview notes, competitor teardowns, internal strategy docs, sales call notes, demo objections, lost-deal notes, renewal risks, support tickets, implementation notes, CS notes, roadmap docs, usage exports, customer emails, or battlecards), share them with Claude or point it at `prework/`. The scans will use them first and fill gaps with public research.

**Use the evidence your role gives you, but label confidence honestly.** Sales objections, support tickets, CS renewal notes, implementation escalations, roadmap debates, usage patterns, and engineering constraints are all useful signals. Treat any one source as directional unless it is backed by customer interviews, support tickets, usage data, revenue data, direct customer quotes, or repeated patterns across multiple sources.

**If you arrived with little or no prework, you can still do this.** The market and competitor scans run on public web research, so you are not blocked. For the customer/internal analysis, use whatever you can dig up — a handful of support emails, your own notes from customer conversations — and where you have nothing, turn the exercise around: ask Claude "what are the most important questions I should be asking my customers?" and capture those as research to run after the accelerator. Mark anything that is your own assumption as an assumption. Do not ask Claude to invent customer data, and do not let a confident-sounding paragraph stand in for evidence you don't have. A short, honest `insights.md` with three real signals and some open questions beats a long one full of plausible fiction.

**New to GitHub terms?** Commit means save, push means upload, pull means download, repo is your folder of files. There's a Claude skill that handles this. Just say "save my work" or "back this up" and Claude will take care of it.

---

## Getting good output

**Push back.** The first pass is rarely the best. If a finding doesn't have evidence behind it, ask for sources. If something reads as generic, ask the model to make it specific or drop it.

**Verify spot-checks.** Click a couple of the source links to make sure they actually say what the model claims. AI models are confident even when they're wrong.

**Customize the prompts for your context.** If a prompt isn't producing what you need, modify it. Change the role, sharpen the mission, adjust the quality bar. Any of the four pieces (Role / Context / Mission / Quality bar) can be tuned to fit your VBU, segment, or geography.

---

## 1. Market Scan

What's changing in your market that creates opportunity or threat.

```
# Role
You are a market research analyst. You produce tight, evidence-based findings, not generic statements. You distinguish what is actually happening from what vendors and analysts claim is happening.

# Context
- Company: [NAME]
- Product: [WHAT IT DOES, WHO IT'S FOR]
- Market / category: [e.g., field service management software for HVAC contractors]
- Geography: [PRIMARY MARKETS]

# Mission
Tell me how my market is changing. I want the structural picture: what's shifting in technology, regulation, economics, and adjacent categories, and where value might be migrating. Specific competitors and specific customer pressures are being covered in separate scans, so don't focus there.

# Quality bar
- Cite a source for every claim. If you can't find evidence, leave it out.
- Concrete findings beat generic statements. Good: "Three of the top five vendors now ship agentic scheduling workflows." Bad: "The market is moving toward AI."
- Be skeptical of vendor marketing and analyst hype.

Start by asking me one or two clarifying questions if you need to focus the research. Then do a first pass and check in.
```

**Done ✓** When the back-and-forth feels solid, run **Prompt 4** to distill the insights and add them to your `insights.md` in your workspace folder (`workspaces/<your-name>/insights.md`). Then ask Claude to "save my work" so it's captured before you move on.

---

## 2. Customer Scan

Understanding your customers, their world, their priorities, and where they're struggling.

```
# Role
You are a research analyst. You build evidence-based pictures of customers in an industry, drawing on primary sources: earnings calls, annual reports, strategic plans, leadership interviews and podcasts, conference talks, job postings, industry publications, practitioner forums, review sites.

# Context
- Company: [NAME]
- Product: [WHAT IT DOES]
- Who I sell to: [a few examples: company type, size, geography, and which function in the org buys or uses it]

# Mission
Help me understand my customers. What's their world like right now? What are leaders at companies like theirs saying their priorities are? What is the function I sell into actually being asked to do this year? Where are they struggling? What language and framing do they use to talk about their problems?

# Quality bar
- Use primary sources and cite them. Verbatim quotes wherever you can find them.
- If you can't find evidence, leave it out. Don't infer, don't invent.
- Concrete findings beat generic statements. Good: "40% of operations leader job postings now require predictive maintenance experience." Bad: "Customers want more efficiency."

Start by asking me one or two clarifying questions if you need to focus the research. Then do a first pass and check in.
```

**Done ✓** When the back-and-forth feels solid, run **Prompt 4** to distill the insights and add them to your `insights.md` in your workspace folder (`workspaces/<your-name>/insights.md`). Then ask Claude to "save my work" before moving on.

---

## 3. Competitive Scan

Who else is in this space, with attention to who's new or coming from an unexpected angle.

```
# Role
You are a competitive intelligence analyst. You write blunt, specific notes, not feature-by-feature comparisons.

# Context
- Company: [NAME]
- Product: [WHAT IT DOES + WHO IT'S FOR]
- Competitors I already know about: [LIST WHAT YOU KNOW, OR LEAVE BLANK]

# Mission
Show me who else is in this space, with extra attention to who's new or coming from an unexpected angle. I want awareness of:
- The traditional competitors I'd expect to see
- New entrants and AI-native challengers
- Horizontal or adjacent players who could move into my space
- Build / in-house alternatives. What customers do if they don't buy from anyone, increasingly viable with AI

I don't need a deep feature teardown of each player. I want a clear map and a sharp eye on what's new, what's encroaching, and where you can see gaps no one is addressing well.

# Quality bar
- Cite a source for every claim.
- If you can't find evidence, leave it out.
- Concrete observations beat lists of features.

Start by asking me one or two clarifying questions if you need to focus the research. Then do a first pass and check in.
```

**Done ✓** When the back-and-forth feels solid, run **Prompt 4** to distill the insights and add them to your `insights.md` in your workspace folder (`workspaces/<your-name>/insights.md`). Then ask Claude to "save my work" before moving on.

---

## 4. Distill Insights

Paste this into each research thread once the back-and-forth is done. It tells the model to produce the insights bullet list you'll save to your `insights.md` file.

```
Take everything we've researched in this thread and distill it into a sharp list of insights I can add to my `workspaces/<my-name>/insights.md` file in this repo.

Add the insights under the appropriate heading in insights.md based on what we researched in this thread:
- Market scan → ## Market Trends
- Customer scan → ## Customers
- Competitive scan → ## Competitors

If the heading does not exist yet in insights.md, create it. If it does, append the new bullets to it.

Format each as:
- **[Concrete finding in one sentence]** [(source)](link). So what: [one line on why it matters for a product team]

Quality bar:
- Only insights that are specific and concrete. Drop anything generic.
- Only insights backed by a source link.
- If you're not sure something belongs, leave it out. I want signal, not volume.
```

---

**Done check:** You have `insights.md` saved to your workspace with sharp, sourced bullets across all three scans, organised under three headings: **Market Trends**, **Customers**, and **Competitors**. Each insight is concrete, evidence-backed, and ties to a decision a product team could make differently. (Optionally also `market-scan.md`, `customer-scan.md`, `competitive-scan.md` for deeper reference.)

---

## Customer analytics analysis

# AI Prompt: Customer Analytics Analysis

> **Workshop guide — not a prompt to run end-to-end.** Copy the fenced blocks one at a time into chat, modify for your context, and chat with the output between blocks.

<!-- workshop-guide: do-not-execute-end-to-end -->

Use these prompts to pull insights from your customer interviews, support tickets, NPS data, and usage analytics. The findings feed into the same running `insights.md` file you started in the market research exercise — customer voice from interviews joins the customer scan insights, and internal data analysis gets its own section so it doesn't crowd out forward-looking insights when you get to ideation tomorrow.

## What to save

Same pattern as market research: distill each analysis into your running `insights.md` in your workspace folder (`workspaces/<your-name>/insights.md`). The Distill prompt at the bottom routes findings to the right heading:

- **Customer Interview Analysis** → under the **Customers** heading (same place as market-research customer-scan insights)
- **Support Ticket / NPS / Usage / Challenge Your Thinking** → under the **Internal Data Analysis Insights** heading

Optionally save the full output of each analysis as a separate reference file in your workspace (`customer-interview-analysis.md`, `support-ticket-analysis.md`, `nps-analysis.md`, `usage-analysis.md`) if you want the raw work. The insights file is the one that matters.

## A note on running these

Run each prompt in its own chat. Different data, different contexts — keep them clean. Sequential is fine (no need to parallelise like market research).

**Skip any section where you don't have the data.** These are independent — you can do interviews only, internal data only, or whatever combination matches what your VBU has.

---

## 1. Customer Interview Analysis

Pull insights from your customer interview transcripts. These join the customer voice in your **Customers** section of insights.md alongside the market scan findings.

### Optional: clean up raw transcripts first

If your transcripts are raw (from a transcription service, with filler words and no structure), use this prompt first to clean them up. Skip if your transcripts are already organised.

```
I have a raw transcript from a customer interview. Please:

1. Clean up the transcript, remove filler words, fix grammar, but keep the customer's voice authentic
2. Organise it into the following sections:
   - Participant details (name/role/company/date)
   - Key pain points discussed
   - Feature requests or wishes
   - Quotes worth highlighting (verbatim)
   - Overall sentiment (positive, negative, mixed)
3. Summarise the top 3 takeaways in bullet points

Here is the transcript:
[PASTE TRANSCRIPT HERE]
```

Repeat for each transcript. Once you have 3+ structured interviews, move on to the analysis below.

### Interview Pattern Analysis

```
I have [N] customer interview summaries from users of [YOUR PRODUCT]. Please analyse them and provide:

1. **Common pain points**, ranked by frequency across interviews
2. **Common requests**, features or capabilities mentioned by multiple customers
3. **Sentiment patterns**, overall satisfaction trends
4. **Contradictions**, any areas where customers disagree or have conflicting needs
5. **AI opportunity areas**, based on the pain points and requests, where could AI add the most value?
6. **Strongest quotes**, the most compelling verbatim quotes for each theme

Here are the interview summaries:
[PASTE ALL SUMMARIES]
```

**Done ✓** When the analysis feels solid, run the **Distill Insights** prompt at the bottom of this file. It will add the key findings to your `workspaces/<your-name>/insights.md` under the **Customers** heading. Then ask Claude to "save my work" before moving on.

---

## 2. Internal Data Analysis

These prompts surface patterns from your internal data. Insights here go under the **Internal Data Analysis Insights** heading in `insights.md`, kept separate from the market-research-level insights so they don't crowd out forward-looking customer and competitor views when you reach ideation.

### Support Ticket Analysis

```
I have support ticket data from [YOUR PRODUCT]. Please analyse and provide:

1. **Top categories** — group tickets by theme and rank by volume
2. **Trending issues** — any categories growing over time?
3. **Resolution patterns** — which issues are quick to resolve vs. take a long time?
4. **Automation candidates** — which ticket types could be deflected or resolved by AI?
5. **Root causes** — what underlying product issues drive the most tickets?

Here is the data:
[PASTE DATA OR DESCRIBE THE FORMAT AND KEY FIELDS]
```

**Done ✓** When the analysis feels solid, run the **Distill Insights** prompt at the bottom. It will add the key findings to your `insights.md` under the **Internal Data Analysis Insights** heading. Then ask Claude to "save my work" before moving on.

### NPS / CSAT Analysis

```
I have NPS survey data for [YOUR PRODUCT]. Please analyse:

1. **Score distribution** — breakdown of Promoters, Passives, and Detractors
2. **Theme extraction** — what are the top themes in verbatim comments?
3. **Sentiment analysis** — categorise comments as positive, negative, or mixed
4. **Actionable insights** — what specific changes would move Detractors to Passives and Passives to Promoters?
5. **AI opportunities** — based on the feedback, where could AI improve the experience?

Here is the data:
[PASTE DATA]
```

**Done ✓** Distill into `insights.md` under **Internal Data Analysis Insights** via the Distill prompt below. Then ask Claude to "save my work".

### Usage Analytics Analysis

```
I have product usage data for [YOUR PRODUCT]. Please help me understand:

1. **Feature adoption** — which features are most/least used?
2. **User segments** — are there distinct usage patterns among different user types?
3. **Drop-off points** — where do users abandon workflows?
4. **Power user behaviours** — what do your most engaged users do differently?
5. **AI integration points** — where in the user journey could AI add the most value?

Here is the data:
[PASTE DATA OR DESCRIBE FORMAT]
```

**Done ✓** Distill into `insights.md` under **Internal Data Analysis Insights** via the Distill prompt below. Then ask Claude to "save my work".

---

## Natural stopping point

If you're tight on time, run the **Distill Insights** prompt at the bottom now and wrap up here. The "Challenge Your Thinking" prompts below are optional — useful if you want to surface less obvious patterns and pressure-test what the data is really telling you.

---

## 3. Optional: Challenge Your Thinking

The prompts above give you an organised view. These push you to question it. As you work through them, ask: *is this a forward-looking insight about a customer problem, or is it a backlog item about my current software?* Bug-fix-shaped findings belong in your backlog, not your insights.

### The Revenue Concentration Risk

```
Look at my customer and revenue data. Show me where concentration risk exists:

1. What percentage of revenue comes from the top 10 customers? Top 20?
2. If your biggest customer left tomorrow, what would the impact be?
3. Which customer segments are growing vs shrinking?
4. Are your most profitable customers also your most satisfied (by NPS/CSAT)? If not, why not?
5. Where is there a mismatch between customer size and support cost? (Big customers who cost a lot to support vs small customers who are self-sufficient)

I want the uncomfortable findings, not the reassuring ones.
```

**Done ✓** Distill the uncomfortable findings into `insights.md` under **Internal Data Analysis Insights** via the Distill prompt below. Then ask Claude to "save my work".

### The Support Ticket Iceberg

```
I have support ticket data. But tickets only capture problems that customers bother to report. Help me find the iceberg below the surface:

1. For every ticket category, estimate how many customers experience this problem but do NOT raise a ticket. (Hint: if 70% of support is by phone, your ticketing system understates the problem.)
2. Which issues correlate with customer churn? Do customers who raise [category] tickets leave at higher rates?
3. Which ticket categories represent a PRODUCT problem vs a TRAINING problem vs a DOCUMENTATION problem?
4. What would happen if you eliminated the #1 ticket category entirely? How much support cost would you save? How much would customer satisfaction improve?
5. Look at tickets from your longest-tenured customers. What are they STILL complaining about after years? These are the failures you have normalised.
```

**Done ✓** Distill into `insights.md` under **Internal Data Analysis Insights** via the Distill prompt below. Then ask Claude to "save my work".

### The "Nobody Uses That" Audit

```
Look at my feature usage data and identify:

1. Features with less than 10% adoption. For each one: was this a feature nobody wanted, or a feature nobody knows about?
2. Features that were used heavily at launch and declined over time. What happened?
3. Features that a small group of users love but most ignore. Are those users your most valuable segment, or an edge case?
4. The 3 features your product team is most proud of. Are they actually the most used? If not, why the disconnect?
5. What are users doing INSTEAD of using the features you built for that job?
```

**Done ✓** Distill into `insights.md` under **Internal Data Analysis Insights** via the Distill prompt below. Then ask Claude to "save my work".

---

## 4. Distill Insights (paste into each analysis thread once it's done)

```
Take everything we've found from this analysis and distill it into a sharp list of insights I can add to my `workspaces/<my-name>/insights.md` file in this repo.

Add the insights under the appropriate heading in insights.md based on what we analysed in this thread:
- Customer interview analysis → ## Customers
- Support ticket / NPS / usage / "Challenge Your Thinking" analyses → ## Internal Data Analysis Insights

If the heading does not exist yet in insights.md, create it. If it does, append the new bullets to it.

Format each insight as:
- **[Concrete finding in one sentence]** (evidence: [what data this is from]). So what: [one line on why it matters for product direction].

Quality bar:
- Only insights that are specific and concrete. Drop anything generic.
- Each insight should help understand a customer problem, pain point, or opportunity — something forward-looking. Drop anything that's just a complaint about a specific bug or current feature; those belong in your backlog, not your insights.
- Only insights backed by the data we analysed. Don't infer, don't invent.
- Speed is not validation. Producing an insight fast does not make it true, and an insight that only confirms what I already hoped or believed is the one to distrust most — flag it, label its confidence, and note the disconfirming evidence I'd need to check it.
- If you're not sure something belongs, leave it out. I want signal, not volume.
```

---

**Done check:** Your `workspaces/<your-name>/insights.md` now has insights from both the external market scans and your internal data analysis. The **Customers** section holds insights from the market scan and your customer interviews. The **Internal Data Analysis Insights** section holds findings from support/NPS/usage data and the optional challenge prompts. Each insight is concrete, evidence-backed, and points to a decision a product team could make differently — not a backlog item.

---

## Cross-cutting findings

# AI Prompt: Cross-Cutting Findings

> **Workshop guide — not a prompt to run end-to-end.** Copy the fenced blocks one at a time into chat, modify for your context, and chat with the output between blocks.

<!-- workshop-guide: do-not-execute-end-to-end -->

You've built `insights.md` this morning from market research (`01`) and customer analytics (`02`). Now look across everything you've gathered and surface what's worth pulling together: alignments, contradictions, and assumptions to challenge.

The output goes back into `insights.md` as a new section called **Cross-cutting findings**, so everything still lives in one file.

---

## Bring It Together

```
Read my `workspaces/<my-name>/insights.md` file. It has insights organised under four headings: Market Trends, Customers, Competitors, and Internal Data Analysis Insights.

Look across all four sections and tell me:

1. Where do findings align across headings? (e.g., a market trend that the customer interviews also surface, a competitive move that internal usage data confirms.)
2. Where do they contradict? (e.g., market research says one thing, customer interviews say another.)
3. Opportunities that sit at the intersection of external trends and internal data. Things you wouldn't see by reading any one section alone.
4. The three most important evidence-backed findings to brief leadership on, drawing from across all four sections.
5. Stay inside the bounds of the evidence already in insights.md. Don't invent a roadmap, business case, or product strategy unless I explicitly ask for that next.

Add a new section to insights.md called `## Cross-cutting findings` and write your answers under it. Cite which heading(s) each cross-cut draws from.
```

## Contradiction Finder

When the synthesis above feels too neat, push harder:

```
Look at the insights in workspaces/<my-name>/insights.md again. Find the contradictions I am glossing over:

1. Where does my customer feedback (under Customers) say one thing but my usage data (under Internal Data Analysis Insights) say another?
2. Where do market trends paint a rosy picture that the internal data contradicts?
3. What is my internal narrative about competitive position, and what does the evidence under Competitors actually show?
4. Where am I selectively citing evidence that supports what I already believe?
5. What is the single finding I am most tempted to ignore? Why?

Append a sub-section called `### Contradictions to sit with` under the existing Cross-cutting findings section. Do not reassure me. Surface the tensions.
```

**Done ✓** Ask Claude to "save my work" so the new Cross-cutting findings section in `workspaces/<your-name>/insights.md` is captured before you move on.

---

**Done check:** Your `workspaces/<your-name>/insights.md` now has a Cross-cutting findings section at the bottom, surfacing alignments, contradictions, and assumptions to challenge across the morning's research. You can name the three most important insights from this morning.

---

## Recurring market research agent

# Recurring Market Research Agent

> **Workshop guide — not a prompt to run end-to-end.** Copy the fenced blocks one at a time into chat, modify for your context, and chat with the output between blocks.

<!-- workshop-guide: do-not-execute-end-to-end -->

Set up a weekly agent that does market research on a cadence and delivers a brief you can act on. Do this during Day 1 if you have time, or come back to it after the workshop. Both are fine. The point is to leave with something that keeps running without you.

## Choose your path

Two ways to set this up. Both produce similar weekly briefs. Pick the one that fits how you work.

| | Claude Code Routines | Claude Cowork |
|---|---|---|
| Runs on | Your local machine via Claude Code | Anthropic's infrastructure (web) |
| Web research | Yes | Yes |
| Local file access | Yes (reads files in your repo or folder) | No (upload files into a Project instead) |
| Setup | Requires Claude Code Desktop | Easier, no install |
| Best for | "Read my files too, give me a tailored brief" | "Just give me a web-research brief" |

You can switch later. The agent prompt is portable between both.

---

## Option A: Claude Code Routines (10 mins)

### 1. Open Claude Code Desktop

Open the **Routines** panel in the sidebar and click **New Routine**.

### 2. Configure the routine

- **Name:** Weekly Market Research Agent
- **Repo or folder:** attach any local folder with context you want the agent to read (workshop outputs, competitor research, strategic docs). Skip this if you want a web-only brief.
- **Connectors:** enable web search. Also enable a delivery connector (Slack, Gmail, Drive) so the brief lands in front of you on Monday morning instead of sitting in a folder.
- **Environment:** default is fine unless the agent needs domains outside Anthropic's trusted network list

### 3. Paste the agent prompt (below) into the Instructions field

Customize the bracketed fields before saving.

### 4. Save the prompt as a repo file

If you attached a folder, commit the prompt to it as `weekly-market-research-agent.md`. The routine is the trigger; the markdown file is the durable asset.

### 5. Add a schedule trigger

In the **Select a trigger** section:

- Trigger type: **Schedule**
- Frequency: **Weekly**
- Day/time: **Monday 8:00 AM** (local, auto-converts to UTC)

### 6. Test before activating

Click **Run Now** for a manual test run. Verify connectors authenticated and output landed where you wanted it. Iterate on the prompt until the test run reads clean.

### 7. Activate

Toggle the routine active. Assign a review owner who reads each Monday's brief.

**CLI shortcut:** inside any Claude Code session, run `/schedule weekly market research at 8am Monday`. Manage with `/schedule list`, `/schedule update`, `/schedule run`.

---

## Option B: Claude Cowork (10 mins)

### 1. Open Cowork and create a Project

Create a Project for your recurring research (e.g. "Weekly Market Research"). Upload any context you want the agent to use. This could be workshop outputs (`insights.md`, scan files, personas), competitor lists, your strategic plan, or nothing at all if you want a purely web-based brief.

### 2. Create a scheduled task

Open the Project → Scheduled tasks → New task. Configure:

- **Name:** Weekly Market Research Agent
- **Cadence:** Weekly, Monday 8:00 AM (or whenever fits your week)
- **Connectors:** enable web research. Also enable a delivery connector (Slack, Gmail, Drive) so the brief lands in front of you on Monday morning instead of sitting in a Project folder.

### 3. Paste the agent prompt (below) into the task

Customize the bracketed fields before saving.

### 4. Save the prompt as a Project file

Save it as `weekly-market-research-agent.md` in the Project. The schedule is the trigger; the markdown file is the durable asset you can fork and reuse.

### 5. Activate the schedule

Confirm the cadence and let it run. Assign a review owner who reads each Monday's brief.

---

## Personalize the agent

The base prompt below is intentionally generic. The value comes from what you customize. Before saving it, swap in details that make the weekly brief useful for your VBU:

- **Competitors to watch.** Name 3-5 specific competitors.
- **Sources you trust.** Publications, analysts, newsletters, or sites you'd actually cite in a leadership meeting.
- **Customer segments.** Be specific about who you sell to (company size, geography, vertical, buyer type).
- **Internal context.** Your current strategic bets, roadmap themes, areas of investment.
- **What "useful" looks like.** What would you actually act on? Pricing moves? AI launches? Regulatory shifts? Feature adoption trends? M&A?

Don't skip this. A generic agent produces generic briefs. A specific agent produces signal.

---

## Agent prompt (paste into the scheduled task or routine)

```
You are my recurring market research agent.

# Context
- Company: [NAME]
- Product: [WHAT IT DOES, WHO IT'S FOR]
- Strategic focus this year: [KEY BETS / THEMES]
- Competitors to watch: [3-5 NAMES]
- Customer segments I care about: [BE SPECIFIC]
- Sources I trust: [PUBLICATIONS, ANALYSTS, NEWSLETTERS]
- What I'd act on: [PRICING MOVES / AI LAUNCHES / REGULATORY SHIFTS / FEATURE ADOPTION / M&A]

# Your job
Every week, research changes in our market that could affect product direction, revenue opportunities, or competitive risk.

# Track
1. Industry and market shifts
2. Competitor moves
3. New AI/product capabilities
4. Customer pressures
5. Regulatory, economic, or operational shifts
6. Adjacent industry examples worth borrowing from

# Use
- Web research
- Whatever context I've provided above or attached
- Prior weekly briefs you've produced (so you can track what's changed)

# Output
Create a markdown file named `market-brief-[YYYY-MM-DD].md` with this structure:

## Bottom line
A few sentences a product leader could skim before deciding whether to read the rest.

## What changed in the market
Insights in this format, or "Nothing material this week":
- **[Concrete finding in one sentence]** [(source)](link). So what: [one line on why it matters for our product].

## Competitor moves
Same format. Report what's worth knowing, or "Nothing material this week".

## Customer pressure signals
Same format. Report what's worth knowing, or "Nothing material this week".

## To dig into next week
Open questions, weak signals worth watching, things that need more evidence.

# Quality bar
- Never invent. If you cannot find evidence for a claim, leave it out. Better to say "Nothing material this week" than to fill space with speculation or hedged language.
- Cite a source link for every claim. If a claim has no source, drop it.
- Concrete findings beat generic statements.
- Report what is worth knowing, not what fills a quota. If only one thing is worth flagging, flag one thing. If nothing changed in a section, say so.
- Separate confirmed evidence from inference. Flag weak sources.
- Enough detail to be readable by a product leader at a glance.
```
