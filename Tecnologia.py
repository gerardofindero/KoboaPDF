import pandas as pd
from Consumo    import calc_consumo , consumoEq
from libreriaReguladores_ import Atac_Elec

def tecnologia(Excel,Nocircuito, NomCircuito,voltaje):
    Aparatos_C = pd.DataFrame()
        # index=['Computadora','Laptop','Modem','Repetidor','Equipos Apple','Extra','Impresora','Regulador','Nobreak','Monitor','Switch','Router','HDD', 'Otro','Notas'],
        # columns=['Marca','Standby','Nominal', 'Zona','Existencia','Atacable','Notas','CodigoN','CodigoS','Clave'])

    Circuito    = Excel.loc[Nocircuito]
    Columnas    = Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("tecnologia", case=False)]
    Equipos     = Circuito[InfoEquipos]
    Equipos     = Equipos.fillna('X')
    Zona        = Equipos.filter(regex='zona_c_i')[0]
    if Zona=='otro':
        Zona    = Equipos.filter(regex='zona_otro_c_i')[0]

    Notas         = Equipos.filter(regex='notas_c_i')[0]
    #stnby        = Circuito.filter(regex='circuito_standby_c_i')[0]
    stnbyCod      = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
    stnbyEq       = Equipos.filter(regex='equipos_standby')
    stnbyEqAppl   = Equipos.filter(regex='equipos_standby_apple_c_i')
    indx=0

    for i in stnbyEq:
        if i == 1:
            if indx == 1:
                InfoDeco = Equipos.filter(regex='laptop')
                Aparatos_C.loc['Laptop', 'Standby']      = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Laptop', 'Marca']        = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Laptop', 'CodigoS']      = stnbyCod
                Aparatos_C.loc['Laptop', 'Nominal']      = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Laptop', 'CodigoN']      = InfoDeco.filter(regex='codigofindero_c_i')[0]
                Aparatos_C.loc['Laptop', 'Notas']        = Notas
                Aparatos_C.loc['Laptop', 'Clave']        = 'TC'
                Aparatos_C.loc['Laptop', 'Zona']         = Zona
                Aparatos_C.loc['Laptop', 'Atacable']     = 'Si'

            if indx == 2:
                InfoDeco = Equipos.filter(regex='computadora')
                Aparatos_C.loc['Computadora', 'Standby']      = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Computadora', 'Marca']        = InfoDeco.filter(regex='marca_c_i')[0]
                Aparatos_C.loc['Computadora', 'CodigoS']      = stnbyCod
                Aparatos_C.loc['Computadora', 'Nominal']      = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Computadora', 'CodigoN']      = InfoDeco.filter(regex='codigofindero_c_i')[0]
                Aparatos_C.loc['Computadora', 'Notas']        = Notas
                Aparatos_C.loc['Computadora', 'Clave']        = 'TC'
                Aparatos_C.loc['Computadora', 'Zona']         = Zona
                Aparatos_C.loc['Computadora', 'Atacable']     = 'Si'

            if indx == 3:
                InfoDeco = Equipos.filter(regex='monitor1')
                Aparatos_C.loc['Monitor', 'Standby']      = InfoDeco.filter(regex='standby_c_i')[0]
                Aparatos_C.loc['Monitor', 'CodigoS']      = stnbyCod
                Aparatos_C.loc['Monitor', 'Nominal']      = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Monitor', 'CodigoN']      = InfoDeco.filter(regex='codigofindero_c_i')[0]
                Aparatos_C.loc['Monitor', 'Notas']        = Notas
                Aparatos_C.loc['Monitor', 'Clave']        = 'TC'
                Aparatos_C.loc['Monitor', 'Zona']         = Zona
                Aparatos_C.loc['Monitor', 'Atacable']     = 'Si'

                InfoDeco = Equipos.filter(regex='monitor2')
                if InfoDeco.filter(regex='existencia_c_i')[0] == 'si':
                    Aparatos_C.loc['Monitor2', 'Standby']      = InfoDeco.filter(regex='standby_c_i')[0]
                    Aparatos_C.loc['Monitor2', 'CodigoS']      = stnbyCod
                    Aparatos_C.loc['Monitor2', 'Nominal']      = InfoDeco.filter(regex='consumo')[0]
                    Aparatos_C.loc['Monitor2', 'CodigoN']      = InfoDeco.filter(regex='codigofindero_c_i')[0]
                    Aparatos_C.loc['Monitor2', 'Notas']        = Notas
                    Aparatos_C.loc['Monitor2', 'Clave']        = 'TC'
                    Aparatos_C.loc['Monitor2', 'Zona']         = Zona
                    Aparatos_C.loc['Monitor2', 'Atacable']     = 'Si'

            if indx == 4:

                InfoDeco = Equipos.filter(regex='repetidor1')
                Aparatos_C.loc['Repetidor', 'Marca']      = InfoDeco.filter(regex='marca_c_i')[0]
                if Aparatos_C.loc['Repetidor', 'Marca'] == 'otro':
                    Aparatos_C.loc['Repetidor', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
                Aparatos_C.loc['Repetidor', 'Standby']    = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Repetidor', 'CodigoS']    = stnbyCod
                Aparatos_C.loc['Repetidor', 'Nominal']    = 'NA'
                Aparatos_C.loc['Repetidor', 'CodigoN']    = 'NA'
                Aparatos_C.loc['Repetidor', 'Atacable']   = 'Si'
                Aparatos_C.loc['Repetidor', 'Zona']       = Zona
                Aparatos_C.loc['Repetidor', 'Notas']       = Notas
                Aparatos_C.loc['Repetidor', 'Clave']     = 'TC'
                Aparatos_C.loc['Repetidor', 'Atacable']     = 'No'

                InfoDeco = Equipos.filter(regex='repetidor2')
                if InfoDeco.filter(regex='existencia')[0]=='si':
                    Aparatos_C.loc['Repetidor2', 'Marca']      = InfoDeco.filter(regex='marca_c_i')[0]
                    if Aparatos_C.loc['Repetidor2', 'Marca'] == 'otro':
                        Aparatos_C.loc['Repetidor2', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
                    Aparatos_C.loc['Repetidor2', 'Standby']    = InfoDeco.filter(regex='standby')[0]
                    Aparatos_C.loc['Repetidor2', 'CodigoS']    = stnbyCod
                    Aparatos_C.loc['Repetidor2', 'Nominal']    = 'NA'
                    Aparatos_C.loc['Repetidor2', 'Atacable']   = 'Si'
                    Aparatos_C.loc['Repetidor2', 'Zona']       = Zona
                    Aparatos_C.loc['Repetidor2', 'Notas']       = Notas
                    Aparatos_C.loc['Repetidor2', 'Clave']     = 'TC'
                    Aparatos_C.loc['Repetidor2', 'Atacable']     = 'No'

                InfoDeco = Equipos.filter(regex='repetidor3')
                if InfoDeco.filter(regex='existencia')[0]=='si':
                    Aparatos_C.loc['Repetidor3', 'Marca']      = InfoDeco.filter(regex='marca_c_i')[0]
                    if Aparatos_C.loc['Repetidor3', 'Marca'] == 'otro':
                        Aparatos_C.loc['Repetidor3', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
                    Aparatos_C.loc['Repetidor3', 'Standby']    = InfoDeco.filter(regex='standby')[0]
                    Aparatos_C.loc['Repetidor3', 'CodigoS']    = stnbyCod
                    Aparatos_C.loc['Repetidor3', 'Nominal']    = 'NA'
                    Aparatos_C.loc['Repetidor3', 'CodigoN']    = 'NA'
                    Aparatos_C.loc['Repetidor3', 'Atacable']   = 'Si'
                    Aparatos_C.loc['Repetidor3', 'Zona']       = Zona
                    Aparatos_C.loc['Repetidor3', 'Notas']       = Notas
                    Aparatos_C.loc['Repetidor3', 'Clave']     = 'TC'
                    Aparatos_C.loc['Repetidor3', 'Atacable']     = 'No'

            if indx == 5:
                InfoDeco = Equipos.filter(regex='modem1')
                Aparatos_C.loc['Modem', 'Marca']      = InfoDeco.filter(regex='marca_c_i')[0]
                if Aparatos_C.loc['Modem', 'Marca'] == 'otro':
                    Aparatos_C.loc['Modem', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
                Aparatos_C.loc['Modem', 'Standby']    = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Modem', 'CodigoS']    = stnbyCod
                Aparatos_C.loc['Modem', 'Nominal']    = 'NA'
                Aparatos_C.loc['Modem', 'CodigoN']    = 'NA'
                Aparatos_C.loc['Modem', 'Atacable']   = 'Si'
                Aparatos_C.loc['Modem', 'Zona']       = Zona
                Aparatos_C.loc['Modem', 'Notas']      = Notas
                Aparatos_C.loc['Modem', 'Clave']     = 'TC'
                Aparatos_C.loc['Modem', 'Atacable']     = 'No'

                InfoDeco = Equipos.filter(regex='modem2')
                Otro     = InfoDeco.filter(regex='existencia_c_i')[0]
                if Otro == 'si':
                    Aparatos_C.loc['Modem2', 'Marca']      = InfoDeco.filter(regex='marca_c_i')[0]
                    if Aparatos_C.loc['Modem2', 'Marca'] == 'otro':
                        Aparatos_C.loc['Modem2', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
                    Aparatos_C.loc['Modem2', 'Standby']    = InfoDeco.filter(regex='standby')[0]
                    Aparatos_C.loc['Modem2', 'CodigoS']    = stnbyCod
                    Aparatos_C.loc['Modem2', 'Nominal']    = 'NA'
                    Aparatos_C.loc['Modem2', 'CodigoN']    = 'NA'
                    Aparatos_C.loc['Modem2', 'Atacable']   = 'Si'
                    Aparatos_C.loc['Modem2', 'Zona']       = Zona
                    Aparatos_C.loc['Modem2', 'Notas']       = Notas
                    Aparatos_C.loc['Modem2', 'Clave']     = 'TC'
                    Aparatos_C.loc['Modem2', 'Atacable']     = 'No'

            if indx == 6:
                InfoDeco = Equipos.filter(regex='router1')
                Nota = Equipos.filter(regex='router_notas_c_i')[0]
                Aparatos_C.loc['Router', 'Marca']      = InfoDeco.filter(regex='marca_c_i')[0]
                # if Aparatos_C.loc['Router', 'Marca'] == 'otro':
                #     Aparatos_C.loc['Router', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
                Aparatos_C.loc['Router', 'Standby']    = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Router', 'CodigoS']    = stnbyCod
                Aparatos_C.loc['Router', 'Nominal']    = 'NA'
                Aparatos_C.loc['Router', 'CodigoN']    = 'NA'
                Aparatos_C.loc['Router', 'Atacable']   = 'Si'
                Aparatos_C.loc['Router', 'Zona']       = Zona
                Aparatos_C.loc['Router', 'Notas']       = Notas
                Aparatos_C.loc['Router', 'Clave']     = 'TC'
                Aparatos_C.loc['Router', 'Atacable']     = 'No'

                InfoDeco = Equipos.filter(regex='router2')
                Otro     = InfoDeco.filter(regex='existencia_c_i')[0]
                if Otro == 'si':
                    Aparatos_C.loc['Router2', 'Marca']      = InfoDeco.filter(regex='marca_c_i')[0]
                    if Aparatos_C.loc['Router2', 'Marca'] == 'otro':
                        Aparatos_C.loc['Router2', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
                    Aparatos_C.loc['Router2', 'Standby']    = InfoDeco.filter(regex='standby')[0]
                    Aparatos_C.loc['Router2', 'CodigoS']    = stnbyCod
                    Aparatos_C.loc['Router2', 'Nominal']    = 'NA'
                    Aparatos_C.loc['Router2', 'CodigoN']    = 'NA'
                    Aparatos_C.loc['Router2', 'Atacable']   = 'Si'
                    Aparatos_C.loc['Router2', 'Zona']       = Zona
                    Aparatos_C.loc['Router2', 'Notas']       = Notas
                    Aparatos_C.loc['Router2', 'Clave']     = 'TC'
                    Aparatos_C.loc['Router2', 'Atacable']     = 'No'

                InfoDeco = Equipos.filter(regex='router3')
                Otro     = InfoDeco.filter(regex='existencia_c_i')[0]

                if Otro == 'si':
                    InfoDeco = Equipos.filter(regex='router3')
                    Aparatos_C.loc['Router3', 'Marca']      = InfoDeco.filter(regex='marca_c_i')[0]
                    if Aparatos_C.loc['Router3', 'Marca'] == 'otro':
                        Aparatos_C.loc['Router3', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
                    Aparatos_C.loc['Router3', 'Standby']    = InfoDeco.filter(regex='standby')[0]
                    Aparatos_C.loc['Router3', 'CodigoS']    = stnbyCod
                    Aparatos_C.loc['Router3', 'Nominal']    = 'NA'
                    Aparatos_C.loc['Router3', 'CodigoN']    = 'NA'
                    Aparatos_C.loc['Router3', 'Atacable']   = 'Si'
                    Aparatos_C.loc['Router3', 'Zona']       = Zona
                    Aparatos_C.loc['Router3', 'Notas']       = Notas
                    Aparatos_C.loc['Router3', 'Clave']     = 'TC'
                    Aparatos_C.loc['Router3', 'Atacable']     = 'No'

                InfoDeco = Equipos.filter(regex='router4')
                Otro     = InfoDeco.filter(regex='existencia_c_i')[0]
                if Otro == 'si':
                    Aparatos_C.loc['Router4', 'Marca']      = InfoDeco.filter(regex='marca_c_i')[0]
                    if Aparatos_C.loc['Router4', 'Marca'] == 'otro':
                        Aparatos_C.loc['Router4', 'Marca']      = InfoDeco.filter(regex='marca_otro')[0]
                    Aparatos_C.loc['Router4', 'Standby']    = InfoDeco.filter(regex='standby')[0]
                    Aparatos_C.loc['Router4', 'CodigoS']    = stnbyCod
                    Aparatos_C.loc['Router4', 'Nominal']    = 'NA'
                    Aparatos_C.loc['Router4', 'CodigoN']    = 'NA'
                    Aparatos_C.loc['Router4', 'Atacable']   = 'Si'
                    Aparatos_C.loc['Router4', 'Zona']       = Zona
                    Aparatos_C.loc['Router4', 'Notas']       = Notas
                    Aparatos_C.loc['Router4', 'Clave']     = 'TC'
                    Aparatos_C.loc['Router4', 'Atacable']     = 'No'

            if indx == 8:
                InfoDeco = Equipos.filter(regex='conmutador')
                Aparatos_C.loc['Conmutador', 'Marca']      = InfoDeco.filter(regex='marca_c_i')[0]
                Aparatos_C.loc['Conmutador', 'Standby']    = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Conmutador', 'CodigoS']    = stnbyCod
                Aparatos_C.loc['Conmutador', 'Nominal']    = 'NA'
                Aparatos_C.loc['Conmutador', 'CodigoN']    = 'NA'
                Aparatos_C.loc['Conmutador', 'Notas']      = Notas
                Aparatos_C.loc['Conmutador', 'Clave']      = 'TC'
                Aparatos_C.loc['Conmutador', 'Zona']       = Zona
                Aparatos_C.loc['Conmutador', 'Atacable']     = 'No'





            if indx == 9:
                InfoDeco = Equipos.filter(regex='cctv')
                Aparatos_C.loc['CCTV', 'Marca']   = InfoDeco.filter(regex='marca_c_i')[0]
                Aparatos_C.loc['CCTV', 'Standby'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['CCTV', 'CodigoS']    = stnbyCod
                Aparatos_C.loc['CCTV', 'Nominal']    = 'NA'
                Aparatos_C.loc['CCTV', 'CodigoN']    = 'NA'
                Aparatos_C.loc['CCTV', 'Notas']       = Notas
                Aparatos_C.loc['CCTV', 'Equipos']   = InfoDeco.filter(regex='equipos_c_i')[0]
                Aparatos_C.loc['CCTV', 'CAM_Numero'] = InfoDeco.filter(regex='camaras_c_i')[0]
                Aparatos_C.loc['CCTV', 'CAM_Standby']   = InfoDeco.filter(regex='camaras_standby_c_i')[0]
                Aparatos_C.loc['CCTV', 'GRAB_Standby'] = InfoDeco.filter(regex='grabador_standby_c_i')[0]
                Aparatos_C.loc['CCTV', 'RESP_Standby']   = InfoDeco.filter(regex='respaldo_standby_c_i')[0]
                Aparatos_C.loc['CCTV', 'Clave']     = 'TC'
                Aparatos_C.loc['CCTV', 'Zona']       = Zona
                Aparatos_C.loc['CCTV', 'Atacable']     = 'No'
            if indx == 10:
                InfoDeco = Equipos.filter(regex='camara')
                Aparatos_C.loc['Camara', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                Aparatos_C.loc['Camara', 'Standby'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Camara', 'CodigoS']    = stnbyCod
                Aparatos_C.loc['Camara', 'Nominal']    = 'NA'
                Aparatos_C.loc['Camara', 'CodigoN']    = 'NA'
                Aparatos_C.loc['Camara', 'Notas']       = Notas
                Aparatos_C.loc['Camara', 'Clave']     = 'TC'
                Aparatos_C.loc['Camara', 'Zona']       = Zona
                Aparatos_C.loc['Camara', 'Atacable']     = 'No'



            if indx ==11:
                InfoDeco = Equipos.filter(regex='telefono')
                Aparatos_C.loc['Telefono', 'Marca']      = InfoDeco.filter(regex='marca_c_i')[0]
                Aparatos_C.loc['Telefono', 'Standby']      = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Telefono', 'CodigoS']    = stnbyCod
                Aparatos_C.loc['Telefono', 'Nominal']    = 'NA'
                Aparatos_C.loc['Telefono', 'CodigoN']    = 'NA'
                Aparatos_C.loc['Telefono', 'Notas']       = Notas
                Aparatos_C.loc['Telefono', 'Clave']     = 'TC'
                Aparatos_C.loc['Telefono', 'Zona']       = Zona
                Aparatos_C.loc['Telefono', 'Atacable']     = 'No'

            if indx ==12:
                InfoDeco = Equipos.filter(regex='impresora')
                Aparatos_C.loc['Impresora', 'Marca']      = InfoDeco.filter(regex='marca_c_i')[0]
                Aparatos_C.loc['Impresora', 'Standby']      = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Impresora', 'CodigoS']    = stnbyCod
                Aparatos_C.loc['Impresora', 'Nominal']    = 'NA'
                Aparatos_C.loc['Impresora', 'CodigoN']    = 'NA'
                Aparatos_C.loc['Impresora', 'Notas']       = Notas
                Aparatos_C.loc['Impresora', 'Clave']     = 'TC'
                Aparatos_C.loc['Impresora', 'Zona']       = Zona
                Aparatos_C.loc['Impresora', 'Atacable']     = 'Si'


            if indx == 13:
                InfoDeco = Equipos.filter(regex='HDD')
                Aparatos_C.loc['HDD', 'Marca'] = InfoDeco.filter(regex='cantidad')[0]
                Aparatos_C.loc['HDD', 'Standby'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['HDD', 'CodigoS']    = stnbyCod
                Aparatos_C.loc['HDD', 'Nominal']    = 'NA'
                Aparatos_C.loc['HDD', 'CodigoN']    = 'NA'
                Aparatos_C.loc['HDD', 'Notas']       = Notas
                Aparatos_C.loc['HDD', 'Clave']     = 'TC'
                Aparatos_C.loc['HDD', 'Zona']       = Zona
                Aparatos_C.loc['HDD', 'Atacable']     = 'No'


            if indx == 14:
                InfoDeco = Equipos.filter(regex='cerca')
                Aparatos_C.loc['Cerca', 'Standby'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Cerca', 'CodigoS']    = stnbyCod
                Aparatos_C.loc['Cerca', 'Nominal']    = 'NA'
                Aparatos_C.loc['Cerca', 'CodigoN']    = 'NA'
                Aparatos_C.loc['Cerca', 'Notas']       = Notas
                Aparatos_C.loc['Cerca', 'Clave']     = 'TC'
                Aparatos_C.loc['Cerca', 'Zona']       = Zona
                Aparatos_C.loc['Cerca', 'Atacable']     = 'No'

            if indx == 15:
                InfoDeco = Equipos.filter(regex='sensor_puerta')
                Aparatos_C.loc['Puerta', 'Standby'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Puerta', 'CodigoS']    = stnbyCod
                Aparatos_C.loc['Puerta', 'Nominal']    = 'NA'
                Aparatos_C.loc['Puerta', 'CodigoN']    = 'NA'
                Aparatos_C.loc['Puerta', 'Notas']       = Notas
                Aparatos_C.loc['Puerta', 'Clave']     = 'TC'
                Aparatos_C.loc['Puerta', 'Zona']       = Zona
                Aparatos_C.loc['Puerta', 'Atacable']     = 'No'

            if indx == 16:
                InfoDeco = Equipos.filter(regex='electroiman')
                Aparatos_C.loc['Electroiman', 'Standby'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Electroiman', 'CodigoS']    = stnbyCod
                Aparatos_C.loc['Electroiman', 'Nominal']    = 'NA'
                Aparatos_C.loc['Electroiman', 'CodigoN']    = 'NA'
                Aparatos_C.loc['Electroiman', 'Notas']       = Notas
                Aparatos_C.loc['Electroiman', 'Clave']     = 'TC'
                Aparatos_C.loc['Electroiman', 'Zona']       = Zona
                Aparatos_C.loc['Electroiman', 'Atacable']     = 'No'

            if indx == 17:
                InfoDeco = Equipos.filter(regex='fax')
                Aparatos_C.loc['Fax', 'Marca'] = InfoDeco.filter(regex='marca_c_i')[0]
                Aparatos_C.loc['Fax', 'Standby'] = InfoDeco.filter(regex='standby')[0]
                Aparatos_C.loc['Fax', 'CodigoS']    = stnbyCod
                Aparatos_C.loc['Fax', 'Nominal']    = 'NA'
                Aparatos_C.loc['Fax', 'CodigoN']    = 'NA'
                Aparatos_C.loc['Fax', 'Notas']       = Notas
                Aparatos_C.loc['Fax', 'Clave']     = 'TC'
                Aparatos_C.loc['Fax', 'Zona']       = Zona
                Aparatos_C.loc['Fax', 'Atacable']     = 'Si'
        indx=indx+1


    InfoDeco = Equipos.filter(regex='regulador1')
    if InfoDeco.filter(regex='existencia')[0]=='si':

        Aparatos_C.loc['Regulador', 'Zona']       = Zona
        Aparatos_C.loc['Regulador', 'Marca']      = InfoDeco.filter(regex='marca')[0]
        Aparatos_C.loc['Regulador', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['Regulador', 'CodigoS']    = stnbyCod
        Aparatos_C.loc['Regulador', 'Nominal']    = 'NA'
        Aparatos_C.loc['Regulador', 'CodigoN']    = 'NA'
        Aparatos_C.loc['Regulador', 'Equipos']      = InfoDeco.filter(regex='equipos_c_i')[0]
        if Aparatos_C.loc['Regulador', 'Equipos'] == 'otro':
            Aparatos_C.loc['Regulador', 'Equipos']      = InfoDeco.filter(regex='equipos_otro_c_i')[0]
        Aparatos_C.loc['Regulador', 'Capacidad']      = InfoDeco.filter(regex='capacidad_c_i')[0]
        Aparatos_C.loc['Regulador', 'Notas']       = 'Equipos conectados: '+Aparatos_C.loc['Regulador', 'Equipos']+','+Notas
        Aparatos_C.loc['Regulador', 'Max_Potencia'] = PotenciaMAx_Reg(Aparatos_C, Aparatos_C.loc['Regulador', 'Equipos'])
        Aparatos_C.loc['Regulador', 'Atacable'] = Atac_Elec(voltaje, Aparatos_C.loc['Regulador', 'Standby'],Aparatos_C.loc['Regulador', 'Max_Potencia'])
        Aparatos_C.loc['Regulador', 'Clave'] = 'RG,Regulador Equipos electronicos,TO,EL'+''+str(Aparatos_C.loc['Regulador', 'Max_Potencia'])
    InfoDeco = Equipos.filter(regex='regulador2')
    if InfoDeco.filter(regex='existencia')[0]=='si':
        Aparatos_C.loc['Regulador2', 'Zona']       = Zona
        Aparatos_C.loc['Regulador2', 'Marca']      = InfoDeco.filter(regex='marca')[0]
        Aparatos_C.loc['Regulador2', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['Regulador2', 'CodigoS']    = stnbyCod
        Aparatos_C.loc['Regulador2', 'Nominal']    = 'NA'
        Aparatos_C.loc['Regulador2', 'CodigoN']    = 'NA'
        Aparatos_C.loc['Regulador2', 'Equipos']      = InfoDeco.filter(regex='equipos_c_i')[0]
        if Aparatos_C.loc['Regulador2', 'Equipos'] == 'otro':
            Aparatos_C.loc['Regulador2', 'Equipos']      = InfoDeco.filter(regex='equipos_otro_c_i')[0]
        Aparatos_C.loc['Regulador2', 'Capacidad']      = InfoDeco.filter(regex='capacidad_c_i')[0]
        Aparatos_C.loc['Regulador2', 'Notas']       = 'Equipos conectados: '+Aparatos_C.loc['Regulador', 'Equipos']+','+Notas
        Aparatos_C.loc['Regulador2', 'Max_Potencia'] = PotenciaMAx_Reg(Aparatos_C,Aparatos_C.loc['Regulador2', 'Equipos'])
        Aparatos_C.loc['Regulador2', 'Atacable'] = Atac_Elec(voltaje, Aparatos_C.loc['Regulador2', 'Standby'],
                                                            Aparatos_C.loc['Regulador2', 'Max_Potencia'])
        Aparatos_C.loc['Regulador2', 'Clave'] = 'RG,Regulador Equipos electronicos,TO,EL' + '' + str(
            Aparatos_C.loc['Regulador2', 'Max_Potencia'])

        InfoDeco = Equipos.filter(regex='regulador3')
        if InfoDeco.filter(regex='existencia')[0]=='si':
            Aparatos_C.loc['Regulador3', 'Zona']       = Zona
            Aparatos_C.loc['Regulador3', 'Marca']      = InfoDeco.filter(regex='marca')[0]
            Aparatos_C.loc['Regulador3', 'Standby']    = InfoDeco.filter(regex='standby')[0]
            Aparatos_C.loc['Regulador3', 'CodigoS']    = stnbyCod
            Aparatos_C.loc['Regulador3', 'Nominal']    = 'NA'
            Aparatos_C.loc['Regulador3', 'CodigoN']    = 'NA'
            Aparatos_C.loc['Regulador3', 'Equipos']      = InfoDeco.filter(regex='equipos_c_i')[0]
            if Aparatos_C.loc['Regulador3', 'Equipos'] == 'otro':
                Aparatos_C.loc['Regulador3', 'Equipos']      = InfoDeco.filter(regex='equipos_otro_c_i')[0]
            Aparatos_C.loc['Regulador3', 'Capacidad']      = InfoDeco.filter(regex='capacidad_c_i')[0]
            Aparatos_C.loc['Regulador3', 'Notas']       = 'Equipos conectados: '+Aparatos_C.loc['Regulador', 'Equipos']+','+Notas
            Aparatos_C.loc['Regulador3', 'Max_Potencia'] = PotenciaMAx_Reg(Aparatos_C,
                                                                           Aparatos_C.loc['Regulador3', 'Equipos'])
            Aparatos_C.loc['Regulador3', 'Atacable'] = Atac_Elec(voltaje, Aparatos_C.loc['Regulador3', 'Standby'],
                                                                 Aparatos_C.loc['Regulador3', 'Max_Potencia'])
            Aparatos_C.loc['Regulador3', 'Clave'] = 'RG,Regulador Equipos electronicos,TO,EL' + '' + str(
                Aparatos_C.loc['Regulador3', 'Max_Potencia'])

        InfoDeco = Equipos.filter(regex='nobreak1')
    if InfoDeco.filter(regex='existencia')[0]=='si':
        Aparatos_C.loc['NoBreak', 'Clave']      = 'NB'
        Aparatos_C.loc['NoBreak', 'Zona']       = Zona
        Aparatos_C.loc['NoBreak', 'Marca']      = InfoDeco.filter(regex='marca')[0]
        Aparatos_C.loc['NoBreak', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['NoBreak', 'CodigoS']    = stnbyCod
        Aparatos_C.loc['NoBreak', 'Nominal']    = 'NA'
        Aparatos_C.loc['NoBreak', 'CodigoN']    = 'NA'
        Aparatos_C.loc['NoBreak', 'Equipos']      = InfoDeco.filter(regex='equipos_c_i')[0]
        if Aparatos_C.loc['NoBreak', 'Equipos'] == 'otro':
            Aparatos_C.loc['NoBreak', 'Equipos']      = InfoDeco.filter(regex='equipos_otro_c_i')[0]
        Aparatos_C.loc['NoBreak', 'Capacidad']      = InfoDeco.filter(regex='capacidad_c_i')[0]
        Aparatos_C.loc['NoBreak', 'Notas']       = 'Equipos conectados: '+Aparatos_C.loc['Regulador', 'Equipos']+','+Notas
        Aparatos_C.loc['NoBreak', 'Atacable']     = 'Si'

    InfoDeco = Equipos.filter(regex='nobreak2')
    if InfoDeco.filter(regex='existencia')[0]=='si':
        Aparatos_C.loc['NoBreak2', 'Clave']      = 'NB'
        Aparatos_C.loc['NoBreak2', 'Zona']       = Zona
        Aparatos_C.loc['NoBreak2', 'Marca']      = InfoDeco.filter(regex='marca')[0]
        Aparatos_C.loc['NoBreak2', 'Standby']    = InfoDeco.filter(regex='standby')[0]
        Aparatos_C.loc['NoBreak2', 'CodigoS']    = stnbyCod
        Aparatos_C.loc['NoBreak2', 'Nominal']    = 'NA'
        Aparatos_C.loc['NoBreak2', 'CodigoN']    = 'NA'
        Aparatos_C.loc['NoBreak2', 'Equipos']      = InfoDeco.filter(regex='equipos_c_i')[0]
        if Aparatos_C.loc['NoBreak2', 'Equipos'] == 'otro':
            Aparatos_C.loc['NoBreak2', 'Equipos']      = InfoDeco.filter(regex='equipos_otro_c_i')[0]
        Aparatos_C.loc['NoBreak2', 'Capacidad']      = InfoDeco.filter(regex='capacidad_c_i')[0]
        Aparatos_C.loc['NoBreak2', 'Notas']       = 'Equipos conectados: '+Aparatos_C.loc['Regulador', 'Equipos']+','+Notas
        Aparatos_C.loc['NoBreak2', 'Atacable']     = 'Si'

        InfoDeco = Equipos.filter(regex='nobreak3')
        if InfoDeco.filter(regex='existencia')[0]=='si':
            Aparatos_C.loc['NoBreak3', 'Clave']      = 'NB'
            Aparatos_C.loc['NoBreak3', 'Zona']       = Zona
            Aparatos_C.loc['NoBreak3', 'Marca']      = InfoDeco.filter(regex='marca')[0]
            Aparatos_C.loc['NoBreak3', 'Standby']    = InfoDeco.filter(regex='standby')[0]
            Aparatos_C.loc['NoBreak3', 'CodigoS']    = stnbyCod
            Aparatos_C.loc['NoBreak3', 'Nominal']    = 'NA'
            Aparatos_C.loc['NoBreak3', 'CodigoN']    = 'NA'
            Aparatos_C.loc['NoBreak3', 'Equipos']      = InfoDeco.filter(regex='equipos_c_i')[0]
            if Aparatos_C.loc['NoBreak3', 'Equipos'] == 'otro':
                Aparatos_C.loc['NoBreak3', 'Equipos']      = InfoDeco.filter(regex='equipos_otro_c_i')[0]
            Aparatos_C.loc['NoBreak3', 'Capacidad']      = InfoDeco.filter(regex='capacidad_c_i')[0]
            Aparatos_C.loc['NoBreak3', 'Notas']       = 'Equipos conectados: '+Aparatos_C.loc['Regulador', 'Equipos']+','+Notas
            Aparatos_C.loc['NoBreak3', 'Atacable']     = 'Si'



    # InfoDeco = Equipos.filter(regex='HDD')
    # Aparatos_C.loc['HDD', 'Marca'] = InfoDeco.filter(regex='cantidad')[0]
    # Aparatos_C.loc['HDD', 'Standby'] = InfoDeco.filter(regex='standby')[0]

    return Aparatos_C


def PotenciaMAx_Reg(Aparatos_C,Equipos):
    Equipos_Conectados=(Equipos.split())
    PotenciaMax=0
    Aparatos_C=Aparatos_C.fillna('X')
    for i in (Equipos_Conectados):
        if i=='laptop':
            if not Aparatos_C.loc['Laptop', 'Nominal']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['TV', 'Nominal']
            if not Aparatos_C.loc['Laptop', 'Standby']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['TV', 'Standby']

        if i=='computadora':
            if not Aparatos_C.loc['Computadora', 'Nominal']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['TV', 'Nominal']
            if not Aparatos_C.loc['Computadora', 'Standby']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['TV', 'Standby']

        if i=='modem':
            if not Aparatos_C.loc['Modem', 'Standby']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['Decodificador1', 'Standby']
        if i=='repetidor':
            if not Aparatos_C.loc['Repetidor', 'Standby']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['Modem', 'Standby']
        if i=='router':
            if not Aparatos_C.loc['Router', 'Standby']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['Decodificador2', 'Standby']
        if i=='conmutador':
            if not Aparatos_C.loc['Conmutador', 'Standby']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['Decodificador3', 'Standby']
        if i=='camara':
            if not Aparatos_C.loc['Camara', 'Standby']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['Repetidor', 'Standby']
        if i=='puerta':
            if not Aparatos_C.loc['Puerta', 'Nominal']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['Bluray', 'Nominal']
            if not Aparatos_C.loc['Puerta', 'Standby']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['Bluray', 'Standby']
        if i=='impresora':
            if not Aparatos_C.loc['Bocina', 'Nominal']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['Bocina', 'Nominal']
            if not Aparatos_C.loc['Bocina', 'Standby']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['Bocina', 'Standby']
        if i=='telefono':
            if not Aparatos_C.loc['Consola', 'Standby']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['Consola', 'Standby']
        if i=='cerca':
            if not Aparatos_C.loc['Consola2', 'Standby']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['Consola2', 'Standby']
        if i=='hdd':
            if not Aparatos_C.loc['EquipoExtra', 'Standby']=='X':
                PotenciaMax=PotenciaMax+Aparatos_C.loc['EquipoExtra', 'Standby']


    PotenciaMax=PotenciaMax+PotenciaMax*0.1
    return PotenciaMax
