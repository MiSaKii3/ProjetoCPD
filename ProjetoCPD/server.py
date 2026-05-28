"""
Neste ficheiro encontra-se o servidor RPC responsável por
receber pedidos dos clientes e executar operações remotamente.

Operações suportadas:
- procura sequencial de números primos;
- procura paralela de números primos;
- Game of Life sequential;
- Game of Life paralelo.

O servidor utiliza:
- sockets RPC;
- serialização JSON,
- threads para múltiplos cliéntes;
- processamento RPC.

"""

# ============================================================
# IMPORTS
# ============================================================

import socket
import threading

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
# PROCESSAMENTO DOS PEDIDOS
# ============================================================

"""
Função que processa pedidos RPC enviados pelos clientes.

Args:
    request:
        Pedido recebido.

Returns:
    Resposta enviada ao cliente.

"""

def process_request(request):

    operation = request.get("operation")

    # ============================================================
    # PRIMOS SEQUENCIAL
    # ============================================================

    if operation == "prime_sequential":

        timeout = request.get("timeout", 5)

        result = find_max_prime_sequential(timeout)

        return {
            "status": "ok",
            "operation": operation,
            "result": result
        }

    # ============================================================
    # PRIMOS PARALELO
    # ============================================================

    elif operation == "prime_parallel":

        timeout = request.get("timeout", 5)

        workers = request.get("workers", 4)

        result = find_max_prime_parallel(
            timeout,
            workers
        )

        return {
            "status": "ok",
            "operation": operation,
            "workers": workers,
            "result": result
        }

    # ============================================================
    # GAME OF LIFE SEQUENCIAL
    # ============================================================

    elif operation == "game_sequential":

        grid = request.get("grid")

        generations = request.get(
            "generations",
            10
        )

        result = game_of_life_sequential(
            grid,
            generations
        )

        return {
            "status": "ok",
            "operation": operation,
            "result": result
        }

    # ============================================================
    # GAME OF LIFE PARALELO
    # ============================================================

    elif operation == "game_parallel":

        grid = request.get("grid")

        generations = request.get(
            "generations",
            10
        )

        workers = request.get(
            "workers",
            4
        )

        result = game_of_life_parallel(
            grid,
            generations,
            workers
        )

        return {
            "status": "ok",
            "operation": operation,
            "workers": workers,
            "result": result
        }

    # ============================================================
    # OPERAÇÃO INVÁLIDA
    # ============================================================

    return {
        "status": "error",
        "message": "operação inválida"
    }

# ============================================================
# CLIENT HANDLER
# ============================================================

"""
Função responsável por tratar um cliente.

Cada cliente é executado numa thread distinta,
permitindo múltiplas ligações em simultâneo.

Args:
    connection:
        Socket de comunicação.
        
    address:
        Endereço do cliente.

"""

def handle_client(connection, address):

    print(f"\n[SERVER] Cliente conectado com: {address}")

    try:

        # Recebe pedido
        request = receive_message(connection)

        print("[SERVER] Pedido recebido:")
        print(request)

        # Processa a operação
        response = process_request(request)

        # Envia resposta
        send_message(connection, response)

        print("[SERVER] Resposta enviada")

    except Exception as error:

        print("[SERVER] erro:")
        print(error)

        send_message(connection, {
            "status": "error",
            "message": str(error)
        })

    finally:

        connection.close()

        print("[SERVER] Ligação encerrada")


# ============================================================
# SERVIDOR PRINCIPAL
# ============================================================

"""
Inicializa o servidor RPC.

Funções:
- aceitar clientes;
- criar threads;
- processar pedidos;
- devolver respostas;

"""

def start_server():

    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    #Evita o erro "Address already in use"
    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server_socket.bind((HOST, PORT))

    server_socket.listen()

    print("=" * 50)
    print("Servidor RPC")
    print("=" * 50)

    print(f"[SERVER] À escuta em {HOST}:{PORT}")

    while True:

        # Aceita ligação
        connection, address = server_socket.accept()

        #Criação da thread
        thread = threading.Thread(
            target=handle_client,
            args=(connection, address)
        )

        # Inicia a thread
        thread.start()


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    start_server()