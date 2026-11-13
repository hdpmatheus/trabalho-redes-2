
# Participantes: Thais Carvalho, Vicente Alves, Matheus Henrique 

import socket
import threading
from datetime import datetime
import argparse


# Função responsável por atender cada cliente
def atender_cliente(conexao, endereco):
    print(f"Cliente conectado: {endereco[0]}:{endereco[1]}")

    try:
        with conexao:
            with conexao.makefile("r", encoding="utf-8") as leitor:
                for linha in leitor:
                    texto = linha.rstrip("\r\n")

                    # Verifica se a mensagem está vazia
                    if not texto.strip():
                        conexao.sendall(
                            "Mensagem vazia não permitida\n".encode("utf-8")
                        )
                        continue

                    horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                    print(
                        f"[{horario}] {endereco[0]}:{endereco[1]} - {texto}"
                    )

                    # Envia confirmação ao cliente
                    conexao.sendall(
                        "Mensagem recebida\n".encode("utf-8")
                    )

    except OSError as erro:
        print(f"Erro na conexão com {endereco}: {erro}")

    finally:
        print(f"Cliente desconectado: {endereco[0]}:{endereco[1]}")


# Configura os parâmetros do servidor
parser = argparse.ArgumentParser()
parser.add_argument("--host", default="0.0.0.0")
parser.add_argument("--port", type=int, default=5000)
args = parser.parse_args()

# Cria o socket TCP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((args.host, args.port))
    servidor.listen()

    print(f"Servidor aguardando conexões na porta {args.port}...")

    while True:
        conexao, endereco = servidor.accept()

        # Cria uma thread para cada cliente
        thread = threading.Thread(
            target=atender_cliente,
            args=(conexao, endereco)
        )
        thread.start()

except KeyboardInterrupt:
    print("\nServidor encerrado.")

finally:
    servidor.close()
