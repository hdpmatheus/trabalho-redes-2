# Exercício 2 — Servidor Echo (UDP)
O cliente envia mensagens por UDP. O servidor mostra a mensagem e o endereço do remetente no terminal e devolve os mesmos dados ao cliente.
## Requisitos
- Linux e Python 3.10 ou superior.
- Não é necessário instalar bibliotecas adicionais.
## Como executar
Abra dois terminais na pasta `exercicio2`. No primeiro, inicie o servidor.
```bash
python3 servidor.py --host 127.0.0.1 --porta 6000
```Deixe o servidor aberto. No segundo terminal, inicie o cliente.
```bash
python3 cliente.py --host 127.0.0.1 --porta 6000
```
Digite uma mensagem, como `Olá, redes!`. O cliente deve mostrar `Eco: Olá, redes!`. Envie outras mensagens no mesmo terminal. Digite `sair` para fechar só o cliente. Para parar o servidor, pressione `Ctrl+C` no primeiro terminal.
Os parâmetros `--host` e `--porta` são opcionais. Os valores padrão são `127.0.0.1` (o próprio computador) e `6000`. Se mudar a porta, use o mesmo número nos dois comandos.
O cliente verifica o limite de 65.507 bytes após codificar a mensagem em UTF-8 e avisa se não receber resposta em 3 segundos. Para testar esse aviso, pare o servidor e envie uma mensagem pelo cliente.
