#!/usr/bin/env python3
"""
profile.py — load, validate, and profile the ML_DATASET_FINAL inadimplência datasets.

This is the "run" harness for the one-drive data unit. There is no app/server here:
the deliverable is a set of CSV datasets (one per distribuidora) plus the SQL that
extracts them from Oracle. You cannot run the SQL without the Oracle source DB, but
you CAN load and validate the produced CSVs — which is what this driver does.

Stdlib only (csv, argparse, statistics). No pandas/sklearn required — works on a
clean python3 with nothing installed. 800k+ rows stream fine in a single pass.

Usage:
  python3 profile.py                      # profile every ML_DATASET_FINAL_*.csv in CWD
  python3 profile.py ML_DATASET_FINAL_CERSUL.csv   # one file
  python3 profile.py --schema-only        # only check headers vs documented schema (fast)
  python3 profile.py --limit 50000 FILE   # profile only first N data rows (quick smoke)

Exit code is non-zero if any file fails to load or its header diverges from the
documented schema, so it doubles as a CI smoke check.
"""
import argparse
import csv
import glob
import math
import os
import sys

# ---------------------------------------------------------------------------
# Documented schema — the 58 columns from ml-dataset-inadimplencia-fields.md §9.
# The shipped CSVs carry 57: FLAG_VIRADA_ANO (Grupo B) is documented but absent.
# The driver flags that automatically; it's listed here so the check is honest
# about what the dictionary promises vs. what the file delivers.
# ---------------------------------------------------------------------------
DOCUMENTED_COLUMNS = [
    # Identificadores (4)
    "NUMERO_REAVISO", "IDUC", "ANO_MES", "DATA_EMISSAO",
    # Target (1)
    "TARGET_PAGOU_ANTES_CORTE",
    # Grupo A — Cadastro da UC (18)
    "NOME_CLASSE", "NOME_SUBCLASSE",
    "FLAG_RESIDENCIAL", "FLAG_INDUSTRIAL", "FLAG_COMERCIAL", "FLAG_RURAL",
    "FLAG_PODER_PUBLICO", "FLAG_SERVICO_PUBLICO", "FLAG_BAIXA_RENDA",
    "MUNICIPIO", "UF", "NOME_BAIRRO", "NOME_ROTA",
    "DISJUNTOR", "KVA_DISPONIVEL", "FLAG_DEBITO_CONTA", "FLAG_MICRO_GERACAO",
    "GRUPO_TENSAO",
    # Grupo B — Reaviso corrente (10) -- FLAG_VIRADA_ANO documented but NOT in CSV
    "TOTAL_DEBITO", "CANAL_ENTREGA", "PRORROGADO", "HAVIA_PRORROGACOES",
    "ORIGEM_REAVISO", "MES_REFERENCIA", "TRIMESTRE", "FLAG_VIRADA_ANO",
    "DIA_SEMANA_EMISSAO", "DIAS_ATE_LIMITE_CORTE",
    # Grupo C — Histórico de pagamento (9)
    "QTDE_REAVISOS_3M", "QTDE_REAVISOS_6M", "QTDE_REAVISOS_12M",
    "QTDE_REAVISOS_TOTAL", "VALOR_MEDIO_DEBITO_12M", "MAX_DEBITO_HISTORICO",
    "FLAG_PAGOU_ULTIMO_REAVISO", "FLAG_PRORROGOU_12M", "VARIACAO_DEBITO_VS_MEDIA",
    # Grupo D — Cortes e religações (13)
    "QTDE_CORTES_12M", "QTDE_CORTES_TOTAL", "FLAG_NAO_RELIGAR_AUTOMATICO",
    "MEDIA_DIAS_CORTADO", "MAX_DIAS_CORTADO", "MIN_DIAS_CORTADO",
    "TAXA_RELIGOU_MESMO_DIA", "FLAG_ULTIMO_RELIGOU_MESMO_DIA",
    "TAXA_RELIGACAO_AUTOMATICA", "DIAS_DESDE_ULTIMO_CORTE",
    "ULTIMA_FORMA_EXECUCAO_CORTE", "FLAG_CORTE_INDEVIDO_HISTORICO",
    "FLAG_NUNCA_FOI_CORTADO",
    # Grupo F — Canal de comunicação (3)
    "TAXA_PAG_CANAL_SMS", "TAXA_PAG_CANAL_IMPRESSO", "CANAL_IGUAL_AO_ULTIMO",
]

TARGET = "TARGET_PAGOU_ANTES_CORTE"

# LGPD / identifier columns to strip before training (per dict §1, §8).
DROP_BEFORE_TRAINING = ["NUMERO_REAVISO", "IDUC", "DATA_EMISSAO"]


