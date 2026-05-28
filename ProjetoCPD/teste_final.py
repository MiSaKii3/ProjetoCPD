from primos import *
from game_of_life import *
from client import send_request

import time
import random

"""
Ficheiro central de testes automáticos do projeto CPD.

Conteúdo:
- Testes dos números primos;
- Testes do Game of Life;
- Testes RPC cliente-servidor;
- Comparações de desempenho entre versões sequenciais e paralelas.

"""

# ============================================================
# IMPORTS
# ============================================================

import time
import random

from primos import (
    is_prime,
    find_max_prime_sequential,
    find_max_prime_parallel
)

from game_of_life import (
    game_of_life_sequential,
    game_of_life_parallel
)

from client import send_request


# ============================================================
# TESTES - NÚMEROS PRIMOS
# ============================================================

"""
Objetivo:
Testar a correção e desempenho das implementações
sequencial e paralela da procura de números primos.
"""


# ------------------------------------------------------------
# TESTE is_prime
# ------------------------------------------------------------

def test_is_prime():

    print("\n" + "=" * 60)
    print("TESTE - is_prime")
    print("=" * 60)

    test_cases = [

        (2, True),
        (3, True),
        (4, False),
        (5, True),
        (9, False),
        (11, True),
        (15, False),
        (17, True),
        (25, False),
        (29, True)

    ]

    for number, expected in test_cases:

        result = is_prime(number)

        if result == expected:
            print(f"[OK]   {number}")

        else:
            print(f"[FAIL] {number}")


# ------------------------------------------------------------
# TESTE SEQUENCIAL
# ------------------------------------------------------------

def test_prime_sequential(timeout = 5):

    print("\n=== TESTE PRIMOS SEQUENCIAL ===")

    start = time.time()

    result = find_max_prime_sequential(timeout)

    elapsed = time.time() - start

    print(f"Maior primo encontrado: {result}")
    print(f"Tempo de execução: {elapsed:.2f}s")


# ------------------------------------------------------------
# TESTE PARALELO
# ------------------------------------------------------------

def test_prime_parallel(timeout = 5,
                        workers = 4):

    print("\n=== TESTE PRIMOS PARALELO ===")

    start = time.time()

    result = find_max_prime_parallel(timeout, workers)

    elapsed = time.time() - start

    print(f"Maior primo encontrado: {result}")
    print(f"Workers: {workers}")
    print(f"Tempo de execução: {elapsed:.2f}s")


# ------------------------------------------------------------
# COMPARAÇÃO ENTRE VERSÕES
# ------------------------------------------------------------

def compare_prime_versions(timeout = 5,
                           workers = 4):

    print("\n" + "=" * 60)
    print("COMPARAÇÃO - NÚMEROS PRIMOS")
    print("=" * 60)

    # Sequencial
    start_seq = time.time()

    seq_result = find_max_prime_sequential(timeout)

    seq_time = time.time() - start_seq

    # Paralela
    start_par = time.time()

    par_result = find_max_prime_parallel(timeout, workers)

    par_time = time.time() - start_par

    # Resultados
    print(f"\nSequencial: {seq_result}")
    print(f"Paralela:   {par_result}")

    print("\n=== TEMPOS ===")

    print(f"Sequencial: {seq_time:.2f}s")
    print(f"Paralela:   {par_time:.2f}s")

    # Speedup
    if par_time > 0:

        speedup = seq_time / par_time

        efficiency = speedup / workers

        print("\n=== DESEMPENHO ===")

        print(f"Speedup:    {speedup:.2f}x")
        print(f"Eficiência: {efficiency:.2f}")


# ============================================================
# TESTES - GAME OF LIFE
# ============================================================

"""
Objetivo:
Validar a consistência dos resultados e comparar
o desempenho das versões sequencial e paralela.
"""


# ------------------------------------------------------------
# TESTE CONSISTÊNCIA
# ------------------------------------------------------------

def test_game_consistency():

    print("\n" + "=" * 60)
    print("TESTE - CONSISTÊNCIA GAME OF LIFE")
    print("=" * 60)

    initial_grid = [

        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]

    ]

    generations = 5

    result_seq = game_of_life_sequential(
        initial_grid,
        generations
    )

    result_par = game_of_life_parallel(
        initial_grid,
        generations,
        workers = 4
    )

    if result_seq == result_par:

        print("[OK] Resultados iguais")

        print("\nResultado final:")

        for row in result_seq:
            print(row)

    else:
        print("[FAIL] Resultados diferentes")


# ------------------------------------------------------------
# TESTE SEQUENCIAL
# ------------------------------------------------------------

def test_game_sequential(rows = 50,
                         cols = 50,
                         generations = 10):

    print("\n=== TESTE GAME OF LIFE SEQUENCIAL ===")

    grid = [

        [random.choice([0, 1]) for _ in range(cols)]

        for _ in range(rows)

    ]

    start = time.time()

    game_of_life_sequential(
        grid,
        generations
    )

    elapsed = time.time() - start

    print(f"Grelha: {rows}x{cols}")
    print(f"Gerações: {generations}")
    print(f"Tempo: {elapsed:.2f}s")


