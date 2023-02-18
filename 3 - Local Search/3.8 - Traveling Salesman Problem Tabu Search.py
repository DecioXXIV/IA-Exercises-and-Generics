import random
import numpy as np

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# Traveling Salesman Problem: we got "n" cities and a Traveling Salesman, who has to visit each city only once and go back to the starting city.
# Every move between two cities implies a cost, and we want this cost to be the lowest possible.

# Each state is represented by a sequence of indexes (each index is related to a city), representing the cycle travelled by the salesman.
# Each state has its own neighborhood and each neighbor is obtained by "swapping" two cities into the sequence.
# Each state is then evaluated by a function that calculates the total cost "payed" by the Traveling Salesman: obviously, the goal is to minimize this cost.

# FUNCTION: we have the Space of States' information as a List of Adiacency Lists.
# This function translates the List of Adiacency Lists into an Adiacency Matrix.
def build_graph(graph_infos):
    graph_nodes = list(graph_infos.keys())
    N = len(graph_nodes)
    graph_arcs = np.zeros((N,N), np.int)

    for node in graph_nodes:
        node_idx = graph_nodes.index(node)
        for neighbor in graph_infos[node]:
            neighbor_idx = graph_nodes.index(neighbor[0])
            cost = neighbor[1]
            graph_arcs[node_idx][neighbor_idx] = cost
    
    return graph_nodes, graph_arcs


# FUNCTION: Evaluating Function
def eval_function(current, graph_arcs):
    total_cost = 0

    for idx in range(0,len(current)-1):
        current_city_idx = current[idx]
        next_city_idx = current[idx+1]
        total_cost += graph_arcs[current_city_idx][next_city_idx]

# Last Distance = Distance "Last City-First City" 
    current_city_idx = current[len(current)-1]
    next_city_idx = current[0]
    total_cost += graph_arcs[current_city_idx][next_city_idx]

    return total_cost


# FUNCTION: generates the current state's neighborhood.
# It's ordered by Increasing "total_distance": the first neighbor will be chosen cause it is the best "next_state"
def generate_neighbors(current, graph_arcs):
    neighbors_list = list()
    N = len(current)

    for i in range(0, N-1):
        for j in range(i+1, N):
            neighbor = np.copy(current).tolist()

            temp = neighbor[i]
            neighbor[i] = neighbor[j]
            neighbor[j] = temp

            neighbor_eval = eval_function(neighbor, graph_arcs)

            neighbors_list.append((neighbor, neighbor_eval, (current[i], current[j])))
# Observation, a "neighbor_list" item:
    # - item[0] = neighbor -> the new state, generated by "swapping" two cities in the ordered sequence.
    # - item[1] = neighbor_eval -> the new state evaluation.
    # - item[2][0] and item[2][1] = swapped cities, the tuple represents "the move".

    neighbors_list.sort(key=lambda x: x[1])

    return neighbors_list

# FUNCTION: executes the "Tabu Test" on the chosen move.
def tabu_test(move, tabu_list):
    a, b = move[2]
    if ((a, b) in tabu_list or (b, a) in tabu_list):
        return True
    else:
        return False


# *** ********************* ***
# *** TABU SEARCH FUNCTIONS ***
# *** ********************* ***

def tabu_search(graph_nodes, graph_arcs, TABU_TENURE):
    print("*** **************************************** ***")
    print("*** Tabu Search x Traveling Salesman Problem ***")
    print("*** **************************************** ***\n")

    print("Cities: " + str(graph_nodes))
    print("Distances: ")
    print(graph_arcs)
    print()

# Starting State Inizialization
    N = len(graph_nodes)
    current = list(range(0,N))
    random.shuffle(current)

    current_eval = eval_function(current, graph_arcs)

# Best Inizialization
    best = current
    best_eval = current_eval

# Tabu Search Cycle
    tabu_list = dict()
    iteration = 1

    while iteration-1 < MAX_ITERATIONS:
        
        if iteration == 1:
            print("ITERATION = %d" % iteration)
            
            current_best_cities = list()
            for index in best:
                current_best_cities.append(graph_nodes[index])

            print("Starting State = %s" % str(current_best_cities))
            print("Starting Cost = %d\n" % best_eval)

        neighbors_full_list = generate_neighbors(current, graph_arcs)
        neighbors_list = list()

        for neighbor in neighbors_full_list:
            is_tabu = tabu_test(neighbor, tabu_list)
            if is_tabu == False:
                neighbors_list.append(neighbor)
        
        current = neighbors_list[0][0]
        current_eval = eval_function(current, graph_arcs)

        if current_eval < best_eval:
            best = current
            best_eval = current_eval

            current_best_cities = list()
            for index in best:
                current_best_cities.append(graph_nodes[index])

            print("New Best Found at Iteration %d" % iteration)
            print("New Best = %s" % str(current_best_cities))
            print("Cost = %d\n" % best_eval)
        
        for move in list(tabu_list):
            tabu_list[move] -= 1
            if tabu_list[move] == 0:
                tabu_list.pop(move)
        
        move = neighbors_list[0][2]
        tabu_list[move] = TABU_TENURE

        iteration += 1
    
    final_cities = list()
    for index in best:
        final_cities.append(graph_nodes[index])
    
    print("*** ITERATION %d: SEARCH IS OVER! ***" % iteration)
    print("Final State = %s" % str(final_cities))
    print("Final Cost = %d\n" % best_eval)


