import pandas as pd
from Consumo    import consumoEq
from Consumo    import calc_consumo , consumoEq, temperatura

def bombas (Excel,Nocircuito):
    Aparatos_C = pd.DataFrame(
        index=['Bomba de Presión', 'Bomba de Gravitación', 'Alberca','Bomba de Recirculación' ,'Tuberia'],
        columns=['Tipo', 'Standby', 'Nominal','Real', 'Marca','CodigoN','CodigoS','Existencia','Zona', 'Atacable','Clave'])

    Aparatos_C = pd.DataFrame(columns=['Aparatos'])
    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("plomeria", case=False)]
    Equipos= Circuito[InfoEquipos]
    Equipos=Equipos.fillna('X')
    indx=0
    CodigoStandby= Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
    Aparatos_C.loc['Tuberia', 'TinacoEx'] = Equipos.filter(regex='tinaco_existencia_c_i')[0]
    Aparatos_C.loc['Tuberia', 'TinacoAl'] = Equipos.filter(regex='tinaco_altura_c_i')[0]
    InfoDeco = Equipos.filter(regex='bomba1')
    Bomba = InfoDeco.filter(regex='tipo')[0]
    #zona = InfoDeco.filter(regex='zona_c_i')[0]
    # if zona=='otro':
    #     zona = InfoDeco.filter(regex='zona_otro')[0]
    # InfoDeco = Equipos.filter(regex='tuberia')
    # Aparatos_C.loc['Tuberia', 'Pastilla'] = InfoDeco.filter(regex='pastilla')[0]
    # Aparatos_C.loc['Tuberia', 'Codos'] = InfoDeco.filter(regex='codos')[0]
    #Aparatos_C.loc['Tuberia', 'Jarros'] = InfoDeco.filter(regex='jarrosdeaire')[0]
    #Aparatos_C.loc['Tuberia', 'Valvulas'] = InfoDeco.filter(regex='valvulas_numero')[0]
    #Aparatos_C.loc['Tuberia', 'Valvulas Abiertas'] = InfoDeco.filter(regex='valvulas_abiertas')[0]
    # Aparatos_C.loc['Tuberia', 'Diametro'] = InfoDeco.filter(regex='diametro')[0]
    # Aparatos_C.loc['Tuberia', 'PresionOFF PA'] = InfoDeco.filter(regex='presion_off_pa')[0]
    # Aparatos_C.loc['Tuberia', 'PresionOFF PB'] = InfoDeco.filter(regex='presion_off_pb')[0]
    # Aparatos_C.loc['Tuberia', 'PresionOFF PM'] = InfoDeco.filter(regex='presion_off_pm')[0]
    # Aparatos_C.loc['Tuberia', 'Fuga'] = InfoDeco.filter(regex='fuga')[0]
    # Aparatos_C.loc['Tuberia', 'Sist. Prezurizador'] = InfoDeco.filter(regex='sistemapresurizador')[0]
    Aparatos_C.loc['Tuberia', 'CodigoS'] = 'X'
    Aparatos_C.loc['Tuberia', 'CodigoN'] = 'X'
    Aparatos_C.loc['Tuberia', 'Clave'] = 'X'

    if Bomba=='presurizadora_hidroneumatico':
        InfoBomba= Equipos.filter(regex='hidro')

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
            Aparatos_C.loc['Bomba de Presión', 'Valvulas Abiertas']      = InfoBomba.filter(regex='valvulas_verificar')[0]
            Aparatos_C.loc['Bomba de Presión', 'Diametro']               = InfoBomba.filter(regex='diametro')[0]
            Aparatos_C.loc['Bomba de Presión', 'Codos']                  = InfoBomba.filter(regex='codos')[0]
            Aparatos_C.loc['Bomba de Presión', 'Fuga']                   = InfoBomba.filter(regex='fuga')[0]

            Aparatos_C.loc['Bomba de Presión', 'Inspección']             = InfoBomba.filter(regex='inspeccion')[0]
            Aparatos_C.loc['Bomba de Presión', 'Inspección_Lugar']       = InfoBomba.filter(regex='inspeccion_lugar')[0]
            Aparatos_C.loc['Bomba de Presión', 'PruebasF']               = InfoBomba.filter(regex='pruebafugas')[0]
            Aparatos_C.loc['Bomba de Presión', 'Presurizador']           = InfoBomba.filter(regex='sistemapresurizador_c_i')[0]
            Aparatos_C.loc['Bomba de Presión', 'Clave'] = 'BP'
            Aparatos_C.loc['Bomba de Presión', 'Atacable'] = 'Si'
            #print(Aparatos_C.loc['Bomba de Presión', 'Nominal'])

    if Bomba == 'gravitacional':
        InfoDeco = Equipos.filter(regex='gravitacional')

        if not InfoDeco.filter(regex='nominal').empty and InfoDeco.filter(regex='nominal')[0]!=0:
            Aparatos_C.loc['Bomba de Gravitación', 'Nominal'] = InfoDeco.filter(regex='nominal')[0]

        if not InfoDeco.filter(regex='real').empty and InfoDeco.filter(regex='real')[0]!=0:
            Aparatos_C.loc['Bomba de Gravitación', 'Nominal'] = InfoDeco.filter(regex='real')[0]

        Aparatos_C.loc['Bomba de Gravitación', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
        Aparatos_C.loc['Bomba de Gravitación', 'Marca'] = 'Bomba Gravitacional'
        Aparatos_C.loc['Bomba de Gravitación', 'Diametro'] = InfoDeco.filter(regex='diametro')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Longitud'] = InfoDeco.filter(regex='longitud')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Delta'] = InfoDeco.filter(regex='delta')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Acceso'] = InfoDeco.filter(regex='acceso')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Flujo'] = InfoDeco.filter(regex='flujo')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Obstaculos'] = InfoDeco.filter(regex='obstaculos_c_i')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Codos'] = InfoDeco.filter(regex='codos')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Valvulas'] = InfoDeco.filter(regex='valvulas')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Nombre'] = InfoDeco.filter(regex='nombre')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'Notas'] = InfoDeco.filter(regex='notas')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'voz'] = InfoDeco.filter(regex='voz')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'CodigoN'] = InfoDeco.filter(regex='real_codigofindero')[0]
        Aparatos_C.loc['Bomba de Gravitación', 'CodigoS'] = CodigoStandby
        Aparatos_C.loc['Bomba de Gravitación', 'Zona'] = zona
        Aparatos_C.loc['Bomba de Gravitación', 'Atacable'] = 'Si'
        Aparatos_C.loc['Bomba de Gravitación', 'Clave'] = 'BG'

    if Bomba == 'recirculacion':
        ##Ahorro 40%
        InfoDeco = Equipos.filter(regex='recirculacion')
        Aparatos_C.loc['Bomba de Recirculación', 'Marca'] = ' '
        Aparatos_C.loc['Bomba de Recirculación', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
        Aparatos_C.loc['Bomba de Recirculación', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
        Aparatos_C.loc['Bomba de Recirculación', 'Timer'] = InfoDeco.filter(regex='timer')[0]
        Aparatos_C.loc['Bomba de Recirculación', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero')[0]

        if Aparatos_C.loc['Bomba de Recirculación', 'Standby'] > 0:
            Aparatos_C.loc['Bomba de Recirculación', 'CodigoS'] = CodigoStandby

        Aparatos_C.loc['Bomba de Recirculación', 'Notas'] = InfoDeco.filter(regex='notas')[0]
        Aparatos_C.loc['Bomba de Recirculación', 'Zona'] = zona
        Aparatos_C.loc['Bomba de Recirculación', 'Atacable'] = 'Si'
        Aparatos_C.loc['Bomba de Recirculación', 'Clave'] = 'BR'

    if Bomba == 'filtro_de_alberca':
        InfoDeco = Equipos.filter(regex='alberca')
        print(InfoDeco)
        Aparatos_C.loc['Alberca', 'Zona']    = InfoDeco.filter(regex='zona')[0]
        Aparatos_C.loc['Alberca', 'Nombre']  = InfoDeco.filter(regex='nombre')[0]
        Aparatos_C.loc['Alberca', 'Standby'] = InfoDeco.filter(regex='standby')[0]

        if not InfoDeco.filter(regex='nominal').empty and InfoDeco.filter(regex='nominal')[0]!=0:
            Aparatos_C.loc['Alberca', 'Nominal'] = InfoDeco.filter(regex='nominal')[0]
        if not InfoDeco.filter(regex='real').empty and InfoDeco.filter(regex='real')[0]!=0:
            Aparatos_C.loc['Alberca', 'Nominal'] = InfoDeco.filter(regex='real')[0]

        Aparatos_C.loc['Alberca', 'Solar'] = InfoDeco.filter(regex='solar')[0]

        Aparatos_C.loc['Alberca', 'CodigoN'] = InfoDeco.filter(regex='codigofindero_c_i')[0]

        if Aparatos_C.loc['Alberca', 'Standby'] !='Nm':
            Aparatos_C.loc['Alberca', 'CodigoS'] = CodigoStandby

        Aparatos_C.loc['Alberca', 'Marca'] = InfoDeco.filter(regex='marca')[0]
        Aparatos_C.loc['Alberca', 'Volumen'] = InfoDeco.filter(regex='volumen')[0]
        Aparatos_C.loc['Alberca', 'Notas'] = InfoDeco.filter(regex='notas')[0]
        Aparatos_C.loc['Alberca', 'Atacable'] = 'Si'
        Aparatos_C.loc['Alberca', 'Clave'] = 'X'

        
    Aparatos=Aparatos_C.dropna(1,thresh=1)

    print(Aparatos)
    return Aparatos