# ------------------------------------------------------------
# TESTE PARALELO
# ------------------------------------------------------------

def test_game_parallel(rows = 50,
                       cols = 50,
                       generations = 10,
                       workers = 4):

    print("\n=== TESTE GAME OF LIFE PARALELO ===")

    grid = [

        [random.choice([0, 1]) for _ in range(cols)]

        for _ in range(rows)

    ]

    start = time.time()

    game_of_life_parallel(
        grid,
        generations,
        workers
    )

    elapsed = time.time() - start

    print(f"Grelha: {rows}x{cols}")
    print(f"Gerações: {generations}")
    print(f"Workers: {workers}")
    print(f"Tempo: {elapsed:.2f}s")


# ------------------------------------------------------------
# COMPARAÇÃO ENTRE VERSÕES
# ------------------------------------------------------------

def compare_game_versions(rows = 100,
                          cols = 100,
                          generations = 10,
                          workers = 4):

    print("\n" + "=" * 60)
    print("COMPARAÇÃO - GAME OF LIFE")
    print("=" * 60)

    random.seed(42)

    grid = [

        [random.choice([0, 1]) for _ in range(cols)]

        for _ in range(rows)

    ]

    # Sequencial
    start_seq = time.time()

    seq_result = game_of_life_sequential(
        grid,
        generations
    )

    seq_time = time.time() - start_seq

    # Paralela
    start_par = time.time()

    par_result = game_of_life_parallel(
        grid,
        generations,
        workers
    )

    par_time = time.time() - start_par

    print(f"\nDimensão: {rows}x{cols}")
    print(f"Gerações: {generations}")
    print(f"Workers: {workers}")

    print("\n=== TEMPOS ===")

    print(f"Sequencial: {seq_time:.4f}s")
    print(f"Paralela:   {par_time:.4f}s")

    # Consistência
    print("\n=== CONSISTÊNCIA ===")

    if seq_result == par_result:
        print("Resultados iguais")

    else:
        print("Resultados diferentes")

    # Speedup
    if par_time > 0:

        speedup = seq_time / par_time

        efficiency = speedup / workers

        print("\n=== DESEMPENHO ===")

        print(f"Speedup:    {speedup:.2f}x")
        print(f"Eficiência: {efficiency:.2f}")


# ============================================================
# TESTES RPC
# ============================================================

"""
Objetivo:
Testar a comunicação cliente-servidor
e a execução remota das operações.
"""


# ------------------------------------------------------------
# TESTE RPC - PRIMOS
# ------------------------------------------------------------

def test_rpc_prime():

    print("\n" + "=" * 60)
    print("TESTE RPC - PRIMOS")
    print("=" * 60)

    request = {

        "method": "prime_parallel",

        "params": {
            "timeout": 5,
            "workers": 4
        }

    }

    response = send_request(request)

    print("\nResposta do servidor:")
    print(response)


# ------------------------------------------------------------
# TESTE RPC - GAME OF LIFE
# ------------------------------------------------------------

def test_rpc_game():

    print("\n" + "=" * 60)
    print("TESTE RPC - GAME OF LIFE")
    print("=" * 60)

    request = {

        "method": "game_parallel",

        "params": {

            "grid": [

                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 0]

            ],

            "generations": 5,
            "workers": 4
        }

    }

    response = send_request(request)

    print("\nResposta do servidor:")
    print(response)


# ------------------------------------------------------------
# TESTE RPC - list_methods
# ------------------------------------------------------------

def test_list_methods():

    print("\n" + "=" * 60)
    print("TESTE RPC - LIST METHODS")
    print("=" * 60)

    request = {

        "method": "list_methods",
        "params": {}

    }

    response = send_request(request)

    print("\nMétodos disponíveis:")
    print(response)


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    # ========================================================
    # TESTES PRIMOS
    # ========================================================

    test_is_prime()

    test_prime_sequential(timeout = 5)

    test_prime_parallel(
        timeout = 5,
        workers = 4
    )

    compare_prime_versions(
        timeout = 5,
        workers = 4
    )

    # ========================================================
    # TESTES GAME OF LIFE
    # ========================================================

    test_game_consistency()

    test_game_sequential(
        rows = 50,
        cols = 50,
        generations = 10
    )

    test_game_parallel(
        rows = 50,
        cols = 50,
        generations = 10,
        workers = 4
    )

    compare_game_versions(
        rows = 100,
        cols = 100,
        generations = 10,
        workers = 4
    )

    # ========================================================
    # TESTES RPC
    # ========================================================

    # IMPORTANTE:
    # O servidor deve estar em execução.

    test_rpc_prime()

    test_rpc_game()

    test_list_methods()