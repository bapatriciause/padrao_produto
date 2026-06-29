# PoC Build For Handoff

> **Interaction rule:** Do not run this file end to end. Work with the user section by section. Ask clarifying questions, pause for their judgement, and treat the prompts as starting points to adapt, not scripts to execute blindly.

> **Before each copyable prompt block:** If the context is incomplete, ask 1-3 clarifying questions before producing output. After each major section, stop and ask what the user wants to challenge, refine, or change before continuing.

Use this chapter after ideation, agentic prototype shaping, and Responsible AI fit. The goal is to lock one idea, build a rough but understandable PoC, and leave with something the team can show, critique, and hand to developers.

This is not about polish. Broken is fine. Confusing is not.

---

## 1. Lock Your Top Idea

**Time:** 30 mins

Use this before opening a blank prototype. The output should be a one-sentence scope and the one thing the PoC must prove.

> **Reality check (runs all week):** before committing to a build, run the four recurring gut-checks on the locked idea one last time — who pays and what it displaces; is it still the customer's #1 problem, not your 5th; would a real customer react or just nod; and, for an agentic PoC especially, *what breaks when it's wrong and who pulls the plug.* If the idea can't survive these, fix the idea before you build the prototype.

```text
I need to lock my top idea before building a PoC.

Read my workspace files:

- `workspaces/<my-name>/problem-statements.md`
- `workspaces/<my-name>/problem-stack-rank.md` if it exists
- `workspaces/<my-name>/hmw-questions.md`
- `workspaces/<my-name>/ideas.md`
- `workspaces/<my-name>/clusters.md`
- `workspaces/<my-name>/use-cases.md`
- `workspaces/<my-name>/use-cases/<short-name>.md` if I have a top use case file
- `workspaces/<my-name>/rai-fit.md` if it exists

Help me decide whether my top use case is still the right one to build.

Ask me one question at a time where judgement is needed. Do not make the decision for me.

Pressure-test:

- Does this solve the top-ranked customer problem?
- What did persona or use-case stress-testing reveal that the idea does not yet reflect?
- If I showed this to the target persona right now, what would confuse them?
- What is the strongest version I can have ready by the end of today?
- What is the one thing the PoC must prove?

Then produce:

- One-sentence PoC scope: who it is for, what it does, and how we know it works
- The one thing the PoC must show
- The top 2-3 things to leave out for now
- The biggest open question for tomorrow's build/handoff

Save this to `workspaces/<my-name>/poc-scope.md`.
```

**Done check:** The participant can pitch the PoC in one sentence and name the one thing it must show.

---

## Before you build: commercial check — revenue is the gate

Run this the moment the idea is locked, before you open a prototype (deck: "BEFORE YOU BUILD"). In the agentic lane you sell the work itself, not a screen — so the value is the labour and workarounds the agent removes. **No concept advances to build or demo without an answer to all three:**

- **Who pays?** Name the budget owner whose labour line shrinks when the agent does the work — a real person, not "the customer."
- **What does it displace?** The people-time, tool, or workaround that goes away. Anchor it to the ~$6 of labour : $1 of software split.
- **A price that survives a CFO.** A number and a model where the value dwarfs the cost of running the agent.

```
Here is my locked idea: [paste]. Play a sceptical CFO and attack my commercial case.

Ask me one question at a time:
1. Who exactly pays, and whose budget or labour line does it come from?
2. What people-time, tool, or workaround does it remove — and roughly what is that worth (anchor to labour cost vs software cost)?
3. What price and model would you actually sign off, and where does the value dwarf the cost of running the agent?

Be hard on weak answers. If I can't name a buyer, a displacement, and a defensible price, tell me the idea isn't ready to build — and what I'd need to find to make it ready.
```

If you can't answer all three, fix the idea (or pick a stronger one) before building. This is the same commercial gut-check that recurs all week — here it is a hard gate, not a nice-to-have. (The deeper version is Mark Miller, Step 5.)

"I don't know yet" is a legitimate answer — capture it as an open question to resolve, not a failure to hide. The gate exists to sharpen the commercial case and surface what's still unknown, not to punish honest uncertainty. A captured "we don't yet know who pays" is a real output; a confident made-up buyer is not.

---

## 2. Build The PoC

**Time:** 90 mins

Use this to build a rough working prototype that makes the idea real enough to react to. Rough is fine, and ambition is fine — as long as it stays a throwaway front end (see the scope note in the prompt).

```text
Build a working HTML prototype for this PoC scope:

[paste the one-sentence PoC scope from `poc-scope.md`]

Use my persona, problem statement, and use case files as context. If you need to inspect files, read:

- `workspaces/<my-name>/poc-scope.md`
- `workspaces/<my-name>/personas/`
- `workspaces/<my-name>/problem-statements.md`
- `workspaces/<my-name>/use-cases/<short-name>.md`
- `workspaces/<my-name>/rai-fit.md` if it exists

Build the front end that brings the idea to life — one screen or a few linked screens, whatever the story needs. Use realistic sample data. Make it look real enough that a user could react to it.

Prototype the thing that does the job — the agentic move, not another dashboard. Make the agent's reasoning visible in the UI (show it doing the work and why it acted), and include the human-in-the-loop approval step where one belongs.

Fake the magic. You are mocking the agentic concept, not building working AI or real integrations — in a mock, anything is possible, so show the boldest version of the agent doing the job and push the limits. Keep it a throwaway prototype, not the real product: flat HTML with faked data and plumbing — no database, no login or authentication, no real backend, no production polish. Build as many flat screens as the idea needs, but spend the time proving the one thing it must show, not engineering the rest.

When the first version is ready:

- Tell me where to open it
- Explain what the prototype is meant to prove
- Ask me what feels confusing, missing, or overbuilt
```

---

## 3. Refine Against The Weakest Persona

Use this after the first version opens.

```text
Critique this prototype against my weakest or most skeptical persona.

Focus on:

- Would they understand what this does in a few seconds?
- Does it solve the problem they actually care about?
- What would confuse them?
- What important need did I miss?
- What should I fix with the time left?

Give me the top 3 changes only. Then wait while I choose what to change.
```

---

## 4. Capture The Handoff Notes

Use this at the end of the build block.

```text
Create a short handoff note at `workspaces/<my-name>/poc-handoff.md`.

Include:

- What the PoC does
- Who it is for
- What problem it solves
- What the prototype proves
- What is fake or placeholder
- What should be built next
- Open questions for developers, product, or customer validation

Keep it concise. This is for tomorrow's team handoff, not a full specification.
```

---

## 5. Last gut-check: run it past Mark Miller

This is the closing move of Day 2. Once the PoC and handoff notes exist, pressure-test the commercial case with **Mark Miller** — the standalone commercial-reviewer evaluator at `prompts-v2/day-two/mark-miller-evaluator.md`. It asks the question the prototype can't: can this actually earn revenue, deepen workflow ownership, or defend the moat?

Don't read the full evaluator first — start with the short intake at the top of that file and let Mark Miller interview you. Point it at your `poc-scope.md`, `poc-handoff.md`, problem statement, and use case for context.

Optional but recommended: a strong-looking PoC that can't survive Mark Miller is a signal to sharpen the commercial story now, before the handoff — not after.

---

**Done check:** The participant can demo the prototype in 60 seconds, explain the problem it solves, name the persona it serves, point to `poc-handoff.md` for the next build conversation, and — if they ran it — knows what Mark Miller flagged about the commercial case.
