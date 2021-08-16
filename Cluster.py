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
    Equipos = EquiposCTV.filter(regex='equipos')
    indx=0
    Nominal=0

    CodStandby   = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
    Tierra       = Circuito.filter(regex='clustertv_tierra_c_i')[0]
    Enchufes     = Circuito.filter(regex='clustertv_enchufes_c_i')[0]
    Maniobras    = Circuito.filter(regex='clustertv_maniobras_c_i')[0]
    Maniobras_Detalles = Circuito.filter(regex='clustertv_maniobras_detalles_c_i')[0]
    InfoDeco     = Circuito.filter(regex='clustertv_notas_c_i')


    if not InfoDeco.empty:
        Notas=InfoDeco[0]

    InfoDeco = Circuito.filter(regex='zona_c_i')[0]

    if InfoDeco == 'otro':
        Zona=Lugar(Circuito.filter(regex='zona_otro_c_i')[0])
    else:
        Zona=Lugar(InfoDeco)


    if isinstance(Circuito.filter(regex='clustertv_equipos_desconectar_c_i')[0], str):
        Nomedidos = Circuito.filter(regex='clustertv_equipos_desconectar_c_i')[0]
    else:
        Nomedidos = " no_hay"


    for i in Equipos:
        if i == 1:

            if indx == 1:
                ##Televisión
                NomAparato = 'tv1'
                InfoDeco = Circuito.filter(regex=NomAparato)
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
                Aparatos_C.loc['TV', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero')[0]
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
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Decodificador1', 'Existencia'] = 1
                Otro = InfoDeco.filter(regex='marca_otro_c_i')
                if pd.isna(Otro[0]):

                    Aparatos_C.loc['Decodificador1','Marca']   = InfoDeco.filter(regex='decodificador1_marca_c_i')[0]
                else:
                    Aparatos_C.loc['Decodificador1', 'Marca'] = Otro[0]

                Aparatos_C.loc['Decodificador1', 'Atacable'] = 'Si'
                Aparatos_C.loc['Decodificador1', 'CodigoS'] =  CodStandby
                Aparatos_C.loc['Decodificador1', 'Lugar'] = Zona

                if 'decodificador1' in Nomedidos:
                    print("decodificador 1 no desconectado")
                else:
                    Aparatos_C.loc['Decodificador1', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])

            if indx == 3:
            ##Modem
                NomAparato = 'modem'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Modem', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Modem', 'Existencia'] = 1
                Aparatos_C.loc['Modem', 'Atacable'] = 'No'
                Aparatos_C.loc['Modem', 'Lugar'] = Zona
                Aparatos_C.loc['Modem', 'CodigoS'] = CodStandby
                if 'modem' in Nomedidos:
                    print("modem no desconectado")
                else:
                    Aparatos_C.loc['Modem', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])



            if indx == 4:
            ##Repetidor
                NomAparato = 'repetidor'
                InfoDeco = Circuito.filter(regex=NomAparato)

                Aparatos_C.loc['Repetidor', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Repetidor', 'Existencia'] = 1
                Aparatos_C.loc['Repetidor', 'Atacable'] = 'No'
                Aparatos_C.loc['Repetidor', 'CodigoS'] =  CodStandby
                Aparatos_C.loc['Repetidor', 'Lugar'] = Zona
                if 'repetidor' in Nomedidos:
                    print("repetidor no desconectado")
                else:
                    Aparatos_C.loc['Repetidor', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])

            if indx == 5:
                NomAparato = 'consola1'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Consola1', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Consola1', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Consola1', 'Existencia'] = 1
                Aparatos_C.loc['Consola1', 'Atacable'] = 'Si'
                Aparatos_C.loc['Consola1', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero')[0]
                Aparatos_C.loc['Consola1', 'CodigoS'] =  CodStandby
                Aparatos_C.loc['Consola1', 'Lugar'] = Zona

                if 'consola1' in Nomedidos:
                    print("consola1 no desconectado")
                else:
                    Aparatos_C.loc['Consola1', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])

            ##Antena
            if indx == 6:
                NomAparato = 'antena'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Antena', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Antena', 'Existencia'] = 1
                Aparatos_C.loc['Antena', 'Atacable'] = 'Si'
                Aparatos_C.loc['Antena', 'CodigoS'] =  CodStandby
                Aparatos_C.loc['Antena', 'Lugar'] = Zona
                if 'antena' in Nomedidos:
                    print("antena no desconectado")
                else:
                    Aparatos_C.loc['Antena', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
            # Sonido
            if indx == 7:
                NomAparato = 'sonido'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Sonido', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Sonido', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Sonido', 'Existencia'] = 1
                Aparatos_C.loc['Sonido', 'Atacable'] = 'Si'
                Aparatos_C.loc['Sonido', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero')[0]
                Aparatos_C.loc['Sonido', 'CodigoS'] =  CodStandby
                Aparatos_C.loc['Sonido', 'Lugar'] = Zona
                Aparatos_C.loc['Sonido', 'Tolerancia']=False

                if 'sonido' in Nomedidos:
                    print("sonido no desconectado")
                else:
                    Aparatos_C.loc['Sonido', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
            ##Bocinas
            if indx == 8:
                NomAparato = 'bocina'
                # Aparatos_C.loc['Bocinas', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Bocinas', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Bocinas', 'Existencia'] = InfoDeco.filter(regex='numero')[0]
                Aparatos_C.loc['Bocinas', 'Atacable'] = 'Si'
                Aparatos_C.loc['Bocinas', 'CodigoS'] =  CodStandby
                Aparatos_C.loc['Bocinas', 'Lugar'] = Zona
                if 'bocina' in Nomedidos:
                    print("bocinas no desconectado")
                else:
                    Aparatos_C.loc['Bocinas', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])


            # Blueray
            if indx == 9:
                NomAparato = 'bluray'
                InfoDeco = Circuito.filter(regex=NomAparato)
                tipo= InfoDeco.filter(regex='tipo')[0]
                Aparatos_C.loc['Bluray', 'CodigoS'] = CodStandby
                Aparatos_C.loc['Bluray', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero')[0]
                InfoDeco = Circuito.filter(regex=tipo)
                Aparatos_C.loc['Bluray', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Bluray', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Bluray', 'Existencia'] = 1
                Aparatos_C.loc['Bluray', 'Atacable'] = 'Si'
                Aparatos_C.loc['Blueray', 'Lugar'] = Zona
                if 'bluray' in Nomedidos:
                    print("blueray no desconectado")
                else:

                    Aparatos_C.loc['Bluray', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])

            if indx == 10:
            ##Regulador
                NomAparato='regulador1'
                InfoDeco = Circuito.filter(regex=NomAparato)
                if not InfoDeco.empty:
                    Aparatos_C.loc['Regulador1', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                    Aparatos_C.loc['Regulador1', 'Equipos'] = InfoDeco.filter(regex='equipos_c_i')[0]
                    Aparatos_C.loc['Regulador1', 'Existencia'] =1
                    Aparatos_C.loc['Regulador1', 'Atacable'] = 'Si'
                    Aparatos_C.loc['Regulador1', 'Lugar'] = Zona

                if InfoDeco.filter(regex='regulador1_apagado_c_i')[0] == 'si':
                    Aparatos_C.loc['Regulador1', 'Standby'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                    Aparatos_C.loc['Regulador1', 'CodigoS'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]

                elif InfoDeco.filter(regex='regulador1_apagado_c_i')[0] == 'no':
                    Aparatos_C.loc['Regulador1', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['Regulador1', 'CodigoS'] =  CodStandby



            if indx == 11:
            ##Nobreak
                NomAparato = 'nobreak'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['NoBreak', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['NoBreak', 'Factor de potencia'] = InfoDeco.filter(regex='facpot')[0]
                Aparatos_C.loc['NoBreak', 'Capacidad'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['NoBreak', 'Equipos'] = InfoDeco.filter(regex='equipos')[0]
                Aparatos_C.loc['NoBreak', 'Existencia'] = 1
                Aparatos_C.loc['NoBreak', 'Atacable'] = 'Si'
                Aparatos_C.loc['NoBreak', 'Lugar'] = Zona

                if InfoDeco.filter(regex='nobreak_apagado_c_i')[0] == 'si':
                    Aparatos_C.loc['NoBreak', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                    Aparatos_C.loc['NoBreak', 'CodigoS'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                elif InfoDeco.filter(regex='nobreak_apagado_c_i')[0] == 'no':
                    Aparatos_C.loc['NoBreak', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['NoBreak', 'CodigoS'] =  CodStandby

            ##Decodificador2
            if indx == 12:
                NomAparato = 'decodificador2'
                # Aparatos_C.loc['Decodificador2', 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                if InfoDeco.filter(regex='marca')[0] == 'otro':
                    Aparatos_C.loc['Decodificador2', 'Marca'] = InfoDeco.filter(regex='otro')[0]
                else:
                    Aparatos_C.loc['Decodificador2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Decodificador2', 'CodigoS'] = CodStandby
                Aparatos_C.loc['Decodificador2', 'Existencia'] = 1
                Aparatos_C.loc['Decodificador2', 'Atacable'] = 'Si'
                Aparatos_C.loc['Decodificador2', 'Lugar'] = Zona
                if 'decodificador2' in Nomedidos:
                    print("decodificador2 no desconectado")
                else:
                    Aparatos_C.loc['Decodificador2', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])

            ##Regulador2
            if indx == 13:
                NomAparato = 'regulador2'
                InfoDeco = Circuito.filter(regex=NomAparato)
                if not InfoDeco.empty:
                    Aparatos_C.loc['Regulador2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                    Aparatos_C.loc['Regulador2', 'Equipos'] = InfoDeco.filter(regex='equipos_c_i')[0]
                    Aparatos_C.loc['Regulador2', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador2', 'Atacable'] = 'Si'
                    Aparatos_C.loc['Regulador2', 'Lugar'] = Zona

                if InfoDeco.filter(regex='regulador2_apagado_c_i')[0] == 'si':
                    Aparatos_C.loc['Regulador2', 'Standby'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                    Aparatos_C.loc['Regulador2', 'CodigoS'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
                elif InfoDeco.filter(regex='regulador2_apagado_c_i')[0] == 'no':
                    Aparatos_C.loc['Regulador2', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                    Aparatos_C.loc['Regulador2', 'CodigoS'] =  CodStandby
            ##Consola2
            if indx == 14:
                NomAparato = 'consola2'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Consola2', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
                Aparatos_C.loc['Consola2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Consola2', 'Existencia'] = 1
                Aparatos_C.loc['Consola2', 'Atacable'] = 'Si'
                Aparatos_C.loc['Consola2', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero')[0]
                Aparatos_C.loc['Consola2', 'CodigoS'] =  CodStandby
                Aparatos_C.loc['Consola2', 'Lugar'] = Zona
                if 'consola2' in Nomedidos:
                    print("consola2 no desconectado")
                else:
                    Aparatos_C.loc['Consola2', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])

            if indx == 15:
            ##EquipoExtra
                NomAparato = 'eqextra'
                InfoDeco = Circuito.filter(regex=NomAparato)

                Aparatos_C.loc['Equipoextra', 'Marca'] = InfoDeco.filter(regex='eqextra_c_i')[0]
                Aparatos_C.loc['EquipoExtra', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Nominal=InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Equipoextra', 'Existencia'] = 1
                Aparatos_C.loc['Equipoextra', 'Atacable'] = 'No'
                Aparatos_C.loc['Equipoextra', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero')[0]
                Aparatos_C.loc['Equipoextra', 'Lugar'] = Zona
                Aparatos_C.loc['Equipoextra', 'CodigoS'] = CodStandby
                if 'eqextra' in Nomedidos:
                    print("eqextra no desconectado no desconectado")
                else:
                    Aparatos_C.loc['Equipoextra', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])

            if indx == 16:
            ##EquipoExtra
                NomAparato = 'eqextra2'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Equipoextra2', 'Marca'] = InfoDeco.filter(regex='eqextra2_c_i')[0]
                Aparatos_C.loc['EquipoExtra2', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Nominal = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Equipoextra2', 'Existencia'] = 1
                Aparatos_C.loc['Equipoextra2', 'Atacable'] = 'No'
                Aparatos_C.loc['Equipoextra2', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero')[0]
                Aparatos_C.loc['Equipoextra2', 'Lugar'] = Zona
                Aparatos_C.loc['Equipoextra2', 'CodigoS'] = CodStandby
                if 'eqextra2' in Nomedidos:
                    print("eqextra no desconectado no desconectado")
                else:
                    Aparatos_C.loc['Equipoextra2', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])

            if indx == 17:
            ##EquipoExtra
                NomAparato = 'eqextra3'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Equipoextra3', 'Marca'] = InfoDeco.filter(regex='eqextra3_c_i')[0]
                Aparatos_C.loc['EquipoExtra3', 'Nominal'] = InfoDeco.filter(regex='consumo')[0]
                Nominal = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Equipoextra3', 'Existencia'] = 1
                Aparatos_C.loc['Equipoextra3', 'Atacable'] = 'No'
                Aparatos_C.loc['Equipoextra3', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero')[0]
                Aparatos_C.loc['Equipoextra3', 'Lugar'] = Zona
                Aparatos_C.loc['Equipoextra3', 'CodigoS'] = CodStandby
                if 'eqextra3' in Nomedidos:
                    print("eqextra no desconectado no desconectado")
                else:
                    Aparatos_C.loc['Equipoextra3', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])

        InfoDeco = Circuito.filter(regex='eqdeahorro')
        if not InfoDeco.empty:
            Aparatos_C.loc['Equipo Ahorro', 'Marca'] = InfoDeco[0]
            Aparatos_C.loc['Equipo Ahorro', 'Existencia'] = 1
            Aparatos_C.loc['Equipo Ahorro', 'Atacable'] = 'No'
        indx = indx + 1

    Aparatos_C.loc['Notas', 'Marca'] ='Sin notas'
    Aparatos_C.loc['Notas', 'Existencia'] = 1
    if not pd.isna(Circuito.filter(regex='clustertv_notas_c_i')[0]):
        Textocompleto=Circuito.filter(regex='clustertv_notas_c_i')[0] +'; '+ Maniobras
        Info_C.loc['Notas', 'Info']      = Textocompleto
        Aparatos_C.loc['Notas', 'Marca'] = Textocompleto
        Aparatos_C.loc['Notas', 'Existencia'] = 1


    if not pd.isna(Aparatos_C.loc['Regulador1', 'Clave']):
        if 'otro1' in Aparatos_C.loc['Regulador1', 'Clave']:
            Aparatos_C.loc['Regulador1', 'Clave']=Aparatos_C.loc['Regulador1', 'Clave'].replace('otro1',Aparatos_C.loc['Equipoextra', 'Marca'])
        if 'otro2' in Aparatos_C.loc['Regulador1', 'Clave']:
            Aparatos_C.loc['Regulador1', 'Clave']=Aparatos_C.loc['Regulador1', 'Clave'].replace('otro2',Aparatos_C.loc['Equipoextra2', 'Marca'])
        if 'otro3' in Aparatos_C.loc['Regulador1', 'Clave']:
            Aparatos_C.loc['Regulador1', 'Clave']=Aparatos_C.loc['Regulador1', 'Clave'].replace('otro3', Aparatos_C.loc['Equipoextra3', 'Marca'])

    if not pd.isna(Aparatos_C.loc['Regulador2', 'Clave']):
        if 'otro1' in Aparatos_C.loc['Regulador2', 'Clave']:
            Aparatos_C.loc['Regulador2', 'Clave']=Aparatos_C.loc['Regulador2', 'Clave'].replace('otro1',Aparatos_C.loc['Equipoextra', 'Marca'])
        if 'otro2' in Aparatos_C.loc['Regulador2', 'Clave']:
            Aparatos_C.loc['Regulador2', 'Clave']=Aparatos_C.loc['Regulador2', 'Clave'].replace('otro2',Aparatos_C.loc['Equipoextra2', 'Marca'])
        if 'otro3' in Aparatos_C.loc['Regulador2', 'Clave']:
            Aparatos_C.loc['Regulador2', 'Clave']=Aparatos_C.loc['Regulador2', 'Clave'].replace('otro3', Aparatos_C.loc['Equipoextra3', 'Marca'])

    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()
    TotConsumo = calc_consumo(Aparatos_C)
    Info_C.loc['Consumo Total', 'Info'] = TotConsumo
    EquiposC = Aparatos.fillna(0)
    if EquiposC.loc['Equipo Ahorro','Marca']!=0:
        Multis=1
    zona=Zona
    Info_C.loc['Consumo Total', 'Info'] = TotConsumo


    return Aparatos, TotConsumo, zona

