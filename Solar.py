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
    Aparatos_C.loc['Modulos', 'Separados'] = Equipos.filter(regex='modulos_separados')[0]
    Aparatos_C.loc['Modulos', 'Potencia'] = Equipos.filter(regex='modulos_potencia_W')[0]
    Aparatos_C.loc['Modulos', 'Cantidad'] = Equipos.filter(regex='modulos_cantidad')[0]

    print(Equipos)

    return Aparatos_C
    #print(CS)