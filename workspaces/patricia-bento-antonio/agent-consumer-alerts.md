# Agente de Avisos ao Consumidor — Especificação

## Overview

**Agente:** Detector de Anomalias + Gerador de Alertas Personalizados  
**Objetivo:** Monitorar consumo de energia do consumidor em tempo real (ou batch diário) e enviar alerta inteligente quando detectar anomalia.  
**Resultado esperado:** SMS/email/portal mostrando aviso personalizado ao consumidor.

---

## Agente: Como Funciona

### **Stage 1: Detecção de Anomalia**

**Input:**
```
{
  "consumer_id": "CERTEL_0001",
  "consumer_type": "residential",  # residential, commercial, industrial, prosumer_gd
  "consumption_history": [
    {"date": "2026-06-01", "hour": 0, "kwh": 1.2},
    {"date": "2026-06-01", "hour": 1, "kwh": 1.1},
    ...
    {"date": "2026-06-20", "hour": 14, "kwh": 5.8}  # Today
  ],
  "has_solar_panel": true,
  "solar_generation_today": 3.2  # kWh gerado
}
```

**Logic:**
1. Calcula média de consumo dos últimos 30 dias
2. Detecta se consumo de hoje/agora é **> 30% acima da média**
3. Se sim, marca como **"anomaly"** + tipo (spike, sustained, pico horário)

**Output:**
```json
{
  "is_anomaly": true,
  "anomaly_type": "spike",  # spike | sustained | peak_hour
  "consumption_today": 5.8,
  "avg_consumption": 4.2,
  "increase_pct": 38,
  "context": {
    "solar_generation": 3.2,
    "solar_potential_today": 5.0,
    "weather": "sunny"  # Optional: se tiver integração
  }
}
```

---

### **Stage 2: Agente LLM — Gerar Alerta Personalizado**

**Input:** Resultado da Stage 1 + dados do consumidor

**Prompt pra LLM:**
```
Você é assistente de uma distribuidora de energia. 
Detectamos uma anomalia no consumo do consumidor [NOME].

Fatos:
- Consumo hoje: 5.8 kWh (38% acima da média)
- Tipo de consumidor: residencial com painel solar
- Geração solar hoje: 3.2 kWh (potencial: 5.0 kWh)
- Tipo de anomalia: spike

Gere uma mensagem AMIGÁVEL e CURTA (máx 160 caracteres pra SMS) que:
1. Avisa sobre a anomalia
2. Sugere ação se aplicável (ex: "Verifique ar condicionado" ou "Ative compensação de GD")
3. NÃO é assustadora, NÃO é spam

Saída: Só a mensagem, nada mais.
```

**Output (Exemplo):**
```
"Seu consumo hoje foi 38% acima do normal. Verifique equipamentos ligados. 
Seu painel solar pode compensar 3.2 kWh — ative em nosso app!"
```

---

## Estrutura de Dados

### **Input esperado: Arquivo CSV ou JSON com série histórica**

```csv
consumer_id,date,hour,kwh,consumer_type,has_solar
CERTEL_0001,2026-05-21,0,1.2,residential,true
CERTEL_0001,2026-05-21,1,1.1,residential,true
CERTEL_0001,2026-05-21,2,0.9,residential,true
...
CERTEL_0001,2026-06-20,14,5.8,residential,true
CERTEL_0002,2026-05-21,0,8.5,commercial,false
CERTEL_0002,2026-05-21,1,8.3,commercial,false
...
```

**Mínimo de dados:**
- 1 mês de histórico (30+ dias)
- 1-5 consumidores reais
- Granularidade: horária (ou diária, se for isso que você tem)

---

## Componentes do Código

### **1. Anomaly Detector**
```python
def detect_anomaly(consumption_history, threshold_pct=30):
    """
    Input: lista de (date, hour, kwh)
    Output: (is_anomaly, anomaly_type, metrics)
    """
    avg_30d = mean(consumption_history[-720:])  # Últimos 30 dias
    today_consumption = consumption_history[-24:]  # Últimas 24h
    
    if mean(today_consumption) > avg_30d * (1 + threshold_pct/100):
        return True, "sustained", {...}
    
    # Check for spike (pico horário)
    if max(today_consumption) > avg_30d * (1 + threshold_pct/100):
        return True, "spike", {...}
    
    return False, None, {}
```

### **2. Agente LLM (Claude)**
```python
def generate_alert(anomaly_data, consumer_data):
    """
    Input: anomaly detection result + consumer context
    Output: alerta em linguagem natural (SMS/email)
    """
    prompt = f"""
    Você é assistente de uma distribuidora de energia.
    Consumidor: {consumer_data['name']}
    Anomalia: {anomaly_data['anomaly_type']} ({anomaly_data['increase_pct']}% acima da média)
    Contexto: {consumer_data['context']}
    
    Gere alerta amigável, máx 160 caracteres.
    """
    
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text
```

### **3. Pipeline End-to-End**
```python
def run_alert_pipeline(consumption_data, consumer_data):
    # Stage 1: Detect
    is_anomaly, anom_type, metrics = detect_anomaly(
        consumption_data['history']
    )
    
    if not is_anomaly:
        return None  # No alert
    
    # Stage 2: Generate Alert
    alert_message = generate_alert(
        {"anomaly_type": anom_type, **metrics},
        consumer_data
    )
    
    # Stage 3: Return alert (ready to send)
    return {
        "consumer_id": consumer_data['id'],
        "message": alert_message,
        "channel": "sms" if len(alert_message) < 160 else "email",
        "timestamp": now()
    }
```

---

## MVP (Minimum Viable Product) — 1 dia

**Escopo:**
1. ✅ Anomaly detection (regra simples: 30% threshold)
2. ✅ LLM agente gerando 3 alertas de exemplo
3. ✅ Mockup de UI (consumidor vê alerta)
4. ❌ Integração real (SMS, email, API)
5. ❌ Dashboard de configuração

**Entrada:** 1-2 consumidores com 30 dias de histórico (real ou sintético)  
**Saída:** 3 exemplos de alertas + screenshot da UI

---

## Próximos Passos

1. **Você encontra dados reais de consumo** → a gente roda com esses
2. **Ou você diz "vamos usar sintéticos"** → a gente gera 1 mês de dados realistas
3. Eu codo o agente em Python
4. Testamos com dados reais/sintéticos
5. Mockamos a UI (portal/app mostrando alertas)

---

**Data:** 24 de junho de 2026  
**Status:** Aguardando dados de consumo  
**Próximo:** Decidir entre dados reais ou sintéticos
