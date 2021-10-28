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
    indx=0
    CodigoStandby= Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
    InfoDeco = Equipos.filter(regex='bomba1')
    Bomba = InfoDeco.filter(regex='tipo')[0]
    zona = InfoDeco.filter(regex='zona_c_i')[0]
    if zona=='otro':
        zona = InfoDeco.filter(regex='zona_otro')[0]

    #Aparatos_C.loc['Bomba', 'CodigoS'] = 'X'
    #Aparatos_C.loc['Bomba', 'CodigoN'] = 'X'

    InfoDeco = Equipos.filter(regex='tuberia')

    Aparatos_C.loc['Tuberia', 'Codos'] = InfoDeco.filter(regex='codos')[0]
    Aparatos_C.loc['Tuberia', 'Valvulas'] = InfoDeco.filter(regex='valvulas')[0]
    Aparatos_C.loc['Tuberia', 'Valvulas Abiertas'] = InfoDeco.filter(regex='valvulas_abiertas')[0]
    Aparatos_C.loc['Tuberia', 'Diametro'] = InfoDeco.filter(regex='diametro')[0]
    Aparatos_C.loc['Tuberia', 'PresionOFF PA'] = InfoDeco.filter(regex='presion_off_pa')[0]
    Aparatos_C.loc['Tuberia', 'PresionOFF PB'] = InfoDeco.filter(regex='presion_off_pb')[0]
    Aparatos_C.loc['Tuberia', 'PresionOFF PM'] = InfoDeco.filter(regex='presion_off_pm')[0]
    Aparatos_C.loc['Tuberia', 'Fuga'] = InfoDeco.filter(regex='fuga')[0]
    Aparatos_C.loc['Tuberia', 'Sist. Prezurizador'] = InfoDeco.filter(regex='sistemapresurizador')[0]
    Aparatos_C.loc['Tuberia', 'CodigoS'] = 'X'
    Aparatos_C.loc['Tuberia', 'CodigoN'] = 'X'
    Aparatos_C.loc['Tuberia', 'Clave'] = 'X'

    if Bomba=='presurizadora_hidroneumatico':
        InfoBomba= InfoDeco.filter(regex='bombap')

        Aparatos_C.loc['Bomba de Presión', 'Standby'] = consumoEq(consumoEq(InfoBomba.filter(regex='standby')[0]))

        if not InfoDeco.filter(regex='nominal').empty and InfoDeco.filter(regex='nominal')[0]!=0:
            Aparatos_C.loc['Bomba de Presión', 'Nominal'] = consumoEq(InfoDeco.filter(regex='nominal')[0])

        if not InfoDeco.filter(regex='real').empty and InfoDeco.filter(regex='real')[0]!=0:
            Aparatos_C.loc['Bomba de Presión', 'Nominal'] = consumoEq(InfoDeco.filter(regex='real')[0])

        Aparatos_C.loc['Bomba de Presión', 'CodigoS'] = CodigoStandby
        Aparatos_C.loc['Bomba de Presión', 'CodigoN'] = InfoBomba.filter(regex='real_codigofindero')[0]
        Aparatos_C.loc['Bomba de Presión', 'Notas'] = InfoBomba.filter(regex='notas')[0]
        Aparatos_C.loc['Bomba de Presión', 'Zona'] = zona
        Aparatos_C.loc['Bomba de Presión', 'Marca'] = ' '
        Aparatos_C.loc['Bomba de Presión', 'Atacable'] = 'Si'
        Aparatos_C.loc['Bomba de Presión', 'Encendido +35min'] = Equipos.filter(regex='hidro_tiempo_c_i')[0]
        Aparatos_C.loc['Bomba de Presión', 'Clave'] = 'BP'
        print(Aparatos_C.loc['Bomba de Presión', 'Nominal'])

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
        Aparatos_C.loc['Alberca', 'Zona'] = zona
        Aparatos_C.loc['Alberca', 'Nombre'] = InfoDeco.filter(regex='nombre')[0]
        Aparatos_C.loc['Alberca', 'Standby'] = InfoDeco.filter(regex='standby')[0]

        if not InfoDeco.filter(regex='nominal').empty and InfoDeco.filter(regex='nominal')[0]!=0:
            Aparatos_C.loc['Alberca', 'Nominal'] = InfoDeco.filter(regex='nominal')[0]
        if not InfoDeco.filter(regex='real').empty and InfoDeco.filter(regex='real')[0]!=0:
            Aparatos_C.loc['Alberca', 'Nominal'] = InfoDeco.filter(regex='real')[0]

        Aparatos_C.loc['Alberca', 'Solar'] = InfoDeco.filter(regex='solar')[0]
        Aparatos_C.loc['Alberca', 'CodigoN'] = InfoDeco.filter(regex='real_codigofindero')[0]

        if Aparatos_C.loc['Alberca', 'Standby'] !='Nm':
            Aparatos_C.loc['Alberca', 'CodigoS'] = CodigoStandby

        Aparatos_C.loc['Alberca', 'Marca'] = InfoDeco.filter(regex='marca')[0]
        Aparatos_C.loc['Alberca', 'Volumen'] = InfoDeco.filter(regex='volumen')[0]
        Aparatos_C.loc['Alberca', 'Notas'] = InfoDeco.filter(regex='notas')[0]
        Aparatos_C.loc['Alberca', 'Atacable'] = 'Si'
        Aparatos_C.loc['Alberca', 'Clave'] = 'X'


    # NomAparato = 'Tinaco'
    # Aparatos_C.loc[1, 'Aparatos'] = NomAparato
    # InfoDeco = Equipos.filter(regex='tinaco1')
    # Aparatos_C.loc[1, 'No. de Tinacos'] = InfoDeco.filter(regex='existencia')[0]
    # Aparatos_C.loc[1, 'Altura del tinaco'] = InfoDeco.filter(regex='altura')[0]
    #
    #
    # NomAparato = 'Tuberia'
    # Aparatos_C.loc[2, 'Aparatos'] = NomAparato
    # InfoDeco = Equipos.filter(regex='tuberia')
    # Aparatos_C.loc[2, 'Presion de agua'] = InfoDeco.filter(regex='presion')[0]
    # Aparatos_C.loc[2, 'Hay jarros de aire'] = InfoDeco.filter(regex='jarrosaire')[0]
    # Aparatos_C.loc[2, 'Diametro tuberia'] = InfoDeco.filter(regex='diametro')[0]
    #Aparatos_C.loc[2, 'Presion planta baja'] = InfoDeco.filter(regex='presionpb')[0]
    Aparatos=Aparatos_C.dropna(1,thresh=1)
    return Aparatos
