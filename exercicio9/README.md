## Exercício 9 — Tráfego DHCP

Foi utilizado o Wireshark para capturar a negociação DHCP ao conectar o computador à rede Wi-Fi. Foram identificadas as quatro mensagens do processo DORA: Discover, Offer, Request e ACK. O computador procurou um servidor DHCP, recebeu uma oferta de endereço IP, solicitou esse endereço e recebeu a confirmação do roteador 192.168.1.1.

**Filtro utilizado:** `dhcp`