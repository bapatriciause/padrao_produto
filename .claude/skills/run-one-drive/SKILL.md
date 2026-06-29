---
name: run-one-drive
description: Load, validate, profile, and "run" the one-drive ML inadimplência datasets (ML_DATASET_FINAL CSVs). Use when asked to run, inspect, validate, profile, screenshot, or sanity-check the inadimplência / delinquency-prediction dataset, check its schema against the data dictionary, or look at target balance / class imbalance.
---

# Run: one-drive (ML inadimplência dataset)

`one-drive` is a **data unit**, not an app. There is no server, GUI, or REPL. The
deliverables are:

- `ML_DATASET_FINAL_{ALIANCA,CERSUL,CETRIL,CHESP}.csv` — one dataset per
  distribuidora (~810k rows total), 1 row per reaviso emitido. Target =
  `TARGET_PAGOU_ANTES_CORTE` (1 = pagou antes do corte, 0 = não pagou).
- `ml-dataset-inadimplencia-extract.sql` — the Oracle extraction that *produces*
  those CSVs (DROP/CREATE TABLE against REAVISO, REAVISO_CORTES, RELIGACOES, …).
- `ml-dataset-inadimplencia-fields.md` — the data dictionary (58 documented columns).

"Running" this unit means **loading and validating the produced CSVs**. The SQL
cannot be run here (it needs the live Oracle source DB — see Gotchas). The harness
is `profile.py`, a stdlib-only Python driver. Paths below are relative to the
`one-drive/` unit root.

## Prerequisites

Only stock `python3` (tested on 3.13). **No pip install needed** — `profile.py`
uses the standard library only (`csv`, `argparse`, `statistics`). 800k rows stream
in one pass.

```bash
python3 --version   # 3.x; no pandas/sklearn/duckdb required
```

(Optional, only if you go on to model: `python3 -m pip install pandas scikit-learn`.
The container ships `numpy` 2.2.3 but no pandas/sklearn by default.)

## Run (agent path) — the driver

`.claude/skills/run-one-drive/profile.py` is the harness. Run it from the unit root.

**Fast schema check across all 4 files** (~instant — reads headers only):

```bash
python3 .claude/skills/run-one-drive/profile.py --schema-only
```

**Full profile of one file** (CERSUL is smallest at 79k rows, ~3s):

```bash
python3 .claude/skills/run-one-drive/profile.py ML_DATASET_FINAL_CERSUL.csv
```

**Quick smoke on a slice of a big file** (first N data rows):

```bash
python3 .claude/skills/run-one-drive/profile.py --limit 5000 ML_DATASET_FINAL_CHESP.csv
```

**Profile everything** (default — no args; ~20s for all four):

```bash
python3 .claude/skills/run-one-drive/profile.py
```

For each file the driver prints: column count vs. documented schema (naming any
missing/extra columns), row count, `TARGET_PAGOU_ANTES_CORTE` balance with an
imbalance warning, and a per-column null %/numeric min..max..mean line (LGPD
columns tagged `[DROP-LGPD]`). Exit code is non-zero if a file fails to load or
carries an **undocumented** column; a documented-but-missing column is a warning
(exit 0) because all shipped files miss `FLAG_VIRADA_ANO` (see Gotchas).

## Verified findings (from running the driver this session)

These came out of the runs above — quote them, don't re-derive:

- **Severe class imbalance, every file.** Positives (`=1`) are 0.0–0.1% of rows:
  ALIANCA 37/227,926 (6159:1), CERSUL 15/79,236 (5281:1), CETRIL 85/227,152
  (2671:1), CHESP 397/275,484 (693:1). This is far beyond the dict's "3:1" note —
  treat as a rare-event problem (class weights / resampling / PR-AUC, not accuracy).
- **`FLAG_VIRADA_ANO` is documented but absent from all 4 CSVs** → 57 columns
  shipped, 58 documented.
- **`MEDIA_DIAS_CORTADO` / `MAX_DIAS_CORTADO` / `MIN_DIAS_CORTADO` carry negative
  values** (down to ~-44,100) and are ~91% null — the dict defines them as
  non-negative durations (DATA_FINAL − DATA_CORTE). Clean/clip before use.
- **`TAXA_PAG_CANAL_SMS` is 100% null in CERSUL** (and `CANAL_ENTREGA` is all 0 =
  impresso there) — that distribuidora has no SMS-delivered reavisos in the window.

## Direct invocation (reuse from your own code)

The validators are plain functions — import without running `main()`:

```bash
python3 -c "
import sys; sys.path.insert(0, '.claude/skills/run-one-drive')
import profile as p
import csv
with open('ML_DATASET_FINAL_CERSUL.csv', newline='') as f:
    header = next(csv.reader(f))
print('missing/extra vs dict:', p.check_header(header))
print('drop before training:', p.DROP_BEFORE_TRAINING)
"
```

`DOCUMENTED_COLUMNS`, `check_header()`, and `DROP_BEFORE_TRAINING` (the LGPD
identifiers `NUMERO_REAVISO`, `IDUC`, `DATA_EMISSAO`) are the reusable pieces.

## Gotchas

- **The SQL is Oracle-only and not runnable here.** `ml-dataset-inadimplencia-extract.sql`
  uses `NOLOGGING`, `TO_CHAR(d,'Q')`, `NVL`, and DROP/CREATE against proprietary
  tables (REAVISO, REAVISO_CORTES, RELIGACOES, NAO_RELIGAR_AUTOMATICO, …). There is
  no Oracle instance in this container, so the dataset is consumed read-only — you
  validate the CSVs, you don't regenerate them.
- **57 vs 58 columns is expected**, not corruption — `FLAG_VIRADA_ANO` was dropped
  from the final extraction. The dict's §9 count (58) is stale relative to the files.
- **Header case differs from the dict.** CSV headers are UPPERCASE
  (`FLAG_DEBITO_CONTA`); the dictionary writes some as lowercase (`flag_debito_conta`).
  `profile.py` matches on the uppercase names the files actually use.
- **`IDUC`/`NUMERO_REAVISO`/`DATA_EMISSAO` are LGPD identifiers** — strip before
  training (dict §8). The driver tags them `[DROP-LGPD]` so you don't feed them in.
- **All 4 headers are byte-identical** (same md5), so schema fixes apply uniformly.
- **`ano_mes` is a split key, not a feature** — temporal split only, never shuffle
  (data-leakage risk, dict §1/§8).

## Troubleshooting

- `no ML_DATASET_FINAL_*.csv found in CWD` → you're not in the unit root. `cd` to
  `one-drive/` (where the CSVs live) before running, or pass explicit paths.
- Want a single file but typed a bad name → the driver prints `!! not found: <path>`
  and continues; check the filename (`ML_DATASET_FINAL_<DISTRIBUIDORA>.csv`).
- Profiling feels slow on the full set → use `--schema-only` for header checks, or
  `--limit N <file>` to sample; a full 275k-row file profile is ~9s.
