import pandas as pd
from Consumo    import calc_consumo , consumoEq


def cocina(Excel,Nocircuito, NomCircuito):
    Aparatos_C = pd.DataFrame(
        index=['Microondas', 'Cafetera', 'Licuadora', 'Horno', 'Lavavajillas','CAfetera2', 'Dispensador','Filtro', 'Estufa', 'Tostador', 'Thermomix', 'Otro','Notas'],
        columns=['Marca','Standby', 'Nominal','Existencia','Zona','Atacable','Notas','CodigoN', 'CodigoS','Clave'])

    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("cocina", case=False)]
    Equipos = Circuito[InfoEquipos]
    Equipos = Equipos.fillna('X')
    #print(Equipos)
    stnby = Circuito.filter(regex='circuito_standby_c_i')[0]
    stnbyCod = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]

    if Equipos.filter(regex='zona_c_i')[0] == 'otro':
        zona = Equipos.filter(regex='zona_otro_c_i')[0]
    else:
        zona = Equipos.filter(regex='zona_c_i')[0]


    indx = 0

    ERquipos= Equipos.filter(regex='equipos')
    print(ERquipos)

    for i in ERquipos:
        if i == 1:
            if indx == 2:
                InfoDeco = Equipos.filter(regex='microondas')

                Aparatos_C.loc['Microondas','Nominal']   = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Microondas','Standby']   = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Microondas', 'Marca']    = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Microondas', 'Existencia'] = 1
                Aparatos_C.loc['Microondas', 'Atacable'] = 'Si'
                Aparatos_C.loc['Microondas', 'Zona'] = zona
                Aparatos_C.loc['Microondas', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                    Aparatos_C.loc['Microondas', 'CodigoN']     =Aparatos_C.loc['Microondas', 'CodigoN'] +','+ InfoDeco.filter(regex='codigofindero2_c_i')[0]

                Aparatos_C.loc['Microondas', 'CodigoS'] = stnbyCod
                Aparatos_C.loc['Microondas', 'Clave'] = 'MC'
                Aparatos_C.loc['Microondas', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]


            if indx == 3:
                InfoDeco = Circuito.filter(regex='cafetera1')
                Aparatos_C.loc['Cafetera', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Cafetera', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                if InfoDeco.filter(regex='marca_c_i')[0] == 'otro':
                    Aparatos_C.loc['Cafetera', 'Marca'] = InfoDeco.filter(regex='marca_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Cafetera', 'Marca'] = InfoDeco.filter(regex='marca_c_i')[0]
                Aparatos_C.loc['Cafetera', 'Existencia'] = 1
                Aparatos_C.loc['Cafetera', 'Atacable'] = 'Si'
                Aparatos_C.loc['Cafetera', 'Zona'] = zona
                Aparatos_C.loc['Cafetera', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Cafetera', 'CodigoS'] = stnbyCod
                Aparatos_C.loc['Cafetera', 'Clave'] = 'CF'
                Aparatos_C.loc['Cafetera', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]

            if indx == 4:
                InfoDeco = Circuito.filter(regex='licuadora')
                Aparatos_C.loc['Licuadora', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Licuadora', 'Existencia'] = 1
                Aparatos_C.loc['Licuadora', 'Zona'] = zona
                Aparatos_C.loc['Licuadora', 'CodigoN'] = Circuito.filter(regex='cocina_electrodomesticos_codigofindero_c_i')[0]
                #Aparatos_C.loc['Microondas', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                if Circuito.filter(regex='cocina_electrodomesticos_codigofindero2_c_i')[0]!='X':
                    Aparatos_C.loc['Licuadora', 'CodigoN']     =Aparatos_C.loc['Licuadora', 'CodigoN'] +','+ \
                                                                 Circuito.filter(regex='cocina_electrodomesticos_codigofindero2_c_i')[0]

                Aparatos_C.loc['Licuadora', 'Clave'] = 'X'
                Aparatos_C.loc['Licuadora', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]

            if indx == 5:
                InfoDeco = Circuito.filter(regex='horno')
                Aparatos_C.loc['Horno', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Horno', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Horno', 'Existencia'] = 1
                Aparatos_C.loc['Horno', 'Zona'] = zona
                Aparatos_C.loc['Horno', 'Atacable'] = 'NF'
                Aparatos_C.loc['Horno', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Horno', 'Clave'] = 'X'
                Aparatos_C.loc['Horno', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]

            if indx == 6:
                InfoDeco = Circuito.filter(regex='lavavajillas')
                Aparatos_C.loc['Lavavajillas', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Lavavajillas', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Lavavajillas', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Lavavajillas', 'Existencia'] = 1
                Aparatos_C.loc['Lavavajillas', 'Zona'] = zona
                Aparatos_C.loc['Lavavajillas', 'Atacable'] = 'Si'
                Aparatos_C.loc['Lavavajillas', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Lavavajillas', 'Clave'] = 'X'
                Aparatos_C.loc['Lavavajillas', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]


            if indx == 7:
                InfoDeco = Circuito.filter(regex='dispensador')
                Aparatos_C.loc['Dispensador', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Dispensador', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Dispensador', 'Existencia'] = 1
                Aparatos_C.loc['Dispensador', 'Zona'] = zona
                Aparatos_C.loc['Dispensador', 'Atacable'] = 'Si'
                Aparatos_C.loc['Dispensador', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Dispensador', 'CodigoS'] = stnbyCod
                Aparatos_C.loc['Dispensador', 'Clave'] = 'DA'
                Aparatos_C.loc['Dispensador', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]

            if indx == 8:
                InfoDeco = Circuito.filter(regex='filtro')
                Aparatos_C.loc['Filtro', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Filtro', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Filtro', 'Existencia'] = 1
                Aparatos_C.loc['Filtro', 'Zona'] = zona
                Aparatos_C.loc['Filtro', 'Atacable'] = 'Si'
                Aparatos_C.loc['Filtro', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Filtro', 'CodigoS'] = stnbyCod
                Aparatos_C.loc['Filtro', 'Clave'] = 'FL'
                Aparatos_C.loc['Filtro', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]


            if indx == 9:
                InfoDeco = Circuito.filter(regex='estufa')
                Aparatos_C.loc['Estufa', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Estufa', 'Existencia'] = 1
                Aparatos_C.loc['Estufa', 'Zona'] = zona
                Aparatos_C.loc['Estufa', 'Atacable'] = 'NF'
                Aparatos_C.loc['Estufa', 'CodigoN'] =InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Estufa', 'Clave'] = 'X'
                Aparatos_C.loc['Estufa', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]

            if indx == 10:
                InfoDeco = Circuito.filter(regex='tostador')
                Aparatos_C.loc['Tostador', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Tostador', 'Existencia'] = 1
                Aparatos_C.loc['Tostador', 'Zona'] = zona
                Aparatos_C.loc['Tostador', 'Atacable'] = 'NF'
                Aparatos_C.loc['Tostador', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Tostador', 'Clave'] = 'X'
                Aparatos_C.loc['Tostador', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]

            if indx == 11:
                InfoDeco = Circuito.filter(regex='thermomix')
                Aparatos_C.loc['Thermomix', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Thermomix', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Thermomix', 'Existencia'] = 1
                Aparatos_C.loc['Thermomix', 'Zona'] = zona
                Aparatos_C.loc['Thermomix', 'Atacable'] = 'Si'
                Aparatos_C.loc['Thermomix', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Thermomix', 'CodigoS'] = stnbyCod
                Aparatos_C.loc['Thermomix', 'Clave'] = 'X'
                Aparatos_C.loc['Thermomix', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]

            if indx == 12:
                InfoDeco = Circuito.filter(regex='otro')
                Aparatos_C.loc['Otro', 'Marca'] = Circuito.filter(regex='cocina_otro_c_i')[0]
                Aparatos_C.loc['Otro', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                # Aparatos_C.loc['Otro', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Otro', 'Nominal'] = 'X'
                Aparatos_C.loc['Otro', 'Atacable'] = 'NS'
                Aparatos_C.loc['Otro', 'Zona'] = zona
                Aparatos_C.loc['Otro', 'Existencia'] = 1
                Aparatos_C.loc['Otro', 'CodigoN'] = Circuito.filter(regex='cocina_electrodomesticos_codigofindero_c_i')[0]
                Aparatos_C.loc['Otro', 'CodigoS'] = stnbyCod
                Aparatos_C.loc['Otro', 'Clave'] = 'X'
                Aparatos_C.loc['Otro', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]
        indx = indx + 1
    #Aparatos_C.loc['Notas', 'Marca'] = Equipos.filter(regex='cocina_notas_c_i')[0]
    #Aparatos_C.loc['Notas', 'Existencia'] = 1
    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()
    #print(Aparatos)


    return Aparatos