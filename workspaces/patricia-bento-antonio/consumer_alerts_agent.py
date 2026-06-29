#!/usr/bin/env python3
"""
Agente de Avisos ao Consumidor — Detecta anomalias e gera alertas
"""

import json
from datetime import datetime, timedelta
import statistics
import anthropic

# ============================================================================
# STAGE 1: Synthetic Data Generation
# ============================================================================

def generate_synthetic_consumption(
    consumer_id: str,
    consumer_type: str = "residential",
    days: int = 30,
    has_solar: bool = False,
    anomaly_on_day: int = None,  # Dia em que forçar anomalia
    anomaly_type: str = "spike"   # "spike" ou "sustained"
) -> list:
    """
    Gera série histórica realista de consumo (horário)
    """
    consumption = []
    base_consumption = {
        "residential": 3.0,
        "commercial": 15.0,
        "industrial": 50.0,
        "prosumer_gd": 2.0,
    }

    base = base_consumption.get(consumer_type, 3.0)

    start_date = datetime.now() - timedelta(days=days)

    for day_offset in range(days):
        current_date = start_date + timedelta(days=day_offset)

        for hour in range(24):
            # Padrão base com variação diária
            hour_factor = 0.6 if 0 <= hour <= 6 else (1.2 if 12 <= hour <= 18 else 0.9)
            daily_variation = 0.9 + (day_offset % 7) * 0.05  # Padrão semanal

            kwh = base * hour_factor * daily_variation

            # Add noise
            import random
            kwh += random.gauss(0, kwh * 0.1)

            # Força anomalia em dia específico
            if anomaly_on_day is not None and day_offset == anomaly_on_day:
                if anomaly_type == "spike":
                    if 13 <= hour <= 18:  # Spike 13h-18h
                        kwh *= 4.0  # 4x mais para garantir > 30%
                elif anomaly_type == "sustained":
                    kwh *= 2.5  # Sustained 2.5x (150% acima)

            consumption.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "hour": hour,
                "kwh": round(max(0.1, kwh), 2)
            })

    return consumption


def generate_consumer_profiles(count: int = 3) -> list:
    """
    Gera perfis de consumidores realistas
    """
    profiles = [
        {
            "id": "CERTEL_0001",
            "name": "João Silva",
            "type": "residential",
            "has_solar": True,
            "solar_capacity_kwp": 5.0,
            "location": "São Paulo",
            "consumption": generate_synthetic_consumption(
                "CERTEL_0001",
                "residential",
                days=30,
                has_solar=True,
                anomaly_on_day=28,
                anomaly_type="spike"
            )
        },
        {
            "id": "CERTEL_0002",
            "name": "Empresa Logística XYZ",
            "type": "commercial",
            "has_solar": False,
            "solar_capacity_kwp": 0,
            "location": "Guarulhos",
            "consumption": generate_synthetic_consumption(
                "CERTEL_0002",
                "commercial",
                days=30,
                has_solar=False,
                anomaly_on_day=25,
                anomaly_type="sustained"
            )
        },
        {
            "id": "CERTEL_0003",
            "name": "Maria Santos",
            "type": "residential",
            "has_solar": False,
            "solar_capacity_kwp": 0,
            "location": "Campinas",
            "consumption": generate_synthetic_consumption(
                "CERTEL_0003",
                "residential",
                days=30,
                has_solar=False,
                anomaly_on_day=22,
                anomaly_type="spike"
            )
        }
    ]

    return profiles[:count]


# ============================================================================
# STAGE 2: Anomaly Detection
# ============================================================================

def detect_anomaly(
    consumer_profile: dict,
    threshold_pct: int = 30
) -> dict:
    """
    Detecta anomalia no consumo do consumidor
    (aumento > threshold_pct)
    """
    consumption = consumer_profile["consumption"]

    # Consumo das ultimas 24h (hoje)
    today_consumption = [c["kwh"] for c in consumption[-24:]]

    # Consumo dos ultimos 30 dias (exceto hoje)
    hist_consumption = [c["kwh"] for c in consumption[:-24]]

    if not hist_consumption or not today_consumption:
        return {
            "is_anomaly": False,
            "anomaly_type": None,
            "metrics": {}
        }

    # Estatisticas
    avg_30d = statistics.mean(hist_consumption)
    avg_today = statistics.mean(today_consumption)
    max_today = max(today_consumption)
    max_hour_today = consumption[-24 + today_consumption.index(max_today)]["hour"]

    # Detecta tipos de anomalia (SOMENTE AUMENTO)
    increase_pct = ((avg_today - avg_30d) / avg_30d) * 100 if avg_30d > 0 else 0
    spike_increase = ((max_today - avg_30d) / avg_30d) * 100 if avg_30d > 0 else 0

    is_anomaly = False
    anomaly_type = None

    # Anomalia = AUMENTO significativo
    if increase_pct > threshold_pct:
        is_anomaly = True
        anomaly_type = "sustained"

    if spike_increase > threshold_pct and not is_anomaly:
        is_anomaly = True
        anomaly_type = "spike"

    return {
        "is_anomaly": is_anomaly,
        "anomaly_type": anomaly_type,
        "metrics": {
            "avg_30d": round(avg_30d, 2),
            "avg_today": round(avg_today, 2),
            "increase_pct": round(increase_pct, 1),
            "max_today": round(max_today, 2),
            "max_hour_today": max_hour_today,
            "spike_increase": round(spike_increase, 1),
        }
    }


