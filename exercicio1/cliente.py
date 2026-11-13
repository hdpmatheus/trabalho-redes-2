
# Participantes: Thais Carvalho, Vicente Alves, Matheus Henrique 

import socket
import argparse


# Configura os parâmetros do cliente
parser = argparse.ArgumentParser()
parser.add_argument("--host", default="127.0.0.1")
parser.add_argument("--port", type=int, default=5000)
args = parser.parse_args()

# Cria o socket TCP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conecta ao servidor
    cliente.connect((args.host, args.port))
    print("Conectado ao servidor!")
    print("Digite suas mensagens ou 'sair' para encerrar.")

    # Cria um leitor para receber as respostas
    with cliente.makefile("r", encoding="utf-8") as leitor:
        while True:
            mensagem = input("Você: ")

            # Verifica o comando de saída
            if mensagem.strip().lower() == "sair":
                print("Encerrando conexão...")
                break

            # Verifica se a mensagem está vazia
            if not mensagem.strip():
                print("Não é permitido enviar mensagens vazias.")
                continue

            # Envia a mensagem ao servidor
            cliente.sendall((mensagem + "\n").encode("utf-8"))

            # Recebe a resposta do servidor
            resposta = leitor.readline()

            if not resposta:
                print("O servidor encerrou a conexão.")
                break

            print("Servidor:", resposta.strip())

except ConnectionRefusedError:
    print("Não foi possível conectar. Verifique se o servidor está ativo.")

except OSError as erro:
    print(f"Erro de comunicação: {erro}")

finally:
    cliente.close()
    print("Conexão encerrada.")
