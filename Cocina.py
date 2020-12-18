import pandas as pd
from Consumo    import calc_consumo

def cocina(Excel,Nocircuito, NomCircuito):
    Aparatos_C = pd.DataFrame(
        index=['Microondas', 'Cafetera', 'Licuadora', 'Horno', 'Lavavajillas','CAfetera2', 'Dispensador','Filtro', 'Estufa', 'Tostador', 'Thermomix', 'Otro','Notas'],
        columns=['Marca','Consumo', 'Nominal','Existencia'])

    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("cocina", case=False)]
    Equipos = Circuito[InfoEquipos]
    #print(Equipos)


    indx = 0
    for i in Equipos:
        if i == 1:


            if indx == 2:
                InfoDeco = Circuito.filter(regex='microondas')

                Aparatos_C.loc['Microondas','Nominal']   = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Microondas','Consumo']   = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Microondas', 'Marca']    = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Microondas', 'Existencia'] = 1

            if indx == 3:
                InfoDeco = Circuito.filter(regex='cafetera1')
                Aparatos_C.loc['Cafetera', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Cafetera', 'Consumo'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Cafetera', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Cafetera', 'Existencia'] = 1

            if indx == 4:
                InfoDeco = Circuito.filter(regex='licuadora')
                Aparatos_C.loc['Licuadora', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Licuadora', 'Existencia'] = 1

            if indx == 5:
                InfoDeco = Circuito.filter(regex='horno')
                Aparatos_C.loc['Horno', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Horno', 'Existencia'] = 1

            if indx == 6:
                InfoDeco = Circuito.filter(regex='lavavajillas')
                Aparatos_C.loc['Lavavajillas', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Lavavajillas', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Lavavajillas', 'Existencia'] = 1

            if indx == 7:
                InfoDeco = Circuito.filter(regex='cafetera2')

                Aparatos_C.loc['Cafetera2', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Cafetera2', 'Consumo'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Cafetera2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Cafetera2', 'Existencia'] = 1

            if indx == 8:
                InfoDeco = Circuito.filter(regex='dispensador')
                Aparatos_C.loc['Dispensador', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Dispensador', 'Existencia'] = 1

            if indx == 9:
                InfoDeco = Circuito.filter(regex='filtro')
                Aparatos_C.loc['Filtro', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Filtro', 'Existencia'] = 1

            if indx == 10:
                InfoDeco = Circuito.filter(regex='estufa')
                Aparatos_C.loc['Estufa', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Estufa', 'Existencia'] = 1

            if indx == 11:
                InfoDeco = Circuito.filter(regex='tostador')
                Aparatos_C.loc['Tostador', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Tostador', 'Existencia'] = 1

            if indx == 12:
                InfoDeco = Circuito.filter(regex='thermomix')
                Aparatos_C.loc['Thermomix', 'Consumo'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Thermomix', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Thermomix', 'Existencia'] = 1

            if indx == 13:
                InfoDeco = Circuito.filter(regex='otro')
                Aparatos_C.loc['Otro', 'Marca'] = InfoDeco.filter(regex='cocina_otro_c_i')[0]
                Aparatos_C.loc['Otro', 'Consumo'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Otro', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]


                Aparatos_C.loc['Otro', 'Existencia'] = 1

        indx = indx + 1
    Aparatos_C.loc['Notas', 'Marca'] = Equipos.filter(regex='cocina_notas_c_i')[0]
    Aparatos_C.loc['Notas', 'Existencia'] = 1
    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()

    return Aparatos