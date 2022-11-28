from amplpy import AMPL, Environment
import os
import sys
import pandas as pd
import numpy as np
from multiprocessing import Pool

def mute():
    sys.stdout = open(os.devnull, 'w')

def extractData(model_name, data_name):
    ampl = AMPL(Environment('./ampl_mswin64'))
    ampl.read(model_name)
    #ampl.eval("option gurobi_options 'threads=2';")
    ampl.read_data(data_name)
    cli = int(ampl.get_parameter('cli').value())
    loc = int(ampl.get_parameter('loc').value())
    FC = ampl.get_parameter('FC').get_values().to_pandas()["FC"]
    ICap = ampl.get_parameter('ICap').get_values().to_pandas()["ICap"]
    dem = ampl.get_parameter('dem').get_values().to_pandas()["dem"]
    TC = ampl.get_parameter('TC').get_values().to_pandas()
    return cli, loc, FC, ICap, dem, TC


def solve(model_name, data_name):
    ampl = AMPL(Environment('./ampl_mswin64'))
    ampl.read(model_name)
    #ampl.eval("option gurobi_options 'threads=2';")
    ampl.read_data(data_name)
    #x = ampl.get_parameter('x')
    #x.set_values(facilities)
    ampl.solve()
    try:
        totalcost = ampl.get_objective('Total_Cost').value()
    except:
        totalcost = 0
        print("bruh")
        return totalcost
    return totalcost

def solveAlter(model_name, data_name, openFacilities = []):
    ampl = AMPL(Environment('./ampl_mswin64'))
    ampl.read(model_name)
    #ampl.eval("option gurobi_options 'threads=2';")
    ampl.setOption("solver_msg", 0)
    ampl.setOption("gurobi_options", 'threads=1')
    ampl.read_data(data_name)
    loc = int(ampl.get_parameter('loc').value())
    facilities = openFacilities
    if len(facilities) != loc:
        facilities = pd.DataFrame(np.array([np.ones(loc).astype(int)]).transpose(), columns=["x"])
        facilities = facilities.set_index(facilities.index + 1)
        return 0
    else:
        #print(np.array([facilities]).transpose())
        facilities = pd.DataFrame(np.array([facilities]).transpose(), columns=["x"])
        facilities = facilities.set_index(facilities.index + 1)
    
    x = ampl.get_parameter('x')
    x.set_values(facilities)
    ampl.solve()

    totalcost = ampl.get_objective('Total_Cost').value()
    if "infeasible" in ampl.get_objective('Total_Cost').result():
        #print("\n ampl status", ampl.get_objective('Total_Cost').result(), "\n")
        #print("BRUHHHHHHHHHH")
        totalcost = float('inf')

    return totalcost


#if __name__ != "__main__":
#    mute()

if __name__ == "__main__":
    # solution = pd.DataFrame([np.arange(50), np.ones(50)])

    calls = [(os.path.join("example/model_param.mod"), os.path.join("processed_datasets/" + data)) for data in os.listdir("processed_datasets")]

    with Pool(processes=12) as p:
        data = p.starmap(solveAlter, calls)

#def run(model, data):
#    runfile = open("AMPL_run.run", "w")