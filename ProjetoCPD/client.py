"""
Neste ficheiro encontra-se o cliente RPC responsável por
enviar pedidos ao servidor.

O cliente estabelece ligação TCP com o servidor,
envia pedidos remotos (RPC) e recebe os respetivos
resultados.

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
# ENVIO DE PEDIDOS
# ============================================================

"""
A função send_request envia um pedido RPC ao servidor.

Args:
    request:
        Pedido que contém:
        - operação;
        - argumentos;
        - parametros;

Returns:
    Resposta enviada pelo servidor.

"""

def send_request(request):

    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client_socket.connect((HOST, PORT))

    #Envia o pedido
    send_message(client_socket, request)

    #Recebe resposta
    response = receive_message(client_socket)

    client_socket.close()

    return response



# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("CLIENTE RPC")
    print("=" * 50)