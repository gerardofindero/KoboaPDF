import pandas as pd
from Consumo    import calc_consumo , consumoEq



def comunicaciones(Excel,Nocircuito, NomCircuito):
    Aparatos_C = pd.DataFrame(
        index=['Telefono','Conmutador','Modem','Repetidor','Switch','Router','Fax','Regulador' 'Otro','Equipos','Notas'],
        columns=['Marca','Standby', 'Zona','Nominal','Existencia','Atacable','Notas','CodigoN','CodigoS'])

    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    CodStandby = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
    InfoEquipos = Columnas[Columnas.str.contains("comunicaciones_equipos", case=False)]
    Equipos = Circuito[InfoEquipos]

    
    if isinstance(Circuito.filter(regex='comunicaciones_equipos_desconectar_c_i')[0], str):
        Nomedidos = Circuito.filter(regex='comunicaciones_equipos_desconectar_c_i')[0]
    else:
        Nomedidos = " no_hay"

    indx = 0

    for i in Equipos:
        if i == 1:
            Circuito=Circuito.filter(regex='comunicaciones')

            if indx == 1:
                InfoDeco = Circuito.filter(regex='telefono')
                if InfoDeco.filter(regex='zona')[0] == 'otro':
                    Aparatos_C.loc['Telefono', 'Zona'] = InfoDeco.filter(regex='zona_otro')[0]
                else:
                    Aparatos_C.loc['Telefono', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                Aparatos_C.loc['Telefono', 'Marca']    = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Telefono', 'Existencia'] = 1
                Aparatos_C.loc['Telefono', 'Atacable'] = 'No'
                Aparatos_C.loc['Telefono', 'Notas'] = 'No'


                # if 'telefono' in Nomedidos:
                #     print("telefono no desconectado")
                # else:
                #     Aparatos_C.loc['Telefono', 'Standby'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                #     Aparatos_C.loc['Telefono', 'CodigoS'] = InfoDeco.filter(regex='codigofindero')[0]




            if indx == 2:
                InfoDeco = Circuito.filter(regex='conmutador')
                if InfoDeco.filter(regex='zona')[0] == 'otro':
                    Aparatos_C.loc['Conmutador', 'Zona'] = InfoDeco.filter(regex='zona_otro')[0]
                else:
                    Aparatos_C.loc['Conmutador', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                Aparatos_C.loc['Conmutador', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Conmutador', 'Existencia'] = 1
                Aparatos_C.loc['Conmutador', 'Atacable'] = 'No'
                Aparatos_C.loc['Conmutador', 'Notas'] = 'No'

                if 'conmutador' in Nomedidos:
                    print("conmutador no desconectado")
                else:
                    Aparatos_C.loc['Conmutador', 'Standby'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                    Aparatos_C.loc['Conmutador', 'CodigoS'] = CodStandby



            if indx == 3:
                InfoDeco = Circuito.filter(regex='modem1')
                if InfoDeco.filter(regex='zona')[0] == 'otro':
                    Aparatos_C.loc['Modem', 'Zona'] = InfoDeco.filter(regex='zona_otro')[0]
                else:
                    Aparatos_C.loc['Modem', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                Aparatos_C.loc['Modem', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Modem', 'Existencia'] = 1
                Aparatos_C.loc['Modem', 'Atacable'] = 'No'
                Aparatos_C.loc['Modem', 'Notas'] = 'No'
                Aparatos_C.loc['Modem', 'CodigoS'] = CodStandby

                if not InfoDeco.filter(regex='regonob_c_i')[0] == 'ninguno':
                    if InfoDeco.filter(regex='regonob_c_i')[0] == 'regulador':
                        Aparatos_C.loc['Regulador', 'Standby'] = InfoDeco.filter(regex='regulador_consumo_c_i')[0]
                        Aparatos_C.loc['Regulador', 'Marca'] = InfoDeco.filter(regex='regulador_marca_c_i')[0]

                if 'modem' in Nomedidos:
                    print("modem no desconectado")
                else:
                    Aparatos_C.loc['Modem', 'Standby'] = consumoEq(InfoDeco.filter(regex='consumo_c_i')[0])
                    Aparatos_C.loc['Regulador', 'CodigoS'] = CodStandby


            if indx == 4:
                InfoDeco = Circuito.filter(regex='repetidor')
                if InfoDeco.filter(regex='zona')[0]=='otro':
                    Aparatos_C.loc['Repetidor', 'Zona'] = InfoDeco.filter(regex='zona_otro')[0]
                else:
                    Aparatos_C.loc['Repetidor', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                Aparatos_C.loc['Repetidor', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Repetidor', 'Existencia'] = 1
                Aparatos_C.loc['Repetidor', 'Atacable'] = 'No'
                Aparatos_C.loc['Repetidor', 'Notas'] = InfoDeco.filter(regex='notas')[0]

                if 'repetidor' in Nomedidos:
                    print("repetidor no desconectado")
                else:
                    Aparatos_C.loc['Repetidor', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['Repetidor', 'CodigoS'] = CodStandby


            if indx == 5:
                InfoDeco = Circuito.filter(regex='switch')
                if InfoDeco.filter(regex='zona')[0]=='otro':
                    Aparatos_C.loc['Switch', 'Zona'] = InfoDeco.filter(regex='zona_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Switch', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                Aparatos_C.loc['Switch', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Switch', 'Existencia'] = 1
                Aparatos_C.loc['Switch', 'Atacable'] = 'No'
                Aparatos_C.loc['Switch', 'Notas'] = InfoDeco.filter(regex='notas')[0]

                if 'switch' in Nomedidos:
                    print("switch no desconectado")
                else:
                    Aparatos_C.loc['Switch', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['Switch', 'CodigoS'] = CodStandby

            if indx == 6:
                InfoDeco = Circuito.filter(regex='router')
                Aparatos_C.loc['Router', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                Aparatos_C.loc['Router', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Router', 'Existencia'] = 1
                Aparatos_C.loc['Router', 'Atacable'] = 'No'
                Aparatos_C.loc['Router', 'Notas'] = InfoDeco.filter(regex='notas')[0]

                if 'router' in Nomedidos:
                    print("router no desconectado")
                else:
                    Aparatos_C.loc['Router', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['Router', 'CodigoS'] = CodStandby


            if indx == 7:
                InfoDeco = Circuito.filter(regex='fax')
                Aparatos_C.loc['Fax', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                Aparatos_C.loc['Fax', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Fax', 'Existencia'] = 1
                Aparatos_C.loc['Fax', 'Atacable'] = 'Si'
                Aparatos_C.loc['Fax', 'Notas'] = InfoDeco.filter(regex='notas')[0]

                if 'fax' in Nomedidos:
                    print("fax no desconectado")
                else:
                    Aparatos_C.loc['Fax', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['Fax', 'CodigoS'] = CodStandby

            if indx == 8:

                InfoDeco = Circuito.filter(regex='comunicaciones_otro')
                Aparatos_C.loc['Otro', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                if InfoDeco.filter(regex='zona')[0] == 'otro':
                    Aparatos_C.loc['Otro', 'Zona'] = InfoDeco.filter(regex='zona_otro')[0]
                else:
                    Aparatos_C.loc['Otro', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                Aparatos_C.loc['Otro', 'Marca'] = InfoDeco.filter(regex='comunicaciones_otro_c_i')[0]
                Aparatos_C.loc['Otro', 'Existencia'] = 1
                Aparatos_C.loc['Otro', 'Atacable'] = 'Si'
                Aparatos_C.loc['Otro', 'Notas'] = InfoDeco.filter(regex='nota')[0]


                if 'otro' in Nomedidos:
                    print("otro no desconectado")
                else:
                    Aparatos_C.loc['Otro', 'Standby'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                    Aparatos_C.loc['Otro', 'CodigoS'] = CodStandby

        indx = indx + 1

    Aparatos_C.loc['Notas', 'Marca'] = Circuito.filter(regex='comunicaciones_otro_nota_c_i')[0]
    Aparatos_C.loc['Notas', 'Existencia'] = 1

    if Nomedidos!=0:
        SumaMedidos= Aparatos_C['Standby'].sum()
        TotalE=consumoEq(Circuito.filter(regex='comunicaciones_standby_total_c_i')[0])
        Aparatos_C.loc['Equipos', 'Marca'] = Nomedidos
        Aparatos_C.loc['Equipos', 'Standby'] = TotalE-SumaMedidos
        Aparatos_C.loc['Otro', 'Zona'] = Aparatos_C['Zona'].mode()[0]
        Aparatos_C.loc['Equipos', 'CodigoS'] = 'FF'
        Aparatos_C.loc['Equipos', 'Atacable'] = 'No'
        Aparatos_C.loc['Equipos', 'Existencia'] = 1


    Aparatos = Aparatos_C[Aparatos_C['Standby'].notna()]
    Aparatos.reset_index()

    return Aparatos