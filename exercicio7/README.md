## Exercício 7 — Resolução de Nomes via DNS

Foi utilizado o Wireshark para analisar consultas DNS feitas ao acessar o YouTube. Foram identificadas consultas dos tipos A, AAAA e HTTPS, enviadas ao servidor DNS 177.74.224.29. Na resposta do tipo A, o servidor retornou oito endereços IPv4 associados ao domínio www.youtube.com, como 142.251.153.4 e 142.251.151.4.

**Filtro utilizado:** `dns.qry.name == "www.youtube.com"`