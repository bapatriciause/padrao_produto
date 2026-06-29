# -*- coding: utf-8 -*-
"""
================================================================================
 MOTOR DE DETECÇÃO DE IRREGULARIDADES (PERDAS NÃO-TÉCNICAS) - BAIXA TENSÃO
================================================================================
Estratégia (sem casos rotulados disponíveis):
    Camada 1 - Regras determinísticas  -> alta precisão, totalmente explicáveis
    Camada 2 - Anomalia não-supervisionada (Isolation Forest) -> ganho de recall
    Camada 3 - Score combinado + priorização para inspeção de campo

Entrada : CSVs "Análise de leitura - meses anteriores" (somente BT)
Saída   : ranking_suspeitas.csv  +  relatório no console

Cada UC recebe: motivos (por que foi sinalizada), score 0-100 e prioridade.
Estruturado para evoluir para o modelo supervisionado (XGBoost) quando a base
de casos confirmados estiver disponível.
================================================================================
"""
import os
import sys
import glob
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

try:                                   # console Windows costuma ser cp1252
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ------------------------------------------------------------------ CONFIG ----
PASTA_DADOS = r"C:\Users\patricia.bento\Downloads\Detecção de fraude\Datasets 2"
PASTA_SAIDA = r"C:\Users\patricia.bento\Downloads\motor-deteccao-fraude"

# Limiares ajustáveis das regras (calibráveis quando houver retorno de campo)
LIM_QUEDA_BRUSCA   = 0.60   # queda >= 60% vs média dos 3 meses anteriores
LIM_QUEDA_MODERADA = 0.40   # queda entre 40% e 60%
LIM_TROCA_QUEDA    = 0.30   # queda >= 30% acompanhada de troca de medidor
CONSUMO_MINIMO_REL = 30     # ignora quedas em UCs de baixíssimo consumo (ruído)

# Pesos das regras (severidade) — somados e limitados a 100
PESO = {
    "CLANDESTINA":     100,   # desligada porém consumindo
    "QUEDA_ZERO":       80,   # zerou tendo histórico (ligada e lida)
    "QUEDA_BRUSCA":     60,   # queda >= 60%
    "TROCA_QUEDA":      45,   # troca de medidor + queda
    "ZERO_PERSISTENTE": 35,   # 4 meses zerados (pode ser imóvel vago)
    "QUEDA_MODERADA":   25,   # queda 40-60%
}

# Combinação final entre regras e anomalia estatística
W_REGRAS   = 0.65
W_ANOMALIA = 0.35
RANDOM_STATE = 42


# -------------------------------------------------------------- UTILITÁRIOS ---
def parse_num(serie: pd.Series) -> pd.Series:
    """Converte texto numérico BR (vírgula decimal, ponto de milhar) para float."""
    s = serie.astype(str).str.strip()
    # remove ponto de milhar somente quando há vírgula decimal
    tem_virgula = s.str.contains(",", regex=False)
    s = s.where(~tem_virgula, s.str.replace(".", "", regex=False))
    s = s.str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce")


def municipio_do_arquivo(caminho: str) -> str:
    nome = os.path.basename(caminho).replace(".csv", "")
    return nome.split(" - ")[-1].strip()


# ---------------------------------------------------------------- 1. CARGA ----
def carregar(pasta: str) -> pd.DataFrame:
    arquivos = sorted(glob.glob(os.path.join(pasta, "*.csv")))
    frames = []
    for caminho in arquivos:
        df = pd.read_csv(caminho, sep=";", dtype=str, encoding="utf-8-sig")
        df["MUNICIPIO"] = municipio_do_arquivo(caminho)
        frames.append(df)
        print(f"  carregado: {municipio_do_arquivo(caminho):<14} {len(df):>6} UCs")
    base = pd.concat(frames, ignore_index=True)

    # tipagem dos campos numéricos
    for c in ["CONSUMOMES", "CONSUMOMES1", "CONSUMOMES2", "CONSUMOMES3",
              "MEDIA", "DIFERENCA", "LEITURA_LIDA", "LEITURA_ATUAL_KWH"]:
        base[c] = parse_num(base[c])
    for c in ["IDNAOLEITURA", "TROCA_MEDIDOR_MES_ATUAL",
              "TROCA_MEDIDOR_MES_SEGUINTE", "IDMOTIVODESLIG"]:
        base[c] = pd.to_numeric(base[c], errors="coerce").fillna(0).astype(int)
    base["LIGADO"] = base["LIGADO"].fillna("").str.strip().str.upper()
    base["COMPETENCIA"] = base["COMPETENCIA"].str.split().str[0]
    return base


