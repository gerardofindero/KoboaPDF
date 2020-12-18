import pandas as pd
from Consumo    import calc_consumo

def iluminacion (Excel,Nocircuito):
    Aparatos_C = pd.DataFrame(index=['E1 Lum1','E1 Lum2','E1 Lum3','E2 Lum1','E2 Lum2','E2 Lum3','E3 Lum1','E3 Lum2','E3 Lum3'],
                              columns=['Lugar', 'Lugar Especifico','Tecnologia', 'Consumo', 'Numero', 'Tamano','Entrada','Sobreiluminacion','Acceso','Adecuaciones','Existencia'])
    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Circuito[Columnas.str.contains("iluminacion", case=False)]


    InfoEsce = InfoEquipos.filter(regex='esce1')
    InfoLum = InfoEsce.filter(regex='luminaria1')

    if InfoLum.filter(regex='lugar')[0] == 'otro':
        lugar = InfoLum.filter(regex='lugar_extra')[0]
    else:
        lugar = InfoLum.filter(regex='lugar')[0]

    Aparatos_C.loc['E1 Lum1', 'Lugar'] = lugar

    lugar_especifico = InfoLum.filter(regex='lugar_especifico')[0]

    if lugar_especifico=='otro':
        Aparatos_C.loc['E1 Lum1', 'Lugar Especifico'] = InfoLum.filter(regex='lugar_otro_c_i')[0]
    else:
        Aparatos_C.loc['E1 Lum1', 'Lugar Especifico'] = lugar_especifico

    Aparatos_C.loc['E1 Lum1', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
    Aparatos_C.loc['E1 Lum1', 'Consumo'] = InfoLum.filter(regex='consumo')[0]
    Aparatos_C.loc['E1 Lum1', 'Numero'] = InfoLum.filter(regex='numero')[0]
    Aparatos_C.loc['E1 Lum1', 'Tamano'] =InfoLum.filter(regex='tipoytam')[0]
    Aparatos_C.loc['E1 Lum1', 'Entrada']     = InfoLum.filter(regex='entrada')[0]
    #Aparatos_C.loc['E1 Lum1', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
    Aparatos_C.loc['E1 Lum1', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
    Aparatos_C.loc['E1 Lum1', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
    Aparatos_C.loc['E1 Lum1', 'Existencia'] = 1

    if InfoEsce.filter(regex='otros1')[0] == 'si':
        Aparatos_C.loc['E1 Lum2', 'Existencia'] = 1

    InfoLum = InfoEsce.filter(regex='luminaria2')
    Aparatos_C.loc['E1 Lum2', 'Lugar'] = lugar

    Aparatos_C.loc['E1 Lum2', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
    Aparatos_C.loc['E1 Lum2', 'Consumo'] = InfoLum.filter(regex='consumo')[0]
    Aparatos_C.loc['E1 Lum2', 'Numero'] = InfoLum.filter(regex='numero')[0]
    Aparatos_C.loc['E1 Lum2', 'Tamano'] = InfoLum.filter(regex='tipoytam')[0]
    Aparatos_C.loc['E1 Lum2', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
    #Aparatos_C.loc['E1 Lum2', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
    Aparatos_C.loc['E1 Lum2', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
    Aparatos_C.loc['E1 Lum2', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]


    if InfoEsce.filter(regex='otros2')[0] == 'si':
        Aparatos_C.loc['E1 Lum3', 'Existencia'] = 1

    InfoLum = InfoEsce.filter(regex='luminaria3')
    Aparatos_C.loc['E1 Lum3', 'Lugar'] = lugar

    Aparatos_C.loc['E1 Lum3', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
    Aparatos_C.loc['E1 Lum3', 'Consumo'] = InfoLum.filter(regex='consumo')[0]
    Aparatos_C.loc['E1 Lum3', 'Numero'] = InfoLum.filter(regex='numero')[0]
    Aparatos_C.loc['E1 Lum3', 'Tamano'] = InfoLum.filter(regex='tipoytam')[0]
    Aparatos_C.loc['E1 Lum3', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
    #Aparatos_C.loc['E1 Lum3', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
    Aparatos_C.loc['E1 Lum3', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
    Aparatos_C.loc['E1 Lum3', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]

    if InfoEquipos.filter(regex='adicionalesce')[0] == 'si':
        Aparatos_C.loc['E2 Lum1', 'Existencia'] = 1

    InfoEsce = InfoEquipos.filter(regex='esce2')
    InfoLum = InfoEsce.filter(regex='luminaria1')

    if InfoLum.filter(regex='lugar')[0] == 'otro':
        lugar = InfoLum.filter(regex='lugar_extra')[0]
    else:
        lugar = InfoLum.filter(regex='lugar')[0]

    Aparatos_C.loc['E2 Lum1', 'Lugar'] = lugar

    lugar_especifico = InfoLum.filter(regex='lugar_especifico')[0]

    if lugar_especifico=='otro':
        Aparatos_C.loc['E2 Lum1', 'Lugar Especifico'] = InfoLum.filter(regex='lugar_otro_c_i')[0]
    else:
        Aparatos_C.loc['E2 Lum1', 'Lugar Especifico'] = lugar_especifico

    Aparatos_C.loc['E2 Lum1', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
    Aparatos_C.loc['E2 Lum1', 'Consumo'] = InfoLum.filter(regex='consumo')[0]
    Aparatos_C.loc['E2 Lum1', 'Numero'] = InfoLum.filter(regex='numero')[0]
    Aparatos_C.loc['E2 Lum1', 'Tamano'] =InfoLum.filter(regex='tipoytam')[0]
    Aparatos_C.loc['E2 Lum1', 'Entrada']     = InfoLum.filter(regex='entrada')[0]
    #Aparatos_C.loc['E2 Lum1', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
    Aparatos_C.loc['E2 Lum1', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
    Aparatos_C.loc['E2 Lum1', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]

    if InfoEsce.filter(regex='otros1')[0] == 'si':
        Aparatos_C.loc['E2 Lum2', 'Existencia'] = 1

    InfoLum = InfoEsce.filter(regex='luminaria2')
    Aparatos_C.loc['E2 Lum2', 'Lugar'] = lugar
    Aparatos_C.loc['E2 Lum2', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
    Aparatos_C.loc['E2 Lum2', 'Consumo'] = InfoLum.filter(regex='consumo')[0]
    Aparatos_C.loc['E2 Lum2', 'Numero'] = InfoLum.filter(regex='numero')[0]
    Aparatos_C.loc['E2 Lum2', 'Tamano'] = InfoLum.filter(regex='tipoytam')[0]
    Aparatos_C.loc['E2 Lum2', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
    #Aparatos_C.loc['E2 Lum2', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
    Aparatos_C.loc['E2 Lum2', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
    Aparatos_C.loc['E2 Lum2', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]

    if InfoEsce.filter(regex='otros2')[0] == 'si':
        Aparatos_C.loc['E2 Lum3', 'Existencia'] = 1

    InfoLum = InfoEsce.filter(regex='luminaria3')
    Aparatos_C.loc['E2 Lum3', 'Lugar'] = lugar
    Aparatos_C.loc['E2 Lum3', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
    Aparatos_C.loc['E2 Lum3', 'Consumo'] = InfoLum.filter(regex='consumo')[0]
    Aparatos_C.loc['E2 Lum3', 'Numero'] = InfoLum.filter(regex='numero')[0]
    Aparatos_C.loc['E2 Lum3', 'Tamano'] = InfoLum.filter(regex='tipoytam')[0]
    Aparatos_C.loc['E2 Lum3', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
    #Aparatos_C.loc['E2 Lum3', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
    Aparatos_C.loc['E2 Lum3', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
    Aparatos_C.loc['E2 Lum3', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]


    if InfoEquipos.filter(regex='adicionalesce1')[0] == 'si':
        Aparatos_C.loc['E3 Lum1', 'Existencia'] = 1

    InfoEsce = InfoEquipos.filter(regex='esce3')
    InfoLum = InfoEsce.filter(regex='luminaria1')


    if InfoLum.filter(regex='lugar')[0] == 'otro':
        lugar = InfoLum.filter(regex='lugar_extra')[0]
    else:
        lugar = InfoLum.filter(regex='lugar')[0]

    Aparatos_C.loc['E3 Lum1', 'Lugar'] = lugar

    lugar_especifico = InfoLum.filter(regex='lugar_especifico')[0]

    if lugar_especifico == 'otro':
        Aparatos_C.loc['E3 Lum1', 'Lugar Especifico'] = InfoLum.filter(regex='lugar_otro_c_i')[0]
    else:
        Aparatos_C.loc['E3 Lum1', 'Lugar Especifico'] = lugar_especifico


    Aparatos_C.loc['E3 Lum1', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
    Aparatos_C.loc['E3 Lum1', 'Consumo'] = InfoLum.filter(regex='consumo')[0]
    Aparatos_C.loc['E3 Lum1', 'Numero'] = InfoLum.filter(regex='numero')[0]
    Aparatos_C.loc['E3 Lum1', 'Tamano'] = InfoLum.filter(regex='tipoytam')[0]
    Aparatos_C.loc['E3 Lum1', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
    #Aparatos_C.loc['E3 Lum1', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
    Aparatos_C.loc['E3 Lum1', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
    Aparatos_C.loc['E3 Lum1', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]

    if InfoEsce.filter(regex='otros1')[0] == 'si':
        Aparatos_C.loc['E3 Lum2', 'Existencia'] = 1

    InfoLum = InfoEsce.filter(regex='luminaria2')
    Aparatos_C.loc['E3 Lum2', 'Lugar'] = lugar
    Aparatos_C.loc['E3 Lum2', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
    Aparatos_C.loc['E3 Lum2', 'Consumo'] = InfoLum.filter(regex='consumo')[0]
    Aparatos_C.loc['E3 Lum2', 'Numero'] = InfoLum.filter(regex='numero')[0]
    Aparatos_C.loc['E3 Lum2', 'Tamano'] = InfoLum.filter(regex='tipoytam')[0]
    Aparatos_C.loc['E3 Lum2', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
    #Aparatos_C.loc['E3 Lum2', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
    Aparatos_C.loc['E3 Lum2', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
    Aparatos_C.loc['E3 Lum2', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]

    if InfoEsce.filter(regex='otros2')[0] == 'si':
        Aparatos_C.loc['E3 Lum3', 'Existencia'] = 1

    InfoLum = InfoEsce.filter(regex='luminaria3')
    Aparatos_C.loc['E3 Lum3', 'Lugar'] = lugar
    Aparatos_C.loc['E3 Lum3', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
    Aparatos_C.loc['E3 Lum3', 'Consumo'] = InfoLum.filter(regex='consumo')[0]
    Aparatos_C.loc['E3 Lum3', 'Numero'] = InfoLum.filter(regex='numero')[0]
    Aparatos_C.loc['E3 Lum3', 'Tamano'] = InfoLum.filter(regex='tipoytam')[0]
    Aparatos_C.loc['E3 Lum3', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
    #Aparatos_C.loc['E3 Lum3', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
    Aparatos_C.loc['E3 Lum3', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
    Aparatos_C.loc['E3 Lum3', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]


    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()
    #print(Aparatos)
    return Aparatos
