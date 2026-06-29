# Front-end — Explicabilidade ("por quê?") & Confirmação do Lote (FE-03) Specification

**Status:** In Review
**Owner:** Patrícia Bento Antônio (R&D)
**Created:** 2026-06-25
**Last Updated:** 2026-06-25

> Spec-filha de [FE-00 Visão Geral](FE-00-visao-geral.md). Herda design system, contrato de
> dados e guardrails de RAI da spec-âncora. Componentes irmãos:
> [FE-01 Grid & Decisão](FE-01-grid-decisao.md) · [FE-02 Funil & KPIs](FE-02-funil-kpis.md).

## Overview

Dois mecanismos que sustentam **"IA recomenda, humano decide"**:

1. **Drill-down "por quê?"** — por UC, abre o **raciocínio do agente** em 3 passos
   (sinais detectados → raciocínio → próxima melhor ação), para o operador entender a
   recomendação antes de aceitar ou ajustar.
2. **Confirmação do lote** — modal de revisão final com o resumo das decisões (contagem
   por ação, valor do lote de corte, recuperação esperada e **nº de ajustes sobre a IA**)
   antes de gerar as ordens. É o ponto de **registro/auditoria** da decisão humana.

Referência viva: linha `.reason` (trace `.trace`/`.step`) e modal `#ov`/`.modal` em
[`../poc/poc-selecao-corte.html`](../poc/poc-selecao-corte.html).

## Goals

- **Explicar cada recomendação** em linguagem clara, sem caixa-preta.
- Deixar o operador **revisar o lote inteiro** antes de confirmar (nada é executado sem revisão).
- Tornar a **decisão humana auditável**: registrar o par (recomendação IA, decisão do operador) e o nº de ajustes.
- Reforçar que **nenhum corte/mensagem é executado pelo front** — só registro da decisão.

## Non-Goals

- Não define a grid/decisão (FE-01) nem funil/KPIs (FE-02).
- Não envia SMS/WhatsApp/PIX nem executa o corte — isso é backend (a PoC só faz mock/alert).
- Não especifica a tela de auditoria (consulta posterior); aqui só **produz** o registro.

## User Stories

### Como **operador**, quero ver por que a IA recomendou aquela ação, para confiar ou discordar com base

**Acceptance Criteria:**
- [ ] Cada linha tem um botão **"por quê?"** que expande/retrai a explicação.
- [ ] A explicação tem 3 passos: **Sinais detectados**, **Raciocínio do agente** (voz da IA), **Próxima melhor ação** (ação + prioridade /1000).
- [ ] Os sinais mostram débito/faturas/atraso, prob. do modelo, medidor + dias desde o vencimento (janela 90d) e as flags.

### Como **operador/supervisor**, quero revisar o resumo do lote antes de confirmar, para não gerar ordens por engano

**Acceptance Criteria:**
- [ ] Botão **"Confirmar lote ▸"** abre um modal de revisão.
- [ ] O modal lista a **contagem por ação** (cortar / sms / acordo / revisar / proteger), o **valor no lote de corte**, a **recuperação esperada (30d)** e o **nº de ajustes sobre a IA**.
- [ ] **Gerar lote** confirma; **Voltar** (ou clicar fora) fecha sem confirmar.
- [ ] Na PoC, "Gerar lote" é **mock** (alert) — em produção dispara o `POST /confirmar`.

## Technical Design

### Architecture

Ambos operam sobre o estado já carregado/decidido (UCs + `dec`). O drill-down é uma linha
expansível na própria grid (toggle local). A confirmação monta um resumo a partir das
decisões atuais e, em produção, envia o `POST /api/lote-corte/confirmar` (FE-00).

### Data Model

**Drill-down "por quê?"** consome, por UC: `deb`, `fat`, `dias`, `prob`, `medidor`,
`diasVenc`, `flags`, `motivo`, `rec`, `prio` (campos já definidos em FE-01).

**Resumo de confirmação** (derivado das decisões `dec`):

| Item | Cálculo |
|------|---------|
| Contagem por ação | nº de UCs por valor de `dec` (5 ações) |
| Valor no lote de corte | `Σ deb` das UCs com `dec === "cortar"` |
| Recuperação esperada (30d) | `valor do lote × recupRate (0,50)` |
| Ajustes sobre a IA (auditoria) | nº de UCs com `dec ≠ rec` |

**Payload de auditoria** (POST, ver FE-00): por UC, `{ id, recIA, decisaoOperador, prio, prob, scoreOrigem }`
+ `ciclo` e `usuario`.

### API Design

- **Confirmar:** `POST /api/lote-corte/confirmar` com `{ ciclo, usuario, decisoes:[…] }` → resumo gravado.
- O front **não** chama canais (SMS/PIX) nem executa o corte diretamente; o backend orquestra após a confirmação.

### UI/UX Design

**Drill-down "por quê?" (`.reason`)** — linha extra sob a UC, escondida por padrão, com 3 cards:

