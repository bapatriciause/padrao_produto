# Troubleshooting & FAQ

Quick fixes for when things aren't working. Don't spend more than 2 minutes on any problem — ask your facilitator or a teammate.

---

## AI Giving Bad Output

**It's too generic / surface-level:**
```
That's too generic. Be more specific to [YOUR INDUSTRY/PRODUCT].
Give me concrete examples, not categories.
```

**It's making things up:**
```
Stop. Only use information I've given you. If you don't know something,
say "I don't have data for that" instead of guessing.
```

**It ignored my instructions:**
```
You missed what I asked for. I specifically want [RESTATE YOUR REQUEST].
Go back and try again, focusing only on that.
```

**It gave me a wall of text:**
```
Too long. Give me the top 3 points only, as bullet points,
one sentence each.
```

**It's being too agreeable:**
```
Stop being nice. Challenge my assumptions. What's wrong with
what I just said? Where am I being naive?
```

**It keeps going off-track:**
Start a new conversation. Paste your key context in fresh. Sometimes it's faster to restart than to redirect.

---

## Claude Code Specific

**"I don't have permission":**
Claude Code will ask for permission to read/write files or run commands. Type `y` to allow, or check the permission prompt carefully.

**It's editing the wrong file:**
```
Stop. You're editing [WRONG FILE]. I want you to edit [RIGHT FILE].
Don't touch anything else.
```

**It's writing too much code:**
```
Keep it simple. Single HTML file, no frameworks, no build tools.
I want to open the file in a browser and see it work.
```

**It's stuck in a loop:**
Press `Ctrl+C` to cancel, then try rephrasing your request.

**I want to undo what it just did:**
```
Undo the last change you made.
```
Or use git: `git checkout -- [filename]`

---

## Git / GitHub

**"I've never used git before":**
You only need 4 commands:
```bash
git pull                    # Get latest changes
git add .                   # Stage your changes
git commit -m "my message"  # Save with a description
git push                    # Upload to GitHub
```

**"It says I have a conflict":**
```bash
git stash            # Temporarily hide your changes
git pull             # Get the latest
git stash pop        # Bring your changes back
```
If that doesn't work, ask your facilitator.

**"I accidentally edited someone else's file":**
```bash
git checkout -- [filename]   # Undo changes to that file
```

**"I can't push":**
```bash
git pull --rebase    # Pull first, then push
git push
```

**"I'm lost — where am I?":**
```bash
git status           # Shows what's changed
pwd                  # Shows which folder you're in
ls                   # Shows files in current folder
```

---

## Terminal Basics

**"What is the terminal?":**
It's a text-based way to interact with your computer. Instead of clicking, you type commands.

**"How do I open a file?":**
```bash
open filename.html        # Opens in default app (Mac)
code filename.html        # Opens in VS Code
start filename.html       # Opens in default app (Windows)
```

**"How do I get to my workspace folder?":**
```bash
cd workspaces/your-name   # Replace your-name with your folder name
```

**"How do I see my files?":**
```bash
ls                        # List files
ls -la                    # List with details
```

**"How do I go back?":**
```bash
cd ..                     # Go up one folder
cd ~                      # Go to home folder
```

---

## "I'm Completely Stuck"

1. **Ask Claude:** Describe your problem to Claude in plain English. It can help with git, code, prompts, or anything else.
2. **Ask a teammate:** If others from your VBU are working in this repo, they may have hit the same issue.
3. **Ask a facilitator:** Raise your hand. No question is too basic.
4. **Start fresh:** If everything is broken, you can always re-clone:
   ```bash
   cd ~
   rm -rf <your-repo-folder>
   git clone <YOUR-VBU-REPO-URL>
   cd <your-repo-folder>
   ```
   Your committed work is safe on GitHub.

---

## Useful Claude Prompts for When You're Lost

```
I'm at an AI accelerator and I'm stuck. Here's what I'm trying to do:
[EXPLAIN IN PLAIN ENGLISH]. What should I try next?
```

```
I ran this command and got this error: [PASTE ERROR].
What went wrong and how do I fix it?
```

```
I'm new to this. Can you explain what [TERM/CONCEPT] means
in simple language?
```
