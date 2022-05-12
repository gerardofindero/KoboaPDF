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
    stnby = Circuito.filter(regex='circuito_standby_c_i')[0]
    stnbyCod = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
    CodigoN  = Equipos.filter(regex='cocina_electrodomesticos_codigofindero_c_i')[0]
    if Equipos.filter(regex='electrodomesticos_codigofindero2_c_i')[0]!='X':
        CodigoN  =CodigoN  +','+ Circuito.filter(regex='electrodomesticos_codigofindero2_c_i')[0]
    if Equipos.filter(regex='zona_c_i')[0] == 'otro':
        zona = Equipos.filter(regex='zona_otro_c_i')[0]
    else:
        zona = Equipos.filter(regex='zona_c_i')[0]


    indx = 0
    ERquipos= Equipos.filter(regex='equipos')

    for i in ERquipos:
        if i == 1:
            if indx == 2:
                InfoDeco = Equipos.filter(regex='microondas')
                try:
                    Aparatos_C.loc['Microondas','Nominal']   = consumoEq(InfoDeco.filter(regex='consumo')[0])
                    Aparatos_C.loc['Microondas','Standby']   = consumoEq(InfoDeco.filter(regex='standby')[0])
                except:
                    Aparatos_C.loc['Microondas','Nominal']   = InfoDeco.filter(regex='consumo')[0]
                    Aparatos_C.loc['Microondas','Standby']   = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Microondas', 'Marca']    = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Microondas', 'Existencia'] = 1
                Aparatos_C.loc['Microondas', 'Atacable'] = 'Si'
                Aparatos_C.loc['Microondas', 'Zona'] = zona

                if CodigoN=='X':
                    if InfoDeco.filter(regex='espendiente_c_i')[0]=='no':
                        Aparatos_C.loc['Microondas', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]
                    else:
                        Aparatos_C.loc['Microondas', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                        if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                            Aparatos_C.loc['Microondas', 'CodigoN']     =Aparatos_C.loc['Microondas', 'CodigoN'] +','+ InfoDeco.filter(regex='codigofindero2_c_i')[0]
                else:
                    Aparatos_C.loc['Microondas', 'CodigoN']     = CodigoN
                Aparatos_C.loc['Microondas', 'CodigoS'] = stnbyCod
                Aparatos_C.loc['Microondas', 'Clave'] = 'MC'
                Aparatos_C.loc['Microondas', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]


            if indx == 3:
                InfoDeco = Equipos.filter(regex='cafetera1')
                Aparatos_C.loc['Cafetera', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Cafetera', 'Standby'] = InfoDeco.filter(regex='standby')[0]
                if InfoDeco.filter(regex='marca_c_i')[0] == 'otro':
                    Aparatos_C.loc['Cafetera', 'Marca'] = InfoDeco.filter(regex='marca_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Cafetera', 'Marca'] = InfoDeco.filter(regex='marca_c_i')[0]
                Aparatos_C.loc['Cafetera', 'Existencia'] = 1
                Aparatos_C.loc['Cafetera', 'Atacable'] = 'Si'
                Aparatos_C.loc['Cafetera', 'Zona'] = zona

                if CodigoN=='X':
                    if InfoDeco.filter(regex='espendiente_c_i')[0]=='no':
                        Aparatos_C.loc['Cafetera', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]
                    else:
                        Aparatos_C.loc['Cafetera', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                        if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                            Aparatos_C.loc['Cafetera', 'CodigoN']     =Aparatos_C.loc['Cafetera', 'CodigoN'] +','+ InfoDeco.filter(regex='codigofindero2_c_i')[0]
                else:
                    Aparatos_C.loc['Cafetera', 'CodigoN']     = CodigoN

                Aparatos_C.loc['Cafetera', 'CodigoS'] = stnbyCod
                Aparatos_C.loc['Cafetera', 'Clave'] = 'CF'
                Aparatos_C.loc['Cafetera', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]

                InfoDeco = Equipos.filter(regex='cafetera2')
                if InfoDeco.filter(regex='cafetera2_existencia_c_i')[0]=='si':
                    Aparatos_C.loc['Cafetera2', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                    Aparatos_C.loc['Cafetera2', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    if InfoDeco.filter(regex='marca_c_i')[0] == 'otro':
                        Aparatos_C.loc['Cafetera2', 'Marca'] = InfoDeco.filter(regex='marca_otro_c_i')[0]
                    else:
                        Aparatos_C.loc['Cafetera2', 'Marca'] = InfoDeco.filter(regex='marca_c_i')[0]
                    Aparatos_C.loc['Cafetera2', 'Existencia'] = 1
                    Aparatos_C.loc['Cafetera2', 'Atacable'] = 'Si'
                    Aparatos_C.loc['Cafetera2', 'Zona'] = zona

                    if CodigoN=='X':
                        if InfoDeco.filter(regex='espendiente_c_i')[0]=='no':
                            Aparatos_C.loc['Cafetera2', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]
                        else:
                            Aparatos_C.loc['Cafetera2', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                            if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                                Aparatos_C.loc['Cafetera2', 'CodigoN']     =Aparatos_C.loc['Cafetera2', 'CodigoN'] +','+ InfoDeco.filter(regex='codigofindero2_c_i')[0]
                    else:
                        Aparatos_C.loc['Cafetera2', 'CodigoN']     = CodigoN

                    Aparatos_C.loc['Cafetera2', 'CodigoS'] = stnbyCod
                    Aparatos_C.loc['Cafetera2', 'Clave'] = 'CF'
                    Aparatos_C.loc['Cafetera2', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]

                InfoDeco = Equipos.filter(regex='cafetera3')
                if InfoDeco.filter(regex='cafetera3_existencia_c_i')[0]=='si':
                    Aparatos_C.loc['Cafetera3', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                    Aparatos_C.loc['Cafetera3', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    if InfoDeco.filter(regex='marca_c_i')[0] == 'otro':
                        Aparatos_C.loc['Cafetera3', 'Marca'] = InfoDeco.filter(regex='marca_otro_c_i')[0]
                    else:
                        Aparatos_C.loc['Cafetera3', 'Marca'] = InfoDeco.filter(regex='marca_c_i')[0]
                    Aparatos_C.loc['Cafetera3', 'Existencia'] = 1
                    Aparatos_C.loc['Cafetera3', 'Atacable'] = 'Si'
                    Aparatos_C.loc['Cafetera3', 'Zona'] = zona
                    if CodigoN=='X':
                        if InfoDeco.filter(regex='espendiente_c_i')[0]=='no':
                            Aparatos_C.loc['Cafetera3', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]
                        else:
                            Aparatos_C.loc['Cafetera3', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                            if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                                Aparatos_C.loc['Cafetera3', 'CodigoN']     =Aparatos_C.loc['Cafetera3', 'CodigoN'] +','+ InfoDeco.filter(regex='codigofindero2_c_i')[0]
                    else:
                        Aparatos_C.loc['Cafetera3', 'CodigoN']     = CodigoN
                    Aparatos_C.loc['Cafetera3', 'CodigoS'] = stnbyCod
                    Aparatos_C.loc['Cafetera3', 'Clave'] = 'CF'
                    Aparatos_C.loc['Cafetera3', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]



            if indx == 4:
                InfoDeco = Equipos.filter(regex='licuadora')
                try:
                    Aparatos_C.loc['Licuadora','Nominal']   = consumoEq(InfoDeco.filter(regex='consumo')[0])
                    Aparatos_C.loc['Licuadora','Standby']   = consumoEq(InfoDeco.filter(regex='standby')[0])
                except:
                    Aparatos_C.loc['Licuadora','Nominal']   = InfoDeco.filter(regex='consumo')[0]
                    Aparatos_C.loc['Licuadora','Standby']   = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Licuadora', 'Existencia'] = 1
                Aparatos_C.loc['Licuadora', 'Zona'] = zona
                if CodigoN=='X':
                    Aparatos_C.loc['Licuadora', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                    if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                        Aparatos_C.loc['Licuadora', 'CodigoN']     =Aparatos_C.loc['Licuadora', 'CodigoN'] +','+ \
                                                                    InfoDeco.filter(regex='codigofindero2_c_i')[0]
                else:
                    Aparatos_C.loc['Licuadora', 'CodigoN'] = CodigoN

                Aparatos_C.loc['Licuadora', 'Clave'] = 'X'
                Aparatos_C.loc['Licuadora', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]

            if indx == 5:
                InfoDeco = Equipos.filter(regex='horno')
                if InfoDeco.filter(regex='espendiente_c_i')[0]=='no':
                    Aparatos_C.loc['Horno', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]
                else:
                    CodigoNN  = InfoDeco.filter(regex='codigofindero_c_i')[0]
                    if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                        CodigoNN  =CodigoNN  +','+ InfoDeco.filter(regex='codigofindero2_c_i')[0]
                    if CodigoNN=='X':
                        Aparatos_C.loc['Horno', 'CodigoN'] = CodigoN
                    else:
                        Aparatos_C.loc['Horno', 'CodigoN'] = CodigoNN

                try:
                    Aparatos_C.loc['Horno', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                    Aparatos_C.loc['Horno', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                except:
                    Aparatos_C.loc['Horno', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                    Aparatos_C.loc['Horno', 'Standby'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Horno', 'Existencia'] = 1
                Aparatos_C.loc['Horno', 'Zona'] = zona
                Aparatos_C.loc['Horno', 'Atacable'] = 'NF'
                Aparatos_C.loc['Horno', 'Clave'] = 'X'
                Aparatos_C.loc['Horno', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]

            if indx == 6:
                InfoDeco = Equipos.filter(regex='hornito')
                if InfoDeco.filter(regex='espendiente_c_i')[0]=='no':
                    Aparatos_C.loc['Hornito', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]
                else:
                    CodigoNN  = InfoDeco.filter(regex='codigofindero_c_i')[0]
                    if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                        CodigoNN  =CodigoNN  +','+ InfoDeco.filter(regex='codigofindero2_c_i')[0]
                    if CodigoNN=='X':
                        Aparatos_C.loc['Hornito', 'CodigoN'] = CodigoN
                    else:
                        Aparatos_C.loc['Hornito', 'CodigoN'] = CodigoNN

                try:
                    Aparatos_C.loc['Hornito', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                    Aparatos_C.loc['Hornito', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                except:
                    Aparatos_C.loc['Hornito', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                    Aparatos_C.loc['Hornito', 'Standby'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Hornito', 'Existencia'] = 1
                Aparatos_C.loc['Hornito', 'Zona'] = zona
                Aparatos_C.loc['Hornito', 'Atacable'] = 'NF'
                Aparatos_C.loc['Hornito', 'Clave'] = 'X'
                Aparatos_C.loc['Hornito', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]

            if indx == 7:
                InfoDeco = Equipos.filter(regex='lavavajillas')
                try:
                    Aparatos_C.loc['Lavavajillas', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                    Aparatos_C.loc['Lavavajillas', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                except:
                    Aparatos_C.loc['Lavavajillas', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                    Aparatos_C.loc['Lavavajillas', 'Standby'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Lavavajillas', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Lavavajillas', 'Existencia'] = 1
                Aparatos_C.loc['Lavavajillas', 'Zona'] = zona
                Aparatos_C.loc['Lavavajillas', 'Atacable'] = 'Si'



                if CodigoN=='X':
                    if InfoDeco.filter(regex='espendiente_c_i')[0]=='no':
                        Aparatos_C.loc['Lavavajillas', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]
                    else:
                        Aparatos_C.loc['Lavavajillas', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                        if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                            Aparatos_C.loc['Lavavajillas', 'CodigoN']     =Aparatos_C.loc['Lavavajillas', 'CodigoN'] +','+ InfoDeco.filter(regex='codigofindero2_c_i')[0]
                else:
                    Aparatos_C.loc['Lavavajillas', 'CodigoN']     = CodigoN

                Aparatos_C.loc['Lavavajillas', 'Clave'] = 'X'
                Aparatos_C.loc['Lavavajillas', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]


            if indx == 8:
                InfoDeco = Equipos.filter(regex='dispensador')
                Aparatos_C.loc['Dispensador', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Dispensador', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Dispensador', 'Existencia'] = 1
                Aparatos_C.loc['Dispensador', 'Zona'] = zona
                Aparatos_C.loc['Dispensador', 'Atacable'] = 'Si'
                if CodigoN=='X':
                    if InfoDeco.filter(regex='espendiente_c_i')[0]=='no':
                        Aparatos_C.loc['Dispensador', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]
                    else:
                        Aparatos_C.loc['Dispensador', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                        if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                            Aparatos_C.loc['Dispensador', 'CodigoN']     =Aparatos_C.loc['Dispensador', 'CodigoN'] +','+ InfoDeco.filter(regex='codigofindero2_c_i')[0]
                else:
                    Aparatos_C.loc['Dispensador', 'CodigoN']     = CodigoN
                Aparatos_C.loc['Dispensador', 'CodigoS'] = stnbyCod
                Aparatos_C.loc['Dispensador', 'Clave'] = 'DA'
                Aparatos_C.loc['Dispensador', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]

            if indx == 9:
                InfoDeco = Equipos.filter(regex='filtro')
                Aparatos_C.loc['Filtro', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Filtro', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Filtro', 'Existencia'] = 1
                Aparatos_C.loc['Filtro', 'Zona'] = zona
                Aparatos_C.loc['Filtro', 'Atacable'] = 'Si'
                Aparatos_C.loc['Filtro', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                Aparatos_C.loc['Filtro', 'CodigoS'] = stnbyCod
                Aparatos_C.loc['Filtro', 'Clave'] = 'FL'
                Aparatos_C.loc['Filtro', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]


            if indx == 10:
                InfoDeco = Equipos.filter(regex='estufa')
                if CodigoN=='X':
                    if InfoDeco.filter(regex='espendiente_c_i')[0]=='no':
                        Aparatos_C.loc['Estufa', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]
                    else:
                        Aparatos_C.loc['Estufa', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                        if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                            Aparatos_C.loc['Estufa', 'CodigoN']     =Aparatos_C.loc['Estufa', 'CodigoN'] +','+ InfoDeco.filter(regex='codigofindero2_c_i')[0]
                else:
                    Aparatos_C.loc['Estufa', 'CodigoN']     = CodigoN
                Aparatos_C.loc['Estufa', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Estufa', 'Existencia'] = 1
                Aparatos_C.loc['Estufa', 'Zona'] = zona
                Aparatos_C.loc['Estufa', 'Atacable'] = 'Si'
                Aparatos_C.loc['Estufa', 'Clave'] = 'EF'
                Aparatos_C.loc['Estufa', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]

            if indx == 11:
                InfoDeco = Equipos.filter(regex='tostador')
                if CodigoN=='X':
                    if InfoDeco.filter(regex='espendiente_c_i')[0]=='no':
                        Aparatos_C.loc['Tostador', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]
                    else:
                        Aparatos_C.loc['Tostador', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                        if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                            Aparatos_C.loc['Tostador', 'CodigoN']     =Aparatos_C.loc['Tostador', 'CodigoN'] +','+ InfoDeco.filter(regex='codigofindero2_c_i')[0]
                else:
                    Aparatos_C.loc['Tostador', 'CodigoN']     = CodigoN

                Aparatos_C.loc['Tostador', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Tostador', 'Existencia'] = 1
                Aparatos_C.loc['Tostador', 'Zona'] = zona
                Aparatos_C.loc['Tostador', 'Atacable'] = 'NF'
                Aparatos_C.loc['Tostador', 'Clave'] = 'X'
                Aparatos_C.loc['Tostador', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]


            if indx == 12:
                InfoDeco = Equipos.filter(regex='thermomix')
                Aparatos_C.loc['Thermomix', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Thermomix', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Thermomix', 'Existencia'] = 1
                Aparatos_C.loc['Thermomix', 'Zona'] = zona
                Aparatos_C.loc['Thermomix', 'Atacable'] = 'Si'
                if CodigoN=='X':
                    Aparatos_C.loc['Thermomix', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                    if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                        Aparatos_C.loc['Thermomix', 'CodigoN']     =Aparatos_C.loc['Thermomix', 'CodigoN'] +','+ \
                                                                    InfoDeco.filter(regex='codigofindero2_c_i')[0]
                else:
                    Aparatos_C.loc['Thermomix', 'CodigoN'] = CodigoN

                Aparatos_C.loc['Thermomix', 'CodigoS'] = stnbyCod
                Aparatos_C.loc['Thermomix', 'Clave'] = 'X'
                Aparatos_C.loc['Thermomix', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]

            if indx == 13:
                InfoDeco = Equipos.filter(regex='otro')
                if InfoDeco.filter(regex='espendiente_c_i')[0]=='no':
                    Aparatos_C.loc['Otro', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]
                else:
                    Aparatos_C.loc['Otro', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                    if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                        Aparatos_C.loc['Otro', 'CodigoN']     =Aparatos_C.loc['Otro', 'CodigoN'] +','+ InfoDeco.filter(regex='codigofindero2_c_i')[0]
                Aparatos_C.loc['Otro', 'Marca'] = InfoDeco.filter(regex='cocina_otro_c_i')[0]
                Aparatos_C.loc['Otro', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                # Aparatos_C.loc['Otro', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Otro', 'Nominal'] = 'X'
                Aparatos_C.loc['Otro', 'Atacable'] = 'NS'
                Aparatos_C.loc['Otro', 'Zona'] = zona
                Aparatos_C.loc['Otro', 'Existencia'] = 1
                Aparatos_C.loc['Otro', 'CodigoS'] = stnbyCod
                Aparatos_C.loc['Otro', 'Clave'] = 'X'
                Aparatos_C.loc['Otro', 'Notas'] = Equipos.filter(regex='cocina_notas_c_i')[0]
        indx = indx + 1

    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()

    return Aparatos