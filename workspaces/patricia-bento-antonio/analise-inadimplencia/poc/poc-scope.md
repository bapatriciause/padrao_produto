# PoC Lock — Assistente Inteligente de Seleção de Corte

> Lock no estilo Day 2 (H-poc-build-for-handoff). Protótipo descartável para a
> equipe reagir — não é o produto final.

## Scope (uma frase)
Na tela de **geração de ordem de corte** do E2 Comercial, um agente de IA pré-marca
cada UC como **Incluir / Excluir / Revisar**, atribui **Prioridade (0–1000)** e
exibe uma **justificativa de 1 linha**; o operador **confirma ou sobrescreve** antes
de gerar o lote (human-in-the-loop).

## A única coisa que o PoC precisa provar
Que a IA consegue **triar o lote de corte de forma explicável, auditável e com
humano no comando**, reduzindo **corte indevido** e priorizando por recuperação ×
custo — e que isso cabe **dentro da tela que já existe** (campos `Marcado`,
`Prioridade` do `ReavisoOrdemDeCorteDTO`).

## Movimento agêntico (não é dashboard)
Sinal (lote gerado) → o agente **raciocina** sobre cada UC (flags de risco, débito,
prob. de pagamento, custo de execução) → **recomenda** marca + prioridade →
**mostra o porquê** → **espera aprovação humana** → registra a decisão (auditoria).

## O que fica de fora (deliberadamente)
- Modelo treinado de verdade (o score é **mockado**; vem do modelo pós-reaviso
  quando o rótulo for corrigido — ver `../README.md`).
- Integração real com o E2 Comercial / Oracle / MDM.
- Roteirização de equipes, parcelamento, religação (são outros agentes dos 11).

## Commercial check (do material existente — validar)
- **Quem paga:** distribuidora / cooperativa (supervisor de Cobrança é o usuário;
  diretoria comercial é o budget owner). Caso real: **Certaja, caso 1032894 —
  priorização de ordens de corte**.
- **O que substitui:** triagem manual de flags coloridas, inconsistente entre
  operadores; e o custo de **corte indevido** (R$ 5–15 mil/evento + multa ANEEL;
  ~740 ações/dia no setor).
- **Tamanho do valor:** evitar cortes de baixo ROI e indevidos + acelerar os de
  alto valor. (Ordem de grandeza do setor: ABRADEE ~R$ 6 bi/ano não arrecadados.)

## Responsible AI (guardrails visíveis no protótipo)
Serviço essencial, restrição de corte, baixa renda e micro-geração → o agente
**recomenda excluir/revisar**, nunca corta sozinho; toda decisão final é humana e
fica registrada. Validar limiares com **Regulatório/Jurídico** (Res. ANEEL
479/2012 e 1000/2021) antes de qualquer uso real.

## Maior pergunta em aberto
O rótulo do modelo pós-reaviso (e várias features comportamentais) precisa ser
re-extraído a partir de `REAVISO_CORTES.CORTADO`. Até lá, o score é ilustrativo.

## Narrativa de valor (talking points — por que gerir o corte com IA)
- **Medidor convencional = deslocamento.** A maioria das cooperativas ainda usa
  medidor convencional; cada corte exige equipe em campo (R$ 80–200/visita).
  Cortar à toa, ou cortar dívida pequena, **não se paga** → priorização importa.
- **Janela de 90 dias.** Passado o prazo regulatório, a cooperativa **não pode mais
  suspender** aquela dívida → urgência: priorizar antes da janela fechar; após,
  excluir do corte e mandar para cobrança/acordo. (Validar prazo com Regulatório.)
- **Custo de caixa.** Quanto mais tarde o cliente paga, mais tempo a cooperativa
  fica **sem o dinheiro em caixa** — atraso prolongado é custo financeiro.
- **Medidores digitais (programa ANEEL).** Com a digitalização da medição, o corte
  vira **remoto e barato**; o ganho de uma boa priorização **escala** — e o agente
  fica ainda mais relevante.
- **Conclusão:** faz sentido **um agente que monitore prazo, tipo de medidor e
  valor, e conduza o corte** na hora certa, no caso certo.

## Stress-test — persona "Sérgio" (operador de cobrança), DIRECIONAL
Ver `../personas/persona-operador-cobranca.md`. Reação ao PoC (role-play):

- **Usaria? 8/10** — "pra parar de decidir no olho e ter onde me segurar quando
  questionam". Vira 10 com: dizer **quem tentar SMS antes de cortar** e **agrupar por rota**.
- **Gostou:** justificativa + "por quê?" (auditoria); protegidos auto-excluídos com
  confirmação humana; KPI deslocamentos evitados + lógica de medidor.
- **Objeções → mudanças propostas:**
  1. "Cortar é o último passo — e o SMS/ligação antes?" → agente recomenda a
     **próxima melhor ação** (cobrar/SMS/acordo antes do corte p/ quem tem alta
     prob. de pagar), não só Incluir/Excluir/Revisar.
  2. "Cadê a rota? 10 UCs de R$40 na mesma rua compensa, uma a uma não." →
     mostrar **rota**, **agrupar/ordenar por rota** e sinalizar **cluster**
     (deslocamento compartilhado muda o ROI).
  3. "Quero fechar o lote rápido." → **filtro 'janela fechando ≤7d'**, ordenar por
     prioridade, **marcar em lote**.
  4. "De onde vem o % de pagamento?" → explicitar a origem do score (no real,
     "baseado em N reavisos do histórico").
- **Quote pra guardar:** *"Mando equipe na rua e o cara já tinha pagado ontem."*

## Arquivo
`poc-selecao-corte.html` — abrir no navegador (duplo clique). Autocontido, sem
backend, dados fictícios.
