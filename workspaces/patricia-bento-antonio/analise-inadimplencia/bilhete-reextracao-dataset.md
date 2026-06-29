# Bilhete de Re-extração — Dataset de Inadimplência (pós-reaviso)

> **Para:** quem roda o extract no Oracle E2 Comercial (dono dos dados de Cobrança).
> **Base atual:** `ml-dataset-inadimplencia-extract.sql` → `ML_DATASET_FINAL_<cliente>.csv`.
> **Evidência:** `analise-inadimplencia/saidas/relatorio_qualidade.md` (EDA sobre os 4 datasets).
> **Por quê:** o dataset atual **não é treinável** — o rótulo está quase vazio e várias
> features-chave vieram constantes. Antes de treinar qualquer modelo, precisamos de
> uma nova extração. Itens marcados **[validar c/ Cobrança]** dependem de confirmação
> de domínio antes de virar regra.

---

## 1. ⛔ CRÍTICO — Redefinir o alvo (`TARGET_PAGOU_ANTES_CORTE`)

**Problema:** o alvo hoje é `CASE WHEN REAVISO.CANCELADO='S' THEN 1 ELSE 0`. Resultado:
~0,07% de positivos (37/227k em Aliança, 15/79k em Cersul, 85/227k em Cetril, 397/275k
em Chesp). `REAVISO.CANCELADO` é um flag administrativo raro — quando o cliente paga, o
que é cancelada é a **ordem de corte**, não o reaviso.

**Correção proposta** — derivar o alvo do desfecho da ordem de corte (`REAVISO_CORTES`):

```sql
-- 1 = não houve corte executado (pagou/regularizou antes); 0 = corte executado
CASE WHEN EXISTS (
  SELECT 1 FROM REAVISO_CORTES RC
  WHERE RC.NUMERO_REAVISO = R.NUMERO_REAVISO
    AND RC.CORTADO = 'C'                 -- 'C'=cortado / 'A'=cancelado p/ pagamento / 'F'=não informado
) THEN 0 ELSE 1 END                       AS target_pagou_antes_corte
```

Cobre os dois caminhos de "pagou antes do corte": (a) reaviso resolvido no prazo, sem
ordem de corte; (b) ordem gerada mas cancelada por pagamento (`CORTADO='A'`).

**[validar c/ Cobrança]** confirmar a semântica de `CORTADO` ('C'/'A'/'F') e se o link
`REAVISO_CORTES.NUMERO_REAVISO = REAVISO.NUMERO_REAVISO` cobre todos os cortes.
**Opcional (robustez):** cruzar com pagamento da fatura (`DT_PAGAMENTO ≤ LIMITE_CORTE`).

**Censura temporal:** excluir reavisos cujo desfecho ainda não fechou (corte ainda
pode acontecer). Manter só os com janela encerrada:

```sql
AND R.LIMITE_CORTE < TRUNC(SYSDATE) - :margem_dias   -- ex.: margem = PrazoCorte + 15
```

---

## 2. ⚠️ Features comportamentais vieram constantes em ZERO

No EDA, estas saíram = 0 em ~100% das linhas nas 4 distribuidoras — ou seja, sem sinal:
`FLAG_PAGOU_ULTIMO_REAVISO`, `HAVIA_PRORROGACOES`, `FLAG_PRORROGOU_12M`,
`FLAG_NAO_RELIGAR_AUTOMATICO`, `FLAG_CORTE_INDEVIDO_HISTORICO`.

São justamente os preditores mais fortes esperados. Investigar **por feature**:
- `FLAG_PAGOU_ULTIMO_REAVISO` e taxas de pagamento históricas → dependem do conceito de
  "pago", que estava quebrado (item 1). **Recalcular a partir do novo alvo (`CORTADO`)**,
  não de `CANCELADO`.
- `HAVIA_PRORROGACOES` / `PRORROGADO` → conferir se o campo é populado nessas
  distribuidoras (pode ser não-uso real) **[validar c/ Cobrança]**.
- `FLAG_NAO_RELIGAR_AUTOMATICO` → conferir se `NAO_RELIGAR_AUTOMATICO` tem registros e se
  o join (`IDUC` + `PEDIDO_CANCELADO='N'` + `DATAHORA <= DATA_EMISSAO`) está correto.
- `FLAG_CORTE_INDEVIDO_HISTORICO` → conferir se `RELIGACOES.CORTE_INDEVIDO` é preenchido.

> Distinguir **bug de ETL/join** (corrigir) de **não-uso real do recurso** (documentar e
> descartar a feature, sem fingir que tem sinal).

---

## 3. 🧹 Limpeza de dados

- `ANO_MES` com sentinela **`1900-01`** (Cersul, Chesp) → tratar data nula; não usar
  como variável temporal sem limpar.
- `DIAS_ATE_LIMITE_CORTE` com máximos implausíveis (~9.800 dias em Cersul/Chesp) →
  `LIMITE_CORTE` com data-sentinela; corrigir na origem ou winsorizar.
- `FLAG_BAIXA_RENDA` = 0 em 100% → o join com `DADOSBAIXARENDA` não está trazendo.
  Corrigir; se não houver dado, **identificar baixa renda por subclasse/tarifa** (mesmo
  contorno do projeto de fraude) **[validar c/ Regulatório]**.

---

## 4. 🔁 Features úteis omitidas (reincluir se possível)

Já existem nas tabelas intermediárias, mas ficaram de fora do `ML_DATASET_FINAL`:
- Grupo E — **Acordos** (`ML_FEAT_ACORDOS`): `qtde_acordos_*`, `taxa_cumprimento_acordos`,
  `flag_acordo_ativo`, `valor_divida_acordo_ativo`, `meses_desde_ultimo_acordo`.
- Grupo C: `TAXA_PAGAMENTO_12M`, `TAXA_PAGAMENTO_TOTAL` (recalcular via novo alvo).
- Grupo F: `qtde_sms_12m`. Grupo A: `meses_desde_ligacao`, `nr_moradores`.

Acordo é forte preditor de propensão a pagar — vale recuperar.

---

## 5. ✅ Checklist de validação (rodar na nova extração)

- [ ] Distribuição do alvo por distribuidora — esperar **~30–60% positivos** (não 0,07%).
- [ ] Distribuição estável mês a mês (sem mês anômalo por suspensão regulatória).
- [ ] As 5 features do item 2 agora têm variância (ou foram documentadas como não-uso).
- [ ] Sem sentinela `1900` em `ANO_MES`; `DIAS_ATE_LIMITE_CORTE` em faixa plausível (≤ ~90).
- [ ] Cobertura de nulos por feature dentro do esperado (corte/canal nulos só p/ UC sem histórico).
- [ ] Manter `IDUC`/`NUMERO_REAVISO` em tabela de acesso restrito (devolver o score à operação); remover do vetor de treino (LGPD).

---

## Resumo (1 linha)
Re-extrair com **alvo a partir de `REAVISO_CORTES.CORTADO`** + **recalcular/consertar as
features comportamentais zeradas** + **limpar sentinelas** + **reincluir acordos**;
depois revalidar o balanço de classes antes de treinar (meta AUC ≥ 0,80 v1).
