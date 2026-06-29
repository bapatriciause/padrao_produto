#!/usr/bin/env bash
# ============================================================================
# db.sh — Driver de consulta ao banco de inadimplência (schema ml_inadimplencia)
#
# Abre uma conexão psql ao Postgres que o pipeline sql/ alimenta e roda SQL.
# Detecta o cliente igual ao 00_run_all.sh: usa `psql` do host se existir,
# senão usa o psql DENTRO do container Docker. Garante que o container esteja
# de pé. O search_path já vem em ml_inadimplencia, então as tabelas/views podem
# ser referenciadas sem o prefixo do schema.
#
# Uso:
#   ./db.sh "SELECT count(*) FROM reaviso;"      # roda uma query
#   ./db.sh -f consulta.sql                      # roda um arquivo .sql
#   ./db.sh                                      # abre psql interativo
#   ./db.sh --check                              # validação rápida (contagens)
#
# Variáveis (mesmos defaults do pipeline):
#   PGUSER=postgres PGPASSWORD=postgres PGDATABASE=agente_cobranca
#   PGHOST=localhost PGPORT=5432 CONTAINER=agente-cobranca-postgres SCHEMA=ml_inadimplencia
# ============================================================================
set -euo pipefail

PGHOST="${PGHOST:-localhost}"; PGPORT="${PGPORT:-5432}"
PGUSER="${PGUSER:-postgres}"; export PGPASSWORD="${PGPASSWORD:-postgres}"
PGDATABASE="${PGDATABASE:-agente_cobranca}"
CONTAINER="${CONTAINER:-agente-cobranca-postgres}"
SCHEMA="${SCHEMA:-ml_inadimplencia}"

# search_path já posicionado no schema do dataset
OPT=(-v ON_ERROR_STOP=1 -P "pager=off")
SETPATH="SET search_path TO ${SCHEMA};"

ensure_up() {  # garante o container de pé (só no modo docker)
  if ! docker exec "$CONTAINER" pg_isready -U "$PGUSER" >/dev/null 2>&1; then
    echo ">> subindo container $CONTAINER..." >&2
    docker start "$CONTAINER" >/dev/null
    for _ in $(seq 1 15); do
      docker exec "$CONTAINER" pg_isready -U "$PGUSER" >/dev/null 2>&1 && break
      sleep 1
    done
  fi
}

# run_sql: recebe SQL pela STDIN, prefixa o search_path e executa (host OU container)
run_sql() {
  if command -v psql >/dev/null 2>&1; then
    { printf '%s\n' "$SETPATH"; cat; } \
      | psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" "${OPT[@]}" -f -
  else
    ensure_up
    { printf '%s\n' "$SETPATH"; cat; } \
      | docker exec -i "$CONTAINER" psql -U "$PGUSER" -d "$PGDATABASE" "${OPT[@]}" -f -
  fi
}

CHECK_SQL="SELECT d.sigla,
                  count(*)                        AS reavisos,
                  sum(r.target_pagou_antes_corte) AS positivos
           FROM reaviso r JOIN distribuidora d USING (id_distribuidora)
           GROUP BY d.sigla ORDER BY d.sigla;"

case "${1:-}" in
  --check)  printf '%s\n' "$CHECK_SQL"        | run_sql ;;
  -f)       shift; cat "$1"                   | run_sql ;;   # arquivo .sql do host
  "")       # psql interativo (só faz sentido com TTY)
            if command -v psql >/dev/null 2>&1; then
              psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" "${OPT[@]}" -c "$SETPATH" -
            else
              ensure_up
              docker exec -it "$CONTAINER" psql -U "$PGUSER" -d "$PGDATABASE" "${OPT[@]}" -c "$SETPATH"
            fi ;;
  *)        printf '%s\n' "$1"                | run_sql ;;   # primeiro arg = string SQL
esac
