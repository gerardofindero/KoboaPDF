import pandas as pd

def solar(Excel,Nocircuito, Nomcircuito):
    Aparatos_C = pd.DataFrame(
        index=['Modulos','Baterias'],
        columns=['Cantidad','Separados','Potencia','Mes','Inclinacion','Sombreado','SomNotas','MarcaC','MarcaM',
                 'Interconexion','InterNotas','InverNotas','Codigo'])

    Circuito = Excel.loc[Nocircuito]
    Columnas = Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("solar", case=False)]
    Equipos = Circuito[InfoEquipos]
    CS = Equipos.filter(regex='modulos')
    Aparatos_C.loc['Modulos', 'Cantidad'] = CS.filter(regex='cantidad')[0]
    Aparatos_C.loc['Modulos', 'Separados'] = CS.filter(regex='separados')[0]
    Aparatos_C.loc['Modulos', 'Potencia'] = CS.filter(regex='potencia_W')[0]

    return Aparatos_C
    #print(CS)