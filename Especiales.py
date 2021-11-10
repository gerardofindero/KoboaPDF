import pandas as pd
import numpy as np
from Consumo    import calc_consumo , consumoEq

def especiales(Excel,Nocircuito, NomCircuito):
    Aparatos_C = pd.DataFrame(
        index=['Especial1', 'Especial2', 'Especial3'],
        columns=['Equipo' ,'Standby', 'Nominal', 'Marca','Zona','Existencia','Atacable','Notas','CodigoN','CodigoS','Clave'])

    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("equipos_especiales", case=False)]
    Equipos= Circuito[InfoEquipos]
    stnby=Circuito.filter(regex='circuito_standby_c_i')[0]
    CodStandby= Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]

#############################Equipo Especial 1###############################################
    if Circuito.filter(regex='equipos_especiales1_c_i')[0] == 'otro':
        Aparatos_C.loc['Especial1','Equipo']  = Circuito.filter(regex='equipos_especial1_nombre_c_i')[0]
    else:
        Aparatos_C.loc['Especial1', 'Equipo'] =Circuito.filter(regex='equipos_especiales1_c_i')[0]

    InfoDeco = Circuito.filter(regex='especial1')
    Aparatos_C.loc['Especial1', 'Zona']        = InfoDeco.filter(regex='zona_c_i')[0]
    Aparatos_C.loc['Especial1', 'Nominal']     = consumoEq(InfoDeco.filter(regex='nominal')[0])
    Aparatos_C.loc['Especial1', 'Marca']       = InfoDeco.filter(regex='marca')[0]
    Aparatos_C.loc['Especial1', 'Notas']       = InfoDeco.filter(regex='notas')[0]
    Aparatos_C.loc['Especial1', 'CodigoN']     = InfoDeco.filter(regex='nominal_codigofindero_c_i')[0]
    Aparatos_C.loc['Especial1', 'Standby']     = consumoEq(InfoDeco.filter(regex='standby_c_i')[0])
    Aparatos_C.loc['Especial1', 'Maniobras']   = InfoDeco.filter(regex='maniobras_c_i')[0]
    Aparatos_C.loc['Especial1', 'ManiobrasD']  = InfoDeco.filter(regex='maniobras_detalles_c_i')[0]
    Aparatos_C.loc['Especial1', 'CodigoS']     = CodStandby
    Aparatos_C.loc['Especial1', 'Clave'] = 'X'
    if Aparatos_C.loc['Especial1','Standby'] !=0:
        Aparatos_C.loc['Especial1', 'Atacable']='Si'
    else:
        Aparatos_C.loc['Especial1', 'Atacable'] = 'NF'
    Aparatos_C.loc['Especial1', 'Existencia'] = 1



#############################Equipo Especial 2###############################################
    if Circuito.filter(regex='equipos_especial1_otro_c_i')[0]=='si':
        if Circuito.filter(regex='equipos_especiales2_c_i')[0] == 'otro':
            Aparatos_C.loc['Especial2', 'Equipo'] = Circuito.filter(regex='equipos_especial2_nombre_c_i')[0]
        else:
            Aparatos_C.loc['Especial2', 'Equipo'] = Circuito.filter(regex='equipos_especiales2_c_i')[0]
        InfoDeco = Circuito.filter(regex='especial2')
        Aparatos_C.loc['Especial2', 'Zona']       = InfoDeco.filter(regex='zona_c_i')[0]
        Aparatos_C.loc['Especial2', 'Nominal']    = consumoEq(InfoDeco.filter(regex='nominal')[0])
        Aparatos_C.loc['Especial2', 'Marca']      = InfoDeco.filter(regex='marca')[0]
        Aparatos_C.loc['Especial2', 'Existencia'] = 1
        Aparatos_C.loc['Especial2', 'Notas']      = InfoDeco.filter(regex='notas')[0]
        Aparatos_C.loc['Especial2', 'Maniobras']  = InfoDeco.filter(regex='maniobras_c_i')[0]
        Aparatos_C.loc['Especial2', 'ManiobrasD'] = InfoDeco.filter(regex='maniobras_detalles_c_i')[0]
        Aparatos_C.loc['Especial2', 'CodigoN']    = InfoDeco.filter(regex='nominal_codigofindero_c_i')[0]
        Aparatos_C.loc['Especial2', 'CodigoS']    = CodStandby
        Aparatos_C.loc['Especial2', 'Standby']    = consumoEq(InfoDeco.filter(regex='standby_c_i')[0])
        Aparatos_C.loc['Especial2', 'Clave'] = 'X'
        if Aparatos_C.loc['Especial2', 'Standby'] != 0:
            Aparatos_C.loc['Especial2', 'Atacable'] = 'Si'
        else:
            Aparatos_C.loc['Especial2', 'Atacable'] = 'NF'

############################Equipo Especial 1###############################################
    if Circuito.filter(regex='equipos_especial2_otro_c_i')[0] == 'si':
        if Circuito.filter(regex='equipos_especiales3_c_i')[0] == 'otro':
            Aparatos_C.loc['Especial3', 'Equipo'] = Circuito.filter(regex='equipos_especial3_nombre_c_i')[0]
        else:
            Aparatos_C.loc['Especial3', 'Equipo'] = Circuito.filter(regex='equipos_especiales3_c_i')[0]
        InfoDeco = Circuito.filter(regex='especial3')
        Aparatos_C.loc['Especial3', 'Zona']       = InfoDeco.filter(regex='zona_c_i')[0]
        Aparatos_C.loc['Especial3', 'Nominal']    = consumoEq(InfoDeco.filter(regex='nominal')[0])
        Aparatos_C.loc['Especial3', 'Marca']      = InfoDeco.filter(regex='marca')[0]
        Aparatos_C.loc['Especial3', 'Existencia'] = 1
        Aparatos_C.loc['Especial3', 'Notas']      = InfoDeco.filter(regex='notas')[0]
        Aparatos_C.loc['Especial3', 'Maniobras']  = InfoDeco.filter(regex='maniobras_c_i')[0]
        Aparatos_C.loc['Especial3', 'ManiobrasD'] = InfoDeco.filter(regex='maniobras_detalles_c_i')[0]
        Aparatos_C.loc['Especial3', 'CodigoN']    = InfoDeco.filter(regex='nominal_codigofindero_c_i')[0]
        Aparatos_C.loc['Especial3', 'Standby']    = consumoEq(InfoDeco.filter(regex='standby_c_i')[0])
        Aparatos_C.loc['Especial3','CodigoS']     = CodStandby
        Aparatos_C.loc['Especial3', 'Clave'] = 'X'
        if Aparatos_C.loc['Especial3','Standby'] !=0:
            Aparatos_C.loc['Especial3', 'Atacable']='Si'
        else:
            Aparatos_C.loc['Especial3', 'Atacable'] = 'NF'


    TotalConsumo = 5 #calc_consumo(Aparatos_C)
    Aparatos = Aparatos_C[Aparatos_C['Equipo'].notna()]
    Aparatos.reset_index()

    return Aparatos , TotalConsumo