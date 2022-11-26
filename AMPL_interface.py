from amplpy import AMPL, Environment
import os
import pandas as pd
import numpy as np
from multiprocessing import Pool


def solve(model_name, data_name, facilities=0):
    ampl = AMPL(Environment('./ampl_mswin64'))
    ampl.read(model_name)
    #ampl.eval("option threads 2;")
    ampl.read_data(data_name)
    #x = ampl.get_parameter('x')
    #x.set_values(facilities)
    ampl.solve()

if __name__ == "__main__":
    # solution = pd.DataFrame([np.arange(50), np.ones(50)])

    calls = [(os.path.join("example/1_CFLP_model.mod"), os.path.join("processed_datasets/" + data)) for data in os.listdir("processed_datasets")]
    print(len(calls))

    with Pool(processes=12) as p:
       data = p.starmap(solve, calls)


#def run(model, data):
#    runfile = open("AMPL_run.run", "w")