def tabu_search_aspiration_criterion(graph_nodes, graph_arcs, TABU_TENURE):
    print("*** **************************************************************** ***")
    print("*** Tabu Search w/ Aspiration Criterion x Traveling Salesman Problem ***")
    print("*** **************************************************************** ***\n")

    print("Cities: " + str(graph_nodes))
    print("Distances: ")
    print(graph_arcs)
    print()

# Starting State Inizialization
    N = len(graph_nodes)
    current = list(range(0,N))
    random.shuffle(current)

    current_eval = eval_function(current, graph_arcs)

# Best Inizialization
    best = current
    best_eval = current_eval

# Tabu Search Cycle
    tabu_list = dict()
    iteration = 1

    while iteration-1 < MAX_ITERATIONS:
        
        if iteration == 1:
            print("ITERATION = %d" % iteration)
        
            current_best_cities = list()
            for index in best:
                current_best_cities.append(graph_nodes[index])

            print("Starting State = %s" % str(current_best_cities))
            print("Starting Cost = %d" % best_eval)

        neighbors_full_list = generate_neighbors(current, graph_arcs)

        next = neighbors_full_list[0][0]
        next_eval = eval_function(next, graph_arcs)

        if next_eval < best_eval:
            best = next
            best_eval = next_eval

            current = next
            current_eval = next_eval

            current_best_cities = list()
            for index in best:
                current_best_cities.append(graph_nodes[index])

            print("New Best Found at Iteration %d" % iteration)
            print("New Best = %s" % str(current_best_cities))
            print("Cost = %d\n" % best_eval)

        for move in tabu_list.copy():
            tabu_list[move] -= 1
            if tabu_list[move] == 0:
                tabu_list.pop(move)
        
        move = neighbors_full_list[0][2]
        tabu_list[move] = TABU_TENURE

        iteration += 1
    
    final_cities = list()
    for index in best:
        final_cities.append(graph_nodes[index])
    
    print("*** ITERATION %d: SEARCH IS OVER! ***" % iteration)
    print("Final State = %s" % str(final_cities))
    print("Final Cost = %d\n" % best_eval)
        
# *** **** ***
# *** MAIN ***
# *** **** ***

# Parameters Settings
TABU_TENURE = 3
MAX_ITERATIONS = 25

# Search State Settings
graph_infos = dict()
graph_infos['Milano'] = [('Torino',126),('Genova',119),('Bologna',201),('Firenze',250),('Roma',478),('Napoli',658),('Palermo',887)]
graph_infos['Torino'] = [('Milano',126),('Genova',123),('Bologna',296),('Firenze',318),('Roma',525),('Napoli',712),('Palermo',906)]
graph_infos['Genova'] = [('Milano',119),('Torino',123),('Bologna',192),('Firenze',199),('Roma',402),('Napoli',589),('Palermo',791)]
graph_infos['Bologna'] = [('Milano',201),('Torino',296),('Genova',192),('Firenze',81),('Roma',304),('Napoli',471),('Palermo',729)]
graph_infos['Firenze'] = [('Milano',250),('Torino',318),('Genova',199),('Bologna',81),('Roma',232),('Napoli',408),('Palermo',653)]
graph_infos['Roma'] = [('Milano',478),('Torino',525),('Genova',402),('Bologna',304),('Firenze',232),('Napoli',188),('Palermo',426)]
graph_infos['Napoli'] = [('Milano',658),('Torino',712),('Genova',589),('Bologna',471),('Firenze',408),('Roma',188),('Palermo',313)]
graph_infos['Palermo'] = [('Milano',887),('Torino',906),('Genova',791),('Bologna',729),('Firenze',653),('Roma',426),('Napoli',313)]

graph_nodes, graph_arcs = build_graph(graph_infos)

tabu_search(graph_nodes, graph_arcs, TABU_TENURE)
tabu_search_aspiration_criterion(graph_nodes, graph_arcs, TABU_TENURE)