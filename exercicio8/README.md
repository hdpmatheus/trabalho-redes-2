## Exercício 8 — Tráfego ICMP (ping)

Foi utilizado o comando ping para testar a comunicação com o roteador 192.168.1.1. No Wireshark, foram identificados quatro pacotes de solicitação e quatro de resposta ICMP. Os tempos de ida e volta (RTT) foram de 8,99 ms, 3,44 ms, 9,03 ms e 2,77 ms, com média de 6,058 ms. Todos os pacotes receberam resposta, sem nenhuma perda.

**Comando utilizado:** `ping -c 4 192.168.1.1`

**Filtro utilizado:** `icmp`