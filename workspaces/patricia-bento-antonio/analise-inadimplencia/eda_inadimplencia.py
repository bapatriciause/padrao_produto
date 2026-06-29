#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EDA / Relatório de Qualidade de Dados — Inadimplência (modelo pós-reaviso)
==========================================================================

Perfila os datasets `ML_DATASET_FINAL_<cliente>.csv` (1 linha por reaviso) e
gera um relatório de qualidade de dados antes de qualquer treino de modelo.

Alinhado ao P-031 ("avaliar qualidade do dado, se realmente tem as informações")
e ao Day 2 do AI Accelerator (evidência honesta antes de construir).

ACHADO QUE MOTIVOU ESTA ANÁLISE
-------------------------------
O target `TARGET_PAGOU_ANTES_CORTE` (derivado de `REAVISO.CANCELADO='S'`) está
quase vazio (~0,02% de positivos). Diagnóstico: `REAVISO.CANCELADO` é flag
administrativo raro; o pagamento antes do corte é capturado no desfecho da ordem
de corte (`REAVISO_CORTES.CORTADO` = 'A' cancelada por pagamento vs 'C' executada).
Este script QUANTIFICA o problema — não o corrige (o fix é no extract SQL/Oracle).

Como rodar
----------
    python eda_inadimplencia.py
Saídas em `saidas/`:
    - relatorio_qualidade.md          (relatório legível)
    - perfil_colunas_<cliente>.csv    (nulos/tipo/distintos por coluna)
    - resumo_consolidado.csv          (1 linha por cliente)

