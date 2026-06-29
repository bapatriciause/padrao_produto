# Motor de Detecção de Irregularidades (Perdas Não-Técnicas)

Protótipo de detecção de fraude/desvio de energia que roda sobre dados reais,
sem depender de casos rotulados.

Há dois executáveis:
- **`motor_multicliente.py`** — processa os **5 clientes** nos 2 formatos de
  dados e gera ranking por cliente + consolidado. **Use este.**
- `motor_deteccao.py` — versão inicial, só Coopera (mantida como referência).

## Clientes e formatos

| Cliente | Formato | Origem |
|---|---|---|
| Coopera | análise de leitura (3 meses, BT) | `Datasets 2/` |
| Aliança, Chesp, Cetril, Cersul | histórico faturamento (24 meses) | `Datasets teste/` |

São distribuidoras distintas — **não se cruzam por IDUC**, cada uma é analisada
isoladamente. O formato de faturamento habilita atributos extras (classe,
benchmark do sistema/peer, micro-geração, sazonalidade, z-score de 12 meses).

## Por que esta abordagem

Como ainda **não há base de casos confirmados** (fraude/legítimo) para treino
supervisionado, o motor combina duas camadas que **não precisam de rótulos**:

| Camada | Técnica | Papel |
|---|---|---|
| 1. Regras determinísticas | lógica de negócio | Alta precisão, 100% explicável |
| 2. Anomalia não-supervisionada | Isolation Forest | Ganho de recall (acha padrões fora das regras) |
| 3. Score combinado | 0,65·regras + 0,35·anomalia | Priorização para inspeção |

Quando a base de casos confirmados existir, a Camada 2 evolui para um
classificador supervisionado (XGBoost/LightGBM) reaproveitando os mesmos atributos.

## Regras implementadas

| Regra | Condição | Severidade |
|---|---|---|
| Ligação clandestina | UC desligada (`LIGADO=N`) com consumo > 0 | 100 (CRÍTICA) |
| Queda para zero | Consumo zerou tendo histórico, ligada e lida | 80 |
| Queda brusca | Queda ≥ 60% vs média dos 3 meses | 60 |
| Troca + queda | Troca de medidor com queda ≥ 30% | 45 |
| Tarifa social — consumo muito alto | Baixa renda/desconto/BPC com média 12m ≥ 500 kWh | 55 |
| Tarifa social — consumo alto | Baixa renda/desconto/BPC com média 12m 300-500 kWh | 35 |
| Peer baixo | Consumo < 25% da média do sistema p/ a classe + queda | 40 |
| Zero persistente | 4 meses zerados (validar imóvel vago) | 35 |
| Queda moderada | Queda entre 40% e 60% | 25 |

> **Tarifa social** é identificada pela **subclasse** (`RESIDENCIAL BAIXA RENDA`,
> `BAIXA RENDA`, `DESCONTO SOCIAL`, `BPC`) ou pela **tarifa** (`B1r`/`B1d`),
> porque o campo `FLAG_BAIXA_RENDA` veio **vazio (0)** em toda a base. O corte de
> consumo (300/500 kWh) é **regulatório** e deve ser validado com a área de
> regulação. Só se aplica aos 4 distribuidores; Coopera não traz subclasse.

**Sempre excluídos da suspeita** (não são fraude):
- UCs sem leitura no período (`IDNAOLEITURA ≠ 0`) → reagendar leitura
- UCs desligadas sem consumo → situação normal

## Tratamento de sazonalidade (rural / irrigação)

UCs rurais, agropecuárias ou de irrigação (`NOME_CLASSE`/`NOME_SUBCLASSE` com
"rural"/"agro", ou `ENERGIA_IRRIGACAO` em 2/3) têm oscilação sazonal legítima.
Para elas, a queda é avaliada **ano-a-ano** (mês corrente vs **mesmo mês do ano
anterior**), não contra a média recente — assim entressafra não vira falso
positivo. Para as demais (residencial/comercial, estáveis), mantém-se a
comparação contra a média dos 3 meses anteriores.

> `FLAG_SAZONAL` veio quase vazio (declaração cadastral rara), por isso a
> sazonalidade é inferida por classe/irrigação, não por esse flag.

## Como rodar

**Modo padrão (anonimizado — seguro para versionar/compartilhar):**
```bash
python motor_multicliente.py     # detecção -> saidas/ranking_*.csv
python gerar_dashboard.py        # dashboards -> saidas/dashboard_<cliente>.html
```

