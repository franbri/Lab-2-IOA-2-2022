import numpy as np
import math
from AMPL_interface import solve, extractData
import os
from multiprocessing import Pool

# this function returns a set of posible solutions utilizing a custom method to create minimal number of open centers
def initSolution(modelFile, problemFile):
    # get data from the especific instance of the problem
    cli, loc, FC, ICap, dem, TC = extractData(os.path.join("models/" + modelFile), os.path.join("processed_datasets/" + problemFile))

    # number of minimum centers to open satisfying all clients
    howmany = math.ceil(sum(dem)/min(ICap))
    # create a list of ones representing allthe open centers
    solution = np.array([1] * howmany)
    # resize the list to complete all open an closed centers
    solution.resize((1, loc))
    # list of possible solutions
    out = np.empty((0, loc), int)
    # add the basic solution to the list
    out = np.append(out, solution, axis=0)
    # randomize the first solution to get variety
    # randomize to a total of half the size of locationss
    for x in range(math.ceil(loc/2)):
        np.random.shuffle(solution[0])
        out = np.append(out, solution, axis=0)
    # return list of possible solutions
    return out

# function to find all neighbors for a given solution
def neighbors(solution):
    # convert solution base to a simple list
    base = np.array(solution).reshape(len(solution)).tolist()
    # create a matrix with all solutions
    solutions = np.array(base * len(base)).reshape((len(base), len(base)))
    # substract identity matrix from the solutions matrix
    solutions = (solutions - np.eye(len(base)))
    # absolute to change -1 to 1
    solutions = np.abs(solutions).astype(int)
    return solutions

# main loop of the tabu search heuristic for a given model and data, also takes the number of iterations
def tabu(modelFile, problemFile, iterations):
    # get solutions to the problem
    neighborhood = initSolution(modelFile, problemFile)
    # calculate the cost of the solutions
    calls = [(os.path.join("models/" + modelFile), os.path.join("processed_datasets/" + problemFile), solution) for solution in neighborhood]
    with Pool(processes=12) as p:
        cost = p.starmap(solve, calls)
    # get an sorting index
    cost = np.array(cost)
    order = np.argsort(cost).astype(int)
    # sort costs and neighborhood based in the best solutions
    cost = cost[order]
    neighborhood = neighborhood[order]
    # initialize solution as best solution of initial ser
    solution = neighborhood[0]
    # set best solution to the only solution
    bestSolution = solution
    # best cost is the cost of the solution
    bestCost = cost[0]
    # all costs is a list that show the progress of the best solution in the algorithm
    allCosts = [bestCost]
    # tabu list of solutions that will not be visited again
    tabu = [tuple(bestSolution)]

    # main loop
    for iter in range(iterations):
        # generate new neighborhood from the actual solution, not necessarily the best
        neighborhood = neighbors(solution)
        # list of solutions to delete from the neighborhood that are in the tabu list
        to_delete = []
        for sol in neighborhood:
            if tuple(sol) in tabu:
                to_delete.append(tuple(sol))
        # actual deletion of solutions from neighborhood
        neighborhood = np.delete(neighborhood, to_delete, 0)
        # solve the neighborhood of solutions to get the costs
        calls = [(os.path.join("models/" + modelFile), os.path.join("processed_datasets/" + problemFile), solution) for solution in neighborhood]
        with Pool() as p:
            cost = p.starmap(solve, calls)
        # sort solutions based on cost
        cost = np.array(cost)
        order = np.argsort(cost).astype(int)
        cost = cost[order]
        neighborhood = neighborhood[order]
        # adding infeasible solutions to tabu list
        infeasible = np.where(cost == float('inf'))
        for index in infeasible:
            to_delete.append(tuple(neighborhood[index]))
        # check if new best
        for index in range(len(cost)):
            # update best
            if cost[index] < bestCost:
                bestSolution = neighborhood[index]
                bestCost = cost[index]
            # select new solution to next iteration
            if tuple(neighborhood[index]) not in tabu:
                solution = neighborhood[index]
                tabu.append(tuple(solution))
                break
        # add cost to metrics list
        allCosts.append(cost[index])
        # remove from tabu list when list is full
        if len(tabu) > len(bestSolution)*2:
            print("deleted from tabu")
            tabu = tabu[1:]
        # feedback prints, to show user what the program is doing
        #print(allCosts)
        #print("tamaño lista tabu", len(tabu))
        #print(solution)
        print("iteracion numero:", iter)
        #print("mejor solucion", bestSolution)
        #print(bestSolution)
        #print(bestCost)
        #print(cost)
        #print(neighborhood)
    return bestSolution, bestCost, allCosts

if __name__ == "__main__":
    tabu("model_param.mod", "capa.dat", 10)