# ------------------------------------------------- 2. ENGENHARIA DE ATRIBUTOS --
def engenharia(base: pd.DataFrame) -> pd.DataFrame:
    df = base.copy()
    hist = df[["CONSUMOMES1", "CONSUMOMES2", "CONSUMOMES3"]].fillna(0)
    atual = df["CONSUMOMES"].fillna(0)

    df["media_hist"] = hist.mean(axis=1)
    df["soma_hist"]  = hist.sum(axis=1)
    df["consumo_atual"] = atual

    # nº de meses zerados na janela (atual + 3 anteriores)
    janela = pd.concat([atual, hist["CONSUMOMES1"], hist["CONSUMOMES2"],
                        hist["CONSUMOMES3"]], axis=1)
    df["n_zeros_janela"] = (janela == 0).sum(axis=1)

    # queda relativa vs média histórica (positivo = caiu)
    with np.errstate(divide="ignore", invalid="ignore"):
        df["queda_ratio"] = np.where(df["media_hist"] > 0,
                                     (df["media_hist"] - atual) / df["media_hist"],
                                     0.0)
        df["razao_atual_media"] = np.where(df["media_hist"] > 0,
                                           atual / df["media_hist"], np.nan)
    # coeficiente de variação dos 4 meses
    media4 = janela.mean(axis=1)
    std4 = janela.std(axis=1, ddof=0)
    df["cv"] = np.where(media4 > 0, std4 / media4, 0.0)

    df["troca_medidor"] = ((df["TROCA_MEDIDOR_MES_ATUAL"] == 1) |
                           (df["TROCA_MEDIDOR_MES_SEGUINTE"] == 1)).astype(int)
    df["lido"]   = (df["IDNAOLEITURA"] == 0)
    df["ligado"] = (df["LIGADO"] == "S")
    return df


# ------------------------------------------------------------- 3. REGRAS ------
def aplicar_regras(df: pd.DataFrame) -> pd.DataFrame:
    motivos = [[] for _ in range(len(df))]
    score_regra = np.zeros(len(df))

    atual      = df["consumo_atual"].values
    media      = df["media_hist"].values
    soma_hist  = df["soma_hist"].values
    queda      = df["queda_ratio"].values
    lido       = df["lido"].values
    ligado     = df["ligado"].values
    troca      = df["troca_medidor"].values

    for i in range(len(df)):
        # UC sem leitura no período não é fraude — apenas reagendamento
        if not lido[i]:
            continue

        # R1 - Desligada porém consumindo => possível ligação clandestina
        if (not ligado[i]) and atual[i] > 0:
            motivos[i].append("Consumo registrado com UC desligada (possível ligação clandestina)")
            score_regra[i] += PESO["CLANDESTINA"]

        # As demais regras pressupõem UC ligada
        if ligado[i]:
            # R2 - Zerou tendo histórico
            if atual[i] == 0 and soma_hist[i] > 0:
                motivos[i].append("Consumo zerou no mês corrente tendo histórico anterior")
                score_regra[i] += PESO["QUEDA_ZERO"]

            # R3 - Zero persistente (4 meses) -> pode ser imóvel vago
            elif atual[i] == 0 and soma_hist[i] == 0:
                motivos[i].append("Consumo zero persistente (4 meses) — validar se imóvel vago/sazonal")
                score_regra[i] += PESO["ZERO_PERSISTENTE"]

            # R4/R5 - Quedas relevantes (apenas com consumo > 0 e média relevante)
            elif atual[i] > 0 and media[i] >= CONSUMO_MINIMO_REL:
                if queda[i] >= LIM_QUEDA_BRUSCA:
                    motivos[i].append(f"Queda de consumo de {queda[i]*100:.0f}% vs média (>=60%)")
                    score_regra[i] += PESO["QUEDA_BRUSCA"]
                elif queda[i] >= LIM_QUEDA_MODERADA:
                    motivos[i].append(f"Queda de consumo de {queda[i]*100:.0f}% vs média (40-60%)")
                    score_regra[i] += PESO["QUEDA_MODERADA"]

            # R6 - Troca de medidor acompanhada de queda
            if troca[i] == 1 and queda[i] >= LIM_TROCA_QUEDA and atual[i] > 0:
                motivos[i].append("Troca de medidor acompanhada de queda de consumo")
                score_regra[i] += PESO["TROCA_QUEDA"]

    df = df.copy()
    df["motivos"] = ["; ".join(m) for m in motivos]
    df["score_regra"] = np.minimum(score_regra, 100)
    return df


