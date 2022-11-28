from amplpy import AMPL, Environment
import os
import pandas as pd
import numpy as np
from multiprocessing import Pool

# this function returns the data from a model using ampl interpreter
## this is easier to do that recreate a reader
def extractData(model_name, data_name):
    # create a ampl instance with given model and data
    ampl = AMPL(Environment('./ampl_mswin64'))
    ampl.read(model_name)
    ampl.readData(data_name)
    #retireve values from ampl instance
    cli = int(ampl.getParameter('cli').value())
    loc = int(ampl.getParameter('loc').value())
    FC = ampl.getParameter('FC').getValues().toPandas()["FC"]
    ICap = ampl.getParameter('ICap').getValues().toPandas()["ICap"]
    dem = ampl.getParameter('dem').getValues().toPandas()["dem"]
    TC = ampl.getParameter('TC').getValues().toPandas()
    # return values from ampl
    return cli, loc, FC, ICap, dem, TC

# this is the solver wrapper that calls ampl with a given model, data and the solution to optimize
def solveAlter(model_name, data_name, openFacilities = []):
     # create a ampl instance with given model and data
    ampl = AMPL(Environment('./ampl_mswin64'))
    ampl.read(model_name)
    # options to reduce output and limit threads of gurobi to one to solve multiple problems in parallel
    ampl.setOption("solver_msg", 0)
    ampl.setOption("gurobi_options", 'threads=1')
    ampl.read_data(data_name)
    # set the facilities parameter in the model 
    facilities = pd.DataFrame(np.array([openFacilities]).transpose(), columns=["x"])
    facilities = facilities.set_index(facilities.index + 1)
    x = ampl.get_parameter('x')
    x.set_values(facilities)
    # solve the problem with ampl
    ampl.solve()
    # get cost of the solution
    totalcost = ampl.get_objective('Total_Cost').value()
    # if given solution is infeasible set the cost to inf/highNumber
    if "infeasible" in ampl.get_objective('Total_Cost').result():
        totalcost = float('inf')
    # return the cost of the solution
    return totalcost

# guard to not let this code execute when importing and multithreading, but execute when calling this especific file
# for testing purposes
if __name__ == "__main__":
    calls = [(os.path.join("example/model_param.mod"), os.path.join("processed_datasets/" + data)) for data in os.listdir("processed_datasets")]
    with Pool() as p:
        data = p.starmap(solveAlter, calls)