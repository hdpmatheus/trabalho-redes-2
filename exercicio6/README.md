## Exercício 6 — Estabelecimento e Encerramento de Conexão TCP

Foi utilizado o Wireshark para capturar uma conexão TCP com o servidor example.com, utilizando a porta 80. Foram identificados os três pacotes do three-way handshake: SYN, SYN-ACK e ACK, que são utilizados para estabelecer a conexão. Também foram observados os pacotes FIN e ACK, responsáveis pelo encerramento da comunicação.

**Filtro utilizado:** `tcp.port == 34124`