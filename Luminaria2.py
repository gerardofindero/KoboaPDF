import pandas as pd
from Consumo    import calc_consumo
from Ahorro import  ahorro_luces
from Consumo    import calc_consumo , consumoEq
from Correciones import Lugar
import numpy as np


def palabras(DT):
    DT=pd.DataFrame()
    DT=DT.replace('hal_geno','halógena')
    return DT


def iluminacion (Excel,Nocircuito):
    Aparatos_C = pd.DataFrame(index=['Incandecentes E1','Halogeno E1','Fluorecentes E1','Tira E1','LED E1',
                                     'Incandecentes E2','Halogeno E2','Fluorecentes E2','Tira E2','LED E2',
                                     'Incandecentes E3','Halogeno E3','Fluorecentes E3','Tira E3','LED E3',
                                     'Incandecentes E4','Halogeno E4','Fluorecentes E4','Tira E4','LED E4'],
                              columns=['Lugar', 'LugarEs','Fuga','Tecnologia','FugaDET','Standby'
                                       'Consumo', 'Numero','Fundidos','Total','Combinacion', 'Sobreilum',
                                       'CodigoN','CodigoS','DobCodigo','Codigo2N','Gasto','Donde','DondeDetalle',
                                       'Cajillo','Varios','TipoyTam','Entrada','Adicional','Funcion','Acceso',
                                       'Adecuaciones','Apagador','Notas'])
    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Circuito[Columnas.str.contains("iluminacion", case=False)]

