import pandas as pd
from Consumo    import calc_consumo , consumoEq
def lavanderia(Excel,Nocircuito, NomCircuito):
    Aparatos_C = pd.DataFrame(
        index=['Lavadora', 'Secadora', 'Lavasecadora', 'Plancha', 'PlanchaV','Regulador'],
        columns=[ 'Marca','Standby', 'Nominal','Existencia','Atacable','Zona','Notas','CodigoN','CodigoS','ReguladorL','ReguladorS','Regulador'])

    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("lavanderia_equipos", case=False)]
    Equipos = Circuito[InfoEquipos]
    Notass=Circuito.filter(regex='lavanderia_notas_c_i')[0]
    indx=0
    for i in Equipos:
        if i == 1:
            if indx == 1:
                InfoDeco = Circuito.filter(regex='lavadora')
                Aparatos_C.loc['Lavadora','Nominal']   = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Lavadora','Standby']   = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Lavadora', 'Marca']    = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Lavadora', 'Existencia'] = 1
                Aparatos_C.loc['Lavadora', 'Zona'] = 'Cuarto de lavado'
                if Aparatos_C.loc['Lavadora','Standby'] !=0:
                    Aparatos_C.loc['Lavadora', 'Atacable'] = 'Si'
                else:
                    Aparatos_C.loc['Lavadora', 'Atacable'] = 'NF'
                Aparatos_C.loc['Lavadora', 'Notas'] = Notass
                Aparatos_C.loc['Lavadora', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Lavadora', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]



            if indx == 2:
                InfoDeco = Circuito.filter(regex='secadora')
                Aparatos_C.loc['Secadora', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Secadora', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Secadora', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Secadora', 'Existencia'] = 1
                Aparatos_C.loc['Secadora', 'Zona'] = 'Cuarto de lavado'
                Aparatos_C.loc['Secadora', 'Notas'] = Notass
                if Aparatos_C.loc['Secadora','Standby'] !=0:
                    Aparatos_C.loc['Secadora', 'Atacable'] = 'Si'
                else:
                    Aparatos_C.loc['Secadora', 'Atacable'] = 'NF'
                Aparatos_C.loc['Secadora', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Secadora', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]

                Aparatos_C.loc['Secadora', 'Regulador'] = consumoEq(InfoDeco.filter(regex='reguladorSN')[0])

            if indx == 3:
                InfoDeco = Circuito.filter(regex='lavaseca')
                Aparatos_C.loc['Lavasecadora', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Lavasecadora', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Lavasecadora', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Lavasecadora', 'Existencia'] = 1
                Aparatos_C.loc['Lavasecadora', 'Notas'] = Notass
                Aparatos_C.loc['Lavasecadora', 'Zona'] = 'Cuarto de lavado'
                if Aparatos_C.loc['Lavasecadora','Standby'] !=0:
                    Aparatos_C.loc['Lavasecadora', 'Atacable'] = 'Si'
                else:
                    Aparatos_C.loc['Lavasecadora', 'Atacable'] = 'NF'
                Aparatos_C.loc['Lavasecadora', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                Aparatos_C.loc['Lavasecadora', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]




            if indx == 4:
                InfoDeco = Circuito.filter(regex='plancha')
                Aparatos_C.loc['Plancha', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Plancha', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Plancha', 'Existencia'] = 1
                Aparatos_C.loc['Plancha', 'Zona'] = 'Cuarto de lavado'
                Aparatos_C.loc['Plancha', 'Atacable'] = 'NF'
                Aparatos_C.loc['Plancha', 'Notas'] = Notass
                Aparatos_C.loc['Plancha', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]



            if indx == 5:
                InfoDeco = Circuito.filter(regex='vertical')
                Aparatos_C.loc['PlanchaV', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['PlanchaV', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['PlanchaV', 'Existencia'] = 1
                Aparatos_C.loc['PlanchaV', 'Zona'] = 'Cuarto de lavado'
                Aparatos_C.loc['PlanchaV', 'Atacable'] = 'NF'
                Aparatos_C.loc['PlanchaV', 'Notas'] = Notass
                Aparatos_C.loc['PlanchaV', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]

        indx=indx+1

    InfoEquipos = Columnas[Columnas.str.contains("lavanderia", case=False)]
    Equipos = Circuito[InfoEquipos]
    if Equipos.filter(regex='mismo_regulador_c_i')[0] == 'no':

        if Equipos.filter(regex='lavadora_reguladorSN')[0]=='si':
            InfoDeco = Circuito.filter(regex='lavadora')
            Aparatos_C.loc['ReguladorL', 'CodigoS'] = InfoDeco.filter(regex='regulador_standby_codigofindero_c_i')[0]
            Aparatos_C.loc['ReguladorL', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_standby')[0])
            Aparatos_C.loc['ReguladorL', 'Marca'] = InfoDeco.filter(regex='marca')[0]
            Aparatos_C.loc['ReguladorL', 'Existencia'] = 1
            Aparatos_C.loc['ReguladorL', 'Notas'] = Notass

        if Equipos.filter(regex='secadora_reguladorSN')[0]=='si':
            InfoDeco = Circuito.filter(regex='secadora')
            Aparatos_C.loc['ReguladorS', 'CodigoS'] = InfoDeco.filter(regex='regulador_standby_codigofindero_c_i')[0]
            Aparatos_C.loc['ReguladorS', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_standby')[0])
            Aparatos_C.loc['ReguladorS', 'Marca'] = InfoDeco.filter(regex='marca')[0]
            Aparatos_C.loc['ReguladorS', 'Existencia'] = 1
            Aparatos_C.loc['ReguladorS', 'Notas'] = Notass

    if Equipos.filter(regex='mismo_regulador_c_i')[0] == 'si':
        Aparatos_C.loc['Regulador', 'CodigoS'] = Equipos.filter(regex='mismo_regulador_standby_codigofindero_c_i')[0]
        Aparatos_C.loc['Regulador', 'Standby'] = consumoEq(Equipos.filter(regex='mismo_regulador_standby_c_i')[0])
        Aparatos_C.loc['Regulador', 'Marca']   = Equipos.filter(regex='mismo_regulador_marca_c_i')[0]
        Aparatos_C.loc['Regulador', 'Existencia'] = 1
        Aparatos_C.loc['Regulador', 'Notas'] = Notass

    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()


    return Aparatos