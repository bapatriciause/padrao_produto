# Practical Product Management With AI

> **Interaction rule:** Do not run this file end to end. Work with the user section by section. Ask clarifying questions, pause for their judgement, and treat the prompts as starting points to adapt, not scripts to execute blindly.

> **Before each copyable prompt block:** If the context is incomplete, ask 1-3 clarifying questions before producing output. After each major section, stop and ask what the user wants to challenge, refine, or change before continuing.

Use this chapter for the Day 1 practical product-management block. The goal is to show participants that Claude can turn real product work into usable artifacts, but that quality comes from the return loop: give context, inspect the output, then tell Claude what to improve.

---

## The Loop: Prompt, Output, Return

Every useful Claude session has three moves:

- **Prompt:** give Claude context, source material, goal, and quality bar.
- **Output:** let Claude produce a draft artifact.
- **Return:** inspect the draft and tell Claude what to improve.

The return is where the quality comes from. Do not treat the first answer as finished.

Examples:

- A Jira ticket plus GitHub code becomes a customer-ready setup guide.
- An existing importer plus the codebase becomes a PoC browser extension and a scoped SOW.
- A skill output plus the sandbox becomes a walkthrough script for a customer meeting.
- A recorded demo walkthrough becomes blog, LinkedIn, release notes, customer email, or internal update content.

---

## Demo To Content

Use this after you have a rough feature, prototype, walkthrough, or demo artifact. The goal is to turn what you built into clear external or internal content without losing the product story, customer problem, or evidence.

Workshop timing:

- **5 mins:** record a 3-5 minute walkthrough.
- **25 mins:** draft and refine content with Claude.
- **10 mins:** turn the repeatable approach into a reusable skill or prompt.

### Participant Prompt

Paste this into Claude with the transcript, finished artifacts, and examples of your usual writing.

```text
You are my product content partner. Help me turn a short product demo walkthrough into publish-ready content.

I am attaching or pointing you to:

- A transcript of me walking through [feature/prototype/use case]
- Any finished artifacts from the build: screenshots, prototype files, specs, notes, demo script, or repo files
- Examples of content I normally make: blog posts, LinkedIn posts, release notes, customer emails, sales notes, or internal updates

Your job is to turn the demo into useful content that keeps the product story accurate and specific.

First, ask only the 1-3 questions you genuinely need. If the materials are enough, make reasonable assumptions and start.

Use this process:

1. Understand the demo
   - What customer problem does it solve?
   - Who is it for?
   - What changed because of the accelerator work?
   - What proof, artifact, or demo moment makes it credible?

2. Protect the content
   - Strip customer-specific names, confidential details, private data, credentials, and anything that sounds like an unapproved claim.
   - Replace sensitive names with neutral descriptions.
   - Flag anything I should confirm before sharing externally.

3. Match my voice
   - Read my examples and mirror the structure, tone, length, and level of detail.
   - Tell me briefly what patterns you are copying before drafting.

4. Fit the business story
   - Use the company/product context I provide or files in this repo.
   - If web research is available, check the company/product and main competitors.
   - If web research is not available, use the materials I provided and ask me what competitor or market context matters.
   - Make the angle stronger than a generic "we used AI" story. Anchor it in the customer problem, product value, speed of learning, and what changed.

5. Draft the content
   Produce only the formats I ask for. If I do not specify formats, suggest a sensible short set and ask me to choose before drafting:
   - LinkedIn post
   - Short blog post
   - Release note
   - Customer email
   - Sales enablement note
   - Internal update

For each draft, include:

- Suggested title or hook
- Draft body
- What source material it used
- Any claims I should verify before publishing

After the first draft, stop. Ask me what to keep, cut, sharpen, or change before you revise.
```

---

## Optional: Make This Repeatable

After the drafts are useful, turn the workflow into a reusable team prompt.

```text
Turn the content workflow we just used into a reusable prompt for my team.

It should tell future users:

- What inputs to provide
- What sensitive information to remove
- How to describe the audience and channel
- How to include tone examples
- How to ask for blog, LinkedIn, release note, customer email, sales note, or internal update outputs
- How to force a review pause before final polish

Keep it short enough that someone would actually use it.
```

---

**Done check:** You have at least one useful content draft, a list of claims or sensitive details to verify, and a reusable prompt if the team wants to repeat the workflow.
