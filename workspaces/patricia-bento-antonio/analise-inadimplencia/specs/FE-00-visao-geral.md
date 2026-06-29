# Front-end — Assistente IA de Seleção de Corte (Visão Geral) Specification

**Status:** In Review
**Owner:** Patrícia Bento Antônio (R&D)
**Created:** 2026-06-25
**Last Updated:** 2026-06-25

## Overview

Front-end do **Assistente de Seleção de Corte** — uma tela de apoio à decisão para a
**cobrança de energia**. Para um **lote de corte** (UCs elegíveis), a tela mostra a
recomendação da IA por UC (**próxima melhor ação**), a **prioridade** e uma **justificativa**;
o operador **confirma ou sobrescreve** cada decisão (human-in-the-loop), com **funil de
cobrança** e **KPIs de impacto** como contexto. Hoje existe um protótipo funcional (mock) —
`../poc/poc-selecao-corte.html`. Esta spec (e as filhas FE-01/02/03) definem o front-end de
produção a partir desse protótipo.

> **Esta é a spec-âncora.** Define o que vale para a tela toda: design system, navegação,
> contrato de dados e guardrails. As specs de componente referenciam esta:
> [FE-01 Grid & Decisão](FE-01-grid-decisao.md) · [FE-02 Funil & KPIs](FE-02-funil-kpis.md) ·
> [FE-03 Explicabilidade & Confirmação](FE-03-explicabilidade-confirmacao.md).

## Glossário (termos que aparecem na tela)

Só os termos do domínio que o **front exibe**. O cálculo e a origem dos dados são do backend.

| Termo | O que é |
|-------|---------|
| **UC (Unidade Consumidora)** | A ligação/instalação do cliente (o "ponto de consumo"). Cada linha da grid é uma UC. |
| **Reaviso** | Aviso de débito emitido ao cliente inadimplente **antes** de cortar. O lote de corte parte dos reavisos em aberto (aparece no funil). |
| **Ordem de corte** | A decisão de suspender o fornecimento de uma UC. A tela ajuda a **selecionar** quais UCs entram na ordem. |
| **Medidor Convencional × Digital (inteligente)** | Tipo de medidor da UC, exibido como coluna/chip. *Convencional*: corte exige deslocamento de equipe. *Digital/inteligente*: corte/religação remotos e baratos. |
| **MDM** | Sistema que faz a ligação direta com os medidores inteligentes (corte/religação remoto). Na tela aparece só como rótulo do medidor "Digital (MDM)". |
| **Janela de 90 dias** | Prazo regulatório (Res. ANEEL): passado o prazo desde o vencimento, **não se pode mais cortar** aquela dívida. A tela prioriza antes de a janela fechar e sinaliza quando ela está fechando. |

## Goals

- Tela **explicável e auditável**, com **aprovação humana** em toda decisão de corte.
- Recomendar a **próxima melhor ação** por UC (Cortar / SMS-PIX / Acordo / Revisar / Não cortar), não só "cortar/não cortar".
- Registrar a decisão do operador (e o ajuste sobre a IA) para auditoria, via API.
- Padrão visual consistente com os tokens da própria PoC (`poc-selecao-corte.html`).
- Operação rápida: filtrar, ordenar por prioridade, **marcar em lote**.

## Non-Goals

- **Não** treina nem serve o modelo (o score vem do backend; hoje é mock).
- **Não** especifica o backend, a fonte de dados nem as integrações de execução do corte (são dependências).
- **Não** envia SMS/WhatsApp/PIX de verdade nem executa corte — o front só registra a decisão.
- **Não** cobre autenticação/perfis de acesso de produção (a definir — ver Open Questions).

## User Stories

### Como **operador de cobrança**, quero ver o lote já triado pela IA (ação + prioridade + motivo) e ajustar o que for preciso, para fechar o lote rápido e com rastreabilidade

**Acceptance Criteria:**
- [ ] Cada UC mostra recomendação da IA, prioridade (0–1000) e justificativa de 1 linha.
- [ ] Consigo **sobrescrever** a decisão; o ajuste fica visível ("ajustado") e é registrado.
- [ ] Consigo filtrar, ordenar por prioridade e **aplicar uma ação a vários de uma vez**.

### Como **supervisor de cobrança**, quero ver o funil e os KPIs do lote, para entender o impacto antes de confirmar

