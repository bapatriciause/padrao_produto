# Responsible AI Fit — Idea #5: Avisos ao Consumidor

**Data:** 24 de junho de 2026
**Ideia avaliada:** Agente de detecção de anomalias de consumo + alertas SMS/WhatsApp
**Lentes analisadas:** Safety → Transparency → Fairness

---

## Watch-outs Principais

### CRITICO: Falsos Positivos

**O problema:** Consumidor recebe alerta mas consumo está normal.

**Causas identificadas:**
- Novos clientes (média = 0, qualquer consumo é "anomalia")
- Troca de medidor (perda de histórico)
- Sazonalidade (verão vs. inverno, consumo varia naturalmente)

**Impacto:** Desconfiança na distribuidora, reclamações, risco de churn.

---

### MEDIO: Falta de Contexto no Alerta

**O problema:** SMS/WhatsApp mostra variacao % mas nao explica causa.

**Design:** Nao menciona "IA" (consumidor vê como alerta normal).

**Implicacao:** Se for falso positivo, consumidor fica confuso.

---

## Design Change — Antes de Prototipar

VALIDAR E FILTRAR dados nos CSVs reais:

1. Novos clientes: Excluir consumidores onde MEDIA < 50 kWh
2. Trocas de medidor: Excluir linhas onde TROCA_MEDIDOR_MES_ATUAL = 1
3. Sazonalidade: Ajustar threshold por mes (verao +15%, inverno -10%)
4. Resultado: Enviar alertas apenas pra consumidores com historico estavel

---

## Questao a Carregar

Como validar taxa de falsos positivos com dados reais?

Opcoes:
- Enviar pra amostra pequena (100 consumidores) e coletar feedback
- Perguntar consumidor "esse alerta faz sentido pra voce?"
- Monitorar taxa de reclamacoes/respostas por canal (SMS vs WhatsApp vs Portal)

---

## Contexto de Aceitacao

- Consumidores ja recebem alertas por outros motivos (normalizado)
- Fairness e aceitavel (quem tem anomalia recebe, quem nao tem nao recebe)
- Transparencia sobre IA nao e requisito (alerta parece natural)

---

Status: Pronto pra prototipar com mitigacoes acima.

Proximo: Implementar filtros nos dados antes de enviar alertas reais.
