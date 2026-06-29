# Manual — Usando este conteúdo no Claude Cowork

Este manual adapta o fluxo do *Volaris AI Accelerator (Product Track)* para ser usado no **Cowork**, sem terminal. A metodologia e os prompts são os mesmos do repositório original (`prompts-v2/`); aqui o foco é **como operar tudo dentro do Cowork** e **como reaproveitar o método em novos produtos**.

> O conteúdo de pensamento (pesquisa, personas, problemas, ideias, PoC) é idêntico em qualquer interface do Claude. O Cowork ganha do chat puro porque **lê vários arquivos do repo de uma vez**, **grava os artefatos direto nas pastas** e consegue **salvar no Git** ("save my work").

---

## 1. Antes de começar

**O que você precisa:**
- Acesso ao Claude com **Cowork** habilitado.
- Este repositório clonado na sua máquina (já está em `Documents/accelerator-palm-beach-useall`, conectado ao seu GitHub `padrao_produto`).
- Suas evidências de cliente (entrevistas, tickets, dados, pesquisa) — opcional, mas é o que dá qualidade ao resultado.

**Abrindo o repo no Cowork:**
1. No Cowork, abra/aponte para a pasta do projeto (`accelerator-palm-beach-useall`).
2. As *skills* do projeto ficam em `.claude/skills/` e carregam automaticamente — incluindo **`save-my-work`** (salvar no Git em linguagem natural).
3. Confirme que o Claude enxerga o repo pedindo: *"Liste as pastas de topo deste repositório e o que cada uma faz."*

---

## 2. Cowork vs. Claude Code — o que muda na prática

| Recurso | Como fica no Cowork |
|---|---|
| Ler vários arquivos do repo | ✅ Funciona igual — peça "leia `insights.md` e a pasta `personas/`". |
| Gravar artefatos nas pastas | ✅ O Claude escreve direto nos arquivos da sua workspace. |
| "Save my work" (commit + push) | ✅ A skill `save-my-work` funciona desde que o Git esteja configurado (já está). |
| Rodar sessões em **paralelo** | ⚠️ Em vez de abrir várias janelas de terminal, abra **outra conversa/aba do Cowork** apontando para o mesmo projeto. |
| Conectar fontes externas (e-mail, SharePoint, etc.) | ✅ Via *connectors* do Cowork — útil para puxar evidências sem baixar arquivo. |

**Regra de ouro mantida do workshop:** cada capítulo é uma **conversa**, não um script. Cole **um bloco por vez**, questione a saída, decida o que guardar — não jogue o arquivo inteiro de uma vez.

---

## 3. Estrutura do repositório

```
accelerator-palm-beach-useall/
├─ MANUAL-COWORK.md          ← este manual
├─ modelo-projeto/           ← ESQUELETO reutilizável (copie p/ cada produto novo)
├─ prompts-v2/               ← os prompts do workshop (NÃO editar; só copiar blocos)
│  ├─ 00-onboarding.md
│  ├─ day-one/  (A → D + slides)
│  └─ day-two/  (E → H + slides + mark-miller)
├─ templates/                ← modelos originais (persona.md, ideas.md)
├─ guides/                   ← guias de repo/git
├─ troubleshooting/          ← soluções de problemas comuns
└─ workspaces/               ← SEU trabalho fica aqui
   └─ patricia-bento-antonio/ ← exemplo já preenchido (produto de inadimplência)
```

> **Não edite** `prompts-v2/`, `templates/`, `guides/` e `troubleshooting/`. Para adaptar um prompt, copie o bloco para dentro da sua workspace.

---

## 4. Começando um produto novo (a estrutura reutilizável)

Para cada produto/iniciativa nova, peça ao Cowork:

```
Copie a pasta `modelo-projeto/` para `workspaces/<nome-do-produto>/`
e renomeie os marcadores para o meu contexto. Depois me mostre o
arquivo `_COMECE-AQUI.md`.
```

Isso cria uma workspace limpa com todos os artefatos do fluxo já pré-criados (vazios), prontos para preencher. Veja `modelo-projeto/_COMECE-AQUI.md` para o passo a passo dentro da pasta.

---