**Modo real (uso interno — IDUC e nomes verdadeiros, para validação/inspeção):**
```bash
FRAUDE_REAL=1 python motor_multicliente.py    # -> saidas-real/ranking_*.csv
FRAUDE_REAL=1 python gerar_dashboard.py        # -> saidas-real/dashboard_<cliente>.html
```
A pasta `saidas-real/` é **ignorada pelo Git** (`.gitignore`) — os dados reais
nunca sobem para o repositório. No Windows (PowerShell): `$env:FRAUDE_REAL=1; python ...`.

Requisitos: `pandas`, `numpy`, `scikit-learn`.

## Dashboard (persona faturamento × financeiro)

`gerar_dashboard.py` produz **um dashboard por cliente** (segregação de dados —
cada distribuidora vê apenas as próprias UCs): `saidas/dashboard_<cliente>.html`
+ um `saidas/index.html` de navegação. Cada arquivo é autocontido e abre no
navegador. Desenhado para o usuário de faturamento/financeiro: **R$ em risco/ano**
como métrica principal, fila priorizada **por valor recuperável**, R$ por
prioridade e drill-down por UC com os motivos. Tiles de KPI são clicáveis e
abrem a composição do valor (por nível e por tipo de irregularidade).

**Abas funcionais** (barra de módulos E2): **Dashboard** (KPIs + R$ por nível +
por tipo) · **Alertas & triagem** (fila com filtros, busca, drill-down) ·
**Mapa** (Leaflet/OpenStreetMap com pinos por nível de risco — **ILUSTRATIVO**:
município real via IBGE, mas posição por UC sintética até integrar a BDGD;
plota as ~400 UCs de maior valor) · **Distribuição geográfica** (R$ por
município — agregação) · **Parâmetros do modelo** (regras, pesos e metodologia
reais do motor, importados de `motor_multicliente`).

**Tema:** padrão visual **E2 ZeroPerdas** (tokens da spec v1.2 —
`docs-plataforma-deteccao-fraudes-v1.2.md`): tema claro, header em gradiente da
suíte E2, Roboto/Roboto Mono, escala de risco como cor primária, voz da IA em
violeta. A validar contra o guia oficial do E2.

**Estimativa financeira** (em `estimar_financeiro`): energia não faturada =
(consumo de referência − consumo atual) × tarifa efetiva do cliente. A tarifa
efetiva vem de `VALOR_TOTAL_MES / KWH_REAL` (mediana, meses ≥100 kWh); Coopera
usa premissa de R$ 0,95/kWh (não há valor faturado nesse formato). O gap é
**winsorizado no P99** por cliente para não inflar o total com baselines
implausíveis (erro de leitura). É ESTIMATIVA de priorização, não perda confirmada.

## Saída

Em `saidas/`: um `ranking_<cliente>.csv` por cliente + `ranking_consolidado.csv`.
Cada UC suspeita traz `prioridade`, `score_final`, scores de regra/anomalia,
consumo atual/médio, % de queda (recente e ano-a-ano), peer, flags e o campo
**`motivos`** — explicabilidade para o inspetor.

Prioridades: **CRÍTICA** (clandestina) → **ALTA** (≥70) → **MÉDIA** (≥40) →
**BAIXA** (watchlist).

## Parâmetros calibráveis

No topo de `motor_multicliente.py`: limiares de queda, corte de consumo da
tarifa social, pesos das regras e os pesos da combinação final. Devem ser
recalibrados com o **retorno das inspeções de campo**.

## Limitações conhecidas

- **Coopera** (formato análise de leitura) não traz classe, subclasse, peer,
  micro-geração nem 12 meses — então não tem tratamento de sazonalidade nem
  regra de tarifa social; usa só comparação com o próprio histórico de 3 meses.
- Sem rótulos, os scores são **indicadores de risco**, não probabilidade de
  fraude. A validação de campo é o que transforma isso em modelo supervisionado.
- Cortes regulatórios (ex.: consumo da tarifa social) exigem validação com a
  área de regulação antes de virar ação oficial.

## Roadmap

1. **Agora:** regras + anomalia sobre dados reais (este protótipo)
2. **Curto prazo:** calibrar limiares com retorno de campo; cruzar com histórico
   de 24 meses (datasets de faturamento) para features de tendência
3. **Médio prazo:** modelo supervisionado com a base de ~6.942 casos confirmados
4. **Longo prazo:** integração com a plataforma E2 ZeroPerdas (fila de alertas
   com aprovação humana, mapa, dashboard)
