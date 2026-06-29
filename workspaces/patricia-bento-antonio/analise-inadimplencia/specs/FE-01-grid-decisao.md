# Front-end — Grid de Triagem & Decisão do Operador (FE-01) Specification

**Status:** In Review
**Owner:** Patrícia Bento Antônio (R&D)
**Created:** 2026-06-25
**Last Updated:** 2026-06-25

> Spec-filha de [FE-00 Visão Geral](FE-00-visao-geral.md). Herda design system, contrato de
> dados, enum de ação e guardrails de RAI da spec-âncora. Componentes irmãos:
> [FE-02 Funil & KPIs](FE-02-funil-kpis.md) · [FE-03 Explicabilidade & Confirmação](FE-03-explicabilidade-confirmacao.md).

## Overview

A **grid de triagem** é o núcleo da tela: uma tabela onde cada linha é uma **UC do lote
de corte**, mostrando os sinais, a probabilidade de pagamento, a **prioridade da IA**, a
**recomendação (próxima melhor ação)** e a **decisão do operador**. Acompanha a **barra de
ferramentas** (filtros, busca, ordenação por prioridade e marcação em lote). É onde o
operador fecha o lote — confirmando ou sobrescrevendo a IA, com rastreabilidade.

Referência viva: tabela `#tabela` e barra `.toolbar` em [`../poc/poc-selecao-corte.html`](../poc/poc-selecao-corte.html).

## Goals

- Mostrar o lote **já ordenado por prioridade** (decrescente por padrão), pronto para fechar.
- Permitir **sobrescrever** a decisão da IA por UC, deixando o ajuste **visível e auditável**.
- Operação rápida em volume: **filtrar**, **buscar**, **ordenar** e **aplicar ação em lote**.
- Tornar os sinais de risco/proteção legíveis num relance (chips), sem abrir cada UC.

## Non-Goals

- Não define o cálculo de `prob`/`prio`/`rec`/`motivo` (vem pronto do backend — ver FE-00).
- Não cobre o drill-down "por quê?" nem o modal de confirmação (ver FE-03).
- Não cobre o funil nem os KPIs (ver FE-02).
- Não executa corte nem envia mensagem — só registra a decisão.

## User Stories

### Como **operador de cobrança**, quero ver o lote triado e ordenado por prioridade para tratar primeiro o que mais importa

**Acceptance Criteria:**
- [ ] A grid carrega ordenada por **Prioridade IA decrescente**.
- [ ] Clicar no cabeçalho **Prioridade IA ⇅** alterna entre decrescente e crescente.
- [ ] A prioridade é exibida com cor por faixa: **≥700 vermelho**, **≥350 laranja**, **<350 cinza**.

### Como **operador**, quero ajustar a decisão de uma UC quando discordo da IA, e que esse ajuste fique registrado

**Acceptance Criteria:**
- [ ] Cada linha tem um seletor **Decisão do operador** com as 5 ações (`cortar`, `sms`, `acordo`, `revisar`, `proteger`).
- [ ] O seletor inicia no valor recomendado pela IA (`dec = rec`).
- [ ] Quando a decisão difere da recomendação, a linha mostra a tag **"ajustado"**.
- [ ] Ao mudar a decisão, KPIs (FE-02) e contadores recalculam ao vivo.

### Como **operador**, quero filtrar, buscar e marcar vários de uma vez para fechar o lote rápido

**Acceptance Criteria:**
- [ ] Filtros por ação (Todos / Cortar / SMS-PIX / Acordo / Revisar / Não cortar) + filtro **⏳ Janela ≤7d**.
- [ ] Busca por **UC, classe ou município** (case-insensitive).
- [ ] **Aplicar aos filtrados**: uma ação escolhida é aplicada a todas as linhas que passam pelo filtro + busca atuais.

## Technical Design

### Architecture

Componente de tabela renderizado a partir do array de UCs do lote (`GET /api/lote-corte`,
ver FE-00). O estado de decisão (`dec`) vive no front; o filtro/busca/ordenação são locais.
Toda mudança chama um `render()` que reaplica filtro → busca → ordenação e re-renderiza.

