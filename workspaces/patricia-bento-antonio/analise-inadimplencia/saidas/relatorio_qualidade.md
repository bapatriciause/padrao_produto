# Relatório de Qualidade de Dados — Inadimplência (pós-reaviso)

> Gerado por `eda_inadimplencia.py`. Grão: 1 linha por reaviso (`ML_DATASET_FINAL_<cliente>.csv`). Análise exploratória **antes** de treinar qualquer modelo — alinhada ao P-031 e à honestidade de evidência do Day 2.

## 1. ⚠️ Achado crítico — o rótulo está inviável

O target `TARGET_PAGOU_ANTES_CORTE` (= `REAVISO.CANCELADO='S'`) é quase inexistente. Com tão poucos positivos **não há treino supervisionado possível**, e o valor é implausível (contradiz recuperação de 50%+ do benchmark).

| Cliente | Reavisos | UCs | Reav./UC | Positivos (pagou) | % positivos |
|---|---:|---:|---:|---:|---:|
| ALIANCA | 227.926 | 26.775 | 8.51 | 37 | 0.0162% |
| CERSUL | 79.236 | 10.541 | 7.52 | 15 | 0.0189% |
| CETRIL | 227.152 | 22.603 | 10.05 | 85 | 0.0374% |
| CHESP | 275.484 | 27.016 | 10.2 | 397 | 0.1441% |
| **TOTAL** | **809.798** | | | **534** | **0.0659%** |

**Diagnóstico (confirmado com análise do `ml-dataset-inadimplencia-extract.sql`):** `REAVISO.CANCELADO` é flag administrativo raro. O pagamento antes do corte é capturado no desfecho da ordem de corte — `REAVISO_CORTES.CORTADO`: `'A'` (cancelada por pagamento) → target=1; `'C'` (executada) → target=0. **Ação:** redefinir o target no extract a partir de `CORTADO` (e opcionalmente cruzar `DT_PAGAMENTO ≤ LIMITE_CORTE`). Esta coluna de desfecho **não está** no dataset atual, então o rótulo correto não pode ser reconstruído aqui — precisa de nova extração.

## 2. Cobertura temporal e datas-sentinela

| Cliente | Período válido (ANO_MES) | Sentinela 1900 | DATA_EMISSAO fora de 2020–2026 |
|---|---|---:|---:|
| ALIANCA | 2023-12 … 2025-12 | 0 (0.00%) | 0 |
| CERSUL | 2024-01 … 2025-12 | 46 (0.06%) | 0 |
| CETRIL | 2023-12 … 2025-12 | 0 (0.00%) | 0 |
| CHESP | 2023-12 … 2025-12 | 34 (0.01%) | 0 |

`ANO_MES = 1900-01` é competência nula vazando do Oracle (sentinela). Excluir ou imputar antes de usar como variável temporal de split.

## 3. Qualidade por coluna (nulos inesperados)

Colunas com nulos acima do esperado (exclui as que são NULL por design — sem histórico de corte/canal):

**CHESP:** `MUNICIPIO` 41.99% · `UF` 41.99%

## 4. Distribuições numéricas e valores implausíveis


**ALIANCA**

| Feature | mediana | média | p99 | máx | negativos | zeros |
|---|---:|---:|---:|---:|---:|---:|
| TOTAL_DEBITO | 165,85 | 267,41 | 1.677,33 | 157.290,62 | 0 | 0 |
| DIAS_ATE_LIMITE_CORTE | 15,00 | 15,78 | 25,00 | 385,00 | 0 | 0 |
| QTDE_REAVISOS_12M | 8,00 | 7,02 | 12,00 | 24,00 | 0 | 12.928 |
| QTDE_CORTES_TOTAL | 3,00 | 4,65 | 25,00 | 69,00 | 0 | 54.218 |
| VARIACAO_DEBITO_VS_MEDIA | 1,02 | 1,13 | 3,76 | 141,71 | 0 | 10 |
| DIAS_DESDE_ULTIMO_CORTE | 890,00 | 1.535,87 | 6.468,93 | 46.012,00 | 0 | 0 |

**CERSUL**