# ------------------------------------------------ 4. ANOMALIA (ISOLATION FOREST)
def anomalia(df: pd.DataFrame) -> pd.DataFrame:
    feats = pd.DataFrame({
        "consumo_atual": df["consumo_atual"].fillna(0),
        "media_hist":    df["media_hist"].fillna(0),
        "queda_ratio":   df["queda_ratio"].fillna(0),
        "razao":         df["razao_atual_media"].clip(0, 5).fillna(1.0),
        "cv":            df["cv"].fillna(0),
        "n_zeros":       df["n_zeros_janela"].fillna(0),
        "troca":         df["troca_medidor"].fillna(0),
    })
    # treina apenas na população válida (ligada e lida)
    mask = (df["ligado"] & df["lido"]).values
    X = StandardScaler().fit_transform(feats.values)

    modelo = IsolationForest(n_estimators=300, contamination="auto",
                             random_state=RANDOM_STATE, n_jobs=-1)
    modelo.fit(X[mask])
    raw = modelo.score_samples(X)          # menor = mais anômalo
    # normaliza 0..1 (1 = mais anômalo) sobre a população válida
    lo, hi = raw[mask].min(), raw[mask].max()
    anom = (hi - raw) / (hi - lo) if hi > lo else np.zeros_like(raw)
    anom = np.clip(anom, 0, 1)

    df = df.copy()
    df["score_anomalia"] = np.where(mask, anom, 0.0)
    return df


