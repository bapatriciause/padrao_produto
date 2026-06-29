# Persona: Técnico

**Cláudio — Analista de Sistemas | Implementador de plataformas de TI**

*A pessoa que faz a plataforma Useall funcionar operacionalmente*

---

## Entrevistas de Origem

**Confiança: Directional** (extraída de padrões em Deise/CERBRANORTE e Jonas/CERTEL)

- Deise (CERBRANORTE): Precisa de "digitalização do processo, maior eficiência operacional, rastreabilidade e transparência"
- Jonas (CERTEL): Precisa de "acompanhamento em tempo real, identificação de anomalias, dados confiáveis"

**O que os une:** Ambos pedem integrações complexas, dados em tempo real, confiabilidade total. Quem faz isso funcionar é o técnico — mas ainda não temos entrevista direta com ele.

---

## Seu Mundo

Cláudio é o analista de sistemas ou líder técnico que recebe o pedido de Deise ou Jonas ("preciso de reconhecimento facial integrado" ou "preciso de leitura em tempo real") e precisa:

**Enfrentar a realidade operacional:**
- Integrar reconhecimento facial com sistema legado de assembleias que funciona em mainframe dos anos 2000
- Garantir que dados de consumo chegam em tempo real quando os medidores falam uma linguagem, o sistema billing fala outra, e o CRM fala uma terceira
- Fazer tudo funcionar 24/7 — downtime é inaceitável. Quando cai, **Cláudio toma a ligação**, não o CEO
- Treinar 8 pessoas em operações (que têm medo de tecnologia) para usar a nova plataforma

**Navegar pressões externas:**
- Regulatória: ANEEL exige rastreabilidade total — "preciso de auditoria completa de cada ação"
- Concorrencial: Agregadoras entram em 2025, distribuidora precisa inovar ou morre — "não posso quebrar nada enquanto a gente se move"
- Técnica: Plataforma Useall é cloud, mas infraestrutura local é on-prem, routers de 15 anos, conexão de internet ruins — "não posso assumir cloud perfeita"
- Humana: Tim é pequeno (3–4 pessoas), ninguém fala inglês, suporte internacional é difícil, documentação é escassa

**Atender simultaneamente:**
- Pressão do negócio: "vai ficar pronto para a demo em 3 semanas?"
- Pressão regulatória: "temos auditoria externa, tudo precisa estar documentado"
- Pressão do dia-a-dia: "a leitura de consumo caiu — consumidores estão reclamando, vamos perder clientes"

---

## Motivações & Objetivos

1. **Fazer a coisa certa funcionar** — "Quando a integração entra em produção, não pode quebrar. Reputação dele é pessoal."
2. **Reduzir o caos** — "Hoje tudo é manual, em spreadsheet, com 5 pessoas fazendo workaround. Preciso de um sistema que funcione sozinho."
3. **Ficar relevante** — "Mercado está mudando, preciso dominar cloud/APIs/dados em tempo real ou viro obsoleto."
4. **Ser ouvido** — "Quero que entendam que a complexidade é real. Não é só clicar e pronto."

---

## Pontos de Dor & Frustrações

### Integração & Complexidade

- **Dados fragmentados**: Consumo vem de smartmeters via MQTT, billing fala JSON, CRM espera XML. Cláudio precisa traduzir tudo. "Cada integração é um projeto do zero, documentação do vendor é ruim ou paga."
- **Latência e acurácia**: Jonas quer "tempo real", mas "tempo real" para um é 5 segundos, para outro é 5 minutos. "A gente nunca sabe qual é a expectativa real até que quebra em produção."
- **Dados sujos**: Medidores enviam lixo. "50% do tempo que passo é limpando dado, não implementando feature."

### Operação & Uptime

- **Sem redundância**: "Temos um servidor, uma conexão. Quando cai, cai tudo. Não tenho orçamento para cluster."
- **Monitoria cega**: "Não vejo o que está acontecendo de verdade. Sistema fala OK, mas consumidor reclama que leitura está errada."
- **Suporte 24/7 informal**: "Quando quebraba noite, ligam pra mim em casa. Não há escala."

### Mudança & Comunicação