| Feature | mediana | média | p99 | máx | negativos | zeros |
|---|---:|---:|---:|---:|---:|---:|
| TOTAL_DEBITO | 156,61 | 354,54 | 2.979,03 | 233.873,55 | 0 | 0 |
| DIAS_ATE_LIMITE_CORTE | 15,00 | 21,35 | 27,00 | 9.829,00 | 0 | 0 |
| QTDE_REAVISOS_12M | 7,00 | 6,60 | 12,00 | 13,00 | 0 | 5.650 |
| QTDE_CORTES_TOTAL | 1,00 | 2,32 | 17,00 | 52,00 | 0 | 35.035 |
| VARIACAO_DEBITO_VS_MEDIA | 1,03 | 1,17 | 4,07 | 484,83 | 0 | 10 |
| DIAS_DESDE_ULTIMO_CORTE | 1.542,00 | 1.999,65 | 5.924,00 | 6.649,00 | 0 | 0 |

**CETRIL**

| Feature | mediana | média | p99 | máx | negativos | zeros |
|---|---:|---:|---:|---:|---:|---:|
| TOTAL_DEBITO | 144,76 | 222,77 | 1.583,22 | 85.769,45 | 0 | 0 |
| DIAS_ATE_LIMITE_CORTE | 25,00 | 25,93 | 39,00 | 127,00 | 0 | 0 |
| QTDE_REAVISOS_12M | 9,00 | 8,00 | 12,00 | 13,00 | 0 | 9.396 |
| QTDE_CORTES_TOTAL | 2,00 | 3,77 | 22,00 | 52,00 | 0 | 57.273 |
| VARIACAO_DEBITO_VS_MEDIA | 1,00 | 1,06 | 2,67 | 242,37 | 0 | 0 |
| DIAS_DESDE_ULTIMO_CORTE | 694,00 | 1.269,71 | 6.114,44 | 46.006,00 | 0 | 0 |

**CHESP**

| Feature | mediana | média | p99 | máx | negativos | zeros |
|---|---:|---:|---:|---:|---:|---:|
| TOTAL_DEBITO | 149,88 | 228,04 | 1.609,45 | 109.749,97 | 0 | 0 |
| DIAS_ATE_LIMITE_CORTE | 15,00 | 16,69 | 18,00 | 9.858,00 | 0 | 0 |
| QTDE_REAVISOS_12M | 9,00 | 7,77 | 12,00 | 20,00 | 0 | 10.794 |
| QTDE_CORTES_TOTAL | 3,00 | 4,76 | 28,00 | 78,00 | 0 | 62.571 |
| VARIACAO_DEBITO_VS_MEDIA | 1,03 | 1,14 | 3,54 | 891,82 | 0 | 25 |
| DIAS_DESDE_ULTIMO_CORTE | 827,00 | 1.245,07 | 4.755,88 | 5.313,00 | 0 | 0 |

> ⚠️ `DIAS_ATE_LIMITE_CORTE` com máximos implausíveis (prazo normal é 15–30 dias): ALIANCA (máx 385d, 8 linhas > 90d); CERSUL (máx 9.829d, 48 linhas > 90d); CETRIL (máx 127d, 1 linhas > 90d); CHESP (máx 9.858d, 41 linhas > 90d). Provável `LIMITE_CORTE` com data-sentinela — limpar/winsorizar antes do treino.

> `DIAS_ATE_LIMITE_CORTE` negativo (se houver) indica limite de corte antes da emissão — inconsistência a investigar.

## 5. Composição (segmentos e operacional)


**ALIANCA**

- Classe: RESIDENCIAL: 89.8% · COMERCIAL, SERVIÇOS E OUTRAS : 7.5% · RURAL: 2.2% · INDUSTRIAL: 0.4% · PODERES PUBLICOS: 0.1% · SERVIÇOS PÚBLICO: 0.0% · ILUMINACAO PUBLICA: 0.0%
- Grupo tensão: B: 99.8% · A: 0.2%
- Baixa renda: 0.0%
- Nunca foi cortado: 23.8%
- Canal de entrega: Impresso: 100.0%
- Origem do reaviso: Manual: 100.0%
- Última forma de corte: COD (campo): 57.6% · (nulo): 23.8% · Outros: 18.6% · MDM (remoto): 0.0% · COD→MDM: 0.0%
- Alta cardinalidade (precisa encoding/agrupamento): `NOME_BAIRRO` (60), `NOME_ROTA` (141)

