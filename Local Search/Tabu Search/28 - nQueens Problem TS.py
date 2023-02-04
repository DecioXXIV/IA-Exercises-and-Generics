import random
import numpy as np

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# nQueens Problem: we got a Chessboard ("N" rows and "N" columns) and we want to place "N" Queens on it in order to have none of them putting the others in check.
# We decide to exploit the "Tabu Search" Algorithm.

# To simplify the state definition and the problem itself, we decide to place only one Queen for each column of the board.
# In this way we can easily represent the board with a vector of dimension "N": each index stands for a column index and each value stands for a row index.
# For example, if we have: vector[2] = 5, it means that we have a Queen on the (5,2) cell.

# Each state has his own neighborhood, obtained imposing the "swap" between two columns of the board.
# If we have "N" columns, the neighborhood's cardinality is equal to: N(N-1)/2.
# Each state is evaluated in terms fo the number of conflicts between the queens: we want to reach "0" for this value.

def tweak(solution):
    solution_copy = np.copy(solution)
# We randomely choose two separate column indexes
    x = random.randint(0, N-1)
    y = random.randint(0, N-1)
    while x == y:
        y = random.randint(0, N-1)
    
# Column Swap
    temp = solution_copy[y]
    solution_copy[y] = solution_copy[x]
    solution_copy[x] = temp

    return solution_copy


def get_starting_state(solution):
    for c in range(0, N):
        solution = tweak(solution)
    return solution


def generate_neighbors(state):
    neighbors_list = list()
    t = len(state)

    for i in range(0, t-1):
        for j in range(i+1, t):
# Observation, double "for":
    # i = 0 -> j = [1, ..., t-1]
    # i = 1 -> j = [2, ..., t-1]
    # ...
            buffer = np.copy(state)
            temp = buffer[i]
            buffer[i] = buffer[j]
            buffer[j] = temp
            neighbor_eval = eval_function(buffer)
            neighbors_list.append((buffer, neighbor_eval, (state[i], state[j])))
# Observation, a "neighbors_list" item:
    # - item[0] = neighbor_state
    # - item[1] = neighbor_eval
    # - item[2][0] = first column in the swap
    # - item[2][1] = second column in the swap

# The "neighbors_list" gets ordered by Decreasing "neighbor_eval" -> the first item has the best evaluation.
    neighbors_list.sort(key=lambda x: x[1])
    return neighbors_list


def tabu_test(move, tabu_list):
    a, b = move[2]
    if ((a,b) in tabu_list or (b,a) in tabu_list):
        return True
    else:
        return False


def eval_function(state):
# Chessboard Definition
    board = [[0] * N for i in range(N)]
# Placing the Queens on the Chessboard
    for i in range(0, N):
        board[state[i]][i] = 'Q'

# Possible Moves on the Chessboard: having one Queen on each column/row, we need to count only the conflicts on the diagonals
    dx = [1,1,-1,-1]
    dy = [1,-1,1,-1]
# Observations:
    # - dx == 1, dy == 1: "Bottom-Right" move
    # - dx == 1, dy == -1: "Bottom-Left" move
    # - dx == -1, dy == 1: "Top-Right" move
    # - dx == -1, dy == -1: "Top-Left" move

    conflicts = 0

    for i in range(0, N):
        x = state[i]
        y = i

# Conflicts Count
        for j in range(0,4):
            temp_x = x
            temp_y = y
            while True:
                temp_x += dx[j]
                temp_y += dy[j]

                if (temp_x < 0 or temp_x >= N) or (temp_y < 0 or temp_y >= N):
                    break

                if board[temp_x][temp_y] == 'Q':
                    conflicts += 1
    
    return conflicts


def print_chessboard(state):
# Chessboard Definition
    board = [[0] * N for i in range(N)]
# Placing the Queens on the Chessboard
    for i in range(0, N):
        board[state[i]][i] = 'Q'

    for x in range(0, N):
        for y in range(0, N):
            if board[x][y] == 'Q':
                print("Q    ", end="")
            else:
                print(".    ", end="")
        print("\n")


def tabu_search(tabu_tenure):
    print("*** ***************** ***")
    print("*** %d QUEENS PROBLEM ***" % N)
    print("*** ***************** ***\n")

# Initial State
    current = get_starting_state(range(0, N))
    current_eval = eval_function(current)

# "Best" Initialization
    best = current
    best_eval = current_eval

    tabu_list = dict()

    print("STARTING STATE: Conflicts = %d" % best_eval)
    print_chessboard(best)

    iterations = 1

    while(iterations < MAX_ITERATIONS and best_eval > 0):
        print("ITERATION: %d" % iterations)
        print("Actual Best Evaluation: %d" % best_eval)

        neighbors_list_full = generate_neighbors(current)
        neighbors_list = list()
        
        for neighbor in neighbors_list_full:
            is_tabu = tabu_test(neighbor, tabu_list)
            if is_tabu == False:
                neighbors_list.append(neighbor)

        #for idx in range(0,len(neighbors_list)):
            #neighbor = neighbors_list[idx]
            #is_tabu = tabu_test(neighbor, tabu_list)
            #if is_tabu:
                #neighbors_list.pop(idx)

# Observation, a "neighbors_list" item:
    # - item[0] = neighbor_state
    # - item[1] = neighbor_eval
    # - item[2][0] = first column in the swap
    # - item[2][1] = second column in the swap

        next = neighbors_list[0][0]
        next_eval = eval_function(next)

        delta_eval = best_eval - next_eval
        if delta_eval > 0:
            best = next
            best_eval = next_eval
        
        current = next
        current_eval = next_eval

        for move in tabu_list:
            tabu_list[move] -= 1
            if tabu_list[move] == 0:
                tabu_list.pop(move)
        
        next_move = neighbors_list[0][2]
        tabu_list[next_move] = tabu_tenure

        iterations += 1
    
    print("\n*** SEARCH IS OVER! ***")
    print("*** FINAL STATE: Conflicts = %d" % best_eval)
    print_chessboard(best)


# *** **** ***
# *** MAIN ***
# *** **** ***

# Parameters Settings
N = 8 # "Classic" Chessboard
MAX_ITERATIONS = 100
TABU_TENURE = 5

tabu_search(TABU_TENURE)