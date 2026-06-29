# Ideation — 6 Ideas

## Overview
6 product ideas geradas para resolver PS #1 (Perdas) e PS #2 (Consumidor Engagement).

---

## Idea #1: Software Task as a Service

**Description:** Transformar cadastro de consumidor/unidade consumidora de formulário tradicional para conversacional. Usuário manda documento + conversa com sistema em vez de preencher 20 campos.

**Problem it solves:**
- Cláudio (técnico) passa ~50% do tempo preenchendo formulários ao invés de resolver problemas
- Erro manual em cadastro → fonte de fraude/adulteração
- Fricção operacional gigante

**Maps to:** PS #1 (Perdas) — indiretamente (menos erro, libera tempo), PS #2 (Consumidor) — operacional

**Viability:** 🟡 Médio — design-heavy, 2-3 dias de prototipagem

**Differentiator:** ALTO — ninguém no setor faz isso bem. Fundacional (extensível a todo sistema).

**Evidence:** 63 tickets E2 Comercial sobre cadastro/integração

---

## Idea #2: Leitura Online (Real-time Metering)

**Description:** Aproveitar medidores digitais instalados nas unidades consumidoras para trazer leituras em tempo real, habilitando visibilidade e alertas contínuos.

**Problem it solves:**
- Hoje leitura é manual/mensal → não há visibilidade de picos ou anomalias
- Consumidor não sabe consumo real até fatura chegar
- Perdas/fraudes não são detectadas em tempo real

**Maps to:** PS #1 (Perdas) — detecção em tempo real, PS #2 (Consumidor) — transparência imediata

**Viability:** 🟡 Médio — depende de infraestrutura de medidor inteligente

**Differentiator:** Médio — agregadoras já fazem isso

**Evidence:** Entrevista CERTEL: "monitoramento em tempo real do consumo é ferramenta estratégica"

---

## Idea #3: Agentes de Cobrança Automáticos

**Description:** Automatizar decisão de corte de energia. Ao invés de Cláudio analisar manualmente quais consumidores devem ter corte (múltiplas variáveis: dias vencido, padrão histórico, inadimplência prévia, tipo de cliente), o sistema recomenda/executa com base em regras e histórico.

**Problem it solves:**
- Cobrança hoje é manual e baseada em regras simples (ex: 30 dias vencido = corte)
- Não leva em conta contexto (ex: cliente que sempre paga atrasado mas paga)
- Cláudio gasta tempo analisando cada caso individualmente

**Maps to:** PS #1 (Perdas) — reduz inadimplência, PS #2 (Consumidor) — comunicação estruturada

**Viability:** 🟢 Alto — automação pura, viável em 2-3 dias

**Differentiator:** Médio — workflow padrão, execução boa

**Evidence:** Processo regulatório real (distribuidor precisa fazer avisos antes de corte)

---

## Idea #4: Agente de Detecção de Fraude

**Description:** Identificar anomalias que indicam fraude: consumidores classificados como "baixa renda" com consumo muito superior ao padrão, furtos (ligações clandestinas), desvio de energia, adulterações de medidor. Sistema analisa medição + faturamento + GD integrado.

**Problem it solves:**
- Perdas não técnicas comem R$ 3,3B/ano no setor
- Hoje detecção é reativa (auditor encontra) ou baseada em denuncia
- Cláudio não tem visibilidade de padrões de fraude

**Maps to:** PS #1 (Perdas) — CRÍTICO direto

**Viability:** 🟢 Alto — ML puro, pode começar com dados históricos

**Differentiator:** ALTO — integração medição+faturamento+GD poucos fazem bem

**Evidence:** R$ 3,3B em perdas não técnicas (insights), Equatorial CEO: "perdas são gargalo econômico"

---

## Idea #5: Avisos Ativos ao Consumidor (Consumo & Educação)

**Description:** Sistema envia alertas proativos ao consumidor final: "seu consumo está 30% acima do normal", "picos em X horário", "oportunidade de reduzir consumo com Y ação". Educação contínua sobre consumo.

**Problem it solves:**
- Consumidor só vê consumo quando fatura chega (reativo)
- Agregadora oferece app em tempo real → consumidor sai para lá
- Distribuidor perde retenção (churn silencioso)

