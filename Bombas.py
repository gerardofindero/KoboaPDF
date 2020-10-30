import pandas as pd
from Consumo    import calc_consumo

def bombas (Excel,Nocircuito):
    print("Plomeria")
    Aparatos_C = pd.DataFrame(columns=['Aparatos'])
    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("plom", case=False)]
    Equipos= Circuito[InfoEquipos]
    indx=0

    NomAparato='Bomba'
    Aparatos_C.loc[0,'Aparatos'] = NomAparato
    InfoDeco = Equipos.filter(regex='bomba1')
    Aparatos_C.loc[0, 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
    Aparatos_C.loc[0, 'Tipo de bomba'] = InfoDeco.filter(regex='tipo')[0]
    Aparatos_C.loc[0, 'Sistema de la bomba'] =InfoDeco.filter(regex='sistema')[0]

    NomAparato = 'Tinaco'
    Aparatos_C.loc[1, 'Aparatos'] = NomAparato
    InfoDeco = Equipos.filter(regex='tinaco1')
    Aparatos_C.loc[1, 'No. de Tinacos'] = InfoDeco.filter(regex='existencia')[0]
    Aparatos_C.loc[1, 'Altura del tinaco'] = InfoDeco.filter(regex='altura')[0]


    NomAparato = 'Tuberia'
    Aparatos_C.loc[2, 'Aparatos'] = NomAparato
    InfoDeco = Equipos.filter(regex='tuberia')
    Aparatos_C.loc[2, 'Presion de agua'] = InfoDeco.filter(regex='presion')[0]
    Aparatos_C.loc[2, 'Hay jarros de aire'] = InfoDeco.filter(regex='jarrosaire')[0]
    Aparatos_C.loc[2, 'Diametro tuberia'] = InfoDeco.filter(regex='diametro')[0]
    Aparatos_C.loc[2, 'Presion planta baja'] = InfoDeco.filter(regex='presionpb')[0]

    return Aparatos_C