**Acceptance Criteria:**
- [ ] Vejo o funil de cobrança e KPIs (recuperação esperada, indevidos evitados, deslocamentos evitados, ROI).
- [ ] Os KPIs recalculam ao vivo quando o operador ajusta decisões.

## Technical Design

### Architecture

**Tela separada** (front-end próprio, standalone) — não embarcada em outro sistema.
Ela **não acessa o banco diretamente**: consome uma **API de um backend C#**, que é quem
lê/grava no banco. O protótipo atual é HTML/JS puro (mock); a tela de produção é um front
próprio consumindo essa API.

```
[ Tela Seleção de Corte (front-end separado) ]
   GET  /api/lote-corte?ciclo=YYYY-MM   → lote (UCs) + funil + parâmetros
   POST /api/lote-corte/confirmar       → grava decisões (auditoria) e devolve resumo
            │
            ▼
   [ Backend C# do Assistente de Corte ]  → lê/grava o banco (fora do escopo desta spec)
```

Princípio: o front é "burro" quanto à regra — recebe `rec`/`prio`/`prob`/`flags`/`motivo`
prontos do backend C# e cuida de exibição, interação e registro da decisão do operador.
**Esta spec cobre apenas o front-end**; o backend C# e a fonte de dados são dependências.

### Data Model

O front opera sobre dois objetos vindos da API (detalhe campo-a-campo em FE-01/02):

- **UC do lote** (1 por linha da grid): identificação mascarada, classe, débito, dias,
  medidor, dias até a janela, `prob`, `prio`, `rec` (ação recomendada), `flags`, `motivo`,
  e a origem do score (`mock` | `modelo-v1`).
- **Estágio do funil**: tipo (`stock` | `aviso` | `ia`) + rótulos/valores.
- **Decisão do operador** (`dec`): criada no front, inicia igual à recomendação da IA.
  O par (`rec` da IA, `dec` do operador) é o que vira **auditoria** no POST.

> LGPD: o front **nunca** exibe o id cru da UC — só um id mascarado (ex.: `UC-70188`).
> Município também mascarado. Detalhe em FE-01.

### API Design

Contrato que o **front consome** (especificado do ponto de vista do front; o backend é dependência):

- `GET /api/lote-corte?ciclo=YYYY-MM` → `{ ciclo, parametros:{recupRate,custoCorte}, ucs:[…], funil:[…] }`
- `POST /api/lote-corte/confirmar` → `{ ciclo, usuario, decisoes:[{id, recIA, decisaoOperador, prio, prob, scoreOrigem}] }` → resumo do lote.

Enum de ação (`rec`/`dec`), valores exatos, sem acento: `cortar`, `sms`, `acordo`, `revisar`, `proteger`.

### UI/UX Design

Protótipo de referência (visual e interações): [`../poc/poc-selecao-corte.html`](../poc/poc-selecao-corte.html).

**Regiões da tela** (cada uma com sua spec):
1. Cabeçalho + avisos (PoC/RAI).
2. **Funil de cobrança + KPIs** → FE-02.
3. Barra de ferramentas: filtros, busca, ordenar, **marcar em lote**, confirmar → FE-01.
4. **Grid de triagem** (UC × ação/prioridade/decisão) → FE-01.
5. **Drill-down "por quê?"** e **modal de confirmação** → FE-03.

**Design system (tokens definidos na própria PoC `poc-selecao-corte.html`):**
- Fontes: **Roboto** (texto) + **Roboto Mono** (números).
- Gradiente de header: `#5026a6 → #2b4fc4 → #1f86d4 → #2bb8e8`.
- Cores: accent `#1e88e5`/`#1669bb`; voz da IA `#5b4bd6`; positivo `#1e9e57`; alerta `#e53935`.
- Cards: cantos arredondados (10–14px), borda `#e6e9f0`, sombra suave.

**Guardrails no front (Responsible AI):**
- UCs com **serviço essencial, restrição de corte, baixa renda, micro-geração** ou **janela
  >90 dias** vêm como `proteger`/`revisar` — o front **não permite** ação "cortar" sem
  sobrescrita explícita e registrada do operador.
