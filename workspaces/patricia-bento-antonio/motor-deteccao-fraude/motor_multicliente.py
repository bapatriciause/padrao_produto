# -*- coding: utf-8 -*-
"""
================================================================================
 MOTOR DE DETECÇÃO DE IRREGULARIDADES (PNT) — MULTI-CLIENTE
================================================================================
Processa os 5 clientes em 2 formatos de dados, normalizando para um conjunto
comum de atributos e gerando um ranking de inspeção POR CLIENTE.

  Coopera ............ "análise de leitura"  (Datasets 2)  — wide, 3 meses, BT
  Aliança/Chesp/
  Cetril/Cersul ...... histórico faturamento (Datasets teste) — long, 24 meses

Estratégia (sem casos rotulados): regras determinísticas + anomalia não
supervisionada (Isolation Forest) + score combinado e priorizado.

O formato de faturamento habilita atributos extras: classe, benchmark do
sistema (peer), micro-geração e sazonalidade (usados para EVITAR falso
positivo em quedas legítimas).
================================================================================
"""
import os
import sys
import glob
import random
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ------------------------------------------------------------------ CONFIG ----
BASE = r"C:\Users\patricia.bento\Downloads\Detecção de fraude"
PASTA_COOPERA = os.path.join(BASE, "Datasets 2")
PASTA_FATUR   = os.path.join(BASE, "Datasets teste")
_REAL = os.environ.get("FRAUDE_REAL") == "1"   # FRAUDE_REAL=1 -> dados reais (uso interno)
PASTA_SAIDA   = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "saidas-real" if _REAL else "saidas")

LIM_QUEDA_BRUSCA   = 0.60
LIM_QUEDA_MODERADA = 0.40
LIM_TROCA_QUEDA    = 0.30
CONSUMO_MINIMO_REL = 30
LIM_PEER_BAIXO     = 0.25     # consome < 25% da média do sistema p/ a classe
# tarifa social com consumo alto (corte regulatório — validar com a área)
LIM_BR_ALTO        = 300      # kWh/mês (média 12m)
LIM_BR_MUITO_ALTO  = 500      # kWh/mês (média 12m)
# tarifa média assumida p/ Coopera (não há VALOR_TOTAL_MES neste formato)
TARIFA_PADRAO_COOPERA = 0.95  # R$/kWh — PREMISSA, ajustar com a área financeira

PESO = {
    "CLANDESTINA":     100,
    "QUEDA_ZERO":       80,
    "QUEDA_BRUSCA":     60,
    "BR_MUITO_ALTO":    55,    # tarifa social com consumo muito alto
    "TROCA_QUEDA":      45,
    "PEER_BAIXO":       40,
    "BR_ALTO":          35,    # tarifa social com consumo alto
    "ZERO_PERSISTENTE": 35,
    "QUEDA_MODERADA":   25,
}
W_REGRAS, W_ANOMALIA = 0.65, 0.35
RANDOM_STATE = 42

# colunas candidatas para o detector de anomalia (usa as disponíveis por cliente)
FEATS_ANOMALIA = ["consumo_atual", "media_hist", "media_12m", "queda_ratio",
                  "queda_yoy", "peer_ratio", "n_zeros_janela", "robust_z", "cv",
                  "npicos", "troca_medidor"]


# ------------------------------------------------------- UTILITÁRIOS NUMÉRICOS -
def num_br(serie):
    """Texto numérico com vírgula decimal (Coopera) -> float."""
    s = serie.astype(str).str.strip()
    tem_v = s.str.contains(",", regex=False)
    s = s.where(~tem_v, s.str.replace(".", "", regex=False)).str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce")


def colunas_comuns():
    """Esqueleto do dataframe normalizado (uma linha por UC)."""
    return ["cliente", "IDUC", "identificacao", "classe", "competencia",
            "consumo_atual", "media_hist", "media_12m", "queda_ratio", "queda_yoy",
            "razao_atual_media", "cv", "n_zeros_janela", "robust_z", "npicos",
            "peer_ratio", "troca_medidor", "ligado", "lido",
            "micro_geracao", "sazonal", "sazonal_prone", "baixa_renda",
            "referencia_kwh", "tarifa_efetiva"]