### Data Model

Cada **UC do lote** (1 linha) — campos consumidos pela grid (do contrato do backend):

| Campo | Tipo | Uso na grid | Observação |
|-------|------|-------------|------------|
| `id` | string | Coluna UC (negrito) | **Mascarado** (ex.: `UC-70188`) — nunca o IDUC cru (LGPD) |
| `muni` | string | Sub-linha do UC | **Mascarado** (ex.: `Içara ***`) |
| `cls` | string | Coluna Classe | Residencial / Comercial / Industrial / Rural / Poder Público |
| `deb` | number | Coluna Débito | `R$` com 2 casas, fonte mono, alinhado à direita |
| `fat` | number | Coluna Fat. | nº de faturas em aberto |
| `dias` | number | Coluna Atraso | exibido como `Xd` |
| `prob` | number 0–1 | Coluna Prob. pagto | barra + `%`; cor por faixa (ver abaixo) |
| `prio` | number 0–1000 | Coluna Prioridade IA | cor por faixa; coluna ordenável |
| `rec` | enum ação | Coluna Recomendação IA | badge colorido + rótulo |
| `flags` | `[texto, tipo][]` | Coluna Sinais | chips; `tipo` ∈ `risk` `prot` `meter` `digi` |
| `motivo` | string | (usado em FE-03) | justificativa de 1 linha |
| `medidor` | string | (usado em FE-02/03) | `Convencional` / `Digital (MDM)` |
| `diasVenc` | number | (filtro Janela) | dias desde o vencimento; janela de corte = 90d |
| `dec` | enum ação | Coluna Decisão | **criado no front**, inicia = `rec` |

**Enum de ação** (valores exatos, sem acento): `cortar`, `sms`, `acordo`, `revisar`, `proteger`.
Rótulos exibidos: `cortar`→"Cortar", `sms`→"SMS / PIX antes", `acordo`→"Oferecer acordo",
`revisar`→"Revisar", `proteger`→"Não cortar".

### API Design

Consome o lote de FE-00 (`GET /api/lote-corte?ciclo=YYYY-MM`). Não faz chamada própria;
o POST de confirmação é de FE-03.

### UI/UX Design

**Colunas da tabela** (na ordem da PoC):
`UC / Município` · `Classe` · `Débito`(num) · `Fat.`(num) · `Atraso`(num) · `Sinais` ·
`Prob. pagto` · `Prioridade IA ⇅`(num, ordenável) · `Recomendação IA` · `Decisão do operador` · `(por quê?)`.

**Cores por faixa:**
- `prob`: `< 0,30` vermelho `#e53935` · `< 0,55` laranja `#fb8c00` · senão verde `#2e7d32`.
- `prio`: `≥ 700` vermelho · `≥ 350` laranja · senão cinza `#7d8aa6`.

**Chips de sinais (`flags`):**
- `risk` (fundo rosa, texto vermelho): ex. "Débito alto", "Reincidente", "Bloqueio religação", "Janela 90d: 6d", "Janela >90d · vedado".
- `prot` (fundo azul-claro, texto azul): ex. "Baixa renda", "Restrição de corte", "Serviço essencial", "Micro-geração", "1ª suspensão 12m", "Fatura posterior paga", "Rural / safra", "Fatura valor baixo".
- `meter` (cinza): "Convencional". `digi` (azul-petróleo): "Digital · MDM".
- Sem flags → "—".

**Badges de recomendação/decisão** (mesma paleta de FE-00):
`cortar` vermelho · `sms` azul · `acordo` roxo (IA) · `revisar` laranja · `proteger` verde — cada um com um "dot" da cor.

**Override e auditoria:** seletor `Decisão do operador` por linha; quando `dec ≠ rec`,
mostrar tag **"ajustado"** ao lado. O par (`rec`, `dec`) é o registro de auditoria (POST em FE-03).

