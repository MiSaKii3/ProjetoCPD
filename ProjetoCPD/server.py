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

from primos import (
    find_max_prime_sequential,
    find_max_prime_parallel
)

from game_of_life import (
    game_of_life_sequential,
    game_of_life_parallel
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

        # Processamento RPC
        response = process_request(message)

        send_message(connection, response)

        connection.close()

def process_request(request):

    operation = request.get("operation")

    # ========================================================
    # PRIMOS SEQUENCIAL
    # ========================================================

    if operation == "prime_sequential":

        timeout = request.get("timeout", 5)

        result = find_max_prime_sequential(timeout)

        return {
            "status": "ok",
            "result": result
        }

    # ========================================================
    # PRIMOS PARALELO
    # ========================================================

    elif operation == "prime_parallel":

        timeout = request.get("timeout", 5)
        workers = request.get("workers", 4)

        result = find_max_prime_parallel(
            timeout,
            workers
        )

        return {
            "status": "ok",
            "result": result
        }

    # ========================================================
    # GAME OF LIFE SEQUENCIAL
    # ========================================================

    elif operation == "game_sequential":

        grid = request.get("grid")
        generations = request.get("generations")

        result = game_of_life_sequential(
            grid,
            generations
        )

        return {
            "status": "ok",
            "result": result
        }

    # ========================================================
    # GAME OF LIFE PARALELO
    # ========================================================

    elif operation == "game_parallel":

        grid = request.get("grid")
        generations = request.get("generations")
        workers = request.get("workers", 4)

        result = game_of_life_parallel(
            grid,
            generations,
            workers
        )

        return {
            "status": "ok",
            "result": result
        }

    # ========================================================
    # ERRO
    # ========================================================

    return {
        "status": "error",
        "message": "Operação inválida"
    }
# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    start_server()