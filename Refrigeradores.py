import pandas as pd
from Consumo    import calc_consumo
from Condiciones import condicionesRefrigeracion
from Consumo    import calc_consumo , consumoEq, temperatura



def refrigerador(Excel,Nocircuito,NomCircuito):
    Aparatos_C = pd.DataFrame(index=['Refrigerador','Congelador','Minibar','Cava','Hielos','Refrigerador2','Congelador2','Minibar2','Cava2','Hielos2','Regulador','Notas','Problemas']
                              ,columns=['Marca','Volumen','Temp Refri','Temp Conge','Pot Compresor','Temp Compresor',
                                        'Prob Comp','Prob Descr','Empaques','Termostato','Ventilacion','Cierre', 'Existencia'])
    Regulador = pd.DataFrame(index=['Regulador'],columns=['Marca','Consumo'])
    Info_R    = pd.DataFrame(index=['Refrigeracion'], columns=['Notas','Voz'])
    # Libreria = pd.DataFrame(index=['Refrigerador','Congelador','Minibar','Cava','Hielos'], columns=['Marca', 'Codigo', 'Texto'])

    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("equipos_refrigeracion", case=False)]
    Equipos= Circuito[InfoEquipos]
    #print(Equipos)
    indx=0
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

                Aparatos_C.loc['Refrigerador', 'Marca'] = InfoDeco.filter(regex='marca')[0]


                Aparatos_C.loc['Refrigerador', 'Volumen'] = (float(alto) * float(ancho) * float(profundo))*(1/(30.48**3))*0.56


                Aparatos_C.loc['Refrigerador', 'Temp Refri'] = temperatura(InfoDeco.filter(regex='trefri')[0])

                Aparatos_C.loc['Refrigerador', 'Temp Conge'] = temperatura(InfoDeco.filter(regex='tconge')[0])

                PotCompresor=InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Refrigerador', 'Pot Compresor'] =Watt
                if not InfoDeco.filter(regex='compresor_temp')[0]:
                    Aparatos_C.loc['Refrigerador', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                else:
                    Aparatos_C.loc['Refrigerador', 'Temp Compresor'] =0

                Aparatos_C.loc['Refrigerador', 'Prob Comp'] = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Refrigerador', 'Prob Descr'] = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Refrigerador', 'Empaques'] = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Refrigerador', 'Termostato'] = InfoDeco.filter(regex='termostato')[0]
                Aparatos_C.loc['Refrigerador', 'Ventilacion'] = InfoDeco.filter(regex='ventilacion')[0]
                Aparatos_C.loc['Refrigerador', 'Cierre'] = InfoDeco.filter(regex='cierre')[0]
                Aparatos_C.loc['Regulador', 'Volumen'] = InfoDeco.filter(regex='regulador_consumo')[0]
                Aparatos_C.loc['Regulador', 'Marca'] = InfoDeco.filter(regex='regulador_marca')[0]
                Aparatos_C.loc['Problemas', 'Marca'] = Circuito.filter(regex='_problemas_otro_c_i')[0]
                Aparatos_C.loc['Problemas', 'Existencia']=1



            if indx == 2:
                NomAparato = 'congelador1'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Congelador', 'Existencia'] = 1
                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundidad')[0]
                Aparatos_C.loc['Congelador', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Congelador', 'Volumen'] = float(alto) * float(ancho) * float(profundo) / 1000
                Aparatos_C.loc['Congelador', 'Temp Conge'] = InfoDeco.filter(regex='congelador1_temp')[0]
                Aparatos_C.loc['Congelador', 'Pot Compresor'] = InfoDeco.filter(regex='compresor_potencia_c_i')[0]

                PotCompresor = InfoDeco.filter(regex='compresor_potencia_c_i')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Congelador', 'Pot Compresor'] = Watt

                Aparatos_C.loc['Congelador', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                Aparatos_C.loc['Congelador', 'Prob Comp'] = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Congelador', 'Prob Descr'] = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Congelador', 'Empaques'] = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Congelador', 'Termostato'] = InfoDeco.filter(regex='termostato')[0]
                Aparatos_C.loc['Congelador', 'Ventilacion'] = InfoDeco.filter(regex='ventilacion')[0]
                Aparatos_C.loc['Congelador', 'Cierre'] = InfoDeco.filter(regex='cierre')[0]
                Regulador.loc['Regulador', 'Consumo'] = InfoDeco.filter(regex='regulador_consumo')[0]
                Regulador.loc['Regulador', 'Marca'] = InfoDeco.filter(regex='regulador_marca')[0]

            if indx == 3:
                NomAparato = 'minibar1'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Minibar', 'Existencia'] = 1
                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]
                Aparatos_C.loc['Minibar', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Minibar', 'Volumen'] = float(alto) * float(ancho) * float(profundo) / 1000
                Aparatos_C.loc['Minibar', 'Temp Refri'] = InfoDeco.filter(regex='minibar1_temp_c_i')[0]
                Aparatos_C.loc['Minibar', 'Pot Compresor'] = InfoDeco.filter(regex='compresor_potencia')[0]

                PotCompresor = InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Minibar', 'Pot Compresor'] = Watt

                Aparatos_C.loc['Minibar', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                Aparatos_C.loc['Minibar', 'Prob Comp'] = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Minibar', 'Prob Descr'] = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Minibar', 'Empaques'] = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Minibar', 'Termostato'] = InfoDeco.filter(regex='termostato')[0]
                Aparatos_C.loc['Minibar', 'Ventilacion'] = InfoDeco.filter(regex='ventilacion')[0]
                Aparatos_C.loc['Minibar', 'Cierre'] = InfoDeco.filter(regex='cierre')[0]
                Regulador.loc['Regulador', 'Consumo'] = InfoDeco.filter(regex='regulador_consumo')[0]
                Regulador.loc['Regulador', 'Marca'] = InfoDeco.filter(regex='regulador_marca')[0]


            if indx == 4:
                NomAparato = 'cava1'
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Cava', 'Existencia'] = 1
                alto = InfoDeco.filter(regex='alto')[0]
                ancho = InfoDeco.filter(regex='ancho')[0]
                profundo = InfoDeco.filter(regex='profundo')[0]
                Aparatos_C.loc['Cava', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Cava', 'Volumen'] = float(alto) * float(ancho) * float(profundo) / 1000
                Aparatos_C.loc['Cava', 'Temp Refri'] = InfoDeco.filter(regex='cava1_temp_c_i')[0]

                #Aparatos_C.loc['Cava', 'Pot Compresor'] = InfoDeco.filter(regex='compresor_potencia')[0]
                PotCompresor = InfoDeco.filter(regex='compresor_potencia')[0]
                Watt = consumoEq(PotCompresor)
                Aparatos_C.loc['Cava', 'Pot Compresor'] = Watt


                Aparatos_C.loc['Cava', 'Temp Compresor'] = InfoDeco.filter(regex='compresor_temp')[0]
                Aparatos_C.loc['Cava', 'Prob Comp'] = InfoDeco.filter(regex='compresor_problema')[0]
                Aparatos_C.loc['Cava', 'Prob Descr'] = InfoDeco.filter(regex='compresor_problema_descrp')[0]
                Aparatos_C.loc['Cava', 'Empaques'] = InfoDeco.filter(regex='empaques')[0]
                Aparatos_C.loc['Cava', 'Termostato'] = InfoDeco.filter(regex='termostato')[0]
                Aparatos_C.loc['Cava', 'Ventilacion'] = InfoDeco.filter(regex='ventilacion')[0]
                Aparatos_C.loc['Cava', 'Cierre'] = InfoDeco.filter(regex='cierre')[0]
                Regulador.loc['Regulador', 'Consumo'] = InfoDeco.filter(regex='regulador_consumo')[0]
                Regulador.loc['Regulador', 'Marca'] = InfoDeco.filter(regex='regulador_marca')[0]
        indx+=1
    Aparatos_C.loc['Notas', 'Marca'] = Circuito.filter(regex='refrigeracion_notas_c_i')[0]
    Aparatos_C.loc['Notas', 'Existencia'] = 1
    Info_R.loc['Refrigeracion', 'Notas'] = Circuito.filter(regex='refrigeracion_notas_c_i')[0]
    Info_R.loc['Refrigeracion', 'Voz']   = Circuito.filter(regex='refrigeracion_voz_c_i')[0]
    TotalCons=0

    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()




    return Aparatos, TotalCons