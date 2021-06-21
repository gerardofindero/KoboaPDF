import pandas as pd
from Consumo    import calc_consumo , consumoEq


def cocina(Excel,Nocircuito, NomCircuito):
    Aparatos_C = pd.DataFrame(
        index=['Microondas', 'Cafetera', 'Licuadora', 'Horno', 'Lavavajillas','CAfetera2', 'Dispensador','Filtro', 'Estufa', 'Tostador', 'Thermomix', 'Otro','Notas'],
        columns=['Marca','Standby', 'Nominal','Existencia','Zona','Atacable','Notas','CodigoN', 'CodigoS'])

    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("cocina", case=False)]
    Equipos = Circuito[InfoEquipos]
    #print(Equipos)
    stnby = Circuito.filter(regex='circuito_standby_c_i')[0]
    stnbyCod = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
    indx = 0
    for i in Equipos:
        if i == 1:


            if indx == 2:
                InfoDeco = Circuito.filter(regex='microondas')

                Aparatos_C.loc['Microondas','Nominal']   = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Microondas','Standby']   = stnby
                Aparatos_C.loc['Microondas', 'Marca']    = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Microondas', 'Existencia'] = 1
                Aparatos_C.loc['Microondas', 'Atacable'] = 'Si'
                Aparatos_C.loc['Microondas', 'Zona'] = 'Cocina'

                Aparatos_C.loc['Microondas', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Microondas', 'CodigoS'] = stnbyCod

            if indx == 3:
                InfoDeco = Circuito.filter(regex='cafetera1')
                Aparatos_C.loc['Cafetera', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Cafetera', 'Standby'] = stnby
                Aparatos_C.loc['Cafetera', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Cafetera', 'Existencia'] = 1
                Aparatos_C.loc['Cafetera', 'Atacable'] = 'Si'
                Aparatos_C.loc['Cafetera', 'Zona'] = 'Cocina'
                Aparatos_C.loc['Cafetera', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Cafetera', 'CodigoS'] = stnbyCod

            if indx == 4:
                InfoDeco = Circuito.filter(regex='licuadora')
                Aparatos_C.loc['Licuadora', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Licuadora', 'Existencia'] = 1
                Aparatos_C.loc['Licuadora', 'Zona'] = 'Cocina'
                Aparatos_C.loc['Licuadora', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]


            if indx == 5:
                InfoDeco = Circuito.filter(regex='horno')
                Aparatos_C.loc['Horno', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Horno', 'Existencia'] = 1
                Aparatos_C.loc['Horno', 'Zona'] = 'Cocina'
                Aparatos_C.loc['Horno', 'Atacable'] = 'NF'
                Aparatos_C.loc['Horno', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]

            if indx == 6:
                InfoDeco = Circuito.filter(regex='lavavajillas')
                Aparatos_C.loc['Lavavajillas', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Lavavajillas', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Lavavajillas', 'Existencia'] = 1
                Aparatos_C.loc['Lavavajillas', 'Zona'] = 'Cocina'
                Aparatos_C.loc['Lavavajillas', 'Atacable'] = 'NF'
                Aparatos_C.loc['Lavavajillas', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]


            if indx == 7:
                InfoDeco = Circuito.filter(regex='cafetera2')

                Aparatos_C.loc['Cafetera2', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Cafetera2', 'Standby'] =stnby
                Aparatos_C.loc['Cafetera2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Cafetera2', 'Existencia'] = 1
                Aparatos_C.loc['Cafetera2', 'Atacable'] = 'Si'
                Aparatos_C.loc['Cafetera2', 'Zona'] = 'Cocina'
                Aparatos_C.loc['Cafetera2', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Cafetera2', 'CodigoS'] = stnbyCod

            if indx == 8:
                InfoDeco = Circuito.filter(regex='dispensador')
                Aparatos_C.loc['Dispensador', 'Standby'] = stnby
                Aparatos_C.loc['Dispensador', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Dispensador', 'Existencia'] = 1
                Aparatos_C.loc['Dispensador', 'Zona'] = 'Cocina'
                Aparatos_C.loc['Dispensador', 'Atacable'] = 'Si'
                Aparatos_C.loc['Dispensador', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Dispensador', 'CodigoS'] = stnbyCod

            if indx == 9:
                InfoDeco = Circuito.filter(regex='filtro')
                Aparatos_C.loc['Filtro', 'Standby'] = stnby
                Aparatos_C.loc['Filtro', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Filtro', 'Existencia'] = 1
                Aparatos_C.loc['Filtro', 'Zona'] = 'Cocina'
                Aparatos_C.loc['Filtro', 'Atacable'] = 'Si'
                Aparatos_C.loc['Filtro', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Filtro', 'CodigoS'] = stnbyCod


            if indx == 10:
                InfoDeco = Circuito.filter(regex='estufa')
                Aparatos_C.loc['Estufa', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Estufa', 'Existencia'] = 1
                Aparatos_C.loc['Estufa', 'Zona'] = 'Cocina'
                Aparatos_C.loc['Estufa', 'Atacable'] = 'NF'
                Aparatos_C.loc['Estufa', 'CodigoN'] =InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]


            if indx == 11:
                InfoDeco = Circuito.filter(regex='tostador')
                Aparatos_C.loc['Tostador', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Tostador', 'Existencia'] = 1
                Aparatos_C.loc['Tostador', 'Zona'] = 'Cocina'
                Aparatos_C.loc['Tostador', 'Atacable'] = 'NF'
                Aparatos_C.loc['Tostador', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]


            if indx == 12:
                InfoDeco = Circuito.filter(regex='thermomix')
                Aparatos_C.loc['Thermomix', 'Standby'] = stnby
                Aparatos_C.loc['Thermomix', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Thermomix', 'Existencia'] = 1
                Aparatos_C.loc['Thermomix', 'Zona'] = 'Cocina'
                Aparatos_C.loc['Thermomix', 'Atacable'] = 'Si'
                Aparatos_C.loc['Thermomix', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Thermomix', 'CodigoS'] = stnbyCod

            if indx == 13:
                InfoDeco = Circuito.filter(regex='otro')
                Aparatos_C.loc['Otro', 'Marca'] = InfoDeco.filter(regex='cocina_otro_c_i')[0]
                Aparatos_C.loc['Otro', 'Standby'] = stnby
                Aparatos_C.loc['Otro', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Otro', 'Atacable'] = 'Si'
                Aparatos_C.loc['Otro', 'Zona'] = 'Cocina'
                Aparatos_C.loc['Otro', 'Existencia'] = 1
                Aparatos_C.loc['Otro', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Otro', 'CodigoS'] = stnbyCod

        indx = indx + 1
    Aparatos_C.loc['Notas', 'Marca'] = Equipos.filter(regex='cocina_notas_c_i')[0]
    Aparatos_C.loc['Notas', 'Existencia'] = 1
    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()
    #print(Aparatos)
    return Aparatos