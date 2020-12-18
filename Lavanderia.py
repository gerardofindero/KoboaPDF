import pandas as pd
from Consumo    import calc_consumo

def lavanderia(Excel,Nocircuito, NomCircuito):
    Aparatos_C = pd.DataFrame(
        index=['Lavadora', 'Secadora', 'Lavasecadora', 'Plancha', 'PlanchaV'],
        columns=[ 'Marca','Consumo', 'Nominal','Existencia'])

    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("lavanderia_equipos", case=False)]
    Equipos = Circuito[InfoEquipos]
    indx=0
    for i in Equipos:
        if i == 1:
            if indx == 1:
                InfoDeco = Circuito.filter(regex='lavadora')
                #Aparatos_C.loc['Lavadora','Equipo']    = InfoDeco.filter(regex='nombre')[0]
                Aparatos_C.loc['Lavadora','Nominal']   = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Lavadora','Consumo']   = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Lavadora', 'Marca']    = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Lavadora', 'Existencia'] = 1
            if indx == 2:
                InfoDeco = Circuito.filter(regex='secadora')
                # Aparatos_C.loc['Lavadora','Equipo']    = InfoDeco.filter(regex='nombre')[0]
                Aparatos_C.loc['Secadora', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Secadora', 'Consumo'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Secadora', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Secadora', 'Existencia'] = 1
            if indx == 3:
                InfoDeco = Circuito.filter(regex='lavaseca')
                # Aparatos_C.loc['Lavadora','Equipo']    = InfoDeco.filter(regex='nombre')[0]
                Aparatos_C.loc['Lavasecadora', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Lavasecadora', 'Consumo'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Lavasecadora', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Lavasecadora', 'Existencia'] = 1
            if indx == 4:
                InfoDeco = Circuito.filter(regex='plancha')
                Aparatos_C.loc['Plancha', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Plancha', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Plancha', 'Existencia'] = 1
            if indx == 5:
                InfoDeco = Circuito.filter(regex='vertical')
                Aparatos_C.loc['PlanchaV', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['PlanchaV', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['PlanchaV', 'Existencia'] = 1
        indx=indx+1
    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()

    #print(Aparatos)
    return Aparatos