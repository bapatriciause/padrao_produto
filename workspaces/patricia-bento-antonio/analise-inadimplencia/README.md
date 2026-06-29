# Análise de Inadimplência

> **Status: em definição / aguardando datasets de treino.** Segundo modelo do
> workspace, seguindo o padrão de `../motor-deteccao-fraude/`. A abordagem e o
> recorte do PoC ainda vão ser fechados — ver "Decisão pendente" abaixo.

Trabalho do AI Accelerator (Volaris). Diferente da fraude, **inadimplência já
nasce com visão agêntica** — alinhada ao Day 2 (mirar AI Directed / AI Delegated,
não um painel; passar pelos reality checks; Responsible AI com **fairness e
safety em destaque**, porque corte de energia é ação regulada, sobre consumidor
muitas vezes vulnerável).

## Fonte de dados (corrigido)

Não vem dos CSVs de fraude. Vem do **modelo Oracle do E2 Comercial — módulo
Cobrança**: `REAVISO`, `REAVISO_GERACAO`, `REAVISO_CORTES`, `RELIGACOES`,
`DESLIGAMENTOS`, `PARCELA_DIVIDA_ESP(_PARC)`, `NAO_RELIGAR_AUTOMATICO`,
`UC`, `DADOSBAIXARENDA`, `UC_TRRESTRICAO_CORTE`, e taxas de recuperação do
relatório ANEEL Res. 479/2012.

## Insumos já recebidos (`C:\Users\patricia.bento\Downloads\Inadimplencia\`)

| Arquivo | Conteúdo |
|---|---|
| `docs-cobranca-inadimplencia-definitivo.docx` | **Doc mestre** — fluxo completo, entidades, jobs Hangfire, regulatório, **portfólio de 11 agentes** |
| `ml-dataset-inadimplencia.md` | Spec de ML do modelo **pós-reaviso** (target `REAVISO.CANCELADO`) — features + queries Oracle |
| `agente-preditor-inadimplencia-pre-vencimento.docx` | Plano do Agente 1 (modelo **pré-vencimento**) |
| `agente-canal-mensagem-llm.docx` | Plano do Agente 2 (otimização de canal/mensagem, LLM) |
| `agentes-corte-scoring.docx` | Plano dos Agentes 3/4 (seleção + scoring de corte) |
| `docs-benchmarking-cobranca-inadimplencia.docx` | Benchmarks de mercado (ABRADEE, PDD, AUC alvo, custos) |
| `P-031 - Prevenção de inadimplência.docx` | Notas de produto / clientes-alvo (funil de cobrança) |
| `Dados_Analise_Cortes_Reavisos_E2Comercial.xlsx` | **Dado real** — volumes mensais 2025 (9 distribuidoras): enviados, cortes, religações, total de reavisos |

## Os dois modelos preditivos

| | **Pré-vencimento** (Agente 1) | **Pós-reaviso** (ml-dataset spec) |
|---|---|---|
| Pergunta | Antes do vencimento, a UC vai deixar de pagar? | Dado o reaviso, paga antes do corte? |
| Target | a definir (não pagou no vencimento) | `REAVISO.CANCELADO` (S/N) |
| Momento | início da cadeia (custo de ação ≈ 0) | já dentro do ciclo de cobrança |
| Spec pronta? | plano v1.0 | **sim** — features + SQL Oracle |
| Posição | "maior impacto sistêmico" (doc) | base de scoring p/ Agentes 3, 4 |

## Benchmarks de mercado (do doc, a validar)

- Receita não arrecadada do setor: ~R$ 6 bi/ano (ABRADEE).
- Inadimplência residencial 6,1%; setor público 17,7% (ABRADEE).
- PDD/Receita: melhores ~0,8–1,4% (CPFL, Equatorial) vs. média 2,5–3,5%.
- AUC-ROC alvo: ≥0,80 (v1) / ≥0,87 (v2). ~740 ações judiciais/dia por corte indevido.

## Guardrails (Responsible AI — Day 2)

- **Human-in-the-loop obrigatório** em qualquer ação de corte; o agente
  recomenda/prioriza, pessoa decide. Os campos `Prioridade`, `Marcado`,
  `Urgencia` já existem no schema para isso.
