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
    Aparatos_C = pd.DataFrame(index=['E1 Lum1','E1 Lum2','E1 Lum3','E2 Lum1','E2 Lum2','E2 Lum3','E3 Lum1','E3 Lum2','E3 Lum3'],
                              columns=['Lugar', 'Lugar Especifico','Tecnologia', 'Consumo', 'Numero','Fundidos', 'Tamano','Entrada',
                                       'Sobreiluminacion','Acceso','Adecuaciones','Adicional','Existencia','DondeAD','Cajillo',
                                       'Apagador' ,'Notas','CodigoN','CodigoS','Standby'])
    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Circuito[Columnas.str.contains("iluminacion", case=False)]

####Lum1
    InfoEsce = InfoEquipos.filter(regex='esce1')
    InfoLum = InfoEsce.filter(regex='luminaria1')


    if InfoLum.filter(regex='lugar')[0] == 'otro':
        lugar = InfoLum.filter(regex='lugar_extra')[0]
    else:
        lugar = InfoLum.filter(regex='lugar')[0]
    Aparatos_C.loc['E1 Lum1', 'Lugar']                = Lugar(lugar)

    lugar_especifico                                  = InfoLum.filter(regex='lugar_especifico')[0]
    if lugar_especifico=='otro':
        Aparatos_C.loc['E1 Lum1', 'Lugar Especifico'] = Lugar(InfoLum.filter(regex='lugar_otro_c_i')[0])
    else:
        Aparatos_C.loc['E1 Lum1', 'Lugar Especifico'] = Lugar(lugar_especifico)

    if InfoLum.filter(regex='tipoytam')[0] == 'otro':
        Aparatos_C.loc['E1 Lum1', 'Tamano']          = InfoLum.filter(regex='tipoytam_otro')[0]
    else:
        Aparatos_C.loc['E1 Lum1', 'Tamano']         = InfoLum.filter(regex='tipoytam')[0]

    if InfoLum.filter(regex='entrada')[0] == 'otro':
        Aparatos_C.loc['E1 Lum1', 'Entrada']        = InfoLum.filter(regex='entrada_otro')[0]
    else:
        Aparatos_C.loc['E1 Lum1', 'Entrada']        = InfoLum.filter(regex='entrada')[0]

    if InfoLum.filter(regex='acceso')[0] == 'otro':
        Aparatos_C.loc['E1 Lum1', 'Acceso'] = InfoLum.filter(regex='acceso_otro')[0]
    else:
        Aparatos_C.loc['E1 Lum1', 'Acceso'] = InfoLum.filter(regex='acceso')[0]

    if InfoLum.filter(regex='donde')[0] == 'otro':
        Aparatos_C.loc['E1 Lum1', 'DondeAD'] = InfoLum.filter(regex='donde_otro')[0]
    else:
        Aparatos_C.loc['E1 Lum1', 'DondeAD'] = InfoLum.filter(regex='donde')[0]

    Aparatos_C.loc['E1 Lum1', 'Tecnologia']         = InfoLum.filter(regex='tecnologia')[0]

    Aparatos_C.loc['E1 Lum1', 'Numero']             = InfoLum.filter(regex='numero')[0]
    Aparatos_C.loc['E1 Lum1', 'Sobreiluminacion']   = InfoLum.filter(regex='sobreilum')[0]
    Aparatos_C.loc['E1 Lum1', 'Adecuaciones']       = InfoLum.filter(regex='adecuaciones')[0]
    Aparatos_C.loc['E1 Lum1', 'DondeAD']            = InfoLum.filter(regex='donde')[0]
    Aparatos_C.loc['E1 Lum1', 'Cajillo']            = InfoLum.filter(regex='cajillo')[0]
    Aparatos_C.loc['E1 Lum1', 'Apagador']           = InfoLum.filter(regex='apagador')[0]
    Aparatos_C.loc['E1 Lum1', 'Notas']              = InfoLum.filter(regex='notas_c_i')[0]
    standbby=InfoLum.filter(regex='standby_c_i')[0]


    if not InfoLum.filter(regex='standby_c_i').empty:
        Aparatos_C.loc['E1 Lum1', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
        Aparatos_C.loc['E1 Lum1', 'CodigoN'] = InfoLum.filter(regex='codigofindero')[0]
    else:
        Aparatos_C.loc['E1 Lum1', 'CodigoS'] = InfoLum.filter(regex='standby')[0]
        Aparatos_C.loc['E1 Lum1', 'Standby'] = consumoEq(InfoLum.filter(regex='consumo')[0])

    Aparatos_C.loc['E1 Lum1', 'Existencia']         = 1



    if not InfoLum.filter(regex='adicional_c_i').empty:
        Aparatos_C.loc['E1 Lum1', 'Adicional'] = InfoLum.filter(regex='adicional_c_i')[0]







########Lum 2 #############################################################################################################
    if InfoEsce.filter(regex='otros1')[0] == 'si':
        Aparatos_C.loc['E1 Lum2', 'Existencia'] = 1

        InfoLum = InfoEsce.filter(regex='luminaria2')




        Aparatos_C.loc['E1 Lum2', 'Lugar'] = Lugar(lugar)





        Aparatos_C.loc['E1 Lum2', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
        Aparatos_C.loc['E1 Lum2', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
        Aparatos_C.loc['E1 Lum2', 'Numero'] = InfoLum.filter(regex='numero')[0]
        Aparatos_C.loc['E1 Lum2', 'Tamano'] = InfoLum.filter(regex='tipoytam')[0]
        if InfoLum.filter(regex='entrada')[0] == 'otro':
            Aparatos_C.loc['E1 Lum2', 'Entrada'] = InfoLum.filter(regex='entrada_otro')[0]
        else:
            Aparatos_C.loc['E1 Lum2', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
        Aparatos_C.loc['E1 Lum2', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
        Aparatos_C.loc['E1 Lum2', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
        Aparatos_C.loc['E1 Lum2', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
        Aparatos_C.loc['E1 Lum2', 'Notas'] = InfoLum.filter(regex='notas_c_i')[0]
        Aparatos_C.loc['E1 Lum2', 'CodigoN'] = InfoLum.filter(regex='codigofindero')[0]
        if not InfoLum.filter(regex='adicional_c_i').empty:
            Aparatos_C.loc['E1 Lum2', 'Adicional'] = InfoLum.filter(regex='adicional_c_i')[0]

    if InfoEsce.filter(regex='otros2')[0] == 'si':
        Aparatos_C.loc['E1 Lum3', 'Existencia'] = 1
        InfoLum = InfoEsce.filter(regex='luminaria3')
        Aparatos_C.loc['E1 Lum3', 'Lugar'] = Lugar(lugar)
        Aparatos_C.loc['E1 Lum3', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
        Aparatos_C.loc['E1 Lum3', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
        Aparatos_C.loc['E1 Lum3', 'Numero'] = InfoLum.filter(regex='numero')[0]
        Aparatos_C.loc['E1 Lum3', 'Tamano'] = InfoLum.filter(regex='tipoytam')[0]
        if InfoLum.filter(regex='entrada')[0] == 'otro':
            Aparatos_C.loc['E1 Lum3', 'Entrada'] = InfoLum.filter(regex='entrada_otro')[0]
        else:
            Aparatos_C.loc['E1 Lum3', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
        Aparatos_C.loc['E1 Lum3', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
        Aparatos_C.loc['E1 Lum3', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
        Aparatos_C.loc['E1 Lum3', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
        Aparatos_C.loc['E1 Lum3', 'Notas'] = InfoLum.filter(regex='notas_c_i')[0]
        Aparatos_C.loc['E1 Lum3', 'CodigoN'] = InfoLum.filter(regex='codigofindero')[0]
        if not InfoLum.filter(regex='adicional_c_i').empty:
            Aparatos_C.loc['E1 Lum3', 'Adicional'] = InfoLum.filter(regex='adicional_c_i')[0]

    if InfoEquipos.filter(regex='adicionalesce')[0] == 'si':
        Aparatos_C.loc['E2 Lum1', 'Existencia'] = 1

        InfoEsce = InfoEquipos.filter(regex='esce2')
        InfoLum = InfoEsce.filter(regex='luminaria1')

        if InfoLum.filter(regex='lugar')[0] == 'otro':
            lugar = InfoLum.filter(regex='lugar_extra')[0]
        else:
            lugar = InfoLum.filter(regex='lugar')[0]
        Aparatos_C.loc['E2 Lum1', 'Lugar'] = Lugar(lugar)
        lugar_especifico = InfoLum.filter(regex='lugar_especifico')[0]
        if lugar_especifico=='otro':
            Aparatos_C.loc['E2 Lum1', 'Lugar Especifico'] = Lugar(InfoLum.filter(regex='lugar_otro_c_i')[0])
        else:
            Aparatos_C.loc['E2 Lum1', 'Lugar Especifico'] = Lugar(lugar_especifico)

        Aparatos_C.loc['E2 Lum1', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
        Aparatos_C.loc['E2 Lum1', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
        Aparatos_C.loc['E2 Lum1', 'Numero'] = InfoLum.filter(regex='numero')[0]
        Aparatos_C.loc['E2 Lum1', 'Tamano'] =InfoLum.filter(regex='tipoytam')[0]
        if InfoLum.filter(regex='entrada')[0] == 'otro':
            Aparatos_C.loc['E2 Lum1', 'Entrada'] = InfoLum.filter(regex='entrada_otro')[0]
        else:
            Aparatos_C.loc['E2 Lum1', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
        Aparatos_C.loc['E2 Lum1', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
        Aparatos_C.loc['E2 Lum1', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
        Aparatos_C.loc['E2 Lum1', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
        Aparatos_C.loc['E2 Lum1', 'Notas'] = InfoLum.filter(regex='notas_c_i')[0]
        Aparatos_C.loc['E2 Lum1', 'CodigoN'] = InfoLum.filter(regex='codigofindero')[0]
        if not InfoLum.filter(regex='adicional_c_i').empty:
            Aparatos_C.loc['E2 Lum1', 'Adicional'] = InfoLum.filter(regex='adicional_c_i')[0]

        if InfoEsce.filter(regex='otros1')[0] == 'si':
            Aparatos_C.loc['E2 Lum2', 'Existencia'] = 1

            InfoLum = InfoEsce.filter(regex='luminaria2')
            Aparatos_C.loc['E2 Lum2', 'Lugar'] = Lugar(lugar)
            Aparatos_C.loc['E2 Lum2', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
            Aparatos_C.loc['E2 Lum2', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
            Aparatos_C.loc['E2 Lum2', 'Numero'] = InfoLum.filter(regex='numero')[0]
            Aparatos_C.loc['E2 Lum2', 'Tamano'] = InfoLum.filter(regex='tipoytam')[0]
            if InfoLum.filter(regex='entrada')[0] == 'otro':
                Aparatos_C.loc['E2 Lum2', 'Entrada'] = InfoLum.filter(regex='entrada_otro')[0]
            else:
                Aparatos_C.loc['E2 Lum2', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
            Aparatos_C.loc['E2 Lum2', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
            Aparatos_C.loc['E2 Lum2', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
            Aparatos_C.loc['E2 Lum2', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
            Aparatos_C.loc['E2 Lum2', 'Notas'] = InfoLum.filter(regex='notas_c_i')[0]
            Aparatos_C.loc['E2 Lum2', 'CodigoN'] = InfoLum.filter(regex='codigofindero')[0]
            if not InfoLum.filter(regex='adicional_c_i').empty:
                Aparatos_C.loc['E2 Lum2', 'Adicional'] = InfoLum.filter(regex='adicional_c_i')[0]

        if InfoEsce.filter(regex='otros2')[0] == 'si':
            Aparatos_C.loc['E2 Lum3', 'Existencia'] = 1

            InfoLum = InfoEsce.filter(regex='luminaria3')
            Aparatos_C.loc['E2 Lum3', 'Lugar'] = Lugar(lugar)
            Aparatos_C.loc['E2 Lum3', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
            Aparatos_C.loc['E2 Lum3', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
            Aparatos_C.loc['E2 Lum3', 'Numero'] = InfoLum.filter(regex='numero')[0]
            Aparatos_C.loc['E2 Lum3', 'Tamano'] = InfoLum.filter(regex='tipoytam')[0]
            if InfoLum.filter(regex='entrada')[0] == 'otro':
                Aparatos_C.loc['E2 Lum3', 'Entrada'] = InfoLum.filter(regex='entrada_otro')[0]
            else:
                Aparatos_C.loc['E2 Lum3', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
            Aparatos_C.loc['E2 Lum3', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
            Aparatos_C.loc['E2 Lum3', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
            Aparatos_C.loc['E2 Lum3', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
            Aparatos_C.loc['E2 Lum3', 'Notas'] = InfoLum.filter(regex='notas_c_i')[0]
            Aparatos_C.loc['E2 Lum3', 'CodigoN'] = InfoLum.filter(regex='codigofindero')[0]
            if not InfoLum.filter(regex='adicional_c_i').empty:
                Aparatos_C.loc['E2 Lum3', 'Adicional'] = InfoLum.filter(regex='adicional_c_i')[0]

    if InfoEquipos.filter(regex='adicionalesce1')[0] == 'si':
        Aparatos_C.loc['E3 Lum1', 'Existencia'] = 1

        InfoEsce = InfoEquipos.filter(regex='esce3')
        InfoLum = InfoEsce.filter(regex='luminaria1')
        if InfoLum.filter(regex='lugar')[0] == 'otro':
            lugar = InfoLum.filter(regex='lugar_extra')[0]
        else:
            lugar = InfoLum.filter(regex='lugar')[0]
        Aparatos_C.loc['E3 Lum1', 'Lugar'] = Lugar(lugar)

        lugar_especifico = InfoLum.filter(regex='lugar_especifico')[0]
        if lugar_especifico == 'otro':
            Aparatos_C.loc['E3 Lum1', 'Lugar Especifico'] = Lugar(InfoLum.filter(regex='lugar_otro_c_i')[0])
        else:
            Aparatos_C.loc['E3 Lum1', 'Lugar Especifico'] = Lugar(lugar_especifico)
        Aparatos_C.loc['E3 Lum1', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
        Aparatos_C.loc['E3 Lum1', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
        Aparatos_C.loc['E3 Lum1', 'Numero'] = InfoLum.filter(regex='numero')[0]
        Aparatos_C.loc['E3 Lum1', 'Tamano'] = InfoLum.filter(regex='tipoytam')[0]
        if InfoLum.filter(regex='entrada')[0] == 'otro':
            Aparatos_C.loc['E3 Lum1', 'Entrada'] = InfoLum.filter(regex='entrada_otro')[0]
        else:
            Aparatos_C.loc['E3 Lum1', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
        Aparatos_C.loc['E3 Lum1', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
        Aparatos_C.loc['E3 Lum1', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
        Aparatos_C.loc['E3 Lum1', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
        Aparatos_C.loc['E3 Lum1', 'Notas'] = InfoLum.filter(regex='notas_c_i')[0]
        Aparatos_C.loc['E3 Lum1', 'CodigoN'] = InfoLum.filter(regex='codigofindero')[0]
        if not InfoLum.filter(regex='adicional_c_i').empty:
            Aparatos_C.loc['E3 Lum1', 'Adicional'] = InfoLum.filter(regex='adicional_c_i')[0]

        if InfoEsce.filter(regex='otros1')[0] == 'si':
            Aparatos_C.loc['E3 Lum2', 'Existencia'] = 1

            InfoLum = InfoEsce.filter(regex='luminaria2')
            Aparatos_C.loc['E3 Lum2', 'Lugar'] = Lugar(lugar)
            Aparatos_C.loc['E3 Lum2', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
            Aparatos_C.loc['E3 Lum2', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
            Aparatos_C.loc['E3 Lum2', 'Numero'] = InfoLum.filter(regex='numero')[0]
            Aparatos_C.loc['E3 Lum2', 'Tamano'] = InfoLum.filter(regex='tipoytam')[0]
            if InfoLum.filter(regex='entrada')[0] == 'otro':
                Aparatos_C.loc['E3 Lum2', 'Entrada'] = InfoLum.filter(regex='entrada_otro')[0]
            else:
                Aparatos_C.loc['E3 Lum2', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
            Aparatos_C.loc['E3 Lum2', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
            Aparatos_C.loc['E3 Lum2', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
            Aparatos_C.loc['E3 Lum2', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
            Aparatos_C.loc['E3 Lum2', 'Notas'] = InfoLum.filter(regex='notas_c_i')[0]
            Aparatos_C.loc['E3 Lum2', 'CodigoN'] = InfoLum.filter(regex='codigofindero')[0]
            if not InfoLum.filter(regex='adicional_c_i').empty:
                Aparatos_C.loc['E3 Lum2', 'Adicional'] = InfoLum.filter(regex='adicional_c_i')[0]

        if InfoEsce.filter(regex='otros2')[0] == 'si':
            Aparatos_C.loc['E3 Lum3', 'Existencia'] = 1

            InfoLum = InfoEsce.filter(regex='luminaria3')
            Aparatos_C.loc['E3 Lum3', 'Lugar'] = Lugar(lugar)
            Aparatos_C.loc['E3 Lum3', 'Tecnologia'] = InfoLum.filter(regex='tecnologia')[0]
            Aparatos_C.loc['E3 Lum3', 'Consumo'] = consumoEq(InfoLum.filter(regex='consumo')[0])
            Aparatos_C.loc['E3 Lum3', 'Numero'] = InfoLum.filter(regex='numero')[0]
            Aparatos_C.loc['E3 Lum3', 'Tamano'] = InfoLum.filter(regex='tipoytam')[0]
            if InfoLum.filter(regex='entrada')[0] == 'otro':
                Aparatos_C.loc['E3 Lum3', 'Entrada'] = InfoLum.filter(regex='entrada_otro')[0]
            else:
                Aparatos_C.loc['E3 Lum3', 'Entrada'] = InfoLum.filter(regex='entrada')[0]
            Aparatos_C.loc['E3 Lum3', 'Sobreiluminacion'] = InfoLum.filter(regex='sobreilum')[0]
            Aparatos_C.loc['E3 Lum3', 'Acceso'] = InfoLum.filter(regex='acceso')[0]
            Aparatos_C.loc['E3 Lum3', 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
            Aparatos_C.loc['E3 Lum3', 'Notas'] = InfoLum.filter(regex='notas_c_i')[0]
            Aparatos_C.loc['E3 Lum3', 'CodigoN'] = InfoLum.filter(regex='codigofindero')[0]
            if not InfoLum.filter(regex='adicional_c_i').empty:
                Aparatos_C.loc['E3 Lum3', 'Adicional'] = InfoLum.filter(regex='adicional_c_i')[0]


    Aparatos_C.replace('hal_geno', 'halogena',inplace=True)
    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()

    #ahorro_luces(Aparatos)
    return Aparatos
