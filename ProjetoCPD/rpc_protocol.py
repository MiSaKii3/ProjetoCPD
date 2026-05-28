"""
Neste ficheiro encontra-se o protocolo RPC utilizado na comunicação
entre cliente e servidor.

Responsabilidades:
- serialização de mensagens;
- envio de dados;
- receção de mensagens;
- conversão JSON <-> Python.

"""

# ============================================================
# IMPORTS
# ============================================================

import json

# ============================================================
# ENVIO DE MENSAGENS
# ============================================================

"""
Função que envia uma mensagem JSON através de uma ligação socket.

Args:
    connection:
        Socket de comunicação.
        
    message:
        Mensagem a enviar.

"""

def send_message(connection, message):

    data = json.dumps(message)

    connection.sendall(data.encode())

# ============================================================
# RECEÇÃO DE MENSAGENS
# ============================================================

"""
Função que recebe uma mensagem JSON.

Args:
    connection:
        Socket de comunicação.

    Return:
        Mensagem enviada.

"""

def receive_message(connection):

    data = connection.recv(4096).decode()

    return json.loads(data)