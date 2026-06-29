#!/usr/bin/env python3
"""
Agente de Avisos ao Consumidor — com dados REAIS de consumo
Processa dados de 3 cidades (Criciuma, Forquilhinha, Nova Veneza)
Detecta anomalias mensais e gera alertas personalizados
"""

import pandas as pd
import json
import glob
import numpy as np
from datetime import datetime
import anthropic

# ============================================================================
# STAGE 1: Carregar e processar dados reais
# ============================================================================

def load_real_data():
    """
    Carrega dados dos 3 CSVs reais
    """
    files = glob.glob(r"C:\Users\patricia.bento\Downloads\Análise de leitura - meses anteriores-Padrão*.csv")

    all_data = []

    for file in files:
        # Extrair nome da cidade
        city = file.split(" - ")[-1].replace(".csv", "")

        # Ler CSV
        df = pd.read_csv(file, sep=';', encoding='utf-8-sig')

        # Converter para numérico
        df['CONSUMOMES'] = pd.to_numeric(df['CONSUMOMES'], errors='coerce')
        df['MEDIA'] = pd.to_numeric(df['MEDIA'], errors='coerce')
        df['CONSUMOMES1'] = pd.to_numeric(df['CONSUMOMES1'], errors='coerce')
        df['CONSUMOMES2'] = pd.to_numeric(df['CONSUMOMES2'], errors='coerce')
        df['CONSUMOMES3'] = pd.to_numeric(df['CONSUMOMES3'], errors='coerce')

        # Calcular variação
        df['VARIACAO_PCT'] = ((df['CONSUMOMES'] - df['MEDIA']) / df['MEDIA'] * 100).fillna(0)
        df['VARIACAO_PCT'] = df['VARIACAO_PCT'].replace([np.inf, -np.inf], 0)

        # Adicionar cidade e dados de origem
        df['CIDADE'] = city
        df['DATA_ANALISE'] = datetime.now().strftime("%Y-%m-%d")

        all_data.append(df)

    return pd.concat(all_data, ignore_index=True)


# ============================================================================
# STAGE 2: Detecção de anomalias
# ============================================================================

def detect_anomalies(df, threshold_pct=30):
    """
    Detecta consumidores com variação > threshold_pct
    """
    anomalias = df[df['VARIACAO_PCT'] > threshold_pct].copy()

    # Classificar por severidade
    anomalias['SEVERIDADE'] = 'ALTO'
    anomalias.loc[anomalias['VARIACAO_PCT'] <= 50, 'SEVERIDADE'] = 'MÉDIO'
    anomalias.loc[anomalias['VARIACAO_PCT'] <= 100, 'SEVERIDADE'] = 'MÉDIO'
    anomalias.loc[anomalias['VARIACAO_PCT'] > 100, 'SEVERIDADE'] = 'CRÍTICO'

    return anomalias.sort_values('VARIACAO_PCT', ascending=False)


# ============================================================================
# STAGE 3: Agente LLM — Gerar alertas personalizados
# ============================================================================

def generate_alert_with_claude(consumer_data, use_mock=True):
    """
    Gera alerta personalizado usando Claude LLM
    """

    nome = consumer_data['NOME']
    consumo_atual = consumer_data['CONSUMOMES']
    media = consumer_data['MEDIA']
    variacao = consumer_data['VARIACAO_PCT']
    cidade = consumer_data['CIDADE']
    mes1 = consumer_data['CONSUMOMES1']
    mes2 = consumer_data['CONSUMOMES2']
    mes3 = consumer_data['CONSUMOMES3']

    # Mock: gerar template realista
    if use_mock:
        if variacao > 200:
            return f"ALERTA CRÍTICO: Seu consumo este mês foi {variacao:.0f}% acima da média. " \
                   f"Consumo: {consumo_atual:.0f} kWh vs. Média: {media:.0f} kWh. " \
                   f"Verifique equipamentos e vazamentos imediatamente."
        elif variacao > 100:
            return f"Atenção: Aumento significativo de {variacao:.0f}% no seu consumo. " \
                   f"Este mês: {consumo_atual:.0f} kWh. Média: {media:.0f} kWh. " \
                   f"Verifique ar-condicionado e chuveiro elétrico."
        else:
            return f"Consumo aumentou {variacao:.0f}% este mês ({consumo_atual:.0f} kWh). " \
                   f"Média histórica: {media:.0f} kWh. Dicas: reduz climatização, use água fria."

    # Versão real com Claude (quando tiver API key)
    prompt = f"""Você é assistente de uma distribuidora de energia.
Detectamos anomalia no consumo de um cliente.

CLIENTE: {nome} ({cidade})
CONSUMO ESTE MÊS: {consumo_atual:.0f} kWh
MÉDIA ÚLTIMOS 3 MESES: {media:.0f} kWh
AUMENTO: {variacao:.0f}%

HISTÓRICO:
- 3 meses atrás: {mes3:.0f} kWh
- 2 meses atrás: {mes2:.0f} kWh
- 1 mês atrás: {mes1:.0f} kWh

Gere uma mensagem PROFISSIONAL e ÚTIL (máx 150 caracteres) que:
1. Alerta sobre a anomalia sem assustar
2. Sugere ação específica baseado na magnitude
3. Oferece suporte

Responda APENAS COM a mensagem."""

    try:
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    except Exception as e:
        # Fallback se API não tiver credencial
        return f"Consumo aumentou {variacao:.0f}% ({consumo_atual:.0f} kWh vs {media:.0f} kWh). Verificar equipamentos."


