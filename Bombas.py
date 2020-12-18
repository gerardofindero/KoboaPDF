import pandas as pd
from Consumo    import calc_consumo

def bombas (Excel,Nocircuito):
    Aparatos_C = pd.DataFrame(
        index=['Bomba', 'Gravitacion', 'Alberca', 'Tuberia'],
        columns=['Tipo', 'Consumo', 'Nominal','Real', 'Marca', 'Existencia'])

    Aparatos_C = pd.DataFrame(columns=['Aparatos'])
    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("plomeria", case=False)]
    Equipos= Circuito[InfoEquipos]
    indx=0

    InfoDeco = Equipos.filter(regex='bomba1')
    Aparatos_C.loc['Bomba', 'Tipo'] = InfoDeco.filter(regex='tipo')[0]

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


    InfoBomba= InfoDeco.filter(regex='bomba')
    Aparatos_C.loc['Bomba', 'Nominal'] = InfoBomba.filter(regex='nominal')[0]

    InfoDeco = Equipos.filter(regex='gravitacional')
    Aparatos_C.loc['Gravitacion', 'Real'] = InfoDeco.filter(regex='real')[0]
    Aparatos_C.loc['Gravitacion', 'Nominal'] = InfoDeco.filter(regex='nominal')[0]
    Aparatos_C.loc['Gravitacion', 'Marca'] = InfoDeco.filter(regex='marca')[0]
    Aparatos_C.loc['Gravitacion', 'Diametro'] = InfoDeco.filter(regex='diametro')[0]
    Aparatos_C.loc['Gravitacion', 'Longitud'] = InfoDeco.filter(regex='longitud')[0]
    Aparatos_C.loc['Gravitacion', 'Delta'] = InfoDeco.filter(regex='delta')[0]
    Aparatos_C.loc['Gravitacion', 'Acceso'] = InfoDeco.filter(regex='acceso')[0]
    Aparatos_C.loc['Gravitacion', 'Flujo'] = InfoDeco.filter(regex='flujo')[0]
    Aparatos_C.loc['Gravitacion', 'Obstaculos'] = InfoDeco.filter(regex='obstaculos_c_i')[0]
    Aparatos_C.loc['Gravitacion', 'Codos'] = InfoDeco.filter(regex='codos')[0]
    Aparatos_C.loc['Gravitacion', 'Valvulas'] = InfoDeco.filter(regex='valvulas')[0]
    Aparatos_C.loc['Gravitacion', 'Nombre'] = InfoDeco.filter(regex='nombre')[0]
    Aparatos_C.loc['Gravitacion', 'Notas'] = InfoDeco.filter(regex='notas')[0]
    Aparatos_C.loc['Gravitacion', 'voz'] = InfoDeco.filter(regex='voz')[0]

    Aparatos_C.loc['Bomba', 'Encendido +35min'] = Equipos.filter(regex='hidro_tiempo_c_i')[0]
    #
    # InfoDeco = Equipos.filter(regex='alberca')
    # Aparatos_C.loc['Alberca', 'Tipo'] = InfoDeco.filter(regex='tipo')[0]
    # #Aparatos_C.loc['Alberca', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
    # Aparatos_C.loc['Alberca', 'Nominal'] = InfoDeco.filter(regex='nominal')[0]
    # Aparatos_C.loc['Alberca', 'Marca'] = InfoDeco.filter(regex='marca')[0]


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
