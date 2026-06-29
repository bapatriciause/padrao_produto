---
name: save-my-work
description: Save the user's current work to git on their behalf in plain language, with light coaching so they gradually learn the concepts. Use this skill whenever the user says anything like "save my work", "save my progress", "save what I've done", "back this up", "back up my work", "save this", "don't lose this", "save the changes", "save where I am", "save and back up", or any similar phrasing that implies they want their current state preserved. Use it even when they don't mention git — especially then. This skill is designed for people writing research, personas, notes, or other markdown content in a git repo, who use git but aren't fluent in the jargon. It does the operation for them, names what just happened in plain English, and quietly teaches the small handful of concepts worth knowing. Do NOT use this skill for saving individual files via a text editor's save function, for exporting files, or for non-git backup workflows.
---

# Save My Work

The user is writing research notes, personas, or similar content in a git repo. They think of git as "save and backup" — and honestly, for what they're doing, that's a reasonable mental model. Your job is to make the operation feel as easy as saving a document, while quietly introducing the few concepts that will help them next time something doesn't go perfectly smoothly.

## The philosophy

**Training wheels, not a black box.** A black box leaves them helpless next time. Training wheels mean you do the work, say what you did in plain language, and over time they start to recognise what's happening.

Two principles:

1. **Match their language.** They say "save" and "back up" — use those words back. *Save* = commit (a snapshot on this computer). *Back up* = push (a copy online where it's safe and others can see it). Use the plain words; mention the git word in italics maybe once if it seems useful, then drop it.

2. **Hide the rest.** *Stage, HEAD, origin, upstream, fast-forward, rebase, ref* — never useful to them. Translate or omit.

The risk here is genuinely lower than with code — markdown conflicts are human-readable, there's no production to break, the worst case is "two versions of a paragraph need merging". Lean towards just doing the thing.

## What to do

### 1. Check there's a git repo

Run `git rev-parse --is-inside-work-tree`.

- **Not a git repo:** "Your work isn't being tracked yet, so I can't save snapshots of it. Want me to set that up? It means from now on every time you say 'save', I can take a snapshot you can come back to later." If yes → `git init`. If no → offer a one-off file copy.
- **Yes:** Continue.

### 2. See what's changed

Run `git status --porcelain`.

- **Nothing changed:** "Nothing new to save since last time — you're already up to date." Stop.
- **Things changed:** Continue. A summary is fine ("Looks like you've updated 3 files") — only list filenames if they ask or if it seems genuinely useful (e.g. they were working on one persona but 7 files changed, which might surprise them).

### 3. Ask one short question

Don't auto-generate a message from the diff and pretend it's smart. Ask:

> "What were you working on? Even a few words is fine — I'll use it as the label so you can find this save later."

Use their answer as the commit message, verbatim or lightly cleaned. If they say "just save it" or similar, use "Work in progress" with the date.

This question does double duty: it gives a useful label, *and* it gently teaches that saves are findable later — which is the single most useful thing they can learn about git.

### 4. Save the snapshot

Run `git add -A` then `git commit -m "<their message>"`. Don't narrate the commands.

### 5. Sync with the remote, then back it up online

Run `git remote -v`.

- **No remote configured:** "Saved on this computer. There's no online backup set up for this — if you'd like one (so it's safe if your laptop dies, and so others can see it), let me know and we can sort it out, or a colleague can set it up in a few minutes." Stop here.
- **Remote exists:** Pull first, then push.
  1. Run `git pull --no-rebase`. Most of the time this is a no-op — nothing new from online. If it merges in updates cleanly, mention that briefly in the final confirmation ("I also pulled in some updates from online while I was at it"). If it surfaces conflicts, go to step 7.
  2. Then run `git push`. If it's a new branch that's never been pushed, use `git push -u origin <branch>` automatically — don't make them think about it.

This pull-before-push pattern means "save" also keeps their local copy current with whatever teammates have pushed, which matches what they usually expect "save" to do.

### 6. Handle push outcomes

**Push succeeded:** "Saved and backed up online." Done. Optionally, the first time in a conversation, add a short aside: "By the way — 'saved' means there's a snapshot on this computer; 'backed up' means there's also a copy online. If you ever lose your laptop, the backup has you covered."

**Push rejected (online has changes you don't have):**

> "Looks like there are some updates online that aren't on your computer yet — probably someone else added or changed something. I need to pull those in before I can finish backing up. Okay if I do that?"

If yes → `git pull --no-rebase`.

- Clean pull → push again → "Saved and backed up. I also pulled in the latest updates from online while I was at it."
- Conflict → step 7.

**Push failed (auth):** "I couldn't connect to the backup — looks like a sign-in issue. Try signing in to GitHub (or wherever this is backed up) and let me know when you're ready." Don't dump the error.

**Push failed (network):** "Saved on your computer, but the backup couldn't reach the internet. Want to try again in a moment?"

### 7. Handle overlapping edits (conflicts)

Markdown conflicts are usually genuinely manageable — they look like two versions of a paragraph side by side. Don't make this scary.

Run `git diff --name-only --diff-filter=U` to see which files overlap.

> "A couple of files were also changed by someone else, so I need your help picking which version to keep. The files are: [list].
>
> For each one I'll show you both versions and you can tell me which to use, or whether you want to combine them. Ready?"

For each conflicted file:

1. Open it and find the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
2. Show both versions in plain language, without the markers: "Here's your version: [...]. Here's the other version: [...]."
3. Ask: "Keep yours, keep theirs, or combine?"
4. Edit the file to leave only the chosen content, removing all markers.

Once all files are resolved: `git add` them, `git commit` (a default message like "Combined edits from both sides" is fine), then push. Confirm: "Saved and backed up. I kept your version for [file], used the other version for [file], and combined them for [file]."

If at any point they want to bail out: `git merge --abort` — but call it "cancel the merging-in step" not "abort". Their original work is untouched.

### 8. Confirm in plain English

Good confirmations:

- "Saved and backed up."
- "Saved on your computer. No online backup set up yet for this one."
- "Saved and backed up. I pulled in some updates from online while I was at it."

Avoid:

- "Committed 4 files to HEAD and pushed to origin/main."
- "Successfully executed git add, git commit, and git push."
- Anything with "repository", "upstream", "ref", or "fast-forward".

## Things to never do without asking

- **Never force anything** (`git push --force`, `--force-with-lease`). If a normal save won't work, ask the user.
- **Never throw away changes** (`git checkout --`, `git reset --hard`, `git clean`). They said save, not delete.
- **Never rebase** without explicit consent — it rewrites history and confuses people later.
- **Never switch branches** as part of saving. Save where they are.
- **Never delete files** unilaterally, even ones that look like they shouldn't be there.

## Light coaching moments

Sprinkle these in *once* when they naturally come up, never as a lecture. Each one is one or two sentences max.

- **First successful save in a conversation:** "By the way — 'saved' means a snapshot on this computer; 'backed up' means also copied online."
- **First time you mention a branch (if it comes up):** "A branch is just a named version of the project — yours is called `[name]`, which keeps your work separate from the main shared version until it's ready."
- **First time pulling in others' changes:** "This is normal whenever you're working alongside other people — git just needs to combine what you've done with what they've done."
- **After a conflict is resolved:** "Conflicts sound scarier than they are — it just means two people edited the same bit at the same time and git asked a human to pick."

If they ask "what's a commit?" or "what does push mean?" — answer in one sentence, plainly, and move on. Don't seize the opportunity to teach them all of git.

## Edge cases

- **All changed files are in `.gitignore`:** "The files you've been working on are set up to be excluded from snapshots — that might be intentional, or it might be a mistake. Want me to check with someone?"
- **Detached HEAD:** "Your work is in an unusual state where new saves won't stick properly. Let me put you back on solid ground first — okay?" Then create a branch.
- **Submodules with changes:** Out of scope. "This project has smaller projects inside it that I'd rather not touch automatically. I'll save the main project's changes and flag the rest for you."
- **`.env` or files that look like secrets in the changes:** Mention it. "I noticed `.env` in the changes — those usually contain passwords or keys that shouldn't be backed up online. Want me to skip it?" Don't remove unilaterally.

## Tone

Calm, conversational, never patronising. The user is smart — they just don't want to learn a version control system to save their research notes. Treat git as plumbing, but tell them what colour the pipes are if they seem curious.
