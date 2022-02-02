import pandas as pd
#from Consumo    import consumoEq

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
    Aparatos_C.loc['Aire Acondicionado', 'Zona'] = zona
    Aparatos_C.loc['Aire Acondicionado', 'ZonaTermica'] = Equipos.filter(regex='zonaTermica')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Tecnologia'] = tec
    Aparatos_C.loc['Aire Acondicionado', 'Alimentacion'] = Equipos.filter(regex='alimentacion_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Nominal'] = Equipos.filter(regex='consumo_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Nominal2F3F'] = Equipos.filter(regex='consumo2F3F_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Nominal1F'] = Equipos.filter(regex='consumo1F_c_i')[0]
    if not Equipos.filter(regex='codigofindero_c_i')[0]=='X':
        Aparatos_C.loc['Aire Acondicionado', 'CodigoN'] = Equipos.filter(regex='codigofindero_c_i')[0]
        if not Equipos.filter(regex='codigofindero2_c_i')[0]=='X':
            Aparatos_C.loc['Aire Acondicionado', 'CodigoN'] = Aparatos_C.loc['Aire Acondicionado', 'CodigoN'] \
                                                              +','+ Equipos.filter(regex='codigofindero2_c_i')[0]
    else:
        Aparatos_C.loc['Aire Acondicionado', 'CodigoN'] = Equipos.filter(regex='codigofinderoQQ_c_i')[0]

    Aparatos_C.loc['Aire Acondicionado', 'Gasto']       = Equipos.filter(regex='gasto_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Standby']     = Equipos.filter(regex='standby_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Standby2F3F'] = Equipos.filter(regex='standby2F3F_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Standby1F']   = Equipos.filter(regex='standby1F_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Codigofuga2F3F'] = Equipos.filter(regex='codigofuga2F3F_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'TemperaturaP']   = Equipos.filter(regex='temperatura_programada')[0]
    Aparatos_C.loc['Aire Acondicionado', 'SEER']           = Equipos.filter(regex='seer_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Personas']       = Equipos.filter(regex='personas')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Marca']          = Equipos.filter(regex='marca')[0]
    Aparatos_C.loc['Aire Acondicionado', 'RefrigeranteFugas'] = Equipos.filter(regex='refrigerante_fugasTxt_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'RefrigeranteTXT']  = Equipos.filter(regex='refrigerante_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Marca']       = Equipos.filter(regex='marca')[0]
    Aparatos_C.loc['Aire Acondicionado', 'CP']          = Equipos.filter(regex='cp_c_i')[0]
    Aparatos_C.loc['Aire Acondicionado', 'Notas']       = Equipos.filter(regex='notas_c_i')[0]
    Aparatos_C.loc['Habitacion', 'Temperatura']         = Equipos.filter(regex='temperatura_habitacion')[0]

    InfoDeco = Equipos.filter(regex='cuarto')
    Aparatos_C.loc['Habitacion', 'Largo'] = InfoDeco.filter(regex='largo_c_i')[0]
    Aparatos_C.loc['Habitacion', 'Ancho'] = InfoDeco.filter(regex='ancho_c_i')[0]
    Aparatos_C.loc['Habitacion', 'Actividad'] = InfoDeco.filter(regex='actividad_c_i')[0]
    Aparatos_C.loc['Habitacion', 'Iluminacion'] = InfoDeco.filter(regex='iluminacion_c_i')[0]
    Aparatos_C.loc['Habitacion', 'FuentesCalor'] = InfoDeco.filter(regex='fuentes_calor_c_i')[0]
    Aparatos_C.loc['Habitacion', 'Cortinas'] = InfoDeco.filter(regex='cortinas_c_i')[0]
    Aparatos_C.loc['Habitacion', 'Pelicula'] = InfoDeco.filter(regex='pelicula_c_i')[0]
    Aparatos_C.loc['Habitacion', 'Paredes'] = InfoDeco.filter(regex='paredes_c_i')[0]
    Aparatos_C.loc['Habitacion', 'Filtraciones'] = InfoDeco.filter(regex='filtraciones_c_i')[0]
    Aparatos_C.loc['Habitacion', 'FiltracionesTXT'] = InfoDeco.filter(regex='filtracionesTxt_c_i')[0]



    InfoDeco=Equipos.filter(regex='evaporador')
    # Aparatos_C.loc['Evaporador', 'Zona'] = zona
    # Aparatos_C.loc['Evaporador', 'Tecnologia'] = tec
    Aparatos_C.loc['Evaporador', 'Ubicacion'] = InfoDeco.filter(regex='ubicacion')[0]
    Aparatos_C.loc['Evaporador', 'Velocidad'] = InfoDeco.filter(regex='velocidad')[0]
    Aparatos_C.loc['Evaporador', 'Alto'] = InfoDeco.filter(regex='alto')[0]
    Aparatos_C.loc['Evaporador', 'Largo'] = InfoDeco.filter(regex='largo')[0]
    Aparatos_C.loc['Evaporador', 'Limpieza'] = InfoDeco.filter(regex='limpieza')[0]
    Aparatos_C.loc['Evaporador', 'Ventilador'] = InfoDeco.filter(regex='ventilador_c_i')[0]
    Aparatos_C.loc['Evaporador', 'VentiladorTXT'] = InfoDeco.filter(regex='ventiladorTxt_c_i')[0]
    Aparatos_C.loc['Evaporador', 'Temperatura'] = InfoDeco.filter(regex='temperatura')[0]
    Aparatos_C.loc['Evaporador', 'Nominal']     = Equipos.filter(regex='consumo_c_i')[0]
    Aparatos_C.loc['Evaporador', 'Nominal2F3F'] = Equipos.filter(regex='consumo2F3F_c_i')[0]
    Aparatos_C.loc['Evaporador', 'Nominal1F'] = Equipos.filter(regex='consumo1F_c_i')[0]

    InfoDeco = Equipos.filter(regex='condensador')

    Aparatos_C.loc['Condensador', 'Refrigerante'] = InfoDeco.filter(regex='refrigerante_c_i')[0]
    Aparatos_C.loc['Condensador', 'RefrigeranteOTRO'] = InfoDeco.filter(regex='refrigerante_otro_c_i')[0]
    Aparatos_C.loc['Condensador', 'SucPRES'] = InfoDeco.filter(regex='presion_succion_c_i')[0]
    Aparatos_C.loc['Condensador', 'SucTEMP'] = InfoDeco.filter(regex='temperatura_succion_c_i')[0]
    Aparatos_C.loc['Condensador', 'DesPRES'] = InfoDeco.filter(regex='presion_descarga_c_i')[0]
    Aparatos_C.loc['Condensador', 'DesTEMP'] = InfoDeco.filter(regex='temperatura_descarga_c_i')[0]
    Aparatos_C.loc['Condensador', 'Radiacion'] = InfoDeco.filter(regex='radiacion')[0]
    Aparatos_C.loc['Condensador', 'Limpieza'] = InfoDeco.filter(regex='limpieza')[0]
    Aparatos_C.loc['Condensador', 'Ventilador'] = InfoDeco.filter(regex='ventilador_c_i')[0]
    Aparatos_C.loc['Condensador', 'VentiladorTXT'] = InfoDeco.filter(regex='ventiladorTxt_c_i')[0]
    Aparatos_C.loc['Condensador', 'Tuberias'] = InfoDeco.filter(regex='tuberias')[0]

    Aparatos_C = Aparatos_C.fillna('X')

    Aparatos_C.loc['Aire Acondicionado', 'Clave'] = 'AA'+'/'+str(Aparatos_C.loc['Aire Acondicionado', 'Nominal'])+'/'\
                                                    + Aparatos_C.loc['Aire Acondicionado', 'ZonaTermica']+'/'\
                                                    + str(Aparatos_C.loc['Aire Acondicionado', 'CP']) + '/' \
                                                    + str(Aparatos_C.loc['Aire Acondicionado', 'TemperaturaP']) + '/' \
                                                    + Aparatos_C.loc['Habitacion', 'Pelicula'] + '/'\
                                                    + Aparatos_C.loc['Habitacion', 'Paredes'] + '/' \
                                                    + Aparatos_C.loc['Condensador', 'Radiacion'] + '/' \
                                                    + Aparatos_C.loc['Habitacion', 'Filtraciones'] + '/' \
                                                    + Aparatos_C.loc['Habitacion', 'FiltracionesTXT'] + '/' \
                                                    + str(Aparatos_C.loc['Evaporador', 'Velocidad']) + '/' \
                                                    + str(Aparatos_C.loc['Evaporador', 'Alto']) + '/' \
                                                    + str(Aparatos_C.loc['Evaporador', 'Largo']) + '/' \
                                                    + str(Aparatos_C.loc['Evaporador', 'Temperatura']) + '/' \
                                                    + str(Aparatos_C.loc['Habitacion', 'Temperatura']) + '/' \
                                                    + str(Aparatos_C.loc['Habitacion', 'Alto'] )+ '/' \
                                                    + str(Aparatos_C.loc['Habitacion', 'Largo']) + '/' \
                                                    + str(Aparatos_C.loc['Aire Acondicionado', 'Personas']) + '/' \
                                                    + Aparatos_C.loc['Habitacion', 'Actividad'] + '/' \
                                                    + Aparatos_C.loc['Habitacion', 'Iluminacion'] + '/' \
                                                    + Aparatos_C.loc['Habitacion', 'FuentesCalor'] + '/' \
                                                    + Aparatos_C.loc['Evaporador', 'Limpieza']    + '/' \
                                                    + Aparatos_C.loc['Condensador', 'Limpieza']   + '/' \
                                                    + Aparatos_C.loc['Evaporador', 'Ventilador']  + '/' \
                                                    + Aparatos_C.loc['Condensador', 'Ventilador'] + '/' \
                                                    + Aparatos_C.loc['Evaporador', 'VentiladorTXT'] + '/' \
                                                    + Aparatos_C.loc['Condensador', 'VentiladorTXT'] + '/' \
                                                    + Aparatos_C.loc['Condensador', 'Tuberias'] + '/' \
                                                    + Aparatos_C.loc['Aire Acondicionado', 'RefrigeranteFugas'] + '/' \
                                                    + Aparatos_C.loc['Aire Acondicionado', 'RefrigeranteTXT'] + '/' \
                                                    + str(Aparatos_C.loc['Condensador', 'SucTEMP'] )+ '/' \
                                                    + str(Aparatos_C.loc['Condensador', 'DesTEMP'])


    Aparatos_C.loc['Aire Acondicionado', 'CodigoS'] = 'FF1'
    Aparatos_C.loc['Aire Acondicionado', 'Atacable'] = 'Si'
    Aparatos_C.loc['Aire Acondicionado', 'Standby'] = 5
    #Aparatos_C.drop(Aparatos_C[Aparatos_C.Nominal == 'X'].index, inplace=True)
    Aparatos_C.drop(['Condensador', 'Evaporador','Habitacion'],inplace=True)

    return Aparatos_C