# ============================================================ FORMATO COOPERA ==
def featurizar_coopera(cliente="Coopera"):
    arquivos = sorted(glob.glob(os.path.join(PASTA_COOPERA, "*.csv")))
    frames = []
    for c in arquivos:
        muni = os.path.basename(c).replace(".csv", "").split(" - ")[-1].strip()
        d = pd.read_csv(c, sep=";", dtype=str, encoding="utf-8-sig")
        d["MUNICIPIO"] = muni
        frames.append(d)
    df = pd.concat(frames, ignore_index=True)

    for col in ["CONSUMOMES", "CONSUMOMES1", "CONSUMOMES2", "CONSUMOMES3", "MEDIA"]:
        df[col] = num_br(df[col])
    for col in ["IDNAOLEITURA", "TROCA_MEDIDOR_MES_ATUAL", "TROCA_MEDIDOR_MES_SEGUINTE"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    hist = df[["CONSUMOMES1", "CONSUMOMES2", "CONSUMOMES3"]].fillna(0)
    atual = df["CONSUMOMES"].fillna(0)
    janela = pd.concat([atual, hist["CONSUMOMES1"], hist["CONSUMOMES2"], hist["CONSUMOMES3"]], axis=1)

    out = pd.DataFrame(index=df.index)
    out["cliente"] = cliente
    out["IDUC"] = df["IDUC"]
    out["identificacao"] = df["MUNICIPIO"].fillna("") + " | " + df["NOME"].fillna("")
    out["classe"] = ""
    out["competencia"] = df["COMPETENCIA"].str.split().str[0]
    out["consumo_atual"] = atual
    out["media_hist"] = hist.mean(axis=1)
    out["media_12m"] = hist.mean(axis=1)            # só há 3 meses neste formato
    with np.errstate(divide="ignore", invalid="ignore"):
        out["queda_ratio"] = np.where(out["media_hist"] > 0,
                                      (out["media_hist"] - atual) / out["media_hist"], 0.0)
        out["razao_atual_media"] = np.where(out["media_hist"] > 0, atual / out["media_hist"], np.nan)
    m4, s4 = janela.mean(axis=1), janela.std(axis=1, ddof=0)
    out["cv"] = np.where(m4 > 0, s4 / m4, 0.0)
    out["n_zeros_janela"] = (janela == 0).sum(axis=1)
    out["robust_z"] = np.nan
    out["npicos"] = np.nan
    out["peer_ratio"] = np.nan
    out["troca_medidor"] = ((df["TROCA_MEDIDOR_MES_ATUAL"] == 1) |
                            (df["TROCA_MEDIDOR_MES_SEGUINTE"] == 1)).astype(int)
    out["ligado"] = (df["LIGADO"].fillna("").str.strip().str.upper() == "S")
    out["lido"] = (df["IDNAOLEITURA"] == 0)
    out["micro_geracao"] = 0
    out["sazonal"] = 0
    out["baixa_renda"] = 0           # formato Coopera não traz subclasse/tarifa
    out["queda_yoy"] = np.nan        # só há 3 meses — sem comparação ano a ano
    out["sazonal_prone"] = 0         # sem classe/irrigação neste formato
    out["referencia_kwh"] = out["media_hist"]
    out["tarifa_efetiva"] = TARIFA_PADRAO_COOPERA   # premissa (sem valor faturado)
    return out[colunas_comuns()]


# ========================================================= FORMATO FATURAMENTO ==
def featurizar_faturamento(caminho):
    cliente = os.path.basename(caminho).replace("DATASET_FINAL_HISTORICO_", "").replace(".csv", "").title()
    usecols = ["IDUC", "ANO_MES", "KWH_REAL", "VALOR_TOTAL_MES", "GRUPO_TENSAO_MES",
               "LIGADO_MES", "MEDIA_KWH_SISTEMA", "NPICOS120", "TIPO_CALCULO",
               "NOME_CLASSE", "NOME_SUBCLASSE", "TARIFA", "FLAG_MICRO_GERACAO",
               "FLAG_SAZONAL", "ENERGIA_IRRIGACAO", "MUNICIPIO", "NOME_BAIRRO"]
    df = pd.read_csv(caminho, sep=",", dtype=str, encoding="utf-8-sig", usecols=usecols)
    df["ANO_MES"] = df["ANO_MES"].str[:7]                     # YYYY-MM
    df["KWH_REAL"] = pd.to_numeric(df["KWH_REAL"], errors="coerce")
    df["VALOR_TOTAL_MES"] = pd.to_numeric(df["VALOR_TOTAL_MES"], errors="coerce")

    # tarifa efetiva do cliente (R$/kWh) — mediana sobre meses de consumo
    # relevante (>=100 kWh) para reduzir distorção da taxa mínima/custo fixo
    mt = (df["KWH_REAL"] >= 100) & (df["VALOR_TOTAL_MES"] > 0)
    tarifa_efetiva = float((df.loc[mt, "VALOR_TOTAL_MES"] / df.loc[mt, "KWH_REAL"]).median())

    meses = sorted(df["ANO_MES"].dropna().unique())
    atual_m = meses[-1]
    prior3 = meses[-4:-1]
    prior12 = meses[-13:-1]

    # matriz UC x mês de consumo
    kwh = (df.groupby(["IDUC", "ANO_MES"])["KWH_REAL"].last().unstack("ANO_MES"))

    # só UCs ativas no mês corrente
    ativos = kwh[atual_m].notna()
    kwh = kwh[ativos]
    idx = kwh.index

    consumo_atual = kwh[atual_m].fillna(0)
    media_hist = kwh[prior3].mean(axis=1)
    media_12m = kwh[prior12].mean(axis=1)
    jan = kwh[[atual_m] + prior3]
    n_zeros = (jan == 0).sum(axis=1)
    m4, s4 = jan.mean(axis=1), jan.std(axis=1, ddof=0)
    cv = np.where(m4 > 0, s4 / m4, 0.0)
    # z robusto vs próprio histórico (12m)
    med12 = kwh[prior12].median(axis=1)
    mad12 = (kwh[prior12].sub(med12, axis=0)).abs().median(axis=1)
    robust_z = (consumo_atual - med12) / (1.4826 * mad12 + 1e-6)

    with np.errstate(divide="ignore", invalid="ignore"):
        queda = np.where(media_hist > 0, (media_hist - consumo_atual) / media_hist, 0.0)
        razao = np.where(media_hist > 0, consumo_atual / media_hist, np.nan)

    # atributos estáticos: linha do mês corrente
    est = (df[df["ANO_MES"] == atual_m].drop_duplicates("IDUC").set_index("IDUC"))
    est = est.reindex(idx)
    peer = pd.to_numeric(est["MEDIA_KWH_SISTEMA"], errors="coerce")
    with np.errstate(divide="ignore", invalid="ignore"):
        peer_ratio = np.where(peer > 0, consumo_atual / peer, np.nan)

    # comparação ano-a-ano: mesmo mês do ano anterior (neutraliza sazonalidade)
    yoy_m = meses[-13] if len(meses) >= 13 else None
    if yoy_m:
        kwh_yoy = kwh[yoy_m]
        with np.errstate(divide="ignore", invalid="ignore"):
            queda_yoy = np.where(kwh_yoy.values > 0,
                                 (kwh_yoy.values - consumo_atual.values) / kwh_yoy.values, np.nan)
    else:
        queda_yoy = np.full(len(idx), np.nan)

    out = pd.DataFrame(index=idx)
    out["cliente"] = cliente
    out["IDUC"] = idx
    out["identificacao"] = (est["MUNICIPIO"].fillna("") + " | " + est["NOME_BAIRRO"].fillna("")).values
    out["classe"] = est["NOME_CLASSE"].fillna("").values
    out["competencia"] = atual_m
    out["consumo_atual"] = consumo_atual.values
    out["media_hist"] = media_hist.values
    out["media_12m"] = media_12m.values
    out["queda_ratio"] = queda
    out["queda_yoy"] = queda_yoy
    out["razao_atual_media"] = razao
    out["cv"] = cv
    out["n_zeros_janela"] = n_zeros.values
    out["robust_z"] = robust_z.values
    out["npicos"] = pd.to_numeric(est["NPICOS120"], errors="coerce").fillna(0).values
    out["peer_ratio"] = peer_ratio
    out["troca_medidor"] = 0                                  # não há flag neste formato
    out["ligado"] = (est["LIGADO_MES"].fillna("").str.strip().str.upper() == "S").values
    out["lido"] = True                                        # histórico já faturado
    out["micro_geracao"] = pd.to_numeric(est["FLAG_MICRO_GERACAO"], errors="coerce").fillna(0).astype(int).values
    out["sazonal"] = pd.to_numeric(est["FLAG_SAZONAL"], errors="coerce").fillna(0).astype(int).values
    # tarifa social: identificada pela subclasse ou pela tarifa (B1r/B1d)
    sub = est["NOME_SUBCLASSE"].fillna("").str.lower()
    tar = est["TARIFA"].fillna("").str.upper()
    out["baixa_renda"] = (sub.str.contains(r"baixa renda|bx renda|desconto social|bpc", regex=True)
                          | tar.isin(["B1R", "B1D"])).astype(int).values
    # UCs com sazonalidade esperada (rural/agro, irrigação ou sazonal cadastrado):
    # nelas a queda é avaliada ano-a-ano, não contra a média recente.
    irrig = pd.to_numeric(est["ENERGIA_IRRIGACAO"], errors="coerce").fillna(1)
    classe_l = est["NOME_CLASSE"].fillna("").str.lower()
    is_rural = classe_l.str.contains("rural|agro") | sub.str.contains("rural|agro")
    is_saz = pd.to_numeric(est["FLAG_SAZONAL"], errors="coerce").fillna(0) == 1
    out["sazonal_prone"] = (is_rural | irrig.isin([2, 3]) | is_saz).astype(int).values
    # referência de consumo p/ estimar energia não faturada:
    # ano-a-ano nas sazonais (com base YoY), média recente nas demais
    ref = media_hist.values.copy()
    if yoy_m is not None:
        usa_yoy = out["sazonal_prone"].values.astype(bool) & ~np.isnan(queda_yoy)
        ref = np.where(usa_yoy, kwh_yoy.values, media_hist.values)
    out["referencia_kwh"] = ref
    out["tarifa_efetiva"] = tarifa_efetiva
    out = out.reset_index(drop=True)
    return out[colunas_comuns()], cliente


# ----------------------------------------------------------------- REGRAS ------
def aplicar_regras(f):
    n = len(f)
    motivos = [[] for _ in range(n)]
    score = np.zeros(n)
    atual = f["consumo_atual"].values
    media = f["media_hist"].values
    media12 = f["media_12m"].values
    queda = f["queda_ratio"].values
    queda_yoy = f["queda_yoy"].values
    sp = f["sazonal_prone"].values
    peer = f["peer_ratio"].values
    troca = f["troca_medidor"].values
    lido = f["lido"].values
    ligado = f["ligado"].values
    micro = f["micro_geracao"].values
    br = f["baixa_renda"].values

    for i in range(n):
        if not lido[i]:
            continue
        # Tarifa social com consumo alto — sinal de irregularidade cadastral
        # (independe de queda; usa a média de 12 meses para evitar pico pontual)
        if br[i] and media12[i] >= LIM_BR_MUITO_ALTO:
            motivos[i].append(f"Tarifa social com consumo muito alto ({media12[i]:.0f} kWh/mês méd. 12m)")
            score[i] += PESO["BR_MUITO_ALTO"]
        elif br[i] and media12[i] >= LIM_BR_ALTO:
            motivos[i].append(f"Tarifa social com consumo alto ({media12[i]:.0f} kWh/mês méd. 12m)")
            score[i] += PESO["BR_ALTO"]
        if (not ligado[i]) and atual[i] > 0:
            motivos[i].append("Consumo registrado com UC desligada (possível ligação clandestina)")
            score[i] += PESO["CLANDESTINA"]
        if ligado[i]:
            # Queda "efetiva": UCs sazonais (rural/irrigação) comparam ano-a-ano
            # (mesmo mês do ano anterior); as demais, contra a média recente.
            if sp[i]:
                qy = queda_yoy[i]
                q_eff = None if np.isnan(qy) else qy
                ref = "vs mesmo mês do ano anterior"
            else:
                q_eff = queda[i]
                ref = "vs média"

            if atual[i] == 0 and media[i] > 0:
                # zero com histórico: em UC sazonal, só se o mesmo mês do ano
                # anterior teve consumo (senão é entressafra, não fraude)
                if (not sp[i]) or (q_eff is not None and q_eff > 0):
                    motivos[i].append("Consumo zerou tendo histórico anterior")
                    score[i] += PESO["QUEDA_ZERO"]
            elif atual[i] == 0 and (media12[i] == 0 or np.isnan(media12[i])):
                motivos[i].append("Consumo zero persistente — validar imóvel vago/sazonal")
                score[i] += PESO["ZERO_PERSISTENTE"]
            elif atual[i] > 0 and media[i] >= CONSUMO_MINIMO_REL and not micro[i]:
                # micro-geração (solar) reduz consumo legitimamente -> não pontua
                if q_eff is not None:
                    if q_eff >= LIM_QUEDA_BRUSCA:
                        motivos[i].append(f"Queda de consumo de {q_eff*100:.0f}% {ref} (>=60%)")
                        score[i] += PESO["QUEDA_BRUSCA"]
                    elif q_eff >= LIM_QUEDA_MODERADA:
                        motivos[i].append(f"Queda de consumo de {q_eff*100:.0f}% {ref} (40-60%)")
                        score[i] += PESO["QUEDA_MODERADA"]
            if (troca[i] == 1 and q_eff is not None
                    and q_eff >= LIM_TROCA_QUEDA and atual[i] > 0):
                motivos[i].append("Troca de medidor acompanhada de queda de consumo")
                score[i] += PESO["TROCA_QUEDA"]
            # consumo muito abaixo do benchmark do sistema + queda própria
            if (not np.isnan(peer[i]) and peer[i] < LIM_PEER_BAIXO and atual[i] > 0
                    and q_eff is not None and q_eff >= LIM_QUEDA_MODERADA and not micro[i]):
                motivos[i].append(f"Consumo {peer[i]*100:.0f}% da média do sistema para a classe")
                score[i] += PESO["PEER_BAIXO"]

    f = f.copy()
    f["motivos"] = ["; ".join(m) for m in motivos]
    f["score_regra"] = np.minimum(score, 100)
    return f


# ----------------------------------------------------- ANOMALIA (POR CLIENTE) --
def aplicar_anomalia(f):
    cols = [c for c in FEATS_ANOMALIA if c in f.columns and f[c].notna().mean() > 0.5]
    X = f[cols].copy()
    for c in cols:
        X[c] = pd.to_numeric(X[c], errors="coerce")
        X[c] = X[c].fillna(X[c].median())
    Xs = StandardScaler().fit_transform(X.values)
    mask = (f["ligado"] & f["lido"]).values
    if mask.sum() < 50:
        f = f.copy(); f["score_anomalia"] = 0.0; return f
    modelo = IsolationForest(n_estimators=300, contamination="auto",
                             random_state=RANDOM_STATE, n_jobs=-1)
    modelo.fit(Xs[mask])
    raw = modelo.score_samples(Xs)
    lo, hi = raw[mask].min(), raw[mask].max()
    anom = np.clip((hi - raw) / (hi - lo), 0, 1) if hi > lo else np.zeros_like(raw)
    f = f.copy()
    f["score_anomalia"] = np.where(mask, anom, 0.0)
    return f


# ------------------------------------------------- SCORE FINAL + PRIORIDADE ----
def priorizar(f):
    f = f.copy()
    f["score_final"] = (W_REGRAS * f["score_regra"] + W_ANOMALIA * f["score_anomalia"] * 100).round(1)
    f["situacao"] = np.where(~f["lido"], "SEM_LEITURA",
                    np.where((~f["ligado"]) & (f["consumo_atual"] == 0), "DESLIGADA", "ANALISAR"))
    tem_regra = f["score_regra"] > 0
    anomala = f["score_anomalia"] >= 0.95
    f["suspeita"] = (f["situacao"] == "ANALISAR") & (tem_regra | anomala)
    f["origem"] = np.where(tem_regra, "regra", np.where(anomala, "anomalia", "-"))
    so_anom = f["suspeita"] & (~tem_regra) & anomala
    f.loc[so_anom, "motivos"] = "Padrão de consumo anômalo (detecção estatística)"

    def faixa(r):
        if not r["suspeita"]:
            return "-"
        if "clandestina" in r["motivos"].lower():
            return "CRÍTICA"
        if r["score_final"] >= 70:
            return "ALTA"
        if r["score_final"] >= 40:
            return "MÉDIA"
        return "BAIXA"
    f["prioridade"] = f.apply(faixa, axis=1)
    return f


# --------------------------------------------------------- ANONIMIZAÇÃO --------
# Substitui dados pessoais (nome do consumidor e IDUC) por valores fictícios nas
# saídas, para que os arquivos possam ser versionados/compartilhados com segurança
# (LGPD). Desligue (ANONIMIZAR = False) apenas para uso interno com dado real.
ANONIMIZAR = not _REAL          # anonimiza por padrão; FRAUDE_REAL=1 mantém dado real
_PRIMEIROS = ["Ana", "Bruno", "Carla", "Diego", "Eduarda", "Felipe", "Gabriela",
              "Henrique", "Isabela", "João", "Karina", "Lucas", "Mariana", "Nelson",
              "Otávio", "Patrícia", "Rafael", "Sandra", "Tiago", "Vanessa"]
_SOBRENOMES = ["Silva", "Souza", "Oliveira", "Santos", "Pereira", "Costa", "Almeida",
               "Ferreira", "Rodrigues", "Gomes", "Martins", "Araújo", "Ribeiro",
               "Carvalho", "Lima", "Barbosa"]


def _anonimizar(susp, cliente):
    """Pseudonimiza o IDUC e, na Coopera (único formato com nome de pessoa),
       substitui o nome do consumidor por um nome fictício. Mantém o município
       (cidade pública, não é dado pessoal) e toda a parte analítica intacta."""
    rng = random.Random(42)
    susp = susp.copy()
    pref = "".join(ch for ch in cliente.upper() if ch.isalpha())[:3] or "UC"
    susp["IDUC"] = [f"{pref}{i:06d}" for i in range(1, len(susp) + 1)]
    if cliente.lower() == "coopera":
        susp["identificacao"] = [
            f"{str(s).split(' | ')[0]} | {rng.choice(_PRIMEIROS)} {rng.choice(_SOBRENOMES)}"
            for s in susp["identificacao"]]
    return susp


# ----------------------------------------------------------------- SAÍDA -------
def salvar_e_resumir(f, cliente):
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    susp = f[f["suspeita"]].sort_values("score_final", ascending=False)
    if ANONIMIZAR:
        susp = _anonimizar(susp, cliente)
    cols = ["cliente", "IDUC", "identificacao", "classe", "competencia", "prioridade",
            "score_final", "valor_estimado_mes", "valor_estimado_ano",
            "energia_nao_faturada_mes", "score_regra", "score_anomalia", "consumo_atual",
            "media_hist", "media_12m", "queda_ratio", "queda_yoy", "peer_ratio",
            "n_zeros_janela", "baixa_renda", "sazonal_prone", "micro_geracao",
            "sazonal", "baseline_alto", "origem", "motivos"]
    out = susp[cols].copy()
    out["score_anomalia"] = (out["score_anomalia"] * 100).round(1)
    out["queda_ratio"] = (out["queda_ratio"] * 100).round(0)
    out["queda_yoy"] = (out["queda_yoy"] * 100).round(0)
    out["peer_ratio"] = (out["peer_ratio"] * 100).round(0)
    arq = os.path.join(PASTA_SAIDA, f"ranking_{cliente.lower()}.csv")
    out.to_csv(arq, sep=";", index=False, encoding="utf-8-sig")

    total = len(f)
    cnt = susp["prioridade"].value_counts()
    return {
        "cliente": cliente, "ucs": total,
        "sem_leitura": int((f["situacao"] == "SEM_LEITURA").sum()),
        "desligadas": int((f["situacao"] == "DESLIGADA").sum()),
        "suspeitas": len(susp),
        "CRÍTICA": int(cnt.get("CRÍTICA", 0)), "ALTA": int(cnt.get("ALTA", 0)),
        "MÉDIA": int(cnt.get("MÉDIA", 0)), "BAIXA": int(cnt.get("BAIXA", 0)),
        "valor_ano": float(susp["valor_estimado_ano"].sum()),
        "arquivo": arq, "susp_df": susp[cols],
    }


def estimar_financeiro(f):
    """Estima energia não faturada e R$ em risco (ESTIMATIVA — não é perda confirmada).
       Clandestina: todo o consumo é não faturado. Demais: gap vs referência.
       Winsoriza o gap no P99 do cliente para não inflar o total com baselines
       implausíveis (erro de leitura/rollover de medidor)."""
    f = f.copy()
    cland = (~f["ligado"]) & (f["consumo_atual"] > 0)
    ref = f["referencia_kwh"].fillna(0)
    gap = np.maximum(0.0, ref - f["consumo_atual"])
    lost = np.where(cland, f["consumo_atual"].astype(float), gap.astype(float))

    pos = lost[lost > 0]
    cap = float(np.percentile(pos, 99)) if len(pos) else np.inf
    f["baseline_alto"] = (lost > cap).astype(int)          # marca p/ validar leitura
    lost = np.minimum(lost, cap)

    f["energia_nao_faturada_mes"] = np.round(lost, 0)
    f["valor_estimado_mes"] = np.round(lost * f["tarifa_efetiva"].fillna(0), 2)
    f["valor_estimado_ano"] = np.round(f["valor_estimado_mes"] * 12, 2)
    return f


def processar(f, cliente):
    f = aplicar_regras(f)
    f = aplicar_anomalia(f)
    f = priorizar(f)
    f = estimar_financeiro(f)
    return salvar_e_resumir(f, cliente)


# ------------------------------------------------------------------ MAIN -------
def main():
    resumos = []
    print(">> Coopera (análise de leitura)")
    resumos.append(processar(featurizar_coopera(), "Coopera"))

    for c in sorted(glob.glob(os.path.join(PASTA_FATUR, "*.csv"))):
        nome = os.path.basename(c).replace("DATASET_FINAL_HISTORICO_", "").replace(".csv", "").title()
        print(f">> {nome} (histórico de faturamento)")
        f, cliente = featurizar_faturamento(c)
        resumos.append(processar(f, cliente))

    # tabela consolidada
    print("\n" + "=" * 86)
    print(" CONSOLIDADO — 5 CLIENTES")
    print("=" * 86)
    hdr = (f"{'CLIENTE':<10}{'UCs':>9}{'SUSPEITAS':>11}{'CRÍTICA':>9}{'ALTA':>7}"
           f"{'MÉDIA':>7}{'BAIXA':>7}{'R$/ANO (est.)':>18}")
    print(hdr); print("-" * 86)
    tot = {k: 0 for k in ["ucs", "suspeitas", "CRÍTICA", "ALTA", "MÉDIA", "BAIXA", "valor_ano"]}
    consolid = []
    for r in resumos:
        print(f"{r['cliente']:<10}{r['ucs']:>9,}{r['suspeitas']:>11,}"
              f"{r['CRÍTICA']:>9}{r['ALTA']:>7}{r['MÉDIA']:>7}{r['BAIXA']:>7}"
              f"{('R$ '+format(r['valor_ano'], ',.0f')):>18}")
        for k in tot:
            tot[k] += r[k]
        consolid.append(r["susp_df"])
    print("-" * 86)
    print(f"{'TOTAL':<10}{tot['ucs']:>9,}{tot['suspeitas']:>11,}"
          f"{tot['CRÍTICA']:>9}{tot['ALTA']:>7}{tot['MÉDIA']:>7}{tot['BAIXA']:>7}"
          f"{('R$ '+format(tot['valor_ano'], ',.0f')):>18}")
    print("=" * 86)

    cons = pd.concat(consolid, ignore_index=True).sort_values(
        ["prioridade", "score_final"], ascending=[True, False])
    arq = os.path.join(PASTA_SAIDA, "ranking_consolidado.csv")
    cons.to_csv(arq, sep=";", index=False, encoding="utf-8-sig")
    print(f"\nRankings por cliente + consolidado salvos em: {PASTA_SAIDA}")


if __name__ == "__main__":
    main()
