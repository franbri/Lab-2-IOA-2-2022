from amplpy import AMPL, Environment
import os
from multiprocessing import Pool


def solve(model_name, data_name):
    ampl = AMPL(Environment('./ampl_mswin64'))

    ampl.read(model_name)
    ampl.read_data(data_name)

    ampl.solve()

if __name__ == "__main__":
    with Pool(processes=2) as p:
       data = p.starmap(solve, [(os.path.join("example/1_CFLP_model.mod"), os.path.join("example/CAP134_AMPL.dat")), 
       (os.path.join("example/1_CFLP_model.mod"), os.path.join("example/1_CFLP_Data.dat")), 
       (os.path.join("example/1_CFLP_model.mod"), os.path.join("example/CAP134_AMPL.dat"))])


#def run(model, data):
#    runfile = open("AMPL_run.run", "w")