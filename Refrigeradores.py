import pandas as pd
from Consumo    import calc_consumo


def refrigerador(Excel,Nocircuito):
    Aparatos_C = pd.DataFrame(index=['Refrigerador','Congelador','Minibar','Cava','Hielos','Refrigerador2','Congelador2','Minibar2','Cava2','Hielos2','Regulador']
                              ,columns=['Marca','Nominal','Consumo','T_Compresor','T_Refrigerador','Problema'])

    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("refrigeracion", case=False)]
    Equipos= Circuito[InfoEquipos]

    indx=0
    for i in Equipos:
        if i == 1:
            if indx == 1:
                NomAparato='refrigerador'
                #Aparatos_C.loc[indx,'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Refrigerador', 'Marca']         = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Refrigerador','Problemas']      = InfoDeco.filter(regex='problemas')[0]
                Aparatos_C.loc['Refrigerador','T Compresor']    = InfoDeco.filter(regex='temp_compresor_refrigerador_c_i')[0]
                Aparatos_C.loc['Refrigerador','Nominal']        = InfoDeco.filter(regex='fp')[0]
                Aparatos_C.loc['Refrigerador','T Refrigerador'] = InfoDeco.filter(regex='temp_refri_refrigerador')[0]
                Aparatos_C.loc['Refrigerador','Problema Refri'] = InfoDeco.filter(regex='temp_refri_refrigerador')[0]
                Aparatos_C.loc['Refrigerador','Problema Compresor'] = InfoDeco.filter(regex='temp_refri_refrigerador')[0]
                ReguRef = InfoDeco.filter(regex='regulador')
                if not ReguRef.empty:
                    Aparatos_C.loc['Regulador', 'Consumo'] = InfoDeco.filter(regex='consumo_regulador')[0]
                    Aparatos_C.loc['Regulador', 'Marca']   = InfoDeco.filter(regex='marca_regulador')[0]

            if indx == 2:
                NomAparato='congelador'
                #Aparatos_C.loc[indx, 'Aparatos'] = NomAparato
                InfoDeco = Circuito.filter(regex=NomAparato)
                Aparatos_C.loc['Congelador', 'Marca']              = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Congelador', 'Capacidad']          = InfoDeco.filter(regex='capacidad')[0]
                Aparatos_C.loc['Congelador', 'Problemas']          = InfoDeco.filter(regex='problemas')[0]
                Aparatos_C.loc['Congelador', 'T Compresor']        = InfoDeco.filter(regex='temp_compresor')[0]
                Aparatos_C.loc['Congelador', 'Potencia Compresor'] = InfoDeco.filter(regex='fp')[0]
                Aparatos_C.loc['Congelador', 'T Refrigerador'] = InfoDeco.filter(regex='temp_refrigerador')[0]
                ReguRef = InfoDeco.filter(regex='regulador')
                if not ReguRef.empty:
                    Aparatos_C.loc['Regulador', 'Consumo']  = InfoDeco.filter(regex='consumo_regulador')[0]
                    Aparatos_C.loc['Regulador', 'Marca']    = InfoDeco.filter(regex='marca_regulador')[0]

        indx+=1
    TotalCons=180
    print(Aparatos_C)
    #TotalCons= calc_consumo(Aparatos_C)

    return Aparatos_C, TotalCons