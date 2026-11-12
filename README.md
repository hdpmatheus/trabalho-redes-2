# Trabalho 2 — Redes de Computadores 2

Trabalho prático da disciplina **Redes de Computadores 2**, ministrada pelo
professor **Alessandro Vivas Andrade**.

## Integrantes

- Matheus Henrique
- Thais Pereira
- Vicente Alves

## Sobre o trabalho

O objetivo é desenvolver habilidades práticas de programação em redes usando
os protocolos TCP e UDP, além de analisar o tráfego real de uma rede com o
Wireshark. A lista é dividida em duas partes:

**Programação com sockets (Python):** comunicação cliente-servidor com TCP e
UDP, uso de threads para atender vários clientes ao mesmo tempo, controle de
concorrência com `threading.Lock`, sistemas de chat com broadcast de
mensagens e comunicação bidirecional em tempo real com WebSockets e `asyncio`.
Todos os programas tratam erros de conexão, validam entradas e recebem host e
porta pela linha de comando.

**Análise de tráfego (Wireshark):** captura e inspeção de pacotes de alguns dos
principais protocolos da Internet: cabeçalhos HTTP, abertura (three-way
handshake) e encerramento de conexões TCP, resolução de nomes via DNS,
medição de tempo de ida e volta (RTT) com ICMP e o processo DORA de obtenção
de endereço via DHCP.

## Exercícios

| Diretório | Conteúdo | Responsável |
|---|---|---|
| `exercicio1/` | Cliente-servidor TCP multithread | Thais Pereira |
| `exercicio2/` | Servidor echo UDP | Vicente Alves |
| `exercicio3/` | Chat em rede com TCP | Matheus Henrique |
| `exercicio4/` | Servidor de hora com threads e contador thread-safe | Thais Pereira |
| `exercicio5/` | Wireshark: tráfego HTTP | Matheus Henrique |
| `exercicio6/` | Wireshark: abertura e encerramento de conexão TCP | Thais Pereira |
| `exercicio7/` | Wireshark: resolução de nomes via DNS | Vicente Alves |
| `exercicio8/` | Wireshark: tráfego ICMP (ping) | Vicente Alves |
| `exercicio9/` | Wireshark: tráfego DHCP (DORA) | Vicente Alves |
| `exercicio10/` | Chat em rede com WebSockets | Matheus Henrique |

Cada diretório contém um `README.md` com as instruções de execução ou, nos
exercícios do Wireshark, a captura (`.pcapng`), um print e a análise do que foi
observado.

## Requisitos

- Linux
- Python 3.10 ou superior
- Wireshark (exercícios 5 a 9)
- Biblioteca `websockets`, apenas para o Exercício 10: `pip install websockets`

## Como executar

Os exercícios de programação seguem o mesmo padrão: inicie o servidor em um
terminal e um ou mais clientes em outros terminais. Por exemplo:

```bash
cd exercicio3
python3 servidor.py --porta 5001     # terminal 1
python3 cliente.py --porta 5001      # terminais 2, 3, ...
```

Todos os programas aceitam `--host` e `--porta`; use `--help` para ver as
opções de cada um.