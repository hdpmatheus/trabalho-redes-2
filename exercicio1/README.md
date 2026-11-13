# Exercício 1 — Comunicação TCP entre Cliente e Servidor

Comunicação utilizando TCP, com suporte a vários clientes simultâneos. O servidor recebe mensagens, registra a data, o horário e o endereço do cliente, e envia uma confirmação de recebimento.

## Dependências

Nenhuma além do Python 3.10+.

## Como executar

**Terminal 1 — Servidor:**

```bash
python3 servidor.py --host 0.0.0.0 --port 5000
```

**Terminal 2 — Cliente:**

```bash
python3 cliente.py --host 127.0.0.1 --port 5000
```

Para testar vários clientes simultaneamente, abra dois ou mais terminais e execute o cliente em cada um.

Digite mensagens normalmente e `sair` para encerrar a conexão.

## Funcionamento

- **Servidor:** utiliza uma thread para cada cliente conectado, permitindo o atendimento simultâneo. Recebe as mensagens, registra data, horário, IP e porta do remetente e envia uma confirmação.
- **Cliente:** conecta-se ao servidor, permite o envio de várias mensagens e exibe as respostas recebidas. Não permite o envio de mensagens vazias.
- **Protocolo:** TCP, com mensagens em texto UTF-8, utilizando quebra de linha (`\n`) para separar cada mensagem.