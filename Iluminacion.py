import pandas as pd
from Consumo    import calc_consumo

def iluminacion (Excel,Nocircuito):

    Aparatos_C = pd.DataFrame(columns=['Aparatos'])
    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("ilum", case=False)]
    Equipos= Circuito[InfoEquipos]
    indx=0

    NomAparato='Luminaria'
    Aparatos_C.loc[0,'Aparatos'] = NomAparato
    InfoDeco = Circuito.filter(regex='luminaria1')
    Aparatos_C.loc[0, 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
    Aparatos_C.loc[0, 'Numero de luminarias'] = InfoDeco.filter(regex='numero')[0]
    Aparatos_C.loc[0, 'Tecnología luminaria'] =InfoDeco.filter(regex='tecnologia')[0]
    Aparatos_C.loc[0, 'Tamaño luminaria'] = InfoDeco.filter(regex='tamano')[0]
    Entrada= InfoDeco.filter(regex='entrada')[0]
    if Entrada == 'otro':
        Aparatos_C.loc[0, 'Entrada luminaria'] = InfoDeco.filter(regex='entrada')[1]
    else:
        Aparatos_C.loc[0, 'Entrada luminaria'] = InfoDeco.filter(regex='entrada')[0]


    if Circuito.filter(regex='otros_focos1').any:

        NomAparato = 'Luminaria'
        Aparatos_C.loc[1, 'Aparatos'] = NomAparato
        InfoDeco = Circuito.filter(regex='luminaria2')
        Aparatos_C.loc[1, 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
        Aparatos_C.loc[1, 'Numero de luminarias'] = InfoDeco.filter(regex='numero')[0]
        Aparatos_C.loc[1, 'Tecnología luminaria'] = InfoDeco.filter(regex='tecnologia')[0]
        Aparatos_C.loc[1, 'Tamaño luminaria'] = InfoDeco.filter(regex='tamano')[0]
        Entrada = InfoDeco.filter(regex='entrada')[0]
        if Entrada == 'otro':
            Aparatos_C.loc[1, 'Entrada luminaria'] = InfoDeco.filter(regex='entrada')[1]
        else:
            Aparatos_C.loc[1, 'Entrada luminaria'] = InfoDeco.filter(regex='entrada')[0]

    if Circuito.filter(regex='otros_focos2').any:

        NomAparato = 'Luminaria'
        Aparatos_C.loc[2, 'Aparatos'] = NomAparato
        InfoDeco = Circuito.filter(regex='luminaria3')
        Aparatos_C.loc[2, 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
        Aparatos_C.loc[2, 'Numero de luminarias'] = InfoDeco.filter(regex='numero')[0]
        Aparatos_C.loc[2, 'Tecnología luminaria'] = InfoDeco.filter(regex='tecnologia')[0]
        Aparatos_C.loc[2, 'Tamaño luminaria'] = InfoDeco.filter(regex='tamano')[0]
        Entrada = InfoDeco.filter(regex='entrada')[0]
        if Entrada == 'otro':
            Aparatos_C.loc[2, 'Entrada luminaria'] = InfoDeco.filter(regex='entrada')[1]
        else:
            Aparatos_C.loc[2, 'Entrada luminaria'] = InfoDeco.filter(regex='entrada')[0]

    TotNominal=calc_consumo(Aparatos_C)
    return Aparatos_C
