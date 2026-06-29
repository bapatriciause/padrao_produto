---
name: use-inadimplencia-db
description: Conectar, consultar e usar o banco PostgreSQL de inadimplência (schema ml_inadimplencia) que o pipeline sql/ cria a partir dos CSVs ML_DATASET_FINAL. Use quando pedirem para consultar, conectar, rodar query/SQL no banco, abrir o psql, contar reavisos, olhar o balanço do target, ler a view de ML (vw_reaviso_ml), ou construir/reconstruir o banco a partir dos CSVs.
---

# Usar o banco de inadimplência (schema `ml_inadimplencia`)

O pipeline em `sql/` carrega os CSVs `ML_DATASET_FINAL_*.csv` num esquema
relacional normalizado dentro do PostgreSQL. Esta skill é sobre **consultar e
usar** esse banco depois de construído. (Para validar/profilar os CSVs crus,
veja a skill irmã `run-one-drive`.)

- **Banco:** `agente_cobranca` · **schema:** `ml_inadimplencia` · `postgres:17`
- **Onde roda:** container Docker `agente-cobranca-postgres` (`localhost:5432`,
  credenciais default `postgres`/`postgres`). **Não há `psql` no host** — tudo
  passa por `docker exec`.
- **Driver:** `.claude/skills/use-inadimplencia-db/db.sh` — um wrapper psql que
  sobe o container se preciso, posiciona o `search_path` em `ml_inadimplencia`
  (então você consulta as tabelas **sem o prefixo do schema**) e roda SQL.

Caminhos abaixo são relativos ao diretório `one-drive/`.

## Pré-requisitos

Só Docker. A imagem `postgres:17` e o container `agente-cobranca-postgres` já
existem nesta máquina (vêm de `../agente-cobranca/docker-compose.yml`).

```bash
docker --version                                   # Docker presente
docker start agente-cobranca-postgres              # sobe o container (idempotente)
docker exec agente-cobranca-postgres pg_isready -U postgres   # espera "accepting connections"
```

O `db.sh` já chama `docker start` sozinho se o container estiver parado — você
normalmente não precisa fazer isso à mão.

## Consultar o banco (caminho do agente) — o driver

`.claude/skills/use-inadimplencia-db/db.sh` aceita três formas:

```bash
cd one-drive

# 1) uma query como string (sem precisar prefixar o schema):
./.claude/skills/use-inadimplencia-db/db.sh "SELECT count(*) AS reavisos FROM reaviso;"

# 2) um arquivo .sql do host (transmitido via STDIN ao container):
./.claude/skills/use-inadimplencia-db/db.sh -f minha_consulta.sql

# 3) validação rápida (contagem + positivos por distribuidora):
./.claude/skills/use-inadimplencia-db/db.sh --check
```

`--check` deve imprimir (bate com `sql/README.md` e com a `run-one-drive`):

```
  sigla  | reavisos | positivos
---------+----------+-----------
 ALIANCA |   227926 |        37
 CERSUL  |    79236 |        15
 CETRIL  |   227152 |        85
 CHESP   |   275484 |       397
```

Toda saída começa com uma linha `SET` (é o `SET search_path TO ml_inadimplencia;`
que o driver injeta antes de cada query) — pode ignorar.

### Consultas úteis (verificadas)

```bash
DB=./.claude/skills/use-inadimplencia-db/db.sh

# Balanço do target — classe MUITO rara (~0,07% positivos):
$DB "SELECT target_pagou_antes_corte AS target, count(*),
       round(100.0*count(*)/sum(count(*)) over (),4) AS pct
     FROM vw_reaviso_ml GROUP BY 1 ORDER BY 1;"
#  target | count  |   pct
# --------+--------+---------
#       0 | 809264 | 99.9341
#       1 |    534 |  0.0659

# Vetor de treino pronto (sem campos LGPD): 51 colunas
$DB "SELECT count(*) FROM information_schema.columns
     WHERE table_schema='ml_inadimplencia' AND table_name='vw_reaviso_ml';"

# Linhas por tabela do schema:
$DB "SELECT 'reaviso',count(*) FROM reaviso
     UNION ALL SELECT 'uc',count(*) FROM uc
     UNION ALL SELECT 'reaviso_features',count(*) FROM reaviso_features;"
# reaviso=809798, uc=86935, reaviso_features=809798
```

## Modelo de dados (o que consultar)

