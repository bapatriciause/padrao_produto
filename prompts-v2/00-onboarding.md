# Onboarding

> **Onboarding exception:** This is the only v2 chapter where you paste one large block up front. Claude should still walk you through the setup one step at a time after you paste it.

> **Interaction rule:** Paste the onboarding block once, then work with Claude section by section. Claude should ask clarifying questions, pause for your judgement, and treat the setup as a guided conversation.

> **Before each copyable prompt block:** If the context is incomplete, ask 1-3 clarifying questions before producing output. After each major section, stop and ask what the user wants to challenge, refine, or change before continuing.

Use this first. This file keeps the original onboarding flow intact, but the facilitator should still pause between steps and keep the user actively making decisions.

---

## Onboarding

# Onboarding

> **This one is different from the other prompts.** It's a single block meant to be pasted into Claude Code in full — Claude will then walk you through it step by step.

**Open this as the very first thing on Day 1, once you have Claude Code running in this repo.**

Copy the entire prompt below into Claude Code, including all sections, and let it guide you through setup.

If anything goes sideways during onboarding (or later), check `troubleshooting/README.md` or ask a facilitator.

---

```
You are helping me onboard onto an AI Accelerator GitHub repository. This is my first time using this repo and I may be new to GitHub and Claude Code. Walk me through the following steps one at a time, waiting for my response before moving to the next step. Use plain English and explain what you're doing.

## Step 1: Tour the repo

Read the following files in this repo and give me a summary:
- README.md
- guides/github-and-repo-guide.md
- The folder structure (just list the top-level folders and what each is for)

Then tell me:
- What this repo is for
- The 3-4 most important things I need to know before I start
- The rules I should follow (especially around prompts/ and templates/ being read-only)

## Step 2: Set up my workspace

Ask me:
1. What is my first and last name?
2. Is anyone else from my business unit working in this same repo? (If yes, how many of us, 2, 3, 4, or 5?)
3. What is your role in the business? For example: Product, Sales, Customer Success, Support, Implementation, Engineering, GM/leadership, Operations, or something else.
4. How comfortable are you with Claude Code and GitHub today: new, somewhat comfortable, or confident?
5. What kind of customer or business evidence are you bringing? For example: interviews, sales notes, support tickets, usage data, NPS, churn/renewal notes, roadmap docs, competitor research, financial/customer revenue data, or API access.
6. What do you most want to leave the Product Track with? For example: a validated problem, a stronger use case, a prototype direction, a revenue proposal, or clearer customer evidence.

Based on my answers:
- If I'm the only person, tell me I can either work directly in workspaces/ or create my own subfolder for organisation
- If there are multiple of us, create a folder for me at workspaces/<my-name-in-kebab-case>/ and put a placeholder README.md inside it that says it's my workspace. Confirm the folder was created.
- Create or update `workspaces/<my-name-in-kebab-case>/participant-profile.md` with my role, comfort level, evidence types, workshop goal, and any teammate coordination notes. If I am working directly in `workspaces/`, save it as `workspaces/participant-profile.md`.
- Tell me: "We'll use this profile to adapt the prompts. If you're closer to Sales, we'll draw on commercial signals. If you're closer to Support or CS, we'll draw on tickets, renewals, and customer pain. If you're closer to Product or Engineering, we'll draw on roadmap, workflow, data, and feasibility. The role does not decide the answer — it decides what evidence we should remember to use."
- Note my comfort level for later. If I said "new" or "somewhat comfortable", plan to explain each step in plain English and move one decision at a time. If I said "confident", plan to compress the teaching and let me move faster — but still hold the interrogation, customer stack-rank, and kill-your-darlings passes firm, because those are where the value is for an experienced participant. Do not lower the depth checks for anyone.

## Step 2b: How to work efficiently with Claude

Explain this before any exercises start:

"You do not have to sit and wait for one Claude conversation to finish before doing anything else. Some exercises can run in parallel because they look at different evidence. Claude cannot open extra sessions for you, but it can tell you when it would help. You open a new Claude Code session/window yourself, paste the section Claude gives you, and keep working.

Examples:
- One chat can research market trends
- One chat can analyse customer or internal data
- One chat can look at competitors

If you are new to Claude Code, it is completely fine to run one chat at a time. If you are comfortable, open multiple Claude Code sessions/windows yourself to move faster. This is not something you have to decide once for the whole workshop; Claude should point it out when a section can run in parallel and tell you what to paste where. The important thing is to bring the outputs back together into the files in your workspace, especially `insights.md`.

Use parallel chats for independent research or analysis. Use one focused chat for judgement-heavy work like choosing problem statements, refining personas, selecting use cases, Responsible AI fit, and PoC handoff review."

Then say: "During the workshop, I'll flag when opening another Claude Code session/window could save time. You can always choose to keep one chat if that feels easier."

## Step 3: Help me upload my prework

If multiple people from my business unit are sharing this repo, first check with me to avoid duplicate uploads:

"Before we upload anything, are you handling the prework upload for the whole team, or is each person uploading different files? If you're not sure, pause here and check with your teammates so we don't end up with duplicates in prework/. Common patterns:
- One person uploads everything for the team
- Each person uploads the files they personally gathered
- Each category (interviews, analytics, market research, etc.) has a designated owner

Tell me which one applies and what files I should upload."

Then read prework/README.md. Ask me about each prework category one at a time, only for the files I'm responsible for:

1. **Customer interview transcripts.** "Do you have any customer interview transcripts you'd like to upload? They can be from external customers or internal team members (sales, support, etc.). If yes, tell me where the files are on your computer and I'll help you copy them into prework/customer-interviews/ (create the folder if it doesn't exist). Before copying, check whether a teammate has already uploaded the same file."

2. **Customer analytics / data.** "Do you have any customer data exports, support tickets, NPS data, usage analytics, churn data, past RFPs, etc.? If yes, tell me where the files are and I'll help you copy them into prework/customer-data/. CSV, Excel, PDF, Word, all of these work. Before copying, check whether a teammate has already uploaded the same file."

3. **Market research.** "Do you have any existing market research, competitive analysis, or industry reports? If yes, tell me where the files are and I'll help you copy them into prework/market-research/. Before copying, check whether a teammate has already uploaded the same file."

4. **Product research / user insights.** "Do you have any existing user research, product strategy docs, or roadmap materials? If yes, tell me where the files are and I'll help you copy them into prework/product-research/. Before copying, check whether a teammate has already uploaded the same file."

5. **Role-specific evidence.** "Do you have evidence from your role that doesn't fit neatly above? Examples: Sales notes, demo objections, lost-deal notes, renewal risk notes, Customer Success adoption themes, Support escalations, Implementation notes, Engineering feasibility notes, roadmap debates, or GM/customer revenue context. If yes, tell me where the files are and I'll help you copy them into prework/role-specific-evidence/. We'll label these clearly so Claude treats them as evidence from your vantage point, not universal truth."

6. **API access.** "Does your VBU have API access to systems you'd like to query during the workshop (your support ticketing system, your own product APIs, etc.)? If yes, help me fill in prework/_api-access.md to document what access exists. **Do NOT put actual API tokens or credentials in this file. Bring them securely on the day (1Password, Azure Key Vault, or share in person).** If a teammate already filled this in, review their entries together rather than overwriting."

For each "yes", help me move/copy the files into the right subfolder. Create the folder if it doesn't exist yet. For each "no", note it and move on, that's fine.

## Step 4: Confirm

When we're done, give me a summary of:
- What workspace folder was created (if any)
- What role, comfort level, evidence types, and workshop goal were saved in `participant-profile.md`
- What prework was uploaded and where
- What prework categories I said I don't have

## Step 5: Save my onboarding work

Tell me: "Now that we've set up your workspace and uploaded your prework, let's save it. The easy way to save in this repo is to just say 'save my work' or 'back this up' to me — I'll handle the rest. Try it now."

When I say it, use the `save-my-work` skill: ask me for a short label (e.g. "Onboarding complete"), then commit and push for me. Confirm in plain English when done.

Then STOP. Do not start any exercises. Wait until you're told what to run next.
```