**Maps to:** PS #2 (Consumidor) — CRÍTICO direto

**Viability:** 🟢 Alto — rápido de prototipar (1 dia), requer UI simples

**Differentiator:** Médio — agregadoras já fazem, mas distribuidor não oferece bem

**Evidence:** Entrevista CERTEL: "monitoramento em tempo real... para aproximar distribuidora do consumidor"; insights: mercado livre abre ago 2026

---

## Idea #6: Monitoramento Climático & Rede Proativa

**Description:** Monitorar dados climáticos (tempestades, eventos extremos) e alertar gestor técnico pra se preparar. Além disso, comunicar proativamente ao consumidor: "identificamos risco de queda de energia por tempestade, estamos acompanhando". Reduz surpresa, aumenta confiança.

**Problem it solves:**
- Eventos climáticos extremos causam falhas de rede (picos 20x volume normal)
- Distribuidor reage depois que cai → consumidor furioso
- Consumidor fica sem energia sem aviso previo

**Maps to:** PS #1 (Perdas) — reduz falhas não técnicas, PS #2 (Consumidor) — comunicação proativa, confiança

**Viability:** 🟡 Médio — depende de dados climáticos externos, integração com SCADA

**Differentiator:** Alto — diferencia na comunicação proativa

**Evidence:** Insights: "eventos climáticos extremos, picos 20x acima do volume normal"

---

## Ranking por Impacto + Viabilidade

| Rank | Idea | PS1 | PS2 | Viability | Speed | Differentiator | Comment |
|------|------|-----|-----|-----------|-------|---|---|
| 🔴 1 | #5 (Avisos Consumidor) | 🟡 Med | 🟢 HIGH | 🟢 HIGH | 1 day | Med (aggregators do it) | Fast to sell, immediate impact |
| 🔴 2 | #4 (Fraude Detection) | 🟢 HIGH | 🟢 Med | 🟢 HIGH | 2 days | HIGH (integration angle) | R$ 3.3B impact, foundational |
| 🟡 3 | #3 (Cobrança Agents) | 🟢 MED | 🟡 Med | 🟢 HIGH | 2 days | Med | Automation, regulatory fit |
| 🟡 4 | #2 (Real-time Metering) | 🟡 Med | 🟢 HIGH | 🟡 Med | 2 days | Med (aggregators do it) | Infrastructure dependent |
| 🟡 5 | #1 (Task as a Service) | 🟡 Med | 🟡 Med | 🟡 Med | 2-3 days | HIGH (transformational) | Design-heavy, foundational |
| 🟡 6 | #6 (Climate Monitoring) | 🟡 Med | 🟢 HIGH | 🟡 Med | 2-3 days | HIGH (proactive comms) | External data dependency |

---

## Strategic Paths Forward

### **Path A: Fast Sell (2 days)**
1. **Day 1-2:** Prototype #5 (Avisos Consumidor)
   - Resolves PS #2 directly
   - Quick to show impact
   - Consumer-facing (visible demo)

**Output:** 1 solid prototype ready to pitch

---

### **Path B: Comprehensive (4 days)**
1. **Day 1-2:** Prototype #5 (Avisos Consumidor) — solid
2. **Day 3-4:** Start #1 (Task as Service) — direction + exploration

**Output:** 1 production-ready, 1 exploration

---

### **Path C: Parallel (if team available)**
1. **You focus on:** #5 (Avisos Consumidor) or #4 (Fraude)
2. **Teammate focus on:** #1 (Task as Service) or #4/6

**Output:** 2 prototypes, shallow or solid depending on resource split

---

## Notes

- **#5 is easy to sell:** Problem is felt (Jonas knows aggregator threat), solution is simple (shows in 30 sec), result is fast (weeks not months)
- **#4 is hard to sell but huge impact:** Problem is invisible (6.6% lost), solution is complex (ML + integration), result takes time (3-6 months)
- **#1 is transformational but time-consuming:** Design-heavy, not immediately visible impact, but changes how entire system is used
- **Choose based on:**
  - 2-day sprint? → #5 only
  - 4-day sprint? → #5 + #1 sequential
  - Team available? → #5 + #4 parallel

---

**Date:** 23 de junho de 2026  
**Workshop Stage:** Day 2 — Ideation  
**Next:** Choose path, start prototyping
