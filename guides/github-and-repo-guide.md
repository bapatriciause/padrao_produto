# GitHub & Repo Guide, Volaris AI Accelerator

## Getting Started

### 1. Clone the repo

You should have already received an invitation to your VBU's repository on GitHub. Clone it locally:

```bash
git clone <YOUR-VBU-REPO-URL>
cd <your-repo-folder>
```

If you don't know the URL or haven't been invited yet, ask your facilitator.

### 2. Find or create your workspace folder

Each participant works in their own subfolder under `workspaces/`. If you're sharing this repo with teammates from your VBU:

```bash
mkdir workspaces/your-name
```

Use kebab-case (e.g. `workspaces/jane-smith/`). If you're the only one working in this repo, you can use `workspaces/` directly.

By the end of the workshop your workspace will look roughly like this. Most files sit flat at the root; only `personas/` and `use-cases/` have subfolders because there are multiple files in each. You don't need to pre-create anything — the prompts create files as you go.

```
workspaces/
  your-name/
    insights.md              ← chapter A (market scans, customer analytics, cross-cutting)
    personas/                ← chapter B (one file per persona)
    problem-statements.md    ← chapter C
    hmw-questions.md         ← chapter C
    opportunity-areas.md     ← chapter E
    ideas.md                 ← chapter E (ideation pool)
    clusters.md              ← chapter E
    use-cases.md             ← chapter F (summary across all use cases)
    use-cases/               ← chapters F–H (deep dives on your top 1–2)
    rai-fit.md               ← chapter G
    poc-scope.md             ← chapter H (PoC scope + handoff notes)
```

> **Note on placeholders.** Prompts often reference paths like `workspaces/<my-name>/insights.md` or `workspaces/<your-name>/insights.md`. The `<my-name>` / `<your-name>` bit is a placeholder for your workspace folder — Claude will figure out which folder is yours from the conversation.

### 3. Save your work

The easy way — just ask Claude in plain English:

> "Save my work" or "back this up"

Claude will commit and push for you, and ask what you were working on so the save has a useful label. This works for almost everything you'll do in the workshop. The underlying mechanism is a Claude Code skill in `.claude/skills/save-my-work/` — you don't need to touch it, it activates automatically when you ask to save.

If you'd rather learn the git commands directly:

```bash
git add workspaces/your-name/
git commit -m "Your name: [what you did]"
git push
```

The shorthand: **pull → work → add → commit → push.**

---

## What's Where

| Folder | What | Can I edit it? |
|---|---|---|
| `prompts-v2/` | AI prompt chapters for each exercise (the workshop flow) | No, copy to your workspace first |
| `templates/` | Clean templates for personas and the ideation pool | No, copy to your workspace first |
| `guides/` | Setup and how-to-use guides | No |
| `troubleshooting/` | Quick fixes when things break | No |
| `prework/` | Where you upload existing materials (research, transcripts, analytics) | Yes, upload here |
| `workspaces/your-name/` | **Your working area** | **Yes** |

---

## Try Claude Code Right Now

These quick prompts show what Claude Code can do beyond just chatting. Open your terminal, navigate to your workspace folder, and try:

**Read and summarise a file:**
```
Look at the chapters in the prompts-v2/ folder and tell me which one
I should use first for market research.
```

**Create a file from a conversation:**
```
Create a markdown file in my workspace folder called market-notes.md
with a template for capturing market research findings.
```

**Search the repo:**
```
Search all the prompt files for anything about personas.
Summarise what I need to know.
```

**Build something:**
```
Create a simple HTML page in my prototype folder that shows a
dashboard with three cards summarising key metrics for my product area.
Make it look professional with nice styling.
```

**Analyse data:**
```
I'm going to paste some data. Analyse it and create a markdown
summary with the key findings, saved to my workspace folder.
```

**The difference from Claude chat:** Claude Code can read your files, create new ones, run commands, build prototypes, and interact with your whole workspace. It's not just answering questions, it's doing work alongside you.

---

## Tips

- **Commit often**, small saves are better than one giant one at the end
- **Use descriptive messages**, "Jane: added IT director persona" not "update"
- **Stay in your workspace folder**, don't edit other people's work
- **Copy prompts and templates first**, copy them into your workspace before editing
- **Ask Claude for help**, the simplest way to save is just to say "save my work" or "back this up" — Claude handles the rest

---

## GitHub Web Fallback (if your terminal isn't working)

If you can't get Claude Code or the terminal working on Day 1, you can still participate using GitHub's web interface. It's slower but it always works.

### Edit a file in the browser

1. Go to your VBU's repo on github.com
2. Navigate to the file you want to edit
3. Click the **pencil icon** (top right of the file) to edit
4. Make your changes. Markdown formatting symbols (`#`, `-`, `>`, `|`) should stay; just fill in your content where you see `[square brackets]`
5. Click the green **Commit changes...** button
6. In the popup, make sure it says **"Commit directly to the `main` branch"** and type a short description, then click **Commit changes**

### Upload files (PDFs, spreadsheets, etc.)

1. Navigate to the folder you want to upload to (typically a `prework/` subfolder)
2. Click **Add file** → **Upload files**
3. Drag your files in or click **choose your files**
4. Confirm "Commit directly to the `main` branch" and click **Commit changes**

### Verify your work

After committing, refresh the page, your changes should be visible immediately.

> If you're using the web interface, let your facilitator know. They may be able to help get your terminal working so you can use Claude Code, which is faster and much more powerful.

---

## If Something Goes Wrong

See [troubleshooting/README.md](../troubleshooting/README.md) for quick fixes.
