"""
Neste ficheiro encontra-se implementada a versão sequencial e paralela do Game of Life.

Conteúdo deste ficheiro:

- Função auxiliar para contagem de vizinhos vivos;
- Função responsável pelo cálculo do próximo estado de cada célula;
- Versão sequencial da simulação;
- Versão paralela com recurso a multiprocessing;
- Divisão da grelha em regiões independentes;
- Comunicação entre processos através de Queue;
- Sincronização entre gerações da simulação.

"""

# ============================================================
# IMPORTS
# ============================================================

import multiprocessing

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def count_neighbors(grid, row, col):
    """
    Conta o número de vizinhos vivos de uma célula.

    A função verifica as 8 posições adjacentes:
    - horizontal;
    - vertical;
    - diagonal;

    A grelha não é cíclica, pelo que células
    nas fronteiras possuem menos vizinhos.

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

    #Percorre posições adjacentes
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

    Regras:
    - uma célula viva com menos de 2 vizinhos morre;
    - uma célula viva com 2 ou 3 vizinhos sobrevive;
    - uma célula viva com mais de 3 vizinhos morre;
    - uma célula morta com exatamente 3 vizinhos nasce.

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

    current_cell = grid[row][col]

    # ============================================================
    # CÉLULA VIVA
    # ============================================================

    # Célula viva
    if current_cell == 1:

        # Subpopulação ou sobrepopulação
        if alive_neighbors < 2 or alive_neighbors > 3:
            return 0

        # Sobrevive
        return 1

    # ============================================================
    # CÉLULA MORTA
    # ============================================================

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
    simultaneamente a todas as células, que
    são processadas num único processo.

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

    # Cópia da grelha inical
    current_grid = [row[:] for row in grid]

    # ============================================================
    # PROCESSAMENTO DAS GERAÇÕES
    # ============================================================

    for _ in range(generations):

        # Nova geração
        new_grid = [[0 for _ in range(cols)] for _ in range(rows)]

        # Atualização de cada célula
        for row in range(rows):
            for col in range(cols):

                new_grid[row][col] = compute_next_state(
                    current_grid,
                    row,
                    col
                )

        # Atualiza a grelha atual
        current_grid = new_grid

    return current_grid


# ============================================================
# WORKER PARALELO
# ============================================================

"""
    Worker responsável pelo processamento
    de uma região da grelha.

    Cada worker cálcula o próximo estado
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

def game_of_life_worker(grid,
                        start_row,
                        end_row,
                        result_queue):

    cols = len(grid[0])

    partial_result = []

    # ============================================================
    # PROCESSAMENTO DAS LINHAS ATRIBUÍDAS
    # ============================================================

    for row in range(start_row, end_row):

        new_row = []

        for col in range(cols):

            new_row.append(
                compute_next_state(grid, row, col)
            )

        # Guarda linha calculada
        partial_result.append((row, new_row))

    # Envia resultado parcial
    result_queue.put(partial_result)


# ============================================================
# VERSÃO PARALELA
# ============================================================

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

def game_of_life_parallel(grid,
                          generations,
                          workers):

    rows = len(grid)
    cols = len(grid[0])

    #Evita criar mais workers do que linhas
    workers = min(workers, rows)

    current_grid = [row[:] for row in grid]

    # ============================================================
    # EXECUÇÃO DAS GERAÇÕES
    # ============================================================

    for _ in range(generations):

        # Queue usada para recolha de resultados
        result_queue = multiprocessing.Queue()

        processes = []

        #Divisão equilibrada das linhas
        base_rows = rows // workers
        extra_rows = rows % workers

        current_start = 0

        #Os primeiros workers recebem uma linha extra
        #caso a divisão não seja exata
        for i in range(workers):

            #Alguns workers recebem +1 linha
            rows_for_this_worker = base_rows

            if i < extra_rows:
                rows_for_this_worker += 1

            start_row = current_start
            end_row = start_row + rows_for_this_worker

            # Criação do processo responsável
            # pela região atribuída
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

            current_start = end_row

        # Nova grelha da geração seguinte
        new_grid = [[0 for _ in range(cols)] for _ in range(rows)]

        # Recolha de resultados
        # Grelha reconstruída a partir dos
        # resultados enviados pelos workers

        for _ in range(workers):

            partial_result = result_queue.get()

            for row_index, row_data in partial_result:
                new_grid[row_index] = row_data

        # Espera pelos workers - sincronização dos processos
        for process in processes:
            process.join()

        #Apenas após todos os workers terminarem
        #a nova geração é validada
        current_grid = new_grid

    return current_grid