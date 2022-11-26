from OR import read_file

cli, loc, FC, ICap, dem, TC = read_file('cap41.txt')

with open('cap41.txt', 'r') as txt, open('cap41.dat', 'w') as dat:
    dimensiones = txt.readline().split()
    
    #clientes y centros
    dat.write("param loc := " + dimensiones[0] +';\n')
    dat.write("param cli := " + dimensiones[1] +';\n')

    #costos de instalacion
    dat.write("param FC := ")
    for idC, C in enumerate(FC):
        if(idC+1 != len(FC)):
            dat.write(str(idC+1) + ' ' + str(C) + '\t')
        else:
            dat.write(str(idC+1) + ' ' + str(C))
    dat.write(';\n\n')

    #Capacidad de cada centro
    dat.write("param ICap := ")
    for idC, C in enumerate(ICap):
        if(idC+1 != len(ICap)):
            dat.write(str(idC+1) + ' ' + str(C) + '\t')
        else:
            dat.write(str(idC+1) + ' ' + str(C))
    dat.write(';\n\n')

    dat.write("param dem := ")
    for idC, C in enumerate(dem):
        if(idC+1 != len(dem)):
            dat.write(str(idC+1) + ' ' + str(C) + '\t')
        else:
            dat.write(str(idC+1) + ' ' + str(C))
    dat.write(';\n\n')

    dat.write("param TC := ")
    for i in range(1, len(TC) + 1):
        if(i != len(TC)):
            dat.write(str(i) + ' ')
        else:
            dat.write(str(i) + ' :=')
    dat.write('\n\n')

    for list in TC:
        dat.write(str(TC.index(list) + 1) + '\t')
        for element in list:
            dat.write(str(element) + ' ')
        dat.write('\n')

    txt.close()
    dat.close()