- Respeitar **restrições ao corte** (`UC_TRRESTRICAO_CORTE`, serviço essencial,
  baixa renda, decisão judicial) e a Res. ANEEL 479/2012.
- Decisões com impacto regulatório/jurídico → validar com Regulatório/Jurídico
  antes de virar ação oficial (não substituir o parecer dessas áreas).

## Convenções herdadas do motor de fraude

- Cada distribuidora analisada isoladamente (não cruzar por IDUC).
- Segregação de dados / LGPD: modo anonimizado como padrão; modo real em pasta
  ignorada pelo Git. Saídas explicáveis (motivo por UC). Parâmetros calibráveis.

## ⚠️ Achado crítico — rótulo do dataset pós-reaviso (2026-06-25)

Os datasets reais chegaram em `Inadimplencia/Datasets teste/` (`ML_DATASET_FINAL_*`,
4 distribuidoras, ~810k reavisos, 57 cols). **O target `TARGET_PAGOU_ANTES_CORTE`
está praticamente vazio:**

| Distribuidora | Linhas | target=1 | % |
|---|---:|---:|---:|
| ALIANCA | 227.926 | 37 | 0,016% |
| CERSUL | 79.236 | 15 | 0,019% |
| CETRIL | 227.152 | 85 | 0,037% |
| CHESP | 275.484 | 397 | 0,144% |

~534 positivos em 810k → inviável para treino e **implausível** (contradiz o
benchmark de recuperação 50%+). Diagnóstico provável: o extract usa
`REAVISO.CANCELADO='S'` (flag administrativo raro). O pagamento antes do corte é
capturado no desfecho da **ordem de corte** — `REAVISO_CORTES.CORTADO='A'`
(cancelada por pagamento) vs `'C'` (executada). **Rótulo a redefinir e validar com
quem gerou o extract / área de cobrança.** Detalhe menor: `ANO_MES` tem sentinela
`1900-01` em CERSUL/CHESP.

**EDA construído** (`eda_inadimplencia.py` → `saidas/relatorio_qualidade.md`,
`perfil_colunas_*.csv`, `resumo_consolidado.csv`). Outros achados, além do rótulo:

- **Features comportamentais constantes-zero** em ~todas distribuidoras —
  `FLAG_PAGOU_ULTIMO_REAVISO`, `HAVIA_PROROGACOES`, `FLAG_PRORROGOU_12M`,
  `FLAG_NAO_RELIGAR_AUTOMATICO`, `FLAG_CORTE_INDEVIDO_HISTORICO` ≈ 0 em ~100%.
  Mesma família de campos do target → o re-extract precisa revisar **também** essas
  features (não só o rótulo). São justamente os preditores mais fortes esperados.
- **`FLAG_BAIXA_RENDA` = 0 em 100%** (igual ao achado da fraude) → feature de
  fairness/vulnerabilidade inutilizável como está; identificar baixa renda por
  subclasse/tarifa.
- **Canal degenerado:** `CANAL_ENTREGA` = Impresso em 100% → o estudo do Agente 2
  (otimização de canal) **não é possível com esta base** (sem variação SMS).
- **Geografia frágil:** `MUNICIPIO`/`UF` nulos em 42% (CHESP); mascarado em CETRIL.
- **Datas-lixo:** `DIAS_ATE_LIMITE_CORTE` com máx ~9.800 dias (CERSUL/CHESP) →
  `LIMITE_CORTE` com sentinela; winsorizar.
- **Positivo:** volume robusto (~810k reavisos, ~87k UCs), débito coerente
  (mediana ~R$150), e **recorrência alta (7,5–10 reavisos/UC)** = inadimplência
  crônica é a norma nessas distribuidoras.

## Decisão pendente (próximo passo)

1. **Bloqueador:** redefinir/confirmar o target do modelo pós-reaviso (ver achado acima).
2. **EDA / relatório de qualidade de dados** sobre os 4 datasets — alinhado ao P-031
   ("avaliar qualidade do dado"); útil independente do fix do rótulo.
3. **Foco do PoC** — candidatos: pós-reaviso (dados prontos, depende do fix); Agente 1
   pré-vencimento (maior impacto, target a desenhar); Agentes 3/9 "curto prazo".
4. PoC agêntico (assistente de seleção de corte) pode ser mockado pro workshop.
