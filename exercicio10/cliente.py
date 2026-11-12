#!/usr/bin/env python3
"""
Exercício 10 - Cliente de Chat com WebSockets (Python)

 Conecta ao servidor WebSocket, registra o nome de usuário e permite enviar
  e receber mensagens ao mesmo tempo. Digite "sair" para encerrar.

Como enviar e receber ao mesmo tempo:
  input() é bloqueante e travaria o asyncio. Por isso o teclado é lido por
  uma thread separada (daemon), que coloca cada linha numa fila asyncio.
  Duas tarefas assíncronas rodam em paralelo: uma recebe do servidor e outra
  envia o que chega da fila.
"""

import argparse
import asyncio
import json
import sys
import threading

from websockets.asyncio.client import ClientConnection, connect
from websockets.exceptions import ConnectionClosed, InvalidURI


def ler_teclado(loop: asyncio.AbstractEventLoop, fila: asyncio.Queue) -> None:
    """Thread que lê o teclado e entrega cada linha à fila do asyncio."""
    for linha in sys.stdin:
        loop.call_soon_threadsafe(fila.put_nowait, linha.rstrip("\n"))
    loop.call_soon_threadsafe(fila.put_nowait, None)  # EOF (Ctrl+D)


def exibir(bruto: str) -> None:
    """Formata e exibe uma mensagem recebida do servidor."""
    try:
        dados = json.loads(bruto)
    except json.JSONDecodeError:
        print(bruto)
        return
    tipo = dados.get("tipo")
    if tipo == "mensagem":
        print(f"[{dados.get('nome')}] {dados.get('texto')}")
    elif tipo == "sistema":
        print(f"*** {dados.get('texto')} ***")
    elif tipo == "erro":
        print(f"ERRO: {dados.get('texto')}")


async def receber(ws: ClientConnection) -> None:
    """Tarefa que exibe continuamente as mensagens recebidas."""
    try:
        async for bruto in ws:
            exibir(bruto)
    except ConnectionClosed:
        pass
    print("Conexão com o servidor encerrada.")


async def enviar(ws: ClientConnection, fila: asyncio.Queue) -> None:
    """Tarefa que envia o que o usuário digita."""
    while True:
        linha = await fila.get()
        if linha is None or linha.strip().lower() == "sair":
            await ws.close()  # fechamento limpo (close frame)
            return
        if not linha.strip():
            continue
        await ws.send(json.dumps({"tipo": "mensagem", "texto": linha},
                                 ensure_ascii=False))


async def main() -> None:
    parser = argparse.ArgumentParser(description="Cliente de chat WebSocket")
    parser.add_argument("--host", default="127.0.0.1",
                        help="endereço do servidor (padrão: 127.0.0.1)")
    parser.add_argument("--porta", type=int, default=8765,
                        help="porta do servidor (padrão: 8765)")
    parser.add_argument("--nome", help="nome de usuário (se omitido, é perguntado)")
    args = parser.parse_args()

    nome = (args.nome or "").strip()
    while not nome:
        nome = input("Seu nome de usuário: ").strip()

    uri = f"ws://{args.host}:{args.porta}"
    try:
        async with connect(uri, open_timeout=10) as ws:
            await ws.send(json.dumps({"tipo": "entrar", "nome": nome},
                                     ensure_ascii=False))
            print(f"Conectado a {uri}. Entrando como '{nome}'... (digite 'sair' para encerrar)")

            fila: asyncio.Queue = asyncio.Queue()
            threading.Thread(target=ler_teclado,
                             args=(asyncio.get_running_loop(), fila),
                             daemon=True).start()

            # Roda as duas tarefas; quando qualquer uma termina, cancela a outra.
            tarefas = [asyncio.create_task(receber(ws)),
                       asyncio.create_task(enviar(ws, fila))]
            _, pendentes = await asyncio.wait(tarefas,
                                              return_when=asyncio.FIRST_COMPLETED)
            for t in pendentes:
                t.cancel()
    except ConnectionRefusedError:
        print(f"Conexão recusada: não há servidor em {uri}.")
    except (OSError, InvalidURI, asyncio.TimeoutError) as erro:
        print(f"Não foi possível conectar a {uri}: {erro}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCliente encerrado.")