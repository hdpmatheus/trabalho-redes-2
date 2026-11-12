#!/usr/bin/env python3
"""
Exercício 10 - Servidor de Chat com WebSockets

  Servidor de chat usando a biblioteca "websockets" (asyncio). Aceita várias
  conexões simultâneas e retransmite cada mensagem para todos os demais
  clientes, identificando o remetente pelo nome de usuário. Desconexões
  inesperadas são tratadas sem derrubar o servidor.

Diferença em relação ao Exercício 3:
  Aqui não há uma thread por cliente: o asyncio executa todas as conexões em
  uma única thread, alternando entre elas enquanto esperam dados (E/S
  assíncrona). Por isso não é necessário Lock para o conjunto de clientes.

Protocolo (mensagens em JSON):
  cliente -> servidor:  {"tipo": "entrar", "nome": "Ana"}   (primeira mensagem)
                        {"tipo": "mensagem", "texto": "Olá"}
  servidor -> cliente:  {"tipo": "mensagem", "nome": "Ana", "texto": "Olá"}
                        {"tipo": "sistema", "texto": "Ana entrou no chat"}
                        {"tipo": "erro", "texto": "..."}
"""

import argparse
import asyncio
import json
import logging

from websockets.asyncio.server import ServerConnection, broadcast, serve
from websockets.exceptions import ConnectionClosed

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
# Silencia os logs internos detalhados da biblioteca.
logging.getLogger("websockets").setLevel(logging.WARNING)

TAMANHO_MAX_NOME = 20

# Conexões ativas: websocket -> nome do usuário.
clientes: dict[ServerConnection, str] = {}


def json_msg(**campos) -> str:
    """Serializa um dicionário em JSON (mantendo acentos legíveis)."""
    return json.dumps(campos, ensure_ascii=False)


def enviar_para_outros(remetente: ServerConnection, texto_json: str) -> None:
    """Broadcast para todos menos o remetente.
    broadcast() não lança exceção se algum cliente já tiver caído."""
    broadcast([c for c in clientes if c is not remetente], texto_json)


async def registrar(websocket: ServerConnection) -> str | None:
    """Recebe a primeira mensagem e valida o nome. Retorna o nome ou None."""
    try:
        dados = json.loads(await asyncio.wait_for(websocket.recv(), timeout=30))
        nome = str(dados.get("nome", "")).strip()
        if dados.get("tipo") != "entrar":
            raise ValueError
    except (json.JSONDecodeError, ValueError, AttributeError):
        await websocket.send(json_msg(tipo="erro",
                                      texto="primeira mensagem deve ser 'entrar'"))
        return None
    except asyncio.TimeoutError:
        return None

    if not 0 < len(nome) <= TAMANHO_MAX_NOME:
        await websocket.send(json_msg(
            tipo="erro", texto=f"nome deve ter de 1 a {TAMANHO_MAX_NOME} caracteres"))
        return None
    if nome.lower() in (n.lower() for n in clientes.values()):
        await websocket.send(json_msg(tipo="erro", texto="nome já em uso"))
        return None
    return nome


async def atender(websocket: ServerConnection) -> None:
    """Corrotina executada para cada cliente conectado."""
    endereco = websocket.remote_address
    nome = None
    try:
        nome = await registrar(websocket)
        if nome is None:
            return  # registro recusado; a conexão será fechada

        clientes[websocket] = nome
        logging.info("%s entrou (%s:%s). Online: %d",
                     nome, endereco[0], endereco[1], len(clientes))
        await websocket.send(json_msg(
            tipo="sistema", texto=f"Bem-vindo(a), {nome}! Online: {len(clientes)}"))
        enviar_para_outros(websocket, json_msg(tipo="sistema",
                                               texto=f"{nome} entrou no chat"))

        # "async for" recebe mensagens até a conexão fechar.
        async for bruto in websocket:
            try:
                dados = json.loads(bruto)
                texto = str(dados.get("texto", "")).strip()
            except (json.JSONDecodeError, AttributeError):
                await websocket.send(json_msg(tipo="erro", texto="JSON inválido"))
                continue
            if not texto:
                continue  # ignora mensagens vazias
            logging.info("%s: %s", nome, texto)
            enviar_para_outros(websocket,
                               json_msg(tipo="mensagem", nome=nome, texto=texto))

    except ConnectionClosed:
        # Desconexão inesperada (ex.: cliente fechou o terminal/aba).
        logging.info("Conexão de %s caiu inesperadamente", nome or endereco)
    finally:
        # Limpeza sempre executada: o servidor segue atendendo os demais.
        if nome is not None and clientes.pop(websocket, None) is not None:
            logging.info("%s saiu. Online: %d", nome, len(clientes))
            broadcast(clientes, json_msg(tipo="sistema",
                                         texto=f"{nome} saiu do chat"))


async def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor de chat WebSocket")
    parser.add_argument("--host", default="0.0.0.0",
                        help="endereço de escuta (padrão: 0.0.0.0)")
    parser.add_argument("--porta", type=int, default=8765,
                        help="porta de escuta (padrão: 8765)")
    args = parser.parse_args()

    try:
        async with serve(atender, args.host, args.porta) as servidor:
            logging.info("Servidor WebSocket em ws://%s:%d", args.host, args.porta)
            await servidor.serve_forever()
    except OSError as erro:
        logging.error("Não foi possível usar a porta %d: %s", args.porta, erro)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário (Ctrl+C)")