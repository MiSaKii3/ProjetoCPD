"""
Neste ficheiro será feita a implementação da procura sequencial e paralela
do maior número primo dentro de um limite temporal.

Conteúdo aqui presente:
- Função de verificação da primalidade fornecida no enunciado do projeto;
- Versão sequencial da procura;
- Versão paralela com multiprocessing.

"""

# --------------------------------------------------------------------
# IMPORTS
# --------------------------------------------------------------------

import math
import time
import multiprocessing

# --------------------------------------------------------------------
# FUNÇÃO PARA VERIFICAÇÃO DE PRIMALIDADE
# --------------------------------------------------------------------

"""
Implementação da função presente no enunciado do projeto: 
- Verifica se um número é primo.

Definição de número primo: Número natural maior do que 1 que possui exatamente dois divisores
distintos: O número 1 e ele próprio.

"""

def is_prime(n: int) -> bool:

    if n < 2: # Números < 2 não são primos
        return False

    if n in (2, 3): # 2 e 3 são primos
        return True

    if n % 2 == 0 or n % 3 == 0: # Se o resto for 0 o número é divisível
        return False

    divisor = 5 # Começamos a testar divisores a partir do 5

    while divisor * divisor <= n: # Verificação de divisores até à raíz quadrada do número
        if n % divisor == 0 or n % (divisor + 2) == 0:
            return False
        divisor += 6

    return True

# --------------------------------------------------------------------
# VERSÃO SEQUENCIAL
# --------------------------------------------------------------------

"""
Objetivo: Procurar o maior número primo possível durante um determinado intervalo
de tempo.

Estratégias a adotar:
- testar continuamente números ímpares;
- guardar o maior primo encontrado;
- terminar o programa quando o tempo limite é atingido.

"""

def find_max_prime_sequential(timeout: int) -> int:

    #Guarda o instante inicial
    start_time = time.time()

    # Melhor resultado encontrado até ao momento
    max_prime = 2

    # Começo em 3
    candidate = 3

    # Teste apenas de ímpares
    while True:

        # Tempo decorrido
        elapsed_time = time.time() - start_time

        # Verifica se o timeout foi atingido
        if elapsed_time > timeout:
            break

        # Verifica se o número é primo
        if is_prime(candidate):
            max_prime = candidate

        #Próximo ímpar
        candidate += 2

    return max_prime


# ============================================================
# WORKER PARA VERSÃO PARALELA
# ============================================================

"""
Responsável por procurar números primos.

Cada worker irá explorar uma sequência distinta de números, 
evitando sobreposição de trabalho.

- start (int): Primeiro número a testar;
- step (int): Incremento entre candidatos;
- end_time (float): Instante absoluto de término;
- shared_max_prime: Valor partilhado entre processos que contém o maior primo encontrado;
- lock: Mecanismo de sincronização utilizado para evitar race conditions - SEM ELE 2 PROCESSOS
PODERIAM ATUALIZAR shared_max_prime.value;

"""

def prime_worker(start: int,
                 step: int,
                 end_time: float,
                 shared_max_prime,
                 lock):

    # Número atual a testar
    candidate = start

    # Continua enquanto houver tempo disponível
    while time.time() < end_time:

        # Verifica se é primo
        if is_prime(candidate):

            # Apenas um processo pode atualizar o valor partilhado de cada vez
            # Evita race condition
            with lock:

                # Só atualiza se foi encontrado um nº maior
                if candidate > shared_max_prime.value:
                    shared_max_prime.value = candidate

        # Próximo número da sequência
        candidate += step

# ============================================================
# VERSÃO PARALELA
# ============================================================

"""
Responsável por procurar o maior número primo possível com recurso a múltiplos processos em paralelo.

Parâmetros a ter em conta:
- dividir o trabalho entre vários workers de forma a evitar repetições;
- utilização de multiprocessing;
- partilha do melhor resultado encontrado;
- sincronização com Lock;
- terminação coordenada através de timeout - parar todos os workers ao memso tempo.

"""

def find_max_prime_parallel(timeout: int,
                            workers: int) -> int:

    # Instante absoluto de término
    end_time = time.time() + timeout

    # Valor partilhado entre processos
    # 'Q' - Unsigned Long Long - Ideal para números primos grandes
    # 2 - Valor inicial já que é o menor número primo possível
    shared_max_prime = multiprocessing.Value('Q', 2)

    # Lock para sincronização
    lock = multiprocessing.Lock()

    # Lista de processos
    processes = []

    # Cada worker recebe um início diferemte o mesmo salto
    step = workers * 2

    for i in range (workers):

        # Apenas números ímpares
        start = 3 + (i * 2)

        # Criação do processo
        process = multiprocessing.Process(target = prime_worker,
                                          args = (start, step, end_time, shared_max_prime, lock))
        processes.append(process)

        process.start()

    # Espera pela conclusão de todos os processos
    for process in processes:

        process.join()

    return shared_max_prime.value