```
distribuidora ─┐
               ├─< uc >── reaviso ──1:1── reaviso_features
classe_tarifaria┘         (fato core)     (features Grupos C/D/F)
municipio ─< localidade ──┘
```

| Objeto | O que é |
|---|---|
| `distribuidora` | 4 concessionárias (ALIANCA/CERSUL/CETRIL/CHESP) |
| `municipio`, `localidade` | lookups de geografia |
| `classe_tarifaria` | classe/subclasse + one-hots |
| `uc` | cadastro estático da Unidade Consumidora |
| `reaviso` | **fato core**: identificador + `target_pagou_antes_corte` + Grupo B |
| `reaviso_features` | features point-in-time (1:1 com `reaviso`) |
| `vw_reaviso_ml` | **view de treino** — join pronto, **sem campos LGPD** |

Para ML, use **`vw_reaviso_ml`** direto. Para análise/depuração, junte as tabelas
(as PKs/FKs já estão indexadas).

## Construir / reconstruir o banco (se o schema não existir)

Se `ml_inadimplencia` ainda não existe (ou você quer recarregar do zero), rode o
orquestrador. É idempotente (`DROP SCHEMA … CASCADE`) e leva ~2 min (~810k linhas):

```bash
cd one-drive
./sql/00_run_all.sh
```

Confirmar que o schema existe:

```bash
docker exec agente-cobranca-postgres psql -U postgres -d agente_cobranca -tAc \
  "SELECT count(*) FROM information_schema.tables WHERE table_schema='ml_inadimplencia';"
# -> 9  (7 tabelas normalizadas + a staging stg_ml_dataset + a view vw_reaviso_ml)
```

## Caminho humano (psql interativo)

```bash
./.claude/skills/use-inadimplencia-db/db.sh        # abre psql já no schema; \q para sair
```

Útil para explorar com `\dt`, `\d reaviso`, `\dv`. Para automação, prefira passar
a query como argumento (acima).

## Gotchas

- **Sem `psql` no host.** Toda conexão é `docker exec` no container
  `agente-cobranca-postgres`. O `db.sh` cuida disso; comandos `psql` soltos no
  host vão falhar com "command not found".
- **`-f` precisa transmitir via STDIN.** O psql roda **dentro** do container e
  não enxerga caminhos do host. O `db.sh -f` lê o arquivo no host e o injeta por
  STDIN (`-f -`). Um `psql -f /caminho/host.sql` direto daria "No such file".
- **Linha `SET` no topo de toda saída** — é o `search_path` que o driver injeta;
  é esperado, não é erro.
- **Nomes de geografia vêm parcialmente mascarados na origem** (ex.: `I*****`,
  `B******** R*****`). É característica do dado de origem, não do carregamento.
- **Chaves naturais colidem entre distribuidoras.** `numero_reaviso`/`iduc` só
  são únicos *dentro* de uma distribuidora — sempre filtre/junte por
  `id_distribuidora` junto. As PKs reais são surrogates `IDENTITY`.
- **Classe extremamente rara — ~0,07% de `target=1`** (534 em 809.798). Para
  modelar, use `class_weight`/resampling e métricas de classe rara (PR-AUC),
  **nunca acurácia**.
- **LGPD / segurança.** A instância está exposta em `0.0.0.0:5432` com credencial
  default. `iduc`, `numero_reaviso` e `data_emissao` são sensíveis (ficam nas
  tabelas, mas **excluídos** de `vw_reaviso_ml`). Para uso além de
  desenvolvimento local, valide com Segurança/Compliance.
- **O CSV CERSUL pode estar aberto** (arquivo `.~lock.…CERSUL.csv#`). Não atrapalha
  a leitura via STDIN no rebuild, mas feche-o antes de editar.

## Troubleshooting

| Sintoma | Causa / correção |
|---|---|
| `psql: command not found` | Esperado no host. Use `db.sh` (vai pelo container). |
| `could not connect` / `pg_isready` falha | Container parado: `docker start agente-cobranca-postgres` (o `db.sh` já tenta). |
| `relation "reaviso" does not exist` | Schema não construído. Rode `./sql/00_run_all.sh`. |
| `<arquivo.sql>: No such file or directory` | Não use `psql -f` direto; use `db.sh -f arquivo.sql` (transmite por STDIN). |
| `--check` divergente dos números acima | Carga incompleta/parcial. Reconstrua com `./sql/00_run_all.sh`. |
