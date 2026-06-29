---
name: poc-selecao-corte
description: Explica como o protótipo poc-selecao-corte.html funciona por dentro e define o contrato de dados que um backend precisa entregar para substituir os dados mockados. Use quando o pedido envolver entender, dar manutenção, ou construir/conectar um backend, API, modelo ou banco para o "Assistente IA de Seleção de Corte" (a tela de ordem de corte do E2 Comercial, suíte de inadimplência, Agentes 3+4). Gatilhos típicos: "substituir os dados mockados", "criar o backend do PoC de corte", "qual o formato que o front espera", "ligar a tela a um modelo/score real", "como o poc-selecao-corte.html funciona".
---

# PoC — Assistente IA de Seleção de Corte

Esta skill ensina **como o protótipo `poc-selecao-corte.html` funciona por dentro** e, principalmente, **qual é o contrato de dados** que um backend precisa entregar para tirar os dados mockados do meio e conectar dados reais.

## Onde estão as coisas

- Protótipo: `oseias/prototype/poc-selecao-corte.html` (HTML único, autocontido, sem backend, dados fictícios).
- Contexto de produto: `oseias/prototype/poc-scope.md`, `oseias/prototype/poc-handoff.md`, `oseias/prototype/mark-miller-feedback.md`.
- README da iniciativa de inadimplência (modelo, dataset, schema): `oseias/README.md`.

**Sempre leia o HTML atual antes de afirmar como ele se comporta** — esta skill descreve a estrutura, mas o arquivo é a fonte da verdade e pode ter mudado. Os números de linha abaixo são pontos de partida, não garantias.

## O que o PoC prova (e o que não prova)

Prova que a IA pode **triar o lote de corte de forma explicável, auditável e com humano no comando** (human-in-the-loop), priorizando por recuperação × custo e respeitando guardrails regulatórios — e que isso **cabe nos campos que já existem** no schema (`Marcado`, `Prioridade` do `ReavisoOrdemDeCorteDTO`).

**Não prova** que o modelo funciona: o score `prob` e a `prio` são escritos à mão, o `motivo` (raciocínio) é pré-roteirizado, não há backend, e o funil usa números ilustrativos. O backend é exatamente o que falta para fechar essa lacuna. Veja `mark-miller-feedback.md` (veredito CONDITIONAL: "o modelo não existe").

## Arquitetura do arquivo (3 camadas num só HTML)

1. **CSS** (`<style>`, ~linhas 10–148): tema visual Useall. Não impacta o backend.
2. **Dados mockados** (topo do `<script>`): dois arrays JS — `DATA` (as UCs da tabela) e `FUNNEL` (os estágios do funil) — mais duas constantes. **É isto que o backend substitui.**
3. **Lógica de render** (resto do `<script>`): funções que leem esses arrays e desenham tabela, KPIs e funil. Reagem ao operador mudando decisões.

O fluxo de inicialização no fim do script é simplesmente:
```js
renderFunnel();  // desenha o funil a partir de FUNNEL
render();        // desenha a tabela + KPIs a partir de DATA
```
Trocar o mock por backend = **popular `DATA` e `FUNNEL` a partir de um `fetch` antes de chamar essas duas funções**.

---

## CONTRATO DE DADOS Nº 1 — array `DATA` (uma UC por linha da tabela)

Cada objeto do array `DATA` representa uma Unidade Consumidora elegível ao corte. Estes são os campos que o front-end **lê** (se faltar algum, a tela quebra ou mostra `undefined`):

| Campo | Tipo | Significado | Valores / observações |
|---|---|---|---|
| `id` | string | Identificador da UC | ex. `"UC-70188"`. No real: nº da UC / instalação. |
| `cls` | string | Classe da UC | `"Residencial"`, `"Comercial"`, `"Industrial"`, `"Rural"`, `"Poder Público"`. |
| `muni` | string | Município | mascarado com `***` no mock por privacidade. |
| `deb` | number | Débito total em R$ | usado nos KPIs e na ordenação de valor. |
| `fat` | number | Nº de faturas em aberto | inteiro. |
| `dias` | number | Dias de atraso | inteiro. |
| `medidor` | string | Tipo de medidor | **exatamente** `"Convencional"` ou `"Digital (MDM)"`. O KPI "deslocamentos evitados" compara com a string literal `"Convencional"` — qualquer outro texto quebra a contagem. |
| `diasVenc` | number | Dias desde o vencimento | dirige a **janela regulatória de 90 dias**. O filtro "Janela ≤7d" usa `diasVenc >= 83 && diasVenc < 90`. |
| `prob` | number | Probabilidade de pagamento | **fração de 0 a 1** (0.28 = 28%), não percentual. É o **score do modelo** (hoje mockado). |
| `prio` | number | Prioridade IA | inteiro **0–1000**. Sai do `ReavisoCortes.Prioridade`. Cores: ≥700 vermelho, ≥350 laranja, senão cinza. |
| `rec` | string | Recomendação da IA (próxima melhor ação) | **enum fechado** — veja abaixo. |
| `flags` | array de `[label, tipo]` | Sinais exibidos como chips | cada item é um par `["texto", "tipo"]`. Tipos válidos: `"risk"` (vermelho), `"prot"` (proteção/azul), `"meter"` (medidor convencional/cinza), `"digi"` (digital/ciano). |
| `motivo` | string | Justificativa de 1 linha | aparece no passo 2 do "por quê?". No real: explicação gerada (regras + features que pesaram). |