1. **Sinais detectados** — `Débito: R$X · N fatura(s) · D dias de atraso`; `Prob. de pagamento (modelo): P%`;
   `Medidor: … · diasVenc dias desde o vencimento (janela de corte: 90d)`; `Flags: …` (ou "nenhuma").
2. **Raciocínio do agente** — texto `motivo` em **voz da IA** (itálico, roxo `#5b4bd6`).
3. **Próxima melhor ação** — badge da recomendação + `Prioridade prio/1000` + nota:
   *"O operador confirma ou ajusta na coluna Decisão. A escolha final fica registrada."*

Toggle: clicar "por quê?" alterna `.open` na linha de raciocínio (abrir/fechar).

**Modal de confirmação (`#ov` / `.modal`):**
- Título: **"Confirmar geração do lote"**; subtítulo deixa claro que é revisão (mock — nada é executado).
- Linhas de resumo (`.sumrow`):
  - ✂️ Cortar · 📲 SMS / PIX antes · 🤝 Oferecer acordo · 🔎 Revisar · 🛡️ Não cortar (protegido)
  - Valor no lote de corte · Recuperação esperada (30d) · **Ajustes sobre a IA (auditoria)**
- Ações: **Voltar** (`.btn-ghost`) e **Gerar lote** (`.btn-primary`).
- Fecha ao clicar fora do modal (overlay).
- **Gerar lote (PoC):** alert explicando que em produção o backend persistiria as decisões e
  encaminharia os cortes, e que SMS/PIX e acordos seguiriam pelos canais de cobrança, **com aprovação humana**.

**RAI:** o texto do passo 3 e o subtítulo do modal reforçam human-in-the-loop e que nada é
executado pelo front. Os guardrails que forçam `proteger`/`revisar` são de FE-00/FE-01.

## Implementation Plan

### Phase 1: Explicabilidade
- [ ] Linha expansível "por quê?" com os 3 passos (sinais, raciocínio, próxima ação).
- [ ] Estilo de voz da IA no raciocínio; toggle abrir/fechar por UC.

### Phase 2: Confirmação
- [ ] Modal com resumo (contagem por ação, valor, recuperação, ajustes).
- [ ] Voltar / fechar por overlay; Gerar lote como mock (alert).
- [ ] Trocar o mock por `POST /api/lote-corte/confirmar` quando o backend existir.

## Testing Strategy

- **Unit:** montagem do resumo (contagens, valor do lote, recuperação, nº de ajustes);
  toggle do drill-down; texto dos 3 passos com os campos certos.
- **Integration:** payload do `POST /confirmar` (campos de auditoria, enum sem acento, scoreOrigem).
- **E2E:** abrir "por quê?" → ajustar decisão → confirmar → ver resumo com nº de ajustes correto.

## Rollout Plan

Entregue junto com FE-00/FE-01/FE-02 no piloto (Certel). O `POST /confirmar` real depende do
backend; até lá, "Gerar lote" permanece mock.

## Metrics & Success Criteria

- Operadores **usam o "por quê?"** (uso medido) — sinal de confiança/adoção.
- 100% das confirmações geram **registro de auditoria** com o par recomendação×decisão.
- **% de ajustes sobre a IA** acompanhado ao longo do tempo (calibração do modelo).

## Dependencies

- Campos por UC (`motivo`, `prob`, `prio`, `flags` etc.) do contrato (FE-00/FE-01).
- Parâmetro `recupRate` para a recuperação esperada (FE-02/FE-00).
- Backend `POST /api/lote-corte/confirmar` (auditoria) e, depois, persistência das decisões e encaminhamento dos cortes.

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| "Confirmar tudo" sem revisar (rubber-stamp) | Médio | Média | Resumo destaca nº de ajustes; modal obriga passo de revisão; auditoria registrada |
| Explicação genérica/pouco útil | Médio | Média | `motivo` específico por UC vindo do backend; passos com sinais reais, não texto fixo |
| Confusão sobre o que "Gerar lote" faz | Médio | Média | Subtítulo e alert deixam explícito que nada é executado no front (mock) |

## Open Questions

- [ ] O `motivo` (raciocínio) vem do modelo/LLM ou de regra do backend? Formato/limite de tamanho?
- [ ] Após confirmar, quem dispara os canais (SMS/PIX) e a execução do corte — e com qual nova aprovação?
- [ ] A auditoria fica em tela própria de consulta? (fora do escopo desta spec)
- [ ] `usuario` no payload vem de qual mecanismo de autenticação (perfis/acesso)?

## References

- Protótipo: [`../poc/poc-selecao-corte.html`](../poc/poc-selecao-corte.html) (`.reason`/`.trace`, `btn-confirm`, `#ov`, `btn-generate`)
- Spec-âncora: [FE-00](FE-00-visao-geral.md) · Irmãs: [FE-01](FE-01-grid-decisao.md) · [FE-02](FE-02-funil-kpis.md)
