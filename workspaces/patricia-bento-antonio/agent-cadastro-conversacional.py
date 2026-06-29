"""
Agente Conversacional de Cadastro — Task as a Service
Useall Software · Prototipo para distribuidoras de energia

Fluxo:
  1. Operador envia foto do documento (CPF, RG ou CNH)
  2. Agente extrai dados via Claude Vision
  3. Agente conversa para confirmar / preencher campos faltantes
  4. Agente chama a API de cadastro e retorna o ID da UC criada

Uso:
  python agent-cadastro-conversacional.py --documento caminho/para/foto.jpg
  python agent-cadastro-conversacional.py --documento caminho/para/foto.jpg --api-url https://sua-api/cadastro

Variáveis de ambiente necessárias:
  ANTHROPIC_API_KEY  — chave da API Anthropic
"""

import anthropic
import base64
import json
import argparse
import sys
import os
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------

MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = """Você é um assistente especializado em cadastro de consumidores para distribuidoras de energia elétrica.

Seu papel é ajudar o operador (Cláudio) a cadastrar um consumidor/unidade consumidora (UC) a partir da foto de um documento.

DOCUMENTOS ACEITOS: CPF, RG ou CNH (Carteira Nacional de Habilitação).

CAMPOS NECESSÁRIOS PARA CADASTRO:
1. nome_completo — Nome completo do titular
2. cpf — CPF no formato XXX.XXX.XXX-XX
3. rg — RG (se disponível)
4. data_nascimento — Data de nascimento (DD/MM/AAAA)
5. endereco — Logradouro e número
6. bairro — Bairro
7. cidade — Cidade
8. estado — UF (2 letras)
9. cep — CEP (8 dígitos)
10. classe_tarifaria — Residencial / Comercial / Industrial / Rural / Poder Público
11. tipo_ligacao — Monofásico / Bifásico / Trifásico

INSTRUÇÕES:
- Extraia os dados que conseguir do documento
- Peça somente os campos que FALTAM, um ou dois por vez — não sobrecarregue o operador
- Confirme os dados extraídos antes de pedir mais informações
- Seja direto e profissional, linguagem simples
- Quando todos os campos estiverem preenchidos, apresente um resumo e peça confirmação
- Após confirmação, chame a API de cadastro

FORMATO DE EXTRAÇÃO INTERNA (use JSON no campo de dados, invisível ao operador):
Ao extrair dados do documento, estruture em JSON assim:
{
  "nome_completo": "",
  "cpf": "",
  "rg": "",
  "data_nascimento": "",
  "endereco": "",
  "bairro": "",
  "cidade": "",
  "estado": "",
  "cep": "",
  "classe_tarifaria": "",
  "tipo_ligacao": ""
}
"""


# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------

def carregar_imagem(caminho: str) -> tuple[str, str]:
    """Lê a imagem e retorna (base64, media_type)."""
    path = Path(caminho)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    ext = path.suffix.lower()
    media_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    media_type = media_types.get(ext, "image/jpeg")

    with open(path, "rb") as f:
        dados = base64.standard_b64encode(f.read()).decode("utf-8")

    return dados, media_type


def extrair_json_dados(texto: str) -> dict:
    """Tenta extrair um bloco JSON de dados do texto do assistente."""
    try:
        inicio = texto.find("{")
        fim = texto.rfind("}") + 1
        if inicio >= 0 and fim > inicio:
            return json.loads(texto[inicio:fim])
    except (json.JSONDecodeError, ValueError):
        pass
    return {}