### Enum de `rec` (e da decisão do operador) — **valores exatos, sem acento**
```
"cortar"    → Cortar
"sms"       → SMS / PIX antes
"acordo"    → Oferecer acordo
"revisar"   → Revisar
"proteger"  → Não cortar (protegido)
```
Esses literais aparecem em `ACAO_LABEL`, nos filtros, no menu de decisão e nos cálculos de KPI. **O backend deve devolver `rec` exatamente com uma dessas chaves.**

### Campo de runtime: `dec`
Não vem nos dados — o script cria `d.dec = d.rec` na carga (`DATA.forEach(d => d.dec = d.rec)`). É a **decisão atual do operador**, que começa igual à recomendação e muda quando ele usa o menu. Quando `dec !== rec`, a tela marca "ajustado" (rastro de auditoria). **Ao persistir a decisão no backend, é o par (`rec` da IA, `dec` do operador) que vira a trilha de auditoria.**

### Exemplo de um item real do mock (referência de formato)
```js
{
  id:"UC-48211", cls:"Residencial", muni:"Criciúma ***",
  deb:842.50, fat:3, dias:22, medidor:"Convencional", diasVenc:84,
  prob:0.18, prio:870, rec:"cortar",
  flags:[["Reincidente","risk"],["Débito alto","risk"],["Janela 90d: 6d","risk"],["Convencional","meter"]],
  motivo:"Débito alto e reincidente; janela de corte fechando (6 dias) — priorizar antes de perder o direito de suspender."
}
```

---

## CONTRATO DE DADOS Nº 2 — array `FUNNEL` (estágios do funil de cobrança)

Cada item é um estágio. Há **três tipos** (`type`), cada um com campos próprios:

- **`type:"stock"`** — um estoque da carteira (barra colorida sólida).
  `{ type:"stock", lab, n, v, c }` — `lab` rótulo, `n` nº de UCs, `v` valor R$, `c` cor da barra.
- **`type:"aviso"`** — um aviso/recuperação (barra verde, valor recuperado).
  `{ type:"aviso", lab, canal, rec, recV, preCorte? }` — `rec` clientes recuperados, `recV` valor recuperado, `canal` texto do canal, `preCorte:true` marca os avisos **antes** do corte (entram no destaque "recuperado sem precisar cortar").
- **`type:"ia"`** — o estágio onde a IA atua (barra dividida Cortar/Segurar, borda tracejada roxa).
  `{ type:"ia", lab, n, v, cut, keep }` — `cut` UCs a cortar, `keep` UCs a segurar.

O `renderFunnel()` calcula a largura das barras pela maior `v`/`recV` do array, soma os avisos `preCorte` para o destaque verde, e soma todos os avisos para a "recuperação total do ciclo". **No real, esses números vêm de uma agregação da carteira por ciclo (`ANO_MES`), não do array de UCs da tabela.**

---

## CONTRATO Nº 3 — constantes de cálculo

```js
const RECUP_RATE = 0.50;   // taxa de recuperação esperada se cortar (ilustrativa)
const CUSTO_CORTE = 120;   // custo médio de execução por corte (R$)
```
Os KPIs derivam destas constantes. No real devem virar **parâmetros por distribuidora/cooperativa** (custo de visita varia com tipo de medidor, R$ 80–200/visita; taxa de recuperação vem do histórico). Idealmente o backend entrega esses parâmetros junto, em vez de hardcoded no front.

---

## Como o front consome os dados (o que o backend precisa alimentar)

| Bloco da tela | Função | Lê de | Calcula |
|---|---|---|---|
| Tabela | `render()` | `DATA` | ordena por `prio`; aplica filtro/busca; chips de `flags`; barra de `prob`; menu de `dec` |
| Trilha "por quê?" | dentro de `render()` | `DATA` | 3 passos: sinais (`deb/fat/dias/prob/medidor/diasVenc/flags`) → `motivo` → `rec`+`prio` |
| KPIs | `updateKPIs()` | `DATA` (campo `dec`) | ver fórmulas abaixo |
| Funil | `renderFunnel()` | `FUNNEL` | larguras, recuperado pré-corte, recuperação total |
| Filtros/busca/lote/ordenação | handlers no fim | `DATA` | só mexem em estado de UI e em `dec` |
| Modal confirmar | handler `btn-confirm` | `DATA` (`dec` vs `rec`) | contagens por ação, valor do lote, nº de ajustes sobre a IA |