# ============================================================================
# STAGE 3: Agente LLM — Gerar Alerta Personalizado
# ============================================================================

def generate_alert_with_claude(
    consumer_profile: dict,
    anomaly_result: dict,
    use_mock: bool = True
) -> str:
    """
    Usa Claude para gerar alerta personalizado e amigável
    (ou mockado se use_mock=True)
    """

    if not anomaly_result["is_anomaly"]:
        return None

    metrics = anomaly_result["metrics"]
    consumer_type = consumer_profile["type"]
    has_solar = consumer_profile["has_solar"]
    anomaly_type = anomaly_result["anomaly_type"]

    # Se mockado: gera template realista
    if use_mock:
        # Para spike, usa a leitura do pico (max_hour)
        spike_pct = metrics['spike_increase'] if anomaly_type == "spike" else metrics['increase_pct']

        if has_solar and anomaly_type == "spike":
            return f"Pico de consumo detectado as {metrics['max_hour_today']}h ({spike_pct:.0f}% acima). Seu painel solar pode ajudar!"
        elif consumer_type == "commercial" and anomaly_type == "sustained":
            return f"Consumo {spike_pct:.0f}% acima do esperado. Verifique equipamentos para reduzir gastos."
        else:
            return f"Pico de consumo as {metrics['max_hour_today']}h ({spike_pct:.0f}% acima da media). Desligue equipamentos desnecessarios."

    # Versao real com Claude API
    prompt = f"""Voce e assistente de uma distribuidora de energia.
Detectamos uma anomalia no consumo de um cliente.

CLIENTE: {consumer_profile['name']}
TIPO DE ANOMALIA: {anomaly_type.upper()}

DADOS:
- Consumo medio (ultimos 30 dias): {metrics['avg_30d']} kWh
- Consumo hoje: {metrics['avg_today']} kWh
- Aumento: {metrics['increase_pct']}% acima da media
{f"- Pico as {metrics['max_hour_today']}h: {metrics['max_today']} kWh" if anomaly_type == "spike" else ""}

CONTEXTO CLIENTE:
Tipo: {consumer_type}
{f"Painel solar: {consumer_profile['solar_capacity_kwp']} kWp" if has_solar else "Sem painel solar"}

TAREFA: Gere uma mensagem AMIGAVEL e CURTA (max 160 caracteres) que:
1. Avisa sobre a anomalia (nao-assustadora)
2. Sugere acao pratica:
   - Painel solar: mencione compensacao
   - Pico horario: verifique equipamentos
3. Tom: casual, educativo

Responda APENAS COM a mensagem."""

    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.content[0].text.strip()


# ============================================================================
# PIPELINE COMPLETO
# ============================================================================

def run_alert_pipeline(consumer_profile: dict) -> dict:
    """
    Executa pipeline completo: detecta + gera alerta
    """
    anomaly_result = detect_anomaly(consumer_profile)

    alert_message = None
    if anomaly_result["is_anomaly"]:
        alert_message = generate_alert_with_claude(consumer_profile, anomaly_result)

    return {
        "consumer_id": consumer_profile["id"],
        "consumer_name": consumer_profile["name"],
        "is_anomaly": anomaly_result["is_anomaly"],
        "anomaly_type": anomaly_result["anomaly_type"],
        "metrics": anomaly_result["metrics"],
        "alert_message": alert_message,
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("AGENTE DE AVISOS AO CONSUMIDOR - Prototipo")
    print("="*70)

    # Gera consumidores
    print("\n[1] Gerando dados sinteticos...")
    consumers = generate_consumer_profiles(count=3)
    print(f"OK: {len(consumers)} consumidores gerados")

    # Roda pipeline
    print("\n[2] Detectando anomalias e gerando alertas...\n")
    results = []

    for consumer in consumers:
        print(f"Processando: {consumer['name']} ({consumer['id']})...")
        result = run_alert_pipeline(consumer)
        results.append(result)

        if result["is_anomaly"]:
            print(f"  OK ANOMALIA DETECTADA: {result['anomaly_type'].upper()}")
            print(f"    Consumo medio: {result['metrics']['avg_30d']} kWh")
            print(f"    Consumo hoje: {result['metrics']['avg_today']} kWh")
            print(f"    Aumento: {result['metrics']['increase_pct']}%")
            print(f"  ALERTA gerado:")
            print(f"    \"{result['alert_message']}\"\n")
        else:
            print(f"  OK Sem anomalias detectadas\n")

    # Salva resultado
    print("\n[3] Salvando resultado para analise...")
    with open("alerts_output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("OK Alertas salvos em alerts_output.json")

    print("\n" + "="*70)
    print(f"Pipeline concluido: {sum(1 for r in results if r['is_anomaly'])} anomalias detectadas")
    print("="*70)
