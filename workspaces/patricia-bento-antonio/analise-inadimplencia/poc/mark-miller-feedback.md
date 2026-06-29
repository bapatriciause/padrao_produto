# Mark Miller — Avaliação do Sinal de Receita

> Gate comercial do Day 2 (`prompts-v2/day-two/mark-miller-evaluator.md`).
> Proposta: **Assistente Inteligente de Seleção de Corte** (suíte inadimplência, Agentes 3+4).
> Status: Revisada · Stage: Revisão completa · Data: 2026-06-25.

## Operating Mode: WARTIME
Crescimento >10% com churn ~0 (retenção excelente, ativo real), mas abaixo da barra de
2x (~26%), sem ARR/ARPU conhecidos e com o modelo ainda não construído. Crescimento
saudável, abaixo da barra, relógio da IA correndo na camada de decisão.

## Veredito: **CONDITIONAL**
As duas seções decisivas passam do piso (3,0 cada); há tração real (Certel topou
co-desenvolver; Certaja com caso 1032894 aberto) e profundidade de domínio genuína.
**Capital retido** até responder as 5 perguntas abaixo. Foi a tração que deu o
CONDITIONAL — não a honestidade; as lacunas (número de receita, modelo, compromisso
de pagamento) seguram o resto.

## Notas
| Seção | Nota |
|---|---|
| Intimidade & Validação do Cliente (decisiva) | 3,0 |
| Profundidade da Transformação Agêntica (decisiva) | 3,0 |
| Receita & Share-of-Wallet | 2,0 |
| Proteção de Moat | 3,5 |
| Contexto de Negócio & Vulnerabilidade a IA | 3,0 |
| Eficiência de Capital | 1,5 |
| Urgência Competitiva | 4,0 |

## Onde quebra (resumo)
- **Sem número de receita:** não há ARR/ARPU nem ARR incremental ano 1/2 → tese de
  share-of-wallet não fecha.
- **Modelo não existe:** PoC é mock e o rótulo do dataset está quebrado (re-extração
  pendente) → a seção agêntica é promessa até o modelo rodar.
- **Sem compromisso de pagamento:** Certel/Coopera em testes; ninguém falou de dinheiro.
- **Sem disciplina de capital:** sem orçamento, kill criteria ou checkpoints.
- **Validação direcional:** a persona "Sérgio" foi construída, não entrevistada.

## Onde funciona
- Churn ~0 (moat subestimado); domínio profundo do fluxo de cobrança; **Certel co-dev** +
  **Certaja caso aberto** = pull real; agente assume trabalho hoje manual (Nível 2 c/ HITL);
  time com track record (entregou e vende software); "por que agora" forte (ANEEL medidores
  digitais + janela 90d).

## 5 perguntas para liberar o capital (gate)
1. Qual % do gasto da cooperativa com cobrança/corte/deslocamento você captura hoje, e quanto a iniciativa move?
2. O que falta pra **Certel** virar piloto **pago** (ou co-financiado), e em que prazo?
3. Re-extraído o dataset (rótulo via `CORTADO` + features), o modelo bate AUC ≥0,80 e quanto do trabalho do operador assume?
4. Menor experimento que prova/mata isso — orçamento, prazo e critério de kill?
5. Quanto R$/mês de corte indevido + deslocamento + dívida parada isso remove por cooperativa, e qual a sua fatia?

## Growth Story Test (responder e trazer de volta)
1. Isto prova que a Useall dobra em 3 anos ganhando mais do bolso dos ~70 clientes — ou é arredondamento? Mostrar a conta.
2. Um parágrafo pro board do CSI sobre o que a iniciativa prova sobre conhecer o cliente e crescer dentro dele na era da IA.