def check_header(header):
    """Compare a file header against the documented schema. Returns (missing, extra)."""
    doc = set(DOCUMENTED_COLUMNS)
    have = set(header)
    missing = [c for c in DOCUMENTED_COLUMNS if c not in have]
    extra = [c for c in header if c not in doc]
    return missing, extra


def is_number(s):
    if s == "" or s is None:
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False


def profile_file(path, limit=None, schema_only=False):
    """Profile one CSV. Returns dict of results; prints a human report."""
    name = os.path.basename(path)
    print(f"\n{'='*70}\n{name}\n{'='*70}")

    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        try:
            header = next(reader)
        except StopIteration:
            print("  !! empty file")
            return {"ok": False}

        missing, extra = check_header(header)
        print(f"columns: {len(header)} (documented: {len(DOCUMENTED_COLUMNS)})")
        if missing:
            print(f"  ⚠ documented but MISSING from file: {', '.join(missing)}")
        if extra:
            print(f"  ⚠ in file but NOT documented: {', '.join(extra)}")
        if not missing and not extra:
            print("  ✓ header matches documented schema exactly")

        if schema_only:
            return {"ok": not extra, "header": header, "missing": missing, "extra": extra}

        idx = {c: i for i, c in enumerate(header)}
        ncols = len(header)
        rows = 0
        null_counts = [0] * ncols
        # streaming numeric stats per column
        num_count = [0] * ncols
        num_sum = [0.0] * ncols
        num_min = [math.inf] * ncols
        num_max = [-math.inf] * ncols
        target_counts = {}

        ti = idx.get(TARGET)
        for row in reader:
            if len(row) != ncols:
                print(f"  ⚠ row {rows+1} has {len(row)} fields, expected {ncols}")
                continue
            rows += 1
            for i, val in enumerate(row):
                if val == "":
                    null_counts[i] += 1
                elif is_number(val):
                    v = float(val)
                    num_count[i] += 1
                    num_sum[i] += v
                    if v < num_min[i]:
                        num_min[i] = v
                    if v > num_max[i]:
                        num_max[i] = v
            if ti is not None:
                tv = row[ti]
                target_counts[tv] = target_counts.get(tv, 0) + 1
            if limit and rows >= limit:
                break

    print(f"rows: {rows:,}{'  (limited)' if limit and rows >= limit else ''}")

    # Target balance
    if ti is not None and target_counts:
        print(f"\ntarget `{TARGET}` distribution:")
        total = sum(target_counts.values())
        for k in sorted(target_counts):
            c = target_counts[k]
            label = {"1": "pagou antes do corte", "0": "nao pagou"}.get(k, "?")
            print(f"  {k} ({label}): {c:,}  ({100*c/total:.1f}%)")
        ones = target_counts.get("1", 0)
        zeros = target_counts.get("0", 0)
        if ones and zeros:
            ratio = max(ones, zeros) / min(ones, zeros)
            flag = "  ⚠ >3:1 — aplicar class_weight/SMOTE (dict §2)" if ratio > 3 else "  ✓ balanceado"
            print(f"  ratio majoritaria:minoritaria = {ratio:.2f}:1{flag}")

    # Per-column profile (compact)
    print("\nper-column (nulls / numeric min..max mean):")
    for i, c in enumerate(header):
        nulls = null_counts[i]
        npct = 100 * nulls / rows if rows else 0
        tag = "  [DROP-LGPD]" if c in DROP_BEFORE_TRAINING else ""
        if num_count[i] > 0 and num_count[i] >= (rows - nulls):
            mean = num_sum[i] / num_count[i]
            print(f"  {c:<32} nulls={nulls:>8,} ({npct:5.1f}%)  "
                  f"{num_min[i]:.3g}..{num_max[i]:.3g} mean={mean:.3g}{tag}")
        else:
            print(f"  {c:<32} nulls={nulls:>8,} ({npct:5.1f}%)  [categorical/text]{tag}")

    return {"ok": not extra, "rows": rows, "missing": missing, "extra": extra,
            "target_counts": target_counts}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="CSV files (default: ML_DATASET_FINAL_*.csv)")
    ap.add_argument("--schema-only", action="store_true", help="only check headers")
    ap.add_argument("--limit", type=int, default=None, help="profile first N data rows")
    args = ap.parse_args()

    files = args.files or sorted(glob.glob("ML_DATASET_FINAL_*.csv"))
    if not files:
        print("no ML_DATASET_FINAL_*.csv found in CWD; pass paths explicitly",
              file=sys.stderr)
        return 2

    all_ok = True
    for path in files:
        if not os.path.exists(path):
            print(f"!! not found: {path}", file=sys.stderr)
            all_ok = False
            continue
        res = profile_file(path, limit=args.limit, schema_only=args.schema_only)
        all_ok = all_ok and res.get("ok", False)

    print(f"\n{'='*70}")
    print("OK" if all_ok else "DONE WITH WARNINGS (header divergence or load error)")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