- **Expectativas fluidas**: "Deise pede recurso X em janeiro, em junho muda de ideia, eu já implementei, é late demais."
- **Treinamento é meu trabalho**: "Ninguém na operação entende o sistema. Preciso estar lá todo dia explicando."
- **Feedback vem tarde**: "Só descubro que algo está errado quando o cliente reclama, não durante a implementação."

### Vendor & Produto

- **Documentação ruim**: "Docs do Useall são genéricas. Não fala de cooperativa pequena, de integração com mainframe, de banda ruim."
- **Falta de suporte localizado**: "Empresa em SP é rápida, mas não entendem realidade do interior. Não falam português direto comigo."
- **Roadmap desalinhado**: "Peço recurso de auditoria em janeiro, só chega em dezembro. Nesse meio tempo, ANEEL audita e me queima."

---

## Estratégias & Workarounds

Hoje, Cláudio enfrenta a lacuna entre o ideal (plataforma integrada, tempo real, auditada) e o real com:

- **Planilhas & Scripts**: Constrói jobs em Python que puxam dados, limpam, empurram pro lugar certo. "Não é bonito, mas funciona."
- **Documentação paralela**: Cria seu próprio wiki porque documentação oficial não serve. "Gasto 2 dias documentando o que deveria vir documentado."
- **Treinamento ad-hoc**: Senta com equipe de operações toda semana, na unha, mostrando. "Falta um módulo de onboarding pensado para não-técnico."
- **Monitoramento DIY**: Faz script que manda email se consumo não chegar em 5 min. "O sistema não me avisa, então monitoro eu mesmo."
- **Buffer de tempo**: Promete entrega em 6 semanas pro que leva 3, porque sabe que problemas inesperados vão aparecer. "Sempre aparecem."

---

## Empathy Map

| **Diz** | **Pensa** |
|---|---|
| "A complexidade da integração é real — não é falta de skill, é que cada sistema fala linguagem diferente" | *"Ninguém entende o que eu faço. Quando tudo funciona, é invisível. Quando quebra, sou inimigo."* |
| "Preciso de documentação que fale de meu caso — pequena distribuidora, infraestrutura ruim" | *"Vão pensar que sou lerdo se peço ajuda. Melhor resolver sozinho mesmo que leve 3x mais tempo."* |
| "Dados em tempo real é legal, mas 99.9% uptime é não-negociável" | *"Product quer features. Eu só quero que o que existe NÃO QUEBRE."* |
| "Treinei a galera, mas ninguém retém. Preciso de interface que não exija tanto treinamento" | *"Culpam a gente por tudo. Ninguém vê o quanto a gente faz preventivamente."* |

| **Sente** | **Faz** |
|---|---|
| **Pressão constante** — "Vai quebrar algo que eu não vi?" | Corre scripts de teste locais toda madrugada, antes de deploy |
| **Invisibilidade** — "Ninguém vê o que funciona, só o que quebra" | Envia relatórios mensais pra liderança ("Sistema up 99.8% este mês") |
| **Frustração com ambiguidade** — "O que é 'tempo real' exatamente?" | Pede esclarecimento por email (fica documentado), depois implementa |
| **Culpa e stress** — "Se quebrar, é meu problema" | Monitora 24/7, mesmo quando offline |
| **Isolamento técnico** — "Ninguém aqui entende arquitetura" | Estuda online à noite (Udemy, YouTube), quer entender melhor |

---

## Como Toma Decisões

**Quem influencia Cláudio:**

- **Sua observação empírica**: "Essa integração quebrou 3x em produção — não confio."
- **Aval de comunidade**: "Fórum de DevOps tem 200 pessoas dizendo que API Y não é confiável."
- **Confiança do vendor**: "Docs são claras? Respondem email? Usam próprio produto?"
- **Risco minimizado**: "Vou com opção que tem mais failsafe, mesmo que seja mais complexo."

**O que o faz resistir:**

- Mudança que não tem rollback claro — "Se der ruim, não consigo voltar atrás."
- Tecnologia nova sem comunidade — "Ninguém mais usa, se quebrar estou sozinho."
- Orçamento ou tempo apertado — "Não dá pra fazer certo agora, vai virar dívida técnica que pago depois."

---

## Como Ele Experimenta a Plataforma Useall

