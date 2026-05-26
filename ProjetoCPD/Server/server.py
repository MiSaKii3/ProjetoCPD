"""
Neste ficheiro encontra-se o servidor RPC responsável por
receber pedidos dos clientes e executar operações remotamente.

Operações suportadas:
- procura de números primos;
- Game of Life.

"""

# ============================================================
# IMPORTS
# ============================================================

import socket

from rpc_protocol import (
    send_message,
    receive_message
)



# ============================================================
# CONFIGURAÇÃO
# ============================================================

HOST = "127.0.0.1"
PORT = 5000

# ============================================================
# SERVIDOR
# ============================================================

def start_server():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server_socket.bind((HOST, PORT))

    server_socket.listen()

    print(f"[SERVER] À escuta em {HOST}:{PORT}")

    while True:

        connection, address = server_socket.accept()

        print(f"[SERVER] Cliente conectado ao servidor {address}.")

        message = receive_message(connection)

        print(f"[SERVER] Mensagem recebida:")
        print(message)

        response ={
            "status": "ok",
            "message": "Pedido recebido com sucesso."
        }

        send_message(connection, response)

        connection.close()

# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    start_server()