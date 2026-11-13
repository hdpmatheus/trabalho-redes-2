# Participantes: NOME DOS INTEGRANTES DO GRUPO

import socket
import argparse

# Configura o endereço e a porta do servidor
parser = argparse.ArgumentParser()
parser.add_argument("--host", default="127.0.0.1")
parser.add_argument("--port", type=int, default=5001)
args = parser.parse_args()

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente.connect((args.host, args.port))

    print("Conectado ao servidor de horário!")

    with cliente:
        with cliente.makefile("r", encoding="utf-8") as leitor:
            while True:
                comando = input(
                    "Pressione Enter para consultar o horário ou digite 'sair': "
                )

                if comando.strip().lower() == "sair":
                    print("Encerrando conexão...")
                    break

                # Envia a solicitação de horário ao servidor
                cliente.sendall("HORA\n".encode("utf-8"))

                resposta = leitor.readline()

                if not resposta:
                    print("O servidor encerrou a conexão.")
                    break

                print("Horário atual:", resposta.strip())

except ConnectionRefusedError:
    print("Não foi possível conectar. Verifique se o servidor está ativo.")

except OSError as erro:
    print(f"Erro de comunicação: {erro}")

finally:
    print("Conexão encerrada.")