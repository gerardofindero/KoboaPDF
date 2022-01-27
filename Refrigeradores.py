import pandas as pd
from Condiciones import condicionesRefrigeracion
from LibreriaRefris import ClavesRefri
from Consumo import consumoEq
import math


def refrigerador(Excel,Nocircuito,NomCircuito):
    print("Entrando a funcion refrigerador en Refrigeradores.py")
    Aparatos_C = pd.DataFrame(index=['Refrigerador','Congelador','Minibar','Cava','Hielos','Refrigerador2',
                                     'Congelador2','Minibar2','Cava2','Hielos2','Adicional','Regulador Minibar','Regulador','Regulador2',
                                     'Regulador Refrigerador','Regulador Congelador','Regulador Cava','Regulador Hielos','Refrigeracion','Problemas']
                              ,columns=['Marca','Volumen','Temp Refri','Temp Conge','Pot Compresor','Temp Compresor','Nominal',
                                        'Prob Comp','Prob Descr','Empaques','Termostato','Ventilacion','Cierre', 'Existencia',
                                        'Standby','CodigoN','Notas','Claves','Zona','Prob Refr','Tuberias','Jabon','Alarma','Tipo','Clave'])

    Regulador = pd.DataFrame(index=['Regulador'],columns=['Marca','Standby','Existencia'])
    Info_R    = pd.DataFrame(index=['Refrigeracion'], columns=['Notas','CodigoS','Standby'])
    # Libreria = pd.DataFrame(index=['Refrigerador','Congelador','Minibar','Cava','Hielos'], columns=['Marca', 'Codigo', 'Texto'])


    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("equipos_refrigeracion", case=False)]

    Equipos= Circuito[InfoEquipos]
    #print(Equipos)
    indx=0
    StandbyCod =Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
    notass=Circuito.filter(regex='refrigeracion_notas_c_i')[0]
    Tierra = Circuito.filter(regex='tierra_c_i')[0]
    #MismoReg = Circuito.filter(regex='refrigeracion_mismo_regulador_c_i')[0]

    for i in Equipos:
        if i == 1:
            if indx == 1:

                NomAparato = 'refrigerador1'
                InfoDeco = Circuito.filter(regex=NomAparato)

                Aparatos_C.loc['Refrigerador', 'Existencia'] = 1
                #Aparatos_C.loc['Regulador', 'Existencia'] = 1

                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]
                try:   Aparatos_C.loc['Refrigerador', 'Encendido'] = InfoDeco.filter(regex="encendido_c_i")[0]
                except:Aparatos_C.loc['Refrigerador', 'Encendido'] = 60
                if InfoDeco.filter(regex='zona_c_i')[0] == 'otro':
                    Aparatos_C.loc['Refrigerador', 'Zona'] = InfoDeco.filter(regex='zona_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Refrigerador', 'Zona'] = InfoDeco.filter(regex='zona_c_i')[0]

                if InfoDeco.filter(regex='marca')[0] =='otro':
                    Aparatos_C.loc['Refrigerador', 'Marca'] = InfoDeco.filter(regex='marca_otro')[0]
                else:
                    Aparatos_C.loc['Refrigerador', 'Marca'] = InfoDeco.filter(regex='marca')[0]

                Aparatos_C.loc['Refrigerador', 'Volumen'] = (float(alto) * float(ancho) * float(profundo))
                try:   Aparatos_C.loc['Refrigerador', 'Temp Refri'] = InfoDeco.filter(regex='trefri')[0]
                except:Aparatos_C.loc['Refrigerador', 'Temp Refri'] = 100
                try:   Aparatos_C.loc['Refrigerador', 'Temp Conge'] = InfoDeco.filter(regex='tconge')[0]
                except:Aparatos_C.loc['Refrigerador', 'Temp Conge'] = 100

                PotCompresor=InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Refrigerador', 'Pot Compresor'] =Watt
                try: Aparatos_C.loc['Refrigerador', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                except: Aparatos_C.loc['Refrigerador', 'Temp Compresor'] =100
                Aparatos_C.loc['Refrigerador', 'Prob Refr']   = InfoDeco.filter(regex='problemas_c_i')[0]

                Aparatos_C.loc['Refrigerador', 'Prob Comp']   = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Refrigerador', 'Prob Descr']  = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Refrigerador', 'Empaques']    = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Refrigerador', 'Difusor'] = InfoDeco.filter(regex='ventilador_c_i')[0]
                #Aparatos_C.loc['Refrigerador', 'Termostato']  = InfoDeco.filter(regex='termostato')[0]
                Aparatos_C.loc['Refrigerador', 'Encerrado'] = InfoDeco.filter(regex='encerrado_c_i')[0]
                Aparatos_C.loc['Refrigerador', 'Ventilas'] = InfoDeco.filter(regex='ventilas_c_i')[0]
                Aparatos_C.loc['Refrigerador', 'Cierre']      = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Refrigerador', 'Dispensador'] = InfoDeco.filter(regex='dispensador')[0]
                Aparatos_C.loc['Refrigerador', 'Tuberias']    = InfoDeco.filter(regex='tuberias')[0]
                Aparatos_C.loc['Refrigerador', 'Jabon']       = InfoDeco.filter(regex='jabon')[0]
                Aparatos_C.loc['Refrigerador', 'Alarma']      = InfoDeco.filter(regex='alarma')[0]
                Aparatos_C.loc['Refrigerador', 'Tipo']      = InfoDeco.filter(regex='tipo')[0]
                Aparatos_C.loc['Refrigerador', 'Dispensador']      = InfoDeco.filter(regex='dispensador')[0]
                Aparatos_C.loc['Refrigerador', 'CodigoN']     = InfoDeco.filter(regex='codigofindero')[0]

                if not pd.isna(InfoDeco.filter(regex='standby_c_i')[0]) :
                    Aparatos_C.loc['Refrigerador', 'Standby'] = consumoEq( InfoDeco.filter(regex='standby_c_i')[0])
                    Aparatos_C.loc['Refrigerador', 'CodigoS'] = StandbyCod
                else:
                    Aparatos_C.loc['Refrigerador', 'Standby'] = 0
                    Aparatos_C.loc['Refrigerador', 'CodigoS'] = ' '

                Aparatos_C.loc['Refrigerador', 'Notas'] = Circuito.filter(regex='refrigeracion_notas_c_i')[0]
                Aparatos_C.loc['Refrigerador', 'Clave'] = 'RF'


                ##################
                #print(InfoDeco.filter(regex='regulador_c_i')[0])
                if InfoDeco.filter(regex='regulador_c_i')[0] =='regulador':
                    if InfoDeco.filter(regex='regulador_marca_c_i')[0] =='otro':
                        Aparatos_C.loc['Regulador Refrigerador', 'Marca'] =   InfoDeco.filter(regex='regulador_otro')[0]
                    else:
                        Aparatos_C.loc['Regulador Refrigerador', 'Marca'] =   InfoDeco.filter(regex='regulador_marca')[0]
                    Aparatos_C.loc['Regulador Refrigerador', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_consumo')[0])
                    Aparatos_C.loc['Regulador Refrigerador', 'CodigoS'] = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
                    Aparatos_C.loc['Regulador Refrigerador', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador Refrigerador', 'Notas'] = notass
                    Aparatos_C.loc['Regulador Refrigerador', 'Zona'] = Aparatos_C.loc['Refrigerador', 'Zona']

                Aparatos_C.loc['Problemas', 'Marca'] = Circuito.filter(regex='_problemas_otro_c_i')[0]
                Aparatos_C.loc['Problemas', 'Existencia']=1


#########################
            if indx == 2:
                NomAparato = 'congelador1'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Congelador', 'Existencia'] = 1
                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]

                if InfoDeco.filter(regex='zona_c_i')[0] == 'otro':
                    Aparatos_C.loc['Congelador', 'Zona'] = InfoDeco.filter(regex='zona_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Congelador', 'Zona'] = InfoDeco.filter(regex='zona_c_i')[0]


                if InfoDeco.filter(regex='marca_c_i')[0] == 'otro':
                    Aparatos_C.loc['Congelador', 'Marca'] = InfoDeco.filter(regex='marca_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Congelador', 'Marca'] = InfoDeco.filter(regex='marca_c_i')[0]

                Aparatos_C.loc['Congelador', 'Volumen'] = float(alto) * float(ancho) * float(profundo)
                try:    Aparatos_C.loc['Congelador', 'Temp Conge'] = InfoDeco.filter(regex='congelador1_temp')[0]
                except: Aparatos_C.loc['Congelador', 'Temp Conge'] = 100
                Aparatos_C.loc['Congelador', 'Temp Refr'] = 100
                print(Aparatos_C.loc['Congelador', 'Temp Refr'])
                PotCompresor = InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Congelador', 'Pot Compresor'] = Watt
                try:   Aparatos_C.loc['Congelador', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                except:Aparatos_C.loc['Congelador', 'Temp Compresor'] = 100
                try:   Aparatos_C.loc['Congelador', 'Encendido'] = InfoDeco.filter(regex="encendido_c_i")[0]
                except:Aparatos_C.loc['Congelador', 'Encendido'] = 60
                Aparatos_C.loc['Congelador', 'Prob Comp']   = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Congelador', 'Prob Descr']  = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Congelador', 'Empaques']    = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Congelador', 'Termostato']  = InfoDeco.filter(regex='termostato')[0]
                #Aparatos_C.loc['Congelador', 'Ventilacion'] = InfoDeco.filter(regex='ventilacion')[0]
                Aparatos_C.loc['Congelador','Disposicion']  =InfoDeco.filter(regex='disposicion')[0]
                Aparatos_C.loc['Congelador', 'Cierre']      = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Congelador', 'Tipo']        = InfoDeco.filter(regex='tipo')[0]
                Aparatos_C.loc['Congelador', 'Dispensador'] = InfoDeco.filter(regex='dispensador')[0]
                Aparatos_C.loc['Congelador', 'Alarma']      = InfoDeco.filter(regex='alarma')[0]
                Aparatos_C.loc['Congelador', 'Ventilas'] = InfoDeco.filter(regex='ventilas_c_i')[0]
                Aparatos_C.loc['Congelador', 'Encerrado'] = InfoDeco.filter(regex='encerrado_c_i')[0]
                Aparatos_C.loc['Congelador', 'Prob Refr']   = InfoDeco.filter(regex='problemas_c_i')[0]
                Aparatos_C.loc['Congelador', 'Difusor'] = InfoDeco.filter(regex='ventilador_c_i')[0]
                Aparatos_C.loc['Congelador', 'Tuberias']    = InfoDeco.filter(regex='tuberias')[0]
                #print("encendido conge",InfoDeco.filter(regex="encendido_c_i")[0])
                Aparatos_C.loc['Congelador', 'CodigoN']     = InfoDeco.filter(regex='codigofindero')[0]
                Aparatos_C.loc['Congelador', 'Notas']       = notass
                if not pd.isna(InfoDeco.filter(regex='standby_c_i')[0]) :
                    Aparatos_C.loc['Congelador', 'Standby'] = consumoEq( InfoDeco.filter(regex='standby_c_i')[0])
                    Aparatos_C.loc['Congelador', 'CodigoS'] = StandbyCod
                else:
                    Aparatos_C.loc['Congelador', 'Standby'] = 0
                    Aparatos_C.loc['Congelador', 'CodigoS'] = ' '
                Aparatos_C.loc['Congelador', 'Clave'] = 'CN'

                if InfoDeco.filter(regex='regulador_c_i')[0] != 'ninguno':
                    Aparatos_C.loc['Regulador Congelador', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_consumo')[0])
                    if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
                        Aparatos_C.loc['Regulador Congelador', 'Marca'] =  InfoDeco.filter(regex='regulador_marca')[0]
                    else:
                        Aparatos_C.loc['Regulador Congelador', 'Marca'] =  InfoDeco.filter(regex='regulador_marca')[0]
                    Aparatos_C.loc['Regulador Congelador', 'CodigoS'] = StandbyCod
                    Aparatos_C.loc['Regulador Congelador', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador Congelador', 'Notas'] = notass
                    Aparatos_C.loc['Regulador Congelador', 'Zona'] = Aparatos_C.loc['Congelador', 'Zona']

            if indx == 3:
                NomAparato = 'minibar1'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Minibar', 'Existencia'] = 1
                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]
                try:   Aparatos_C.loc['Minibar', 'Encendido'] = InfoDeco.filter(regex="encendido_c_i")[0]
                except:Aparatos_C.loc['Minibar', 'Encendido'] = 60
                if InfoDeco.filter(regex='marca_c_i')[0] == 'otro':
                    Aparatos_C.loc['Minibar', 'Marca'] = InfoDeco.filter(regex='marca_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Minibar', 'Marca'] = InfoDeco.filter(regex='marca_c_i')[0]

                if InfoDeco.filter(regex='zona_c_i')[0] == 'otro':
                    Aparatos_C.loc['Minibar', 'Zona'] = InfoDeco.filter(regex='zona_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Minibar', 'Zona'] = InfoDeco.filter(regex='zona_c_i')[0]

                Aparatos_C.loc['Minibar', 'Volumen'] = float(alto) * float(ancho) * float(profundo)
                try:   Aparatos_C.loc['Minibar', 'Temp Refri'] = InfoDeco.filter(regex='minibar1_temp_c_i')[0]
                except:Aparatos_C.loc['Minibar', 'Temp Refri'] = 100
                try:   Aparatos_C.loc['Minibar', 'Temp Conge'] = InfoDeco.filter(regex='tconge')[0]
                except:Aparatos_C.loc['Minibar', 'Temp Conge'] = 100
                #Aparatos_C.loc['Minibar', 'Pot Compresor'] = InfoDeco.filter(regex='compresor_potencia')[0]
                Aparatos_C.loc['Minibar', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
                PotCompresor = InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Minibar', 'Pot Compresor'] = Watt
                Aparatos_C.loc['Minibar', 'Notas'] = notass

                try: Aparatos_C.loc['Minibar', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                except: Aparatos_C.loc['Minibar', 'Temp Compresor'] = 100
                Aparatos_C.loc['Minibar', 'Prob Refr'] = InfoDeco.filter(regex='problemas_c_i')[0]
                Aparatos_C.loc['Minibar', 'Prob Comp']      = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Minibar', 'Prob Descr']     = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Minibar', 'Empaques']       = InfoDeco.filter(regex='empaques')[0]
                #Aparatos_C.loc['Minibar', 'Termostato']     = InfoDeco.filter(regex='termostato')[0]
                Aparatos_C.loc['Minibar', 'Encerrado'] = InfoDeco.filter(regex='encerrado_c_i')[0]
                Aparatos_C.loc['Minibar', 'Ventilas'] = InfoDeco.filter(regex='ventilas_c_i')[0]
                Aparatos_C.loc['Minibar', 'Difusor'] = InfoDeco.filter(regex='ventilador_c_i')[0]

                Aparatos_C.loc['Minibar', 'Alarma'] = InfoDeco.filter(regex='alarma')[0]
                #Aparatos_C.loc['Minibar', 'Tipo']    = InfoDeco.filter(regex='Tipo')[0]
                Aparatos_C.loc['Minibar', 'Cierre']         = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Minibar', 'Tipo']           = InfoDeco.filter(regex='tipo')[0]
                Aparatos_C.loc['Minibar', 'Dispensador']    = InfoDeco.filter(regex='dispensador')[0]
                Aparatos_C.loc['Minibar', 'Tuberias'] = InfoDeco.filter(regex='tuberias')[0]
                Aparatos_C.loc['Minibar', 'Jabon'] = InfoDeco.filter(regex='jabon')[0]
                Aparatos_C.loc['Minibar', 'Standby'] = 0
                Aparatos_C.loc['Minibar', 'Clave'] = 'MB'

                if InfoDeco.filter(regex='regulador_c_i')[0] != 'ninguno':

                    Aparatos_C.loc['Regulador Minibar', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_consumo')[0])
                    if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
                        Aparatos_C.loc['Regulador Minibar', 'Marca'] = 'Minibar ' + InfoDeco.filter(regex='regulador_marca')[0]
                    else:
                        Aparatos_C.loc['Regulador Minibar', 'Marca'] = 'Minibar ' + InfoDeco.filter(regex='regulador_marca_otro')[0]

                    Aparatos_C.loc['Regulador Minibar', 'CodigoS'] = StandbyCod
                    Aparatos_C.loc['Regulador Minibar', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador Minibar', 'Notas'] = notass
                    Aparatos_C.loc['Regulador Minibar', 'Zona'] = Aparatos_C.loc['Minibar', 'Zona']


            if indx == 4:
                NomAparato = 'cava1'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Cava', 'Existencia'] = 1
                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]
                if InfoDeco.filter(regex='marca_c_i')[0] == 'otro':
                    Aparatos_C.loc['Cava', 'Marca'] = InfoDeco.filter(regex='marca_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Cava', 'Marca'] = InfoDeco.filter(regex='marca_c_i')[0]

                if InfoDeco.filter(regex='zona_c_i')[0] == 'otro':
                    Aparatos_C.loc['Cava', 'Zona'] = InfoDeco.filter(regex='zona_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Cava', 'Zona'] = InfoDeco.filter(regex='zona_c_i')[0]
                Aparatos_C.loc['Cava', 'Volumen'] = float(alto) * float(ancho) * float(profundo)
                try:   Aparatos_C.loc['Cava', 'Temp Refri'] = InfoDeco.filter(regex='temp_c_i')[0]
                except:Aparatos_C.loc['Cava', 'Temp Refri'] = 100
                Aparatos_C.loc['Cava', 'Temp Conge'] = 100
                Aparatos_C.loc['Cava', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
                #Aparatos_C.loc['Cava', 'Pot Compresor'] = InfoDeco.filter(regex='compresor_potencia')[0]
                PotCompresor = InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Cava', 'Pot Compresor'] = Watt
                try:   Aparatos_C.loc['Cava', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                except:Aparatos_C.loc['Cava', 'Temp Compresor'] = 100
                Aparatos_C.loc['Cava', 'Difusor']   = InfoDeco.filter(regex='ventilador_c_i')[0]
                Aparatos_C.loc['Cava', 'Tuberias']  = InfoDeco.filter(regex='tuberias')[0]
                Aparatos_C.loc['Cava', 'Prob Refr'] = InfoDeco.filter(regex='problemas_c_i')[0]
                Aparatos_C.loc['Cava', 'Encerrado'] = InfoDeco.filter(regex='encerrado_c_i')[0]
                Aparatos_C.loc['Cava', 'Ventilas']  = InfoDeco.filter(regex='ventilas_c_i')[0]
                Aparatos_C.loc['Cava', 'Alarma']    = InfoDeco.filter(regex='alarma')[0]

                Aparatos_C.loc['Cava', 'Prob Comp']      = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Cava', 'Prob Descr']     = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Cava', 'Empaques']       = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Cava', 'Termostato']     = InfoDeco.filter(regex='termostato')[0]
                #Aparatos_C.loc['Cava', 'Ventilacion']    = InfoDeco.filter(regex='ventilacion')[0]
                Aparatos_C.loc['Cava', 'Cierre']         = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Cava', 'Tipo']           = InfoDeco.filter(regex='tipo')[0]
                #Aparatos_C.loc['Cava', 'Dispensador']    = InfoDeco.filter(regex='dispensador')[0]
                try:   Aparatos_C.loc['Cava', 'Encendido'] = InfoDeco.filter(regex="encendido_c_i")[0]
                except:Aparatos_C.loc['Cava', 'Encendido'] = 60
                Aparatos_C.loc['Cava', 'CodigoN']        = InfoDeco.filter(regex='codigofindero')[0]
                Aparatos_C.loc['Cava', 'Notas'] = notass

                if not pd.isna(InfoDeco.filter(regex='standby_c_i')[0]) :
                    Aparatos_C.loc['Cava', 'Standby'] = consumoEq( InfoDeco.filter(regex='standby_c_i')[0])
                    Aparatos_C.loc['Cava', 'CodigoS'] = StandbyCod
                else:
                    Aparatos_C.loc['Cava', 'Standby'] = 0
                    Aparatos_C.loc['Cava', 'CodigoS'] = ' '
                Aparatos_C.loc['Cava', 'Clave'] = 'CV'

                # Aparatos_C.loc['Cava', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby_c_i')[0])
                # Aparatos_C.loc['Cava', 'CodigoS'] =Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]

                if InfoDeco.filter(regex='regulador_c_i')[0] == 'regulador':
                    Aparatos_C.loc['Regulador Cava', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_consumo')[0])
                    if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
                        Aparatos_C.loc['Regulador Cava', 'Marca'] = 'Cava ' + InfoDeco.filter(regex='regulador_marca')[0]
                    else:
                        Aparatos_C.loc['Regulador Cava', 'Marca'] = 'Cava ' + \
                                                               InfoDeco.filter(regex='regulador_marca_otro')[0]

                    Aparatos_C.loc['Regulador Cava', 'CodigoS'] = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
                    Aparatos_C.loc['Regulador Cava', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador Cava', 'Notas'] = notass
                    Aparatos_C.loc['Regulador Cava', 'Zona'] = Aparatos_C.loc['Cava', 'Zona']




            if indx == 5:
                NomAparato = 'hielos1'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Hielos', 'Existencia'] = 1
                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]

                if InfoDeco.filter(regex='marca_c_i')[0] == 'otro':
                    Aparatos_C.loc['Hielos', 'Marca'] = InfoDeco.filter(regex='marca_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Hielos', 'Marca'] = InfoDeco.filter(regex='marca_c_i')[0]

                if InfoDeco.filter(regex='zona_c_i')[0] == 'otro':
                    Aparatos_C.loc['Hielos', 'Zona'] = InfoDeco.filter(regex='zona_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Hielos', 'Zona'] = InfoDeco.filter(regex='zona_c_i')[0]

                Aparatos_C.loc['Hielos', 'Volumen'] = float(alto) * float(ancho) * float(profundo)
                Aparatos_C.loc['Hielos', 'Temp Refri'] = InfoDeco.filter(regex='hielos1_temp_c_i')[0]
                Aparatos_C.loc['Hielos', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
                #Aparatos_C.loc['Cava', 'Pot Compresor'] = InfoDeco.filter(regex='compresor_potencia')[0]
                PotCompresor = InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Hielos', 'Pot Compresor'] = Watt
                Aparatos_C.loc['Hielos', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                Aparatos_C.loc['Hielos', 'Prob Comp'] = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Hielos', 'Prob Descr'] = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Hielos', 'Empaques'] = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Hielos', 'Termostato'] = InfoDeco.filter(regex='termostato')[0]
                Aparatos_C.loc['Hielos', 'Ventilacion'] = InfoDeco.filter(regex='ventilacion')[0]
                Aparatos_C.loc['Hielos', 'Cierre'] = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Hielos', 'Tipo']        = InfoDeco.filter(regex='tipo')[0]
                Aparatos_C.loc['Hielos', 'Dispensador'] = InfoDeco.filter(regex='dispensador')[0]
                Aparatos_C.loc['Hielos', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
                Aparatos_C.loc['Hielos', 'Notas'] = notass
                Aparatos_C.loc['Hielos', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby_c_i')[0])
                Aparatos_C.loc['Hielos', 'CodigoS'] = StandbyCod
                Aparatos_C.loc['Hielos', 'Clave'] = 'HL'

                if InfoDeco.filter(regex='regulador_c_i')[0] != 'ninguno':
                    Aparatos_C.loc['Regulador Hielos', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_consumo')[0])
                    if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
                        Aparatos_C.loc['Regulador Hielos', 'Marca'] = 'Hielos ' + InfoDeco.filter(regex='regulador_marca')[0]
                    else:
                        Aparatos_C.loc['Regulador Hielos', 'Marca'] = 'Hielos ' + InfoDeco.filter(regex='regulador_marca_otro')[0]
                    #Aparatos_C.loc['Regulador', 'CodigoS'] = InfoDeco.filter(regex='regulador_consumo_codigofindero')[0]
                    Aparatos_C.loc['Regulador Hielos', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador Hielos', 'Notas'] = notass
                    Aparatos_C.loc['Regulador Hielos', 'Zona'] = Aparatos_C.loc['Hielos', 'Zona']

            if indx == 6:

                NomAparato = 'refrigerador2'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Refrigerador2', 'Existencia'] = 1
                #Aparatos_C.loc['Regulador', 'Existencia'] = 1

                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]

                if InfoDeco.filter(regex='zona_c_i')[0] == 'otro':
                    Aparatos_C.loc['Refrigerador2', 'Zona'] = InfoDeco.filter(regex='zona_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Refrigerador2', 'Zona'] = InfoDeco.filter(regex='zona_c_i')[0]

                if InfoDeco.filter(regex='marca')[0] == 'otro':
                    Aparatos_C.loc['Refrigerador2', 'Marca'] = InfoDeco.filter(regex='marca_otro')[0]
                else:
                    Aparatos_C.loc['Refrigerador2', 'Marca'] = InfoDeco.filter(regex='marca')[0]


                Aparatos_C.loc['Refrigerador2', 'Volumen'] = (float(alto) * float(ancho) * float(profundo))
                Aparatos_C.loc['Refrigerador2', 'Temp Refri'] = InfoDeco.filter(regex='trefri')[0]
                Aparatos_C.loc['Refrigerador2', 'Temp Conge'] = InfoDeco.filter(regex='tconge')[0]
                PotCompresor=InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Refrigerador2', 'Pot Compresor'] =Watt
                if not InfoDeco.filter(regex='compresor_temp')[0]:

                    Aparatos_C.loc['Refrigerador2', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                else:
                    Aparatos_C.loc['Refrigerador2', 'Temp Compresor'] =0

                Aparatos_C.loc['Refrigerador2', 'Prob Comp'] = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Refrigerador2', 'Prob Descr'] = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Refrigerador2', 'Empaques'] = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Refrigerador2', 'Termostato'] = InfoDeco.filter(regex='termostato')[0]
                Aparatos_C.loc['Refrigerador2', 'Ventilacion'] = InfoDeco.filter(regex='ventilacion_c_i')[0]
                Aparatos_C.loc['Refrigerador2', 'Tipo'] = InfoDeco.filter(regex='ventilacion')[0]
                Aparatos_C.loc['Refrigerador2', 'Dispensador'] = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Refrigerador2', 'Cierre'] = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Refrigerador2', 'Standby'] = 0
                Aparatos_C.loc['Refrigerador2', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
                Aparatos_C.loc['Refrigerador2', 'Clave'] = 'RF'
                Aparatos_C.loc['Regulador', 'Notas'] = notass
                #Aparatos_C.loc['Regulador2', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_consumo')[0])
                #Aparatos_C.loc['Regulador2', 'Marca'] = InfoDeco.filter(regex='regulador_marca')[0]
                #Aparatos_C.loc['Regulador2', 'Existencia'] = 1

                Aparatos_C.loc['Problemas', 'Marca'] = Circuito.filter(regex='_problemas_otro_c_i')[0]
                Aparatos_C.loc['Problemas', 'Existencia']=1


            if indx == 7:
                NomAparato = 'congelador2'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Congelador2', 'Existencia'] = 1
                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]

                if InfoDeco.filter(regex='zona_c_i')[0] == 'otro':
                    Aparatos_C.loc['Congelador2', 'Zona'] = InfoDeco.filter(regex='zona_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Congelador2', 'Zona'] = InfoDeco.filter(regex='zona_c_i')[0]


                if InfoDeco.filter(regex='marca_c_i')[0] == 'otro':
                    Aparatos_C.loc['Congelador2', 'Marca'] = InfoDeco.filter(regex='marca_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Congelador2', 'Marca'] = InfoDeco.filter(regex='marca_c_i')[0]

                Aparatos_C.loc['Congelador2', 'Volumen'] = float(alto) * float(ancho) * float(profundo)
                Aparatos_C.loc['Congelador2', 'Temp Conge'] = InfoDeco.filter(regex='congelador2_temp')[0]
                Aparatos_C.loc['Congelador2', 'Pot Compresor'] = InfoDeco.filter(regex='compresor_potencia_c_i')[0]
                PotCompresor = InfoDeco.filter(regex='compresor_potencia_c_i')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Congelador2', 'Pot Compresor'] = Watt
                Aparatos_C.loc['Congelador2', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                Aparatos_C.loc['Congelador2', 'Prob Comp']   = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Congelador2', 'Prob Descr']  = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Congelador2', 'Empaques']    = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Congelador2', 'Termostato']  = InfoDeco.filter(regex='termostato')[0]
                Aparatos_C.loc['Congelador2', 'Ventilacion'] = InfoDeco.filter(regex='ventilacion')[0]
                Aparatos_C.loc['Congelador2','Disposicion']  =InfoDeco.filter(regex='disposicion')[0]
                Aparatos_C.loc['Congelador2', 'Cierre']      = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Congelador2', 'Tipo']        = InfoDeco.filter(regex='tipo')[0]
                Aparatos_C.loc['Congelador2', 'Dispensador'] = InfoDeco.filter(regex='dispensador')[0]
                Aparatos_C.loc['Congelador2', 'CodigoN']     = InfoDeco.filter(regex='codigofindero')[0]
                Aparatos_C.loc['Congelador2', 'Notas']       = notass
                Aparatos_C.loc['Congelador2', 'Clave'] = 'CN'
                if not pd.isna(InfoDeco.filter(regex='standby_c_i')[0]) :
                    Aparatos_C.loc['Congelador2', 'Standby'] = consumoEq( InfoDeco.filter(regex='standby_c_i')[0])
                    Aparatos_C.loc['Congelador2', 'CodigoS'] = StandbyCod
                else:
                    Aparatos_C.loc['Congelador2', 'Standby'] = 0
                    Aparatos_C.loc['Congelador2', 'CodigoS'] = ' '
                if InfoDeco.filter(regex='regulador_c_i')[0] != 'ninguno':
                    Aparatos_C.loc['Regulador Congelador2', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_consumo')[0])
                    if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
                        Aparatos_C.loc['Regulador Congelador2', 'Marca'] =  InfoDeco.filter(regex='regulador_marca')[0]
                    else:
                        Aparatos_C.loc['Regulador Congelador2', 'Marca'] =  InfoDeco.filter(regex='regulador_marca')[0]
                    Aparatos_C.loc['Regulador Congelador2', 'CodigoS'] = StandbyCod
                    Aparatos_C.loc['Regulador Congelador2', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador Congelador2', 'Notas'] = notass

            if indx == 8:
                NomAparato = 'minibar2'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Minibar2', 'Existencia'] = 1
                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]
                Aparatos_C.loc['Minibar2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Minibar2', 'Volumen'] = float(alto) * float(ancho) * float(profundo)
                Aparatos_C.loc['Minibar2', 'Temp Refri'] = InfoDeco.filter(regex='minibar1_temp_c_i')[0]
                Aparatos_C.loc['Minibar2', 'Pot Compresor'] = InfoDeco.filter(regex='compresor_potencia')[0]
                Aparatos_C.loc['Minibar2', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
                PotCompresor = InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Minibar2', 'Pot Compresor'] = Watt
                Aparatos_C.loc['Minibar2', 'Notas'] = notass
                Aparatos_C.loc['Minibar2', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                Aparatos_C.loc['Minibar2', 'Prob Comp'] = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Minibar2', 'Prob Descr'] = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Minibar2', 'Empaques'] = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Minibar2', 'Termostato'] = InfoDeco.filter(regex='termostato')[0]
                Aparatos_C.loc['Minibar2', 'Ventilacion'] = InfoDeco.filter(regex='ventilacion')[0]
                Aparatos_C.loc['Minibar2', 'Cierre'] = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Minibar2', 'Tipo'] = InfoDeco.filter(regex='tipo')[0]
                Aparatos_C.loc['Minibar2', 'Dispensador'] = InfoDeco.filter(regex='dispensador')[0]
                Aparatos_C.loc['Minibar2', 'Standby'] = 0
                Aparatos_C.loc['Minibar2', 'Clave'] = 'MB'

                if InfoDeco.filter(regex='regulador_c_i')[0] != 'ninguno':

                    Aparatos_C.loc['Regulador', 'Standby'] = consumoEq(
                        InfoDeco.filter(regex='regulador_consumo')[0])
                    if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
                        Aparatos_C.loc['Regulador', 'Marca'] = 'Minibar ' + \
                                                               InfoDeco.filter(regex='regulador_marca')[0]
                    else:
                        Aparatos_C.loc['Regulador', 'Marca'] = 'Minibar ' + \
                                                               InfoDeco.filter(regex='regulador_marca_otro')[0]

                    Aparatos_C.loc['Regulador', 'CodigoS'] = StandbyCod
                    Aparatos_C.loc['Regulador', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador', 'Notas'] = notass

            if indx == 9:
                NomAparato = 'cava2'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Cava2', 'Existencia'] = 1
                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]
                Aparatos_C.loc['Cava2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Cava2', 'Volumen'] = float(alto) * float(ancho) * float(profundo)
                Aparatos_C.loc['Cava2', 'Temp Refri'] = InfoDeco.filter(regex='temp_c_i')[0]
                Aparatos_C.loc['Cava2', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
                PotCompresor = InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Cava2', 'Pot Compresor'] = Watt
                Aparatos_C.loc['Cava2', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                Aparatos_C.loc['Cava2', 'Prob Comp'] = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Cava2', 'Prob Descr'] = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Cava2', 'Empaques'] = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Cava2', 'Termostato'] = InfoDeco.filter(regex='termostato')[0]
                Aparatos_C.loc['Cava2', 'Ventilacion'] = InfoDeco.filter(regex='ventilacion')[0]
                Aparatos_C.loc['Cava2', 'Cierre'] = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Cava2', 'Tipo'] = InfoDeco.filter(regex='tipo')[0]
                Aparatos_C.loc['Cava2', 'Dispensador'] = InfoDeco.filter(regex='dispensador')[0]
                Aparatos_C.loc['Cava2', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
                Aparatos_C.loc['Cava2', 'Notas'] = notass
                Aparatos_C.loc['Cava2', 'Clave'] = 'CV'

                if not pd.isna(InfoDeco.filter(regex='standby_c_i')[0]):
                    Aparatos_C.loc['Cava2', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby_c_i')[0])
                    Aparatos_C.loc['Cava2', 'CodigoS'] = StandbyCod
                else:
                    Aparatos_C.loc['Cava2', 'Standby'] = 0
                    Aparatos_C.loc['Cava2', 'CodigoS'] = ' '

                # Aparatos_C.loc['Cava', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby_c_i')[0])
                # Aparatos_C.loc['Cava', 'CodigoS'] =Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]

                if InfoDeco.filter(regex='regulador_c_i')[0] != 'ninguno':
                    Aparatos_C.loc['Regulador', 'Standby'] = consumoEq(
                        InfoDeco.filter(regex='regulador_consumo')[0])
                    if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
                        Aparatos_C.loc['Regulador', 'Marca'] = 'Cava ' + InfoDeco.filter(regex='regulador_marca')[0]
                    else:
                        Aparatos_C.loc['Regulador', 'Marca'] = 'Cava ' + \
                                                               InfoDeco.filter(regex='regulador_marca_otro')[0]

                    Aparatos_C.loc['Regulador', 'CodigoS'] = \
                    Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
                    Aparatos_C.loc['Regulador', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador', 'Notas'] = notass

            # if indx == 10:
            #     NomAparato = 'hielos2'
            #     InfoDeco = Circuito.filter(regex=NomAparato)
            #     Aparatos_C.loc['Hielos2', 'Existencia'] = 1
            #     alto = InfoDeco.filter(regex='alto')[0]
            #     ancho = InfoDeco.filter(regex='ancho')[0]
            #     profundo = InfoDeco.filter(regex='profundo')[0]
            #
            #     if InfoDeco.filter(regex='marca')[0] == 'otra':
            #         Aparatos_C.loc['Hielos2', 'Marca'] = InfoDeco.filter(regex='marca_otro')[0]
            #     else:
            #         Aparatos_C.loc['Hielos2', 'Marca'] = InfoDeco.filter(regex='marca')[0]
            #
            #     Aparatos_C.loc['Hielos2', 'Volumen'] = float(alto) * float(ancho) * float(profundo)
            #     Aparatos_C.loc['Hielos2', 'Temp Refri'] = temperatura(InfoDeco.filter(regex='hielos1_temp_c_i')[0])
            #     Aparatos_C.loc['Hielos2', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
            #     # Aparatos_C.loc['Cava', 'Pot Compresor'] = InfoDeco.filter(regex='compresor_potencia')[0]
            #     PotCompresor = InfoDeco.filter(regex='compresor_potencia')[0]
            #     Watt = consumoEq(PotCompresor)
            #     Aparatos_C.loc['Hielos2', 'Pot Compresor'] = Watt
            #     Aparatos_C.loc['Hielos2', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
            #     Aparatos_C.loc['Hielos2', 'Prob Comp'] = InfoDeco.filter(regex='compresor_problema')[0]
            #     Aparatos_C.loc['Hielos2', 'Prob Descr'] = InfoDeco.filter(regex='compresor_problema_descrp')[0]
            #     Aparatos_C.loc['Hielos2', 'Empaques'] = InfoDeco.filter(regex='empaques')[0]
            #     Aparatos_C.loc['Hielos2', 'Termostato'] = InfoDeco.filter(regex='termostato')[0]
            #     Aparatos_C.loc['Hielos2', 'Ventilacion'] = InfoDeco.filter(regex='ventilacion')[0]
            #     Aparatos_C.loc['Hielos2', 'Cierre'] = InfoDeco.filter(regex='cierre')[0]
            #     Aparatos_C.loc['Hielos2', 'Tipo'] = InfoDeco.filter(regex='tipo')[0]
            #     Aparatos_C.loc['Hielos2', 'Dispensador'] = InfoDeco.filter(regex='dispensador')[0]
            #     Aparatos_C.loc['Hielos2', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
            #     Aparatos_C.loc['Hielos2', 'Notas'] = notass
            #     Aparatos_C.loc['Hielos2', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby_c_i')[0])
            #     Aparatos_C.loc['Hielos2', 'CodigoS'] = StandbyCod
            #     Aparatos_C.loc['Hielos2', 'Clave'] = 'HL'
            #
            #     if InfoDeco.filter(regex='regulador_c_i')[0] != 'ninguno':
            #         Aparatos_C.loc['Regulador', 'Standby'] = consumoEq(
            #             InfoDeco.filter(regex='regulador_consumo')[0])
            #         if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
            #             Aparatos_C.loc['Regulador', 'Marca'] = 'Hielos ' + InfoDeco.filter(regex='regulador_marca')[
            #                 0]
            #         else:
            #             Aparatos_C.loc['Regulador', 'Marca'] = 'Hielos ' + \
            #                                                    InfoDeco.filter(regex='regulador_marca_otro')[0]
            #         # Aparatos_C.loc['Regulador', 'CodigoS'] = InfoDeco.filter(regex='regulador_consumo_codigofindero')[0]
            #         Aparatos_C.loc['Regulador', 'Existencia'] = 1
            #         Aparatos_C.loc['Regulador', 'Notas'] = notass

            if indx == 10:
                NomAparato = 'adicional'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Adicional', 'Existencia'] = 1
                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]
                Aparatos_C.loc['Adicional', 'Marca'] =   InfoDeco.filter(regex='nombre')[0]
                Aparatos_C.loc['Adicional', 'Volumen'] = float(alto) * float(ancho) * float(profundo)
                Aparatos_C.loc['Adicional', 'Temp Refri'] = InfoDeco.filter(regex='temp_c_i')[0]
                Aparatos_C.loc['Adicional', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
                #Aparatos_C.loc['Cava', 'Pot Compresor'] = InfoDeco.filter(regex='compresor_potencia')[0]
                PotCompresor = InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Adicional', 'Pot Compresor'] = Watt
                Aparatos_C.loc['Adicional', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                Aparatos_C.loc['Adicional', 'Prob Comp'] = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Adicional', 'Prob Descr'] = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Adicional', 'Empaques'] = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Adicional', 'Termostato'] = InfoDeco.filter(regex='termostato')[0]
                Aparatos_C.loc['Adicional', 'Ventilacion'] = InfoDeco.filter(regex='ventilacion')[0]
                Aparatos_C.loc['Adicional', 'Cierre'] = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Adicional', 'Notas'] = notass
                Aparatos_C.loc['Adicional', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby_c_i')[0])
                Aparatos_C.loc['Hielos2', 'Clave'] = 'RF'
                # Aparatos_C.loc['Adicional', 'CodigoS'] = InfoDeco.filter(regex='standby_codigofindero_c_i')[0]

                if not InfoDeco.filter(regex='adicional_regulador_c_i')[0] != 'ninguno':
                    Aparatos_C.loc['Regulador', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_consumo')[0])
                    if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
                        Aparatos_C.loc['Regulador', 'Marca'] = 'Adicional ' + InfoDeco.filter(regex='regulador_marca')[0]
                    else:
                        Aparatos_C.loc['Regulador', 'Marca'] = 'Adicional' + InfoDeco.filter(regex='regulador_otra')[0]
                    Aparatos_C.loc['Regulador', 'CodigoS'] = InfoDeco.filter(regex='regulador_consumo_codigofindero')[0]
                    Aparatos_C.loc['Regulador', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador', 'Notas'] = notass

        indx+=1


    Aparatos_C.loc['Refrigerador', 'Notas'] = Circuito.filter(regex='refrigeracion_notas_c_i')[0]
    Info_R.loc['Refrigeracion', 'Notas'] = Circuito.filter(regex='refrigeracion_notas_c_i')[0]
    Info_R.loc['Refrigeracion', 'Voz']   = Circuito.filter(regex='refrigeracion_notas_c_i')[0]
    TotalCons=0

    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()

    Codigos=ClavesRefri(Aparatos)
    print("Refrigeradores.py Codigos",Codigos)
    Aparatos['Claves']=Codigos

    return Aparatos,TotalCons, Codigos