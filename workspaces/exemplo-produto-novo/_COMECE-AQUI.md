# Comece aqui — Esqueleto de projeto

Esta pasta é um **modelo reutilizável**. Para cada produto novo, copie-a inteira para `workspaces/<nome-do-produto>/` e preencha os arquivos seguindo o fluxo abaixo. Os arquivos já existem vazios para você (e o Claude) saberem exatamente o que produzir em cada etapa.

> Cole **um bloco de prompt por vez** (de `prompts-v2/`), questione a saída e só então grave. Não rode capítulos inteiros de uma vez.

## Ordem de preenchimento

**Setup**
- [ ] `participant-profile.md` — seu papel, evidências e objetivo (prompt: `00-onboarding.md`)

**Dia 1 — Entender o problema**
- [ ] `insights.md` — pesquisa de mercado/cliente/concorrente/interna (prompt: `day-one/A`)
- [ ] `personas/` — 2+ personas com evidência (prompt: `day-one/B`)
- [ ] `jobs-to-be-done.md` — lente de "trabalho a ser feito" (prompt: `day-one/C`)
- [ ] `problem-statements.md` — 1-2 problemas bem definidos (prompt: `day-one/C`)
- [ ] `problem-stack-rank.md` — problemas ranqueados pela ótica do cliente (prompt: `day-one/C`)
- [ ] `hmw-questions.md` — perguntas "Como poderíamos..." (prompt: `day-one/C`)

**Dia 2 — Da ideia ao PoC**
- [ ] `opportunity-areas.md` — áreas de oportunidade (prompt: `day-two/E`)
- [ ] `ideas.md` — ideias em 3 perspectivas (prompt: `day-two/E`)
- [ ] `clusters.md` — ideias agrupadas (prompt: `day-two/E`)
- [ ] `use-cases.md` + `use-cases/<nome>.md` — top 1-2 use cases (prompt: `day-two/F`)
- [ ] `rai-fit.md` — riscos de IA responsável (prompt: `day-two/G`)
- [ ] `poc-scope.md` — escopo de 1 frase + o que o PoC precisa provar (prompt: `day-two/H`)
- [ ] `prototipo/` — arquivos do protótipo/PoC (HTML, mockups) (prompt: `day-two/H`)
- [ ] `poc-handoff.md` — notas de handoff para devs (prompt: `day-two/H`)

**Prioridade mínima se faltar tempo:** `insights.md` → 1 persona forte → 1 problem statement → 1 use case.

## Ao terminar cada etapa
Diga ao Claude: **"salvar meu trabalho"** → ele faz commit + push no GitHub.

## Exemplo pronto
Veja `workspaces/patricia-bento-antonio/` (produto de inadimplência) como referência de um projeto já preenchido.
