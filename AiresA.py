import pandas as pd
from Consumo    import consumoEq

def airesA (Excel,Nocircuito,NomCircuito):
    Aparatos_C = pd.DataFrame(
        index=['Aire Acondicionado','Evaporador','Condensador'],
        columns=['Zona', 'Tecnologia', 'Ubicacion','Nominal', 'CodigoN','Standby','CodigoS','Volumen cuarto','Existencia','Zona', 'Atacable','Clave'])

    Aparatos_C = pd.DataFrame(columns=['Aparatos'])
    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("aires", case=False)]
    Equipos= Circuito[InfoEquipos]
    zona = Equipos.filter(regex='zona')[0]
    tec = Equipos.filter(regex='tecnologia')[0]
    CodStandby   = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]

    # InfoDeco=Equipos.filter(regex='evaporador')
    # Aparatos_C.loc['Evaporador', 'Zona'] = zona
    # Aparatos_C.loc['Evaporador', 'Tecnologia'] = tec
    # Aparatos_C.loc['Evaporador', 'Ubicacion'] = InfoDeco.filter(regex='ubicacion')[0]
    # Aparatos_C.loc['Evaporador', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo_c_i_001')[0])
    # Aparatos_C.loc['Evaporador', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i_001')[0]
    # Aparatos_C.loc['Evaporador', 'Temperatura'] = InfoDeco.filter(regex='temperatura')[0]
    # Aparatos_C.loc['Evaporador', 'Notas'] = InfoDeco.filter(regex='notas')[0]
    # #Aparatos_C.loc['Aire_Acondicionado', 'Volumen Cuarto'] = Equipos.filter(regex='largo')[0]*Equipos.filter(regex='ancho')[0]
    # InfoDeco = Equipos.filter(regex='condensador')
    # Aparatos_C.loc['Condensador', 'Capacidad'] = InfoDeco.filter(regex='capacidad')[0]
    # Aparatos_C.loc['Condensador', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
    # Aparatos_C.loc['Condensador', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]
    # Aparatos_C.loc['Condensador', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
    # Aparatos_C.loc['Condensador', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
    # Aparatos_C.loc['Condensador', 'Notas'] = InfoDeco.filter(regex='notas')[0]
    # print(Aparatos_C)

    InfoDeco = Equipos.filter(regex='evaporador')
    Aparatos_C.loc['Aire Acondicionado', 'Zona'] = zona
    Aparatos_C.loc['Aire Acondicionado', 'Tecnologia'] = tec
    Aparatos_C.loc['Aire Acondicionado', 'Ubicacion'] = InfoDeco.filter(regex='ubicacion')[0]
    #Aparatos_C.loc['Aire Acondicionado', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo_c_i_001')[0])
    #Aparatos_C.loc['Aire Acondicionado', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i_001')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Temperatura'] = InfoDeco.filter(regex='temperatura')[0]
    notasa = InfoDeco.filter(regex='notas')[0]
    # Aparatos_C.loc['Aire_Acondicionado', 'Volumen Cuarto'] = Equipos.filter(regex='largo')[0]*Equipos.filter(regex='ancho')[0]
    InfoDeco = Equipos.filter(regex='condensador')
    Aparatos_C.loc['Aire Acondicionado', 'Capacidad'] = InfoDeco.filter(regex='capacidad')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
    Aparatos_C.loc['Aire Acondicionado', 'CodigoS'] = CodStandby
    #Aparatos_C.loc['Condensador', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
    #Aparatos_C.loc['Condensador', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Notas'] = InfoDeco.filter(regex='notas')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Atacable'] = 'Si'
    Aparatos_C.loc['Aire Acondicionado', 'CodigoN'] = Equipos.filter(regex='aires_consumo_codigofindero_c_i')[0]
    #print(Equipos.filter(regex='consumo_c_i'))
    Aparatos_C.loc['Aire Acondicionado', 'Nominal'] = consumoEq(Equipos.filter(regex='aires_consumo_c_i')[0])
    Aparatos_C.loc['Aire Acondicionado', 'Clave'] = 'X'
    #print(Aparatos_C)
    return Aparatos_C
    indx=0
