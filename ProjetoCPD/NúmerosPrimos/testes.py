"""
Neste ficheiro serão feitos testes automáticos para o conteúdo de primos.py

"""

import time

from primos import (
    is_prime,
    find_max_prime_sequential,
    find_max_prime_parallel
)

# --------------------------------------------------------------------
# TESTES DA FUNÇÃO is_prime
# --------------------------------------------------------------------

"""
Objetivo: testa vários casos de primalidade.

"""

def test_is_prime():

    print("\n=== TESTE is_prime ===")

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

    for number, expect in test_cases:

        result = is_prime(number)

        if result == expect:
            print(f"[OK]   {number}")

        else:
            print(f"[FAIL] {number}")

# --------------------------------------------------------------------
# TESTES DA VERSÃO SEQUENCIAL
# --------------------------------------------------------------------

"""
Objetivo: Executar a versão sequencial e medir desempenho.

"""

def test_sequencial(timeout = 5):

    print("\n=== TESTE SEQUENCIAL ===")

    start = time.time()

    result = find_max_prime_sequential(timeout)

    elapsed = time.time() - start

    print(f"Maior primo encontrado: {result}")
    print(f"Tempo de execução: {elapsed:.2f} segundos")

# --------------------------------------------------------------------
# TESTES DA VERSÃO PARALELA
# --------------------------------------------------------------------

"""
Objetivo: Executar a versão paralela e medir desempenho.

"""

def test_parallel(timeout = 5, workers = 4):

    print("\n=== TESTE PARALELO ===")

    start = time.time()

    result = find_max_prime_parallel(timeout, workers)

    elapsed = time.time() - start

    print(f"Maior primo encontrado: {result}")
    print(f"Workers: {workers}")
    print(f"Tempo de execução: {elapsed: .2f} segundos")

# --------------------------------------------------------------------
# COMPARAÇÃO ENTRE VERSÕES
# --------------------------------------------------------------------

"""
Objetivo: Comparar diretamente as versões sequencial e paralela

"""

def compare_versions(timeout = 5, workers = 4):

    print("\n=== COMPARAÇÃO ===")

    # Sequencial
    start_seq = time.time()

    seq_result = find_max_prime_sequential(timeout)

    seq_time = time.time() - start_seq

    # Paralela
    start_par = time.time()

    par_result = find_max_prime_parallel(timeout, workers)

    par_time = time.time() - start_par

    print("\n=== RESULTADOS ===")

    print(f"Sequencial: {seq_result:}")
    print(f"Paralela: {par_result:}")

    print("\n=== TEMPOS ===")

    print(f"Sequencial: {seq_time:.2f}s")
    print(f"Paralela: {par_time:.2f}s")

    # Speedup
    if par_time > 0:

        speedup = seq_time / par_time

        print(f"\n Speedup: {speedup:.2f}x")

# --------------------------------------------------------------------
# EXECUÇÃO
# --------------------------------------------------------------------

if __name__ == "__main__":

    test_is_prime()

    test_sequencial(timeout = 5)

    test_parallel(timeout = 5, workers = 4)

    compare_versions(timeout = 5, workers = 4)