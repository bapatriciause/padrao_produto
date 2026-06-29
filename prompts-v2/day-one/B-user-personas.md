# User Personas

> **Interaction rule:** Do not run this file end to end. Work with the user section by section. Ask clarifying questions, pause for their judgement, and treat the prompts as starting points to adapt, not scripts to execute blindly.

> **Before each copyable prompt block:** If the context is incomplete, ask 1-3 clarifying questions before producing output. After each major section, stop and ask what the user wants to challenge, refine, or change before continuing.

Use this chapter after participants have evidence in `insights.md`. The goal is to build grounded, distinct personas that can later challenge product decisions, not generic sales archetypes.

---

## Build personas

# Phase 1: Build Your Personas (20 min)

> **Workshop guide — not a prompt to run end-to-end.** Copy the fenced blocks one at a time into chat, modify for your context, and chat with the output between blocks.

<!-- workshop-guide: do-not-execute-end-to-end -->

> **⚠️ One persona per document.** Create a separate markdown file for each persona in your workspace using the template in `templates/persona.md` (e.g. `workspaces/<your-name>/personas/persona-fleet-manager.md`).

> **Ground rule:** Insights first, ideas later. Each persona should represent a genuinely distinct user type with different motivations, different realities, and different needs. If two personas would lead to the same product decisions, merge them.

> **Buyer is not always user.** Some participants may have strong evidence about buyers, budget holders, executives, implementation teams, support teams, or technical admins. Capture that context, but do not let it replace the day-to-day user persona. If the buyer, admin, influencer, and user are different people, name them separately.

> **No interview data? Mark it provisional — don't invent it.** If you have little or no direct evidence for a persona, build a provisional one from what you do have, label it clearly, and write a one-line DATA GAP note (see Step 3c) rather than letting Claude fill the gaps with confident detail. A persona explicitly marked "provisional, needs validation" is worth far more than a polished fiction you can't trace to evidence.

Start with `workspaces/<your-name>/insights.md`. That's the consolidated view of patterns from your market research and customer analytics this morning. The **Customers** section and **Cross-cutting findings** are the most directly relevant for personas.

But `insights.md` is filtered — it holds the observations we pulled out as relevant to product direction. Personas need more than that. Read your raw customer interviews in `prework/customer-interviews/` for the deeper details that didn't make it into insights: how customers actually talk, the workarounds they don't flag as "pain points" but live with daily, the quotes worth carrying forward, the texture of their day.

Look for clusters across the interviews. Which interviewees share similar realities, frustrations, or motivations? Those clusters become your personas.

Consider:
- What are they trying to accomplish in their role and their world?
- What pressures or constraints shape their decisions?
- What are your users' primary goals when using your product?
- How do they interact with your product and what workarounds do they use?
- What do they care about most: price, speed, quality, support?
- What are their biggest frustrations or pain points?
- Where does what users SAY contradict what they DO?

### Persona Generation Prompt

```
I need to create a detailed customer persona for [YOUR PRODUCT]. This persona should be realistic enough that an AI can convincingly simulate a conversation as this person.

Use two sources together:

1. `workspaces/<my-name>/insights.md` — for the organised observations from market research and customer analytics. Pay particular attention to the **Customers** section, **Cross-cutting findings**, and the customer pain points surfaced in the morning's work.
2. `prework/customer-interviews/` — for the raw transcripts. Read these for verbatim quotes, full context, communication style, workarounds, and the deeper details about how customers actually live and work. The transcripts hold nuance that insights.md deliberately filtered out.

**Product:** [YOUR PRODUCT]
**Industry:** [INDUSTRY]
**Typical user roles:** [e.g. Fleet Manager, Compliance Officer]

Review the interviews and identify a cluster of people who share a common reality. Build one composite persona from that cluster, following the structure in templates/persona.md. Include:
1. Which interviews this persona draws from and what pattern unites them
2. The realities they navigate in their day-to-day work, not just within our software
3. Core motivations: what they are trying to accomplish
4. Key pain points grounded in real data, not assumptions
5. Workarounds and coping strategies
6. How they make decisions
7. Use the empathy map format: SAYS / THINKS / FEELS / DOES
8. External pressures from the broader market that show up in their day-to-day (use the Market Trends and Cross-cutting findings sections of insights.md as context)
9. Verbatim quotes from the interviews
10. Communication style: how they talk, express frustration, and push back

IMPORTANT: Describe the persona from their perspective, not yours. Generate one persona only. Save it as a new markdown file in workspaces/<my-name>/personas/.
```

