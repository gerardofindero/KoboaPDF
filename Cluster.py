import pandas as pd
from Consumo    import calc_consumo , consumoEq
from Correciones import Lugar
import numpy as np
from LibreriaTV import ClavesClusterTV
from libreriaReguladores import sepRegAta


def clustertv(Excel,Nocircuito,NomCircuito):

    Aparatos_C = pd.DataFrame(index=['TV','Decodificador1','Decodificador2','Regulador1','Regulador2','NoBreak','Modem','Bluray','HomeTheater'
                                     'Repetidor','Antena','Sonido','Bocinas','Surround', 'Consola1','Consola2','Equipoextra','Equipo Ahorro','Cluster']
                              ,columns=['Marca','Standby','Nominal','Lugar','Tolerancia', 'Pulgadas','Atacable','Existencia','CodigoN','CodigoS','Notas','CodigoFin','Clave','Equipos'])

    Info_C = pd.DataFrame(index=['Nombre Circuito','Ubicación', 'Notas', 'Consumo Total'],columns=['Info'])
    Info_C.loc['Nombre Circuito', 'Info'] = NomCircuito[0]
    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("clustertv", case=False)]

    EquiposCTV= Circuito[InfoEquipos]
    EquiposCTV=EquiposCTV.fillna('X')
    Equipos = EquiposCTV.filter(regex='equipos')

    indx=0
    Nominal=0

    CodStandby   = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
    #Tierra      = Circuito.filter(regex='clustertv_tierra_c_i')[0]
    #Enchufes    = Circuito.filter(regex='clustertv_enchufes_c_i')[0]
    Maniobras    = Circuito.filter(regex='clustertv_maniobras_c_i')[0]
    Maniobras_Detalles = Circuito.filter(regex='clustertv_maniobras_detalles_c_i')[0]
    Notas        = EquiposCTV.filter(regex='notas_c_i')[0]
    InfoDeco = Circuito.filter(regex='zona_c_i')[0]

    if InfoDeco == 'otro':
        Zona=Lugar(Circuito.filter(regex='zona_otro_c_i')[0])
    else:
        Zona=Lugar(InfoDeco)

    for i in Equipos:
        if i == 1:
            if indx == 1:
                ##Televisión
                NomAparato = 'tv1'
                InfoDeco = EquiposCTV.filter(regex=NomAparato)
                if InfoDeco.filter(regex='espendiente_c_i')[0]=='no':
                    Aparatos_C.loc['TV', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ')[0]
                else:
                    Aparatos_C.loc['TV', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
                    if InfoDeco.filter(regex='codigofindero2_c_i')[0]!='X':
                        Aparatos_C.loc['TV', 'CodigoN']     =Aparatos_C.loc['TV', 'CodigoN'] +','\
                                                             + InfoDeco.filter(regex='codigofindero2_c_i')[0]


                Aparatos_C.loc['TV', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                if not InfoDeco.filter(regex='clustertv_tv1_c_i')[0] == 'otro':

                    Aparatos_C.loc['TV', 'Marca'] = InfoDeco.filter(regex='clustertv_tv1_c_i')[0]
                else:
                    Aparatos_C.loc['TV', 'Marca'] = InfoDeco.filter(regex='marca_otro_c_i')[0]

                Aparatos_C.loc['TV', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['TV', 'Tolerancia'] = InfoDeco.filter(regex='tolerancia')[0]
                Aparatos_C.loc['TV', 'Pulgadas'] = InfoDeco.filter(regex='tamano')[0]
                Aparatos_C.loc['TV', 'Existencia'] = 1
                Aparatos_C.loc['TV', 'Lugar'] = Zona
                Aparatos_C.loc['TV', 'CodigoS'] =  CodStandby
                Aparatos_C.loc['TV', 'Notas'] = Notas
                if Aparatos_C.loc['TV', 'Standby'] != 0:
                    Aparatos_C.loc['TV', 'Atacable'] = 'Si'
                else:
                    Aparatos_C.loc['TV', 'Atacable'] = 'NF'
                Aparatos_C.loc['TV', 'Clave'] = ClavesClusterTV(Aparatos_C)

            if indx == 2:
            ##Decodificador
                NomAparato = 'decodificador1'
                InfoDeco = EquiposCTV.filter(regex=NomAparato)
                Aparatos_C.loc['Decodificador1', 'Existencia'] = 1
                Aparatos_C.loc['Decodificador1','Marca']   = InfoDeco.filter(regex='marca_c_i')[0]
                Aparatos_C.loc['Decodificador1', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Decodificador1', 'Atacable'] = 'Si'
                Aparatos_C.loc['Decodificador1', 'CodigoS'] =  CodStandby
                Aparatos_C.loc['Decodificador1', 'Lugar'] = Zona
                Aparatos_C.loc['Decodificador1', 'Notas'] = Notas


            if indx == 3:
            ##Modem
                NomAparato = 'modem'
                InfoDeco = EquiposCTV.filter(regex=NomAparato)
                Aparatos_C.loc['Modem', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Modem', 'Existencia'] = 1
                Aparatos_C.loc['Modem', 'Atacable'] = 'No'
                Aparatos_C.loc['Modem', 'Lugar'] = Zona
                Aparatos_C.loc['Modem', 'CodigoS'] = CodStandby
                Aparatos_C.loc['Modem', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Modem', 'Notas'] = Notas




            if indx == 4:
            ##Repetidor
                NomAparato = 'repetidor'
                InfoDeco = EquiposCTV.filter(regex=NomAparato)

                Aparatos_C.loc['Repetidor', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Repetidor', 'Existencia'] = 1
                Aparatos_C.loc['Repetidor', 'Atacable'] = 'No'
                Aparatos_C.loc['Repetidor', 'CodigoS'] =  CodStandby
                Aparatos_C.loc['Repetidor', 'Lugar'] = Zona
                Aparatos_C.loc['Repetidor', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Repetidor', 'Notas'] = Notas



            if indx == 5:
                NomAparato = 'consola1'
                InfoDeco = EquiposCTV.filter(regex=NomAparato)
                Aparatos_C.loc['Consola1', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Consola1', 'Existencia'] = 1
                Aparatos_C.loc['Consola1', 'Atacable'] = 'Si'
                Aparatos_C.loc['Consola1', 'CodigoS'] =  CodStandby
                Aparatos_C.loc['Consola1', 'Lugar'] = Zona
                Aparatos_C.loc['Consola1', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Consola1', 'Notas'] = Notas


            ##Antena
            if indx == 6:
                NomAparato = 'antena'
                InfoDeco = EquiposCTV.filter(regex=NomAparato)
                Aparatos_C.loc['Antena', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Antena', 'Existencia'] = 1
                Aparatos_C.loc['Antena', 'Atacable'] = 'Si'
                Aparatos_C.loc['Antena', 'CodigoS'] =  CodStandby
                Aparatos_C.loc['Antena', 'Lugar'] = Zona
                Aparatos_C.loc['Antena', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Antena', 'Notas'] = Notas

            # Sonido
            if indx == 7:
                NomAparato = 'sonido'
                InfoDeco = EquiposCTV.filter(regex=NomAparato)
                Aparatos_C.loc['Sonido', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Sonido', 'Existencia'] = 1
                Aparatos_C.loc['Sonido', 'Atacable'] = 'Si'
                Aparatos_C.loc['Sonido', 'CodigoN'] = 'X'
                Aparatos_C.loc['Sonido', 'CodigoS'] =  CodStandby
                Aparatos_C.loc['Sonido', 'Lugar'] = Zona
                Aparatos_C.loc['Sonido', 'Tolerancia']=False
                Aparatos_C.loc['Sonido', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Sonido', 'Notas'] = Notas


            ##Bocinas
            if indx == 8:
                NomAparato = 'bocina'
                # Aparatos_C.loc['Bocinas', 'Aparatos'] = NomAparato
                InfoDeco = EquiposCTV.filter(regex=NomAparato)
                Aparatos_C.loc['Bocinas', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                if Aparatos_C.loc['Bocinas', 'Marca']=='otro':
                    Aparatos_C.loc['Bocinas', 'Marca'] = InfoDeco.filter(regex='marca_otro')[0]
                Aparatos_C.loc['Bocinas', 'Existencia'] = InfoDeco.filter(regex='numero')[0]
                Aparatos_C.loc['Bocinas', 'Atacable'] = 'Si'
                Aparatos_C.loc['Bocinas', 'CodigoS'] =  CodStandby
                Aparatos_C.loc['Bocinas', 'Lugar'] = Zona
                Aparatos_C.loc['Bocinas', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Bocinas', 'Notas'] = Notas

            # Blueray
            if indx == 9:
                print('BLUERAY')
                NomAparato = 'bluray'
                InfoDeco = EquiposCTV.filter(regex=NomAparato)
                tipo= InfoDeco.filter(regex='tipo')[0]
                Aparatos_C.loc['Bluray', 'CodigoS'] = CodStandby
                InfoDeco = Circuito.filter(regex=tipo)
                Aparatos_C.loc['Bluray', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                if Aparatos_C.loc['Bluray', 'Marca'] == 'otro':
                    Aparatos_C.loc['Bluray', 'Marca'] = InfoDeco.filter(regex='marca_otro')[0]
                Aparatos_C.loc['Bluray', 'Existencia'] = 1
                Aparatos_C.loc['Bluray', 'Atacable'] = 'Si'
                Aparatos_C.loc['Bluray', 'Lugar'] = Zona
                Aparatos_C.loc['Bluray', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Bluray', 'Notas'] = Notas

            ##Decodificador2
            if indx == 10:
                NomAparato = 'decodificador2'
                # Aparatos_C.loc['Decodificador2', 'Aparatos'] = NomAparato
                InfoDeco = EquiposCTV.filter(regex=NomAparato)
                if InfoDeco.filter(regex='marca')[0] == 'otro':
                    Aparatos_C.loc['Decodificador2', 'Marca'] = InfoDeco.filter(regex='otro')[0]
                else:
                    Aparatos_C.loc['Decodificador2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Decodificador2', 'CodigoS'] = CodStandby
                Aparatos_C.loc['Decodificador2', 'Existencia'] = 1
                Aparatos_C.loc['Decodificador2', 'Atacable'] = 'Si'
                Aparatos_C.loc['Decodificador2', 'Lugar'] = Zona
                Aparatos_C.loc['Decodificador2', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Decodificador2', 'Notas'] = Notas

            if indx == 11:
                NomAparato = 'decodificador3'
                # Aparatos_C.loc['Decodificador2', 'Aparatos'] = NomAparato
                InfoDeco = EquiposCTV.filter(regex=NomAparato)
                if InfoDeco.filter(regex='marca')[0] == 'otro':
                    Aparatos_C.loc['Decodificador3', 'Marca'] = InfoDeco.filter(regex='otro')[0]
                else:
                    Aparatos_C.loc['Decodificador3', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Decodificador3', 'CodigoS'] = CodStandby
                Aparatos_C.loc['Decodificador3', 'Existencia'] = 1
                Aparatos_C.loc['Decodificador3', 'Atacable'] = 'Si'
                Aparatos_C.loc['Decodificador3', 'Lugar'] = Zona
                Aparatos_C.loc['Decodificador3', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Decodificador3', 'Notas'] = Notas

            ##Consola2
            if indx == 12:
                NomAparato = 'consola2'
                InfoDeco = EquiposCTV.filter(regex=NomAparato)
                #Aparatos_C.loc['Consola2', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Consola2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Consola2', 'Existencia'] = 1
                Aparatos_C.loc['Consola2', 'Atacable'] = 'Si'
                #Aparatos_C.loc['Consola2', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero')[0]
                Aparatos_C.loc['Consola2', 'CodigoS'] =  CodStandby
                Aparatos_C.loc['Consola2', 'Lugar'] = Zona
                Aparatos_C.loc['Consola2', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Consola2', 'Notas'] = Notas

            if indx == 13:
            ##EquipoExtra
                NomAparato = 'eqextra'
                InfoDeco = EquiposCTV.filter(regex=NomAparato)

                Aparatos_C.loc['Equipoextra', 'Marca'] = InfoDeco.filter(regex='eqextra_c_i')[0]
                Aparatos_C.loc['EquipoExtra', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Equipoextra', 'Existencia'] = 1
                Aparatos_C.loc['Equipoextra', 'Atacable'] = 'No'
                Aparatos_C.loc['Equipoextra', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero')[0]
                Aparatos_C.loc['Equipoextra', 'Lugar'] = Zona
                Aparatos_C.loc['Equipoextra', 'CodigoS'] = CodStandby
                Aparatos_C.loc['EquipoExtra', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['EquipoExtra', 'Notas'] = Notas

            if indx == 14:
            ##EquipoExtra
                NomAparato = 'eqextra2'
                InfoDeco = EquiposCTV.filter(regex=NomAparato)
                Aparatos_C.loc['Equipoextra2', 'Marca'] = InfoDeco.filter(regex='eqextra2_c_i')[0]
                Aparatos_C.loc['EquipoExtra2', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Equipoextra2', 'Existencia'] = 1
                Aparatos_C.loc['Equipoextra2', 'Atacable'] = 'No'
                Aparatos_C.loc['Equipoextra2', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero')[0]
                Aparatos_C.loc['Equipoextra2', 'Lugar'] = Zona
                Aparatos_C.loc['Equipoextra2', 'CodigoS'] = CodStandby
                Aparatos_C.loc['Equipoextra2', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['EquipoExtra2', 'Notas'] = Notas

            if indx == 15:
            ##EquipoExtra
                NomAparato = 'eqextra3'
                InfoDeco = EquiposCTV.filter(regex=NomAparato)
                Aparatos_C.loc['Equipoextra3', 'Marca'] = InfoDeco.filter(regex='eqextra3_c_i')[0]
                Aparatos_C.loc['EquipoExtra3', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Equipoextra3', 'Existencia'] = 1
                Aparatos_C.loc['Equipoextra3', 'Atacable'] = 'No'
                Aparatos_C.loc['Equipoextra3', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero')[0]
                Aparatos_C.loc['Equipoextra3', 'Lugar'] = Zona
                Aparatos_C.loc['Equipoextra3', 'CodigoS'] = CodStandby
                Aparatos_C.loc['Equipoextra3', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['EquipoExtra3', 'Notas'] = Notas

        InfoDeco = Circuito.filter(regex='eqdeahorro')
        if not InfoDeco.empty:
            Aparatos_C.loc['Equipo Ahorro', 'Marca'] = InfoDeco[0]
            Aparatos_C.loc['Equipo Ahorro', 'Existencia'] = 1
            Aparatos_C.loc['Equipo Ahorro', 'Atacable'] = 'No'
        indx = indx + 1


    if Circuito.filter(regex='clustertv_regulador1_existencia_c_i')[0]=='si':
        InfoDeco = EquiposCTV.filter(regex='regulador1')
        Aparatos_C.loc['Regulador', 'Clave']      = 'RG'
        Aparatos_C.loc['Regulador', 'Zona']       = Zona
        Aparatos_C.loc['Regulador', 'Marca']      = InfoDeco.filter(regex='marca')[0] + ' del Cluster de TV'
        Aparatos_C.loc['Regulador', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['Regulador', 'CodigoS']    = CodStandby
        Aparatos_C.loc['Regulador', 'Equipos']      = InfoDeco.filter(regex='equipos_c_i')[0]
        if Aparatos_C.loc['Regulador', 'Equipos'] == 'otro':
            Aparatos_C.loc['Regulador', 'Equipos']  = InfoDeco.filter(regex='equipos_otro_c_i')[0]
        Aparatos_C.loc['Regulador', 'Capacidad']    = InfoDeco.filter(regex='capacidad_c_i')[0]
        Aparatos_C.loc['Regulador', 'Notas']        = 'Los equipos que se conectan son: '+Aparatos_C.loc['Regulador', 'Equipos']+','+Notas
        Aparatos_C.loc['Regulador', 'Atacable']     = 'Si'
        Aparatos_C.loc['Regulador', 'Existencia']   = 1



    if Circuito.filter(regex='clustertv_regulador2_existencia_c_i')[0]=='si':
        InfoDeco = EquiposCTV.filter(regex='regulador2')
        Aparatos_C.loc['Regulador2', 'Clave']      = 'RG'
        Aparatos_C.loc['Regulador2', 'Zona']       = Zona
        Aparatos_C.loc['Regulador2', 'Marca']      = InfoDeco.filter(regex='marca')[0] + ' del Cluster de TV'
        Aparatos_C.loc['Regulador2', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['Regulador2', 'CodigoS']    = CodStandby
        Aparatos_C.loc['Regulador2', 'Equipos']      = InfoDeco.filter(regex='equipos_c_i')[0]
        if Aparatos_C.loc['Regulador2', 'Equipos'] == 'otro':
            Aparatos_C.loc['Regulador2', 'Equipos']      = InfoDeco.filter(regex='equipos_otro_c_i')[0]
        Aparatos_C.loc['Regulador2', 'Capacidad']      = InfoDeco.filter(regex='capacidad_c_i')[0]
        Aparatos_C.loc['Regulador2', 'Notas']       = 'Los equipos que se conectan son: '+Aparatos_C.loc['Regulador', 'Equipos']+','+Notas
        Aparatos_C.loc['Regulador2', 'Atacable']     = 'Si'
        Aparatos_C.loc['Regulador2', 'Existencia'] = 1


    if Circuito.filter(regex='clustertv_regulador3_existencia_c_i')[0]=='si':
        InfoDeco = EquiposCTV.filter(regex='regulador3')
        Aparatos_C.loc['Regulador3', 'Clave']      = 'RG'
        Aparatos_C.loc['Regulador3', 'Zona']       = Zona
        Aparatos_C.loc['Regulador3', 'Marca']      = InfoDeco.filter(regex='marca')[0] + ' del Cluster de TV'
        Aparatos_C.loc['Regulador3', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['Regulador3', 'CodigoS']    = CodStandby
        Aparatos_C.loc['Regulador3', 'Equipos']      = InfoDeco.filter(regex='equipos_c_i')[0]
        if Aparatos_C.loc['Regulador3', 'Equipos'] == 'otro':
            Aparatos_C.loc['Regulador3', 'Equipos']  = InfoDeco.filter(regex='equipos_otro_c_i')[0]
        Aparatos_C.loc['Regulador3', 'Capacidad']    = InfoDeco.filter(regex='capacidad_c_i')[0]
        Aparatos_C.loc['Regulador3', 'Notas']        = 'Los equipos que se conectan son: '+Aparatos_C.loc['Regulador', 'Equipos']+','+Notas
        Aparatos_C.loc['Regulador3', 'Atacable']     = 'Si'
        Aparatos_C.loc['Regulador3', 'Existencia']   = 1

    if Circuito.filter(regex='clustertv_nobreak1_existencia_c_i')[0]=='si':
        InfoDeco = EquiposCTV.filter(regex='nobreak1')
        Aparatos_C.loc['NoBreak', 'Clave']      = 'RG'
        Aparatos_C.loc['NoBreak', 'Zona']       = Zona
        Aparatos_C.loc['NoBreak', 'Marca']      = InfoDeco.filter(regex='marca')[0] + ' del Cluster de TV'
        Aparatos_C.loc['NoBreak', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['NoBreak', 'CodigoS']    = CodStandby
        Aparatos_C.loc['NoBreak', 'Equipos']      = InfoDeco.filter(regex='equipos_c_i')[0]
        if Aparatos_C.loc['NoBreak', 'Equipos'] == 'otro':
            Aparatos_C.loc['NoBreak', 'Equipos']  = InfoDeco.filter(regex='equipos_otro_c_i')[0]
        Aparatos_C.loc['NoBreak', 'Capacidad']    = InfoDeco.filter(regex='capacidad_c_i')[0]
        Aparatos_C.loc['NoBreak', 'Notas']        = 'Los equipos que se conectan son: '+\
                                                    Aparatos_C.loc['NoBreak', 'Equipos']+','+Notas
        Aparatos_C.loc['NoBreak', 'Atacable']     = 'Si'
        Aparatos_C.loc['NoBreak', 'Existencia']   = 1

    if Circuito.filter(regex='clustertv_nobreak2_existencia_c_i')[0]=='si':
        InfoDeco = EquiposCTV.filter(regex='nobreak2')
        Aparatos_C.loc['NoBreak2', 'Clave']      = 'RG'
        Aparatos_C.loc['NoBreak2', 'Zona']       = Zona
        Aparatos_C.loc['NoBreak2', 'Marca']      = InfoDeco.filter(regex='marca')[0] + ' del Cluster de TV'
        Aparatos_C.loc['NoBreak2', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['NoBreak2', 'CodigoS']    = CodStandby
        Aparatos_C.loc['NoBreak2', 'Equipos']      = InfoDeco.filter(regex='equipos_c_i')[0]
        if Aparatos_C.loc['NoBreak2', 'Equipos'] == 'otro':
            Aparatos_C.loc['NoBreak2', 'Equipos']  = InfoDeco.filter(regex='equipos_otro_c_i')[0]
        Aparatos_C.loc['NoBreak2', 'Capacidad']    = InfoDeco.filter(regex='capacidad_c_i')[0]
        Aparatos_C.loc['NoBreak2', 'Notas']        = 'Los equipos que se conectan son: '+ \
                                                    Aparatos_C.loc['NoBreak', 'Equipos']+','+Notas
        Aparatos_C.loc['NoBreak2', 'Atacable']     = 'Si'
        Aparatos_C.loc['NoBreak2', 'Existencia']   = 1


    if Circuito.filter(regex='clustertv_nobreak3_existencia_c_i')[0]=='si':
        InfoDeco = EquiposCTV.filter(regex='nobreak3')
        Aparatos_C.loc['NoBreak3', 'Clave']      = 'RG'
        Aparatos_C.loc['NoBreak3', 'Zona']       = Zona
        Aparatos_C.loc['NoBreak3', 'Marca']      = InfoDeco.filter(regex='marca')[0] + ' del Cluster de TV'
        Aparatos_C.loc['NoBreak3', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['NoBreak3', 'CodigoS']    = CodStandby
        Aparatos_C.loc['NoBreak3', 'Equipos']      = InfoDeco.filter(regex='equipos_c_i')[0]
        if Aparatos_C.loc['NoBreak3', 'Equipos'] == 'otro':
            Aparatos_C.loc['NoBreak3', 'Equipos']  = InfoDeco.filter(regex='equipos_otro_c_i')[0]
        Aparatos_C.loc['NoBreak3', 'Capacidad']    = InfoDeco.filter(regex='capacidad_c_i')[0]
        Aparatos_C.loc['NoBreak3', 'Notas']        = 'Los equipos que se conectan son: '+ \
                                                    Aparatos_C.loc['NoBreak', 'Equipos']+','+Notas
        Aparatos_C.loc['NoBreak3', 'Atacable']     = 'Si'
        Aparatos_C.loc['NoBreak3', 'Existencia']   = 1



    # Aparatos_C.loc['Notas', 'Marca'] ='Sin notas'
    # Aparatos_C.loc['Notas', 'Existencia'] = 1

    # if not pd.isna(Circuito.filter(regex='clustertv_notas_c_i')[0]):
    #     Textocompleto=Circuito.filter(regex='clustertv_notas_c_i')[0]
    #     Info_C.loc['Notas', 'Info']      = Textocompleto
    #     Aparatos_C.loc['Notas', 'Marca'] = Textocompleto
    #     Aparatos_C.loc['Notas', 'Existencia'] = 1

    #
    # if not pd.isna(Aparatos_C.loc['Regulador1', 'Clave']):
    #     if 'otro1' in Aparatos_C.loc['Regulador1', 'Clave']:
    #         Aparatos_C.loc['Regulador1', 'Clave']=Aparatos_C.loc['Regulador1', 'Clave'].replace('otro1',Aparatos_C.loc['Equipoextra', 'Marca'])
    #     if 'otro2' in Aparatos_C.loc['Regulador1', 'Clave']:
    #         Aparatos_C.loc['Regulador1', 'Clave']=Aparatos_C.loc['Regulador1', 'Clave'].replace('otro2',Aparatos_C.loc['Equipoextra2', 'Marca'])
    #     if 'otro3' in Aparatos_C.loc['Regulador1', 'Clave']:
    #         Aparatos_C.loc['Regulador1', 'Clave']=Aparatos_C.loc['Regulador1', 'Clave'].replace('otro3', Aparatos_C.loc['Equipoextra3', 'Marca'])
    #
    # if not pd.isna(Aparatos_C.loc['Regulador2', 'Clave']):
    #     if 'otro1' in Aparatos_C.loc['Regulador2', 'Clave']:
    #         Aparatos_C.loc['Regulador2', 'Clave']=Aparatos_C.loc['Regulador2', 'Clave'].replace('otro1',Aparatos_C.loc['Equipoextra', 'Marca'])
    #     if 'otro2' in Aparatos_C.loc['Regulador2', 'Clave']:
    #         Aparatos_C.loc['Regulador2', 'Clave']=Aparatos_C.loc['Regulador2', 'Clave'].replace('otro2',Aparatos_C.loc['Equipoextra2', 'Marca'])
    #     if 'otro3' in Aparatos_C.loc['Regulador2', 'Clave']:
    #         Aparatos_C.loc['Regulador2', 'Clave']=Aparatos_C.loc['Regulador2', 'Clave'].replace('otro3', Aparatos_C.loc['Equipoextra3', 'Marca'])

    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()
    #TotConsumo = calc_consumo(Aparatos_C)
    #Info_C.loc['Consumo Total', 'Info'] = TotConsumo
    EquiposC = Aparatos.fillna(0)
    # if EquiposC.loc['Equipo Ahorro','Marca']!=0:
    #     Multis=1
    zona=Zona
    #Info_C.loc['Consumo Total', 'Info'] = TotConsumo

    return Aparatos, zona