### Onde encaixa (idealmente):

- **Setup inicial**: Conecta API de medição, configura pipeline de consumo, integra CRM
- **Operação diária**: Monitora dados entrando, escalona problemas, treina ops
- **Evolução**: Adiciona novo módulo, expande integração, responde a mudanças regulatórias

### Onde dói:

- **Onboarding**: Docs são genéricas, não falam de sua realidade (pequena, mainframe, banda ruim)
- **Dados de qualidade**: Sistema assume dados bons — ele gasta 50% do tempo limpando
- **Monitoria**: Sem dashboard clara de "saúde" do sistema, descobre problemas tarde
- **Suporte**: Tempo de resposta longo, suporte não fala português, solutions são genéricas

### O que gostaria que fosse diferente:

- "Documentação com casos de uso reais — cooperativa, distribuidora pequena, setup on-prem misto"
- "Dashboard de integridade — verde/amarelo/vermelho — sem ter que abrir 5 abas"
- "Validação de dados integrada — alertar quando chegam dados sujos, não deixar passar"
- "Onboarding passo a passo pra equipe de operações — interface simples, não precisa de técnico"
- "Roadmap transparente — saber quando auditoria, quando failover, quando escalabilidade chegam"

---

## Pressões Externas

### Regulatória (ANEEL, Vigilância)

- "Auditoria externa em 6 meses. Preciso de rastreabilidade completa — quem alterou o quê, quando, por quê."
- "Compliance exige dados imutáveis. Sistema precisa gravar tudo."

### Mercado (Mercado Livre 2025, Agregadoras)

- "Mercado livre chega em 2025. Consumidor vai poder sair. Preciso de plataforma que engaje, que mostre valor."
- "Concorrente agregador já tem app. Nossa distribuidora precisa inovar ou perde cliente."

### Econômica (Orçamento Limitado)

- "Orçamento é apertado. Não posso ter downtime (custa dinheiro), mas também não posso gastar muito em redundância."

### Infraestrutura (Realidade Local)

- "Data center é on-prem, conexão internet é fraca, latência é alta. Não posso assumir cloud perfeita."

---

## Citações-Chave

> "Cada integração é um projeto do zero. Documentação do vendor é ruim ou paga."

> "A gente nunca sabe qual é a expectativa real até que quebra em produção."

> "50% do tempo que passo é limpando dado, não implementando feature."

> "Quando tudo funciona, é invisível. Quando quebra, sou inimigo."

> "Preciso de interface que não exija tanto treinamento — a galera não retém."

> "Ninguém entende a complexidade. Não é falta de skill, é que cada sistema fala linguagem diferente."

---

## Estilo de Comunicação

### Como Pede Ajuda

- Por email (quer documentação)
- Direto: "Tá muito genérico, preciso de exemplo concreto"
- Defensivo: "Tentei do jeito que vocês disseram, não funcionou"

### Como Expressa Frustração

- Silencioso a princípio ("OK, vou resolver sozinho")
- Depois, desabafos pontuais: "Aqui na realidade, as coisas não funcionam como nos docs"
- Reclamação estruturada: Escreve tudo pra mostrar que pensou

### Como Recusa Ideias

- "Legal em teoria, mas em produção não funciona"
- "Não tenho time pra manter"
- "Já tentei, não escalou"

### Como Quer Ser Ouvido

- Exemplos concretos, não abstrações
- Dados (uptime, % de falhas, tempo gasto em cleanup)
- Reconhecimento de que o problema é real e não é falta dele

---

## Resumo

Cláudio é invisível quando tudo funciona e culpado quando quebra. Navega integração complexa, dados sujos, infraestrutura velha, pressão regulatória, equipes pequenas sem expertise, e vendor distante. Quer plataforma que:

1. **Assuma dados ruins** — valide, limpe, alerte
2. **Seja observável** — mostre saúde em tempo real
3. **Fale sua língua** — docs em português, exemplos de pequena distribuidora
4. **Respeite uptime** — redundância, failover, monitoramento integrado
5. **Não exija treinamento profundo** — interface pensada pra não-técnico

Cláudio é o cliente que garante que o que Deise e Jonas pedem realmente **funciona**.
