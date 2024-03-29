import pandas as pd
from Condiciones import condicionesRefrigeracion
from LibreriaRefris import ClavesRefri
from Consumo import consumoEq
import math
from libreriaReguladores_ import Atac_Mec

def refrigerador(Excel,Nocircuito,NomCircuito,voltaje):

    Aparatos_C = pd.DataFrame(index=['Refrigerador','Congelador','Minibar','Cava','Hielos','Refrigerador2',
                                     'Congelador2','Minibar2','Cava2','Hielos2','Adicional','Regulador Minibar','Regulador','Regulador2',
                                     'Regulador Refrigerador','Regulador Congelador','Regulador Cava','Regulador Hielos','Refrigeracion','Problemas']
                              ,columns=['Marca','Volumen','Temp Refri','Temp Conge','Pot Compresor','Temp Compresor','Nominal',
                                        'Prob Comp','Prob Descr','Empaques','Termostato','Ventilacion','Cierre', 'Existencia',
                                        'Standby','CodigoN','Notas','Claves','Zona','Prob Refr','Tuberias','Jabon','Alarma','Tipo','Clave'])

    Regulador = pd.DataFrame(index=['Regulador'],columns=['Marca','Standby','Existencia'])
    Info_R    = pd.DataFrame(index=['Refrigeracion'], columns=['Notas','CodigoS','Standby'])
    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("equipos_refrigeracion", case=False)]

    Equipos= Circuito[InfoEquipos]
    indx=0
    StandbyCod =Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
    notass=Circuito.filter(regex='refrigeracion_notas_c_i')[0]
    Tierra = Circuito.filter(regex='tierra_c_i')[0]

    for i in Equipos:
        if i == 1:

            if indx == 1:
                NomAparato = 'refrigerador1'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Refrigerador', 'Existencia'] = 1
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
                try   : Aparatos_C.loc['Refrigerador', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                except: Aparatos_C.loc['Refrigerador', 'Temp Compresor'] =10
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
                Aparatos_C.loc['Refrigerador', 'Encendido'] = InfoDeco.filter(regex='encendido')[0]
                Aparatos_C.loc['Refrigerador', 'Dispensador']      = InfoDeco.filter(regex='dispensador')[0]
                Aparatos_C.loc['Refrigerador', 'Atacable'] = 'No'

                if InfoDeco.filter(regex='espendiente_c_i')[0]=='si':
                    Aparatos_C.loc['Refrigerador', 'CodigoN']     = InfoDeco.filter(regex='codigofindero')[0]
                else:
                    Aparatos_C.loc['Refrigerador', 'CodigoN']     = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]

                if not pd.isna(InfoDeco.filter(regex='standby_c_i')[0]) :
                    Aparatos_C.loc['Refrigerador', 'Standby'] = consumoEq( InfoDeco.filter(regex='standby_c_i')[0])
                    Aparatos_C.loc['Refrigerador', 'CodigoS'] = StandbyCod
                else:
                    Aparatos_C.loc['Refrigerador', 'Standby'] = 0
                    Aparatos_C.loc['Refrigerador', 'CodigoS'] = ' '

                Aparatos_C.loc['Refrigerador', 'Notas'] = Circuito.filter(regex='refrigeracion_notas_c_i')[0]
                Aparatos_C.loc['Refrigerador', 'Clave'] = 'RF'+ClavesRefri(Aparatos_C.loc['Refrigerador'])


                ##################
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
                    Aparatos_C.loc['Regulador Refrigerador', 'Max_Potencia'] = PotCompresor
                    Aparatos_C.loc['Regulador Refrigerador', 'Atacable'] = Atac_Mec(voltaje, Aparatos_C.loc['Regulador Refrigerador', 'Standby'],
                                                                                Aparatos_C.loc['Regulador Refrigerador', 'Max_Potencia'])
                    Aparatos_C.loc['Regulador Refrigerador', 'Clave'] = 'RG,Regulador Refrigerador,MC'+','+str(consumoEq(Aparatos_C.loc['Regulador Refrigerador', 'Max_Potencia']))
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
                except: Aparatos_C.loc['Congelador', 'Temp Conge'] = 50
                #Aparatos_C.loc['Congelador', 'Temp Refr'] = 50
                PotCompresor = InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Congelador', 'Pot Compresor'] = Watt
                try:   Aparatos_C.loc['Congelador', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                except:Aparatos_C.loc['Congelador', 'Temp Compresor'] = 10
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
                Aparatos_C.loc['Congelador', 'Atacable'] = 'No'

                if InfoDeco.filter(regex='espendiente_c_i')[0]=='si':
                    Aparatos_C.loc['Congelador', 'CodigoN']     = InfoDeco.filter(regex='codigofindero')[0]
                else:
                    Aparatos_C.loc['Congelador', 'CodigoN']     = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]

                Aparatos_C.loc['Congelador', 'Notas']       = notass
                if not pd.isna(InfoDeco.filter(regex='standby_c_i')[0]) :
                    Aparatos_C.loc['Congelador', 'Standby'] = consumoEq( InfoDeco.filter(regex='standby_c_i')[0])
                    Aparatos_C.loc['Congelador', 'CodigoS'] = StandbyCod
                else:
                    Aparatos_C.loc['Congelador', 'Standby'] = 0
                    Aparatos_C.loc['Congelador', 'CodigoS'] = ' '
                Aparatos_C.loc['Congelador', 'Clave'] = 'CN'+ClavesRefri(Aparatos_C.loc['Congelador'])

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
                    #Aparatos_C.loc['Regulador Congelador', 'Clave'] = 'RG,Regulador Congelador,MC'
                    Aparatos_C.loc['Regulador Congelador', 'Max_Potencia'] = PotCompresor
                    Aparatos_C.loc['Regulador Congelador', 'Atacable'] = Atac_Mec(voltaje, Aparatos_C.loc[ 'Regulador Congelador', 'Standby'],
                                                                                    Aparatos_C.loc['Regulador Congelador', 'Max_Potencia'])
                    Aparatos_C.loc['Regulador Congelador', 'Clave'] = 'RG,Regulador Congelador,MC' + ',' + str(consumoEq(Aparatos_C.loc['Regulador Congelador', 'Max_Potencia']))
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

                try   : Aparatos_C.loc['Minibar', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                except: Aparatos_C.loc['Minibar', 'Temp Compresor'] = 10
                Aparatos_C.loc['Minibar', 'Prob Refr'] = InfoDeco.filter(regex='problemas_c_i')[0]
                Aparatos_C.loc['Minibar', 'Prob Comp']      = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Minibar', 'Prob Descr']     = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Minibar', 'Empaques']       = InfoDeco.filter(regex='empaques')[0]
                #Aparatos_C.loc['Minibar', 'Termostato']     = InfoDeco.filter(regex='termostato')[0]
                Aparatos_C.loc['Minibar', 'Encerrado'] = InfoDeco.filter(regex='encerrado_c_i')[0]
                Aparatos_C.loc['Minibar', 'Ventilas'] = InfoDeco.filter(regex='ventilas_c_i')[0]
                Aparatos_C.loc['Minibar', 'Difusor'] = InfoDeco.filter(regex='ventilador_c_i')[0]
                Aparatos_C.loc['Minibar', 'Atacable'] = 'No'

                Aparatos_C.loc['Minibar', 'Alarma'] = InfoDeco.filter(regex='alarma')[0]
                #Aparatos_C.loc['Minibar', 'Tipo']    = InfoDeco.filter(regex='Tipo')[0]
                Aparatos_C.loc['Minibar', 'Cierre']         = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Minibar', 'Tipo']           = InfoDeco.filter(regex='tipo')[0]
                Aparatos_C.loc['Minibar', 'Dispensador']    = InfoDeco.filter(regex='dispensador')[0]
                Aparatos_C.loc['Minibar', 'Tuberias'] = InfoDeco.filter(regex='tuberias')[0]
                Aparatos_C.loc['Minibar', 'Jabon'] = InfoDeco.filter(regex='jabon')[0]
                Aparatos_C.loc['Minibar', 'Standby'] = 0
                Aparatos_C.loc['Minibar', 'CodigoS'] = 0
                Aparatos_C.loc['Minibar', 'Clave'] = 'MB'+ClavesRefri(Aparatos_C.loc['Minibar'])

                if InfoDeco.filter(regex='espendiente_c_i')[0]=='si':
                    Aparatos_C.loc['Minibar', 'CodigoN']     = InfoDeco.filter(regex='codigofindero')[0]
                else:
                    Aparatos_C.loc['Minibar', 'CodigoN']     = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]


                if InfoDeco.filter(regex='regulador_c_i')[0] != 'ninguno':
                    Aparatos_C.loc['Regulador Minibar', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_consumo')[0])
                    # if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
                    #     Aparatos_C.loc['Regulador Minibar', 'Marca'] = 'Minibar ' + InfoDeco.filter(regex='regulador_marca')[0]
                    # else:
                    #     Aparatos_C.loc['Regulador Minibar', 'Marca'] = 'Minibar ' + InfoDeco.filter(regex='regulador_marca_otro')[0]
                    Aparatos_C.loc['Regulador Minibar', 'CodigoS'] = StandbyCod
                    Aparatos_C.loc['Regulador Minibar', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador Minibar', 'Notas'] = notass
                    #Aparatos_C.loc['Regulador Minibar', 'Clave'] = 'RG,Regulador Minibar,MC'
                    Aparatos_C.loc['Regulador Minibar', 'Zona'] = Aparatos_C.loc['Minibar', 'Zona']
                    Aparatos_C.loc['Regulador Minibar', 'Max_Potencia'] = PotCompresor
                    Aparatos_C.loc['Regulador Minibar', 'Atacable'] = Atac_Mec(voltaje, Aparatos_C.loc['Regulador Minibar', 'Standby'],
                                                                                    Aparatos_C.loc[ 'Regulador Minibar', 'Max_Potencia'])
                    Aparatos_C.loc['Regulador Minibar', 'Clave'] = 'RG,Regulador Minibar,MC' + ',' + \
                                                                        str(consumoEq(Aparatos_C.loc['Regulador Minibar', 'Max_Potencia']))


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
                except:Aparatos_C.loc['Cava', 'Temp Compresor'] = 10
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
                Aparatos_C.loc['Cava', 'Atacable'] = 'No'

                if InfoDeco.filter(regex='espendiente_c_i')[0]=='si':
                    Aparatos_C.loc['Cava', 'CodigoN']     = InfoDeco.filter(regex='codigofindero')[0]
                else:
                    Aparatos_C.loc['Cava', 'CodigoN']     = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]
                Aparatos_C.loc['Cava', 'Notas'] = notass

                if not pd.isna(InfoDeco.filter(regex='standby_c_i')[0]) :
                    Aparatos_C.loc['Cava', 'Standby'] = consumoEq( InfoDeco.filter(regex='standby_c_i')[0])
                    Aparatos_C.loc['Cava', 'CodigoS'] = StandbyCod
                else:
                    Aparatos_C.loc['Cava', 'Standby'] = 0
                    Aparatos_C.loc['Cava', 'CodigoS'] = ' '
                Aparatos_C.loc['Cava', 'Clave'] = 'CV'+ClavesRefri(Aparatos_C.loc['Cava'])

                if InfoDeco.filter(regex='regulador_c_i')[0] == 'regulador':
                    Aparatos_C.loc['Regulador Cava', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_consumo')[0])
                    # if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
                    #     Aparatos_C.loc['Regulador Cava', 'Marca'] = 'Cava ' + InfoDeco.filter(regex='regulador_marca')[0]
                    # else:
                    #     Aparatos_C.loc['Regulador Cava', 'Marca'] = 'Cava ' + \
                    #                                            InfoDeco.filter(regex='regulador_marca_otro')[0]
                    Aparatos_C.loc['Regulador Cava', 'CodigoS'] = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
                    Aparatos_C.loc['Regulador Cava', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador Cava', 'Notas'] = notass
                    #Aparatos_C.loc['Regulador Cava', 'Clave'] = 'RG,Regulador Cava,MC'
                    Aparatos_C.loc['Regulador Cava', 'Zona'] = Aparatos_C.loc['Cava', 'Zona']
                    Aparatos_C.loc['Regulador Cava', 'Max_Potencia'] = PotCompresor
                    Aparatos_C.loc['Regulador Cava', 'Atacable'] = Atac_Mec(voltaje, Aparatos_C.loc[
                        'Regulador Cava', 'Standby'],
                                                                               Aparatos_C.loc[
                                                                                   'Regulador Cava', 'Max_Potencia'])
                    Aparatos_C.loc['Regulador Cava', 'Clave'] = 'RG,Regulador Cava,MC' + ',' + str(consumoEq(Aparatos_C.loc[
                        'Regulador Cava', 'Max_Potencia']))



            if indx == 5:
                NomAparato = 'hielos1'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Maquina de Hielos', 'Existencia'] = 1
                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]
                if InfoDeco.filter(regex='marca_c_i')[0] == 'otro':
                    Aparatos_C.loc['Maquina de Hielos', 'Marca'] = InfoDeco.filter(regex='marca_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Maquina de Hielos', 'Marca'] = InfoDeco.filter(regex='marca_c_i')[0]

                if InfoDeco.filter(regex='zona_c_i')[0] == 'otro':
                    Aparatos_C.loc['Maquina de Hielos', 'Zona'] = InfoDeco.filter(regex='zona_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Maquina de Hielos', 'Zona'] = InfoDeco.filter(regex='zona_c_i')[0]
                Aparatos_C.loc['Maquina de Hielos', 'Volumen'] = float(alto) * float(ancho) * float(profundo)
                try:   Aparatos_C.loc['Maquina de Hielos', 'Temp Refri'] = InfoDeco.filter(regex='temp_c_i')[0]
                except:Aparatos_C.loc['Maquina de Hielos', 'Temp Refri'] = 100
                Aparatos_C.loc['Maquina de Hielos', 'Temp Conge'] = 100
                Aparatos_C.loc['Maquina de Hielos', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
                #Aparatos_C.loc['Cava', 'Pot Compresor'] = InfoDeco.filter(regex='compresor_potencia')[0]
                PotCompresor = InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Maquina de Hielos', 'Pot Compresor'] = Watt
                try:   Aparatos_C.loc['Maquina de Hielos', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                except:Aparatos_C.loc['Maquina de Hielos', 'Temp Compresor'] = 100
                Aparatos_C.loc['Maquina de Hielos', 'Difusor']   = InfoDeco.filter(regex='ventilador_c_i')[0]
                Aparatos_C.loc['Maquina de Hielos', 'Tuberias']  = InfoDeco.filter(regex='tuberias')[0]
                Aparatos_C.loc['Maquina de Hielos', 'Prob Refr'] = InfoDeco.filter(regex='problemas_c_i')[0]
                Aparatos_C.loc['Maquina de Hielos', 'Encerrado'] = InfoDeco.filter(regex='encerrado_c_i')[0]
                Aparatos_C.loc['Maquina de Hielos', 'Ventilas']  = InfoDeco.filter(regex='ventilas_c_i')[0]
                Aparatos_C.loc['Maquina de Hielos', 'Alarma']    = InfoDeco.filter(regex='alarma')[0]
                Aparatos_C.loc['Maquina de Hielos', 'Prob Comp']      = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Maquina de Hielos', 'Prob Descr']     = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Maquina de Hielos', 'Empaques']       = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Maquina de Hielos', 'Termostato']     = InfoDeco.filter(regex='termostato')[0]
                #Aparatos_C.loc['Cava', 'Ventilacion']    = InfoDeco.filter(regex='ventilacion')[0]
                Aparatos_C.loc['Maquina de Hielos', 'Cierre']         = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Maquina de Hielos', 'Tipo']           = InfoDeco.filter(regex='tipo')[0]
                #Aparatos_C.loc['Cava', 'Dispensador']    = InfoDeco.filter(regex='dispensador')[0]
                try:   Aparatos_C.loc['Maquina de Hielos', 'Encendido'] = InfoDeco.filter(regex="encendido_c_i")[0]
                except:Aparatos_C.loc['Maquina de Hielos', 'Encendido'] = 60
                Aparatos_C.loc['Maquina de Hielos', 'Atacable'] = 'Si'

                if InfoDeco.filter(regex='espendiente_c_i')[0]=='si':
                    Aparatos_C.loc['Maquina de Hielos', 'CodigoN']     = InfoDeco.filter(regex='codigofindero')[0]
                else:
                    Aparatos_C.loc['Maquina de Hielos', 'CodigoN']     = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]
                Aparatos_C.loc['Maquina de Hielos', 'Notas'] = notass

                if not pd.isna(InfoDeco.filter(regex='standby_c_i')[0]) :
                    Aparatos_C.loc['Maquina de Hielos', 'Standby'] = consumoEq( InfoDeco.filter(regex='standby_c_i')[0])
                    Aparatos_C.loc['Maquina de Hielos', 'CodigoS'] = StandbyCod
                else:
                    Aparatos_C.loc['Maquina de Hielos', 'Standby'] = 0
                    Aparatos_C.loc['Maquina de Hielos', 'CodigoS'] = ' '
                Aparatos_C.loc['Maquina de Hielos', 'Clave'] = 'HL'

                if InfoDeco.filter(regex='regulador_c_i')[0] == 'regulador':
                    Aparatos_C.loc['Regulador Maquina de Hielos', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_consumo')[0])
                    if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
                        Aparatos_C.loc['Regulador Maquina de Hielos', 'Marca'] = 'Cava ' + InfoDeco.filter(regex='regulador_marca')[0]
                    else:
                        Aparatos_C.loc['Regulador Maquina de Hielos', 'Marca'] = 'Cava ' + \
                                                                    InfoDeco.filter(regex='regulador_marca_otro')[0]
                    Aparatos_C.loc['Regulador Maquina de Hielos', 'CodigoS'] = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
                    Aparatos_C.loc['Regulador Maquina de Hielos', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador Maquina de Hielos', 'Notas'] = notass
                    #Aparatos_C.loc['Regulador Maquina de Hielos', 'Clave'] = 'RG,Regulador Hielos,MC'
                    Aparatos_C.loc['Regulador Maquina de Hielos', 'Zona'] = Aparatos_C.loc['Maquina de Hielos', 'Zona']
                    Aparatos_C.loc['Regulador Maquina de Hielos', 'Max_Potencia'] = PotCompresor
                    Aparatos_C.loc['Regulador Maquina de Hielos', 'Atacable'] = Atac_Mec(voltaje, Aparatos_C.loc[
                        'Regulador Maquina de Hielos', 'Standby'],
                                                                               Aparatos_C.loc[
                                                                                   'Regulador Maquina de Hielos', 'Max_Potencia'])
                    Aparatos_C.loc['Regulador Maquina de Hielos', 'Clave'] = 'RG,Regulador Maquina de Hielos,MC' + ',' +str(consumoEq(Aparatos_C.loc[
                        'Regulador Maquina de Hielos', 'Max_Potencia']))


            if indx == 6:

                NomAparato = 'refrigerador2'
                InfoDeco = Circuito.filter(regex=NomAparato)

                Aparatos_C.loc['Refrigerador2', 'Existencia'] = 1
                #Aparatos_C.loc['Regulador', 'Existencia'] = 1

                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]
                try:   Aparatos_C.loc['Refrigerador2', 'Encendido'] = InfoDeco.filter(regex="encendido_c_i")[0]
                except:Aparatos_C.loc['Refrigerador2', 'Encendido'] = 60
                if InfoDeco.filter(regex='zona_c_i')[0] == 'otro':
                    Aparatos_C.loc['Refrigerador2', 'Zona'] = InfoDeco.filter(regex='zona_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Refrigerador2', 'Zona'] = InfoDeco.filter(regex='zona_c_i')[0]

                if InfoDeco.filter(regex='marca')[0] =='otro':
                    Aparatos_C.loc['Refrigerador2', 'Marca'] = InfoDeco.filter(regex='marca_otro')[0]
                else:
                    Aparatos_C.loc['Refrigerador2', 'Marca'] = InfoDeco.filter(regex='marca')[0]

                Aparatos_C.loc['Refrigerador2', 'Volumen'] = (float(alto) * float(ancho) * float(profundo))
                try:   Aparatos_C.loc['Refrigerador2', 'Temp Refri'] = InfoDeco.filter(regex='trefri')[0]
                except:Aparatos_C.loc['Refrigerador2', 'Temp Refri'] = 100
                try:   Aparatos_C.loc['Refrigerador2', 'Temp Conge'] = InfoDeco.filter(regex='tconge')[0]
                except:Aparatos_C.loc['Refrigerador2', 'Temp Conge'] = 100

                PotCompresor=InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Refrigerador2', 'Pot Compresor'] =Watt
                try   : Aparatos_C.loc['Refrigerador2', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                except: Aparatos_C.loc['Refrigerador2', 'Temp Compresor'] =10
                Aparatos_C.loc['Refrigerador2', 'Prob Refr']   = InfoDeco.filter(regex='problemas_c_i')[0]

                Aparatos_C.loc['Refrigerador2', 'Prob Comp']   = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Refrigerador2', 'Prob Descr']  = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Refrigerador2', 'Empaques']    = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Refrigerador2', 'Difusor'] = InfoDeco.filter(regex='ventilador_c_i')[0]
                #Aparatos_C.loc['Refrigerador', 'Termostato']  = InfoDeco.filter(regex='termostato')[0]
                Aparatos_C.loc['Refrigerador2', 'Encerrado'] = InfoDeco.filter(regex='encerrado_c_i')[0]
                Aparatos_C.loc['Refrigerador2', 'Ventilas'] = InfoDeco.filter(regex='ventilas_c_i')[0]
                Aparatos_C.loc['Refrigerador2', 'Cierre']      = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Refrigerador2', 'Dispensador'] = InfoDeco.filter(regex='dispensador')[0]
                Aparatos_C.loc['Refrigerador2', 'Tuberias']    = InfoDeco.filter(regex='tuberias')[0]
                Aparatos_C.loc['Refrigerador2', 'Jabon']       = InfoDeco.filter(regex='jabon')[0]
                Aparatos_C.loc['Refrigerador2', 'Alarma']      = InfoDeco.filter(regex='alarma')[0]
                Aparatos_C.loc['Refrigerador2', 'Tipo']      = InfoDeco.filter(regex='tipo')[0]
                Aparatos_C.loc['Refrigerador2', 'Dispensador']      = InfoDeco.filter(regex='dispensador')[0]
                Aparatos_C.loc['Refrigerador2', 'Atacable'] = 'No'

                if InfoDeco.filter(regex='espendiente_c_i')[0]=='si':
                    Aparatos_C.loc['Refrigerador2', 'CodigoN']     = InfoDeco.filter(regex='codigofindero')[0]
                else:
                    Aparatos_C.loc['Refrigerador2', 'CodigoN']     = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]

                if not pd.isna(InfoDeco.filter(regex='standby_c_i')[0]) :
                    Aparatos_C.loc['Refrigerador2', 'Standby'] = consumoEq( InfoDeco.filter(regex='standby_c_i')[0])
                    Aparatos_C.loc['Refrigerador2', 'CodigoS'] = StandbyCod
                else:
                    Aparatos_C.loc['Refrigerador2', 'Standby'] = 0
                    Aparatos_C.loc['Refrigerador2', 'CodigoS'] = ' '

                Aparatos_C.loc['Refrigerador2', 'Notas'] = Circuito.filter(regex='refrigeracion_notas_c_i')[0]
                Aparatos_C.loc['Refrigerador2', 'Clave'] = 'RF'+ClavesRefri(Aparatos_C.loc['Refrigerador2'])


                ##################
                if InfoDeco.filter(regex='regulador_c_i')[0] =='regulador':
                    if InfoDeco.filter(regex='regulador_marca_c_i')[0] =='otro':
                        Aparatos_C.loc['Regulador Refrigerador2', 'Marca'] =   InfoDeco.filter(regex='regulador_otro')[0]
                    else:
                        Aparatos_C.loc['Regulador Refrigerador2', 'Marca'] =   InfoDeco.filter(regex='regulador_marca')[0]
                    Aparatos_C.loc['Regulador Refrigerador2', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_consumo')[0])
                    Aparatos_C.loc['Regulador Refrigerador2', 'CodigoS'] = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
                    Aparatos_C.loc['Regulador Refrigerador2', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador Refrigerador2', 'Notas'] = notass
                    Aparatos_C.loc['Regulador Refrigerador2', 'Zona'] = Aparatos_C.loc['Refrigerador2', 'Zona']
                    #Aparatos_C.loc['Regulador Refrigerador2', 'Clave'] = 'RG,Regulador Refrigerador2,MC'
                    Aparatos_C.loc['Regulador Refrigerador2', 'Max_Potencia'] = PotCompresor
                    Aparatos_C.loc['Regulador Refrigerador2', 'Atacable'] = Atac_Mec(voltaje, Aparatos_C.loc[
                        'Regulador Refrigerador2', 'Standby'],Aparatos_C.loc['Regulador Refrigerador2', 'Max_Potencia'])
                    Aparatos_C.loc['Regulador Refrigerador2', 'Clave'] = 'RG,Regulador Refrigerador2,MC' + ',' + str(consumoEq(Aparatos_C.loc[
                        'Regulador Refrigerador2', 'Max_Potencia']))

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
                try:    Aparatos_C.loc['Congelador2', 'Temp Conge'] = InfoDeco.filter(regex='congelador1_temp')[0]
                except: Aparatos_C.loc['Congelador2', 'Temp Conge'] = 100
                Aparatos_C.loc['Congelador2', 'Temp Refr'] = 100
                PotCompresor = InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Congelador2', 'Pot Compresor'] = Watt

                try:   Aparatos_C.loc['Congelador2', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                except:Aparatos_C.loc['Congelador2', 'Temp Compresor'] = 10
                try:   Aparatos_C.loc['Congelador2', 'Encendido'] = InfoDeco.filter(regex="encendido_c_i")[0]
                except:Aparatos_C.loc['Congelador2', 'Encendido'] = 60

                Aparatos_C.loc['Congelador2', 'Prob Comp']   = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Congelador2', 'Prob Descr']  = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Congelador2', 'Empaques']    = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Congelador2', 'Termostato']  = InfoDeco.filter(regex='termostato')[0]
                #Aparatos_C.loc['Congelador', 'Ventilacion'] = InfoDeco.filter(regex='ventilacion')[0]
                Aparatos_C.loc['Congelador2','Disposicion']  =InfoDeco.filter(regex='disposicion')[0]
                Aparatos_C.loc['Congelador2', 'Cierre']      = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Congelador2', 'Tipo']        = InfoDeco.filter(regex='tipo')[0]
                Aparatos_C.loc['Congelador2', 'Dispensador'] = InfoDeco.filter(regex='dispensador')[0]
                Aparatos_C.loc['Congelador2', 'Alarma']      = InfoDeco.filter(regex='alarma')[0]
                Aparatos_C.loc['Congelador2', 'Ventilas'] = InfoDeco.filter(regex='ventilas_c_i')[0]
                Aparatos_C.loc['Congelador2', 'Encerrado'] = InfoDeco.filter(regex='encerrado_c_i')[0]
                Aparatos_C.loc['Congelador2', 'Prob Refr']   = InfoDeco.filter(regex='problemas_c_i')[0]
                Aparatos_C.loc['Congelador2', 'Difusor'] = InfoDeco.filter(regex='ventilador_c_i')[0]
                Aparatos_C.loc['Congelador2', 'Tuberias']    = InfoDeco.filter(regex='tuberias')[0]
                Aparatos_C.loc['Congelador2', 'Atacable'] = 'No'

                if InfoDeco.filter(regex='espendiente_c_i')[0]=='si':
                    Aparatos_C.loc['Congelador2', 'CodigoN']     = InfoDeco.filter(regex='codigofindero')[0]
                else:
                    Aparatos_C.loc['Congelador2', 'CodigoN']     = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]

                Aparatos_C.loc['Congelador2', 'Notas']       = notass
                if not pd.isna(InfoDeco.filter(regex='standby_c_i')[0]) :
                    Aparatos_C.loc['Congelador2', 'Standby'] = consumoEq( InfoDeco.filter(regex='standby_c_i')[0])
                    Aparatos_C.loc['Congelador2', 'CodigoS'] = StandbyCod
                else:
                    Aparatos_C.loc['Congelador2', 'Standby'] = 0
                    Aparatos_C.loc['Congelador2', 'CodigoS'] = ' '
                Aparatos_C.loc['Congelador2', 'Clave'] = 'CN'+ClavesRefri(Aparatos_C.loc['Congelador'])

                if InfoDeco.filter(regex='regulador_c_i')[0] != 'ninguno':
                    Aparatos_C.loc['Regulador Congelador2', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_consumo')[0])
                    if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
                        Aparatos_C.loc['Regulador Congelador2', 'Marca'] =  InfoDeco.filter(regex='regulador_marca')[0]
                    else:
                        Aparatos_C.loc['Regulador Congelador2', 'Marca'] =  InfoDeco.filter(regex='regulador_marca')[0]
                    Aparatos_C.loc['Regulador Congelador2', 'CodigoS'] = StandbyCod
                    Aparatos_C.loc['Regulador Congelador2', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador Congelador2', 'Notas'] = notass
                    Aparatos_C.loc['Regulador Congelador2', 'Clave'] = 'RG,Regulador Congelador2,MC'
                    Aparatos_C.loc['Regulador Congelador2', 'Zona'] = Aparatos_C.loc['Congelador2', 'Zona']
                    Aparatos_C.loc['Regulador Congelador2', 'Max_Potencia'] = PotCompresor
                    Aparatos_C.loc['Regulador Congelador2', 'Atacable'] = Atac_Mec(voltaje, Aparatos_C.loc[
                        'Regulador Congelador2', 'Standby'],
                                                                                    Aparatos_C.loc[
                                                                                        'Regulador Congelador2', 'Max_Potencia'])
                    Aparatos_C.loc['Regulador Congelador2', 'Clave'] = 'RG,Regulador Congelador2,MC' + ',' + \
                                                                         str(consumoEq(Aparatos_C.loc[ 'Regulador Congelador2', 'Max_Potencia']))


            if indx == 8:
                NomAparato = 'minibar2'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Minibar2', 'Existencia'] = 1
                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]
                Aparatos_C.loc['Minibar2', 'Volumen'] = float(alto) * float(ancho) * float(profundo)


                try:
                    Aparatos_C.loc['Minibar2', 'Encendido'] = InfoDeco.filter(regex="encendido_c_i")[0]
                except:
                    Aparatos_C.loc['Minibar2', 'Encendido'] = 60
                if InfoDeco.filter(regex='marca_c_i')[0] == 'otro':
                    Aparatos_C.loc['Minibar2', 'Marca'] = InfoDeco.filter(regex='marca_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Minibar2', 'Marca'] = InfoDeco.filter(regex='marca_c_i')[0]

                if InfoDeco.filter(regex='zona_c_i')[0] == 'otro':
                    Aparatos_C.loc['Minibar2', 'Zona'] = InfoDeco.filter(regex='zona_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Minibar2', 'Zona'] = InfoDeco.filter(regex='zona_c_i')[0]

                Aparatos_C.loc['Minibar2', 'Volumen'] = float(alto) * float(ancho) * float(profundo)
                try:
                    Aparatos_C.loc['Minibar2', 'Temp Refri'] = InfoDeco.filter(regex='minibar1_temp_c_i')[0]
                except:
                    Aparatos_C.loc['Minibar2', 'Temp Refri'] = 100
                try:
                    Aparatos_C.loc['Minibar2', 'Temp Conge'] = InfoDeco.filter(regex='tconge')[0]
                except:
                    Aparatos_C.loc['Minibar2', 'Temp Conge'] = 100
                # Aparatos_C.loc['Minibar', 'Pot Compresor'] = InfoDeco.filter(regex='compresor_potencia')[0]
                Aparatos_C.loc['Minibar2', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
                PotCompresor = InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Minibar2', 'Pot Compresor'] = Watt
                Aparatos_C.loc['Minibar2', 'Notas'] = notass

                try:
                    Aparatos_C.loc['Minibar2', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                except:
                    Aparatos_C.loc['Minibar2', 'Temp Compresor'] = 10
                Aparatos_C.loc['Minibar2', 'Prob Refr'] = InfoDeco.filter(regex='problemas_c_i')[0]
                Aparatos_C.loc['Minibar2', 'Prob Comp'] = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Minibar2', 'Prob Descr'] = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Minibar2', 'Empaques'] = InfoDeco.filter(regex='empaques')[0]
                # Aparatos_C.loc['Minibar', 'Termostato']     = InfoDeco.filter(regex='termostato')[0]
                Aparatos_C.loc['Minibar2', 'Encerrado'] = InfoDeco.filter(regex='encerrado_c_i')[0]
                Aparatos_C.loc['Minibar2', 'Ventilas'] = InfoDeco.filter(regex='ventilas_c_i')[0]
                Aparatos_C.loc['Minibar2', 'Difusor'] = InfoDeco.filter(regex='ventilador_c_i')[0]
                Aparatos_C.loc['Minibar2', 'Atacable'] = 'No'

                Aparatos_C.loc['Minibar2', 'Alarma'] = InfoDeco.filter(regex='alarma')[0]
                # Aparatos_C.loc['Minibar', 'Tipo']    = InfoDeco.filter(regex='Tipo')[0]
                Aparatos_C.loc['Minibar2', 'Cierre'] = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Minibar2', 'Tipo'] = InfoDeco.filter(regex='tipo')[0]
                Aparatos_C.loc['Minibar2', 'Dispensador'] = InfoDeco.filter(regex='dispensador')[0]
                Aparatos_C.loc['Minibar2', 'Tuberias'] = InfoDeco.filter(regex='tuberias')[0]
                Aparatos_C.loc['Minibar2', 'Jabon'] = InfoDeco.filter(regex='jabon')[0]
                Aparatos_C.loc['Minibar2', 'Standby'] = 0
                Aparatos_C.loc['Minibar2', 'CodigoS'] = 0
                Aparatos_C.loc['Minibar2', 'Clave'] = 'MB' + ClavesRefri(Aparatos_C.loc['Minibar2'])

                if InfoDeco.filter(regex='espendiente_c_i')[0] == 'si':
                    Aparatos_C.loc['Minibar2', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
                else:
                    Aparatos_C.loc['Minibar2', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]

                if InfoDeco.filter(regex='regulador_c_i')[0] != 'ninguno':
                    Aparatos_C.loc['Regulador Minibar2', 'Standby'] = consumoEq(
                        InfoDeco.filter(regex='regulador_consumo')[0])
                    # if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
                    #     Aparatos_C.loc['Regulador Minibar2', 'Marca'] = 'Minibar ' + \
                    #                                                    InfoDeco.filter(regex='regulador_marca')[0]
                    # else:
                    #     Aparatos_C.loc['Regulador Minibar2', 'Marca'] = 'Minibar ' + \
                    #                                                    InfoDeco.filter(regex='regulador_marca_otro')[0]
                    Aparatos_C.loc['Regulador Minibar2', 'CodigoS'] = StandbyCod
                    Aparatos_C.loc['Regulador Minibar2', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador Minibar2', 'Notas'] = notass
                    # Aparatos_C.loc['Regulador Minibar2', 'Clave'] = 'RG,Regulador Minibar,MC'
                    Aparatos_C.loc['Regulador Minibar2', 'Zona'] = Aparatos_C.loc['Minibar', 'Zona']
                    Aparatos_C.loc['Regulador Minibar2', 'Max_Potencia'] = PotCompresor
                    Aparatos_C.loc['Regulador Minibar2', 'Atacable'] = Atac_Mec(voltaje, Aparatos_C.loc[
                        'Regulador Minibar2', 'Standby'],
                                                                               Aparatos_C.loc[
                                                                                   'Regulador Minibar2', 'Max_Potencia'])
                    Aparatos_C.loc['Regulador Minibar2', 'Clave'] = 'RG,Regulador Minibar2,MC' + ',' + \
                                                                   str(consumoEq(Aparatos_C.loc[
                                                                                     'Regulador Minibar2', 'Max_Potencia']))

            if indx == 9:
                NomAparato = 'cava2'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Cava2', 'Existencia'] = 1
                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]
                Aparatos_C.loc['Cava2', 'Volumen'] = float(alto) * float(ancho) * float(profundo)
                print(Aparatos_C.loc['Cava2', 'Volumen'])
                if InfoDeco.filter(regex='marca_c_i')[0] == 'otro':
                    Aparatos_C.loc['Cava2', 'Marca'] = InfoDeco.filter(regex='marca_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Cava2', 'Marca'] = InfoDeco.filter(regex='marca_c_i')[0]

                if InfoDeco.filter(regex='zona_c_i')[0] == 'otro':
                    Aparatos_C.loc['Cava2', 'Zona'] = InfoDeco.filter(regex='zona_otro_c_i')[0]
                else:
                    Aparatos_C.loc['Cava2', 'Zona'] = InfoDeco.filter(regex='zona_c_i')[0]
                try:
                    Aparatos_C.loc['Cava2', 'Temp Refri'] = InfoDeco.filter(regex='temp_c_i')[0]
                except:
                    Aparatos_C.loc['Cava2', 'Temp Refri'] = 100
                Aparatos_C.loc['Cava2', 'Temp Conge'] = 100
                Aparatos_C.loc['Cava2', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
                # Aparatos_C.loc['Cava2', 'Pot Compresor'] = InfoDeco.filter(regex='compresor_potencia')[0]
                PotCompresor = InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Cava2', 'Pot Compresor'] = Watt
                try:
                    Aparatos_C.loc['Cava2', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                except:
                    Aparatos_C.loc['Cava2', 'Temp Compresor'] = 10
                Aparatos_C.loc['Cava2', 'Difusor'] = InfoDeco.filter(regex='ventilador_c_i')[0]
                Aparatos_C.loc['Cava2', 'Tuberias'] = InfoDeco.filter(regex='tuberias')[0]
                Aparatos_C.loc['Cava2', 'Prob Refr'] = InfoDeco.filter(regex='problemas_c_i')[0]
                Aparatos_C.loc['Cava2', 'Encerrado'] = InfoDeco.filter(regex='encerrado_c_i')[0]
                Aparatos_C.loc['Cava2', 'Ventilas'] = InfoDeco.filter(regex='ventilas_c_i')[0]
                Aparatos_C.loc['Cava2', 'Alarma'] = InfoDeco.filter(regex='alarma')[0]
                Aparatos_C.loc['Cava2', 'Prob Comp'] = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Cava2', 'Prob Descr'] = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Cava2', 'Empaques'] = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Cava2', 'Termostato'] = InfoDeco.filter(regex='termostato')[0]
                # Aparatos_C.loc['Cava2', 'Ventilacion']    = InfoDeco.filter(regex='ventilacion')[0]
                Aparatos_C.loc['Cava2', 'Cierre'] = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Cava2', 'Tipo'] = InfoDeco.filter(regex='tipo')[0]
                # Aparatos_C.loc['Cava2', 'Dispensador']    = InfoDeco.filter(regex='dispensador')[0]
                try:
                    Aparatos_C.loc['Cava2', 'Encendido'] = InfoDeco.filter(regex="encendido_c_i")[0]
                except:
                    Aparatos_C.loc['Cava2', 'Encendido'] = 60
                Aparatos_C.loc['Cava2', 'Atacable'] = 'No'

                if InfoDeco.filter(regex='espendiente_c_i')[0] == 'si':
                    Aparatos_C.loc['Cava2', 'CodigoN'] = InfoDeco.filter(regex='codigofindero')[0]
                else:
                    Aparatos_C.loc['Cava2', 'CodigoN'] = InfoDeco.filter(regex='codigofinderoQQ_c_i')[0]
                Aparatos_C.loc['Cava2', 'Notas'] = notass

                if not pd.isna(InfoDeco.filter(regex='standby_c_i')[0]):
                    Aparatos_C.loc['Cava2', 'Standby'] = consumoEq(InfoDeco.filter(regex='standby_c_i')[0])
                    Aparatos_C.loc['Cava2', 'CodigoS'] = StandbyCod
                else:
                    Aparatos_C.loc['Cava2', 'Standby'] = 0
                    Aparatos_C.loc['Cava2', 'CodigoS'] = ' '
                Aparatos_C.loc['Cava2', 'Clave'] = 'CV' + ClavesRefri(Aparatos_C.loc['Cava2'])

                if InfoDeco.filter(regex='regulador_c_i')[0] == 'regulador':
                    Aparatos_C.loc['Regulador Cava2', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_consumo')[0])
                    # if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
                    #     Aparatos_C.loc['Regulador Cava', 'Marca'] = 'Cava ' + InfoDeco.filter(regex='regulador_marca')[0]
                    # else:
                    #     Aparatos_C.loc['Regulador Cava', 'Marca'] = 'Cava ' + \
                    #                                            InfoDeco.filter(regex='regulador_marca_otro')[0]
                    Aparatos_C.loc['Regulador Cava2', 'CodigoS'] = \
                    Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
                    Aparatos_C.loc['Regulador Cava2', 'Existencia'] = 1
                    Aparatos_C.loc['Regulador Cava2', 'Notas'] = notass
                    # Aparatos_C.loc['Regulador Cava', 'Clave'] = 'RG,Regulador Cava,MC'
                    Aparatos_C.loc['Regulador Cava2', 'Zona'] = Aparatos_C.loc['Cava', 'Zona']
                    Aparatos_C.loc['Regulador Cava2', 'Max_Potencia'] = PotCompresor
                    Aparatos_C.loc['Regulador Cava2', 'Atacable'] = Atac_Mec(voltaje, Aparatos_C.loc[
                        'Regulador Cava2', 'Standby'],
                                                                            Aparatos_C.loc[
                                                                                'Regulador Cava2', 'Max_Potencia'])
                    Aparatos_C.loc['Regulador Cava2', 'Clave'] = 'RG,Regulador Cava2,MC' + ',' + str(consumoEq(Aparatos_C.loc[
                                                                                                                 'Regulador Cava2', 'Max_Potencia']))

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
                # if not InfoDeco.filter(regex='adicional_regulador_c_i')[0] != 'ninguno':
                #     Aparatos_C.loc['Regulador Refrigeracion', 'Standby'] = consumoEq(InfoDeco.filter(regex='regulador_consumo')[0])
                #     if InfoDeco.filter(regex='regulador_marca')[0] != 'otro':
                #         Aparatos_C.loc['Regulador Refrigeracion', 'Marca'] = 'Adicional ' + InfoDeco.filter(regex='regulador_marca')[0]
                #     else:
                #         Aparatos_C.loc['Regulador Refrigeracion', 'Marca'] = 'Adicional' + InfoDeco.filter(regex='regulador_otra')[0]
                #     Aparatos_C.loc['Regulador Refrigeracion', 'CodigoS'] = InfoDeco.filter(regex='regulador_consumo_codigofindero')[0]
                #     Aparatos_C.loc['Regulador Refrigeracion', 'Existencia'] = 1
                #     Aparatos_C.loc['Regulador Refrigeracion', 'Clave'] = 'RG,Regulador equipo de refrigeracion,MC'
                #     Aparatos_C.loc['Regulador Refrigeracion', 'Notas'] = notass
                #     Aparatos_C.loc['Regulador Refrigeracion', 'Max_Potencia'] = Aparatos_C.loc['Refrigeracion', 'Nominal']
                #     Aparatos_C.loc['Regulador Refrigeracion', 'Atacable'] = Atac_Mec(voltaje, Aparatos_C.loc[
                #         'Regulador Refrigeracion', 'Standby'], Aparatos_C.loc['Regulador Refrigeracion', 'Max_Potencia'])

        indx+=1
    Aparatos_C.loc['Refrigerador', 'Notas'] = Circuito.filter(regex='refrigeracion_notas_c_i')[0]
    Info_R.loc['Refrigeracion', 'Notas'] = Circuito.filter(regex='refrigeracion_notas_c_i')[0]
    Info_R.loc['Refrigeracion', 'Voz']   = Circuito.filter(regex='refrigeracion_notas_c_i')[0]
    TotalCons=0
    Codigos=Aparatos_C['Clave']
    Aparatos_C['Claves'] =Codigos

    return Aparatos_C,TotalCons, Codigos