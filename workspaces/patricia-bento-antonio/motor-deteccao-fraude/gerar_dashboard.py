# -*- coding: utf-8 -*-
"""
Gera UM dashboard HTML por cliente (segregação de dados) + index.html.
Tema padrão E2 ZeroPerdas (tokens da spec v1.2). Abas FUNCIONAIS:
Dashboard · Alertas & triagem · Distribuição geográfica · Parâmetros do modelo.
Persona: faturamento × financeiro. Valores são ESTIMATIVAS.
"""
import os, sys, glob, json
import pandas as pd
import motor_multicliente as M           # reusa os parâmetros reais do motor
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "saidas-real" if os.environ.get("FRAUDE_REAL") == "1" else "saidas")
PRIOS = ["CRÍTICA", "ALTA", "MÉDIA", "BAIXA"]

# Centro aproximado da região de cada cliente (apenas para o mapa ilustrativo —
# as posições por UC são sintéticas; coordenadas reais virão da BDGD).
CENTROS = {
    "coopera": [-28.68, -49.37],   # região de Criciúma (SC)
    "cersul":  [-28.47, -49.00],   # sul de Santa Catarina
    "alianca": [-27.05, -49.52],   # vale/norte de Santa Catarina
    "cetril":  [-21.76, -48.83],   # centro de São Paulo
    "chesp":   [-18.42, -50.45],   # sudoeste de Goiás
}


def ri(x):
    return None if pd.isna(x) else int(round(float(x)))


def montar_registros(df):
    recs = []
    for _, r in df.iterrows():
        recs.append({
            "uc": str(r["IDUC"]), "id": str(r["identificacao"])[:48],
            "cls": str(r.get("classe", "")), "pri": r["prioridade"],
            "va": ri(r["valor_estimado_ano"]), "vm": ri(r["valor_estimado_mes"]),
            "enf": ri(r["energia_nao_faturada_mes"]),
            "ca": ri(r["consumo_atual"]), "mh": ri(r["media_hist"]),
            "q": (None if pd.isna(r["queda_ratio"]) else int(r["queda_ratio"])),
            "qy": (None if pd.isna(r["queda_yoy"]) else int(r["queda_yoy"])),
            "br": int(r["baixa_renda"]), "sp": int(r["sazonal_prone"]),
            "ba": int(r.get("baseline_alto", 0)), "sc": ri(r["score_final"]),
            "mot": str(r["motivos"]),
        })
    return recs


def montar_agg(df):
    agg = {"total_va": float(df["valor_estimado_ano"].sum()), "total_uc": int(len(df)),
           "acao_imediata": int(df["prioridade"].isin(["CRÍTICA", "ALTA"]).sum()),
           "mwh_ano": float(df["energia_nao_faturada_mes"].sum() * 12 / 1000.0),
           "por_prioridade": {}}
    for p in PRIOS:
        sub = df[df["prioridade"] == p]
        agg["por_prioridade"][p] = {"c": int(len(sub)), "va": float(sub["valor_estimado_ano"].sum())}
    return agg