**CERSUL**

- Classe: Residencial: 70.4% · Rural: 17.0% · Comercial: 10.2% · Industrial: 1.6% · Poderes Públicos: 0.6% · Serviço Público: 0.1% · Iluminação Pública: 0.0% · Consumo Próprio: 0.0%
- Grupo tensão: B: 99.6% · A: 0.4%
- Baixa renda: 0.0%
- Nunca foi cortado: 44.2%
- Canal de entrega: Impresso: 100.0%
- Origem do reaviso: Automático: 98.9% · Manual: 1.1% · Agrupamento: 0.1% · 6: 0.0%
- Última forma de corte: COD (campo): 53.0% · (nulo): 44.2% · Outros: 2.7%
- Alta cardinalidade (precisa encoding/agrupamento): `NOME_BAIRRO` (114), `NOME_ROTA` (101)

**CETRIL**

- Classe: RESIDENCIAL: 96.5% · RURAL: 2.6% · COMERCIAL: 0.9% · PODERES PUBLICOS: 0.1% · SERVIÇOS PÚBLICO: 0.0% · INDUSTRIAL: 0.0% · ILUMINACAO PUBLICA: 0.0%
- Grupo tensão: B: 100.0% · A: 0.0%
- Baixa renda: 0.0%
- Nunca foi cortado: 25.2%
- Canal de entrega: Impresso: 100.0%
- Origem do reaviso: Manual: 100.0% · Automático: 0.0%
- Última forma de corte: COD (campo): 73.7% · (nulo): 25.2% · Outros: 1.1%
- Alta cardinalidade (precisa encoding/agrupamento): `NOME_BAIRRO` (66), `NOME_ROTA` (97)

**CHESP**

- Classe: Residencial: 82.6% · Comercial: 8.7% · Rural: 7.4% · Poderes Públicos: 1.3% · Industrial: 0.1% · Consumo Próprio: 0.0%
- Grupo tensão: B: 99.9% · A: 0.1%
- Baixa renda: 0.0%
- Nunca foi cortado: 22.7%
- Canal de entrega: Impresso: 100.0%
- Origem do reaviso: Automático: 99.3% · Manual: 0.7% · Agrupamento: 0.0%
- Última forma de corte: COD (campo): 77.3% · (nulo): 22.7%
- Alta cardinalidade (precisa encoding/agrupamento): `NOME_BAIRRO` (234), `NOME_ROTA` (208)

## 6. Features degeneradas / candidatas a descarte

Colunas constantes ou quase-constantes (1 valor cobre >99% das linhas) — sem poder preditivo nesta base; descartar por distribuidora (e revisar se o dado deveria ter variância):

**ALIANCA:** `FLAG_INDUSTRIAL` (=0, 99.6%) · `FLAG_PODER_PUBLICO` (=0, 99.9%) · `FLAG_SERVICO_PUBLICO` (=0, 100.0%) · `FLAG_BAIXA_RENDA` (=0, 100.0%) · `HAVIA_PRORROGACOES` (=0, 100.0%) · `FLAG_PAGOU_ULTIMO_REAVISO` (=0, 100.0%) · `FLAG_PRORROGOU_12M` (=0, 100.0%) · `FLAG_NAO_RELIGAR_AUTOMATICO` (=0, 100.0%) · `FLAG_CORTE_INDEVIDO_HISTORICO` (=0, 100.0%) · `UF` (=SC, 100.0%) · `GRUPO_TENSAO` (=B, 99.8%) · `CANAL_ENTREGA` (=0, 100.0%) · `ORIGEM_REAVISO` (=2, 100.0%)

**CERSUL:** `FLAG_PODER_PUBLICO` (=0, 99.4%) · `FLAG_SERVICO_PUBLICO` (=0, 99.9%) · `FLAG_BAIXA_RENDA` (=0, 100.0%) · `HAVIA_PRORROGACOES` (=0, 100.0%) · `FLAG_PAGOU_ULTIMO_REAVISO` (=0, 99.8%) · `FLAG_PRORROGOU_12M` (=0, 100.0%) · `FLAG_NAO_RELIGAR_AUTOMATICO` (=0, 99.4%) · `FLAG_CORTE_INDEVIDO_HISTORICO` (=0, 100.0%) · `UF` (=SC, 99.1%) · `GRUPO_TENSAO` (=B, 99.6%) · `CANAL_ENTREGA` (=0, 100.0%) · `TAXA_PAG_CANAL_SMS` (=nulo, 100.0%)

