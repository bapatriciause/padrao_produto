# Front-end — Funil de Cobrança & KPIs de Impacto (FE-02) Specification

**Status:** In Review
**Owner:** Patrícia Bento Antônio (R&D)
**Created:** 2026-06-25
**Last Updated:** 2026-06-25

> Spec-filha de [FE-00 Visão Geral](FE-00-visao-geral.md). Herda design system e contrato
> de dados da spec-âncora. Componentes irmãos:
> [FE-01 Grid & Decisão](FE-01-grid-decisao.md) · [FE-03 Explicabilidade & Confirmação](FE-03-explicabilidade-confirmacao.md).

## Overview

Dois blocos de **contexto e impacto** no topo da tela:

1. **Funil de cobrança do ciclo** — mostra o caminho da dívida (faturas vencidas → reaviso
   → elegível a corte → seleção da IA → cortes executados → recuperado), com os **avisos
   multicanal** que recuperam dinheiro **antes** de cortar e o ponto onde a IA atua.
2. **Faixa de KPIs** — métricas do lote que **recalculam ao vivo** conforme o operador
   ajusta decisões na grid (FE-01): recuperação esperada, indevidos evitados, ROI,
   deslocamentos evitados.

Referência viva: `.funnel` / `#funnel-stages` e `.kpis` em [`../poc/poc-selecao-corte.html`](../poc/poc-selecao-corte.html).

## Goals

- Dar ao supervisor o **impacto do lote num relance**, antes de confirmar.
- Mostrar que **avisos resolvem casos sem cortar** (recuperação preventiva) — argumento central.
- Tornar visível o **ponto onde a IA atua** (seleção da ordem de corte) dentro do funil.
- KPIs **vivos**: mudam quando a decisão do operador muda (loop com FE-01).

## Non-Goals

- Não define a grid nem a decisão por UC (ver FE-01).
- Não calcula o score nem as taxas de fundo — usa parâmetros do contrato (ver FE-00).
- Os números do funil são **ilustrativos** nesta fase (faixa real do `.xlsx`); não são saída de modelo.

## User Stories

### Como **supervisor de cobrança**, quero ver o funil do ciclo para entender quanto se recupera só com avisos, antes do corte

**Acceptance Criteria:**
- [ ] O funil mostra os estágios em ordem, com volume (UCs) e valor (R$) por estágio.
- [ ] Os estágios de **aviso** (preventivo / pré-corte / pós-corte) aparecem destacados (verde) com o recuperado.
- [ ] Um bloco de resultado resume **"recuperado sem precisar cortar"** (soma dos avisos pré-corte) e a recuperação total do ciclo.
- [ ] O estágio **"Seleção da ordem de corte"** é marcado como **"IA atua aqui"** e leva à grid ao clicar.

### Como **operador/supervisor**, quero ver os KPIs do lote mudarem quando ajusto decisões, para medir o efeito das minhas escolhas

**Acceptance Criteria:**
- [ ] KPIs: Ordens analisadas, Marcados p/ cortar, Recuperação esperada, Cortes indevidos evitados, ROI estimado, Deslocamentos evitados.
- [ ] Os KPIs **recalculam** a cada mudança de decisão na grid.
- [ ] KPIs ligados à IA têm destaque visual (card `.ai`).

## Technical Design

### Architecture

Dois componentes de leitura. O **funil** renderiza um array de estágios vindo do contrato
(`funil[]` de `GET /api/lote-corte`). Os **KPIs** são **derivados no front** a partir das
decisões atuais (`dec`) da grid + parâmetros do contrato — recalculados no mesmo `render()`/
`updateKPIs()` que a grid dispara (FE-01).

### Data Model

**Estágio do funil** (`funil[]`):

| Campo | Tipo | Uso |
|-------|------|-----|
| `type` | `stock` \| `aviso` \| `ia` | define o visual do estágio |
| `lab` | string | rótulo do estágio |
| `n` | number | nº de UCs (estágios `stock`/`ia`) |
| `v` | number | valor R$ do estágio (`stock`/`ia`) |
| `canal` | string | canais do aviso (ex.: "e-mail · WhatsApp · SMS") — só `aviso` |
| `rec` | number | clientes recuperados — só `aviso` |
| `recV` | number | valor R$ recuperado — só `aviso` |
| `preCorte` | bool | aviso ocorre **antes** do corte (entra no "recuperado sem cortar") |
| `cut` / `keep` | number | no estágio `ia`: UCs marcados p/ cortar vs. segurar |

**Parâmetros do lote** (do contrato, hoje fixos na PoC):
- `recupRate` = **0,50** (taxa de recuperação esperada se cortar).
- `custoCorte` = **R$ 120** (custo médio de execução por corte).

### API Design

- Funil: array `funil[]` dentro de `GET /api/lote-corte` (FE-00).
- KPIs: sem chamada própria — derivados de `ucs[].dec` + `parametros`.

### UI/UX Design

