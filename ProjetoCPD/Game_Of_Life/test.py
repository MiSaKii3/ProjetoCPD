"""
Neste ficheiro serão feitos testes automáticos para o conteúdo de game.py
"""

import time
from game import (
    game_of_life_sequential,
    game_of_life_parallel
)

# --------------------------------------------------------------------
# TESTES DA FUNÇÃO (consistência entre versões)
# --------------------------------------------------------------------

"""
Objetivo: testa se as versões sequencial e paralela produzem o mesmo resultado.
"""


def test_consistency():
    print("\n=== TESTE CONSISTÊNCIA ===")

    # Grelha inicial (blinker)
    initial_grid = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ]

    generations = 5

    result_seq = game_of_life_sequential(initial_grid, generations)
    result_par = game_of_life_parallel(initial_grid, generations, workers=4)

    if result_seq == result_par:
        print("[OK] Versões sequencial e paralela produzem o mesmo resultado")
        print("\nResultado final:")
        for row in result_seq:
            print(row)
    else:
        print("[FAIL] Resultados diferentes entre versões")


# --------------------------------------------------------------------
# TESTES DA VERSÃO SEQUENCIAL
# --------------------------------------------------------------------

"""
Objetivo: Executar a versão sequencial e medir desempenho.
"""


def test_sequential(rows=50, cols=50, generations=10):
    print("\n=== TESTE SEQUENCIAL ===")

    # Criar grelha inicial aleatória
    import random
    grid = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

    start = time.time()
    result = game_of_life_sequential(grid, generations)
    elapsed = time.time() - start

    print(f"Dimensão da grelha: {rows}x{cols}")
    print(f"Número de gerações: {generations}")
    print(f"Tempo de execução: {elapsed:.2f} segundos")


# --------------------------------------------------------------------
# TESTES DA VERSÃO PARALELA
# --------------------------------------------------------------------

"""
Objetivo: Executar a versão paralela e medir desempenho.
"""


def test_parallel(rows=50, cols=50, generations=10, workers=4):
    print("\n=== TESTE PARALELO ===")

    # Criar grelha inicial aleatória
    import random
    grid = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

    start = time.time()
    result = game_of_life_parallel(grid, generations, workers)
    elapsed = time.time() - start

    print(f"Dimensão da grelha: {rows}x{cols}")
    print(f"Número de gerações: {generations}")
    print(f"Workers: {workers}")
    print(f"Tempo de execução: {elapsed:.2f} segundos")


# --------------------------------------------------------------------
# COMPARAÇÃO ENTRE VERSÕES
# --------------------------------------------------------------------

"""
Objetivo: Comparar diretamente as versões sequencial e paralela
"""


def compare_versions(rows=50, cols=50, generations=10, workers=4):
    print("\n=== COMPARAÇÃO ===")

    # Criar mesma grelha para ambas versões
    import random
    random.seed(42)  # Para resultados reproduzíveis
    grid_seq = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]
    random.seed(42)
    grid_par = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

    # Sequencial
    start_seq = time.time()
    seq_result = game_of_life_sequential(grid_seq, generations)
    seq_time = time.time() - start_seq

    # Paralela
    start_par = time.time()
    par_result = game_of_life_parallel(grid_par, generations, workers)
    par_time = time.time() - start_par

    print("\n=== RESULTADOS ===")
    print(f"Sequencial: Grelha final de {rows}x{cols}")
    print(f"Paralela: Grelha final de {rows}x{cols}")

    print("\n=== TEMPOS ===")
    print(f"Sequencial: {seq_time:.2f}s")
    print(f"Paralela: {par_time:.2f}s")

    # Speedup
    if par_time > 0:
        speedup = seq_time / par_time
        print(f"\nSpeedup: {speedup:.2f}x")

        if speedup > 1:
            print("✓ Versão paralela foi mais rápida")
        else:
            print("✗ Versão sequencial foi mais rápida (overhead do paralelismo)")


# --------------------------------------------------------------------
# EXECUÇÃO
# --------------------------------------------------------------------

if __name__ == "__main__":
    # Teste de consistência (grelha pequena conhecida)
    test_consistency()

    # Teste com grelha pequena (pouco ganho com paralelismo)
    test_sequential(rows=50, cols=50, generations=10)
    test_parallel(rows=50, cols=50, generations=10, workers=4)

    # Teste com grelha média (possível algum ganho)
    test_sequential(rows=200, cols=200, generations=10)
    test_parallel(rows=200, cols=200, generations=10, workers=4)

    # Comparação direta
    compare_versions(rows=100, cols=100, generations=10, workers=4)