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

    # Converte o dicionário para JSON
    data = json.dumps(message)

    #Envia todos os bytes da mensagem
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

    # Recebe dados enviados pelo socket
    data = connection.recv(4096).decode()

    # Converte JSON para dicionário Python
    return json.loads(data)