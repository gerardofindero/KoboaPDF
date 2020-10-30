import pandas as pd
from Consumo    import calc_consumo
from Condiciones import condicionesCluster


def clustertv(Excel,Nocircuito):
    print("Cluster de TV")
    Aparatos_C = pd.DataFrame(index=['TV','Decodificador1','Decodificador2','Regulador1','Regulador2','NoBreak','Modem','Repetidor','Antena','Sonido','Bocinas','Surround', 'Consola1','Consola2']
                              ,columns=['Marca','Consumo','Nominal','Tolerancia', 'Pulgadas','Numero'])

    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("cluster_tv", case=False)]
    Equipos= Circuito[InfoEquipos]

    indx=0
    for i in Equipos:
        if i == 1:
            if indx == 1:
                NomAparato='decodificador1'
                #Aparatos_C.loc['Decodificador1','Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Decodificador1','Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Decodificador1','Marca']   = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Decodificador1', 'Numero'] = 1

            if indx == 2:
                NomAparato='reguladortv1'
                #Aparatos_C.loc['Regulador1', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Regulador1', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Regulador1', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Regulador1', 'Numero'] =1

            if indx == 3:
                NomAparato = 'tv1'
                #Aparatos_C.loc['TV', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['TV', 'Consumo'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['TV', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['TV', 'Nominal'] = InfoDeco.filter(regex='nominal')[0]
                Aparatos_C.loc['TV', 'Tolerancia'] = InfoDeco.filter(regex='tolerancia')[0]
                Aparatos_C.loc['TV', 'Pulgadas'] = InfoDeco.filter(regex='size')[0]
                Aparatos_C.loc['TV', 'Numero'] = 1

            if indx == 4:
                NomAparato = 'nobreak'
                #Aparatos_C.loc['NoBreak', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['NoBreak', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['NoBreak', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['NoBreak', 'Numero'] = 1

            if indx == 5:
                NomAparato = 'modem'
                #Aparatos_C.loc['Modem', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Modem', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Modem', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Modem', 'Numero'] = 1

            if indx == 6:
                NomAparato = 'repetidortv'
                #Aparatos_C.loc['Repetidor', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Repetidor', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Repetidor', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Repetidor', 'Numero'] = 1

            if indx == 7:
                NomAparato = 'sonidotv'
                #Aparatos_C.loc['Sonido', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Sonido', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Sonido', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Sonido', 'Numero'] = 1

            if indx == 8:
                NomAparato = 'decodificador2'
                #Aparatos_C.loc['Decodificador2', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Decodificador2', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                if InfoDeco.filter(regex='marca')[0] == 'otro':
                    Aparatos_C.loc['Decodificador2', 'Marca']   = InfoDeco.filter(regex='otra')[0]
                else:
                    Aparatos_C.loc['Decodificador2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Decodificador2', 'Numero'] = 1

            if indx == 9:
                NomAparato = 'reguladortv2'
                #Aparatos_C.loc['Regulador2', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Regulador2', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Regulador2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Regulador2', 'Numero'] = 1

            if indx == 10:
                NomAparato = 'bocinas'
                #Aparatos_C.loc['Bocinas', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Bocinas', 'Consumo'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Bocinas', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Bocinas', 'Numero'] = 1

            if indx == 11:
                NomAparato = 'consola1'
                #Aparatos_C.loc['Consola1', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Consola1', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Consola1', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Consola1', 'Numero'] = 1

            if indx == 12:
                print("Otro")

            if indx == 13:
                NomAparato = 'antena'
                #Aparatos_C.loc['Antena', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Antena', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Antena', 'Marca']   = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Antena', 'Numero'] = 1

            if indx == 14:
                NomAparato = 'consola2'
                #Aparatos_C.loc['Consola2', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Consola2', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Consola2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Consola2', 'Numero'] = 1

            if indx == 15:
                NomAparato = 'surround'
                #Aparatos_C.loc['Surround', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Surround', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Surround', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Surround', 'Numero'] = 1
        indx+=1

    TotConsumo=calc_consumo(Aparatos_C)
    NumAparatos = 2
    Tolerancia = True
    Multis = 0
    Voltaje = True
    condicionesCluster(Aparatos_C,TotConsumo,NumAparatos,Tolerancia,Multis, Voltaje)
    return Aparatos_C , TotConsumo

