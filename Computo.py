import pandas as pd
from Consumo    import calc_consumo , consumoEq


def computo(Excel,Nocircuito, NomCircuito):
    Aparatos_C = pd.DataFrame(
        index=['Computadora','Laptop','Modem','Repetidor','Equipos Apple','Extra','Impresora','Regulador','Nobreak','Monitor','Switch','Router','HDD', 'Otro','Notas'],
        columns=['Marca','Standby','Nominal', 'Zona','Existencia','Atacable','Notas','CodigoN','CodigoS'])

    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("computo", case=False)]
    Equipos = Circuito[InfoEquipos]
    try:
        Nomedidos = Circuito.filter(regex='computo_equipos_desconectar_c_i')[0]
    except:
        Nomedidos =0

    indx = 0
    for i in Equipos:
        if i == 1:
            Circuito=Equipos.filter(regex='computo')
            Zona=Circuito.filter(regex='zona')[0]
            notass = Circuito.filter(regex='_notas_c_i')[0]
            if indx == 3:
                InfoDeco = Circuito.filter(regex='computadora')

                Aparatos_C.loc['Computadora', 'Marca']    = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Computadora', 'Nominal']     = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Computadora', 'Notas'] = InfoDeco.filter(regex='notas')[0]
                Aparatos_C.loc['Computadora', 'Existencia'] = 1
                Aparatos_C.loc['Computadora', 'Atacable'] = 'Si'
                Aparatos_C.loc['Computadora', 'Zona'] = Zona
                Aparatos_C.loc['Computadora', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                if 'computadora' in Nomedidos:
                    print("computadora no desconectado")
                else:
                    Aparatos_C.loc['Computadora', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['Computadora', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]


            if indx == 4:
                InfoDeco = Circuito.filter(regex='laptop')
                #Aparatos_C.loc['Laptop', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Laptop', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Laptop', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Laptop', 'Notas'] = InfoDeco.filter(regex='notas')[0]
                Aparatos_C.loc['Laptop', 'Existencia'] = 1
                Aparatos_C.loc['Laptop', 'Atacable'] = 'Si'
                Aparatos_C.loc['Laptop', 'Zona'] = Zona
                Aparatos_C.loc['Laptop', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                #Aparatos_C.loc['Laptop', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]

            if indx == 5:
                InfoDeco = Circuito.filter(regex='modem')
                Aparatos_C.loc['Modem', 'Marca'] = InfoDeco.filter(regex='marca')[0]

                Aparatos_C.loc['Modem', 'Notas'] = InfoDeco.filter(regex='notas')[0]
                Aparatos_C.loc['Modem', 'Existencia'] = 1
                Aparatos_C.loc['Modem', 'Atacable'] = 'Si'
                Aparatos_C.loc['Modem', 'Zona'] = Zona
                if 'modem' in Nomedidos:
                    print("Modem no desconectado")
                else:
                    Aparatos_C.loc['Modem', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]
                    Aparatos_C.loc['Modem', 'Standby'] = InfoDeco.filter(regex='standby')[0]

            if indx == 6:
                InfoDeco = Circuito.filter(regex='repetidor')
                Aparatos_C.loc['Repetidor', 'Zona'] = Zona

                Aparatos_C.loc['Repetidor', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Repetidor', 'Existencia'] = 1
                Aparatos_C.loc['Repetidor', 'Atacable'] = 'No'
                Aparatos_C.loc['Repetidor', 'Notas'] = InfoDeco.filter(regex='notas')[0]

                Aparatos_C.loc['Repetidor', 'Notas'] = InfoDeco.filter(regex='notas_c_i')[0]

                if 'repetidor' in Nomedidos:
                    print("Repetidor no desconectado")
                else:
                    Aparatos_C.loc['Repetidor', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['Repetidor', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]


            if indx == 7:
                InfoDeco = Circuito.filter(regex='apple')
                notass=InfoDeco.filter(regex='notas')[0]
                tipo=Circuito.filter(regex='computo_equipos_apple_c_i')[0]
                InfoDeco = Circuito.filter(regex=tipo)
                Aparatos_C.loc['Equipos Apple', 'Marca'] = InfoDeco.filter(regex='equipos_apple_c_i')[0]
                Aparatos_C.loc['Equipos Apple', 'Notas'] = notass
                Aparatos_C.loc['Equipos Apple', 'Zona'] = Zona
                if 'apple' in Nomedidos:
                    print("Equipo_Apple no desconectado")
                # InfoDeco = Circuito.filter(regex='mini')
                # Aparatos_C.loc['Equipos Apple', 'Marca'] = InfoDeco.filter(regex='equipos_apple_c_i')[0]
                # Aparatos_C.loc['Equipos Apple', 'Notas'] = notass
                # Aparatos_C.loc['Equipos Apple', 'Zona'] = Zona
                # InfoDeco = Circuito.filter(regex='apple_time')
                # Aparatos_C.loc['Equipos Apple', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                # Aparatos_C.loc['Equipos Apple', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]
                # Aparatos_C.loc['Equipos Apple', 'Notas'] = notass
                # Aparatos_C.loc['Equipos Apple', 'Existencia'] = 1
                # Aparatos_C.loc['Equipos Apple', 'Atacable'] = 'Si'
                # InfoDeco = Circuito.filter(regex='airport')
                # Aparatos_C.loc['Equipos Apple', 'Standby']  = consumoEq(InfoDeco.filter(regex='standby')[0])
                # Aparatos_C.loc['Equipos Apple', 'Marca']    = InfoDeco.filter(regex='equipos_apple_c_i')[0]
                # Aparatos_C.loc['Equipos Apple', 'Notas']   = notass
                # Aparatos_C.loc['Equipos Apple', 'Zona']    = Zona


            if indx == 8:
                InfoDeco = Circuito.filter(regex='modem2')
                Aparatos_C.loc['Modem Extra', 'Zona'] = Zona

                Aparatos_C.loc['Modem Extra', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                #Aparatos_C.loc['Modem Extra', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby_estimado')[0])
                Aparatos_C.loc['Modem Extra', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Modem Extra', 'Existencia'] = 1
                Aparatos_C.loc['Modem Extra', 'Atacable'] = 'No'

                if 'modem2' in Nomedidos:
                    print("Modem Extra no desconectado")
                else:
                    Aparatos_C.loc['Modem Extra', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['Modem Extra', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]

            if indx == 9:
                InfoDeco = Circuito.filter(regex='impresora')
                Aparatos_C.loc['Impresora', 'Zona'] = Zona
                Aparatos_C.loc['Impresora', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                Aparatos_C.loc['Impresora', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Impresora', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Impresora', 'Existencia'] = 1
                Aparatos_C.loc['Impresora', 'Atacable'] = 'Si'
                Aparatos_C.loc['Impresora', 'Notas'] = InfoDeco.filter(regex='notas_c_i')[0]
                if 'impresora' in Nomedidos:
                    print("Impresora no desconectado")
                else:
                    Aparatos_C.loc['Impresora', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['Impresora', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]


            if indx == 10:
                InfoDeco = Circuito.filter(regex='regulador')
                Aparatos_C.loc['Regulador', 'Zona'] = Zona
                # if InfoDeco.filter(regex='consumo_A').empty:
                #     Aparatos_C.loc['Regulador', 'Standby'] = consumoEq(InfoDeco.filter(regex='consumo_A')[0])
                # if InfoDeco.filter(regex='consumo_B').empty:
                #     Aparatos_C.loc['Regulador', 'Standby'] = consumoEq(InfoDeco.filter(regex='consumo_B')[0])
                # if InfoDeco.filter(regex='estimacion_A').empty:
                #     Aparatos_C.loc['Regulador', 'Standby'] = consumoEq(InfoDeco.filter(regex='estimacion_A')[0])
                # if InfoDeco.filter(regex='estimacion_B').empty:
                #     Aparatos_C.loc['Regulador', 'Standby'] = consumoEq(InfoDeco.filter(regex='estimacion_B')[0])
                if InfoDeco.filter(regex='regulador_apagado_c_i')[0] == 'Si':
                    Aparatos_C.loc['Regulador', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                    Aparatos_C.loc['Regulador', 'CodigoS'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                else:
                    if 'regulador' in Nomedidos:
                        print("Regulador no desconectado")
                    else:
                        Aparatos_C.loc['Regulador', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                        Aparatos_C.loc['Regulador', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]


                Aparatos_C.loc['Regulador', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Regulador', 'Existencia'] = 1
                Aparatos_C.loc['Regulador', 'Atacable'] = 'Si'

                Aparatos_C.loc['Regulador', 'Notas'] = notass

            if indx == 11:
                InfoDeco = Circuito.filter(regex='nobreak')
                Aparatos_C.loc['Nobreak', 'Zona'] = Zona

                Aparatos_C.loc['Nobreak', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Nobreak', 'Existencia'] = 1
                Aparatos_C.loc['Nobreak', 'Atacable'] = 'Si'
                Aparatos_C.loc['Nobreak', 'Notas'] = notass

                if InfoDeco.filter(regex='nobreak_apagado_c_i')[0] == 'Si':
                    Aparatos_C.loc['Nobreak', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                    Aparatos_C.loc['Nobreak', 'CodigoS'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                else:
                    if 'nobreak' in Nomedidos:
                        print("Nobreak no desconectado")
                    else:
                        Aparatos_C.loc['Nobreak', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                        Aparatos_C.loc['Nobreak', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]


            if indx == 12:
                InfoDeco = Circuito.filter(regex='monitor')
                Aparatos_C.loc['Monitor', 'Zona'] = Zona

                Aparatos_C.loc['Monitor', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Monitor', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Monitor', 'Notas'] = InfoDeco.filter(regex='notas')[0]
                Aparatos_C.loc['Monitor', 'Atacable'] = 'Si'
                Aparatos_C.loc['Monitor', 'Existencia'] = 1
                Aparatos_C.loc['Monitor', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Monitor', 'Notas'] = InfoDeco.filter(regex='notas_c_i')[0]
                if 'monitor' in Nomedidos:
                    print("Monitor no desconectado")
                else:
                    Aparatos_C.loc['Monitor', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['Monitor', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]



            if indx == 13:
                InfoDeco = Circuito.filter(regex='switch')
                Aparatos_C.loc['Switch', 'Zona'] =Zona

                Aparatos_C.loc['Switch', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Switch', 'Atacable'] = 'No'
                Aparatos_C.loc['Switch', 'Existencia'] = 1
                Aparatos_C.loc['Switch', 'Notas'] = InfoDeco.filter(regex='notas_c_i')[0]

                if 'switch' in Nomedidos:
                    print("Switch no desconectado")
                else:
                    Aparatos_C.loc['Switch', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['Switch', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]

            if indx == 14:
                InfoDeco = Circuito.filter(regex='router')
                Aparatos_C.loc['Router', 'Zona'] = Zona
                Aparatos_C.loc['Router', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Router', 'Notas'] = InfoDeco.filter(regex='notas_c_i')[0]
                Aparatos_C.loc['Router', 'Existencia'] = 1
                Aparatos_C.loc['Router', 'Atacable'] = 'No'
                if 'router' in Nomedidos:
                    print("Router no desconectado")
                else:
                    Aparatos_C.loc['Router', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['Router', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]

            if indx == 15:
                InfoDeco = Circuito.filter(regex='HDD')

                Aparatos_C.loc['HDD', 'Zona'] = Zona
                Aparatos_C.loc['HDD', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['HDD', 'Existencia'] = 1
                Aparatos_C.loc['HDD', 'Atacable'] = 'No'

                if 'HDD' in Nomedidos:
                    print("Router no desconectado")
                else:
                    Aparatos_C.loc['HDD', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['HDD', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]

                Aparatos_C.loc['HDD', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['HDD', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]

            if indx == 16:
                InfoDeco = Circuito.filter(regex='otro')

                Aparatos_C.loc['Otro', 'Zona'] = Zona

                Aparatos_C.loc['Otro', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Otro', 'Marca'] = InfoDeco.filter(regex='otro_marca_c_i')[0]
                Aparatos_C.loc['Otro', 'Notas'] = InfoDeco.filter(regex='notas')[0]
                Aparatos_C.loc['Otro', 'Existencia'] = 1
                Aparatos_C.loc['Otro', 'Atacable'] = 'Si'
                Aparatos_C.loc['Otro', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]


                if 'otro' in Nomedidos:
                    print("Otro no desconectado")
                else:
                    Aparatos_C.loc['Otro', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['Otro', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]

        indx = indx + 1

    #Aparatos_C.loc['Notas', 'Marca'] = Equipos.filter(regex='comunicaciones_otro_nota_c_i')[0]
    #Aparatos_C.loc['Notas', 'Existencia'] = 1
    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()
    #print(Aparatos)
    return Aparatos