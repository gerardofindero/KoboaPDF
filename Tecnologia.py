import pandas as pd
from Consumo    import calc_consumo , consumoEq


def tecnologia(Excel,Nocircuito, NomCircuito):
    Aparatos_C = pd.DataFrame()
        # index=['Computadora','Laptop','Modem','Repetidor','Equipos Apple','Extra','Impresora','Regulador','Nobreak','Monitor','Switch','Router','HDD', 'Otro','Notas'],
        # columns=['Marca','Standby','Nominal', 'Zona','Existencia','Atacable','Notas','CodigoN','CodigoS','Clave'])

    Circuito    = Excel.loc[Nocircuito]
    Columnas    = Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("tecnologia", case=False)]
    Equipos     = Circuito[InfoEquipos]
    Zona        = Equipos.filter(regex='zona_c_i')[0]
    # stnby     = Circuito.filter(regex='circuito_standby_c_i')[0]
    # stnbyCod  = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
    stnbyEq       = Equipos.filter(regex='equipos_standby_c_i')
    stnbyEqAppl   = Equipos.filter(regex='equipos_standby_apple_c_i')

    InfoDeco = Equipos.filter(regex='modem1')
    Aparatos_C.loc['Modem', 'Marca']      = InfoDeco.filter(regex='marca')[0]
    if Aparatos_C.loc['Modem', 'Marca'] == 'otro':
        Aparatos_C.loc['Modem', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
    Aparatos_C.loc['Modem', 'Standby']    = InfoDeco.filter(regex='standby')[0]
    Aparatos_C.loc['Modem', 'Atacable']   = 'Si'
    Aparatos_C.loc['Modem', 'Zona']       = Zona
    InfoDeco = Equipos.filter(regex='modem2')
    Otro     = InfoDeco.filter(regex='existencia_c_i')[0]
    if Otro == 'si':
        Aparatos_C.loc['Modem2', 'Marca']      = InfoDeco.filter(regex='marca')[0]
        if Aparatos_C.loc['Modem2', 'Marca'] == 'otro':
            Aparatos_C.loc['Modem2', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
        Aparatos_C.loc['Modem2', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['Modem2', 'Atacable']   = 'Si'
        Aparatos_C.loc['Modem2', 'Zona']       = Zona

    InfoDeco = Equipos.filter(regex='repetidor1')
    Aparatos_C.loc['Repetidor', 'Marca']      = InfoDeco.filter(regex='marca')[0]
    if Aparatos_C.loc['Repetidor', 'Marca'] == 'otro':
        Aparatos_C.loc['Repetidor', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
    Aparatos_C.loc['Repetidor', 'Standby']    = InfoDeco.filter(regex='standby')[0]
    Aparatos_C.loc['Repetidor', 'Atacable']   = 'Si'
    Aparatos_C.loc['Repetidor', 'Zona']       = Zona
    InfoDeco = Equipos.filter(regex='repetidor2')
    if InfoDeco.filter(regex='existencia')[0]=='si':
        Aparatos_C.loc['Repetidor2', 'Marca']      = InfoDeco.filter(regex='marca')[0]
        if Aparatos_C.loc['Repetidor2', 'Marca'] == 'otro':
            Aparatos_C.loc['Repetidor2', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
        Aparatos_C.loc['Repetidor2', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['Repetidor2', 'Atacable']   = 'Si'
        Aparatos_C.loc['Repetidor2', 'Zona']       = Zona
    InfoDeco = Equipos.filter(regex='repetidor3')
    if InfoDeco.filter(regex='existencia')[0]=='si':
        Aparatos_C.loc['Repetidor3', 'Marca']      = InfoDeco.filter(regex='marca')[0]
        if Aparatos_C.loc['Repetidor3', 'Marca'] == 'otro':
            Aparatos_C.loc['Repetidor3', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
        Aparatos_C.loc['Repetidor3', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['Repetidor3', 'Atacable']   = 'Si'
        Aparatos_C.loc['Repetidor3', 'Zona']       = Zona

    InfoDeco = Equipos.filter(regex='router1')
    Nota = Equipos.filter(regex='router_notas_c_i')[0]
    Aparatos_C.loc['Router', 'Marca']      = InfoDeco.filter(regex='marca')[0]
    if Aparatos_C.loc['Router', 'Marca'] == 'otro':
        Aparatos_C.loc['Router', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
    Aparatos_C.loc['Router', 'Standby']    = InfoDeco.filter(regex='standby')[0]
    Aparatos_C.loc['Router', 'Atacable']   = 'Si'
    Aparatos_C.loc['Router', 'Zona']       = Zona
    InfoDeco = Equipos.filter(regex='router2')
    Otro     = InfoDeco.filter(regex='existencia_c_i')[0]
    if Otro == 'si':
        Aparatos_C.loc['Router2', 'Marca']      = InfoDeco.filter(regex='marca')[0]
        if Aparatos_C.loc['Router2', 'Marca'] == 'otro':
            Aparatos_C.loc['Router2', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
        Aparatos_C.loc['Router2', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['Router2', 'Atacable']   = 'Si'
        Aparatos_C.loc['Router2', 'Zona']       = Zona

    InfoDeco = Equipos.filter(regex='router3')
    Otro     = InfoDeco.filter(regex='existencia_c_i')[0]

    if Otro == 'si':
        InfoDeco = Equipos.filter(regex='router3')
        Aparatos_C.loc['Router3', 'Marca']      = InfoDeco.filter(regex='marca')[0]
        if Aparatos_C.loc['Router3', 'Marca'] == 'otro':
            Aparatos_C.loc['Router3', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
        Aparatos_C.loc['Router3', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['Router3', 'Atacable']   = 'Si'
        Aparatos_C.loc['Router3', 'Zona']       = Zona

    InfoDeco = Equipos.filter(regex='router4')
    Otro     = InfoDeco.filter(regex='existencia_c_i')[0]
    if Otro == 'si':
        Aparatos_C.loc['Router4', 'Marca']      = InfoDeco.filter(regex='marca')[0]
        if Aparatos_C.loc['Router4', 'Marca'] == 'otro':
            Aparatos_C.loc['Router4', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
        Aparatos_C.loc['Router4', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['Router4', 'Atacable']   = 'Si'
        Aparatos_C.loc['Router4', 'Zona']       = Zona

    InfoDeco = Equipos.filter(regex='telefono')
    Aparatos_C.loc['Telefono', 'Marca']      = InfoDeco.filter(regex='marca')[0]
    Aparatos_C.loc['Telefono', 'Standby']      = InfoDeco.filter(regex='standby')[0]

    InfoDeco = Equipos.filter(regex='conmutador')
    Aparatos_C.loc['Conmutador', 'Marca']      = InfoDeco.filter(regex='marca')[0]
    Aparatos_C.loc['Conmutador', 'Standby']      = InfoDeco.filter(regex='standby')[0]

    InfoDeco = Equipos.filter(regex='monitor1')
    Aparatos_C.loc['Monitor', 'Standby']      = InfoDeco.filter(regex='standby')[0]
    InfoDeco = Equipos.filter(regex='monitor2')
    # if Equipos.filter(regex='existencia') == 'si':
    #     Aparatos_C.loc['Monitor2', 'Standby']      = InfoDeco.filter(regex='standby')[0]

    InfoDeco = Equipos.filter(regex='cctv')
    Aparatos_C.loc['CCTV', 'Marca'] = InfoDeco.filter(regex='marca')[0]
    Aparatos_C.loc['CCTV', 'Standby'] = InfoDeco.filter(regex='standby')[0]

    print(Aparatos_C)
    return Aparatos_C