def param_html(premissa):
    regras = [
        ("Ligação clandestina", "UC desligada com consumo &gt; 0", M.PESO["CLANDESTINA"]),
        ("Consumo zerou tendo histórico", "ligada e lida, consumo = 0 com histórico", M.PESO["QUEDA_ZERO"]),
        ("Queda brusca", f"queda &ge; {M.LIM_QUEDA_BRUSCA*100:.0f}% (ano-a-ano em UC sazonal)", M.PESO["QUEDA_BRUSCA"]),
        ("Tarifa social — consumo muito alto", f"benefício social + média 12m &ge; {M.LIM_BR_MUITO_ALTO} kWh", M.PESO["BR_MUITO_ALTO"]),
        ("Troca de medidor + queda", f"troca de medidor + queda &ge; {M.LIM_TROCA_QUEDA*100:.0f}%", M.PESO["TROCA_QUEDA"]),
        ("Consumo abaixo do sistema", f"&lt; {M.LIM_PEER_BAIXO*100:.0f}% da média da classe + queda", M.PESO["PEER_BAIXO"]),
        ("Tarifa social — consumo alto", f"benefício social + média 12m {M.LIM_BR_ALTO}–{M.LIM_BR_MUITO_ALTO} kWh", M.PESO["BR_ALTO"]),
        ("Consumo zero persistente", "4 meses zerados (ligada e lida)", M.PESO["ZERO_PERSISTENTE"]),
        ("Queda moderada", f"queda {M.LIM_QUEDA_MODERADA*100:.0f}–{M.LIM_QUEDA_BRUSCA*100:.0f}%", M.PESO["QUEDA_MODERADA"]),
    ]
    regras.sort(key=lambda x: -x[2])
    linhas = "".join(f"<tr><td>{n}</td><td>{c}</td><td class='r'>{p}</td></tr>" for n, c, p in regras)
    tarifa = ("Coopera: tarifa premissa de R$ 0,95/kWh (formato sem valor faturado)."
              if premissa else "Tarifa efetiva derivada do valor faturado do próprio cliente (mediana R$/kWh).")
    return f"""
    <div class="method">Parâmetros refletem a configuração atual do motor de detecção. Cortes regulatórios
    (ex.: tarifa social) devem ser validados com a área de Regulação. Sem casos confirmados, os scores são
    indicadores de risco — calibrar com retorno de campo.</div>
    <div class="panel"><h2>Regras determinísticas e pesos</h2>
      <table class="bd"><tr><th>Regra</th><th>Condição</th><th class="r">Peso</th></tr>{linhas}</table>
      <div class="note">Uma UC pode disparar várias regras; os pesos somam (limitado a 100).</div>
    </div>
    <div class="panel"><h2>Score e priorização</h2>
      <table class="bd">
        <tr><th>Item</th><th>Valor</th></tr>
        <tr><td>Combinação do score</td><td>{M.W_REGRAS:.0%} regras + {M.W_ANOMALIA:.0%} anomalia (Isolation Forest)</td></tr>
        <tr><td>Faixas de prioridade</td><td>CRÍTICA (clandestina) · ALTA &ge; 70 · MÉDIA &ge; 40 · BAIXA &lt; 40</td></tr>
        <tr><td>UCs sazonais (rural/irrigação)</td><td>queda avaliada ano-a-ano (mesmo mês do ano anterior)</td></tr>
        <tr><td>Estimativa financeira</td><td>energia não faturada × tarifa × 12; gap winsorizado no P99</td></tr>
        <tr><td>Tarifa</td><td>{tarifa}</td></tr>
      </table>
    </div>"""


