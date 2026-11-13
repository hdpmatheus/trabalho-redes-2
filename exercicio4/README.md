# Exercício 4 — Servidor TCP de Horário

Servidor TCP que atende vários clientes simultaneamente e fornece o horário atual no formato HH:MM:SS. Também mantém um contador do total de clientes atendidos e registra as atividades com data, horário e quantidade de clientes.

## Dependências

Nenhuma além do Python 3.10+.

## Como executar

**Terminal 1 — Servidor:**

```bash
python3 servidor.py --host 0.0.0.0 --port 5001
```

**Terminal 2 — Cliente:**

```bash
python3 cliente.py --host 127.0.0.1 --port 5001
```

Abra dois ou mais terminais e execute um cliente em cada um para testar as conexões simultâneas.

Pressione Enter para solicitar o horário atual ou digite `sair` para encerrar a conexão.

## Funcionamento

- **Servidor:** utiliza uma thread para cada cliente conectado. Recebe solicitações e envia o horário atual. O contador de clientes é compartilhado entre as threads e protegido por `threading.Lock`.
- **Cliente:** conecta-se ao servidor, solicita o horário e exibe a resposta recebida. Permite realizar várias consultas na mesma conexão.
- **Protocolo:** comunicação TCP com mensagens em texto UTF-8, utilizando `HORA` como comando para solicitar o horário.
- **Logs:** registram data, horário, endereço IP, porta do cliente e total de clientes atendidos.