import pandas as pd
from Consumo    import calc_consumo , consumoEq
from Condiciones import condicionesCluster



def Lugar(lugar):
    if lugar == 'rec_ppltv_c_i':
        lugar='Recamara Principal'
    if lugar == 'sala_de_tv_pa_c_i':
        lugar='Sala de TV'
    if lugar == 'sala_de_tv_pb_c_i':
        lugar='Sala de TV planta baja'
    if lugar == 'rec_ninostv_c_i':
        lugar='Recamara niños'
    if lugar == 'rec_ninastv_c_i':
        lugar='Recamara niña'
    if lugar == 'cocinatv_c_i':
        lugar='Recamara cocina'
    if lugar == 'cuarto_de_serviciotv_c_i':
        lugar='Cuarto de servicio'

    return lugar



def clustertv(Excel,Nocircuito,NomCircuito):

    Aparatos_C = pd.DataFrame(index=['Info','TV','Decodificador1','Decodificador2','Regulador1','Regulador2','NoBreak','Modem',
                                     'Repetidor','Antena','Sonido','Bocinas','Surround', 'Consola1','Consola2','Equipoextra','Equipo Ahorro','Notas']
                              ,columns=['Marca','Consumo','Nominal','Tolerancia', 'Pulgadas','Existencia'])
    Info_C = pd.DataFrame(index=['Nombre Circuito','Ubicación', 'Notas', 'Consumo Total'],columns=['Info'])
    Info_C.loc['Nombre Circuito', 'Info'] = NomCircuito[0]

    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("clustertv", case=False)]

    EquiposCTV= Circuito[InfoEquipos]
    Equipos = EquiposCTV.filter(regex='equipos')
    indx=0
    Nominal=0
    for i in Equipos:
        if i == 1:
            if indx == 1:
            ##Decodificador
                NomAparato = 'decodificador1'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Decodificador1','Consumo'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Decodificador1', 'Existencia'] = 1
                Otro = InfoDeco.filter(regex='__marca_otro_c_i')

                if pd.isna(Otro[0]):
                    Aparatos_C.loc['Decodificador1','Marca']   = InfoDeco.filter(regex='decodificador1_marca_c_i')[0]
                else:
                    Aparatos_C.loc['Decodificador1', 'Marca'] = Otro[0]


            if indx == 2:
            ##Regulador
                NomAparato='regulador1'
                InfoDeco = Circuito.filter(regex=NomAparato)
                if not InfoDeco.empty:
                    Aparatos_C.loc['Regulador1', 'Consumo'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                    Aparatos_C.loc['Regulador1', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                    Aparatos_C.loc['Regulador1', 'Existencia'] =1


            if indx == 3:
             ##Televisión
                NomAparato = 'tv1'
                InfoDeco = Circuito.filter(regex=NomAparato)

                Aparatos_C.loc['TV', 'Consumo'] =consumoEq( InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['TV', 'Marca'] = InfoDeco.filter(regex='clustertv_tv1_c_i')[0]
                Aparatos_C.loc['TV', 'Nominal'] = InfoDeco.filter(regex='nominal')[0]
                Aparatos_C.loc['TV', 'Tolerancia'] = InfoDeco.filter(regex='tolerancia')[0]
                Aparatos_C.loc['TV', 'Pulgadas'] = InfoDeco.filter(regex='tamano')[0]
                Aparatos_C.loc['TV', 'Existencia'] = 1

            if indx == 5:
            ##Modem
                NomAparato = 'modem'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Modem', 'Consumo'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Modem', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Modem', 'Existencia'] = 1
            if indx == 6:
            ##Repetidor
                NomAparato = 'repetidor'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Repetidor', 'Consumo'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Repetidor', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Repetidor', 'Existencia'] = 1

            if indx == 4:
            ##Nobreak
                NomAparato = 'nobreak'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['NoBreak', 'Consumo'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['NoBreak', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Nobreak', 'Factor de potencia'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Nobreak', 'Capacidad'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['NoBreak', 'Existencia'] = 1

            if indx == 14:
            ##EquipoExtra
                NomAparato = 'eqextra'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Equipoextra', 'Consumo'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Equipoextra', 'Marca'] = InfoDeco.filter(regex='eqextra_c_i')[0]
                Aparatos_C.loc['EquipoExtra', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Nominal=InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Equipoextra', 'Existencia'] = 1

                #Sonido
            if indx == 7:
                NomAparato = 'sonido'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Sonido', 'Consumo'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Sonido', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Sonido', 'Existencia'] = 1

            ##Decodificador2
            if indx == 8:
                NomAparato = 'decodificador2'
                #Aparatos_C.loc['Decodificador2', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Decodificador2', 'Consumo'] = consumoEq(InfoDeco.filter(regex='consumo')[0])

                if InfoDeco.filter(regex='marca')[0] == 'otro':
                    Aparatos_C.loc['Decodificador2', 'Marca']   = InfoDeco.filter(regex='otro')[0]
                else:
                    Aparatos_C.loc['Decodificador2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Decodificador2', 'Existencia'] = 1

            ##Regulador2
            if indx == 9:
                NomAparato = 'regulador2'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Regulador2', 'Consumo'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Regulador2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Regulador2', 'Existencia'] = 1


            ##Bocinas
            if indx == 10:
                NomAparato = 'bocina'
                #Aparatos_C.loc['Bocinas', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Bocinas', 'Consumo'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Bocinas', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Bocinas', 'Existencia'] = InfoDeco.filter(regex='numero')[0]


            ##Consola
            if indx == 11:
                NomAparato = 'consola1'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Consola1', 'Consumo'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Consola1', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Consola1', 'Existencia'] = 1

            ##Antena
            if indx == 12:
                NomAparato = 'antena'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Antena', 'Consumo'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Antena', 'Marca']   = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Antena', 'Existencia'] = 1

            ##Consola2
            if indx == 13:
                NomAparato = 'consola2'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Consola2', 'Consumo'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Consola2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Consola2', 'Existencia'] = 1

        InfoDeco = Circuito.filter(regex='eqdeahorro')
        if not InfoDeco.empty:
            Aparatos_C.loc['Equipo Ahorro', 'Equipo'] = InfoDeco[0]
            Aparatos_C.loc['Equipo Ahorro', 'Existencia'] = 1
        indx = indx + 1


    InfoDeco = Circuito.filter(regex='clustertv_nombre_c_i')[0]
    print(InfoDeco)

    if InfoDeco=='otrotv_c_i':

        Info_C.loc['Ubicación', 'Info'] = Lugar(Circuito.filter(regex='clustertv_nombre_otro_c_i')[0])
        Aparatos_C.loc['Info', 'Marca'] = Lugar(Circuito.filter(regex='clustertv_nombre_otro_c_i')[0])
        Aparatos_C.loc['Info', 'Existencia'] = 1
    else:

        Info_C.loc['Ubicación', 'Info'] = Lugar(InfoDeco)
        Aparatos_C.loc['Info', 'Marca'] = Lugar(InfoDeco)
        Aparatos_C.loc['Info', 'Existencia'] = 1


    InfoDeco = Circuito.filter(regex='clustertv_notas_c_i')
    if not InfoDeco[0]:
        Info_C.loc['Notas', 'Info'] = InfoDeco[0]
        Aparatos_C.loc['Notas', 'Marca'] = InfoDeco[0]
        Aparatos_C.loc['Notas', 'Existencia'] = 1
    else:
        Info_C.loc['Notas', 'Info'] = Circuito.filter(regex='clustertv_notas_c_i')[0]
        Aparatos_C.loc['Notas', 'Marca'] = Circuito.filter(regex='clustertv_notas_c_i')[0]
        Aparatos_C.loc['Notas', 'Existencia'] = 1

    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()
    TotConsumo = calc_consumo(Aparatos_C)
    Info_C.loc['Consumo Total', 'Info'] = TotConsumo
    #Aparatos.loc[]

    EquiposC = Aparatos.fillna(0)
    NumAparatos = EquiposC['Existencia'].sum()

    Multis=0
    Tolerancia=False

    if EquiposC.loc['Equipo Ahorro','Equipo']!=0:
        Multis=1
    #if EquiposC.loc['TV','Tolerancia']!=0:
    Tolerancia  = True
    Voltaje     = True



    resumenCTV= pd.DataFrame(columns=['Equipo', 'Consumo','Resumen'])

    Lib=condicionesCluster(Aparatos_C,Nominal,TotConsumo,NumAparatos,Tolerancia,Multis, Voltaje)
    Info_C.loc['Consumo Total', 'Info'] = TotConsumo


    return Aparatos.copy() , TotConsumo, Lib, Info_C

