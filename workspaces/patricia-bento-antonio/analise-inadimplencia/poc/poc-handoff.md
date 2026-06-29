# Handoff — Assistente Inteligente de Seleção de Corte

> Nota de passagem pro time (dev + produto), não é spec completa. Protótipo em
> `poc-selecao-corte.html`. Contexto: `poc-scope.md`, `../README.md`,
> `../personas/persona-operador-cobranca.md`, `mark-miller-feedback.md`.

## O que o PoC faz
Na tela de **ordem de corte** do E2 Comercial, um agente analisa o lote e, por UC,
recomenda a **próxima melhor ação** — Cortar / SMS-PIX antes / Oferecer acordo /
Revisar / Não cortar — com **prioridade (0–1000)** e **justificativa de 1 linha**.
O operador confirma ou sobrescreve (human-in-the-loop); a decisão fica registrada.
Tem um **funil de cobrança** (contexto da carteira, R$ por estágio, onde a IA atua) e
KPIs ao vivo (recuperação esperada, cortes indevidos evitados, deslocamentos evitados, ROI).

## Para quem
Operador e supervisor de **Cobrança** de distribuidoras/cooperativas (usuário diário =
quem hoje monta o lote no olho pelas flags coloridas). Comprador: diretoria comercial.

## Problema que resolve
Decisão de **quem cortar e como cobrar** é hoje manual, inconsistente entre operadores e
sem rastreabilidade — gerando **corte indevido** (risco jurídico/ANEEL), **deslocamento
à toa** (medidor convencional exige equipe em campo) e perda da **janela de 90 dias**.

## O que o protótipo prova
Que a IA tria o lote de forma **explicável, auditável e com humano no comando**,
priorizando por recuperação × custo e respeitando guardrails regulatórios — e que isso
cabe nos campos que **já existem** no schema (`Marcado`, `Prioridade`). Não prova que o
modelo funciona (ver abaixo).

## O que é fake / placeholder
- **Dados fictícios** (14 UCs) e **score de probabilidade simulado**.
- **Funil com números ilustrativos** (faixa do `.xlsx`, não dados reais de um mês).
- **Sem backend / sem integração** com E2 Comercial, Oracle ou MDM.
- **Persona "Sérgio" é direcional** (construída dos docs, não entrevistada).
- O **modelo pós-reaviso não existe** — o rótulo do dataset atual está quebrado
  (`TARGET_PAGOU_ANTES_CORTE` ≈ 0,07% positivos; ver `../README.md`).

## O que construir a seguir (ordem sugerida)
1. **Re-extração do dataset** (bloqueador nº 1): target a partir de
   `REAVISO_CORTES.CORTADO` ('A'=cancelado por pagamento=1 / 'C'=executado=0), e revisar
   as features comportamentais que vieram **constantes-zero** (`FLAG_PAGOU_ULTIMO_REAVISO`,
   `HAVIA_PRORROGACOES`, `FLAG_PRORROGOU_12M`, `FLAG_NAO_RELIGAR_AUTOMATICO`,
   `FLAG_CORTE_INDEVIDO_HISTORICO`). Limpar sentinela `1900-01` e `LIMITE_CORTE` lixo.
2. **Modelo** (Agente 4 — scoring): LightGBM por distribuidora, split temporal por
   `ANO_MES` (sem embaralhar), meta **AUC ≥ 0,80 (v1)**. Saída → `ReavisoCortes.Prioridade`.
3. **Próxima melhor ação** (Agentes 3/2/8): regra + score decide Cortar/SMS-PIX/Acordo/
   Não cortar; integra canal (SMS/WhatsApp/PIX) e proposta de acordo (`ParcelaDividaEsp`).
4. **Integração na tela**: enriquecer a resposta de `gerarIdSelecaoReavisoOrdemDeCorte()`
   com `Marcado` + `Prioridade` + justificativa (job Hangfire após `TotalmenteLancado`).
5. **Trilha de auditoria** da decisão (recomendação IA × decisão do operador).

## Guardrails (não negociáveis)
Serviço essencial, restrição de corte (`UC_TRRESTRICAO_CORTE`), baixa renda e
micro-geração → recomendação **Não cortar/Revisar**, nunca corte automático. Respeitar
Res. ANEEL 479/2012 e 1000/2021 (janela de corte). Decisão final sempre humana.
Validar limiares com **Regulatório/Jurídico** antes de uso real.

## Perguntas em aberto
**Dev/dados:** a re-extração com `CORTADO` traz balanço treinável (~30–60%)? As features
zeradas eram não-uso da cooperativa ou falha de ETL? Como tratar `FLAG_BAIXA_RENDA`
(vazio) — usar subclasse/tarifa?
**Produto:** o canal SMS/PIX/WhatsApp existe pra acionar antes do corte? Como medir
"deslocamento evitado" no real (tipo de medidor por UC)?
**Validação (gate Mark Miller — `mark-miller-feedback.md`):** virar a **Certel** num
piloto **pago/co-financiado**; medir **share-of-wallet** (R$/mês de corte indevido +
deslocamento + dívida parada por cooperativa, e a fatia da Useall).
