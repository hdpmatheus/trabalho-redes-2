# Participantes: NOME DOS INTEGRANTES DO GRUPO

import socket
import threading
from datetime import datetime
import argparse

# Contador de clientes atendidos
total_clientes = 0

# Controla o acesso ao contador entre as threads
trava = threading.Lock()


# Registra as mensagens com data, horário e total de clientes
def registrar_log(mensagem):
    with trava:
        quantidade = total_clientes

    horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{horario}] [Clientes: {quantidade}] {mensagem}")


# Atende cada cliente conectado
def atender_cliente(conexao, endereco):
    global total_clientes

    with trava:
        total_clientes += 1

    registrar_log(f"Cliente conectado: {endereco[0]}:{endereco[1]}")

    try:
        with conexao:
            with conexao.makefile("r", encoding="utf-8") as leitor:
                for linha in leitor:
                    comando = linha.strip().upper()

                    if comando == "HORA":
                        horario = datetime.now().strftime("%H:%M:%S")
                        conexao.sendall((horario + "\n").encode("utf-8"))

                        registrar_log(
                            f"Horário enviado para {endereco[0]}:{endereco[1]}"
                        )
                    else:
                        conexao.sendall(
                            "Comando inválido. Envie HORA.\n".encode("utf-8")
                        )

    except OSError as erro:
        registrar_log(f"Erro com o cliente {endereco}: {erro}")

    finally:
        registrar_log(f"Cliente desconectado: {endereco[0]}:{endereco[1]}")


# Configura o endereço e a porta do servidor
parser = argparse.ArgumentParser()
parser.add_argument("--host", default="0.0.0.0")
parser.add_argument("--port", type=int, default=5001)
args = parser.parse_args()

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((args.host, args.port))
    servidor.listen()

    registrar_log(f"Servidor aguardando conexões na porta {args.port}...")

    while True:
        conexao, endereco = servidor.accept()

        thread = threading.Thread(
            target=atender_cliente,
            args=(conexao, endereco)
        )
        thread.start()

except KeyboardInterrupt:
    registrar_log("Servidor encerrado.")

finally:
    servidor.close()