def chamar_api_cadastro(dados: dict, api_url: str) -> dict:
    """
    Simula (ou chama de verdade) a API de cadastro.

    Se api_url == 'mock', simula a resposta.
    Caso contrário, faria um POST real (implementar conforme API da Useall).
    """
    if api_url == "mock":
        # Simulação — retorna um ID fictício
        uc_id = f"UC-{datetime.now().strftime('%Y')}-{hash(dados.get('cpf', '')) % 90000 + 10000:05d}"
        return {
            "sucesso": True,
            "uc_id": uc_id,
            "mensagem": f"Unidade consumidora cadastrada com sucesso.",
            "dados_salvos": dados,
        }

    # Chamada real (descomente e ajuste quando tiver a API):
    # import requests
    # response = requests.post(api_url, json=dados, timeout=30)
    # response.raise_for_status()
    # return response.json()

    raise NotImplementedError(
        "Chamada real à API não implementada neste protótipo. "
        "Use --api-url mock para simular."
    )


def campos_faltantes(dados: dict) -> list[str]:
    """Retorna lista de campos obrigatórios ainda vazios."""
    obrigatorios = [
        "nome_completo", "cpf", "data_nascimento",
        "endereco", "bairro", "cidade", "estado", "cep",
        "classe_tarifaria", "tipo_ligacao",
    ]
    return [c for c in obrigatorios if not dados.get(c)]


def formatar_resumo(dados: dict) -> str:
    """Formata os dados coletados em texto legível."""
    linhas = [
        "📋 **Resumo do Cadastro**",
        "",
        f"Nome: {dados.get('nome_completo', '—')}",
        f"CPF: {dados.get('cpf', '—')}",
        f"RG: {dados.get('rg', '—')}",
        f"Nascimento: {dados.get('data_nascimento', '—')}",
        "",
        f"Endereço: {dados.get('endereco', '—')}",
        f"Bairro: {dados.get('bairro', '—')}",
        f"Cidade/UF: {dados.get('cidade', '—')} - {dados.get('estado', '—')}",
        f"CEP: {dados.get('cep', '—')}",
        "",
        f"Classe tarifária: {dados.get('classe_tarifaria', '—')}",
        f"Tipo de ligação: {dados.get('tipo_ligacao', '—')}",
    ]
    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# Agente principal
# ---------------------------------------------------------------------------

