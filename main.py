from OR import read_file
import numpy as np
import pandas as pd
import math
from AMPL_interface import solveAlter, extractData
import os
from multiprocessing import Pool


def betterinitSolution(problemName):
    # cli, loc, FC, ICap, dem, TC = read_file('datasets/' + filename)
    cli, loc, FC, ICap, dem, TC = extractData(os.path.join("example/model_param.mod"), os.path.join("processed_datasets/" + problemName + ".dat"))

    print(ICap)
    if max(dem) > max(ICap):
        print("the problem is infeasible")
        exit()

    howmany = math.ceil(sum(dem)/min(ICap))
    solution = np.array([1] * howmany)
    solution.resize((1, loc))
    out = np.empty((0, loc), int)
    out = np.append(out, solution, axis=0)
    for x in range(math.ceil(loc/2)):
        np.random.shuffle(solution[0])
        out = np.append(out, solution, axis=0)
    return out

def initSolution(filename):
    cli, loc, FC, ICap, dem, TC = read_file('datasets/' + filename)

    mincap = sum(dem)
    # si tengo tiempo aca pongo una wea que busque mejores soluciones

    if max(dem) > max(ICap):
        print("the problem is infeasible")
        exit()

    sol0 = np.zeros(loc).astype(int)
    sumcap = 0
    for index, cap in enumerate(ICap):
        sumcap += cap
        sol0[index] = 1
        if sumcap > mincap:
            # print("bruh")
            break
    return sol0

def neighbors(solution):
    base = np.array(solution).reshape(len(solution)).tolist()
    solutions = np.array(base * len(base)).reshape((len(base), len(base)))
    solutions = (solutions - np.eye(len(base)))
    solutions = np.abs(solutions).astype(int)
    return solutions

def main(problemName, iterations):
    neighborhood = betterinitSolution(problemName)

    calls = [(os.path.join("example/model_param.mod"), os.path.join("processed_datasets/" + problemName + ".dat"), solution) for solution in neighborhood]
    with Pool(processes=12) as p:
        cost = p.starmap(solveAlter, calls)


    cost = np.array(cost)
    order = np.argsort(cost).astype(int)

    cost = cost[order]
    neighborhood = neighborhood[order]

    solution = neighborhood[0]
    bestSolution = solution
    bestCost = cost[0]

    tabu = [tuple(bestSolution)]

    # main loop
    for iter in range(iterations):
        neighborhood = neighbors(solution)

        calls = [(os.path.join("example/model_param.mod"), os.path.join("processed_datasets/" + problemName + ".dat"), solution) for solution in neighborhood]
        with Pool() as p:
            cost = p.starmap(solveAlter, calls)

        cost = np.array(cost)
        order = np.argsort(cost).astype(int)

        cost = cost[order]
        neighborhood = neighborhood[order]

        for index in range(len(cost)):
            if cost[index] < bestCost:
                bestSolution = neighborhood[index]
                bestCost = cost[index]

            if tuple(neighborhood[index]) not in tabu:
                solution = neighborhood[index]
                tabu.append(tuple(solution))
                break
        

        print(bestSolution)
        print(bestCost)
        print(cost)
        print(neighborhood)


    #for iteration in range(iterations):
    #    [0,1,0,0,0]
    #print(cost, solution)

if __name__ == "__main__":
    main("cap134", 10)
