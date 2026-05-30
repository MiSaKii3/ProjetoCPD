# Trabalho prático - Números primos

## Descrição

Projeto desenvolvido no âmbito da unidade curricular de Computação Paralela e Distruibuída no ano letivo 2025/2026. Autoria: Camila Costa - 202300662 e Filipe Tomás -  202200690.

Este trabalho inclui:

1) procura sequencial e paralela de números primos;
2) simulação do jogo Game of Life;
3) sistema RPC com sockets TCP.

---

# Estrutura do projeto

- **primos.py**
    - Implementação da procura de números primos.
  
- **game_of_life.py**
  - Implementação sequencial e paralela do Game of Life.
  
- **rpc_protocol.py**
    - Protocolo de comunicação RPC com serialização JSON.
  
- **server.py**
    - Servidor RCP responsável pelo processamento dos pedidos.
  
- **client.py**
    - Cliente RPC para envio de pedidos remotos.

- **testes.py**
    - Testes automáticos e análise de desempenho.
    
---
 
## Tecnologias usadas

- multiprocessing
- threading
- socket
- json

---

## Execução

### Passos

1. Iniciar o servidor;
2. Iniciar os testes.