# Responsible AI

> **Interaction rule:** Do not run this file end to end. Work with the user section by section. Ask clarifying questions, pause for their judgement, and treat the prompts as starting points to adapt, not scripts to execute blindly.

> **Before each copyable prompt block:** If the context is incomplete, ask 1-3 clarifying questions before producing output. After each major section, stop and ask what the user wants to challenge, refine, or change before continuing.

Use this chapter once the participant has a concrete AI-enabled idea or prototype direction. The goal is to use Responsible AI as a quick lens on the idea, not to build out a risk register. This is not a compliance sign-off, a full risk assessment, or a checklist.

The workshop exercise is a 15-minute conversation. Keep it scannable and judgement-led.

> **Reality check (runs all week):** one of the week's four recurring gut-checks — *"what breaks when it's wrong, and who pulls the plug?"* — is exactly this chapter's job. By the end the participant should be able to answer it for their idea: what the worst wrong output is, who would notice, and how a human intervenes or shuts it off.

---

## Exercise: Responsible AI Fit

**Time:** 15 mins

Start from the idea the participant is prototyping. Claude should ask short questions, one at a time, across four lenses.

- **Explainability** — Can you explain why it produced a given answer or decision?
- **Transparency** — Do users know AI is involved, and why it acted?
- **Fairness** — Could it serve some users better than others?
- **Safety** — What could go wrong if the output is wrong, incomplete, biased, misunderstood, or brittle?

**Mapping note:** For this short exercise, fold Privacy & Security and Veracity & Robustness into **Safety**. If sensitive data, model-boundary risk, hallucination, bad inputs, or edge cases are the important concern, surface them there.

**You are done when:**

- The participant has thought through the most important Responsible AI lens for their idea.
- They know whether one small design assumption needs attention before prototyping.
- They have not tried to solve every risk in the room.

---

## AI Prompt

Copy this prompt into Claude Code with the current use case or prototype idea.

```text
You are a Responsible AI facilitator helping me think about an AI-enabled product idea. Keep this as a short conversation, not a written assessment.

Here is the idea I'm prototyping:

[paste the idea, use case, or prototype summary]

Ask me short, sharp questions across these four lenses:

1. Explainability — can we explain why it produced a given answer or decision?
2. Transparency — do users know AI is involved, and why it acted?
3. Fairness — could it serve some users better than others?
4. Safety — what could go wrong if the output is wrong, incomplete, biased, misunderstood, or brittle?

Use this flow:

1. Ask one question at a time.
2. After each answer, briefly reflect back the implication in 1-2 sentences.
3. Move to the next lens only if it is useful. Skip anything that feels low relevance.
4. Do not solve the risks. Do not produce a checklist.
5. Keep the whole conversation moving so it fits inside 15 minutes.

Fold privacy/security, sensitive data, hallucination, bad inputs, edge cases, and robustness concerns into Safety if they matter for this idea.

Start with the lens most likely to matter for my idea. Ask your first question now.

At the end, give me a tiny recap with:
- the 1-2 watch-outs that matter most
- one thing I may need to change or check before prototyping
- one question to carry forward
```

---

## Save The Output If Needed

If the facilitator asks participants to save their work, use:

```text
Save a very short Responsible AI fit note to `workspaces/<my-name>/rai-fit.md`.

Include:

- The idea assessed
- The 1-2 most important watch-outs
- One design change or check before prototyping
- One question to carry forward

Keep it short enough to read before the next build block.
```

---

## Optional: Deeper Responsible AI Inventory

The main path is the 15-minute fit conversation above. This deeper inventory is **not part of the default flow** — the deck no longer runs it as a timed exercise, and you (Claude) must **not** start it on your own.

Run it only if the facilitator explicitly asks for it, or the participant explicitly requests it after the fit conversation — and even then, confirm before beginning. Do not drift into it just because an idea seems risky: surface the risk as a watch-out in the fit conversation and leave the decision to run the fuller inventory to the facilitator.

---

## Tips

- Keep the main exercise conversational: question, answer, quick reflection, next question.
- Focus on noticing watch-outs, not solving them.
- Explainability and transparency usually matter early because they shape the product experience.
- Safety is the umbrella for sensitive data, bad outputs, brittle behaviour, and edge cases in this short exercise.
- If ownership is unclear, capture it as an open question rather than turning the exercise into governance design.

---

**Done check:** The participant can name the 1-2 Responsible AI watch-outs that matter most for their idea, one design assumption they may need to check, and one question to carry forward.
