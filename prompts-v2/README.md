# Prompts v2

> **Interaction rule:** Do not run this file end to end. Work with the user section by section. Ask clarifying questions, pause for their judgement, and treat the prompts as starting points to adapt, not scripts to execute blindly.

This folder organizes the workshop prompts into larger agenda-based chapters, so you work by stage instead of treating every prompt as a checklist item.

Onboarding sits at the top level. Participant-facing workshop chapters are split into `day-one/` and `day-two/`. Internal test notes, gap analyses, and optional facilitator materials live in `_internal/`.

## Why this version exists

Prompt libraries can accidentally train people to copy and paste without thinking. This version is designed to do the opposite: each chapter asks Claude and the participant to slow down, ask questions, challenge outputs, and adapt the prompts to the business context.

## How to use these prompts

These chapters are thinking aids, not scripts to run. The value comes from your judgement — choosing the context, challenging the output, and deciding what is worth keeping.

- Read the section goal before copying any prompt.
- Paste one prompt block at a time, not a whole chapter.
- Fill in the bracketed context with specifics from your business.
- Ask Claude to point out weak assumptions, missing evidence, and generic output.
- Stop after each major output and decide what to keep, challenge, or change.
- Save only the distilled artifacts you will actually use later.

If you do paste a whole chapter into Claude Code, that is fine — Claude will not run it end to end. It will explain the goal, check your role and evidence, walk you through the first section, and pause. The chapter is a coaching guide, not a batch job. Claude adapts to your role and how comfortable you are: if the material is too easy, tell it and it will move faster; the rigor stays the same for everyone.

## Recommended flow

1. `00-onboarding.md`

Day 1:

1. `day-one/A-market-research.md`
2. `day-one/B-user-personas.md`
3. `day-one/C-problem-definition-hmw-jtbd.md`
4. `day-one/D-practical-product-management-with-ai.md`

Day 2:

1. `day-two/E-ideation.md`
2. `day-two/F-prototype-build-for-agentic-idea.md`
3. `day-two/G-responsible-ai.md`
4. `day-two/H-poc-build-for-handoff.md`

Standalone Day 2 prompt (not part of the A–H sequence):

- `day-two/mark-miller-evaluator.md` — Mark Miller, a tough commercial-reviewer persona. Run it once you have a proposal worth stress-testing, to check it can earn revenue, deepen workflow ownership, or defend the moat before the GM review.

This is a guide, not a script. Facilitators can skip, repeat, or reorder chapters based on what the team has already learned.

## Participant Map

| Chapter | Use when you have | You create | Minimum path |
|---|---|---|---|
| `00-onboarding.md` | Claude Code open in this repo | Your workspace folder and `participant-profile.md` | Paste the onboarding block once, then answer Claude step by step |
| `day-one/A-market-research.md` | Prework, customer/internal data, or web research questions | `insights.md` | Run market, customer, competitor, and internal scans; distill each into `insights.md` |
| `day-one/B-user-personas.md` | `insights.md` and customer evidence | `personas/*.md` | Create at least two evidence-backed personas and score/refine them |
| `day-one/C-problem-definition-hmw-jtbd.md` | Insights and personas | `jobs-to-be-done.md` if useful, `problem-statements.md`, `problem-stack-rank.md`, `hmw-questions.md` | Use the job lens, write 1-2 problem statements, stack-rank them the customer's way, then create HMW questions |
| `day-one/D-practical-product-management-with-ai.md` | A product artifact, demo, walkthrough, ticket, or repo context | Content drafts or reusable product-management prompt | Use Claude for practical product artifacts, especially demo-to-content, with a review loop |
| `day-two/E-ideation.md` | Problem statements and HMWs | `opportunity-areas.md`, `ideas.md`, `clusters.md` | Draft opportunity areas, generate ideas from three perspectives, then cluster them |
| `day-two/F-prototype-build-for-agentic-idea.md` | Idea clusters | `use-cases.md`, `use-cases/<short-name>.md` | Shape, score, commercially test, and persona-stress-test the top 1-2 agentic use cases |
| `day-two/G-responsible-ai.md` | A concrete AI use case | `rai-fit.md` | Surface the 1-2 Responsible AI watch-outs that should shape the design now |
| `day-two/H-poc-build-for-handoff.md` | A top use case and Responsible AI fit notes | `poc-scope.md`, prototype files, `poc-handoff.md` | Lock one idea, build a rough PoC, refine it, and capture handoff notes |
| `day-two/mark-miller-evaluator.md` (standalone) | A proposal-ready use case with evidence | A sharpened commercial case | Run the short intake first; Mark Miller pressure-tests whether it can earn revenue before the GM review |

Replace `<your-name>` or `<my-name>` with your actual workspace folder, for example `workspaces/priya-shah/`.

If you fall behind, keep these current before anything else: `insights.md`, one strong persona, one problem statement, and one use case.

The onboarding step creates `participant-profile.md`. Use it to remind Claude who is in the chair, what evidence they brought, and how comfortable they are with the tooling. The prompts should adapt to the participant's role without assuming that Product, Sales, Customer Success, Support, Engineering, or leadership has the whole truth.

## Working In Parallel

You do not have to wait for one Claude session to finish before starting useful independent work. Market, customer, competitor, and internal-data scans can run in separate Claude Code sessions/windows that you open yourself, then be brought together in `insights.md`.

Use parallel chats for independent research. Claude should tell you when this would help and what to paste in each session, but it cannot open extra sessions for you. Use one focused chat for judgement-heavy decisions: personas, problem statements, use-case selection, Responsible AI fit, and PoC handoff review.

## Slides Companion

Use the day-specific slides companion alongside the chapters:

- `day-one/1-slides-companion-day-one.md`
- `day-two/2-slides-companion-day-two.md`

They pull the weak/strong examples and facilitation checks from the Palm Beach deck into short read-along references participants and facilitators can keep open while they work.

## Facilitation principle

Every chapter should be treated as a conversation. Participants may paste a whole chapter or one block at a time. Claude should not assume the participant has read the whole markdown file, and should not execute the chapter as a batch job. It should explain the goal, check the participant profile and available evidence, work section by section, coach the participant to go deep enough, and pause before moving on. Before advancing, Claude should check whether the output is specific, evidence-backed, and worth keeping, and whether the facilitator has moved the room to the next exercise or the participant is ready to continue.