class AgenteCADastro:
    def __init__(self, api_url: str = "mock"):
        self.client = anthropic.Anthropic()
        self.api_url = api_url
        self.historico: list[dict] = []
        self.dados_cadastro: dict = {}
        self.cadastro_concluido = False

    def enviar_mensagem(self, conteudo_usuario) -> str:
        """Envia mensagem ao Claude e retorna o texto de resposta."""
        self.historico.append({
            "role": "user",
            "content": conteudo_usuario,
        })

        response = self.client.messages.create(
            model=MODEL,
            max_tokens=2048,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            messages=self.historico,
        )

        # Extrai texto da resposta
        texto_resposta = ""
        for bloco in response.content:
            if bloco.type == "text":
                texto_resposta += bloco.text

        self.historico.append({
            "role": "assistant",
            "content": response.content,
        })

        return texto_resposta

    def analisar_documento(self, caminho_imagem: str) -> str:
        """Primeira etapa: envia a imagem e extrai dados."""
        print(f"\n📷 Analisando documento: {caminho_imagem}")
        print("Aguarde...")

        dados_img, media_type = carregar_imagem(caminho_imagem)

        conteudo = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": dados_img,
                },
            },
            {
                "type": "text",
                "text": (
                    "Esta é a foto do documento do consumidor. "
                    "Por favor:\n"
                    "1. Identifique o tipo de documento (CPF, RG ou CNH)\n"
                    "2. Extraia TODOS os dados visíveis\n"
                    "3. Apresente os dados encontrados ao operador de forma clara\n"
                    "4. Informe quais campos ainda precisam ser preenchidos\n\n"
                    "IMPORTANTE: No início da sua resposta, inclua um bloco JSON "
                    "com os dados extraídos, entre ``` json e ```, mesmo que alguns campos estejam vazios."
                ),
            },
        ]

        resposta = self.enviar_mensagem(conteudo)

        # Tenta extrair JSON da resposta para atualizar dados internos
        dados_extraidos = extrair_json_dados(resposta)
        if dados_extraidos:
            self.dados_cadastro.update({k: v for k, v in dados_extraidos.items() if v})

        return resposta

    def loop_conversa(self):
        """Loop interativo com o operador."""
        print("\n" + "=" * 60)
        print("AGENTE: Digite suas respostas abaixo. 'sair' para encerrar.")
        print("=" * 60 + "\n")

        while not self.cadastro_concluido:
            entrada = input("OPERADOR: ").strip()

            if not entrada:
                continue

            if entrada.lower() in ("sair", "cancelar", "exit"):
                print("\nAGENTE: Cadastro cancelado.")
                break

            # Verifica se operador confirmou resumo
            confirmacao = entrada.lower() in (
                "sim", "s", "confirmar", "confirmo", "ok", "correto",
                "está certo", "pode salvar", "salvar", "gravar"
            )

            # Monta contexto adicional para o agente
            contexto = f"{entrada}"
            if confirmacao and campos_faltantes(self.dados_cadastro) == []:
                contexto += (
                    "\n\n[SISTEMA: Operador confirmou. Prossiga com o cadastro. "
                    "Chame a API e informe o resultado.]"
                )

            resposta = self.enviar_mensagem(contexto)

            # Atualiza dados se o agente retornou JSON atualizado
            dados_atualizados = extrair_json_dados(resposta)
            if dados_atualizados:
                self.dados_cadastro.update({k: v for k, v in dados_atualizados.items() if v})

            print(f"\nAGENTE: {resposta}\n")

            # Detecta quando o agente indica que quer finalizar
            gatilhos_api = [
                "chamar a api", "efetuar o cadastro", "salvar o cadastro",
                "registrar no sistema", "criar a unidade consumidora",
                "confirme para eu registrar", "está pronto para cadastrar",
            ]
            if any(g in resposta.lower() for g in gatilhos_api):
                # Verifica se todos os campos estão preenchidos
                faltam = campos_faltantes(self.dados_cadastro)
                if not faltam:
                    print("\n[Sistema chamando API de cadastro...]\n")
                    resultado = chamar_api_cadastro(self.dados_cadastro, self.api_url)
                    if resultado.get("sucesso"):
                        uc_id = resultado.get("uc_id")
                        msg_final = (
                            f"✅ Cadastro realizado com sucesso!\n"
                            f"ID da Unidade Consumidora: **{uc_id}**\n\n"
                            f"O consumidor {self.dados_cadastro.get('nome_completo')} "
                            f"está cadastrado no sistema."
                        )
                        print(f"AGENTE: {msg_final}")
                        self.cadastro_concluido = True
                    else:
                        print(f"AGENTE: ❌ Erro no cadastro: {resultado.get('mensagem')}")


def main():
    parser = argparse.ArgumentParser(
        description="Agente Conversacional de Cadastro de Consumidor/UC"
    )
    parser.add_argument(
        "--documento",
        required=True,
        help="Caminho para a foto do documento (CPF, RG ou CNH)",
    )
    parser.add_argument(
        "--api-url",
        default="mock",
        help="URL da API de cadastro (padrão: 'mock' para simulação)",
    )
    args = parser.parse_args()

    # Verifica API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Erro: variável ANTHROPIC_API_KEY não definida.")
        print("   Execute: set ANTHROPIC_API_KEY=sua_chave_aqui")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  AGENTE CADASTRO CONVERSACIONAL — Useall Software")
    print("  Task as a Service · Distribuidoras de Energia")
    print("=" * 60)

    agente = AgenteCADastro(api_url=args.api_url)

    # Etapa 1: análise do documento
    resposta_inicial = agente.analisar_documento(args.documento)
    print(f"\nAGENTE: {resposta_inicial}\n")

    # Etapa 2: loop de conversa
    agente.loop_conversa()

    print("\n" + "=" * 60)
    print("Sessão encerrada.")


if __name__ == "__main__":
    main()
