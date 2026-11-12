# Exercício 10 — Chat com WebSockets

Chat em tempo real com servidor Python (biblioteca `websockets`, asyncio).
Há dois clientes que funcionam na mesma sala: um em Python (terminal) e um em
HTML/JavaScript (navegador).

## Dependências

```bash
pip install -r requirements.txt     # ou: pip install websockets
```

Requer `websockets` 13 ou superior (usa a API `websockets.asyncio`).

## Como executar

Terminal 1:

```bash
python3 servidor.py --porta 8765
```

Cliente Python (um por terminal):

```bash
python3 cliente.py --host 127.0.0.1 --porta 8765 --nome Ana
```

Cliente no navegador: abra `cliente.html` (duplo clique ou
`xdg-open cliente.html`), confira o endereço `ws://localhost:8765`, digite um
nome e clique em **Entrar**.

Digite `sair` (ou clique em **Sair**) para deixar o chat.

## Funcionamento

- O servidor usa **asyncio** em vez de threads: todas as conexões rodam em uma
  única thread, que alterna entre elas enquanto esperam dados.
- Mensagens trafegam em JSON (`{"tipo": "mensagem", "nome": ..., "texto": ...}`),
  e cada uma é identificada pelo nome do usuário. Nomes repetidos são recusados.
- **Desconexões inesperadas** (terminal ou aba fechados) geram
  `ConnectionClosed`, tratada na corrotina do cliente. O bloco `finally`
  remove o usuário, avisa os demais, e o servidor continua no ar.