# ----------------------------------------------- 5. SCORE FINAL + PRIORIDADE ---
def priorizar(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["score_final"] = (W_REGRAS * df["score_regra"] +
                         W_ANOMALIA * df["score_anomalia"] * 100).round(1)

    # classificação de situação (o que NÃO entra como suspeita de fraude)
    situacao = np.where(~df["lido"], "SEM_LEITURA",
                np.where((~df["ligado"]) & (df["consumo_atual"] == 0), "DESLIGADA",
                "ANALISAR"))
    df["situacao"] = situacao

    # uma UC é suspeita se alguma regra disparou OU anomalia no topo (>=0.95)
    tem_regra = df["score_regra"] > 0
    anomala   = df["score_anomalia"] >= 0.95
    df["suspeita"] = (df["situacao"] == "ANALISAR") & (tem_regra | anomala)
    df["origem"] = np.where(tem_regra, "regra",
                   np.where(anomala, "anomalia", "-"))

    # marca motivo de anomalia pura (sem regra)
    so_anomalia = df["suspeita"] & (~tem_regra) & anomala
    df.loc[so_anomalia, "motivos"] = "Padrão de consumo anômalo (detecção estatística)"

    def faixa(row):
        if not row["suspeita"]:
            return "-"
        if "clandestina" in row["motivos"].lower():
            return "CRÍTICA"
        if row["score_final"] >= 70:
            return "ALTA"
        if row["score_final"] >= 40:
            return "MÉDIA"
        return "BAIXA"
    df["prioridade"] = df.apply(faixa, axis=1)
    return df


# ---------------------------------------------------------- 6. RELATÓRIO -------
def relatorio(df: pd.DataFrame, caminho_saida: str):
    susp = df[df["suspeita"]].sort_values("score_final", ascending=False)

    colunas = ["MUNICIPIO", "COMPETENCIA", "IDUC", "NOME", "prioridade",
               "score_final", "score_regra", "score_anomalia",
               "consumo_atual", "media_hist", "queda_ratio", "n_zeros_janela",
               "LIGADO", "LEITURA_ATUAL_KWH", "motivos"]
    out = susp[colunas].copy()
    out["score_anomalia"] = (out["score_anomalia"] * 100).round(1)
    out["queda_ratio"] = (out["queda_ratio"] * 100).round(0)
    out = out.rename(columns={"queda_ratio": "queda_pct",
                              "score_anomalia": "score_anomalia_0a100"})
    arq = os.path.join(caminho_saida, "ranking_suspeitas.csv")
    out.to_csv(arq, sep=";", index=False, encoding="utf-8-sig")

    total = len(df)
    sem_leitura = int((df["situacao"] == "SEM_LEITURA").sum())
    desligadas  = int((df["situacao"] == "DESLIGADA").sum())

    print("\n" + "=" * 70)
    print(" RESULTADO DO MOTOR DE DETECÇÃO")
    print("=" * 70)
    print(f"  UCs analisadas .................... {total:>6}")
    print(f"  Excluídas (sem leitura) .......... {sem_leitura:>6}  -> reagendar leitura")
    print(f"  Excluídas (desligadas s/ consumo)  {desligadas:>6}  -> situação normal")
    n_regra = int((susp["origem"] == "regra").sum())
    n_anom  = int((susp["origem"] == "anomalia").sum())
    print(f"  SUSPEITAS PARA INSPEÇÃO .......... {len(susp):>6}")
    print(f"     por regra determinística ...... {n_regra:>6}")
    print(f"     somente por anomalia (top 5%) . {n_anom:>6}")
    print("-" * 70)
    print("  Por prioridade:")
    for p in ["CRÍTICA", "ALTA", "MÉDIA", "BAIXA"]:
        n = int((susp["prioridade"] == p).sum())
        if n:
            print(f"     {p:<9} {n:>5}")
    print("-" * 70)
    print("  Por município:")
    for m, n in susp["MUNICIPIO"].value_counts().items():
        print(f"     {m:<14} {n:>5}")
    print("-" * 70)
    print("  TOP 10 prioridades de inspeção:")
    top = susp.head(10)
    for _, r in top.iterrows():
        nome = (r["NOME"] or "")[:24]
        print(f"     [{r['prioridade']:<7}] {r['score_final']:>5.1f} | "
              f"{r['MUNICIPIO']:<11} | UC {r['IDUC']:<11} | {nome:<24} | "
              f"{r['motivos'][:60]}")
    print("=" * 70)
    print(f"\n  Ranking completo salvo em: {arq}")
    print(f"  ({len(susp)} UCs suspeitas, ordenadas por score)")


# ------------------------------------------------------------------ MAIN -------
def main():
    print("Carregando dados (somente BT)...")
    base = carregar(PASTA_DADOS)
    print("Calculando atributos...")
    df = engenharia(base)
    print("Aplicando regras determinísticas...")
    df = aplicar_regras(df)
    print("Treinando detector de anomalia (Isolation Forest)...")
    df = anomalia(df)
    print("Combinando scores e priorizando...")
    df = priorizar(df)
    relatorio(df, PASTA_SAIDA)


if __name__ == "__main__":
    main()