**Done check:** You have at least 2 personas in `workspaces/<your-name>/personas/`, each in its own markdown file following `templates/persona.md`. Each persona traces back to specific interviews and has been critiqued. You can name at least 1 assumption that was challenged by the data. Ask Claude to "save my work" to back up the new personas.

---

## Persona scoring and refinement

# Personas: Scoring and Refinement

> **Workshop guide — not a prompt to run end-to-end.** Copy the fenced blocks one at a time into chat, modify for your context, and chat with the output between blocks.

<!-- workshop-guide: do-not-execute-end-to-end -->

Use this rubric to evaluate the quality and completeness of user personas generated during the accelerator. Score each persona individually, then assess the set as a whole.

---

## The 5-Criteria Scoring System

Rate each persona on the following 5 criteria using a 1-5 scale.

### 1. User-Driven (Weight: High)

Is the persona defined by who the user actually is in their world, or by how the company views them?

| Score | What it looks like |
|---|---|
| 1 | Entirely assumed. No connection to research, interviews, or data. Reads like a marketing segment. |
| 2 | Mostly assumed with superficial references to research. "Based on our interviews" but no specifics. |
| 3 | Some evidence-backed elements, but key attributes are assumed or generic. Mix of real and invented. |
| 4 | Mostly evidence-backed. Quotes, data points, or research findings support the main attributes. |
| 5 | Strongly evidence-backed. Every key attribute ties to specific research, interview quotes, analytics, or support data. Sources are cited. |

### 2. Specificity (Weight: High)

Is the persona specific enough to drive product decisions, or is it a generic archetype?

| Score | What it looks like |
|---|---|
| 1 | Could describe anyone in the industry. No specific context, constraints, or behaviours. |
| 2 | Some specificity but reads like a job description rather than a real person. |
| 3 | Reasonably specific. Has named pain points and goals but lacks situational detail. |
| 4 | Specific. Includes concrete workflows, tools used, constraints faced, and decisions made in a typical week. |
| 5 | Highly specific. You can picture this person's Tuesday morning. Named tools, specific frustrations, concrete examples of workarounds they use today. |

### 3. Distinctiveness (Weight: Medium)

Is this persona clearly different from the other personas in the set?

| Score | What it looks like |
|---|---|
| 1 | Indistinguishable from another persona in the set. |
| 2 | Nominally different (different job title) but same needs, behaviours, and pain points. |
| 3 | Different role and some different needs, but significant overlap in what they want from the product. |
| 4 | Clearly distinct. Different goals, different daily workflows, different relationship with the product. |
| 5 | Entirely distinct. Represents a genuinely different perspective, use case, or value proposition. Would drive different product decisions. |

### 4. Actionability (Weight: High)

Can you make product decisions based on this persona? Does it tell you what to build and what to skip?

| Score | What it looks like |
|---|---|
| 1 | No actionable information. Cannot determine what this person needs from the product. |
| 2 | Vague needs stated but no clear product implications. |
| 3 | Some actionable elements. You could derive a few user stories but would need to make many assumptions. |
| 4 | Clearly actionable. Pain points map to features. Goals map to outcomes. Constraints map to requirements. |
| 5 | Highly actionable. You could write user stories, prioritise a backlog, and make trade-off decisions directly from this persona. Includes decision criteria and what "good enough" looks like for this user. |

### 5. Data Grounding (Weight: Medium)

Is the persona connected to measurable reality — usage data, support tickets, revenue data, market size?

| Score | What it looks like |
|---|---|
| 1 | No quantitative grounding. All qualitative assumptions. |
| 2 | Mentions data categories (e.g. "uses the system daily") but no specifics. |
| 3 | Some data points included but not well-integrated into the persona narrative. |
| 4 | Good data grounding. Includes usage patterns, segment size, revenue relevance, or support frequency. |
| 5 | Strongly data-grounded. Quantified behaviours, linked to analytics, segment sizing included, revenue impact estimated. Data and narrative reinforce each other. |

---

## Step 1: Score each persona

Use this prompt to have AI score a persona. Run it once per persona.