####Lum1
    InfoEsc = InfoEquipos.filter(regex='esce1')
    if InfoEsc.filter(regex='lugar')[0] == 'otro':
        lugar = InfoEsc.filter(regex='lugar_extra')[0]
    else:
        lugar = InfoEsc.filter(regex='lugar')[0]
    lugar_especifico   = InfoEsc.filter(regex='lugar_especifico')[0]
    if lugar_especifico=='otro':
        lugar_especifico  = Lugar(InfoEsc.filter(regex='lugar_otro_c_i')[0])
    else:
        lugar_especifico  = Lugar(lugar_especifico)

    tec = InfoEsc.filter(regex='tecnologia')[0]
    fuga            = InfoEsc.filter(regex='fugaluces')[0]
    fugadetalles    = InfoEsc.filter(regex='fugaluces_detalles')[0]
    standby         = InfoEsc.filter(regex='standby')[0]
    sobreilum       = InfoEsc.filter(regex='sobreilum')[0]
    notas           = InfoEsc.filter(regex='notas')[0]



    tec=tec.split()
    for i in tec:
        if i=='incandescente':
            InfoLum = InfoEquipos.filter(regex='incandescentes')
            Aparatos_C.loc['Incandecentes E1', 'Tecnologia']   = 'incandescentes'
            Aparatos_C.loc['Incandecentes E1', 'Lugar']        = Lugar(lugar)
            Aparatos_C.loc['Incandecentes E1', 'LugarES']      =lugar_especifico
            Aparatos_C.loc['Incandecentes E1', 'Fuga']         = fuga
            Aparatos_C.loc['Incandecentes E1', 'FugaDET']      = fugadetalles
            Aparatos_C.loc['Incandecentes E1', 'Standby']      = standby
            Aparatos_C.loc['Incandecentes E1', 'Sobreilum']    = sobreilum
            Aparatos_C.loc['Incandecentes E1', 'Notas'] = notas

            Aparatos_C.loc['Incandecentes E1', 'Numero']       = InfoLum.filter(regex='numero_c_i')[0]
            Aparatos_C.loc['Incandecentes E1', 'Fundidos']     = InfoLum.filter(regex='fundidos')[0]
            Aparatos_C.loc['Incandecentes E1', 'Total']        = InfoLum.filter(regex='total')[0]
            Aparatos_C.loc['Incandecentes E1', 'Combinacion']  = InfoLum.filter(regex='cobinacion')[0]
            Aparatos_C.loc['Incandecentes E1', 'Consumo']      = consumoEq(InfoLum.filter(regex='consumo')[0])
            Aparatos_C.loc['Incandecentes E1', 'DobCodigo']    = InfoLum.filter(regex='doblecodigo')[0]

            if InfoLum.filter(regex='doblecodigo')[0]=='no':
                Aparatos_C.loc['Incandecentes E1', 'CodigoN']      = InfoLum.filter(regex='codigofindero_')[0]
            else:
                Aparatos_C.loc['Incandecentes E1', 'CodigoN']     = InfoLum.filter(regex='codigofindero2_')[0]


            Aparatos_C.loc['Incandecentes E1', 'Gasto']        = InfoLum.filter(regex='gasto')[0]
            Aparatos_C.loc['Incandecentes E1', 'Donde']        = InfoLum.filter(regex='donde_c_i')[0]
            Aparatos_C.loc['Incandecentes E1', 'DondeDetalle'] = InfoLum.filter(regex='donde_detalle')[0]
            Aparatos_C.loc['Incandecentes E1', 'Cajillo']      = InfoLum.filter(regex='cajillo')[0]
            Aparatos_C.loc['Incandecentes E1', 'Varios']       = InfoLum.filter(regex='varios')[0]
            Aparatos_C.loc['Incandecentes E1', 'TipoyTam']     = InfoLum.filter(regex='tipoytam')[0]
            Aparatos_C.loc['Incandecentes E1', 'Entrada']      = InfoLum.filter(regex='entrada')[0]
            Aparatos_C.loc['Incandecentes E1', 'Adicional']    = InfoLum.filter(regex='adicional')[0]
            Aparatos_C.loc['Incandecentes E1', 'Funcion']      = InfoLum.filter(regex='funcion')[0]

            Aparatos_C.loc['Incandecentes E1', 'Acceso']       = InfoLum.filter(regex='acceso')[0]
            Aparatos_C.loc['Incandecentes E1', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
            Aparatos_C.loc['Incandecentes E1', 'Apagador']     = InfoLum.filter(regex='apagador')[0]

        if i == 'hal_geno':
            InfoLum = InfoEquipos.filter(regex='halogenos')
            Aparatos_C.loc['Halogenos E1', 'Tecnologia']   = 'halogena'
            Aparatos_C.loc['Halogenos E1', 'Lugar']        = Lugar(lugar)
            Aparatos_C.loc['Halogenos E1', 'LugarES']      =lugar_especifico
            Aparatos_C.loc['Halogenos E1', 'Fuga']         = fuga
            Aparatos_C.loc['Halogenos E1', 'FugaDET']      = fugadetalles
            Aparatos_C.loc['Halogenos E1', 'Standby']      = standby
            Aparatos_C.loc['Halogenos E1', 'Sobreilum']    = sobreilum
            Aparatos_C.loc['Halogenos E1', 'Notas'] = notas

            Aparatos_C.loc['Halogenos E1', 'Numero']           = InfoLum.filter(regex='numero')[0]
            Aparatos_C.loc['Halogenos E1', 'Fundidos']         = InfoLum.filter(regex='fundidos')[0]
            Aparatos_C.loc['Halogenos E1', 'Total']            = InfoLum.filter(regex='total')[0]
            Aparatos_C.loc['Halogenos E1', 'Combinacion']      = InfoLum.filter(regex='cobinacion')[0]
            Aparatos_C.loc['Halogenos E1', 'Consumo']          = consumoEq(InfoLum.filter(regex='consumo')[0])
            Aparatos_C.loc['Halogenos E1', 'DobCodigo']        = InfoLum.filter(regex='doblecodigo')[0]
            if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                Aparatos_C.loc['Halogenos E1', 'CodigoN']          = InfoLum.filter(regex='codigofindero_')[0]
            else:
                Aparatos_C.loc['Halogenos E1', 'CodigoN']         = InfoLum.filter(regex='codigofindero2_')[0]
            Aparatos_C.loc['Halogenos E1', 'Gasto']            = InfoLum.filter(regex='gasto')[0]

            Aparatos_C.loc['Halogenos E1', 'Donde']            = InfoLum.filter(regex='donde_c_i')[0]
            Aparatos_C.loc['Halogenos E1', 'DondeDetalle']     = InfoLum.filter(regex='donde_detalle')[0]
            Aparatos_C.loc['Halogenos E1', 'Cajillo']          = InfoLum.filter(regex='cajillo')[0]
            Aparatos_C.loc['Halogenos E1', 'Varios']           = InfoLum.filter(regex='varios')[0]
            Aparatos_C.loc['Halogenos E1', 'TipoyTam']         = InfoLum.filter(regex='tipoytam')[0]
            Aparatos_C.loc['Halogenos E1', 'Entrada']          = InfoLum.filter(regex='entrada')[0]
            Aparatos_C.loc['Halogenos E1', 'Adicional']        = InfoLum.filter(regex='adicional')[0]
            Aparatos_C.loc['Halogenos E1', 'Funcion']          = InfoLum.filter(regex='funcion')[0]

            Aparatos_C.loc['Halogenos E1', 'Acceso']           = InfoLum.filter(regex='acceso')[0]
            Aparatos_C.loc['Halogenos E1', 'Adecuaciones']     = InfoLum.filter(regex='adecuaciones')[0]
            Aparatos_C.loc['Halogenos E1', 'Apagador']         = InfoLum.filter(regex='apagador')[0]

        if i == 'fluorescente':
            InfoLum = InfoEquipos.filter(regex='fluorescentes')
            Aparatos_C.loc['Fluorecentes E1', 'Tecnologia']   = 'fluorescente'
            Aparatos_C.loc['Fluorecentes E1', 'Lugar']        = Lugar(lugar)
            Aparatos_C.loc['Fluorecentes E1', 'LugarES']      =lugar_especifico
            Aparatos_C.loc['Fluorecentes E1', 'Fuga']         = fuga
            Aparatos_C.loc['Fluorecentes E1', 'FugaDET']      = fugadetalles
            Aparatos_C.loc['Fluorecentes E1', 'Standby']      = standby
            Aparatos_C.loc['Fluorecentes E1', 'Sobreilum']    = sobreilum
            Aparatos_C.loc['Fluorecentes E1', 'Notas'] = notas

            Aparatos_C.loc['Fluorecentes E1', 'Numero']           = InfoLum.filter(regex='numero')[0]
            Aparatos_C.loc['Fluorecentes E1', 'Fundidos']         = InfoLum.filter(regex='fundidos')[0]
            Aparatos_C.loc['Fluorecentes E1', 'Total']            = InfoLum.filter(regex='total')[0]
            Aparatos_C.loc['Fluorecentes E1', 'Combinacion']      = InfoLum.filter(regex='cobinacion')[0]
            Aparatos_C.loc['Fluorecentes E1', 'Consumo']          = consumoEq(InfoLum.filter(regex='consumo')[0])
            Aparatos_C.loc['Fluorecentes E1', 'DobCodigo']        = InfoLum.filter(regex='doblecodigo')[0]
            if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                Aparatos_C.loc['Fluorecentes E1', 'CodigoN']          = InfoLum.filter(regex='codigofindero_')[0]
            else:
                Aparatos_C.loc['Fluorecentes E1', 'CodigoN']         = InfoLum.filter(regex='codigofindero2_')[0]
            Aparatos_C.loc['Fluorecentes E1', 'Gasto']            = InfoLum.filter(regex='gasto')[0]

            Aparatos_C.loc['Fluorecentes E1', 'Donde']            = InfoLum.filter(regex='donde_c_i')[0]
            Aparatos_C.loc['Fluorecentes E1', 'DondeDetalle']     = InfoLum.filter(regex='donde_detalle')[0]
            Aparatos_C.loc['Fluorecentes E1', 'Cajillo']          = InfoLum.filter(regex='cajillo')[0]
            Aparatos_C.loc['Fluorecentes E1', 'Varios']           = InfoLum.filter(regex='varios')[0]
            Aparatos_C.loc['Fluorecentes E1', 'TipoyTam']         = InfoLum.filter(regex='tipoytam')[0]
            Aparatos_C.loc['Fluorecentes E1', 'Entrada']          = InfoLum.filter(regex='entrada')[0]
            Aparatos_C.loc['Fluorecentes E1', 'Adicional']        = InfoLum.filter(regex='adicional')[0]
            Aparatos_C.loc['Fluorecentes E1', 'Funcion']          = InfoLum.filter(regex='funcion')[0]

            Aparatos_C.loc['Fluorecentes E1', 'Acceso']            = InfoLum.filter(regex='acceso')[0]
            Aparatos_C.loc['Fluorecentes E1', 'Adecuaciones']      = InfoLum.filter(regex='adecuaciones')[0]
            Aparatos_C.loc['Fluorecentes E1', 'Apagador']          = InfoLum.filter(regex='apagador')[0]

        if i == 'tira_led':
            InfoLum = InfoEquipos.filter(regex='tira')
            Aparatos_C.loc['Tira E1', 'Tecnologia']   = 'led'
            Aparatos_C.loc['Tira E1', 'Lugar']        = Lugar(lugar)
            Aparatos_C.loc['Tira E1', 'LugarES']      =lugar_especifico
            Aparatos_C.loc['Tira E1', 'Fuga']         = fuga
            Aparatos_C.loc['Tira E1', 'FugaDET']      = fugadetalles
            Aparatos_C.loc['Tira E1', 'Standby']      = standby
            Aparatos_C.loc['Tira E1', 'Sobreilum']    = sobreilum
            Aparatos_C.loc['Tira E1', 'Notas'] = notas

            Aparatos_C.loc['Tira E1', 'Numero']            = InfoLum.filter(regex='numero')[0]
            Aparatos_C.loc['Tira E1', 'Fundidos']          = InfoLum.filter(regex='fundidos')[0]
            Aparatos_C.loc['Tira E1', 'Total']             = InfoLum.filter(regex='total')[0]
            Aparatos_C.loc['Tira E1', 'Combinacion']       = InfoLum.filter(regex='cobinacion')[0]
            Aparatos_C.loc['Tira E1', 'Consumo']           = consumoEq(InfoLum.filter(regex='consumo')[0])
            Aparatos_C.loc['Tira E1', 'DobCodigo']         = InfoLum.filter(regex='doblecodigo')[0]

            if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                Aparatos_C.loc['Tira E1', 'CodigoN']           = InfoLum.filter(regex='codigofindero_')[0]
            else:
                Aparatos_C.loc['Tira E1', 'CodigoN']          = InfoLum.filter(regex='codigofindero2_')[0]
            Aparatos_C.loc['Tira E1', 'Gasto']               = InfoLum.filter(regex='gasto')[0]
            Aparatos_C.loc['Tira E1', 'TipoyTam']            = 'Led'
            # Aparatos_C.loc['Tira E1', 'Acceso']            = InfoLum.filter(regex='acceso')[0]
            # Aparatos_C.loc['Tira E1', 'Adecuaciones']      = InfoLum.filter(regex='adecuaciones')[0]
            # Aparatos_C.loc['Tira E1', 'Apagador']          = InfoLum.filter(regex='apagador')[0]

        if i == 'led':
            InfoLum = InfoEquipos.filter(regex='led')
            Aparatos_C.loc['LED E1', 'Tecnologia']   = 'led'
            Aparatos_C.loc['LED E1', 'Lugar']        = Lugar(lugar)
            Aparatos_C.loc['LED E1', 'LugarES']      =lugar_especifico
            Aparatos_C.loc['LED E1', 'Fuga']         = fuga
            Aparatos_C.loc['LED E1', 'FugaDET']      = fugadetalles
            Aparatos_C.loc['LED E1', 'Standby']      = standby
            Aparatos_C.loc['LED E1', 'Sobreilum']    = sobreilum
            Aparatos_C.loc['LED E1', 'Notas'] = notas

            Aparatos_C.loc['LED E1', 'Numero']         = InfoLum.filter(regex='numero')[0]
            Aparatos_C.loc['LED E1', 'Fundidos']       = InfoLum.filter(regex='fundidos')[0]
            Aparatos_C.loc['LED E1', 'Total']          = InfoLum.filter(regex='total')[0]
            Aparatos_C.loc['LED E1', 'Combinacion']    = InfoLum.filter(regex='cobinacion')[0]
            Aparatos_C.loc['LED E1', 'Consumo']        = consumoEq(InfoLum.filter(regex='consumo')[0])
            Aparatos_C.loc['LED E1', 'DobCodigo']      = InfoLum.filter(regex='doblecodigo')[0]

            if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                Aparatos_C.loc['LED E1', 'CodigoN']        = InfoLum.filter(regex='codigofindero_')[0]
            else:
                Aparatos_C.loc['LED E1', 'CodigoN']       = InfoLum.filter(regex='codigofindero2_')[0]
            Aparatos_C.loc['LED E1', 'Gasto']          = InfoLum.filter(regex='gasto')[0]
            Aparatos_C.loc['LED E1', 'TipoyTam'] = 'Led'
            # Aparatos_C.loc['LED', 'Acceso']         = InfoLum.filter(regex='acceso')[0]
            # Aparatos_C.loc['LED', 'Adecuaciones']   = InfoLum.filter(regex='adecuaciones')[0]
            # Aparatos_C.loc['LED', 'apagador']       = InfoLum.filter(regex='apagador')[0]

#######################################################################################################################3
    Esce2 = InfoEquipos.filter(regex='esce2_existencia_c_i')

    if Esce2[0] == 'si':

        InfoEsc = InfoEquipos.filter(regex='esce2')
        if InfoEsc.filter(regex='lugar')[0] == 'otro':
            lugar = InfoEsc.filter(regex='lugar_extra')[0]
        else:
            lugar = InfoEsc.filter(regex='lugar')[0]
        lugar_especifico = InfoEsc.filter(regex='lugar_especifico')[0]
        if lugar_especifico == 'otro':
            lugar_especifico = Lugar(InfoEsc.filter(regex='lugar_otro_c_i')[0])
        else:
            lugar_especifico = Lugar(lugar_especifico)

        tec = InfoEsc.filter(regex='tecnologia')[0]
        fuga = InfoEsc.filter(regex='fugaluces')[0]
        fugadetalles = InfoEsc.filter(regex='fugaluces_detalles')[0]
        standby = InfoEsc.filter(regex='standby')[0]
        sobreilum = InfoEsc.filter(regex='sobreilum')[0]
        notas = InfoEsc.filter(regex='notas')[0]
        tec = tec.split()



        for i in tec:

            if i == 'incandescente':

                InfoLum = InfoEsc.filter(regex='incandescentes')
                Aparatos_C.loc['Incandecentes E2', 'Tecnologia'] = 'incandescente'
                Aparatos_C.loc['Incandecentes E2', 'Lugar'] = Lugar(lugar)
                Aparatos_C.loc['Incandecentes E2', 'LugarES'] = lugar_especifico
                Aparatos_C.loc['Incandecentes E2', 'Fuga'] = fuga
                Aparatos_C.loc['Incandecentes E2', 'FugaDET'] = fugadetalles
                Aparatos_C.loc['Incandecentes E2', 'Standby'] = standby
                Aparatos_C.loc['Incandecentes E2', 'Sobreilum'] = sobreilum
                Aparatos_C.loc['Incandecentes E2', 'Notas'] = notas

                Aparatos_C.loc['Incandecentes E2', 'Numero'] = InfoLum.filter(regex='numero')[0]
                Aparatos_C.loc['Incandecentes E2', 'Fundidos'] = InfoLum.filter(regex='fundidos')[0]
                Aparatos_C.loc['Incandecentes E2', 'Total'] = InfoLum.filter(regex='total')[0]
                Aparatos_C.loc['Incandecentes E2', 'Combinacion'] = InfoLum.filter(regex='cobinacion')[0]
                Aparatos_C.loc['Incandecentes E2', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
                Aparatos_C.loc['Incandecentes E2', 'DobCodigo'] = InfoLum.filter(regex='doblecodigo')[0]
                if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                    Aparatos_C.loc['Incandecentes E2', 'CodigoN'] = InfoLum.filter(regex='codigofindero_')[0]
                else:
                    Aparatos_C.loc['Incandecentes E2', 'CodigoN'] = InfoLum.filter(regex='codigofindero2_')[0]
                Aparatos_C.loc['Incandecentes E2', 'Gasto'] = InfoLum.filter(regex='gasto')[0]
                Aparatos_C.loc['Incandecentes E2', 'Donde'] = InfoLum.filter(regex='donde_c_i')[0]
                Aparatos_C.loc['Incandecentes E2', 'DondeDetalle'] = InfoLum.filter(regex='donde_detalle')[0]
                Aparatos_C.loc['Incandecentes E2', 'Cajillo'] = InfoLum.filter(regex='cajillo')[0]
                Aparatos_C.loc['Incandecentes E2', 'Varios'] = InfoLum.filter(regex='varios')[0]
                Aparatos_C.loc['Incandecentes E2', 'TipoyTam'] = InfoLum.filter(regex='tipoytam')[0]
                Aparatos_C.loc['Incandecentes E2', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
                Aparatos_C.loc['Incandecentes E2', 'Adicional'] = InfoLum.filter(regex='adicional')[0]
                Aparatos_C.loc['Incandecentes E2', 'Funcion'] = InfoLum.filter(regex='funcion')[0]

                Aparatos_C.loc['Incandecentes E2', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
                Aparatos_C.loc['Incandecentes E2', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
                Aparatos_C.loc['Incandecentes E2', 'Apagador'] = InfoLum.filter(regex='apagador')[0]

            if i == 'hal_geno':

                InfoLum = InfoEsc.filter(regex='halogenos')

                Aparatos_C.loc['Halogenos E2', 'Tecnologia'] = 'halogena'
                Aparatos_C.loc['Halogenos E2', 'Lugar'] = Lugar(lugar)
                Aparatos_C.loc['Halogenos E2', 'LugarES'] = lugar_especifico
                Aparatos_C.loc['Halogenos E2', 'Fuga'] = fuga
                Aparatos_C.loc['Halogenos E2', 'FugaDET'] = fugadetalles
                Aparatos_C.loc['Halogenos E2', 'Standby'] = standby
                Aparatos_C.loc['Halogenos E2', 'Sobreilum'] = sobreilum
                Aparatos_C.loc['Halogenos E2', 'Notas'] = notas

                Aparatos_C.loc['Halogenos E2', 'Numero'] = InfoLum.filter(regex='numero_c_i')[0]
                Aparatos_C.loc['Halogenos E2', 'Fundidos'] = InfoLum.filter(regex='fundidos')[0]
                Aparatos_C.loc['Halogenos E2', 'Total'] = InfoLum.filter(regex='total')[0]
                Aparatos_C.loc['Halogenos E2', 'Combinacion'] = InfoLum.filter(regex='cobinacion')[0]
                Aparatos_C.loc['Halogenos E2', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
                Aparatos_C.loc['Halogenos E2', 'DobCodigo'] = InfoLum.filter(regex='doblecodigo')[0]
                if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                    Aparatos_C.loc['Halogenos E2', 'CodigoN'] = InfoLum.filter(regex='codigofindero_')[0]
                else:
                    Aparatos_C.loc['Halogenos E2', 'CodigoN'] = InfoLum.filter(regex='codigofindero2_')[0]
                Aparatos_C.loc['Halogenos E2', 'Gasto'] = InfoLum.filter(regex='gasto')[0]
                Aparatos_C.loc['Halogenos E2', 'Donde'] = InfoLum.filter(regex='donde_c_i')[0]
                Aparatos_C.loc['Halogenos E2', 'DondeDetalle'] = InfoLum.filter(regex='donde_detalle')[0]
                Aparatos_C.loc['Halogenos E2', 'Cajillo'] = InfoLum.filter(regex='cajillo')[0]
                Aparatos_C.loc['Halogenos E2', 'Varios'] = InfoLum.filter(regex='varios')[0]
                Aparatos_C.loc['Halogenos E2', 'TipoyTam'] = InfoLum.filter(regex='tipoytam')[0]
                Aparatos_C.loc['Halogenos E2', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
                Aparatos_C.loc['Halogenos E2', 'Adicional'] = InfoLum.filter(regex='adicional')[0]
                Aparatos_C.loc['Halogenos E2', 'Funcion'] = InfoLum.filter(regex='funcion')[0]

                Aparatos_C.loc['Halogenos E2', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
                Aparatos_C.loc['Halogenos E2', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
                Aparatos_C.loc['Halogenos E2', 'Apagador'] = InfoLum.filter(regex='apagador')[0]

            if i == 'fluorescente':

                InfoLum = InfoEsc.filter(regex='fluorescentes')
                Aparatos_C.loc['Fluorecentes E2', 'Tecnologia'] = 'fluorescente'
                Aparatos_C.loc['Fluorecentes E2', 'Lugar'] = Lugar(lugar)
                Aparatos_C.loc['Fluorecentes E2', 'LugarES'] = lugar_especifico
                Aparatos_C.loc['Fluorecentes E2', 'Fuga'] = fuga
                Aparatos_C.loc['Fluorecentes E2', 'FugaDET'] = fugadetalles
                Aparatos_C.loc['Fluorecentes E2', 'Standby'] = standby
                Aparatos_C.loc['Fluorecentes E2', 'Sobreilum'] = sobreilum
                Aparatos_C.loc['Fluorecentes E2', 'Notas'] = notas

                Aparatos_C.loc['Fluorecentes E2', 'Numero'] = InfoLum.filter(regex='numero')[0]
                Aparatos_C.loc['Fluorecentes E2', 'Fundidos'] = InfoLum.filter(regex='fundidos')[0]
                Aparatos_C.loc['Fluorecentes E2', 'Total'] = InfoLum.filter(regex='total')[0]
                Aparatos_C.loc['Fluorecentes E2', 'Combinacion'] = InfoLum.filter(regex='cobinacion')[0]
                Aparatos_C.loc['Fluorecentes E2', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
                Aparatos_C.loc['Fluorecentes E2', 'DobCodigo'] = InfoLum.filter(regex='doblecodigo')[0]

                if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                    Aparatos_C.loc['Fluorecentes E2', 'CodigoN'] = InfoLum.filter(regex='codigofindero_')[0]
                else:
                    Aparatos_C.loc['Fluorecentes E2', 'CodigoN'] = InfoLum.filter(regex='codigofindero2_')[0]
                Aparatos_C.loc['Fluorecentes E2', 'Gasto'] = InfoLum.filter(regex='gasto')[0]

                Aparatos_C.loc['Fluorecentes E2', 'Donde'] = InfoLum.filter(regex='donde_c_i')[0]
                Aparatos_C.loc['Fluorecentes E2', 'DondeDetalle'] = InfoLum.filter(regex='donde_detalle')[0]
                Aparatos_C.loc['Fluorecentes E2', 'Cajillo'] = InfoLum.filter(regex='cajillo')[0]
                Aparatos_C.loc['Fluorecentes E2', 'Varios'] = InfoLum.filter(regex='varios')[0]
                Aparatos_C.loc['Fluorecentes E2', 'TipoyTam'] = InfoLum.filter(regex='tipoytam')[0]
                Aparatos_C.loc['Fluorecentes E2', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
                Aparatos_C.loc['Fluorecentes E2', 'Adicional'] = InfoLum.filter(regex='adicional')[0]
                Aparatos_C.loc['Fluorecentes E2', 'Funcion'] = InfoLum.filter(regex='funcion')[0]

                Aparatos_C.loc['Fluorecentes E2', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
                Aparatos_C.loc['Fluorecentes E2', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
                Aparatos_C.loc['Fluorecentes E2', 'Apagador'] = InfoLum.filter(regex='apagador')[0]

            if i == 'tira_led':

                InfoLum = InfoEsc.filter(regex='tira')
                Aparatos_C.loc['Tira E2', 'Tecnologia'] = 'led'
                Aparatos_C.loc['Tira E2', 'Lugar'] = Lugar(lugar)
                Aparatos_C.loc['Tira E2', 'LugarES'] = lugar_especifico
                Aparatos_C.loc['Tira E2', 'Fuga'] = fuga
                Aparatos_C.loc['Tira E2', 'FugaDET'] = fugadetalles
                Aparatos_C.loc['Tira E2', 'Standby'] = standby
                Aparatos_C.loc['Tira E2', 'Sobreilum'] = sobreilum
                Aparatos_C.loc['Tira E2', 'Notas'] = notas

                Aparatos_C.loc['Tira E2', 'Numero'] = InfoLum.filter(regex='numero')[0]
                Aparatos_C.loc['Tira E2', 'Fundidos'] = InfoLum.filter(regex='fundidos')[0]
                Aparatos_C.loc['Tira E2', 'Total'] = InfoLum.filter(regex='total')[0]
                Aparatos_C.loc['Tira E2', 'Combinacion'] = InfoLum.filter(regex='cobinacion')[0]
                Aparatos_C.loc['Tira E2', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
                Aparatos_C.loc['Tira E2', 'DobCodigo'] = InfoLum.filter(regex='doblecodigo')[0]

                if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                    Aparatos_C.loc['Tira E2', 'CodigoN'] = InfoLum.filter(regex='codigofindero_')[0]
                else:
                    Aparatos_C.loc['Tira E2', 'CodigoN'] = InfoLum.filter(regex='codigofindero2_')[0]
                Aparatos_C.loc['Tira E2', 'Gasto'] = InfoLum.filter(regex='gasto')[0]
                Aparatos_C.loc['Tira E2', 'TipoyTam'] = 'Led'
                # Aparatos_C.loc['Tira E1', 'Acceso']            = InfoLum.filter(regex='acceso')[0]
                # Aparatos_C.loc['Tira E1', 'Adecuaciones']      = InfoLum.filter(regex='adecuaciones')[0]
                # Aparatos_C.loc['Tira E1', 'Apagador']          = InfoLum.filter(regex='apagador')[0]

            if i == 'led':

                InfoLum = InfoEsc.filter(regex='led')
                Aparatos_C.loc['LED E2', 'Tecnologia'] = 'led'
                Aparatos_C.loc['LED E2', 'Lugar'] = Lugar(lugar)
                Aparatos_C.loc['LED E2', 'LugarES'] = lugar_especifico
                Aparatos_C.loc['LED E2', 'Fuga'] = fuga
                Aparatos_C.loc['LED E2', 'FugaDET'] = fugadetalles
                Aparatos_C.loc['LED E2', 'Standby'] = standby
                Aparatos_C.loc['LED E2', 'Sobreilum'] = sobreilum
                Aparatos_C.loc['LED E2', 'Notas'] = notas

                Aparatos_C.loc['LED E2', 'Numero'] = InfoLum.filter(regex='numero')[0]
                Aparatos_C.loc['LED E2', 'Fundidos'] = InfoLum.filter(regex='fundidos')[0]
                Aparatos_C.loc['LED E2', 'Total'] = InfoLum.filter(regex='total')[0]
                Aparatos_C.loc['LED E2', 'Combinacion'] = InfoLum.filter(regex='cobinacion')[0]
                Aparatos_C.loc['LED E2', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
                Aparatos_C.loc['LED E2', 'DobCodigo'] = InfoLum.filter(regex='doblecodigo')[0]
                if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                    Aparatos_C.loc['LED E2', 'CodigoN'] = InfoLum.filter(regex='codigofindero_')[0]
                else:
                    Aparatos_C.loc['LED E2', 'CodigoN'] = InfoLum.filter(regex='codigofindero2_')[0]
                Aparatos_C.loc['LED E2', 'Gasto'] = InfoLum.filter(regex='gasto')[0]
                Aparatos_C.loc['LED E2', 'TipoyTam'] = 'Led'
                # Aparatos_C.loc['LED', 'Acceso']         = InfoLum.filter(regex='acceso')[0]
                # Aparatos_C.loc['LED', 'Adecuaciones']   = InfoLum.filter(regex='adecuaciones')[0]
                # Aparatos_C.loc['LED', 'apagador']       = InfoLum.filter(regex='apagador')[0]


###################################################################################################################
    Esce3 = InfoEquipos.filter(regex='esce3_existencia_c_i')

    if Esce3[0] == 'si':

        InfoEsc = InfoEquipos.filter(regex='esce3')
        if InfoEsc.filter(regex='lugar')[0] == 'otro':
            lugar = InfoEsc.filter(regex='lugar_extra')[0]
        else:
            lugar = InfoEsc.filter(regex='lugar')[0]
        lugar_especifico = InfoEsc.filter(regex='lugar_especifico')[0]
        if lugar_especifico == 'otro':
            lugar_especifico = Lugar(InfoEsc.filter(regex='lugar_otro_c_i')[0])
        else:
            lugar_especifico = Lugar(lugar_especifico)

        tec = InfoEsc.filter(regex='tecnologia')[0]
        fuga = InfoEsc.filter(regex='fugaluces')[0]
        fugadetalles = InfoEsc.filter(regex='fugaluces_detalles')[0]
        standby = InfoEsc.filter(regex='standby')[0]
        sobreilum = InfoEsc.filter(regex='sobreilum')[0]
        notas = InfoEsc.filter(regex='notas')[0]
        tec = tec.split()
        print(tec)
        for i in tec:
            if i == 'incandescente':
                InfoLum = InfoEsc.filter(regex='incandescentes')
                Aparatos_C.loc['Incandecentes E3', 'Tecnologia'] = 'incandescente'
                Aparatos_C.loc['Incandecentes E3', 'Lugar'] = Lugar(lugar)
                Aparatos_C.loc['Incandecentes E3', 'LugarES'] = lugar_especifico
                Aparatos_C.loc['Incandecentes E3', 'Fuga'] = fuga
                Aparatos_C.loc['Incandecentes E3', 'FugaDET'] = fugadetalles
                Aparatos_C.loc['Incandecentes E3', 'Standby'] = standby
                Aparatos_C.loc['Incandecentes E3', 'Sobreilum'] = sobreilum
                Aparatos_C.loc['Incandecentes E3', 'Notas'] = notas

                Aparatos_C.loc['Incandecentes E3', 'Numero'] = InfoLum.filter(regex='numero')[0]
                Aparatos_C.loc['Incandecentes E3', 'Fundidos'] = InfoLum.filter(regex='fundidos')[0]
                Aparatos_C.loc['Incandecentes E3', 'Total'] = InfoLum.filter(regex='total')[0]
                Aparatos_C.loc['Incandecentes E3', 'Combinacion'] = InfoLum.filter(regex='cobinacion')[0]
                Aparatos_C.loc['Incandecentes E3', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
                Aparatos_C.loc['Incandecentes E3', 'DobCodigo'] = InfoLum.filter(regex='doblecodigo')[0]

                if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                    Aparatos_C.loc['Incandecentes E3', 'CodigoN'] = InfoLum.filter(regex='codigofindero_')[0]
                else:
                    Aparatos_C.loc['Incandecentes E3', 'CodigoN'] = InfoLum.filter(regex='codigofindero2_')[0]
                Aparatos_C.loc['Incandecentes E3', 'Gasto'] = InfoLum.filter(regex='gasto')[0]
                Aparatos_C.loc['Incandecentes E3', 'Donde'] = InfoLum.filter(regex='donde_c_i')[0]
                Aparatos_C.loc['Incandecentes E3', 'DondeDetalle'] = InfoLum.filter(regex='donde_detalle')[0]
                Aparatos_C.loc['Incandecentes E3', 'Cajillo'] = InfoLum.filter(regex='cajillo')[0]
                Aparatos_C.loc['Incandecentes E3', 'Varios'] = InfoLum.filter(regex='varios')[0]
                Aparatos_C.loc['Incandecentes E3', 'TipoyTam'] = InfoLum.filter(regex='tipoytam')[0]
                Aparatos_C.loc['Incandecentes E3', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
                Aparatos_C.loc['Incandecentes E3', 'Adicional'] = InfoLum.filter(regex='adicional')[0]
                Aparatos_C.loc['Incandecentes E3', 'Funcion'] = InfoLum.filter(regex='funcion')[0]

                Aparatos_C.loc['Incandecentes E3', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
                Aparatos_C.loc['Incandecentes E3', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
                Aparatos_C.loc['Incandecentes E3', 'Apagador'] = InfoLum.filter(regex='apagador')[0]

            if i == 'hal_geno':
                InfoLum = InfoEsc.filter(regex='halogenos')
                Aparatos_C.loc['Halogenos E3', 'Tecnologia'] = 'halogena'
                Aparatos_C.loc['Halogenos E3', 'Lugar'] = Lugar(lugar)
                Aparatos_C.loc['Halogenos E3', 'LugarES'] = lugar_especifico
                Aparatos_C.loc['Halogenos E3', 'Fuga'] = fuga
                Aparatos_C.loc['Halogenos E3', 'FugaDET'] = fugadetalles
                Aparatos_C.loc['Halogenos E3', 'Standby'] = standby
                Aparatos_C.loc['Halogenos E3', 'Sobreilum'] = sobreilum
                Aparatos_C.loc['Halogenos E3', 'Notas'] = notas

                Aparatos_C.loc['Halogenos E3', 'Numero'] = InfoLum.filter(regex='numero')[0]
                Aparatos_C.loc['Halogenos E3', 'Fundidos'] = InfoLum.filter(regex='fundidos')[0]
                Aparatos_C.loc['Halogenos E3', 'Total'] = InfoLum.filter(regex='total')[0]
                Aparatos_C.loc['Halogenos E3', 'Combinacion'] = InfoLum.filter(regex='cobinacion')[0]
                Aparatos_C.loc['Halogenos E3', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
                Aparatos_C.loc['Halogenos E3', 'DobCodigo'] = InfoLum.filter(regex='doblecodigo')[0]
                if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                    Aparatos_C.loc['Halogenos E3', 'CodigoN'] = InfoLum.filter(regex='codigofindero_')[0]
                else:
                    Aparatos_C.loc['Halogenos E3', 'CodigoN'] = InfoLum.filter(regex='codigofindero2_')[0]
                Aparatos_C.loc['Halogenos E3', 'Gasto'] = InfoLum.filter(regex='gasto')[0]
                Aparatos_C.loc['Halogenos E3', 'Donde'] = InfoLum.filter(regex='donde_c_i')[0]
                Aparatos_C.loc['Halogenos E3', 'DondeDetalle'] = InfoLum.filter(regex='donde_detalle')[0]
                Aparatos_C.loc['Halogenos E3', 'Cajillo'] = InfoLum.filter(regex='cajillo')[0]
                Aparatos_C.loc['Halogenos E3', 'Varios'] = InfoLum.filter(regex='varios')[0]
                Aparatos_C.loc['Halogenos E3', 'TipoyTam'] = InfoLum.filter(regex='tipoytam')[0]
                Aparatos_C.loc['Halogenos E3', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
                Aparatos_C.loc['Halogenos E3', 'Adicional'] = InfoLum.filter(regex='adicional')[0]
                Aparatos_C.loc['Halogenos E3', 'Funcion'] = InfoLum.filter(regex='funcion')[0]

                Aparatos_C.loc['Halogenos E3', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
                Aparatos_C.loc['Halogenos E3', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
                Aparatos_C.loc['Halogenos E3', 'Apagador'] = InfoLum.filter(regex='apagador')[0]

            if i == 'fluorescente':
                InfoLum = InfoEsc.filter(regex='fluorescentes')
                Aparatos_C.loc['Fluorecentes E3', 'Tecnologia'] = 'fluorescente'
                Aparatos_C.loc['Fluorecentes E3', 'Lugar'] = Lugar(lugar)
                Aparatos_C.loc['Fluorecentes E3', 'LugarES'] = lugar_especifico
                Aparatos_C.loc['Fluorecentes E3', 'Fuga'] = fuga
                Aparatos_C.loc['Fluorecentes E3', 'FugaDET'] = fugadetalles
                Aparatos_C.loc['Fluorecentes E3', 'Standby'] = standby
                Aparatos_C.loc['Fluorecentes E3', 'Sobreilum'] = sobreilum
                Aparatos_C.loc['Fluorecentes E3', 'Notas'] = notas

                Aparatos_C.loc['Fluorecentes E3', 'Numero'] = InfoLum.filter(regex='numero')[0]
                Aparatos_C.loc['Fluorecentes E3', 'Fundidos'] = InfoLum.filter(regex='fundidos')[0]
                Aparatos_C.loc['Fluorecentes E3', 'Total'] = InfoLum.filter(regex='total')[0]
                Aparatos_C.loc['Fluorecentes E3', 'Combinacion'] = InfoLum.filter(regex='cobinacion')[0]
                Aparatos_C.loc['Fluorecentes E3', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
                Aparatos_C.loc['Fluorecentes E3', 'DobCodigo'] = InfoLum.filter(regex='doblecodigo')[0]
                if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                    Aparatos_C.loc['Fluorecentes E3', 'CodigoN'] = InfoLum.filter(regex='codigofindero_')[0]
                else:
                    Aparatos_C.loc['Fluorecentes E3', 'CodigoN'] = InfoLum.filter(regex='codigofindero2_')[0]
                Aparatos_C.loc['Fluorecentes E3', 'Gasto'] = InfoLum.filter(regex='gasto')[0]

                Aparatos_C.loc['Fluorecentes E3', 'Donde'] = InfoLum.filter(regex='donde_c_i')[0]
                Aparatos_C.loc['Fluorecentes E3', 'DondeDetalle'] = InfoLum.filter(regex='donde_detalle')[0]
                Aparatos_C.loc['Fluorecentes E3', 'Cajillo'] = InfoLum.filter(regex='cajillo')[0]
                Aparatos_C.loc['Fluorecentes E3', 'Varios'] = InfoLum.filter(regex='varios')[0]
                Aparatos_C.loc['Fluorecentes E3', 'TipoyTam'] = InfoLum.filter(regex='tipoytam')[0]
                Aparatos_C.loc['Fluorecentes E3', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
                Aparatos_C.loc['Fluorecentes E3', 'Adicional'] = InfoLum.filter(regex='adicional')[0]
                Aparatos_C.loc['Fluorecentes E3', 'Funcion'] = InfoLum.filter(regex='funcion')[0]

                Aparatos_C.loc['Fluorecentes E3', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
                Aparatos_C.loc['Fluorecentes E3', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
                Aparatos_C.loc['Fluorecentes E3', 'Apagador'] = InfoLum.filter(regex='apagador')[0]

            if i == 'tira_led':
                InfoLum = InfoEsc.filter(regex='tira')
                Aparatos_C.loc['Tira E3', 'Tecnologia'] = 'led'
                Aparatos_C.loc['Tira E3', 'Lugar'] = Lugar(lugar)
                Aparatos_C.loc['Tira E3', 'LugarES'] = lugar_especifico
                Aparatos_C.loc['Tira E3', 'Fuga'] = fuga
                Aparatos_C.loc['Tira E3', 'FugaDET'] = fugadetalles
                Aparatos_C.loc['Tira E3', 'Standby'] = standby
                Aparatos_C.loc['Tira E3', 'Sobreilum'] = sobreilum
                Aparatos_C.loc['Tira E3', 'Notas'] = notas

                Aparatos_C.loc['Tira E3', 'Numero'] = InfoLum.filter(regex='numero')[0]
                Aparatos_C.loc['Tira E3', 'Fundidos'] = InfoLum.filter(regex='fundidos')[0]
                Aparatos_C.loc['Tira E3', 'Total'] = InfoLum.filter(regex='total')[0]
                Aparatos_C.loc['Tira E3', 'Combinacion'] = InfoLum.filter(regex='cobinacion')[0]
                Aparatos_C.loc['Tira E3', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
                Aparatos_C.loc['Tira E3', 'DobCodigo'] = InfoLum.filter(regex='doblecodigo')[0]
                if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                    Aparatos_C.loc['Tira E3', 'CodigoN'] = InfoLum.filter(regex='codigofindero_')[0]
                else:
                    Aparatos_C.loc['Tira E3', 'CodigoN'] = InfoLum.filter(regex='codigofindero2_')[0]
                Aparatos_C.loc['Tira E3', 'Gasto'] = InfoLum.filter(regex='gasto')[0]
                Aparatos_C.loc['Tira E3', 'TipoyTam'] = 'Led'
                # Aparatos_C.loc['Tira E1', 'Acceso']            = InfoLum.filter(regex='acceso')[0]
                # Aparatos_C.loc['Tira E1', 'Adecuaciones']      = InfoLum.filter(regex='adecuaciones')[0]
                # Aparatos_C.loc['Tira E1', 'Apagador']          = InfoLum.filter(regex='apagador')[0]

            if i == 'led':
                InfoLum = InfoEsc.filter(regex='led')
                Aparatos_C.loc['LED E3', 'Tecnologia'] = 'led'
                Aparatos_C.loc['LED E3', 'Lugar'] = Lugar(lugar)
                Aparatos_C.loc['LED E3', 'LugarES'] = lugar_especifico
                Aparatos_C.loc['LED E3', 'Fuga'] = fuga
                Aparatos_C.loc['LED E3', 'FugaDET'] = fugadetalles
                Aparatos_C.loc['LED E3', 'Standby'] = standby
                Aparatos_C.loc['LED E3', 'Sobreilum'] = sobreilum
                Aparatos_C.loc['LED E3', 'Notas'] = notas

                Aparatos_C.loc['LED E3', 'Numero'] = InfoLum.filter(regex='numero')[0]
                Aparatos_C.loc['LED E3', 'Fundidos'] = InfoLum.filter(regex='fundidos')[0]
                Aparatos_C.loc['LED E3', 'Total'] = InfoLum.filter(regex='total')[0]
                Aparatos_C.loc['LED E3', 'Combinacion'] = InfoLum.filter(regex='cobinacion')[0]
                Aparatos_C.loc['LED E3', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
                Aparatos_C.loc['LED E3', 'DobCodigo'] = InfoLum.filter(regex='doblecodigo')[0]
                if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                    Aparatos_C.loc['LED E3', 'CodigoN'] = InfoLum.filter(regex='codigofindero_')[0]
                else:
                    Aparatos_C.loc['LED E3', 'CodigoN'] = InfoLum.filter(regex='codigofindero2_')[0]
                Aparatos_C.loc['LED E3', 'Gasto'] = InfoLum.filter(regex='gasto')[0]

                # Aparatos_C.loc['LED', 'Acceso']         = InfoLum.filter(regex='acceso')[0]
                # Aparatos_C.loc['LED', 'Adecuaciones']   = InfoLum.filter(regex='adecuaciones')[0]
                # Aparatos_C.loc['LED', 'apagador']       = InfoLum.filter(regex='apagador')[0]



###################################################################################################################
        Esce4 = InfoEquipos.filter(regex='esce4_existencia_c_i')

        if Esce4[0] == 'si':

            InfoEsc = InfoEquipos.filter(regex='esce4')
            if InfoEsc.filter(regex='lugar')[0] == 'otro':
                lugar = InfoEsc.filter(regex='lugar_extra')[0]
            else:
                lugar = InfoEsc.filter(regex='lugar')[0]
            lugar_especifico = InfoEsc.filter(regex='lugar_especifico')[0]
            if lugar_especifico == 'otro':
                lugar_especifico = Lugar(InfoEsc.filter(regex='lugar_otro_c_i')[0])
            else:
                lugar_especifico = Lugar(lugar_especifico)

            tec = InfoEsc.filter(regex='tecnologia')[0]
            fuga = InfoEsc.filter(regex='fugaluces')[0]
            fugadetalles = InfoEsc.filter(regex='fugaluces_detalles')[0]
            standby = InfoEsc.filter(regex='standby')[0]
            sobreilum = InfoEsc.filter(regex='sobreilum')[0]
            notas = InfoEsc.filter(regex='notas')[0]
            tec = tec.split()

            for i in tec:
                if i == 'incandescente':
                    InfoLum = InfoEsc.filter(regex='incandescentes')
                    Aparatos_C.loc['Incandecentes E4', 'Tecnologia'] = 'incandescente'
                    Aparatos_C.loc['Incandecentes E4', 'Lugar'] = Lugar(lugar)
                    Aparatos_C.loc['Incandecentes E4', 'LugarES'] = lugar_especifico
                    Aparatos_C.loc['Incandecentes E4', 'Fuga'] = fuga
                    Aparatos_C.loc['Incandecentes E4', 'FugaDET'] = fugadetalles
                    Aparatos_C.loc['Incandecentes E4', 'Standby'] = standby
                    Aparatos_C.loc['Incandecentes E4', 'Sobreilum'] = sobreilum
                    Aparatos_C.loc['Incandecentes E4', 'Notas'] = notas

                    Aparatos_C.loc['Incandecentes E4', 'Numero'] = InfoLum.filter(regex='numero')[0]
                    Aparatos_C.loc['Incandecentes E4', 'Fundidos'] = InfoLum.filter(regex='fundidos')[0]
                    Aparatos_C.loc['Incandecentes E4', 'Total'] = InfoLum.filter(regex='total')[0]
                    Aparatos_C.loc['Incandecentes E4', 'Combinacion'] = InfoLum.filter(regex='cobinacion')[0]
                    Aparatos_C.loc['Incandecentes E4', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
                    Aparatos_C.loc['Incandecentes E4', 'DobCodigo'] = InfoLum.filter(regex='doblecodigo')[0]
                    if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                        Aparatos_C.loc['Incandecentes E4', 'CodigoN'] = InfoLum.filter(regex='codigofindero_')[0]
                    else:
                        Aparatos_C.loc['Incandecentes E4', 'CodigoN'] = InfoLum.filter(regex='codigofindero2_')[0]
                    Aparatos_C.loc['Incandecentes E4', 'Gasto'] = InfoLum.filter(regex='gasto')[0]
                    Aparatos_C.loc['Incandecentes E4', 'Donde'] = InfoLum.filter(regex='donde_c_i')[0]
                    Aparatos_C.loc['Incandecentes E4', 'DondeDetalle'] = InfoLum.filter(regex='donde_detalle')[0]
                    Aparatos_C.loc['Incandecentes E4', 'Cajillo'] = InfoLum.filter(regex='cajillo')[0]
                    Aparatos_C.loc['Incandecentes E4', 'Varios'] = InfoLum.filter(regex='varios')[0]
                    Aparatos_C.loc['Incandecentes E4', 'TipoyTam'] = InfoLum.filter(regex='tipoytam')[0]
                    Aparatos_C.loc['Incandecentes E4', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
                    Aparatos_C.loc['Incandecentes E4', 'Adicional'] = InfoLum.filter(regex='adicional')[0]
                    Aparatos_C.loc['Incandecentes E4', 'Funcion'] = InfoLum.filter(regex='funcion')[0]

                    Aparatos_C.loc['Incandecentes E4', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
                    Aparatos_C.loc['Incandecentes E4', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
                    Aparatos_C.loc['Incandecentes E4', 'Apagador'] = InfoLum.filter(regex='apagador')[0]

                if i == 'hal_geno':
                    InfoLum = InfoEsc.filter(regex='halogenos')
                    Aparatos_C.loc['Halogenos E4', 'Tecnologia'] = 'halogena'
                    Aparatos_C.loc['Halogenos E4', 'Lugar'] = Lugar(lugar)
                    Aparatos_C.loc['Halogenos E4', 'LugarES'] = lugar_especifico
                    Aparatos_C.loc['Halogenos E4', 'Fuga'] = fuga
                    Aparatos_C.loc['Halogenos E4', 'FugaDET'] = fugadetalles
                    Aparatos_C.loc['Halogenos E4', 'Standby'] = standby
                    Aparatos_C.loc['Halogenos E4', 'Sobreilum'] = sobreilum
                    Aparatos_C.loc['Halogenos E4', 'Notas'] = notas

                    Aparatos_C.loc['Halogenos E4', 'Numero'] = InfoLum.filter(regex='numero')[0]
                    Aparatos_C.loc['Halogenos E4', 'Fundidos'] = InfoLum.filter(regex='fundidos')[0]
                    Aparatos_C.loc['Halogenos E4', 'Total'] = InfoLum.filter(regex='total')[0]
                    Aparatos_C.loc['Halogenos E4', 'Combinacion'] = InfoLum.filter(regex='cobinacion')[0]
                    Aparatos_C.loc['Halogenos E4', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
                    Aparatos_C.loc['Halogenos E4', 'DobCodigo'] = InfoLum.filter(regex='doblecodigo')[0]
                    if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                        Aparatos_C.loc['Halogenos E4', 'CodigoN'] = InfoLum.filter(regex='codigofindero_')[0]
                    else:
                        Aparatos_C.loc['Halogenos E4', 'CodigoN'] = InfoLum.filter(regex='codigofindero2_')[0]
                    Aparatos_C.loc['Halogenos E4', 'Gasto'] = InfoLum.filter(regex='gasto')[0]
                    Aparatos_C.loc['Halogenos E4', 'Donde'] = InfoLum.filter(regex='donde_c_i')[0]
                    Aparatos_C.loc['Halogenos E4', 'DondeDetalle'] = InfoLum.filter(regex='donde_detalle')[0]
                    Aparatos_C.loc['Halogenos E4', 'Cajillo'] = InfoLum.filter(regex='cajillo')[0]
                    Aparatos_C.loc['Halogenos E4', 'Varios'] = InfoLum.filter(regex='varios')[0]
                    Aparatos_C.loc['Halogenos E4', 'TipoyTam'] = InfoLum.filter(regex='tipoytam')[0]
                    Aparatos_C.loc['Halogenos E4', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
                    Aparatos_C.loc['Halogenos E4', 'Adicional'] = InfoLum.filter(regex='adicional')[0]
                    Aparatos_C.loc['Halogenos E4', 'Funcion'] = InfoLum.filter(regex='funcion')[0]

                    Aparatos_C.loc['Halogenos E4', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
                    Aparatos_C.loc['Halogenos E4', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
                    Aparatos_C.loc['Halogenos E4', 'Apagador'] = InfoLum.filter(regex='apagador')[0]

                if i == 'fluorescente':
                    InfoLum = InfoEsc.filter(regex='fluorescentes')
                    Aparatos_C.loc['Fluorecentes E4', 'Tecnologia'] = 'fluorescente'
                    Aparatos_C.loc['Fluorecentes E4', 'Lugar'] = Lugar(lugar)
                    Aparatos_C.loc['Fluorecentes E4', 'LugarES'] = lugar_especifico
                    Aparatos_C.loc['Fluorecentes E4', 'Fuga'] = fuga
                    Aparatos_C.loc['Fluorecentes E4', 'FugaDET'] = fugadetalles
                    Aparatos_C.loc['Fluorecentes E4', 'Standby'] = standby
                    Aparatos_C.loc['Fluorecentes E4', 'Sobreilum'] = sobreilum
                    Aparatos_C.loc['Fluorecentes E4', 'Notas'] = notas

                    Aparatos_C.loc['Fluorecentes E4', 'Numero'] = InfoLum.filter(regex='numero')[0]
                    Aparatos_C.loc['Fluorecentes E4', 'Fundidos'] = InfoLum.filter(regex='fundidos')[0]
                    Aparatos_C.loc['Fluorecentes E4', 'Total'] = InfoLum.filter(regex='total')[0]
                    Aparatos_C.loc['Fluorecentes E4', 'Combinacion'] = InfoLum.filter(regex='cobinacion')[0]
                    Aparatos_C.loc['Fluorecentes E4', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
                    Aparatos_C.loc['Fluorecentes E4', 'DobCodigo'] = InfoLum.filter(regex='doblecodigo')[0]
                    if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                        Aparatos_C.loc['Fluorecentes E4', 'CodigoN'] = InfoLum.filter(regex='codigofindero_')[0]
                    else:
                        Aparatos_C.loc['Fluorecentes E4', 'CodigoN'] = InfoLum.filter(regex='codigofindero2_')[0]
                    Aparatos_C.loc['Fluorecentes E4', 'Gasto'] = InfoLum.filter(regex='gasto')[0]

                    Aparatos_C.loc['Fluorecentes E4', 'Donde'] = InfoLum.filter(regex='donde_c_i')[0]
                    Aparatos_C.loc['Fluorecentes E4', 'DondeDetalle'] = InfoLum.filter(regex='donde_detalle')[0]
                    Aparatos_C.loc['Fluorecentes E4', 'Cajillo'] = InfoLum.filter(regex='cajillo')[0]
                    Aparatos_C.loc['Fluorecentes E4', 'Varios'] = InfoLum.filter(regex='varios')[0]
                    Aparatos_C.loc['Fluorecentes E4', 'TipoyTam'] = InfoLum.filter(regex='tipoytam')[0]
                    Aparatos_C.loc['Fluorecentes E4', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
                    Aparatos_C.loc['Fluorecentes E4', 'Adicional'] = InfoLum.filter(regex='adicional')[0]
                    Aparatos_C.loc['Fluorecentes E4', 'Funcion'] = InfoLum.filter(regex='funcion')[0]

                    Aparatos_C.loc['Fluorecentes E4', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
                    Aparatos_C.loc['Fluorecentes E4', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
                    Aparatos_C.loc['Fluorecentes E4', 'Apagador'] = InfoLum.filter(regex='apagador')[0]

                if i == 'tira_led':
                    InfoLum = InfoEsc.filter(regex='tira')
                    Aparatos_C.loc['Tira E4', 'Tecnologia'] = 'led'
                    Aparatos_C.loc['Tira E4', 'Lugar'] = Lugar(lugar)
                    Aparatos_C.loc['Tira E4', 'LugarES'] = lugar_especifico
                    Aparatos_C.loc['Tira E4', 'Fuga'] = fuga
                    Aparatos_C.loc['Tira E4', 'FugaDET'] = fugadetalles
                    Aparatos_C.loc['Tira E4', 'Standby'] = standby
                    Aparatos_C.loc['Tira E4', 'Sobreilum'] = sobreilum
                    Aparatos_C.loc['Tira E4', 'Notas'] = notas

                    Aparatos_C.loc['Tira E4', 'Numero'] = InfoLum.filter(regex='numero')[0]
                    Aparatos_C.loc['Tira E4', 'Fundidos'] = InfoLum.filter(regex='fundidos')[0]
                    Aparatos_C.loc['Tira E4', 'Total'] = InfoLum.filter(regex='total')[0]
                    Aparatos_C.loc['Tira E4', 'Combinacion'] = InfoLum.filter(regex='cobinacion')[0]
                    Aparatos_C.loc['Tira E4', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
                    Aparatos_C.loc['Tira E4', 'DobCodigo'] = InfoLum.filter(regex='doblecodigo')[0]
                    if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                        Aparatos_C.loc['Tira E4', 'CodigoN'] = InfoLum.filter(regex='codigofindero_')[0]
                    else:
                        Aparatos_C.loc['Tira E4', 'CodigoN'] = InfoLum.filter(regex='codigofindero2_')[0]
                    Aparatos_C.loc['Tira E4', 'Gasto'] = InfoLum.filter(regex='gasto')[0]
                    Aparatos_C.loc['Tira E4', 'TipoyTam'] = 'Led'
                    # Aparatos_C.loc['Tira E1', 'Acceso']            = InfoLum.filter(regex='acceso')[0]
                    # Aparatos_C.loc['Tira E1', 'Adecuaciones']      = InfoLum.filter(regex='adecuaciones')[0]
                    # Aparatos_C.loc['Tira E1', 'Apagador']          = InfoLum.filter(regex='apagador')[0]

                if i == 'led':
                    InfoLum = InfoEsc.filter(regex='led')
                    Aparatos_C.loc['LED E4', 'Tecnologia'] = 'led'
                    Aparatos_C.loc['LED E4', 'Lugar'] = Lugar(lugar)
                    Aparatos_C.loc['LED E4', 'LugarES'] = lugar_especifico
                    Aparatos_C.loc['LED E4', 'Fuga'] = fuga
                    Aparatos_C.loc['LED E4', 'FugaDET'] = fugadetalles
                    Aparatos_C.loc['LED E4', 'Standby'] = standby
                    Aparatos_C.loc['LED E4', 'Sobreilum'] = sobreilum
                    Aparatos_C.loc['LED E4', 'Notas'] = notas

                    Aparatos_C.loc['LED E4', 'Numero'] = InfoLum.filter(regex='numero')[0]
                    Aparatos_C.loc['LED E4', 'Fundidos'] = InfoLum.filter(regex='fundidos')[0]
                    Aparatos_C.loc['LED E4', 'Total'] = InfoLum.filter(regex='total')[0]
                    Aparatos_C.loc['LED E4', 'Combinacion'] = InfoLum.filter(regex='cobinacion')[0]
                    Aparatos_C.loc['LED E4', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
                    Aparatos_C.loc['LED E4', 'DobCodigo'] = InfoLum.filter(regex='doblecodigo')[0]
                    if InfoLum.filter(regex='doblecodigo')[0] == 'no':
                        Aparatos_C.loc['LED E4', 'CodigoN'] = InfoLum.filter(regex='codigofindero_')[0]
                    else:
                        Aparatos_C.loc['LED E4', 'CodigoN'] = InfoLum.filter(regex='codigofindero2_')[0]
                    Aparatos_C.loc['LED E4', 'Gasto'] = InfoLum.filter(regex='gasto')[0]
                    Aparatos_C.loc['LED E4', 'TipoyTam'] = 'Led'
                    # Aparatos_C.loc['LED', 'Acceso']         = InfoLum.filter(regex='acceso')[0]
                    # Aparatos_C.loc['LED', 'Adecuaciones']   = InfoLum.filter(regex='adecuaciones')[0]
                    # Aparatos_C.loc['LED', 'apagador']       = InfoLum.filter(regex='apagador')[0]


    Aparatos_C.replace('hal_geno', 'halogena',inplace=True)
    Aparatos = Aparatos_C[Aparatos_C['Tecnologia'].notna()]
    Aparatos.reset_index()

    print(Aparatos['TipoyTam'])

    return Aparatos
