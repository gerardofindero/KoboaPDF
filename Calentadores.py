import pandas as pd
from Consumo    import calc_consumo , consumoEq


def calentadores(Excel,Nocircuito, NomCircuito):


    Aparatos_C = pd.DataFrame(
        index=['Ambiente','Calefaccion' ,'Boiler Electrico','Boiler de Gas','Toallas', 'Calentador Otro'],
        columns=[ 'Zona','Marca','Standby', 'Nominal','Existencia','Notas','Atacable','CodigoN','CodigoS','Clave'])

    Circuito = Excel.loc[Nocircuito]
    Columnas = Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("calentador", case=False)]
    Equipos = Circuito[InfoEquipos]
    Tipo = Circuito.filter(regex='calentador_tipo_c_i')
    #print(Tipo)
    CodStnby = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
    Notas= Circuito.filter(regex='calentador_calentadores_notas_c_i')[0]
    indx=0
    Circuito= Equipos.fillna('X')
    for i in Tipo:
        if i == 1:
            if indx == 3:
                InfoDeco = Circuito.filter(regex='portatil')
                if InfoDeco.filter(regex='espendiente_c_i')[0] == 'si':
                    Aparatos_C.loc['Ambiente', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                    if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                        Aparatos_C.loc['Ambiente', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0] \
                                                                   + InfoDeco.filter(regex='codigofindero2_c_i')[0]
                Aparatos_C.loc['Ambiente', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                if Aparatos_C.loc['Ambiente', 'Zona'] != 'otro':
                    Aparatos_C.loc['Ambiente', 'Zona'] = InfoDeco.filter(regex='zona_otro_c_i')[0]

                if InfoDeco.filter(regex='marca')[0]!='otro':
                    Aparatos_C.loc['Ambiente', 'Marca'] = InfoDeco.filter(regex='marca_c_i')[0]
                else:
                    Aparatos_C.loc['Ambiente', 'Marca'] = InfoDeco.filter(regex='marca_otro_c_i')[0]
                Aparatos_C.loc['Ambiente', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Ambiente', 'Standby'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Ambiente', 'Existencia'] = 1
                Aparatos_C.loc['Ambiente', 'Notas'] = Notas
                Aparatos_C.loc['Ambiente', 'Atacable'] = 'Si'
                Aparatos_C.loc['Ambiente', 'Clave'] = 'CP'


            if indx == 4:
                InfoDeco = Circuito.filter(regex='calefaccion_fija')
                Aparatos_C.loc['Calefaccion', 'Zona'] = 'Casa'
                Aparatos_C.loc['Calefaccion', 'Standby'] =  consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Calefaccion', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Calefaccion', 'Marca'] = 'fija'
                Aparatos_C.loc['Calefaccion', 'Existencia'] = 1
                Aparatos_C.loc['Calefaccion', 'Notas'] = Notas
                Aparatos_C.loc['Calefaccion', 'Atacable'] = 'Si'
                print(InfoDeco.filter(regex='codigofindero2_c_i')[0])
                if InfoDeco.filter(regex='espendiente_c_i')[0] == 'si':
                    Aparatos_C.loc['Calefaccion', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                    if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                        Aparatos_C.loc['Calefaccion', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0] \
                                                                   + InfoDeco.filter(regex='codigofindero2_c_i')[0]
                else:
                    Aparatos_C.loc['Calefaccion', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]

                Aparatos_C.loc['Calefaccion', 'CodigoS'] = CodStnby
                Aparatos_C.loc['Calefaccion', 'Clave'] = 'X'

            if indx == 1:
                InfoDeco = Circuito.filter(regex='boiler_luz')

                Aparatos_C.loc['Boiler Electrico', 'Tipo'] = InfoDeco.filter(regex='tipo')[0]
                Aparatos_C.loc['Boiler Electrico', 'Zona'] = 'Casa'
                Aparatos_C.loc['Boiler Electrico', 'Standby'] =  consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Boiler Electrico', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                #Aparatos_C.loc['Boiler Electrico', 'Notas'] = InfoDeco.filter(regex='notas')[0]
                Aparatos_C.loc['Boiler Electrico', 'Atacable'] = 'Si'
                Aparatos_C.loc['Boiler Electrico', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]

                if InfoDeco.filter(regex='espendiente_c_i')[0] == 'si':
                    Aparatos_C.loc['Boiler Electrico', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                    if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                        Aparatos_C.loc['Boiler Electrico', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0] \
                                                                   + InfoDeco.filter(regex='codigofindero2_c_i')[0]
                else:
                    Aparatos_C.loc['Boiler Electrico', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]

                Aparatos_C.loc['Boiler Electrico', 'CodigoS'] = CodStnby
                Aparatos_C.loc['Boiler Electrico', 'Existencia'] = 1
                Aparatos_C.loc['Boiler Electrico', 'Clave'] = 'X'

            if indx == 2:
                InfoDeco = Circuito.filter(regex='boiler_gas')
                if InfoDeco.filter(regex='espendiente_c_i')[0] == 'si':
                    Aparatos_C.loc['Boiler de Gas', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                else:
                    Aparatos_C.loc['Boiler de Gas', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]
                Aparatos_C.loc['Boiler de Gas', 'Zona'] = 'Casa'
                Aparatos_C.loc['Boiler de Gas', 'Standby'] =  consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Boiler de Gas', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Boiler de Gas', 'Existencia'] = 1
                Aparatos_C.loc['Boiler de Gas', 'Notas'] = Notas
                Aparatos_C.loc['Boiler de Gas', 'Atacable'] = 'Si'
                Aparatos_C.loc['Boiler de Gas', 'CodigoS'] = CodStnby
                Aparatos_C.loc['Boiler de Gas', 'Clave'] = 'X'

            if indx == 5:
                InfoDeco = Circuito.filter(regex='toallas')

                Aparatos_C.loc['Toallas', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                Aparatos_C.loc['Toallas', 'Standby'] =  consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Toallas', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Toallas', 'Existencia'] = 1
                Aparatos_C.loc['Toallas', 'Notas'] = InfoDeco.filter(regex='notas')[0]
                Aparatos_C.loc['Toallas', 'Atacable'] = 'Si'
                Aparatos_C.loc['Toallas', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]
                Aparatos_C.loc['Toallas', 'Clave'] = 'X'

            if indx == 6:
                InfoDeco = Equipos.filter(regex='otro')
                Aparatos_C.loc['Calentador Otro', 'Zona'] = InfoDeco.filter(regex='otro_zona_c_i')[0]
                Aparatos_C.loc['Calentador Otro', 'Nominal'] =  consumoEq(InfoDeco.filter(regex='otro_consumo_c_i')[0])
                Aparatos_C.loc['Calentador Otro', 'Marca'] = InfoDeco.filter(regex='tipo_otro_c_i')[0]
                Aparatos_C.loc['Calentador Otro', 'Notas'] = ''
                Aparatos_C.loc['Calentador Otro', 'Existencia'] = 1
                Aparatos_C.loc['Calentador Otro', 'Atacable'] = 'Si'
                Aparatos_C.loc['Notas', 'Existencia'] = 1
                if InfoDeco.filter(regex='otro_espendiente_c_i')[0] == 'si':
                    # Aparatos_C.loc['Calentador Otro', 'CodigoN'] = 'TJ32'
                    Aparatos_C.loc['Calentador Otro', 'CodigoN'] = InfoDeco.filter(regex='otro_codigofindero_c_i')[0]
                    # if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                    #     Aparatos_C.loc['Calentador Otro', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0] \
                    #                                                + InfoDeco.filter(regex='codigofindero2_c_i')[0]
                else:
                    Aparatos_C.loc['Calentador Otro', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]

                Aparatos_C.loc['Calentador Otro', 'Clave'] = 'X'
                #Aparatos_C.loc['Calentador Otro', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]
                #Aparatos_C.loc['Zona', 'Existencia'] = 1
        indx = indx + 1

    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()
    return Aparatos