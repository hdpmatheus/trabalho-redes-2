#!/usr/bin/env python3
"""
Exercício 3 - Cliente de Chat TCP

Pede um nickname, conecta ao servidor de chat e usa duas threads:
    - thread principal: lê o teclado e envia as mensagens;
    - thread receptora: recebe continuamente e exibe as mensagens dos outros.
  Digite "sair" para encerrar sem afetar o servidor nem os demais clientes.
  """

  import argparse
import socket
import threading

# Sinaliza à thread principal que a conexão caiu.
conexao_encerrada = threading.Event()


def receber(leitor) -> None:
    """Thread receptora: exibe tudo o que chega do servidor."""
    try:
        for linha in leitor:
            print(linha.rstrip("\n"))
    except (OSError, ValueError):
        pass  # socket fechado pela thread principal ao sair
    finally:
        if not conexao_encerrada.is_set():
            conexao_encerrada.set()
            print("\nConexão com o servidor perdida. Pressione Enter para sair.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Cliente de chat TCP")
    parser.add_argument("--host", default="127.0.0.1",
                        help="endereço do servidor (padrão: 127.0.0.1)")
    parser.add_argument("--porta", type=int, default=5001,
                        help="porta do servidor (padrão: 5001)")
    parser.add_argument("--nick", help="nickname (se omitido, é perguntado)")
    args = parser.parse_args()

    nick = args.nick
    while not nick or not nick.strip():
        try:
            nick = input("Seu nickname: ")
        except (EOFError, KeyboardInterrupt):
            print()
            return
    nick = nick.strip()

    try:
        sock = socket.create_connection((args.host, args.porta), timeout=10)
    except ConnectionRefusedError:
        print(f"Conexão recusada: não há servidor em {args.host}:{args.porta}.")
        return
    except (socket.timeout, socket.gaierror, OSError) as erro:
        print(f"Não foi possível conectar: {erro}")
        return

    with sock, sock.makefile("r", encoding="utf-8") as leitor:
        try:
            # Registro do nickname (primeira linha do protocolo).
            sock.sendall((nick + "\n").encode("utf-8"))
            resposta = leitor.readline().strip()
            if resposta != "OK":
                print(f"Servidor recusou o nickname: {resposta or 'sem resposta'}")
                return
            # Após o registro, sem timeout: a leitura espera indefinidamente.
            sock.settimeout(None)
        except (OSError, socket.timeout) as erro:
            print(f"Erro no registro: {erro}")
            return

        print(f"Conectado como '{nick}'. Digite 'sair' para encerrar.")
        threading.Thread(target=receber, args=(leitor,), daemon=True).start()

        try:
            while not conexao_encerrada.is_set():
                mensagem = input()
                if conexao_encerrada.is_set():
                    break
                if mensagem.strip().lower() == "sair":
                    break
                if not mensagem.strip():
                    continue  # não envia mensagens vazias
                sock.sendall((mensagem + "\n").encode("utf-8"))
        except (EOFError, KeyboardInterrupt):
            pass
        except OSError:
            print("Falha ao enviar: conexão perdida.")
        finally:
            conexao_encerrada.set()
            # shutdown avisa o servidor (FIN) e desbloqueia a thread receptora.
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
    print("Você saiu do chat.")


if __name__ == "__main__":
    main()