## 5. O fluxo passo a passo

Sempre comece pelo **onboarding**, depois siga Dia 1 → Dia 2. Em cada etapa: cole o bloco do prompt no Cowork, responda às perguntas, e o Claude grava o artefato na sua workspace.

### Onboarding (uma vez por produto)
- **Cole:** o bloco grande de `prompts-v2/00-onboarding.md`.
- **Sai:** sua pasta em `workspaces/<nome>/` + `participant-profile.md` (seu papel, evidências, objetivo).
- No Cowork, o passo de "subir prework" vira: aponte os arquivos de evidência ou conecte a fonte (connector), em vez de copiar pelo terminal.

### Dia 1 — Entender o problema
| Etapa | Prompt | Artefato gerado |
|---|---|---|
| A. Pesquisa de mercado | `day-one/A-market-research.md` | `insights.md` |
| B. Personas | `day-one/B-user-personas.md` | `personas/*.md` |
| C. Definição de problema | `day-one/C-problem-definition-hmw-jtbd.md` | `jobs-to-be-done.md`, `problem-statements.md`, `problem-stack-rank.md`, `hmw-questions.md` |
| D. Product management com IA | `day-one/D-practical-product-management-with-ai.md` | rascunhos de conteúdo / prompt reutilizável |
| Slides Dia 1 | `day-one/1-slides-companion-day-one.md` | referência para o deck |

### Dia 2 — Da ideia ao PoC
| Etapa | Prompt | Artefato gerado |
|---|---|---|
| E. Ideação | `day-two/E-ideation.md` | `opportunity-areas.md`, `ideas.md`, `clusters.md` |
| F. Protótipo (ideia agêntica) | `day-two/F-prototype-build-for-agentic-idea.md` | `use-cases.md`, `use-cases/<nome>.md` |
| G. IA Responsável | `day-two/G-responsible-ai.md` | `rai-fit.md` |
| H. PoC para handoff | `day-two/H-poc-build-for-handoff.md` | `poc-scope.md`, arquivos do protótipo, `poc-handoff.md` |
| Slides Dia 2 | `day-two/2-slides-companion-day-two.md` | referência para o deck |
| (Extra) Avaliador comercial | `day-two/mark-miller-evaluator.md` | caso comercial afiado |

**Se ficar sem tempo, priorize:** `insights.md` → 1 persona forte → 1 problem statement → 1 use case.

---

## 6. Trabalhando em paralelo no Cowork

Pesquisas independentes (mercado, cliente, concorrentes, dados internos) podem rodar ao mesmo tempo:
1. Abra **outra conversa/aba** do Cowork no mesmo projeto.
2. Cole nela só a seção de pesquisa correspondente.
3. Traga todas as saídas de volta para o **`insights.md`** (é o ponto de convergência).

Use **uma conversa focada** para decisões de julgamento: escolher problema, refinar persona, selecionar use case, IA responsável e revisão do PoC.

---

## 7. Salvando seu trabalho

No Cowork, salvar é em linguagem natural — a skill `save-my-work` cuida do Git:

- Diga **"salvar meu trabalho"** ou **"faz backup disso"**.
- O Claude pergunta um rótulo curto (ex: *"Personas prontas"*), faz o *commit* (salva localmente) e o *push* (sobe pro GitHub).

> *Salvar* = snapshot na máquina (commit). *Backup* = cópia online no GitHub (push). Salve com frequência, ao fim de cada etapa.

---

## 8. Quando algo der errado

1. Consulte `troubleshooting/README.md` — cobre os problemas mais comuns de IA, Git e ambiente.
2. Se o "salvar" reclamar de autenticação, é o GitHub pedindo login/token — gere um *Personal Access Token* no GitHub e use no lugar da senha.
3. Se o Claude começar a "rodar o capítulo inteiro" sozinho, lembre-o: *"trabalhe seção por seção e pare para eu decidir"*.

---

## 9. Resumo de uma linha

Abra o projeto no Cowork → copie `modelo-projeto/` para uma nova workspace → siga Onboarding e os capítulos A–H colando **um bloco por vez** → grave os artefatos → diga **"salvar meu trabalho"** ao fim de cada etapa.
