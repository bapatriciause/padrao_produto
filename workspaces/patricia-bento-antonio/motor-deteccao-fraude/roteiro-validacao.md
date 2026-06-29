# Roteiro de Validação — Plataforma de Detecção de Fraude (E2 ZeroPerdas)

Objetivo: testar, com dois usuários reais, se a solução **funciona na prática**
(analista) e se **vale o investimento** (diretor) — antes de evoluir o produto.

> As personas Marcos (diretor) e Renata (analista) são **direcionais**. Estas
> sessões servem também para **validar as próprias personas**: confirme se a
> realidade da pessoa bate com a persona, e ajuste depois.

---

## A regra de ouro (estilo *Mom Test*)

1. **Pergunte sobre comportamento real e passado, não sobre hipótese/opinião.**
   "Você usaria isso?" gera um "sim" educado e inútil. "Como você faz isso hoje?
   Quando foi a última vez?" gera verdade.
2. **Mostre o painel só DEPOIS de entender a rotina atual** (Fase 0) — senão você contamina tudo.
3. **Observe a pessoa usar.** Dê a tarefa e fique quieta. Fale menos, ouça mais. Não ensine, não defenda.
4. **Elogio não é validação.** Busque **compromisso de ação** (tempo, reputação, uma decisão real).

### ⛔ Perguntas que matam a entrevista (evite)
- "Você usaria / gostaria / acha que ajudaria?" → resposta de cortesia.
- Pedir opinião sobre o futuro em vez de comportamento passado.
- Explicar ou defender a ferramenta antes de ouvir a dor.
- Pergunta que já entrega a resposta ("não é ótimo que...?").

**Troque por:** *"como você faz isso hoje?"* · *"me conta da última vez que..."* ·
*"quanto isso te custou?"* · *"o que você fez a respeito?"*

---

## Como conduzir

- Sessão individual, ~40 min, uma pessoa por vez. Peça para **pensar em voz alta**.
- Comece pela **Renata** — ela é quem mata ou aprova a solução na prática.
- Registre: o que ela fez, onde hesitou, o que perguntou, e as **frases dela** (verbatim).

## Hipóteses que estamos testando

| # | Hipótese | Persona | Falhou se... |
|---|---|---|---|
| H1 | A fila é confiável no topo (baixo falso positivo) | Renata | acha caso óbvio de "não é fraude" no topo |
| H2 | Os motivos permitem justificar a inspeção | Renata | "não sei por que isso está aqui" |
| H3 | Sazonal/baixa renda bem tratados | Renata | aponta rural/safra como erro |
| H4 | Ela **trocaria a planilha** por isso | Renata | não se compromete a usar no próximo fechamento |
| H5 | O R$ é crível e o faz agir | Marcos | "é teórico" / não muda decisão de verba |
| H6 | Ele **levaria isso ao orçamento** | Marcos | só com R$ recuperado, não potencial |

---

## Sessão 1 — Renata (analista) · valida a OPERAÇÃO

### Fase 0 — Como é hoje *(NÃO mostre o painel ainda)*
- Me conta seu último fechamento: como você decidiu quais UCs olhar?
- Da última vez que mandou o campo e **não deu em nada** — o que tinha te feito mandar?
- Quanto do seu tempo vai nisso? Que planilha/sistema você usa hoje?
- Como você monta a **rota** de inspeção hoje?

### Fase 1 — Trabalhe como num dia normal *(mostre o painel, observe calada)*
- "Trabalhe esta fila como você faria num dia normal. Pensa em voz alta."
- Observe por onde começa, no que clica, onde hesita. **Não ensine.**

### Fase 2 — Casos reais
- "Escolha os 5 que você atacaria. Desses, quais você **abriria OS hoje**? Quais você **já viu parecido e não deu em nada**?"
- Abrir 1 UC e ler os motivos: "Se seu supervisor perguntasse **por que** você mandou inspecionar essa, o que você responderia? O que daqui você usaria?"
- Achar um caso rural/sazonal: "Esse deveria estar aqui? Por quê?"
- *(depois de ver o Mapa)* "O que disso mudaria como você monta a rota?"
- Caça ao falso positivo: "Tem algum aqui que você **já sabe** que não é fraude?"

### Fase 3 — Compromisso *(o teste de verdade)*
- "Você colocaria essas UCs na **fila de inspeção real desta semana**?"
- "Você **trocaria sua planilha** por isso no próximo fechamento? O que falta pra isso?"
- Hesitou? O entusiasmo era de fachada — **anote o porquê** (é o dado mais valioso).

**✅ bom sinal:** confia no topo · justifica com os motivos · se compromete a usar.
**🚩 alerta:** falso positivo óbvio no topo · "não entendi o critério" · não larga a planilha.

---

## Sessão 2 — Marcos (diretor) · valida o VALOR

### Fase 0 — Como é hoje *(sem mostrar o painel)*
- Da última vez, como você decidiu **onde alocar a equipe** / quanto investir em perdas?
- O que te fez **liberar ou segurar** essa verba?
- Que número você olha hoje pra saber se está perdendo receita? De onde ele vem?
- Como você presta conta de perdas ao conselho/assembleia hoje?

### Fase 1 — Mostre o Dashboard *(observe)*
- "Olha essa tela. O que ela te diz? O que você faria com isso?"
- Deixe ele clicar no R$ em risco e abrir a composição sozinho.

### Fase 2 — Reação
- "Quando você olha esse R$ em risco, o que você **pede antes de agir**?"
- "O que aqui te faria **confiar mais** — ou desconfiar?"

### Fase 3 — Compromisso
- "Você **levaria isso pra próxima reunião de orçamento**? O que precisaria estar aqui pra isso?"
- "Entre **R$ em risco** e **R$ recuperado** — qual você precisa ver pra aprovar?"

**✅ bom sinal:** conecta a uma decisão real de verba · se compromete a escalar.
**🚩 alerta:** "é teórico" · "cadê o que recuperei" · não leva adiante.

---

## O que capturar (use por participante)

```
Participante: ________   Papel real: ________   Cliente/base: ________
Bate com a persona [Marcos/Renata]? (sim / parcial / não) — o que diverge:

Como faz hoje (Fase 0) + quanto custa:
Top 3 momentos de confiança / Top 3 de dúvida:
Falsos positivos que ela apontou (UC + por quê):
COMPROMISSO obtido? (usaria semana que vem / levaria ao orçamento) — sim/não/condicional:
O que faltou para ela agir/decidir:
Frases dela (verbatim):
Decisão: serve pra ela? (sim / com ajustes / não) — quais ajustes:
```

## Critério de decisão (depois das duas sessões)

- **Avança** se: Renata se compromete a usar (não só elogia) e Marcos conecta a uma decisão real de verba.
- **Ajusta antes de avançar** se: falso positivo alto no topo, motivos pouco claros, ou ninguém se compromete — corrige e revalida.
- **Repensa** se: nenhum dos dois projeta uso/decisão real com a ferramenta.

## Próximos passos prováveis (pós-validação)

1. Calibrar limiares com o retorno (os falsos positivos da Renata viram regra).
2. Fechar o ciclo: abrir OS no E2 Comercial + registrar o resultado da inspeção.
3. Para o Marcos: medir **recuperação realizada** e ROI (não só potencial).
4. Quando houver casos confirmados, treinar o modelo supervisionado.
