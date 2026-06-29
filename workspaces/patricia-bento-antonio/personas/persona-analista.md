# Renata — Analista de Faturamento/Perdas que dispara as ações e teme o falso positivo

> **Confiança: DIRECIONAL.** Persona inferida dos padrões operacionais de
> Cláudio/técnico e Deise/CERBRANORTE (time pequeno, dados imperfeitos, retrabalho
> manual) e do contexto de faturamento. **Sem entrevista direta ainda** — validar.

## Entrevistas de Origem

- **Interviews this persona draws from:** Deise/CERBRANORTE e padrões de Cláudio/técnico (operação enxuta, qualidade de dado), contexto de faturamento das distribuidoras.
- **What makes this group distinct:** É **quem opera o painel todo dia** — trabalha a fila, analisa cada UC e **dispara (ou não) a inspeção**. Vive entre a meta de recuperação e o medo de mandar o campo num caso errado. É a persona faturamento×financeiro que definimos como usuária do sistema.

## O Mundo da Renata

Renata trabalha no faturamento/perdas de uma distribuidora regional. Todo mês, depois do fechamento, ela enfrenta um volume grande de unidades consumidoras e precisa decidir **onde valea pena agir**. O time é pequeno — às vezes é ela e mais uma pessoa. Ela cruza dados no sistema comercial, monta planilhas, e usa muito a experiência para separar "fraude provável" de "queda explicável". Quando abre uma ordem de serviço para o campo e não dá em nada, ela sente que desperdiçou um recurso caro e que sua credibilidade caiu um pouco. E ela tem um medo concreto: **autuar o cliente errado** — uma família de baixa renda, um consumo sazonal legítimo — e gerar uma reclamação, um processo, uma dor de cabeça jurídica.

## Motivações & Objetivos

- Bater a meta de recuperação atacando os **casos certos** (maior valor + mais prováveis).
- Reduzir falso positivo — não mandar o campo à toa.
- Ter **justificativa clara** para abrir cada OS (e se proteger se questionada).
- Não errar com cliente sensível (baixa renda, sazonal, micro-geração).
- Tirar o trabalho braçal de planilha das costas.

## Dores & Frustrações

- Volume alto de UCs e tempo curto após o fechamento.
- Falso positivo custa caro: deslocamento de campo, retrabalho, credibilidade.
- Falta de explicação do "por quê" — sistemas que cospem uma lista sem motivo.
- Sazonalidade rural e micro-geração que parecem fraude mas não são.
- Cruzamento manual entre sistemas; planilhas que ela mantém na mão.
- Medo do corte/autuação indevida (risco jurídico e de imagem).

## Soluções de Contorno

- Planilhas próprias com filtros e regras pessoais ("se caiu mais de X% eu olho").
- Cruzamento manual com o histórico no sistema comercial, caso a caso.
- Memória/experiência para descartar os casos "que ela já conhece".
- Conferência dupla antes de abrir OS — porque confiar 100% é arriscado.

## Mapa de Empatia

| Diz | Pensa |
|---|---|
| "Por que esse caso está aqui? Me mostra o motivo." | "Se eu mandar o campo e não for nada, sobra pra mim." |
| "Esse é rural, deve ser safra — não é fraude." | "Quero atacar os que valem a pena e ter como justificar." |
| Sente | Faz |
| Pressionada pela meta, insegura com falso positivo, cansada de planilha. | Trabalha a fila, filtra, cruza dados, decide e dispara (ou suprime) a OS. |

## Como Toma Decisões

- **O que influencia:** clareza do motivo, valor recuperável do caso, confiança no dado, possibilidade de justificar a ação depois.
- **O que a faz resistir:** muitos falsos positivos (perde a confiança rápido); critério opaco ("não sei por que ele apontou isso"); esforço alto para validar cada caso; risco de expor a empresa.

## Como Vivencia o Produto

- **Onde encaixa:** a **fila priorizada por valor**, os **motivos** explicados por UC, o drill-down com consumo e referência, o filtro por nível. É a tela de trabalho dela.
- **Onde falha:** ela precisa **abrir a OS** (integração com o E2 Comercial) e **registrar o resultado** da inspeção; hoje o painel aponta, mas não fecha o ciclo. Quer marcar "verificado/limpo" para o caso não voltar.
- **O que gostaria diferente:** botão "abrir OS" pré-preenchido; registrar o desfecho (confirmado/não) para **calibrar o modelo**; suprimir temporariamente UC já inspecionada.

## Pressões Externas

- Meta de redução de perdas e prazo do fechamento mensal.
- ANEEL e regras de faturamento.
- LGPD e dados sensíveis do consumidor.
- Risco trabalhista/jurídico de corte ou autuação indevida.

## Citações-Chave

> "Antes de eu mandar alguém a campo, preciso saber por que esse caso está na lista."

> "Se a ferramenta me enche de falso positivo uma vez, na semana seguinte eu já não confio nela."

> "Esse consumo caiu, mas é irrigação — no ano passado, no mesmo mês, foi igual. Isso não é fraude."

> "Eu até abro a inspeção, mas tenho que conseguir justificar depois, com dado, se alguém perguntar."

## Estilo de Comunicação

- **Como pede:** quer ver o motivo e o histórico junto ("me mostra a conta"). Pragmática, vai direto ao caso.
- **Como expressa frustração:** "isso aqui é sazonal, não devia estar na fila" / "de novo falso positivo".
- **Como recusa:** se não confia no critério, volta para a planilha dela.
- **O que a convence:** acertar os primeiros casos (precisão no topo da fila) e poder justificar cada ação com dado.

## Resumo — por que a Renata importa para a validação

Renata valida a **camada operacional**: ela dirá se a fila é confiável, se os motivos fazem sentido, se a sazonalidade/baixa renda estão bem tratadas e se ela conseguiria **agir e se justificar**. É ela quem sente o falso positivo na pele. Se ela não confiar no topo da fila, volta para a planilha — e a solução morre na prática, independentemente do que o diretor aprova. Para ela, a validação é: *"eu mandaria o campo nesses casos e conseguiria explicar por quê?"*
