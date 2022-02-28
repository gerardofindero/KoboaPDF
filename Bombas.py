import pandas as pd
from Consumo    import consumoEq
from Consumo    import calc_consumo , consumoEq, temperatura
from libreriaBombasPresurizadoras import crearClavesBP
from libreriaBombasAlberca import crearClavesBA
from libreriaBombas import crearClavesBG
def bombas (Excel,Nocircuito):
    Aparatos_C = pd.DataFrame(
        index=['Bomba de Presión', 'Bomba de Gravitación', 'Alberca','Bomba de Recirculación'],
        columns=['Tipo', 'Standby', 'Nominal','Real', 'Marca','CodigoN','CodigoS','Existencia','Zona', 'Atacable','Clave'])

    Aparatos_C = pd.DataFrame(columns=['Aparatos'])
    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("plomeria", case=False)]
    Equipos= Circuito[InfoEquipos]
    Equipos=Equipos.fillna('X')
    indx=0
    CodigoStandby= Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
    InfoDeco = Equipos.filter(regex='bomba1')
    Bomba = InfoDeco.filter(regex='tipo')[0]
    #zona = InfoDeco.filter(regex='zona_c_i')[0]


    if Bomba=='presurizadora_hidroneumatico':
        InfoBomba= Equipos.filter(regex='hidro')
        #print("InfoBomba en bombas.py: ",InfoBomba)
        Aparatos_C.loc['Bomba de Presión', 'Zona'] = InfoBomba.filter(regex='zona_c_i')[0]
        if InfoBomba.filter(regex='espendiente_c_i')[0]=='si':
            Aparatos_C.loc['Bomba de Presión', 'CodigoN'] = InfoBomba.filter(regex='codigofindero_c_i')[0]
            if InfoBomba.filter(regex='codigofindero2_c_i')[0]!='X':
                Aparatos_C.loc['Bomba de Presión', 'CodigoN']     =Aparatos_C.loc['Bomba de Presión', 'CodigoN'] +','+ InfoBomba.filter(regex='codigofindero2_c_i')[0]

            Aparatos_C.loc['Bomba de Presión', 'Standby'] = consumoEq(consumoEq(InfoBomba.filter(regex='standby')[0]))
            Aparatos_C.loc['Bomba de Presión', 'Nominal'] = consumoEq(InfoBomba.filter(regex='consumo_c_i')[0])
            Aparatos_C.loc['Bomba de Presión', 'CodigoS'] = CodigoStandby
            Aparatos_C.loc['Bomba de Presión', 'Notas']         = InfoBomba.filter(regex='notas')[0]
            Aparatos_C.loc['Bomba de Presión', 'Marca']         = InfoBomba.filter(regex='marca_c_i')[0]
            Aparatos_C.loc['Bomba de Presión', 'Encendido']     = InfoBomba.filter(regex='encender_c_i')[0]
            Aparatos_C.loc['Bomba de Presión', 'Tiempo']        = InfoBomba.filter(regex='tiempo_c_i')[0]
            Aparatos_C.loc['Bomba de Presión', 'TinacoEx']      = InfoBomba.filter(regex='tinaco_existencia_c_i')[0]
            Aparatos_C.loc['Bomba de Presión', 'TinacoAl']      = InfoBomba.filter(regex='tinaco_altura_c_i')[0]
            Aparatos_C.loc['Bomba de Presión', 'TinacoAC']      = InfoBomba.filter(regex='acceso_c_i')[0]
            Aparatos_C.loc['Bomba de Presión', 'PresionOFF PA'] = InfoBomba.filter(regex='presion_off_pa')[0]
            Aparatos_C.loc['Bomba de Presión', 'PresionOFF PB'] = InfoBomba.filter(regex='presion_off_pb')[0]
            Aparatos_C.loc['Bomba de Presión', 'Jarros']        = InfoBomba.filter(regex='jarrosdeaire')[0]
            Aparatos_C.loc['Bomba de Presión', 'Valvulas']               = InfoBomba.filter(regex='valvulas_abrirlas')[0]
            Aparatos_C.loc['Bomba de Presión', 'Valvulas Abiertas']      = InfoBomba.filter(regex='valvulas_abiertas')[0]
            Aparatos_C.loc['Bomba de Presión', 'Valvulas Verificada']      = InfoBomba.filter(regex='valvulas_verificar')[0]
            Aparatos_C.loc['Bomba de Presión', 'Diametro']               = InfoBomba.filter(regex='diametro')[0]
            Aparatos_C.loc['Bomba de Presión', 'Codos']                  = InfoBomba.filter(regex='codos')[0]
            Aparatos_C.loc['Bomba de Presión', 'Fuga']                   = InfoBomba.filter(regex='fuga')[0]
            Aparatos_C.loc['Bomba de Presión', 'Pastilla']               = InfoBomba.filter(regex='pastilla_c_i')[0]
            Aparatos_C.loc['Bomba de Presión', 'Inspección']             = InfoBomba.filter(regex='inspeccion')[0]
            Aparatos_C.loc['Bomba de Presión', 'Inspección Lugar']       = InfoBomba.filter(regex='inspeccion_lugar')[0]
            Aparatos_C.loc['Bomba de Presión', 'PruebasF']               = InfoBomba.filter(regex='pruebafugas')[0]
            Aparatos_C.loc['Bomba de Presión', 'Presurizador']           = InfoBomba.filter(regex='sistemapresurizador_c_i')[0]
            #Aparatos_C.loc['Bomba de Presión', 'Clave']                  = 'BP'+','+str(
            #                                              Aparatos_C.loc['Bomba de Presión', 'Nominal'])+','+\
            #                                              Aparatos_C.loc['Bomba de Presión', 'TinacoEx']+','+\
            #                                              Aparatos_C.loc['Bomba de Presión', 'Pastilla']+','+\
            #                                              Aparatos_C.loc['Bomba de Presión', 'PresionOFF PB']+','+\
            #                                              Aparatos_C.loc['Bomba de Presión', 'PresionOFF PA']+','+\
            #                                              Aparatos_C.loc['Bomba de Presión', 'Valvulas Verificada']+','+\
            #                                              Aparatos_C.loc['Bomba de Presión', 'Valvulas Abiertas']+','+\
            #                                              Aparatos_C.loc['Bomba de Presión', 'Jarros']+','+\
            #                                              Aparatos_C.loc['Bomba de Presión', 'Fuga']+','+'X'+','+\
            #                                              Aparatos_C.loc['Bomba de Presión', 'Inspección']+','+\
            #                                              Aparatos_C.loc['Bomba de Presión', 'Inspección_Lugar']+','+\
            #                                              Aparatos_C.loc['Bomba de Presión', 'PruebasF']
            #print("InfoBomba en Bombas.py: ", Aparatos_C.loc['Bomba de Presión'])
            #print("ClavesBP en Bombas.py: ", clavesBP(Aparatos_C.loc["Bomba de Presión"]))
            Aparatos_C.loc['Bomba de Presión', 'Clave'] = 'BP' + crearClavesBP(Aparatos_C.loc["Bomba de Presión"])
            #print("Aparatos_C.loc['Bomba de Presión', 'Clave']: ",Aparatos_C.loc['Bomba de Presión', 'Clave'])



            Aparatos_C.loc['Bomba de Presión', 'Atacable'] = 'Si'
            #print(Aparatos_C.loc['Bomba de Presión', 'Nominal'])

    if Bomba == 'gravitacional':
        InfoDeco = Equipos.filter(regex='gravitacional')
        #f InfoDeco.filter(regex='espendiente_c_i')[0]=='si':
        #    Aparatos_C.loc['Bomba de Presión', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
        #    if InfoBomba.filter(regex='codigofindero2_c_i')[0]!='X':
        #        Aparatos_C.loc['Bomba de Presión', 'CodigoN']     =Aparatos_C.loc['Bomba de Presión', 'CodigoN'] +','+ InfoBomba.filter(regex='codigofindero2_c_i')[0]
        # Q (segundos en llenar un litro-> se convierte a litros por minuto en claves)
        try   : Aparatos_C.loc['Bomba de Gravitación', 'FlujoSegundos'] = InfoDeco.filter(regex='flujo_segundos')[0]
        except: Aparatos_C.loc['Bomba de Gravitación', 'FlujoSegundos'] = 0
        # Z
        try   : Aparatos_C.loc['Bomba de Gravitación', 'Delta'] = InfoDeco.filter(regex='delta')[0]
        except: Aparatos_C.loc['Bomba de Gravitación', 'Delta'] = 0
        # L
        try   : Aparatos_C.loc['Bomba de Gravitación', 'Longitud'] = InfoDeco.filter(regex='longitud')[0]
        except: Aparatos_C.loc['Bomba de Gravitación', 'Longitud'] = 0
        # nC90
        try   : Aparatos_C.loc['Bomba de Gravitación', 'Codos'] = InfoDeco.filter(regex='codos')[0]
        except: Aparatos_C.loc['Bomba de Gravitación', 'Codos'] = 0
        # D en pulgadas se convierte a metros en las claves
        try   : Aparatos_C.loc['Bomba de Gravitación', 'Diametro'] = InfoDeco.filter(regex='diametro')[0]
        except: Aparatos_C.loc['Bomba de Gravitación', 'Diametro'] = 0
        # T
        try   : Aparatos_C.loc['Bomba de Gravitación', 'Temperatura'] = InfoDeco.filter(regex='temperatura')[0]
        except: Aparatos_C.loc['Bomba de Gravitación', 'Temperatura'] = 20

        Aparatos_C.loc['Bomba de Gravitación', 'Nominal'] = InfoDeco.filter(regex='nominal')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
        Aparatos_C.loc['Bomba de Gravitación', 'Marca'] = 'Bomba Gravitacional'

        Aparatos_C.loc['Bomba de Gravitación', 'Acceso'] = InfoDeco.filter(regex='acceso')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Flujo'] = InfoDeco.filter(regex='flujo')[0]

        Aparatos_C.loc['Bomba de Gravitación', 'ControlPeg'] = InfoDeco.filter(regex='control_pegados')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'ControlCierra'] = InfoDeco.filter(regex='control_cierra')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'ControlContra'] = InfoDeco.filter(regex='control_contrapeso')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'ControlProblemas'] = InfoDeco.filter(regex='control_problemas')[0]
        #Aparatos_C.loc['Bomba de Gravitación', 'Obstaculos'] = InfoDeco.filter(regex='obstaculos_c_i')[0]

        Aparatos_C.loc['Bomba de Gravitación', 'AccesoBomba'] = InfoDeco.filter(regex='accesobomba')[0]

        Aparatos_C.loc['Bomba de Gravitación', 'Valvulas'] = InfoDeco.filter(regex='valvulas')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Valvulas_Abiertas'] = InfoDeco.filter(regex='valvulas_abiertas')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Valvulas_Abrirlas'] = InfoDeco.filter(regex='valvulas_abrirlas')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Sarro'] = InfoDeco.filter(regex='sarro')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Termografia'] = InfoDeco.filter(regex='termografia')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Material'] = InfoDeco.filter(regex='material')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Nombre'] = InfoDeco.filter(regex='nombre')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Notas'] = InfoDeco.filter(regex='notas')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'FugaSup'] = InfoDeco.filter(regex='fugasSup')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'FugaTer'] = InfoDeco.filter(regex='fugasTer')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'FugaTXT'] = InfoDeco.filter(regex='fugasTXT')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Medidor'] = InfoDeco.filter(regex='medidor_c_i')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'MedidorURL'] = InfoDeco.filter(regex='medidor_c_i_URL')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'MedidorLEC'] = InfoDeco.filter(regex='medidor_lectura')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'CodigoS'] = CodigoStandby
        Aparatos_C.loc['Bomba de Gravitación', 'Zona'] = InfoDeco.filter(regex='nombre')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Atacable'] = 'Si'
        Aparatos_C.loc['Bomba de Gravitación', 'Notas'] = InfoDeco.filter(regex='notas')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Clave']     = 'BG' + crearClavesBA(Aparatos_C.loc["Bomba de Gravitación"])




    if Bomba == 'recirculacion':
        ##Ahorro 40%
        InfoDeco = Equipos.filter(regex='recirculacion')
        Aparatos_C.loc['Bomba de Recirculación', 'Marca'] = ' '
        Aparatos_C.loc['Bomba de Recirculación', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
        Aparatos_C.loc['Bomba de Recirculación', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
        Aparatos_C.loc['Bomba de Recirculación', 'Timer'] = InfoDeco.filter(regex='timer')[0]
        Aparatos_C.loc['Bomba de Recirculación', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
        if Aparatos_C.loc['Bomba de Recirculación', 'Standby'] > 0:
            Aparatos_C.loc['Bomba de Recirculación', 'CodigoS'] = CodigoStandby
        Aparatos_C.loc['Bomba de Recirculación', 'Notas'] = InfoDeco.filter(regex='notas')[0]
        Aparatos_C.loc['Bomba de Recirculación', 'Zona'] =  InfoDeco.filter(regex='zona')[0]
        Aparatos_C.loc['Bomba de Recirculación', 'Atacable'] = 'Si'
        Aparatos_C.loc['Bomba de Recirculación', 'Clave'] = 'BR'

    if Bomba == 'filtro_de_alberca':
        InfoDeco = Equipos.filter(regex='alberca')
        Aparatos_C.loc['Alberca', 'Zona']    = InfoDeco.filter(regex='zona')[0]
        if InfoDeco.filter(regex='espendiente_c_i')[0]=='si':
            Aparatos_C.loc['Alberca', 'Nombre']  = InfoDeco.filter(regex='nombre')[0]
            Aparatos_C.loc['Alberca', 'CodigoS'] = CodigoStandby
            try   : Aparatos_C.loc['Alberca', 'Nominal'] = InfoDeco.filter(regex='nominal')[0] # x/W/x potencia
            except: Aparatos_C.loc['Alberca', 'Nominal'] = 0
            try   : Aparatos_C.loc["Alberca", 'Gasto'  ] = InfoDeco.filter(regex='gasto'  )[0] # kWh/x/x consumo
            except: Aparatos_C.loc["Alberca", 'Gasto'  ] = 0
            try   : Aparatos_C.loc['Alberca', 'Volumen'] = InfoDeco.filter(regex='volumen')[0]  # x/x/V  volumen
            except: Aparatos_C.loc['Alberca', 'Volumen'] = 0
            try   : Aparatos_C.loc['Alberca', 'TipoUso'] = InfoDeco.filter(regex='')[0]
            except: Aparatos_C.loc['Alberca', 'TipoUso'] = ""
            try   : Aparatos_C.loc['Alberca', 'Solar'  ] = InfoDeco.filter(regex='solar')[0]
            except: Aparatos_C.loc['Alberca', 'Solar'  ] = ""
            if "alberca" in Aparatos_C.at['Alberca', 'Nombre']:
                Aparatos_C.loc['Alberca', 'Clave'] = 'BA' + "," + crearClavesBA(Aparatos_C.loc["Alberca"])
            else                                              :
                Aparatos_C.loc['Alberca', 'Clave'] = 'X'

            Aparatos_C.loc['Alberca', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]
            Aparatos_C.loc['Alberca', 'Marca'] = InfoDeco.filter(regex='marca')[0]
            Aparatos_C.loc['Alberca', 'Notas'] = InfoDeco.filter(regex='notas')[0]
            Aparatos_C.loc['Alberca', 'Atacable'] = 'Si'
            Aparatos_C.loc['Alberca', 'Existencia'] = 1

    return Aparatos_C