```
You are a product strategy advisor who specialises in user research for vertical software companies. I am going to share a persona I have built from customer interview data. Evaluate it rigorously.

Default to skepticism. Most personas built from thin or partial data sit in the low-to-mid teens. A total above 20/25 usually means you are scoring too generously — re-check each high score against the actual evidence and push inflated scores back down. It is more useful to me to know where this persona is weak than to be told it is strong.

Score this persona on these five criteria using a 1-5 scale:

1. USER-DRIVEN: Is this persona defined by who the user actually is in their world, or by how the company views them? A 5 describes the user's realities and context. A 1 reads like a sales segment.

2. SPECIFICITY: Are motivations and pain points grounded in evidence, or generic? A 5 traces each point to real signals. A 1 could apply to any software user.

3. DISTINCTIVENESS: Would this persona lead to different product decisions than other personas? A 5 means yes. A 1 means they are minor variations.

4. ACTIONABILITY: Could a product team use this to decide what to build? A 5 means yes. A 1 is descriptive but not decision-useful.

5. DATA GROUNDING: Is this built from evidence or intuition? A 5 connects to specific data. A 1 was likely guessed.

Also assess: Is the underlying data strong enough to support this persona? Flag areas where data seems thin, contradictory, or missing.

For this persona: all five scores, total out of 25, biggest strength (one sentence), biggest gap (one sentence).

Format as a scorecard.

**Persona to score:**
[PASTE PERSONA]

**Other personas in the set (for distinctiveness comparison):**
[PASTE OTHER PERSONA NAMES AND BRIEF DESCRIPTIONS]
```

After running the prompt for each persona, fill in the individual scorecard below.

### Individual Persona Scorecard

Use this format for each persona:

```
## Persona: [NAME — ROLE]

| Criteria | Score (1-5) | Evidence / Rationale |
|---|---|---|
| User-Driven | | |
| Specificity | | |
| Distinctiveness | | |
| Actionability | | |
| Data Grounding | | |
| **Total** | **__/25** | |

**Strengths:**
- [What this persona does well]

**Weaknesses:**
- [Where this persona falls short]

**Recommendation:**
- [Specific actions to improve this persona]
```

---

## Step 2: Assess the persona set as a whole

After scoring each persona individually, evaluate the set as a whole.

### Coverage Check

```
Evaluate this set of personas as a complete collection:

1. **Segment coverage:** Do these personas represent the key user segments for [PRODUCT AREA]? Who is missing?
   - Decision makers (buyers, budget holders)
   - Daily operators (hands-on users)
   - Affected parties (people impacted by the product but who don't use it directly)
   - Technical stakeholders (IT, integration, support)

2. **Merge candidates:** Are any two personas so similar that they should be combined? If yes, which ones and what would the merged persona look like?

3. **Missing personas:** Based on the research, is there a user type that clearly matters but has no persona? Identify up to 2 missing personas and describe who they are.

4. **Balance:** Is the set balanced across seniority levels, technical ability, and relationship with the product? Or is it skewed toward one type of user?
```

### Set Scorecard

```
## Persona Set Assessment

| Dimension | Rating | Notes |
|---|---|---|
| Segment coverage | Complete / Gaps / Major gaps | |
| Distinctiveness across set | Strong / Moderate / Weak | |
| Merge candidates | None / 1 pair / Multiple pairs | |
| Missing personas | None / 1 / 2+ | |
| Decision-making utility | High / Medium / Low | |

**Missing persona(s):**
- [Describe any personas that should be added]

**Merge recommendation:**
- [Describe any personas that should be combined]

**Overall set quality:** __/5
```

---

## Step 3: Strengthen weak personas

If a persona scores below 15/25, don't try to patch it. Go back to the source material.

**3a:** Ask AI what's missing:

```
This persona scored [X]/25. The weakest areas were [LIST]. Looking at my interview data and research, what specific evidence exists that I haven't used? What questions should I have asked in interviews that I didn't? Be specific about what data would raise each score by 1-2 points.
```

**3b:** If the data genuinely doesn't exist:

```
I don't have enough data to strengthen this persona. Based on what I DO have, should I:
a) Merge this persona with another one that has stronger evidence?
b) Keep it as a hypothesis and note exactly what data I'd need to validate it?
c) Drop it entirely and focus on personas where the evidence is strong?

Help me decide. What would a rigorous product team do?
```

**3c:** Note the gap honestly in your persona file:

> "DATA GAP: This persona's decision-making process is assumed, not evidenced. We need 2-3 more interviews with [role] to validate. Scheduled for [date] or flagged as post-accelerator follow-up."

Honesty about weak evidence is worth more than confident fiction.

---

## Step 4: Rescore

Run the scoring prompt again for any personas you strengthened. If a persona still can't improve, note what data you'd need to collect after the accelerator.

---

**Done check:** Your updated personas are in your workspace with improved scores. Ask Claude to "save my work" to back up the refined versions. You can name at least one assumption that was challenged and one gap you filled from the data.