### Fórmulas dos KPIs (replicar no backend se for movê-las para o servidor)
```
inc       = UCs com dec === "cortar"
valorLote = soma de deb das inc
recup     = valorLote * RECUP_RATE            // "Recuperação esperada"
custo     = inc.length * CUSTO_CORTE
roi       = recup / custo                      // "ROI estimado do lote"
evitados  = UCs com dec === "proteger" E que têm alguma flag de tipo "prot"   // "Cortes indevidos evitados"
desloc    = UCs com dec !== "cortar" E medidor === "Convencional"             // "Deslocamentos evitados"
```

---

## Como ligar um backend (refactor mínimo no HTML)

O caminho de menor atrito é **manter o front quase intacto** e só trocar a origem dos dados. Hoje o fim do script é:
```js
const DATA = [ ...mock... ];
const FUNNEL = [ ...mock... ];
// ...
renderFunnel();
render();
```
Vira algo como:
```js
let DATA = [], FUNNEL = [];
async function carregar(){
  const r = await fetch("/api/lote-corte?ciclo=2026-06");   // ajustar endpoint
  const json = await r.json();
  DATA = json.ucs;          // array no formato do CONTRATO Nº 1
  FUNNEL = json.funil;      // array no formato do CONTRATO Nº 2
  DATA.forEach(d => d.dec = d.rec);   // mantém a regra do human-in-the-loop
  renderFunnel();
  render();
}
carregar();
```
E o "Gerar lote" (hoje um `alert` mock) passa a fazer `POST` com as decisões do operador:
```js
// payload de auditoria: para cada UC, a recomendação da IA e a decisão final humana
const decisoes = DATA.map(d => ({ id:d.id, recIA:d.rec, decisaoOperador:d.dec, prio:d.prio }));
await fetch("/api/lote-corte/confirmar", {method:"POST", body:JSON.stringify(decisoes)});
```
**Atenção:** `DATA` e `FUNNEL` são declarados hoje com `const` — ao ligar o backend, trocar para `let` (como acima) ou o `fetch` não consegue reatribuir.

### Shape de resposta sugerido para `GET /api/lote-corte`
```json
{
  "ciclo": "2026-06",
  "parametros": { "recupRate": 0.5, "custoCorte": 120 },
  "ucs": [ { "id":"...", "cls":"...", "deb":0, "fat":0, "dias":0,
             "medidor":"Convencional", "diasVenc":0, "prob":0.0,
             "prio":0, "rec":"cortar", "flags":[["...","risk"]], "motivo":"..." } ],
  "funil": [ { "type":"stock", "lab":"...", "n":0, "v":0, "c":"#7d8aa6" } ]
}
```

---

## Mapeamento para o domínio real (E2 Comercial)

Do `poc-handoff.md` e do `README.md` da iniciativa:

- A tela real é a **geração de ordem de corte**; a resposta de `gerarIdSelecaoReavisoOrdemDeCorte()` deve ser **enriquecida** com `Marcado` + `Prioridade` + justificativa (sugerido: job Hangfire após `TotalmenteLancado`).
- `prio` (0–1000) → grava em **`ReavisoCortes.Prioridade`**. `rec`/`dec` → reflete em **`Marcado`** do `ReavisoOrdemDeCorteDTO`.
- **Score `prob` (o bloqueador nº 1):** o modelo pós-reaviso **ainda não existe**. O rótulo do dataset atual está quebrado (`TARGET_PAGOU_ANTES_CORTE` ≈ 0,07% positivos). Precisa ser **re-extraído de `REAVISO_CORTES.CORTADO`** (`'A'` = cancelado por pagamento = 1 / `'C'` = executado = 0). Modelo previsto: LightGBM por distribuidora, split temporal por `ANO_MES`, meta **AUC ≥ 0,80 (v1)**.
- Features que vieram **constantes-zero** e precisam ser revisadas no ETL: `FLAG_PAGOU_ULTIMO_REAVISO`, `HAVIA_PRORROGACOES`, `FLAG_PRORROGOU_12M`, `FLAG_NAO_RELIGAR_AUTOMATICO`, `FLAG_CORTE_INDEVIDO_HISTORICO`. Limpar sentinela `1900-01` e `LIMITE_CORTE` lixo.

## Guardrails — **não negociáveis, devem ser impostos no backend, não só na UI**

Serviço essencial, restrição de corte (`UC_TRRESTRICAO_CORTE`), baixa renda e micro-geração → a IA recomenda **`proteger` (Não cortar) ou `revisar`**, **nunca** `cortar` automático. Decisão final sempre humana e registrada. Respeitar **Res. ANEEL 479/2012 e 1000/2021** (janela de corte). Validar limiares com **Regulatório/Jurídico** antes de qualquer uso real. No protótipo isso é só uma flag `"prot"`; no backend tem que ser uma **regra de bloqueio dura** que o score não pode sobrepor.

## Honestidade de evidência

Ao construir o backend, não invente dados de recuperação, custo de visita ou taxa de pagamento para "preencher" a tela. Enquanto o modelo não roda, deixe claro na resposta da API que o `prob` é placeholder (ex. um campo `"scoreOrigem": "mock"` vs `"modelo-v1"`), para o front poder continuar exibindo o aviso de "ilustrativo".