**CETRIL:** `FLAG_INDUSTRIAL` (=0, 100.0%) · `FLAG_COMERCIAL` (=0, 99.1%) · `FLAG_PODER_PUBLICO` (=0, 99.9%) · `FLAG_SERVICO_PUBLICO` (=0, 100.0%) · `FLAG_BAIXA_RENDA` (=0, 100.0%) · `HAVIA_PRORROGACOES` (=0, 100.0%) · `FLAG_PAGOU_ULTIMO_REAVISO` (=0, 100.0%) · `FLAG_PRORROGOU_12M` (=0, 100.0%) · `FLAG_NAO_RELIGAR_AUTOMATICO` (=0, 100.0%) · `FLAG_ULTIMO_RELIGOU_MESMO_DIA` (=0, 99.8%) · `FLAG_CORTE_INDEVIDO_HISTORICO` (=0, 99.5%) · `MUNICIPIO` (=I*****, 100.0%) · `UF` (=SP, 100.0%) · `GRUPO_TENSAO` (=B, 100.0%) · `CANAL_ENTREGA` (=0, 100.0%) · `ORIGEM_REAVISO` (=2, 100.0%) · `MEDIA_DIAS_CORTADO` (=nulo, 99.8%) · `MAX_DIAS_CORTADO` (=nulo, 99.8%) · `MIN_DIAS_CORTADO` (=nulo, 99.8%) · `TAXA_RELIGOU_MESMO_DIA` (=nulo, 99.8%) · `TAXA_PAG_CANAL_SMS` (=nulo, 100.0%)

**CHESP:** `FLAG_INDUSTRIAL` (=0, 99.9%) · `FLAG_SERVICO_PUBLICO` (=0, 100.0%) · `FLAG_BAIXA_RENDA` (=0, 100.0%) · `FLAG_DEBITO_CONTA` (=0, 99.2%) · `PRORROGADO` (=0, 100.0%) · `HAVIA_PRORROGACOES` (=0, 100.0%) · `FLAG_PAGOU_ULTIMO_REAVISO` (=0, 99.6%) · `FLAG_PRORROGOU_12M` (=0, 100.0%) · `FLAG_NAO_RELIGAR_AUTOMATICO` (=0, 100.0%) · `FLAG_CORTE_INDEVIDO_HISTORICO` (=0, 99.7%) · `CANAL_IGUAL_AO_ULTIMO` (=1, 99.3%) · `GRUPO_TENSAO` (=B, 99.9%) · `CANAL_ENTREGA` (=0, 100.0%) · `ORIGEM_REAVISO` (=1, 99.3%) · `TAXA_PAG_CANAL_SMS` (=nulo, 100.0%)


## 7. Achados consolidados

1. **Rótulo inviável** — redefinir o target a partir de `REAVISO_CORTES.CORTADO` no extract (bloqueador do modelo supervisionado).
2. **Sentinela 1900** em `ANO_MES` (CERSUL/CHESP) — limpar antes do split temporal.
3. **Nulos por design** em features de corte/canal são esperados (UC sem histórico); para árvore (LightGBM) deixar como NaN; para modelos lineares, imputar + flag.
4. **Alta cardinalidade** em bairro/rota/subclasse — target/freq encoding ou agrupar por regional.
5. **Cadastro estático**: features de UC refletem o estado atual no banco, não o estado na data do reaviso (possível leakage leve em cadastro — documentado no dicionário).

## 8. Próximos passos

- [ ] Corrigir o target no extract (`CORTADO`) e reextrair.
- [ ] Revalidar o balanço de classes com o novo rótulo (esperado ~30–60% positivos).
- [ ] Definir split temporal por `ANO_MES` (treino/valid/teste), sem embaralhar.
- [ ] Então treinar baseline (LightGBM) por distribuidora; meta AUC ≥ 0,80 (v1).

---
_Relatório de qualidade — não substitui validação com a área de Cobrança/Regulatório para decisões de corte._
