# Workspaces

This is where you do your actual work during the accelerator. Everyone's work lives under `workspaces/`.

## How to set up your workspace

### If multiple people from your VBU are sharing this repo

Create your own folder. Name it after yourself, in kebab-case:

```bash
mkdir workspaces/your-name
```

Examples: `workspaces/jane-smith/`, `workspaces/alex-patel/`.

The Day-1 onboarding prompt can do this for you automatically. Just tell it your name.

### If you're the only person from your VBU using this repo

You can either create your own folder (same as above) or work directly in `workspaces/` without a subfolder. Either is fine.

## What goes in your workspace

Everything. Filled-in templates, AI outputs, prototypes, scratch notes, exercise outputs. The prompts mostly produce flat files at the root of your workspace (`insights.md`, `problem-statements.md`, `hmw-questions.md`, `ideas.md`, etc.), plus two subfolders that get multiple files: `personas/` (one file per persona) and `use-cases/` (deep dives on your top 1–2 use cases).

See `guides/github-and-repo-guide.md` for the full expected layout. You don't need to pre-create anything — files appear as you work through the prompts.

## Rules

- Don't edit `prompts-v2/` or `templates/` directly. Copy them into your workspace first, then edit your copy.

## Example commit workflow

```bash
git add workspaces/your-name/
git commit -m "your-name: completed market research analysis"
git push
```

If git is confusing, just ask Claude Code to do it for you:

```
Save all my changes and push them to GitHub with the message
"your-name: completed market research analysis"
```
