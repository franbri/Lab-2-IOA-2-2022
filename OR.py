import sys
from math import ceil

# this program purpose is to read OR library problems from txt python variables
def read_file(filename):
    file = open(filename, "r")
    nloc, ncus = file.readline().strip().split(" ")
    loc = int(nloc)
    cli = int(ncus)

    ICap = []
    FC = []
    for index in range(loc):
        temp = file.readline().strip().split(" ")
        ICap.append(int(temp[0]))
        FC.append(float(temp[1]))

    iter_temp = ceil(loc/7)
    dem = []
    TC = []
    for index in range(cli):
        temp = file.readline().strip().split(" ")
        dem.append(int(temp[0]))
        temp_TC = []
        for indexCustomerLoc in range(iter_temp):
            temp_TC = temp_TC + list(map(float, file.readline().strip().split(" ")))
        TC.append(temp_TC)

    return cli, loc, FC, ICap, dem, TC

# guard to not execute this when importing
if __name__ == "__main__":
    read_file(sys.argv[1])
