from OR import read_file
import numpy as np
import pandas as pd
from AMPL_interface import solveAlter
import os
from multiprocessing import Pool


def initSolution(filename):
    cli, loc, FC, ICap, dem, TC = read_file('datasets/' + filename)

    mincap = sum(dem)
    # si tengo tiempo aca pongo una wea que busque mejores soluciones

    sol0 = np.zeros(loc).astype(int)
    sumcap = 0
    for index, cap in enumerate(ICap):
        sumcap += cap
        sol0[index] = 1
        if sumcap > mincap:
            # print("bruh")
            break
    return sol0

# tabu serach swap
#def tabu():
#    lenghtTabu = 10 #
#    refresh = 20 #iterations

def neighbors(solution):
    base = np.array(solution).reshape(len(solution)).tolist()
    solutions = np.array(base * len(base)).reshape((len(base), len(base)))
    solutions = (solutions - np.eye(len(base)))
    solutions = np.abs(solutions).astype(int)
    return solutions



def main(problemName, iterations):
    solution = initSolution(problemName + ".txt")
    cost = solveAlter(os.path.join("example/model_param.mod"), os.path.join("processed_datasets/" + problemName + ".dat"), solution)
    neighborhood = neighbors(solution)
    #print(neighborhood)
    #calls = [(os.path.join("example/model_param.mod"), os.path.join("processed_datasets/" + problemName + ".dat"), solution) for solution in neighborhood]


#    with Pool(processes=12) as p:
#        data = p.starmap(solveAlter, calls)

#    print(data)

    #for iteration in range(iterations):
    #    [0,1,0,0,0]
    #print(cost, solution)

if __name__ == "__main__":
    main("cap91", 5)
