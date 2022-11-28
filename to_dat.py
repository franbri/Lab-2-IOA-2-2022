from OR import read_file
import os, sys

# this function converts all OR-library cap* problems in the datasets folder, and creates a corresponding dat file in the "processed_datasets" folder
def to_dat(filename):
    cli, loc, FC, ICap, dem, TC = read_file('datasets/' + filename)
    name = filename.split('.')[0]
    with open('processed_datasets/' + name + '.dat', 'w') as dat:

        #clients and centers
        dat.write("param cli := " + str(cli) +';\n')
        dat.write("param loc := " + str(loc) +';\n')

        #Facility costs
        dat.write("param FC := ")
        for idC, C in enumerate(FC):
            if(idC+1 != len(FC)):
                dat.write(str(idC+1) + ' ' + str(C) + '\t')
            else:
                dat.write(str(idC+1) + '\t' + str(C))
        dat.write(';\n\n')

        #Facility capacity
        dat.write("param ICap := ")
        for idC, C in enumerate(ICap):
            if(idC+1 != len(ICap)):
                dat.write(str(idC+1) + ' ' + str(C) + '\t')
            else:
                dat.write(str(idC+1) + ' ' + str(C))
        dat.write(';\n\n')

        #Customer demand
        dat.write("param dem := ")
        for idC, C in enumerate(dem):
            if(idC+1 != len(dem)):
                dat.write(str(idC+1) + ' ' + str(C) + '\t')
            else:
                dat.write(str(idC+1) + ' ' + str(C))
        dat.write(';\n\n')
        #Transport Cost
        dat.write("param TC : ")
        for i in range(1, len(TC[0]) + 1):
            if(i != len(TC[0])):
                dat.write(str(i) + '\t')
            else:
                dat.write(str(i) + ' :=')
        dat.write('\n')

        for list in TC:
            dat.write('\n' + str(TC.index(list) + 1))
            for element in list:
                dat.write('\t' + str(element))
        dat.write(';\n')

        dat.close()

# guard to not execute when importing
if __name__ == "__main__":
    # if a name is given, only convert the especified file
    if (len(sys.argv) < 2):
        for filename in os.listdir("datasets"):
            to_dat(filename)
    # else convert all files in datasets folder
    else:
        to_dat(sys.argv[1])



