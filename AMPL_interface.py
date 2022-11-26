from amplpy import AMPL, Environment
import os
import pandas as pd
import numpy as np
from multiprocessing import Pool


def solve(model_name, data_name, facilities):
    ampl = AMPL(Environment('./ampl_mswin64'))

    ampl.read(model_name)
    #ampl.eval("option threads 2;")
    ampl.read_data(data_name)

    x = ampl.get_parameter('x')

    x.set_values(facilities)


    ampl.solve()

if __name__ == "__main__":
    solution = pd.DataFrame([np.arange(50), np.ones(50)])

    with Pool(processes=2) as p:
       data = p.starmap(solve, [(os.path.join("example/1_CFLP_model.mod"), os.path.join("example/CAP134_AMPL.dat"), solution), 
       (os.path.join("example/1_CFLP_model.mod"), os.path.join("example/1_CFLP_Data.dat"), solution), 
       (os.path.join("example/1_CFLP_model.mod"), os.path.join("example/CAP134_AMPL.dat"), solution)])


#def run(model, data):
#    runfile = open("AMPL_run.run", "w")