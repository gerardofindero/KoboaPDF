import pandas as pd
from Consumo    import calc_consumo

def especiales(Excel,Nocircuito):
    print("Especiales")
    Aparatos_C = pd.DataFrame(columns=['Aparatos'])
    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("equipos_especiales", case=False)]
    Equipos= Circuito[InfoEquipos]
    indx=0

    for i in Equipos:
        if i == 'otro':
            esp= 'especial'+ str(indx+1)
            NomAparato= esp
            #Aparatos_C.loc[indx,'Aparatos'] = NomAparato
            InfoDeco = Circuito.filter(regex=NomAparato)
            Aparatos_C.loc[indx,'Aparatos']  = InfoDeco.filter(regex='nombre')[0]
            Aparatos_C.loc[indx,'Nominal']   = InfoDeco.filter(regex='consreal')[0]
            Aparatos_C.loc[indx,'Consumo']   = InfoDeco.filter(regex='consrealstby')[0]
            Aparatos_C.loc[indx, 'Marca']    = InfoDeco.filter(regex='marca')[0]

        if not pd.isnull(i) and i!='otro':

            esp = 'especial' + str(indx + 1)

            NomAparato = esp
            Aparatos_C.loc[indx,'Aparatos'] = i
            InfoDeco = Circuito.filter(regex=NomAparato)
            #Aparatos_C.loc[indx, 'Aparatos'] = InfoDeco.filter(regex='nombre')[0]
            Aparatos_C.loc[indx, 'Nominal']   = InfoDeco.filter(regex='consreal')[0]
            Aparatos_C.loc[indx, 'Consumo']   = InfoDeco.filter(regex='consrealstby')[0]
            Aparatos_C.loc[indx, 'Marca']     = InfoDeco.filter(regex='marca')[0]

        indx = indx +1
    TotalConsumo = calc_consumo(Aparatos_C)

    return Aparatos_C , TotalConsumo