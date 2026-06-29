# Prework

Upload your existing materials here before/during Day 1. The Day-1 onboarding prompt walks you through this, but here's a quick overview.

## What to upload

- Market research, competitive analyses, industry reports
- Customer analytics: support tickets, NPS data, usage analytics, churn data, past RFPs, CSV/Excel exports
- Customer interview transcripts (external customers and internal team members)
- Existing user research, product strategy docs, prior persona work
- Anything else useful for your business or vertical

Just upload files into this folder. As you go, ask Claude Code to organise them into folders (e.g. `prework/customer-interviews/`, `prework/market-research/`). It will create folders as needed.

## Supported file types

Claude Code can read PDF, DOCX, MD, TXT, XLSX, CSV, PPTX, and images (PNG, JPG).

Claude Code cannot transcribe audio or video. Run those through a separate transcription tool first and upload the transcript text.

## File size

GitHub warns on files over 50MB and blocks files over 100MB. For huge data files, sample them down first (e.g. first 5,000 rows of a CSV) or ask Claude to extract key info from the file locally and upload a summary instead.

## Helper files in this folder

These are optional tools you can use. None are required.

- `_api-access.md`, fillable form to document the API access your VBU has (support system, product APIs, etc.). Don't put real tokens in this file.
- `_existing-product-ideas.md`, fillable template to capture product ideas you're already carrying into the accelerator (problem, idea, data needs, expected impact, open questions). Fill it in as part of prework so the workshop can reference what you already have.
- `_example-external-interview.md`, one way to structure an external customer interview. Use it as a model if you want.
- `_example-internal-interview.md`, same for internal interviews (sales, support, success, etc.).
- `_example-customer-analytics.md`, one way to summarise your customer analytics data at a high level. Optional; Claude can analyse raw exports directly.

If your raw interview transcripts need cleaning before analysis, there's a transcript cleanup prompt inside `prompts-v2/day-one/A-market-research.md`. Run that during Day 1, not as prework.
