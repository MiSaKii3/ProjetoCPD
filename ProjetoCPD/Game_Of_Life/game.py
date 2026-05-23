import multiprocessing

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def count_neighbors(grid, row, col):
    """
    Conta o número de vizinhos vivos de uma célula.

    A função verifica as 8 posições adjacentes
    (horizontal, vertical e diagonal), respeitando
    os limites da grelha.

    Args:
        grid (list[list[int]]):
            Grelha atual do jogo.

        row (int):
            Linha da célula.

        col (int):
            Coluna da célula.

    Returns:
        int:
            Número de vizinhos vivos.
    """

    rows = len(grid)
    cols = len(grid[0])

    neighbors = 0

    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):

            # Ignora a própria célula
            if r == row and c == col:
                continue

            # Verifica limites da grelha
            if 0 <= r < rows and 0 <= c < cols:
                neighbors += grid[r][c]

    return neighbors


def compute_next_state(grid, row, col):
    """
    Calcula o próximo estado de uma célula
    de acordo com as regras do Game of Life.

    Args:
        grid (list[list[int]]):
            Grelha atual.

        row (int):
            Linha da célula.

        col (int):
            Coluna da célula.

    Returns:
        int:
            Novo estado da célula:
            1 para viva,
            0 para morta.
    """

    alive_neighbors = count_neighbors(grid, row, col)

    cell = grid[row][col]

    # Célula viva
    if cell == 1:

        # Subpopulação ou sobrepopulação
        if alive_neighbors < 2 or alive_neighbors > 3:
            return 0

        # Sobrevive
        return 1

    # Reprodução
    if alive_neighbors == 3:
        return 1

    return 0


# ============================================================
# VERSÃO SEQUENCIAL
# ============================================================

def game_of_life_sequential(grid, generations):
    """
    Simula o Game of Life utilizando
    uma abordagem sequencial.

    A grelha evolui durante um número fixo
    de gerações, aplicando as regras do jogo
    simultaneamente a todas as células.

    Args:
        grid (list[list[int]]):
            Grelha inicial do jogo.

        generations (int):
            Número de gerações a simular.

    Returns:
        list[list[int]]:
            Grelha final após todas
            as gerações.
    """

    rows = len(grid)
    cols = len(grid[0])

    current_grid = [row[:] for row in grid]

    for _ in range(generations):

        new_grid = [[0 for _ in range(cols)] for _ in range(rows)]

        for row in range(rows):
            for col in range(cols):

                new_grid[row][col] = compute_next_state(
                    current_grid,
                    row,
                    col
                )

        current_grid = new_grid

    return current_grid


# ============================================================
# WORKER PARALELO
# ============================================================

def game_of_life_worker(grid,
                        start_row,
                        end_row,
                        result_queue):
    """
    Worker responsável pelo processamento
    de uma região da grelha.

    Cada worker calcula o próximo estado
    das células pertencentes ao intervalo
    de linhas atribuído.

    Args:
        grid (list[list[int]]):
            Grelha atual.

        start_row (int):
            Linha inicial da região.

        end_row (int):
            Linha final da região.

        result_queue:
            Queue utilizada para devolver
            os resultados ao processo principal.
    """

    cols = len(grid[0])

    partial_result = []

    for row in range(start_row, end_row):

        new_row = []

        for col in range(cols):

            new_row.append(
                compute_next_state(grid, row, col)
            )

        partial_result.append((row, new_row))

    result_queue.put(partial_result)


# ============================================================
# VERSÃO PARALELA
# ============================================================

def game_of_life_parallel(grid,
                          generations,
                          workers):
    """
    Simula o Game of Life recorrendo
    a múltiplos processos em paralelo.

    A grelha é dividida em regiões
    horizontais, sendo cada região
    processada por um worker distinto.

    A sincronização entre gerações é
    garantida pelo processo principal,
    assegurando consistência entre
    a versão sequencial e paralela.

    Args:
        grid (list[list[int]]):
            Grelha inicial do jogo.

        generations (int):
            Número de gerações a simular.

        workers (int):
            Número de processos workers.

    Returns:
        list[list[int]]:
            Grelha final após todas
            as gerações.
    """

    rows = len(grid)
    cols = len(grid[0])

    current_grid = [row[:] for row in grid]

    for _ in range(generations):

        result_queue = multiprocessing.Queue()

        processes = []

        rows_per_worker = rows // workers

        for i in range(workers):

            start_row = i * rows_per_worker

            # Último worker fica com o restante
            if i == workers - 1:
                end_row = rows
            else:
                end_row = start_row + rows_per_worker

            process = multiprocessing.Process(
                target=game_of_life_worker,
                args=(
                    current_grid,
                    start_row,
                    end_row,
                    result_queue
                )
            )

            processes.append(process)

            process.start()

        # Nova grelha
        new_grid = [[0 for _ in range(cols)] for _ in range(rows)]

        # Recolha de resultados
        for _ in range(workers):

            partial_result = result_queue.get()

            for row_index, row_data in partial_result:
                new_grid[row_index] = row_data

        # Espera pelos workers
        for process in processes:
            process.join()

        current_grid = new_grid

    return current_grid