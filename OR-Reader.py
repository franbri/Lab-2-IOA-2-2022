import sys
from math import ceil

def read_file(filename):
    file = open(filename, "r")
    nloc, ncus = file.readline().strip().split(" ")
    loc = int(nloc)
    cli = int(ncus)
    # print(loc, cli)

    ICap = []
    FC = []
    for index in range(loc):
        temp = file.readline().strip().split(" ")
        ICap.append(int(temp[0]))
        FC.append(float(temp[1]))
    # print(ICap)
    # print(FC)

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
    # print(dem)
    # print(TC)

    return cli, loc, FC, ICap, dem, TC

if __name__ == "__main__":
    read_file(sys.argv[1])
