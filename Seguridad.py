import pandas as pd
from Consumo    import calc_consumo , consumoEq


def seguridad(Excel,Nocircuito, NomCircuito):
    Aparatos_C = pd.DataFrame(
        index=['CCTV Grabador','CCTV Camara' ,'CCTV Respaldo','Cerca Electrica', 'Electroiman', 'Sensor Puertas','Regulador',
               'Nobreak', 'Camara', 'Otro', 'Notas'],
        columns=['Marca', 'Standby', 'Nominal', 'Zona', 'Existencia', 'Atacable', 'Notas','CodigoN','CodigoS'])

    Circuito = Excel.loc[Nocircuito]
    Columnas = Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("seguridad", case=False)]
    Equipos = Circuito[InfoEquipos]

    indx = 0
    for i in Equipos:
        if i == 1:
            Circuito = Equipos.filter(regex='seguridad')
            #Zona = Circuito.filter(regex='zona')[0]
            if indx == 2:
                InfoDeco = Circuito.filter(regex='cctv')
                EquipoCCTV=InfoDeco.filter(regex='cctv_equipos_c_i')

                if EquipoCCTV[1]==1:
                    print("Camaras")
                    Aparatos_C.loc['CCTV Camara', 'Standby'] = consumoEq(InfoDeco.filter(regex='camaras_standby_c_i')[0])
                    Aparatos_C.loc['CCTV Camara', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                    Aparatos_C.loc['CCTV Camara', 'Notas'] = InfoDeco.filter(regex='notas')[0]
                    Aparatos_C.loc['CCTV Camara', 'Existencia'] = 1
                    Aparatos_C.loc['CCTV Camara', 'Atacable'] = 'No'
                    Aparatos_C.loc['CCTV Camara', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                    Aparatos_C.loc['CCTV Camara', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero')[0]

                if EquipoCCTV[2] == 1:
                    print("Grabador")
                    Aparatos_C.loc['CCTV Grabador', 'Standby'] = consumoEq(InfoDeco.filter(regex='grabador_standby_c_i')[0])
                    Aparatos_C.loc['CCTV Grabador', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                    Aparatos_C.loc['CCTV Grabador', 'Notas'] = InfoDeco.filter(regex='notas')[0]
                    Aparatos_C.loc['CCTV Grabador', 'Existencia'] = 1
                    Aparatos_C.loc['CCTV Grabador', 'Atacable'] = 'No'
                    Aparatos_C.loc['CCTV Grabador', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                    Aparatos_C.loc['CCTV Grabador', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero')[0]

                if EquipoCCTV[3]==1:
                    print("Respaldo")
                    Aparatos_C.loc['CCTV Respaldo', 'Standby'] = consumoEq(InfoDeco.filter(regex='respaldo_standby_c_i')[0])
                    Aparatos_C.loc['CCTV Respaldo', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                    Aparatos_C.loc['CCTV Respaldo', 'Notas'] = InfoDeco.filter(regex='notas')[0]
                    Aparatos_C.loc['CCTV Respaldo', 'Existencia'] = 1
                    Aparatos_C.loc['CCTV Respaldo', 'Atacable'] = 'No'
                    Aparatos_C.loc['CCTV Respaldo', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                    Aparatos_C.loc['CCTV Respaldo', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero')[0]

            if indx == 3:
                InfoDeco = Circuito.filter(regex='cerca')
                # Aparatos_C.loc['Laptop', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Cerca Electrica', 'Nominal'] = InfoDeco.filter(regex='cerca')[0]
                Aparatos_C.loc['Cerca Electrica', 'Notas'] = InfoDeco.filter(regex='notas')[0]
                Aparatos_C.loc['Cerca Electrica', 'Existencia'] = 1
                Aparatos_C.loc['Cerca Electrica', 'Atacable'] = 'No'
                Aparatos_C.loc['Cerca Electrica', 'Zona'] = 'Exterior'
                Aparatos_C.loc['Cerca Electrica', 'CodigoS'] = InfoDeco.filter(regex='codigofindero')[0]
            if indx == 4:

                InfoDeco = Circuito.filter(regex='electroiman')
                # Aparatos_C.loc['Laptop', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Cerca Electrica', 'Nominal'] = InfoDeco.filter(regex='cerca')[0]
                Aparatos_C.loc['Cerca Electrica', 'Notas'] = InfoDeco.filter(regex='notas')[0]
                Aparatos_C.loc['Cerca Electrica', 'Existencia'] = 1
                Aparatos_C.loc['Cerca Electrica', 'Atacable'] = 'No'
                Aparatos_C.loc['Cerca Electrica', 'Zona'] = 'Exterior'
                Aparatos_C.loc['Cerca Electrica', 'CodigoS'] = InfoDeco.filter(regex='codigofindero')[0]
            if indx == 5:
                InfoDeco = Circuito.filter(regex='sensor')
                # Aparatos_C.loc['Laptop', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby')[0])
                Aparatos_C.loc['Cerca Electrica', 'Nominal'] = InfoDeco.filter(regex='cerca')[0]
                Aparatos_C.loc['Cerca Electrica', 'Notas'] = InfoDeco.filter(regex='notas')[0]
                Aparatos_C.loc['Cerca Electrica', 'Existencia'] = 1
                Aparatos_C.loc['Cerca Electrica', 'Atacable'] = 'No'
                Aparatos_C.loc['Cerca Electrica', 'Zona'] = 'Exterior'
                Aparatos_C.loc['Cerca Electrica', 'CodigoS'] = InfoDeco.filter(regex='codigofindero')[0]

        indx = indx + 1

    # Aparatos_C.loc['Notas', 'Marca'] = Equipos.filter(regex='comunicaciones_otro_nota_c_i')[0]
    # Aparatos_C.loc['Notas', 'Existencia'] = 1
    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()
    return Aparatos