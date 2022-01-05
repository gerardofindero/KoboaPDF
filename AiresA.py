import pandas as pd
from Consumo    import consumoEq

def airesA (Excel,Nocircuito,NomCircuito):
    Aparatos_C = pd.DataFrame(
        index=['Aire Acondicionado','Evaporador','Condensador'],
        columns=['Zona', 'Tecnologia', 'Ubicacion','Alimentacion','Nominal', 'CodigoN','Standby','CodigoS','Volumen cuarto','Existencia','Zona', 'Atacable','Clave'])

    Aparatos_C = pd.DataFrame(columns=['Aparatos'])
    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("aires", case=False)]
    Equipos= Circuito[InfoEquipos]
    Equipos=Equipos.fillna('X')
    zona = Equipos.filter(regex='zona')[0]
    tec = Equipos.filter(regex='tecnologia')[0]
    #CodStandby   = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Zona'] = zona
    Aparatos_C.loc['Aire Acondicionado', 'Tecnologia'] = tec
    Aparatos_C.loc['Aire Acondicionado', 'Alimentacion'] = Equipos.filter(regex='alimentacion_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Nominal'] = consumoEq(Equipos.filter(regex='consumo_c_i')[0])
    Aparatos_C.loc['Aire Acondicionado', 'Nominal2F3F'] = consumoEq(Equipos.filter(regex='consumo2F3F_c_i')[0])
    Aparatos_C.loc['Aire Acondicionado', 'Nominal2F3F'] = consumoEq(Equipos.filter(regex='consumo1F_c_i')[0])
    if not Equipos.filter(regex='codigofindero_c_i')[0]=='X':
        Aparatos_C.loc['Aire Acondicionado', 'CodigoN'] = Equipos.filter(regex='codigofindero_c_i')[0]
        if not Equipos.filter(regex='codigofindero2_c_i')[0]=='X':
            Aparatos_C.loc['Aire Acondicionado', 'CodigoN'] = Aparatos_C.loc['Aire Acondicionado', 'CodigoN'] \
                                                              +','+ Equipos.filter(regex='codigofindero2_c_i')[0]
    else:
        Aparatos_C.loc['Aire Acondicionado', 'CodigoN'] = Equipos.filter(regex='codigofinderoQQ_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Gasto'] = Equipos.filter(regex='gasto_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Standby'] = Equipos.filter(regex='standby_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Standby2F3F'] = Equipos.filter(regex='standby2F3F_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Standby1F'] = Equipos.filter(regex='standby1F_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Codigofuga2F3F'] = Equipos.filter(regex='codigofuga2F3F_c_i')[0]
    Aparatos_C.loc['Habitacion', 'Temperatura'] = Equipos.filter(regex='temperatura_habitacion')[0]
    Aparatos_C.loc['Aire Acondicionado', 'TemperaturaP'] = Equipos.filter(regex='temperatura_programada')[0]





    InfoDeco=Equipos.filter(regex='evaporador')
    # Aparatos_C.loc['Evaporador', 'Zona'] = zona
    # Aparatos_C.loc['Evaporador', 'Tecnologia'] = tec
    Aparatos_C.loc['Evaporador', 'Ubicacion'] = InfoDeco.filter(regex='ubicacion')[0]
    Aparatos_C.loc['Evaporador', 'ZonaTermica'] = InfoDeco.filter(regex='ubicacion')[0]
    Aparatos_C.loc['Evaporador', 'CP'] = InfoDeco.filter(regex='cp')[0]
    Aparatos_C.loc['Evaporador', ''] = InfoDeco.filter(regex='cp')[0]
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







    # Aparatos_C.loc['Aire Acondicionado', 'Temperatura'] = InfoDeco.filter(regex='temperatura')[0]
    # #notasa = InfoDeco.filter(regex='notas')[0]
    # # Aparatos_C.loc['Aire_Acondicionado', 'Volumen Cuarto'] = Equipos.filter(regex='largo')[0]*Equipos.filter(regex='ancho')[0]
    # InfoDeco = Equipos.filter(regex='condensador')
    # Aparatos_C.loc['Aire Acondicionado', 'Capacidad'] = InfoDeco.filter(regex='capacidad')[0]
    # Aparatos_C.loc['Aire Acondicionado', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
    # Aparatos_C.loc['Aire Acondicionado', 'CodigoS'] = CodStandby
    # #Aparatos_C.loc['Condensador', 'Nominal'] = consumoEq(InfoDeco.filter(regex='consumo')[0])
    # #Aparatos_C.loc['Condensador', 'CodigoN'] = InfoDeco.filter(regex='consumo_codigofindero_c_i')[0]
    # Aparatos_C.loc['Aire Acondicionado', 'Notas'] = InfoDeco.filter(regex='notas')[0]
    # Aparatos_C.loc['Aire Acondicionado', 'Atacable'] = 'Si'
    # Aparatos_C.loc['Aire Acondicionado', 'CodigoN'] = Equipos.filter(regex='aires_consumo_codigofindero_c_i')[0]
    # #print(Equipos.filter(regex='consumo_c_i'))
    # Aparatos_C.loc['Aire Acondicionado', 'Nominal'] = consumoEq(Equipos.filter(regex='aires_consumo_c_i')[0])
    # Aparatos_C.loc['Aire Acondicionado', 'Clave'] = 'X'
    print(Aparatos_C)
    return Aparatos_C

