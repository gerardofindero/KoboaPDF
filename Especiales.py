import pandas as pd
from Consumo    import calc_consumo

def especiales(Excel,Nocircuito, NomCircuito):
    Aparatos_C = pd.DataFrame(
        index=['Especial1', 'Especial2', 'Especial3', 'Notas'],
        columns=['Equipo', 'Consumo', 'Nominal', 'Marca','Existencia'])

    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("equipos_especiales", case=False)]
    Equipos= Circuito[InfoEquipos]


    #print(Circuito.filter(regex='equipos_especiales1_c_i'))

    if Circuito.filter(regex='equipos_especiales1_c_i')[0] == 'otro':

        Aparatos_C.loc['Especial1','Equipo']  = Circuito.filter(regex='equipos_especial1_nombre_c_i')[0]
    else:
        Aparatos_C.loc['Especial1', 'Equipo'] =Circuito.filter(regex='equipos_especiales1_c_i')[0]

    InfoDeco = Circuito.filter(regex='especial1')
    Aparatos_C.loc['Especial1','Nominal']   = InfoDeco.filter(regex='nominal')[0]
    Aparatos_C.loc['Especial1','Consumo']   = InfoDeco.filter(regex='standby')[0]
    Aparatos_C.loc['Especial1', 'Marca']    = InfoDeco.filter(regex='marca')[0]
    Aparatos_C.loc['Especial1', 'Existencia'] = 1

    if Circuito.filter(regex='equipos_especiales2_c_i')[0] == 'otro':

        Aparatos_C.loc['Especial2', 'Equipo'] = Circuito.filter(regex='equipos_especial2_nombre_c_i')[0]
    else:
        Aparatos_C.loc['Especial2', 'Equipo'] = Circuito.filter(regex='equipos_especiales2_c_i')[0]

    InfoDeco = Circuito.filter(regex='especial2')
    #Aparatos_C.loc['Especial2', 'Equipo'] = InfoDeco.filter(regex='nombre')[0]
    Aparatos_C.loc['Especial2', 'Nominal'] = InfoDeco.filter(regex='nominal')[0]
    Aparatos_C.loc['Especial2', 'Consumo'] = InfoDeco.filter(regex='standby')[0]
    Aparatos_C.loc['Especial2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
    Aparatos_C.loc['Especial2', 'Existencia'] = 1

    if Circuito.filter(regex='equipos_especiales3_c_i')[0] == 'otro':

        Aparatos_C.loc['Especial3', 'Equipo'] = Circuito.filter(regex='equipos_especial3_nombre_c_i')[0]
    else:
        Aparatos_C.loc['Especial3', 'Equipo'] = Circuito.filter(regex='equipos_especiales3_c_i')[0]

    InfoDeco = Circuito.filter(regex='especial3')
    #Aparatos_C.loc['Especial3', 'Equipo'] = InfoDeco.filter(regex='nombre')[0]
    Aparatos_C.loc['Especial3', 'Nominal'] = InfoDeco.filter(regex='nominal')[0]
    Aparatos_C.loc['Especial3', 'Consumo'] = InfoDeco.filter(regex='standby')[0]
    Aparatos_C.loc['Especial3', 'Marca'] = InfoDeco.filter(regex='marca')[0]
    Aparatos_C.loc['Especial3', 'Existencia'] = 1

    TotalConsumo = 5 #calc_consumo(Aparatos_C)

    notas=Circuito.filter(regex='notas_especial_c_i')
    if not notas.empty:
        Aparatos_C.loc['Notas', 'Equipo'] = notas[0]
        Aparatos_C.loc['Notas', 'Existencia'] = 1

    Aparatos = Aparatos_C[Aparatos_C['Equipo'].notna()]
    Aparatos.reset_index()
    return Aparatos , TotalConsumo