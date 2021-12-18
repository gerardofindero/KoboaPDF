import pandas as pd

def solar(Excel,Nocircuito, Nomcircuito):
    Aparatos_C = pd.DataFrame(
        index=['Modulos','Baterias'],
        columns=['Cantidad','Separados','Potencia','Mes','Inclinacion','Sombreado','SomNotas','MarcaC','MarcaM',
                 'Interconexion','InterNotas','InverNotas','Codigo','Tipo'])

    Circuito = Excel.loc[Nocircuito]
    Columnas = Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("solar", case=False)]
    Equipos = Circuito[InfoEquipos]
    Aparatos_C.loc['Modulos', 'Tipo'] = Equipos.filter(regex='tipo_c_i')[0]
    Aparatos_C.loc['Modulos', 'Inclinacion'] = Equipos.filter(regex='inclinacion_c_i')[0]
    Aparatos_C.loc['Modulos', 'Mes'] = Equipos.filter(regex='mes_c_i')[0]
    Aparatos_C.loc['Modulos', 'Sombreado'] = Equipos.filter(regex='sombreados_c_i')[0]
    Aparatos_C.loc['Modulos', 'Sombreado_Notas'] = Equipos.filter(regex='sombreados_notas_c_i')[0]
    Aparatos_C.loc['Modulos', 'Separados'] = Equipos.filter(regex='modulos_separados')[0]
    Aparatos_C.loc['Modulos', 'Potencia'] = Equipos.filter(regex='modulos_potencia_W')[0]
    Aparatos_C.loc['Modulos', 'Cantidad'] = Equipos.filter(regex='modulos_cantidad')[0]
    Aparatos_C.loc['Modulos', 'Orientacion'] = Equipos.filter(regex='orientacion')[0]
    Aparatos_C.loc['Modulos', 'Aclarar'] = Equipos.filter(regex='aclarar')[0]
    Aparatos_C.loc['Modulos', 'Bat_Numero'] = Equipos.filter(regex='baterias_num_c_i')[0]
    Aparatos_C.loc['Modulos', 'Inversor'] = Equipos.filter(regex='inversores_notas')[0]
    Aparatos_C.loc['Modulos', 'Arreglo'] = Equipos.filter(regex='arreglo_notas_c_i')[0]
    Aparatos_C.loc['Modulos', 'Hotspot'] = Equipos.filter(regex='hotspot_c_i')[0]
    Aparatos_C.loc['Modulos', 'Hotspot_Notas'] = Equipos.filter(regex='hotspot_notas')[0]
    Aparatos_C.loc['Modulos', 'Interconexion'] = Equipos.filter(regex='interconexion_c_i')[0]
    Aparatos_C.loc['Modulos', 'Inter_Derivado'] = Equipos.filter(regex='interconexion_derivado_c_i')[0]
    Aparatos_C.loc['Modulos', 'Inter_Notas'] = Equipos.filter(regex='interconexion_notas_c_i')[0]


    Aparatos_C.loc['Modulos', 'Existencia'] = 1

    print(Equipos)

    return Aparatos_C
    #print(CS)