Requisitos: pandas, numpy.
"""

from __future__ import annotations
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd

# ============================================================================
# CONFIG
# ============================================================================
AQUI = Path(__file__).resolve().parent

# Pasta dos datasets reais (fora do repositório). Sobrescrevível por env var.
DATA_DIR = Path(os.environ.get(
    "INADIMP_DATA_DIR",
    r"C:\Users\patricia.bento\Downloads\Inadimplencia\Datasets teste",
))
SAIDA_DIR = AQUI / "saidas"

TARGET = "TARGET_PAGOU_ANTES_CORTE"

# Limiares de sanidade
TOP_CATEGORIAS = 8          # nº de categorias mostradas por coluna categórica
ALTA_CARDINALIDADE = 50     # acima disso, sinaliza "encoding necessário"
NULO_INESPERADO = 0.30      # % de nulos que merece destaque (em cols não-opcionais)

# Colunas por grupo (do dicionário ml-dataset-inadimplencia-fields.md)
IDENTIFICADORES = ["NUMERO_REAVISO", "IDUC", "ANO_MES", "DATA_EMISSAO"]

NUMERICAS = [
    "TOTAL_DEBITO", "DISJUNTOR", "KVA_DISPONIVEL", "DIAS_ATE_LIMITE_CORTE",
    "QTDE_REAVISOS_3M", "QTDE_REAVISOS_6M", "QTDE_REAVISOS_12M", "QTDE_REAVISOS_TOTAL",
    "VALOR_MEDIO_DEBITO_12M", "MAX_DEBITO_HISTORICO", "VARIACAO_DEBITO_VS_MEDIA",
    "QTDE_CORTES_12M", "QTDE_CORTES_TOTAL", "MEDIA_DIAS_CORTADO", "MAX_DIAS_CORTADO",
    "MIN_DIAS_CORTADO", "TAXA_RELIGOU_MESMO_DIA", "TAXA_RELIGACAO_AUTOMATICA",
    "DIAS_DESDE_ULTIMO_CORTE", "TAXA_PAG_CANAL_SMS", "TAXA_PAG_CANAL_IMPRESSO",
    "MES_REFERENCIA", "TRIMESTRE", "DIA_SEMANA_EMISSAO",
]

# Flags 0/1 (esperam pouquíssimo nulo; nulo aqui é sinal)
FLAGS = [
    "FLAG_RESIDENCIAL", "FLAG_INDUSTRIAL", "FLAG_COMERCIAL", "FLAG_RURAL",
    "FLAG_PODER_PUBLICO", "FLAG_SERVICO_PUBLICO", "FLAG_BAIXA_RENDA",
    "FLAG_DEBITO_CONTA", "FLAG_MICRO_GERACAO", "PRORROGADO", "HAVIA_PRORROGACOES",
    "FLAG_PAGOU_ULTIMO_REAVISO", "FLAG_PRORROGOU_12M", "FLAG_NAO_RELIGAR_AUTOMATICO",
    "FLAG_ULTIMO_RELIGOU_MESMO_DIA", "FLAG_CORTE_INDEVIDO_HISTORICO",
    "FLAG_NUNCA_FOI_CORTADO", "CANAL_IGUAL_AO_ULTIMO",
]

CATEGORICAS = [
    "NOME_CLASSE", "NOME_SUBCLASSE", "MUNICIPIO", "UF", "NOME_BAIRRO", "NOME_ROTA",
    "GRUPO_TENSAO", "CANAL_ENTREGA", "ORIGEM_REAVISO", "ULTIMA_FORMA_EXECUCAO_CORTE",
]

# Colunas em que NULO é esperado/documentado (sem histórico) — não sinalizar
NULO_ESPERADO = {
    "MEDIA_DIAS_CORTADO", "MAX_DIAS_CORTADO", "MIN_DIAS_CORTADO",
    "TAXA_RELIGOU_MESMO_DIA", "TAXA_RELIGACAO_AUTOMATICA", "DIAS_DESDE_ULTIMO_CORTE",
    "ULTIMA_FORMA_EXECUCAO_CORTE", "TAXA_PAG_CANAL_SMS", "TAXA_PAG_CANAL_IMPRESSO",
    "VALOR_MEDIO_DEBITO_12M", "VARIACAO_DEBITO_VS_MEDIA", "MAX_DEBITO_HISTORICO",
    "CANAL_ENTREGA",
}

# Mapas de decodificação (para leitura humana no relatório)
MAP_CANAL = {0: "Impresso", 1: "SMS"}
MAP_ORIGEM = {1: "Automático", 2: "Manual", 3: "Agrupamento", 4: "SMS"}
MAP_FORMA = {1: "COD (campo)", 2: "MDM (remoto)", 3: "COD→MDM", 4: "Outros"}


# ============================================================================
# CARGA
# ============================================================================
def descobrir_datasets() -> dict[str, Path]:
    if not DATA_DIR.exists():
        sys.exit(f"[ERRO] Pasta de dados não encontrada: {DATA_DIR}\n"
                 f"       Defina INADIMP_DATA_DIR apontando para os ML_DATASET_FINAL_*.csv")
    achados = {}
    for p in sorted(DATA_DIR.glob("ML_DATASET_FINAL_*.csv")):
        nome = p.stem.replace("ML_DATASET_FINAL_", "")
        achados[nome] = p
    if not achados:
        sys.exit(f"[ERRO] Nenhum ML_DATASET_FINAL_*.csv em {DATA_DIR}")
    return achados


def coerce_numeric(s: pd.Series) -> pd.Series:
    """Converte para numérico tolerando decimal vírgula."""
    if pd.api.types.is_numeric_dtype(s):
        return s
    direto = pd.to_numeric(s, errors="coerce")
    nao_nulos = s.notna().sum()
    if nao_nulos and direto.notna().sum() < 0.7 * nao_nulos:
        # provavelmente decimal vírgula
        alt = pd.to_numeric(
            s.astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
            errors="coerce",
        )
        if alt.notna().sum() > direto.notna().sum():
            return alt
    return direto


def carregar(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep=",", low_memory=False)
    for c in NUMERICAS + FLAGS + [TARGET]:
        if c in df.columns:
            df[c] = coerce_numeric(df[c])
    if "DATA_EMISSAO" in df.columns:
        df["_DATA_EMISSAO_DT"] = pd.to_datetime(df["DATA_EMISSAO"], errors="coerce")
    return df


# ============================================================================
# ANÁLISES
# ============================================================================
def analisar_datas(df: pd.DataFrame) -> dict:
    """Detecta sentinelas 1900 e período válido."""
    info = {}
    if "ANO_MES" in df.columns:
        am = df["ANO_MES"].astype(str)
        sentinela = am.str.startswith("1900") | am.str.startswith("18")
        info["ano_mes_sentinela_qtd"] = int(sentinela.sum())
        info["ano_mes_sentinela_pct"] = float(sentinela.mean() * 100)
        validos = am[~sentinela]
        info["ano_mes_min"] = validos.min() if len(validos) else None
        info["ano_mes_max"] = validos.max() if len(validos) else None
    if "_DATA_EMISSAO_DT" in df.columns:
        d = df["_DATA_EMISSAO_DT"]
        fora = (d.dt.year < 2020) | (d.dt.year > 2026)
        info["data_emissao_fora_faixa_qtd"] = int(fora.sum())
    return info


def perfil_colunas(df: pd.DataFrame) -> pd.DataFrame:
    linhas = []
    n = len(df)
    for c in df.columns:
        if c.startswith("_"):
            continue
        nulos = int(df[c].isna().sum())
        linhas.append({
            "coluna": c,
            "tipo": str(df[c].dtype),
            "nulos": nulos,
            "nulos_pct": round(nulos / n * 100, 2),
            "distintos": int(df[c].nunique(dropna=True)),
            "nulo_esperado": c in NULO_ESPERADO,
        })
    return pd.DataFrame(linhas)


def resumo_target(df: pd.DataFrame) -> dict:
    n = len(df)
    pos = int(df[TARGET].sum()) if TARGET in df.columns else 0
    return {
        "linhas": n,
        "ucs_distintas": int(df["IDUC"].nunique()) if "IDUC" in df.columns else None,
        "reavisos_por_uc": round(n / df["IDUC"].nunique(), 2) if "IDUC" in df.columns else None,
        "target_pos": pos,
        "target_pos_pct": round(pos / n * 100, 4),
    }


def fmt_num(x) -> str:
    if pd.isna(x):
        return "—"
    if isinstance(x, (int, np.integer)):
        return f"{x:,}".replace(",", ".")
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def describe_numericas(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    cols = [c for c in cols if c in df.columns]
    d = df[cols].describe(percentiles=[0.5, 0.99]).T
    d["negativos"] = [(df[c] < 0).sum() for c in cols]
    d["zeros"] = [(df[c] == 0).sum() for c in cols]
    return d


def features_degeneradas(df: pd.DataFrame, limiar: float = 0.99) -> list[str]:
    """Colunas constantes ou quase-constantes (1 valor cobre >limiar das linhas).
    Sem variância → não ajudam o modelo; devem ser descartadas por distribuidora."""
    achadas = []
    cols = [c for c in (FLAGS + CATEGORICAS + NUMERICAS) if c in df.columns]
    n = len(df)
    for c in cols:
        vc = df[c].value_counts(dropna=False)
        if len(vc) <= 1 or (vc.iloc[0] / n) > limiar:
            top = vc.index[0]
            rot = "nulo" if pd.isna(top) else top
            achadas.append(f"`{c}` (={rot}, {vc.iloc[0]/n*100:.1f}%)")
    return achadas


def top_categorias(s: pd.Series, k: int, decode: dict | None = None) -> str:
    vc = s.value_counts(dropna=False).head(k)
    total = len(s)
    partes = []
    for val, cnt in vc.items():
        rotulo = "(nulo)" if pd.isna(val) else (
            decode.get(int(val), val) if (decode and not pd.isna(val) and float(val).is_integer()) else val
        )
        partes.append(f"{rotulo}: {cnt/total*100:.1f}%")
    return " · ".join(partes)


# ============================================================================
# RELATÓRIO
# ============================================================================
def gerar_relatorio(dados: dict[str, pd.DataFrame]) -> str:
    L = []
    w = L.append
    w("# Relatório de Qualidade de Dados — Inadimplência (pós-reaviso)\n")
    w("> Gerado por `eda_inadimplencia.py`. Grão: 1 linha por reaviso "
      "(`ML_DATASET_FINAL_<cliente>.csv`). Análise exploratória **antes** de treinar "
      "qualquer modelo — alinhada ao P-031 e à honestidade de evidência do Day 2.\n")

    # ---- 1. Achado crítico: target ----
    w("## 1. ⚠️ Achado crítico — o rótulo está inviável\n")
    w("O target `TARGET_PAGOU_ANTES_CORTE` (= `REAVISO.CANCELADO='S'`) é quase "
      "inexistente. Com tão poucos positivos **não há treino supervisionado possível**, "
      "e o valor é implausível (contradiz recuperação de 50%+ do benchmark).\n")
    w("| Cliente | Reavisos | UCs | Reav./UC | Positivos (pagou) | % positivos |")
    w("|---|---:|---:|---:|---:|---:|")
    consolidado = []
    for nome, df in dados.items():
        r = resumo_target(df)
        consolidado.append({"cliente": nome, **r})
        w(f"| {nome} | {fmt_num(r['linhas'])} | {fmt_num(r['ucs_distintas'])} | "
          f"{r['reavisos_por_uc']} | {fmt_num(r['target_pos'])} | {r['target_pos_pct']}% |")
    tot_n = sum(c["linhas"] for c in consolidado)
    tot_p = sum(c["target_pos"] for c in consolidado)
    w(f"| **TOTAL** | **{fmt_num(tot_n)}** | | | **{fmt_num(tot_p)}** | "
      f"**{tot_p/tot_n*100:.4f}%** |\n")
    w("**Diagnóstico (confirmado com análise do `ml-dataset-inadimplencia-extract.sql`):** "
      "`REAVISO.CANCELADO` é flag administrativo raro. O pagamento antes do corte é "
      "capturado no desfecho da ordem de corte — `REAVISO_CORTES.CORTADO`: "
      "`'A'` (cancelada por pagamento) → target=1; `'C'` (executada) → target=0. "
      "**Ação:** redefinir o target no extract a partir de `CORTADO` (e opcionalmente "
      "cruzar `DT_PAGAMENTO ≤ LIMITE_CORTE`). Esta coluna de desfecho **não está** no "
      "dataset atual, então o rótulo correto não pode ser reconstruído aqui — precisa de "
      "nova extração.\n")

    # ---- 2. Datas / sentinelas ----
    w("## 2. Cobertura temporal e datas-sentinela\n")
    w("| Cliente | Período válido (ANO_MES) | Sentinela 1900 | DATA_EMISSAO fora de 2020–2026 |")
    w("|---|---|---:|---:|")
    for nome, df in dados.items():
        di = analisar_datas(df)
        w(f"| {nome} | {di.get('ano_mes_min','?')} … {di.get('ano_mes_max','?')} | "
          f"{fmt_num(di.get('ano_mes_sentinela_qtd',0))} "
          f"({di.get('ano_mes_sentinela_pct',0):.2f}%) | "
          f"{fmt_num(di.get('data_emissao_fora_faixa_qtd',0))} |")
    w("\n`ANO_MES = 1900-01` é competência nula vazando do Oracle (sentinela). Excluir "
      "ou imputar antes de usar como variável temporal de split.\n")

    # ---- 3. Qualidade por coluna ----
    w("## 3. Qualidade por coluna (nulos inesperados)\n")
    w("Colunas com nulos acima do esperado (exclui as que são NULL por design — "
      "sem histórico de corte/canal):\n")
    achou_nulo = False
    for nome, df in dados.items():
        pc = perfil_colunas(df)
        problema = pc[(pc["nulos_pct"] >= NULO_INESPERADO * 100) & (~pc["nulo_esperado"])]
        problema = problema[~problema["coluna"].isin(["DATA_EMISSAO"])]
        if len(problema):
            achou_nulo = True
            w(f"**{nome}:** " + " · ".join(
                f"`{r.coluna}` {r.nulos_pct}%" for r in problema.itertuples()) + "\n")
    if not achou_nulo:
        w("Nenhuma coluna não-opcional com nulos relevantes — bom sinal de integridade.\n")

    # ---- 4. Distribuições numéricas-chave + sanidade ----
    w("## 4. Distribuições numéricas e valores implausíveis\n")
    chave = ["TOTAL_DEBITO", "DIAS_ATE_LIMITE_CORTE", "QTDE_REAVISOS_12M",
             "QTDE_CORTES_TOTAL", "VARIACAO_DEBITO_VS_MEDIA", "DIAS_DESDE_ULTIMO_CORTE"]
    for nome, df in dados.items():
        w(f"\n**{nome}**\n")
        w("| Feature | mediana | média | p99 | máx | negativos | zeros |")
        w("|---|---:|---:|---:|---:|---:|---:|")
        d = describe_numericas(df, chave)
        for c in [c for c in chave if c in d.index]:
            row = d.loc[c]
            w(f"| {c} | {fmt_num(row['50%'])} | {fmt_num(row['mean'])} | "
              f"{fmt_num(row['99%'])} | {fmt_num(row['max'])} | "
              f"{fmt_num(int(row['negativos']))} | {fmt_num(int(row['zeros']))} |")
    # flag de máximos implausíveis em DIAS_ATE_LIMITE_CORTE (LIMITE_CORTE com data-lixo)
    suspeitos = []
    for nome, df in dados.items():
        if "DIAS_ATE_LIMITE_CORTE" in df:
            mx = df["DIAS_ATE_LIMITE_CORTE"].max()
            if mx > 90:
                qt = int((df["DIAS_ATE_LIMITE_CORTE"] > 90).sum())
                suspeitos.append(f"{nome} (máx {fmt_num(mx)}d, {qt} linhas > 90d)")
    if suspeitos:
        w("\n> ⚠️ `DIAS_ATE_LIMITE_CORTE` com máximos implausíveis (prazo normal é 15–30 "
          "dias): " + "; ".join(suspeitos) + ". Provável `LIMITE_CORTE` com data-sentinela "
          "— limpar/winsorizar antes do treino.\n")
    w("> `DIAS_ATE_LIMITE_CORTE` negativo (se houver) indica limite de corte antes da "
      "emissão — inconsistência a investigar.\n")

    # ---- 5. Composição categórica ----
    w("## 5. Composição (segmentos e operacional)\n")
    for nome, df in dados.items():
        w(f"\n**{nome}**\n")
        if "NOME_CLASSE" in df:
            w(f"- Classe: {top_categorias(df['NOME_CLASSE'], TOP_CATEGORIAS)}")
        if "GRUPO_TENSAO" in df:
            w(f"- Grupo tensão: {top_categorias(df['GRUPO_TENSAO'], 4)}")
        if "FLAG_BAIXA_RENDA" in df:
            w(f"- Baixa renda: {df['FLAG_BAIXA_RENDA'].mean()*100:.1f}%")
        if "FLAG_NUNCA_FOI_CORTADO" in df:
            w(f"- Nunca foi cortado: {df['FLAG_NUNCA_FOI_CORTADO'].mean()*100:.1f}%")
        if "CANAL_ENTREGA" in df:
            w(f"- Canal de entrega: {top_categorias(df['CANAL_ENTREGA'], 4, MAP_CANAL)}")
        if "ORIGEM_REAVISO" in df:
            w(f"- Origem do reaviso: {top_categorias(df['ORIGEM_REAVISO'], 4, MAP_ORIGEM)}")
        if "ULTIMA_FORMA_EXECUCAO_CORTE" in df:
            w(f"- Última forma de corte: {top_categorias(df['ULTIMA_FORMA_EXECUCAO_CORTE'], 5, MAP_FORMA)}")
        # cardinalidade alta
        altas = [c for c in ["NOME_SUBCLASSE", "MUNICIPIO", "NOME_BAIRRO", "NOME_ROTA"]
                 if c in df and df[c].nunique() > ALTA_CARDINALIDADE]
        if altas:
            w("- Alta cardinalidade (precisa encoding/agrupamento): " +
              ", ".join(f"`{c}` ({df[c].nunique()})" for c in altas))

    # ---- 6. Features degeneradas ----
    w("\n## 6. Features degeneradas / candidatas a descarte\n")
    w("Colunas constantes ou quase-constantes (1 valor cobre >99% das linhas) — sem "
      "poder preditivo nesta base; descartar por distribuidora (e revisar se o dado "
      "deveria ter variância):\n")
    for nome, df in dados.items():
        deg = features_degeneradas(df)
        if deg:
            w(f"**{nome}:** " + " · ".join(deg) + "\n")
        else:
            w(f"**{nome}:** nenhuma.\n")

    # ---- 7. Achados consolidados + próximos passos ----
    w("\n## 7. Achados consolidados\n")
    w("1. **Rótulo inviável** — redefinir o target a partir de `REAVISO_CORTES.CORTADO` "
      "no extract (bloqueador do modelo supervisionado).")
    w("2. **Sentinela 1900** em `ANO_MES` (CERSUL/CHESP) — limpar antes do split temporal.")
    w("3. **Nulos por design** em features de corte/canal são esperados (UC sem histórico); "
      "para árvore (LightGBM) deixar como NaN; para modelos lineares, imputar + flag.")
    w("4. **Alta cardinalidade** em bairro/rota/subclasse — target/freq encoding ou "
      "agrupar por regional.")
    w("5. **Cadastro estático**: features de UC refletem o estado atual no banco, não o "
      "estado na data do reaviso (possível leakage leve em cadastro — documentado no dicionário).\n")
    w("## 8. Próximos passos\n")
    w("- [ ] Corrigir o target no extract (`CORTADO`) e reextrair.")
    w("- [ ] Revalidar o balanço de classes com o novo rótulo (esperado ~30–60% positivos).")
    w("- [ ] Definir split temporal por `ANO_MES` (treino/valid/teste), sem embaralhar.")
    w("- [ ] Então treinar baseline (LightGBM) por distribuidora; meta AUC ≥ 0,80 (v1).\n")
    w("---\n_Relatório de qualidade — não substitui validação com a área de Cobrança/"
      "Regulatório para decisões de corte._\n")
    return "\n".join(L)


# ============================================================================
# MAIN
# ============================================================================
def main() -> None:
    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    paths = descobrir_datasets()
    print(f"[INFO] {len(paths)} datasets em {DATA_DIR}")

    dados: dict[str, pd.DataFrame] = {}
    consol = []
    for nome, p in paths.items():
        print(f"[INFO] carregando {nome} ...", end=" ", flush=True)
        df = carregar(p)
        dados[nome] = df
        print(f"{len(df):,} linhas".replace(",", "."))
        # perfil de colunas por cliente
        perfil_colunas(df).to_csv(SAIDA_DIR / f"perfil_colunas_{nome}.csv", index=False)
        r = resumo_target(df)
        di = analisar_datas(df)
        consol.append({"cliente": nome, **r, **di})

    pd.DataFrame(consol).to_csv(SAIDA_DIR / "resumo_consolidado.csv", index=False)

    relatorio = gerar_relatorio(dados)
    (SAIDA_DIR / "relatorio_qualidade.md").write_text(relatorio, encoding="utf-8")

    # resumo no console
    print("\n=== TARGET (achado principal) ===")
    tot_n = tot_p = 0
    for c in consol:
        tot_n += c["linhas"]; tot_p += c["target_pos"]
        print(f"  {c['cliente']:10s} {c['linhas']:>9,} linhas  "
              f"{c['target_pos']:>5} positivos  ({c['target_pos_pct']:.4f}%)".replace(",", "."))
    print(f"  {'TOTAL':10s} {tot_n:>9,} linhas  {tot_p:>5} positivos  "
          f"({tot_p/tot_n*100:.4f}%)".replace(",", "."))
    print(f"\n[OK] Relatório: {SAIDA_DIR / 'relatorio_qualidade.md'}")


if __name__ == "__main__":
    main()
