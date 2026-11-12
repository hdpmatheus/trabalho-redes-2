#!/usr/bin/env python3

"""
Exercício 3 = Servidor de Chat TCP 

Servidor de chat que aceita qualquer número de clientes. Cada mensagem recebida é retransmitida para todos os demais, precedida do nome do remetente. Entradas e saídas são anunciadas.

Protocolo (texto UTF-8, uma mensagem por linha terminada em '\n'):
1. A primeira linha enviada pelo cliente é o seu nickname
2. O servidor responde "OK" ou "ERRO <Motivo>" em caso de erro
3. As linhas seguintes são mensagens de chat
"""

import argparse
import socket
import threading
from datetime import datetime


# Clientes conectados: socket -> nickname
# Várias threads acessam este dicionário, por isso ele é protegido por um Lock
clientes: dict[socket.socket, str] = {}
trava_clientes = threading.Lock()

TAMANHO_MAX_NICK = 20


def log(texto: str) -> None:
    """Imprime uma linha de log com a hora atual."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {texto}")


def enviar(conn: socket.socket, texto: str) -> bool:
    """Envia uma linha a um cliente. Retorna False se a conexão falhou."""
    try:
        conn.sendall((texto + "\n").encode("utf-8"))
        return True
    except OSError:
        return False


def broadcast(texto: str, exceto: socket.socket | None = None) -> None:
    """Envia o texto a todos os clientes, exceto ao remetente."""
    # Copia a lista dentro do Lock e envia fora dele, para que um cliente
    # lento não bloqueie as outras threads.
    with trava_clientes:
        destinos = [c for c in clientes if c is not exceto]
    for conn in destinos:
        if not enviar(conn, texto):
            # Cliente com falha: a própria thread dele fará a limpeza.
            log("Falha ao enviar para um cliente; ele será desconectado.")


def atender_cliente(conn: socket.socket, endereco: tuple) -> None:
    """Thread de um cliente: registra o nickname e repassa as mensagens."""
    ip, porta = endereco
    nick = None
    try:
        with conn, conn.makefile("r", encoding="utf-8") as leitor:
            # --- Etapa 1: registro do nickname ---
            linha = leitor.readline()
            if not linha:
                return  # desconectou antes de enviar o nome
            candidato = linha.strip()

            with trava_clientes:
                em_uso = candidato.lower() in (n.lower() for n in clientes.values())
                valido = 0 < len(candidato) <= TAMANHO_MAX_NICK and not em_uso
                if valido:
                    clientes[conn] = candidato
            if not valido:
                motivo = "nome já em uso" if em_uso else \
                    f"nome deve ter de 1 a {TAMANHO_MAX_NICK} caracteres"
                enviar(conn, f"ERRO {motivo}")
                return

            nick = candidato
            enviar(conn, "OK")
            log(f"{nick} entrou ({ip}:{porta}). Online: {len(clientes)}")
            broadcast(f"*** {nick} entrou na sala ***", exceto=conn)

            # --- Etapa 2: loop de mensagens ---
            for linha in leitor:
                mensagem = linha.strip()
                if not mensagem:
                    continue  # ignora mensagens vazias
                log(f"{nick}: {mensagem}")
                broadcast(f"[{nick}] {mensagem}", exceto=conn)

    except (ConnectionResetError, BrokenPipeError, UnicodeDecodeError):
        log(f"Conexão com {ip}:{porta} interrompida abruptamente")
    finally:
        # Remove o cliente e avisa os demais, aconteça o que acontecer.
        if nick is not None:
            with trava_clientes:
                clientes.pop(conn, None)
                restantes = len(clientes)
            log(f"{nick} saiu. Online: {restantes}")
            broadcast(f"*** {nick} saiu da sala ***")


def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor de chat TCP")
    parser.add_argument("--host", default="0.0.0.0",
                        help="endereço de escuta (padrão: 0.0.0.0)")
    parser.add_argument("--porta", type=int, default=5001,
                        help="porta de escuta (padrão: 5001)")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            servidor.bind((args.host, args.porta))
        except OSError as erro:
            print(f"Não foi possível usar a porta {args.porta}: {erro}")
            return
        servidor.listen()
        log(f"Servidor de chat ouvindo em {args.host}:{args.porta}")

        try:
            while True:
                conn, endereco = servidor.accept()
                threading.Thread(target=atender_cliente,
                                 args=(conn, endereco), daemon=True).start()
        except KeyboardInterrupt:
            print()
            log("Servidor encerrado pelo usuário (Ctrl+C)")


if __name__ == "__main__":
    main()