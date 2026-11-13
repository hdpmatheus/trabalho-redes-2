# Exercício 2 — Servidor Echo UDP
# Integrantes: [Matheus Henrique de Paula, Thais Pereira Carvalho e Vicente Alves Cordeiro Júnior ]

import argparse
import socket

MAX_BYTES = 65_507


def main():
    parser = argparse.ArgumentParser(description="Servidor Echo UDP")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--porta", type=int, default=6000)
    args = parser.parse_args()

    if not 1 <= args.porta <= 65535:
        parser.error("A porta deve estar entre 1 e 65535.")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
            # Associa o socket UDP ao endereço em que vai receber mensagens.
            servidor.bind((args.host, args.porta))
            print(f"Servidor UDP ouvindo em {args.host}:{args.porta}.")

            while True:
                dados, remetente = servidor.recvfrom(MAX_BYTES)
                mensagem = dados.decode("utf-8", errors="replace")
                ip, porta = remetente
                print(f"{ip}:{porta} enviou {mensagem!r}")

                # Devolve os mesmos bytes recebidos, sem alterar a mensagem.
                try:
                    servidor.sendto(dados, remetente)
                except OSError as erro:
                    print(f"Não foi possível enviar o eco: {erro}")
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    except OSError as erro:
        print(f"Erro no servidor: {erro}")


if __name__ == "__main__":
    main()
