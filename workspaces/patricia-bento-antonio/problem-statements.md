# Problem Statements & How Might We

## Problem Statement #1: Perdas Não-Técnicas Comem Margem Sem Visibilidade

**Owner:** Jonas — Gerente de Relações com Consumidor / Diretor Operacional (distribuidora pequena/cooperativa)

**Problem:** Gerentes de operação em distribuidoras pequenas/cooperativas têm **perdas não-técnicas (fraude, furtos, adulterações) que consomem 6.6% da energia injetada (R$ 3,3B no setor)**. Mas eles não conseguem **identificar padrões, culpados, ou reduzir de forma sistemática** porque:

- Dados de medição, faturamento e GD estão desintegrados
- ANEEL mudou em março 2025 pra calcular por "mercado medido" — seu sistema ainda usa "mercado faturado"
- Não têm visibilidade de onde estão as perdas (qual consumidor? qual transformador? qual tipo de fraude?)
- Cada 1% de redução volta direto na margem — é financeiro, não operacional

**Impact:** Margens comprimidas. Distribuidoras não conseguem investir em modernização (Lei 15.269, GD, medição inteligente) porque perdas estão comendo o fundo.

**Evidence:**
- Equatorial CEO (Augusto Miranda): "As perdas no sistema elétrico seguem entre os gargalos do setor, tema com peso estratégico para as concessionárias porque afeta a sustentabilidade econômico-financeira da operação" — Movimento Econômico 2026 (insights, linha 137)
- 63 tickets em E2 COMERCIAL sobre faturamento/integração/GD (dashboard-tickets-800.html)
- R$ 3,3 bilhões que distribuidoras arcam com perdas anuais (insights, linha 175)
- ANEEL resolution 1.148/2026 mudança cálculo (insights, linha 183)

---

### HMW: Reduzir Perdas

**How Might We** identificar padrões de fraude/adulteração em tempo real e conectar medição + faturamento + GD numa visão única?

**Sub-questions:**
1. How Might We **detectar padrões de fraude/adulteração em tempo real** (não retrospectivo)?
2. How Might We **quantificar impacto de cada tipo de perda** (furto vs. fraude vs. erro de medição vs. inadimplência)?
3. How Might We **recomendar ação específica** (qual consumidor, qual transformador, qual investigação)?
4. How Might We **medir redução de perdas mensalmente** e reportar pro CFO/CEO?

**Focus:** #1 + #4 (detect + measure)

---

### AI Ladder: Perdas

| Rung | Description | Useall Implementation |
|------|-------------|----------------------|
| **1. Visibility** | Mostrar o problema | Dashboard mensal: "Você tem X% de perdas, R$ Y, tipo Z de fraude" |
| **2. Productivity** | Ajuda manual | Jonas consegue explorar dados, fazer filtros, ver por consumidor/transformador/tipo |
| **3. Automation** | Roda sozinho, humano aprova | Sistema detecta anomalia, sugere ação ("esse consumidor tem consumo 5x acima, investigar"), Jonas aprova/rejeita |
| **4. Autonomy** | Roda e escalona exceções | Sistema executa ação padrão (gera alerta regulatório, bloqueia conexão clandestina), escalona exceção pra Jonas |

**Recommendation:** Start with **Visibility + Productivity** (MVP). Aim for **Automation** (competitive). Build toward **Autonomy** (differentiator).

---

## Problem Statement #2: Consumidor Enxerga Agregadora Como Mais Transparente — Churn Silencioso

**Owner:** Jonas — Gerente de Relações com Consumidor

**Problem:** Gerentes comerciais em distribuidoras regionais enfrentam **ameaça silenciosa: consumidor não reclama, só sai para agregadora ou mercado livre** porque:

- Agregadoras (Sunrun, Solfácil, etc.) oferecem **app/portal com consumo em tempo real, alertas, análise de economia**
- Distribuidora oferece: fatura em PDF, sem visibilidade, sem alertas
- Consumidor com painéis solares não entende sua fatura (compensação de GD) — sem ferramenta que mostre o que acontece, é churn
- Mercado livre abre **agosto 2026** — consumidor de MT vai poder escolher fornecedor
- Distribuidora que não oferece transparência perde antes mesmo de ouvir reclamação

**Impact:** Churn silencioso. Receita desaparece. Custo de aquisição de novo cliente é 3-5x mais caro que retenção.

**Evidence:**
- Entrevista CERTEL (Jonas): "O monitoramento em tempo real do consumo de energia elétrica é uma ferramenta estratégica para aproximar a distribuidora do consumidor, proporcionando maior visibilidade sobre a utilização do serviço e incentivando uma gestão mais consciente do consumo... permitindo que o cliente acompanhe seu perfil de consumo e tome decisões com base em dados confiáveis" (prework/customer-interviews/entrevistas.txt, Cliente 2)
- Insights mostram "agregadoras já oferecem experiência superior" (insights, linha 183)
- 357 tickets vieram de Portal (clientes querem self-service), 404 de Atendimento (não conseguem usar Portal) (dashboard-tickets-800.html)
- Insights: "Mercado livre vai forçar essa mudança" (insights, reposicionamento)

---

### HMW: Engajar Consumidor

**How Might We** oferecer transparência que o consumidor precisa (real-time, alertas, educação) pra que não saia pra agregadora?

**Sub-questions:**
1. How Might We **mostrar consumo em tempo real (ou próximas horas)?**
2. How Might We **alertar consumidor de anomalia/pico** antes dele descobrir que foi cobrado errado?
3. How Might We **educar prosumidor (GD) sobre compensação de crédito** via interface?
4. How Might We **comparar consumo com pares** (benchmarking de economia)?

**Focus:** #1 + #2 (visibility + alerts)

---

### AI Ladder: Engajamento

| Rung | Description | Useall Implementation |
|------|-------------|----------------------|
| **1. Visibility** | Mostrar o problema | App/portal com: consumo últimas 24h, picos, compensação de GD, tarifa cobrada |
| **2. Productivity** | Ajuda manual | Consumidor consegue explorar dados, simular economia, entender fatura |
| **3. Automation** | Roda sozinho, humano aprova | Sistema manda alerta automático: "seu consumo está 30% acima do normal, verifique" |
| **4. Autonomy** | Roda e escalona exceções | Sistema manda alerta + sugestão: "você tem painel solar, pode compensar isso com GD" / escalona pra atendimento se alerta = erro de medição |

**Recommendation:** Start with **Visibility** (MVP). Aim for **Automation** (competitive). Build toward **Autonomy** (differentiator + retention).

---

## Stack Rank: Cliente Perspective

| Priority | Problem | Why | Impact |
|----------|---------|-----|--------|
| 🔴 #1 | **PS #1: Perdas** | Financial survival — margens sendo comprimidas, não consegue investir | Reduzir 1% de perdas = volta R$ 10M+ na margem |
| 🟡 #2 | **PS #2: Consumidor** | Market survival — mercado livre abre ago 2026, precisa reter | Evitar churn silencioso, custa 3-5x menos que aquisição |

---

## Next Steps

1. ✅ Jobs defined and ranked
2. ✅ Problem statements cited
3. ✅ HMWs framed
4. ✅ AI Ladder positioned
5. 📋 **TODO:** Refine HMWs (which sub-question to focus?)
6. 📋 **TODO:** Design MVP for PS #1 (Perdas)
7. 📋 **TODO:** Design MVP for PS #2 (Consumidor)

---

**Date:** 23 de junho de 2026  
**Workspace:** patricia-bento-antonio  
**Evidence base:** 800 tickets + 2 personas (Cláudio/Jonas) + market/customer/competitive insights
