"""
Demo Simulado — Agente Conversacional de Cadastro
Useall Software · Task as a Service

Roda sem API key. Simula o fluxo completo:
  1. "OCR" do documento (dados pré-definidos como se Claude tivesse extraído)
  2. Conversa com o operador para preencher campos faltantes
  3. Chamada à API de cadastro (mock) com retorno de ID da UC

Uso:
  python demo-cadastro-simulado.py
"""

import json
import time
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Paleta de cores ANSI para o terminal
# ---------------------------------------------------------------------------
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
GRAY   = "\033[90m"
WHITE  = "\033[97m"
RED    = "\033[91m"


def agente(texto: str):
    """Imprime mensagem do agente com efeito de digitação."""
    print(f"\n{CYAN}{BOLD}AGENTE:{RESET} ", end="", flush=True)
    for char in texto:
        print(char, end="", flush=True)
        time.sleep(0.012)
    print()


def sistema(texto: str):
    """Imprime mensagem do sistema."""
    print(f"\n{GRAY}[Sistema] {texto}{RESET}")


def separador():
    print(f"\n{GRAY}{'─' * 60}{RESET}")


def operador_input(prompt: str = "") -> str:
    """Lê entrada do operador."""
    print(f"\n{YELLOW}{BOLD}OPERADOR:{RESET} ", end="", flush=True)
    return input().strip()


def simular_ocr():
    """Simula extração de dados via Claude Vision."""
    sistema("Analisando documento... enviando imagem ao Claude Vision...")
    time.sleep(1.5)
    sistema("Processando campos extraídos...")
    time.sleep(1.0)

    # Dados extraídos como se Claude tivesse lido uma CNH
    dados = {
        "nome_completo": "MARIA APARECIDA SOUSA",
        "cpf": "082.456.731-09",
        "rg": "12.345.678-9",
        "data_nascimento": "14/03/1985",
        "endereco": "",        # não constava no documento
        "bairro": "",
        "cidade": "",
        "estado": "",
        "cep": "",
        "classe_tarifaria": "",
        "tipo_ligacao": "",
    }
    return dados


def campos_faltantes(dados: dict) -> list[str]:
    obrigatorios = {
        "endereco": "endereço (logradouro e número)",
        "bairro": "bairro",
        "cidade": "cidade",
        "estado": "estado (UF)",
        "cep": "CEP",
        "classe_tarifaria": "classe tarifária",
        "tipo_ligacao": "tipo de ligação",
    }
    return [(k, v) for k, v in obrigatorios.items() if not dados.get(k)]


def chamar_api_mock(dados: dict) -> dict:
    sistema("Chamando API de cadastro...")
    time.sleep(1.2)
    uc_id = f"UC-{datetime.now().strftime('%Y')}-{abs(hash(dados.get('cpf', ''))) % 90000 + 10000:05d}"
    return {"sucesso": True, "uc_id": uc_id}


# ---------------------------------------------------------------------------
# Fluxo principal da demo
# ---------------------------------------------------------------------------