# ============================================================================
# PIPELINE COMPLETO
# ============================================================================

def run_pipeline(limit=None):
    """
    Executa pipeline completo: carrega dados → detecta anomalias → gera alertas
    """

    print("="*80)
    print("AGENTE DE AVISOS AO CONSUMIDOR — Dados Reais")
    print("="*80)

    # Stage 1: Carregar dados
    print("\n[1] Carregando dados reais...")
    df = load_real_data()
    print(f"✓ {len(df):,} consumidores carregados de 3 cidades")

    # Stage 2: Detectar anomalias
    print("\n[2] Detectando anomalias (> 30%)...")
    anomalias = detect_anomalies(df, threshold_pct=30)
    print(f"✓ {len(anomalias)} consumidores com variação significativa")

    # Stage 3: Gerar alertas
    print("\n[3] Gerando alertas personalizados...\n")

    results = []
    limit = limit or len(anomalias)

    for idx, (_, row) in enumerate(anomalias.head(limit).iterrows()):
        alert_msg = generate_alert_with_claude(row, use_mock=True)

        result = {
            "id": idx + 1,
            "consumidor": row['NOME'],
            "cidade": row['CIDADE'],
            "consumo_atual": float(row['CONSUMOMES']),
            "media_3m": float(row['MEDIA']),
            "variacao_pct": float(row['VARIACAO_PCT']),
            "severidade": row['SEVERIDADE'],
            "historico": {
                "mes1": float(row['CONSUMOMES1']) if pd.notna(row['CONSUMOMES1']) else 0,
                "mes2": float(row['CONSUMOMES2']) if pd.notna(row['CONSUMOMES2']) else 0,
                "mes3": float(row['CONSUMOMES3']) if pd.notna(row['CONSUMOMES3']) else 0,
            },
            "alerta": alert_msg,
            "timestamp": datetime.now().isoformat()
        }

        results.append(result)

        # Print resultado
        print(f"{idx+1:3d}. {row['NOME'][:35]:35s} | {row['CONSUMOMES']:6.0f} kWh | {row['VARIACAO_PCT']:+7.1f}%")
        print(f"     {alert_msg[:70]}...")
        print()

    # Salvar resultados
    print("\n[4] Salvando resultados...")
    output_file = "alerts_real_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"✓ {len(results)} alertas salvos em {output_file}")

    # Salvar dataset completo de anomalias
    csv_file = "anomalias_consumo.csv"
    anomalias.to_csv(csv_file, index=False, encoding='utf-8')
    print(f"✓ Dataset completo salvo em {csv_file}")

    return results, anomalias


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    results, anomalias_df = run_pipeline(limit=20)

    print("\n" + "="*80)
    print(f"Pipeline completo: {len(results)} alertas gerados")
    print("="*80)
    print("\nPróximos passos:")
    print("1. Enviar alertas aos consumidores (SMS/Email/Push)")
    print("2. Carregar dados no portal (alerts-portal-real.html)")
    print("3. Monitorar taxa de resposta/ação")
    print("4. Refinar detecção baseado em feedback")