**Barra de ferramentas:**
- **Filtros** (botões pílula, 1 ativo): `todos` · `cortar` · `sms` · `acordo` · `revisar` · `proteger` · `janela`.
  - Filtros de ação filtram pela **decisão atual** (`dec`), não pela recomendação.
  - **Janela ≤7d**: mostra UCs com `83 ≤ diasVenc < 90` (janela de corte fechando).
- **Busca**: casa contra `id + classe + município` em minúsculas.
- **Aplicar aos filtrados**: `select` de ação + botão "aplicar" → seta `dec` em todas as linhas que passam por filtro + busca.
- **Ordenar**: clique no cabeçalho `Prioridade IA ⇅` alterna asc/desc.
- Botão **"Confirmar lote ▸"** abre o modal (FE-03).

**Guardrail de RAI na grid:** linhas marcadas pelo backend como `proteger`/`revisar` por
serviço essencial, restrição de corte, baixa renda, micro-geração ou janela >90 dias **não
podem** ir para `cortar` sem sobrescrita explícita do operador — e a sobrescrita fica
registrada como ajuste (ver FE-00 › Guardrails).

## Implementation Plan

### Phase 1: Renderização
- [ ] Renderizar a grid a partir do array de UCs (todas as colunas, formatação mono dos números).
- [ ] Aplicar cores de `prob`/`prio` por faixa e chips de `flags` por tipo.
- [ ] Tratar campos `null` (`fat`/`dias`/`medidor`) com "—" (ver FE-00).

### Phase 2: Interação
- [ ] Ordenação por prioridade (toggle) e seletor de decisão com tag "ajustado".
- [ ] Filtros + busca + "aplicar aos filtrados".
- [ ] Disparar recálculo de KPIs (FE-02) a cada mudança de decisão.

## Testing Strategy

- **Unit:** mascaramento de `id`/`muni`; cores por faixa de `prob`/`prio`; lógica de filtro
  (inclui `janela 83–89d`), busca e ordenação; aplicação em lote só nos filtrados.
- **Integration:** consumo do contrato (campos exatos, enum sem acento, `null` em lacunas).
- **E2E:** filtrar → aplicar em lote → ajustar uma linha → ver "ajustado" e KPIs mudarem.
- **Acessibilidade:** seletor e botões navegáveis por teclado; contraste dos chips/badges.

## Rollout Plan

Entregue junto com FE-00 no piloto (Certel), atrás de feature flag. Sem rollout próprio.

## Metrics & Success Criteria

- Operador fecha o lote **sem abrir UC por UC**.
- **% de ajustes sobre a IA** (overrides) monitorado como sinal de calibração do modelo.
- Tempo de triagem do lote menor que o processo manual atual.

## Dependencies

- Contrato `GET /api/lote-corte` (FE-00) com campos da grid prontos.
- KPIs (FE-02) e modal/explicabilidade (FE-03) para o fluxo completo.

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Operador aplica "cortar" em lote sem revisar | Médio | Média | Guardrails bloqueiam casos protegidos; tag "ajustado" e auditoria de overrides |
| Campos `fat`/`dias`/`medidor` ausentes | Médio | Alta | Exibir "—"; não inventar valor; sinalizar |
| Filtro de ação confundir `rec` vs `dec` | Baixo | Média | Filtro opera sempre sobre a **decisão atual** (`dec`); documentar no tooltip |
| Exposição de IDUC/município | Alto | Baixa | Mascaramento obrigatório no front |

## Open Questions

- [ ] Origem futura de `fat`, `dias` e `medidor` — definir com o backend (herdado de FE-00).
- [ ] Derivação e limiar de `diasVenc` para o filtro de janela — validar com Regulatório/Jurídico.
- [ ] Paginação/virtualização para lotes grandes (a PoC tem 14 linhas; produção terá milhares).

## References

- Protótipo: [`../poc/poc-selecao-corte.html`](../poc/poc-selecao-corte.html) (`#tabela`, `.toolbar`, `render()`, `passaFiltro()`)
- Spec-âncora: [FE-00](FE-00-visao-geral.md) · Irmãs: [FE-02](FE-02-funil-kpis.md) · [FE-03](FE-03-explicabilidade-confirmacao.md)