- Campos **indisponíveis** (`fat`, `dias`, `medidor` quando `null`) exibem "—" + aviso, nunca um valor inventado.
- O selo de origem do score (`mock` vs `modelo-v1`) é visível enquanto o modelo não estiver treinado.

## Implementation Plan

### Phase 1: Esqueleto e contrato
- [ ] Estrutura da tela + design system (tokens) aplicados.
- [ ] Consumir `GET /api/lote-corte` (mock server ou backend) e renderizar grid + funil + KPIs.
- [ ] Tratar `null` em campos indisponíveis e exibir selo de origem do score.

### Phase 2: Interação e decisão
- [ ] Decisão do operador (override) + tag "ajustado"; filtros, ordenação, marcar em lote (FE-01).
- [ ] Drill-down "por quê?" e modal de confirmação + `POST /confirmar` (FE-03).

### Phase 3: Integração via backend C#
- [ ] Trocar o mock pelo backend C# real (`GET`/`POST`); na confirmação, o backend persiste as decisões e encaminha os cortes. O front segue como tela separada.

## Testing Strategy

- **Unit:** renderização da grid, recálculo de KPIs, lógica de filtro/ordenação/lote, mascaramento de id.
- **Integration:** consumo do contrato da API (campos exatos, enum de ação, `null` em lacunas).
- **E2E:** fluxo operador — abrir lote → ajustar → confirmar → ver resumo/auditoria.
- **Acessibilidade/visual:** navegação por teclado; conformidade com os tokens da PoC.

## Rollout Plan

Piloto com **1 cliente (Certel)** num ciclo, atrás de feature flag.
Validar com operador real antes de liberar para a base.

## Metrics & Success Criteria

- Operador fecha o lote sem abrir UC por UC; % de ajustes sobre a IA (auditoria) monitorado.
- Redução de **corte indevido** e de **deslocamento à toa** (medido no piloto).
- Tempo de triagem do lote ↓ vs. processo manual atual.

## Dependencies

- **Backend C#** do Assistente de Corte (API `lote-corte`) — lê/grava o banco; fora do escopo desta spec.
- **Modelo** pós-reaviso (score real) — depende da re-extração do dataset (ver `../bilhete-reextracao-dataset.md`).
- **Fonte de dados de cobrança** (via backend C#) — fora do escopo; o front só conhece o contrato da API.
- **Canais** (SMS/WhatsApp/PIX) e **execução remota do corte** (medidores inteligentes / MDM) — integração futura, via backend.

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Modelo não pronto (score mock) | Alto | Alta | Selo de origem do score visível; UI pronta para trocar `mock`→`modelo-v1` sem mudar contrato |
| Campos `fat`/`dias`/`medidor` ausentes na origem | Médio | Alta | Exibir "—" + aviso; KPIs que dependem deles ficam degradados e sinalizados |
| Operador "confirmar tudo" sem revisar (rubber-stamp) | Médio | Média | Destaque dos casos de guardrail; auditoria de ajustes; treinamento no piloto |
| Exposição de dado sensível (id da UC) | Alto | Baixa | Mascaramento obrigatório no front; nunca logar o id cru |

## Open Questions

- [ ] Origem futura de `fat` (nº faturas), `dias` (atraso) e `medidor` — definir com o backend.
- [ ] Limiar da janela de 90 dias e derivação de `diasVenc` — validar com Regulatório/Jurídico.
- [x] ~~A tela embarca em outro sistema ou roda separada?~~ **Decidido:** tela separada (standalone) consumindo a API do backend C#.
- [ ] Perfis de acesso: operador (decide) vs supervisor (só vê)?

## References

- Protótipo: [`../poc/poc-selecao-corte.html`](../poc/poc-selecao-corte.html)
- Escopo/lock: [`../poc/poc-scope.md`](../poc/poc-scope.md) · Handoff: [`../poc/poc-handoff.md`](../poc/poc-handoff.md)
- Gate comercial: [`../poc/mark-miller-feedback.md`](../poc/mark-miller-feedback.md)
- Dados/re-extração: [`../bilhete-reextracao-dataset.md`](../bilhete-reextracao-dataset.md) · EDA: [`../saidas/relatorio_qualidade.md`](../saidas/relatorio_qualidade.md)
- Specs filhas: FE-01 (Grid & Decisão), FE-02 (Funil & KPIs), FE-03 (Explicabilidade & Confirmação)
