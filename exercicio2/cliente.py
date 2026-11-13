# Exercício 2 — Cliente Echo UDP
# Integrantes: [Matheus Henrique de Paula, Thais Pereira Carvalho e Vicente Alves Cordeiro Júnior ]

import argparse
import socket

MAX_BYTES = 65_507
TEMPO_LIMITE = 3


def main():
    parser = argparse.ArgumentParser(description="Cliente Echo UDP")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--porta", type=int, default=6000)
    args = parser.parse_args()

    if not 1 <= args.porta <= 65535:
        parser.error("A porta deve estar entre 1 e 65535.")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
            cliente.settimeout(TEMPO_LIMITE)

            while True:
                mensagem = input("Digite uma mensagem (ou 'sair'): ")
                if mensagem.strip().lower() == "sair":
                    break

                # O limite do UDP é em bytes, não em caracteres.
                dados = mensagem.encode("utf-8")
                if len(dados) > MAX_BYTES:
                    print("Mensagem muito grande. O limite é de 65.507 bytes.")
                    continue

                try:
                    cliente.sendto(dados, (args.host, args.porta))
                    resposta, _ = cliente.recvfrom(MAX_BYTES)
                    print(f"Eco: {resposta.decode('utf-8', errors='replace')}")
                except socket.timeout:
                    print("Nenhuma resposta do servidor em 3 segundos.")
                except OSError as erro:
                    print(f"Erro de comunicação: {erro}")
    except (KeyboardInterrupt, EOFError):
        pass
    except OSError as erro:
        print(f"Erro ao configurar o cliente: {erro}")

    print("Cliente encerrado.")


if __name__ == "__main__":
    main()