def main():
    print(f"\n{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}  AGENTE CADASTRO CONVERSACIONAL — Useall Software{RESET}")
    print(f"{BOLD}  Task as a Service · Demo Simulado{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}")
    print(f"\n{GRAY}Pressione ENTER para iniciar a simulação...{RESET}")
    input()

    # -----------------------------------------------------------------------
    # Etapa 1 — Análise do documento
    # -----------------------------------------------------------------------
    separador()
    sistema("Operador enviou foto da CNH do consumidor.")
    dados = simular_ocr()

    agente(
        "Analisei a CNH enviada. Encontrei os seguintes dados:\n\n"
        f"  Nome:          {dados['nome_completo']}\n"
        f"  CPF:           {dados['cpf']}\n"
        f"  RG:            {dados['rg']}\n"
        f"  Nascimento:    {dados['data_nascimento']}\n\n"
        "Esses dados estão corretos?"
    )

    resposta = operador_input()

    if resposta.lower() in ("não", "nao", "n", "errado"):
        agente("Tudo bem, pode me informar a correção.")
        operador_input()
        agente("Anotado. Vou usar os dados corrigidos.")
    else:
        agente("Ótimo! Vou prosseguir com esses dados.")

    # -----------------------------------------------------------------------
    # Etapa 2 — Campos faltantes: endereço
    # -----------------------------------------------------------------------
    separador()
    agente(
        "O documento não contém o endereço da unidade consumidora. "
        "Qual o endereço completo? (logradouro e número)"
    )
    dados["endereco"] = operador_input() or "Rua das Flores, 142"

    agente("E o bairro?")
    dados["bairro"] = operador_input() or "Jardim América"

    agente("Cidade e estado (UF)?")
    resp = operador_input() or "Porto Alegre / RS"
    # tenta separar cidade/estado
    partes = [p.strip() for p in resp.replace("-", "/").split("/")]
    dados["cidade"] = partes[0] if partes else resp
    dados["estado"] = partes[1].upper()[:2] if len(partes) > 1 else "RS"

    agente("CEP?")
    dados["cep"] = operador_input() or "90110-000"

    # -----------------------------------------------------------------------
    # Etapa 3 — Classe tarifária
    # -----------------------------------------------------------------------
    separador()
    agente(
        "Qual a classe tarifária desta unidade consumidora?\n\n"
        "  1 - Residencial\n"
        "  2 - Comercial\n"
        "  3 - Industrial\n"
        "  4 - Rural\n"
        "  5 - Poder Público"
    )
    opcao = operador_input()
    mapa = {"1": "Residencial", "2": "Comercial", "3": "Industrial", "4": "Rural", "5": "Poder Público"}
    dados["classe_tarifaria"] = mapa.get(opcao, opcao or "Residencial")

    # -----------------------------------------------------------------------
    # Etapa 4 — Tipo de ligação
    # -----------------------------------------------------------------------
    separador()
    agente(
        "Qual o tipo de ligação?\n\n"
        "  1 - Monofásico\n"
        "  2 - Bifásico\n"
        "  3 - Trifásico"
    )
    opcao = operador_input()
    mapa2 = {"1": "Monofásico", "2": "Bifásico", "3": "Trifásico"}
    dados["tipo_ligacao"] = mapa2.get(opcao, opcao or "Monofásico")

    # -----------------------------------------------------------------------
    # Etapa 5 — Resumo e confirmação
    # -----------------------------------------------------------------------
    separador()
    agente(
        f"Perfeito! Aqui está o resumo antes de salvar:\n\n"
        f"  Nome:              {dados['nome_completo']}\n"
        f"  CPF:               {dados['cpf']}\n"
        f"  RG:                {dados['rg']}\n"
        f"  Nascimento:        {dados['data_nascimento']}\n"
        f"  Endereço:          {dados['endereco']}\n"
        f"  Bairro:            {dados['bairro']}\n"
        f"  Cidade/UF:         {dados['cidade']} - {dados['estado']}\n"
        f"  CEP:               {dados['cep']}\n"
        f"  Classe tarifária:  {dados['classe_tarifaria']}\n"
        f"  Tipo de ligação:   {dados['tipo_ligacao']}\n\n"
        "Confirma o cadastro? (sim/não)"
    )

    confirmacao = operador_input()

    if confirmacao.lower() in ("não", "nao", "n", "cancelar"):
        agente("Cadastro cancelado. Nenhum dado foi salvo.")
        sys.exit(0)

    # -----------------------------------------------------------------------
    # Etapa 6 — API de cadastro
    # -----------------------------------------------------------------------
    separador()
    resultado = chamar_api_mock(dados)

    if resultado["sucesso"]:
        uc_id = resultado["uc_id"]
        agente(
            f"Cadastro realizado com sucesso!\n\n"
            f"  ID da Unidade Consumidora: {GREEN}{BOLD}{uc_id}{RESET}{CYAN}\n\n"
            f"  {dados['nome_completo']} está registrada no sistema.\n"
            f"  O número da UC foi gerado e pode ser consultado a qualquer momento."
        )
    else:
        agente(f"Erro ao salvar o cadastro. Tente novamente.")

    separador()
    print(f"\n{GRAY}Sessão encerrada.{RESET}\n")


if __name__ == "__main__":
    main()
