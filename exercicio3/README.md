# Exercício 3 — Chat em Rede (TCP)

Chat com servidor central e qualquer número de clientes. Cada mensagem é
retransmitida para os demais com o nome do remetente, e entradas e saídas
são anunciadas.

## Dependências

Nenhuma além do Python 3.10+.

## Como executar

Terminal 1:

```bash
python3 servidor.py --porta 5001
```

Abra dois ou mais terminais e rode um cliente em cada:

```bash
python3 cliente.py --host 127.0.0.1 --porta 5001
```

O cliente pede o nickname (ou use `--nick Ana`). Digite mensagens
normalmente e `sair` para deixar a sala: o servidor e os outros clientes
continuam funcionando.

## Funcionamento

- **Servidor:** uma thread por cliente. O dicionário de clientes conectados é
  compartilhado entre threads e protegido por `threading.Lock`. Nicknames
  repetidos ou vazios são recusados.
- **Cliente:** duas threads, a principal lê o teclado e envia, e uma thread
  separada recebe e exibe as mensagens continuamente.
- **Protocolo:** texto UTF-8, uma mensagem por linha. A primeira linha é o
  nickname; o servidor responde `OK` ou `ERRO <motivo>`.
