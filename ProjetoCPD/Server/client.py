"""
Neste ficheiro encontra-se o cliente RPC responsável por
enviar pedidos ao servidor.

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
# CLIENTE
# ============================================================

def start_client():

    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client_socket.connect((HOST, PORT))

    request = {
        "operation": "test",
        "message": "Olá servidor"
    }

    send_message(client_socket, request)

    response = receive_message(client_socket)

    print("[CLIENT]")
    print(response)

    client_socket.close()

# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    start_client()