TEMPLATE = r"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>E2 ZeroPerdas · __CLIENTE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Roboto+Mono:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  :root{
    --bg:#eef1f6; --card:#ffffff; --card2:#f5f7fa; --ink:#1f2a37; --mut:#667085;
    --line:#e4e8ef; --accent:#1e88e5; --accent-d:#1669bb;
    --critica:#e53935; --alta:#fb8c00; --media:#f9a825; --baixa:#7d8aa6;
    --ia:#5b4bd6; --pos:#2e7d32;
    --crit-bg:#fdecec; --alta-bg:#fff3e3; --media-bg:#fef8e1; --baixa-bg:#eceff3;
    --grad:linear-gradient(90deg,#5026a6,#2b4fc4,#1f86d4,#2bb8e8);
    --mono:'Roboto Mono',ui-monospace,monospace;
  }
  *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--ink);
    font-family:'Roboto',system-ui,Arial,sans-serif;font-size:14px}
  [hidden]{display:none!important}
  header{background:var(--grad);color:#fff;padding:16px 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px}
  .brand{display:flex;align-items:center;gap:12px}
  .logo{width:38px;height:38px;border-radius:9px;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.4);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px}
  h1{font-size:17px;margin:0;font-weight:500} h1 .cli{font-weight:700}
  .sub{color:rgba(255,255,255,.85);font-size:12px;margin-top:2px}
  .badge{background:rgba(255,255,255,.15);color:#fff;padding:5px 11px;border-radius:6px;font-size:11px;border:1px solid rgba(255,255,255,.4)}
  .modbar{background:#fff;border-bottom:1px solid var(--line);padding:0 24px;display:flex;gap:4px;overflow-x:auto}
  .modbar span{padding:12px 14px;font-size:13px;color:var(--mut);white-space:nowrap;border-bottom:2px solid transparent;cursor:pointer}
  .modbar span:hover{color:var(--accent-d)}
  .modbar span.active{color:var(--accent-d);border-bottom-color:var(--accent);font-weight:500}
  .wrap{padding:20px 24px;max-width:1280px;margin:0 auto}
  .kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px}
  .kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;box-shadow:0 1px 2px rgba(16,24,40,.04)}
  .kpi .lbl{color:var(--mut);font-size:12px} .kpi .val{font-size:25px;font-weight:600;margin-top:6px;font-family:var(--mono)}
  .kpi .val.r{color:var(--accent-d)}
  .kpi.click{cursor:pointer;transition:border-color .12s} .kpi.click:hover{border-color:var(--accent)}
  .kpi .hint{color:var(--accent-d);font-size:11px;margin-top:8px}
  .panel{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin-bottom:20px;box-shadow:0 1px 2px rgba(16,24,40,.04)}
  .panel h2{font-size:12px;margin:0 0 12px;color:var(--mut);text-transform:uppercase;letter-spacing:.5px;font-weight:500}
  .bar{display:flex;align-items:center;gap:10px;margin:8px 0}
  .bar .nm{width:96px} .bar .nm .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
  .bar .track{flex:1;background:var(--card2);border-radius:5px;height:22px;overflow:hidden;border:1px solid var(--line)}
  .bar .fill{height:100%;border-radius:4px}
  .bar .vl{width:175px;text-align:right;color:var(--mut);font-family:var(--mono);font-size:13px}
  .filters{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px;align-items:center}
  select,input{background:#fff;color:var(--ink);border:1px solid var(--line);border-radius:7px;padding:8px 10px;font-size:13px;font-family:inherit}
  input:focus,select:focus{outline:none;border-color:var(--accent)}
  table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}
  th,td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--line);font-size:13px}
  th{color:var(--mut);font-weight:500;cursor:pointer;user-select:none;white-space:nowrap;background:var(--card2)}
  tbody tr:last-child td{border-bottom:none}
  td.r,th.r{text-align:right;font-family:var(--mono)} td.uc{font-family:var(--mono)}
  tbody tr{cursor:pointer} tbody tr:hover{background:#f0f6ff}
  .tag{padding:2px 9px;border-radius:12px;font-size:11px;font-weight:500;font-family:var(--mono)}
  .tag.CRÍTICA{background:var(--crit-bg);color:#c62828} .tag.ALTA{background:var(--alta-bg);color:#e65100}
  .tag.MÉDIA{background:var(--media-bg);color:#a07a00} .tag.BAIXA{background:var(--baixa-bg);color:#5b6675}
  .flag{font-size:10px;background:#fff3e3;color:#b45309;border:1px solid #fcd9a6;border-radius:4px;padding:1px 5px;margin-left:4px}
  .note{color:var(--mut);font-size:12px;margin:10px 2px}
  .ov{position:fixed;inset:0;background:rgba(16,24,40,.45);display:none;align-items:center;justify-content:center;padding:20px;z-index:10}
  .ov.on{display:flex} .mod{background:#fff;border-radius:12px;max-width:560px;width:100%;padding:22px;box-shadow:0 12px 40px rgba(16,24,40,.25)}
  .mod h3{margin:0 0 4px;font-weight:500} .mod .mut{color:var(--mut);font-size:12px;margin-bottom:14px}
  .kv{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px}
  .kv div{background:var(--card2);border:1px solid var(--line);border-radius:8px;padding:10px}
  .kv .k{color:var(--mut);font-size:11px} .kv .v{font-size:16px;font-weight:600;margin-top:3px;font-family:var(--mono)}
  .motbox{background:#f3f1fe;border-left:3px solid var(--ia);border-radius:0 8px 8px 0;padding:12px;font-size:13px;line-height:1.5;color:#36307a}
  .x{float:right;cursor:pointer;color:var(--mut);font-size:22px;line-height:1}
  .bd{width:100%;border-collapse:collapse;margin:4px 0 8px;border:1px solid var(--line);border-radius:8px;overflow:hidden}
  .bd td,.bd th{padding:7px 9px;border-bottom:1px solid var(--line);font-size:13px;text-align:left}
  .bd td.r,.bd th.r{text-align:right;font-family:var(--mono)} .bd th{color:var(--mut);font-weight:500;background:var(--card2)}
  .method{background:#f3f1fe;border-left:3px solid var(--ia);border-radius:0 8px 8px 0;padding:12px;font-size:12px;line-height:1.5;color:#46407e;margin:0 0 14px}
  .btn{background:var(--accent);color:#fff;border:none;border-radius:7px;padding:9px 14px;font-size:13px;font-weight:500;cursor:pointer}
  .btn:hover{background:var(--accent-d)}
  .seclbl{color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.5px;margin:6px 2px}
  .back{color:var(--accent-d);font-size:12px;text-decoration:none} .back:hover{text-decoration:underline}
  footer{padding:16px 24px;color:var(--mut);font-size:11px;border-top:1px solid var(--line);max-width:1280px;margin:0 auto;line-height:1.6}
  @media(max-width:900px){.kpis{grid-template-columns:repeat(2,1fr)}}
</style></head><body>
<header>
  <div class="brand"><div class="logo">E2</div>
    <div><h1>ZeroPerdas · <span class="cli">__CLIENTE__</span></h1>
    <div class="sub">Perdas não-técnicas · priorização por valor recuperável · competência __COMP__</div></div></div>
  <div class="badge">Valores estimados — não perda confirmada</div>
</header>
<nav class="modbar" id="tabs">
  <span data-t="dash" class="active">Dashboard</span>
  <span data-t="fila">Alertas &amp; triagem</span>
  <span data-t="mapa">Mapa</span>
  <span data-t="geo">Distribuição geográfica</span>
  <span data-t="param">Parâmetros do modelo</span>
</nav>
<div class="wrap">
  <a class="back" href="index.html">← todos os clientes</a>

  <section data-tab="dash" style="margin-top:12px">
    <div class="kpis">
      <div class="kpi click" onclick="openKpi('va')"><div class="lbl">R$ em risco / ano (estimado)</div><div class="val r" id="k_va"></div><div class="hint">ver composição ▸</div></div>
      <div class="kpi click" onclick="openKpi('uc')"><div class="lbl">UCs suspeitas</div><div class="val" id="k_uc"></div><div class="hint">ver composição ▸</div></div>
      <div class="kpi click" onclick="openKpi('im')"><div class="lbl">Ação imediata (crítica + alta)</div><div class="val" id="k_im"></div><div class="hint">ver na fila ▸</div></div>
      <div class="kpi click" onclick="openKpi('mwh')"><div class="lbl">Energia não faturada (MWh/ano)</div><div class="val" id="k_mwh"></div><div class="hint">ver composição ▸</div></div>
    </div>
    <div class="panel"><h2>R$/ano estimado por nível de risco</h2><div id="bars"></div>
      <div class="note">Clique numa barra para abrir a fila filtrada por aquele nível.</div></div>
    <div class="panel"><h2>R$/ano estimado por tipo de irregularidade</h2><div id="tipobars"></div></div>
  </section>

  <section data-tab="fila" hidden>
    <div class="filters">
      <select id="f_pri"><option value="">Todos os níveis</option>
        <option>CRÍTICA</option><option>ALTA</option><option>MÉDIA</option><option>BAIXA</option></select>
      <input id="f_q" placeholder="Buscar UC ou nome/bairro..." style="flex:1;min-width:180px">
      <span class="note" id="cnt"></span>
    </div>
    <table id="tb"><thead><tr>
      <th data-s="uc">UC</th><th>Identificação</th><th data-s="pri">Nível</th>
      <th class="r" data-s="va">R$/ano ▼</th><th class="r" data-s="vm">R$/mês</th>
      <th class="r" data-s="enf">kWh não fat./mês</th><th>Motivo</th>
    </tr></thead><tbody id="rows"></tbody></table>
    <div class="note" id="more"></div>
  </section>

  <section data-tab="mapa" hidden>
    <div class="method">Pré-visualização <b>ILUSTRATIVA</b> do mapa operacional. O <b>município é real</b>
      (via código IBGE), mas a <b>posição exata de cada UC é aproximada</b> — só para demonstrar a
      experiência. As coordenadas reais por UC virão da integração com a <b>BDGD</b> (base geográfica da ANEEL),
      como prevê o padrão E2 (base de mapa + camadas BDGD).</div>
    <div style="display:flex;gap:16px;flex-wrap:wrap;margin:6px 2px 10px;font-size:12px;color:var(--mut)">
      <span><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#e53935;margin-right:5px"></span>Crítica</span>
      <span><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#fb8c00;margin-right:5px"></span>Alta</span>
      <span><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#f9a825;margin-right:5px"></span>Média</span>
      <span><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#7d8aa6;margin-right:5px"></span>Baixa</span>
    </div>
    <div class="panel" style="padding:0;overflow:hidden"><div id="map" style="height:460px;width:100%"></div></div>
    <div class="note">Mostrando as <span id="mapn">—</span> UCs de maior valor recuperável. Clique num ponto para ver a UC.</div>
  </section>

  <section data-tab="geo" hidden>
    <div class="panel"><h2>R$/ano estimado por município (top 15)</h2><div id="geobars"></div>
      <div class="note">Agregação por município — não é mapa de coordenadas (a base não traz lat/long).
      Indica onde concentrar as equipes de inspeção.</div></div>
  </section>

  <section data-tab="param" hidden>__PARAM__</section>
</div>
<footer>
  Estimativa: energia não faturada = (consumo de referência − consumo atual) × tarifa efetiva.
  Referência = mesmo mês do ano anterior em UCs sazonais (rural/irrigação), média de 3 meses nas demais.
  Gap winsorizado no P99 para conter erros de leitura. __NOTA_TARIFA__
  Cortes regulatórios devem ser validados com a área de Regulação. Não é prova de fraude — base para inspeção.
  Padrão visual E2 (tokens da spec v1.2) — a validar contra o guia oficial do E2.
</footer>
<div class="ov" id="ov"><div class="mod" id="mod"></div></div>
<script>
const D = __DADOS__;
const PRIOS=["CRÍTICA","ALTA","MÉDIA","BAIXA"];
const fmtR = v => "R$ " + Math.round(v||0).toLocaleString("pt-BR");
const fmtN = v => (v==null?"–":Math.round(v).toLocaleString("pt-BR"));
const COR = {"CRÍTICA":"#e53935","ALTA":"#fb8c00","MÉDIA":"#f9a825","BAIXA":"#7d8aa6"};
const pct = (p,t) => t>0 ? Math.round(100*p/t)+"%" : "–";
function tipoDe(mot){const m=(mot||"").toLowerCase();
  if(m.includes("clandestina"))return"Ligação clandestina";
  if(m.includes("tarifa social"))return"Tarifa social com consumo alto";
  if(m.includes("zerou")||m.includes("zero persistente"))return"Consumo zerado";
  if(m.includes("troca de medidor"))return"Troca de medidor + queda";
  if(m.includes("queda de consumo"))return"Queda de consumo";
  if(m.includes("média do sistema"))return"Consumo abaixo do sistema";
  if(m.includes("anômalo"))return"Anomalia estatística";
  return"Outros";}

k_va.textContent=fmtR(D.agg.total_va); k_uc.textContent=D.agg.total_uc.toLocaleString("pt-BR");
k_im.textContent=D.agg.acao_imediata.toLocaleString("pt-BR"); k_mwh.textContent=Math.round(D.agg.mwh_ano).toLocaleString("pt-BR");

const maxva=Math.max(1,...Object.values(D.agg.por_prioridade).map(o=>o.va));
bars.innerHTML=PRIOS.map(p=>{const o=D.agg.por_prioridade[p];
  return `<div class="bar" style="cursor:pointer" onclick="filtrarPri('${p}')" title="Filtrar a fila por ${p}">
  <div class="nm"><span class="dot" style="background:${COR[p]}"></span>${p}</div>
  <div class="track"><div class="fill" style="width:${(o.va/maxva*100).toFixed(1)}%;background:${COR[p]}"></div></div>
  <div class="vl">${fmtR(o.va)} · ${o.c} UCs</div></div>`}).join("");

function brkTipo(rows){const o={};rows.forEach(r=>{const t=tipoDe(r.mot);(o[t]||(o[t]={c:0,va:0}));o[t].c++;o[t].va+=r.va||0;});return o;}
(function(){const bt=brkTipo(D.recs),ent=Object.entries(bt).sort((a,b)=>b[1].va-a[1].va);
  const mx=Math.max(1,...ent.map(e=>e[1].va));
  tipobars.innerHTML=ent.map(([t,o])=>`<div class="bar"><div class="nm" style="width:210px;font-size:13px">${t}</div>
    <div class="track"><div class="fill" style="width:${(o.va/mx*100).toFixed(1)}%;background:#5b4bd6"></div></div>
    <div class="vl">${fmtR(o.va)} · ${o.c} UCs</div></div>`).join("");})();

(function(){const o={};D.recs.forEach(r=>{const m=(r.id.split(" | ")[0]||"—").trim()||"—";(o[m]||(o[m]={va:0,c:0}));o[m].va+=r.va||0;o[m].c++;});
  const ent=Object.entries(o).sort((a,b)=>b[1].va-a[1].va).slice(0,15);const mx=Math.max(1,...ent.map(e=>e[1].va));
  geobars.innerHTML=ent.map(([m,v])=>`<div class="bar"><div class="nm" style="width:170px;font-size:13px">${m}</div>
    <div class="track"><div class="fill" style="width:${(v.va/mx*100).toFixed(1)}%;background:#1e88e5"></div></div>
    <div class="vl">${fmtR(v.va)} · ${v.c} UCs</div></div>`).join("");})();

let sortKey="va",sortDir=-1,quick=null,quickTipo=null;
function render(){
  const fp=f_pri.value,fq=f_q.value.toLowerCase().trim();
  let rows=D.recs.filter(r=>{
    const okPri = quick==="imediata" ? (r.pri==="CRÍTICA"||r.pri==="ALTA") : (!fp||r.pri===fp);
    const okTipo = !quickTipo || tipoDe(r.mot)===quickTipo;
    return okPri && okTipo && (!fq||r.uc.toLowerCase().includes(fq)||r.id.toLowerCase().includes(fq));});
  const ord={CRÍTICA:0,ALTA:1,MÉDIA:2,BAIXA:3};
  rows.sort((a,b)=>{let av=a[sortKey],bv=b[sortKey];if(sortKey==="pri"){av=ord[a.pri];bv=ord[b.pri];}
    if(typeof av==="string")return sortDir*av.localeCompare(bv);return sortDir*((av||0)-(bv||0));});
  let flt=[]; if(quick==="imediata")flt.push("ação imediata"); if(quickTipo)flt.push("tipo: "+quickTipo);
  cnt.innerHTML=`${rows.length.toLocaleString("pt-BR")} UCs · ${fmtR(rows.reduce((s,r)=>s+(r.va||0),0))}/ano nesta seleção`
    + (flt.length?` · filtro: ${flt.join(" + ")} <a href="#" onclick="limparFiltros();return false" style="color:var(--accent-d)">limpar</a>`:"");
  document.getElementById("rows").innerHTML=rows.slice(0,300).map(r=>`<tr data-i="${D.recs.indexOf(r)}">
    <td class="uc">${r.uc}</td><td>${r.id}${r.ba?'<span class="flag">baseline alto</span>':''}</td>
    <td><span class="tag ${r.pri}">${r.pri}</span></td>
    <td class="r">${fmtR(r.va)}</td><td class="r">${fmtR(r.vm)}</td><td class="r">${fmtN(r.enf)}</td><td>${r.mot}</td></tr>`).join("");
  more.textContent=rows.length>300?`Mostrando as 300 de maior valor (de ${rows.length.toLocaleString("pt-BR")}). Refine os filtros.`:"";
}
const CENTER=__CENTER__;
let _map=null;
function initMap(){
  if(typeof L==="undefined"){document.getElementById("mapn").textContent="(mapa requer internet)";return;}
  if(_map){_map.invalidateSize();return;}
  _map=L.map("map",{scrollWheelZoom:false}).setView([CENTER[0],CENTER[1]],10);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:18,attribution:"© OpenStreetMap"}).addTo(_map);
  const top=[...D.recs].sort((a,b)=>(b.va||0)-(a.va||0)).slice(0,400);
  const jit=s=>{const x=Math.sin(s*12.9898)*43758.5453;return (x-Math.floor(x))-0.5;};
  top.forEach((r,i)=>{const lat=CENTER[0]+jit(i*2+1)*0.30,lng=CENTER[1]+jit(i*2+2)*0.30;
    L.circleMarker([lat,lng],{radius:r.pri==="CRÍTICA"?7:r.pri==="ALTA"?6:5,color:COR[r.pri],fillColor:COR[r.pri],fillOpacity:.85,weight:1})
     .bindPopup(`<b>UC ${r.uc}</b> · ${r.pri}<br>${r.id}<br><b>${fmtR(r.va)}/ano</b><br><span style="color:#555">${r.mot}</span>`).addTo(_map);});
  document.getElementById("mapn").textContent=top.length.toLocaleString("pt-BR");
}
function showTab(t){document.querySelectorAll("#tabs span").forEach(s=>s.classList.toggle("active",s.dataset.t===t));
  document.querySelectorAll("section[data-tab]").forEach(s=>s.hidden=(s.dataset.tab!==t));
  if(t==="mapa")setTimeout(initMap,40);}
function filtrarPri(p){quick=null;quickTipo=null;ov.classList.remove("on");showTab("fila");f_pri.value=p;render();}
function filtrarTipo(t){quick=null;quickTipo=t;ov.classList.remove("on");showTab("fila");f_pri.value="";render();}
function verImediata(){quick="imediata";quickTipo=null;f_pri.value="";ov.classList.remove("on");showTab("fila");render();}
function limparFiltros(){quick=null;quickTipo=null;f_pri.value="";f_q.value="";render();}

function brkPri(rows){const o={};PRIOS.forEach(p=>o[p]={c:0,va:0,enf:0});
  rows.forEach(r=>{const x=o[r.pri];if(x){x.c++;x.va+=r.va||0;x.enf+=r.enf||0;}});return o;}
function tabPri(bp,total){return `<table class="bd"><tr><th>Nível</th><th class="r">UCs</th><th class="r">R$/ano</th><th class="r">%</th><th></th></tr>`+
  PRIOS.map(p=>`<tr style="cursor:pointer" onclick="filtrarPri('${p}')" title="Ver as UCs deste nível na fila"><td><span class="tag ${p}">${p}</span></td><td class="r">${bp[p].c.toLocaleString("pt-BR")}</td><td class="r">${fmtR(bp[p].va)}</td><td class="r">${pct(bp[p].va,total)}</td><td class="r" style="color:var(--accent-d)">ver ›</td></tr>`).join("")+`</table>`;}
function tabTipo(bt,total){const ent=Object.entries(bt).sort((a,b)=>b[1].va-a[1].va);
  return `<table class="bd"><tr><th>Tipo de irregularidade</th><th class="r">UCs</th><th class="r">R$/ano</th><th class="r">%</th><th></th></tr>`+
  ent.map(([t,o])=>`<tr style="cursor:pointer" onclick="filtrarTipo('${t.replace(/'/g,"\\'")}')" title="Ver as UCs deste tipo na fila"><td>${t}</td><td class="r">${o.c.toLocaleString("pt-BR")}</td><td class="r">${fmtR(o.va)}</td><td class="r">${pct(o.va,total)}</td><td class="r" style="color:var(--accent-d)">ver ›</td></tr>`).join("")+`</table>`;}
function openKpi(which){
  const all=D.recs, bp=brkPri(all), bt=brkTipo(all), tv=D.agg.total_va;
  let title,method,body;
  if(which==="va"){title="R$ em risco/ano — composição";
    method="Soma do R$/ano estimado das UCs suspeitas. Por UC: energia não faturada × tarifa efetiva × 12. Gap limitado ao P99 do cliente. Estimativa de priorização, não perda confirmada.";
    body=`<div class="seclbl">Por nível de risco</div>${tabPri(bp,tv)}<div class="seclbl">Por tipo de irregularidade</div>${tabTipo(bt,tv)}`;
  }else if(which==="uc"){title="UCs suspeitas — composição";
    method="UCs sinalizadas por ao menos uma regra de negócio ou por anomalia estatística (5% mais atípicas). Não entram UCs sem leitura nem desligadas sem consumo.";
    body=`<div class="seclbl">Por nível de risco</div>${tabPri(bp,tv)}<div class="seclbl">Por tipo de irregularidade</div>${tabTipo(bt,tv)}`;
  }else if(which==="im"){title="Ação imediata (crítica + alta)";const c=bp["CRÍTICA"],a=bp["ALTA"];
    method="UCs em nível CRÍTICO (ligação clandestina) ou ALTO (maior risco/valor) — recomendadas para inspeção imediata.";
    body=`<table class="bd"><tr><th>Nível</th><th class="r">UCs</th><th class="r">R$/ano</th></tr>
      <tr><td><span class="tag CRÍTICA">CRÍTICA</span></td><td class="r">${c.c}</td><td class="r">${fmtR(c.va)}</td></tr>
      <tr><td><span class="tag ALTA">ALTA</span></td><td class="r">${a.c}</td><td class="r">${fmtR(a.va)}</td></tr></table>
      <button class="btn" onclick="verImediata()">Ver essas UCs na fila ▸</button>`;
  }else{title="Energia não faturada (MWh/ano) — composição";
    method="Soma da energia não faturada estimada por UC (kWh/mês) × 12 ÷ 1000. Mesma base de cálculo do R$, antes da tarifa.";
    body=`<table class="bd"><tr><th>Nível</th><th class="r">UCs</th><th class="r">MWh/ano</th></tr>`+
      PRIOS.map(p=>`<tr><td><span class="tag ${p}">${p}</span></td><td class="r">${bp[p].c}</td><td class="r">${(bp[p].enf*12/1000).toLocaleString("pt-BR",{maximumFractionDigits:0})}</td></tr>`).join("")+`</table>`;}
  document.getElementById("mod").innerHTML=`<span class="x" onclick="ov.classList.remove('on')">×</span><h3>${title}</h3><div class="method">${method}</div>${body}`;
  ov.classList.add("on");
}
function openModal(r){document.getElementById("mod").innerHTML=`<span class="x" onclick="ov.classList.remove('on')">×</span>
  <h3>UC <span class="num">${r.uc}</span> <span class="tag ${r.pri}">${r.pri}</span></h3>
  <div class="mut">${r.id} · ${r.cls||"—"}</div>
  <div class="kv">
    <div><div class="k">R$/ano estimado</div><div class="v" style="color:var(--accent-d)">${fmtR(r.va)}</div></div>
    <div><div class="k">R$/mês estimado</div><div class="v">${fmtR(r.vm)}</div></div>
    <div><div class="k">Consumo atual</div><div class="v">${fmtN(r.ca)} kWh</div></div>
    <div><div class="k">Consumo de referência</div><div class="v">${fmtN(r.mh)} kWh</div></div>
    <div><div class="k">Queda vs média / ano ant.</div><div class="v">${r.q==null?"–":r.q+"%"} / ${r.qy==null?"–":r.qy+"%"}</div></div>
    <div><div class="k">Energia não faturada</div><div class="v">${fmtN(r.enf)} kWh/mês</div></div>
  </div>
  <div class="seclbl">Como o R$ desta UC é estimado</div>
  <div class="method">${fmtN(r.enf)} kWh/mês não faturados × tarifa efetiva × 12 = ${fmtR(r.va)}/ano. Referência: ${fmtN(r.mh)} kWh${r.sp?" (mesmo mês do ano anterior — UC sazonal)":" (média de 3 meses)"}.</div>
  <div class="seclbl">Motivos da sinalização (voz da IA)</div>
  <div class="motbox">${r.mot}${r.br?'<br>• Beneficiário de tarifa social':''}${r.sp?'<br>• UC com sazonalidade esperada (avaliada ano-a-ano)':''}${r.ba?'<br>• Baseline histórico muito alto — validar leitura/cadastro':''}</div>`;
  ov.classList.add("on");}

document.querySelectorAll("#tabs span").forEach(s=>s.onclick=()=>showTab(s.dataset.t));
document.querySelectorAll("th[data-s]").forEach(th=>th.onclick=()=>{const k=th.dataset.s;
  if(sortKey===k)sortDir*=-1;else{sortKey=k;sortDir=(k==="uc"||k==="pri")?1:-1;}
  document.querySelectorAll("th[data-s]").forEach(t=>t.textContent=t.textContent.replace(/ [▼▲]/,""));
  th.textContent+=sortDir<0?" ▼":" ▲";render();});
document.getElementById("rows").addEventListener("click",e=>{const tr=e.target.closest("tr");if(tr)openModal(D.recs[tr.dataset.i]);});
ov.addEventListener("click",e=>{if(e.target===ov)ov.classList.remove("on")});
f_pri.onchange=()=>{quick=null;quickTipo=null;render();};f_q.oninput=render;render();
</script></body></html>"""


def build_html(cliente, recs, agg, comp, premissa):
    nota = ("Tarifa da Coopera é premissa (R$ 0,95/kWh)." if premissa
            else "Tarifa efetiva derivada do valor faturado do próprio cliente.")
    dados = json.dumps({"recs": recs, "agg": agg}, ensure_ascii=False)
    centro = CENTROS.get(cliente.lower(), [-15.78, -47.93])   # fallback: Brasília
    return (TEMPLATE.replace("__CLIENTE__", cliente).replace("__COMP__", comp)
            .replace("__PARAM__", param_html(premissa))
            .replace("__CENTER__", json.dumps(centro))
            .replace("__NOTA_TARIFA__", nota).replace("__DADOS__", dados))


INDEX = """<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<title>E2 ZeroPerdas · Clientes</title>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Roboto+Mono:wght@600&display=swap" rel="stylesheet">
<style>
body{margin:0;background:#eef1f6;color:#1f2a37;font-family:'Roboto',system-ui,Arial}
header{background:linear-gradient(90deg,#5026a6,#2b4fc4,#1f86d4,#2bb8e8);color:#fff;padding:18px 32px;display:flex;align-items:center;gap:12px}
.logo{width:38px;height:38px;border-radius:9px;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.4);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px}
h1{font-size:18px;margin:0;font-weight:500}
.wrap{padding:28px 32px;max-width:1100px;margin:0 auto}
.sub{color:#667085;font-size:13px;margin-bottom:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.card{background:#fff;border:1px solid #e4e8ef;border-radius:12px;padding:20px;text-decoration:none;color:inherit;display:block;box-shadow:0 1px 2px rgba(16,24,40,.04)}
.card:hover{border-color:#1e88e5}
.cn{font-size:16px;font-weight:500;margin-bottom:8px}
.cv{font-size:22px;font-weight:700;color:#1669bb;font-family:'Roboto Mono',monospace} .cv span{font-size:12px;color:#667085;font-weight:400;font-family:'Roboto'}
.cm{color:#667085;font-size:12px;margin-top:6px}</style></head><body>
<header><div class="logo">E2</div><div><h1>ZeroPerdas — Painel por Cliente</h1></div></header>
<div class="wrap">
<div class="sub">Cada cliente acessa apenas o próprio painel (segregação de dados). Valores são estimativas de priorização.</div>
<div class="grid">__CARDS__</div></div></body></html>"""


def main():
    arquivos = sorted(glob.glob(os.path.join(SAIDA, "ranking_*.csv")))
    arquivos = [a for a in arquivos if "consolidado" not in os.path.basename(a)]
    cards = []
    for caminho in arquivos:
        df = pd.read_csv(caminho, sep=";", encoding="utf-8-sig")
        cliente = str(df["cliente"].iloc[0])
        comp = str(df["competencia"].iloc[0]) if "competencia" in df else "—"
        premissa = (cliente.lower() == "coopera")
        recs, agg = montar_registros(df), montar_agg(df)
        dest = os.path.join(SAIDA, f"dashboard_{cliente.lower()}.html")
        with open(dest, "w", encoding="utf-8") as f:
            f.write(build_html(cliente, recs, agg, comp, premissa))
        cards.append({"cli": cliente, "arq": os.path.basename(dest),
                      "va": agg["total_va"], "uc": agg["total_uc"], "im": agg["acao_imediata"]})
        print(f"  {cliente:<10} -> {os.path.basename(dest)}  (R$ {agg['total_va']:,.0f}/ano · {agg['total_uc']:,} UCs)")

    cards.sort(key=lambda c: -c["va"])
    linhas = "".join(
        f'<a class="card" href="{c["arq"]}"><div class="cn">{c["cli"]}</div>'
        f'<div class="cv">R$ {c["va"]:,.0f}<span> /ano estimado</span></div>'
        f'<div class="cm">{c["uc"]:,} UCs · {c["im"]} para ação imediata</div></a>'
        for c in cards).replace(",", ".")
    with open(os.path.join(SAIDA, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX.replace("__CARDS__", linhas))
    print(f"  index.html gerado com {len(cards)} clientes (tema E2, abas funcionais)")


if __name__ == "__main__":
    main()