**Funil (`#funnel-stages`)** — cada estágio é uma linha `[ rótulo | barra | valor ]`:
- Largura da barra proporcional ao maior valor do funil (`v` ou `recV`).
- `stock`: barra de cor própria do estágio; mostra nº de UCs na barra e R$ + UCs no valor.
- `aviso`: estilo verde (recuperação), seta de retorno `↩`, canal em sub-rótulo, "recuperado N" na barra.
- `ia`: barra dividida em dois segmentos — **Cortar** (vermelho) vs **Segurar** (verde) —
  com **contorno tracejado roxo** e marcação **"IA atua aqui"**; clicável → rola até a grid.

**Estágios da PoC (ilustrativos, faixa real do `.xlsx`):**
Faturas vencidas → Aviso preventivo → Reaviso emitido → Aviso pré-corte → Em aberto/elegível
→ **Seleção da ordem de corte (IA)** → Cortes executados → Recuperado pós-corte.

**Bloco de resultado (`#fresult`):**
- Card grande: **"Recuperado sem precisar cortar (pelos avisos)"** = soma `recV`/`rec` dos avisos `preCorte`.
- Texto: recuperação total do ciclo (todos os avisos, pré + pós-corte).

**Faixa de KPIs (`.kpis`)** — cálculo a partir das decisões atuais (`dec`):

| KPI | Cálculo (PoC) | Card |
|-----|---------------|------|
| Ordens analisadas | total de UCs no lote | normal |
| Marcados p/ cortar | nº de `dec === "cortar"` | `.ai` |
| Recuperação esperada | `Σ deb(cortar) × recupRate(0,50)` | normal |
| Cortes indevidos evitados | nº de `dec === "proteger"` **com flag protetora** | `.ai` |
| ROI estimado do lote | `recuperação ÷ (nº cortar × custoCorte)`, em `×` | normal |
| Deslocamentos evitados | nº de `dec ≠ "cortar"` **com medidor Convencional** | `.ai` |

> "Cortes indevidos evitados" conta apenas UCs `proteger` que **têm sinal de proteção**
> (serviço essencial, restrição, baixa renda, micro-geração etc.), não qualquer "não cortar".

**Formatação de números:** `R$` com 2 casas (mono); valores grandes em "R$ X,Y mi" / "X mil".

## Implementation Plan

### Phase 1: Funil
- [ ] Renderizar `funil[]` com os 3 tipos de estágio e barras proporcionais.
- [ ] Bloco de resultado "recuperado sem cortar" + total do ciclo.
- [ ] Estágio IA clicável → rola até a grid (FE-01).

### Phase 2: KPIs vivos
- [ ] Calcular os 6 KPIs a partir de `dec` + parâmetros.
- [ ] Recalcular no mesmo ciclo de render da grid (a cada ajuste de decisão).
- [ ] Marcar visualmente os KPIs `.ai`.

## Testing Strategy

- **Unit:** cálculo de cada KPI (recuperação, ROI, indevidos evitados com flag, deslocamentos);
  soma de avisos `preCorte`; larguras de barra proporcionais ao máximo.
- **Integration:** consumo de `funil[]` e `parametros` do contrato.
- **E2E:** mudar decisões na grid e ver KPIs recalcularem; clicar no estágio IA e rolar à grid.

## Rollout Plan

Entregue junto com FE-00/FE-01 no piloto (Certel). Sem rollout próprio.
Trocar números ilustrativos do funil por dados reais do ciclo quando o backend fornecer.

## Metrics & Success Criteria

- Supervisor entende o impacto do lote **sem abrir relatório à parte**.
- Argumento "recuperado sem cortar" visível e quantificado.
- KPIs ao vivo usados para calibrar decisões antes de confirmar.

## Dependencies

- `funil[]` e `parametros` (`recupRate`, `custoCorte`) no contrato `GET /api/lote-corte` (FE-00).
- Decisões `dec` da grid (FE-01) para os KPIs vivos.
- Validação dos parâmetros `recupRate`/`custoCorte`/custo de deslocamento com um cliente real.

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Números do funil tomados como reais | Médio | Alta | Rótulo "números ilustrativos" no funil; trocar por dados reais no piloto |
| `recupRate`/`custoCorte` não calibrados | Médio | Alta | Parametrizar no contrato; validar com cliente; exibir como estimativa |
| KPI "indevidos evitados" inflado | Médio | Média | Só conta `proteger` **com flag protetora**, não todo "não cortar" |

## Open Questions

- [ ] Origem dos volumes/valores reais do funil por ciclo — definir com o backend.
- [ ] `recupRate` e `custoCorte` por cliente ou globais? Custo de deslocamento separado do custo de corte?
- [ ] O funil é por **ciclo** (todo o lote) ou reflete só o lote filtrado na grid?

## References

- Protótipo: [`../poc/poc-selecao-corte.html`](../poc/poc-selecao-corte.html) (`renderFunnel()`, `updateKPIs()`, `FUNNEL[]`, `RECUP_RATE`, `CUSTO_CORTE`)
- Spec-âncora: [FE-00](FE-00-visao-geral.md) · Irmãs: [FE-01](FE-01-grid-decisao.md) · [FE-03](FE-03-explicabilidade-confirmacao.md)
- Faixa real de volumes: planilha histórica de cortes/reavisos (insumo do projeto).
