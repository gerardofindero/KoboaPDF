import pandas as pd
import math
from scipy import stats
import numpy as np

# 1.b. Lee otra librería (ver cuál es la Protolibreria)
def libreria2():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/Lavadora/Protolibreria_LavadorasySecadoras.xlsx")
        Precios = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/TV y refris/ProtoLibreriaTVs_EDM.xlsx",sheet_name='Precio')
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    Dicc = ['A', 'B', 'C', 'D', 'E'] # Define los nombres de las columnas en Excel.
    Libreria.columns = Dicc



    return Libreria, Precios



def ClavesLavaSeca(EquiposClusterLS):
    EquiposLAVSEC = EquiposClusterLS
    Lib=libreria2()

    for i in EquiposLAVSEC.index:
        Standby = EquiposLAVSEC.loc['TV', 'Standby']
        Codigo = 'C,'+str(Standby)

    return  Codigo


def LeeClavesLavaSeca(Claves,consumo):
    Texto=''
    lib, precios=libreria2()

    if pd.notna(Claves):
        ClavesS = Claves.split(",")

    Standby=float(ClavesS[1])

    if pd.notna(Claves):
        if ClavesS[0]=='L':
            kWh = float(consumo)
            Percentil = (1 - stats.norm.sf(x=(np.log(kWh)), loc=3.3034, scale=0.4575424))

            if Percentil > 0.7:
                Ca = 3
            if 0.33 < Percentil < 0.7:
                Ca = 2
            if 0.33 > Percentil:
                Ca = 1

            if consumo < 20:
                Texto = Texto + ' ' + lib.loc[0, 'E']

        if ClavesS[0] == 'S':
            if consumo < 20:
                Texto = Texto + ' ' + lib.loc[3, 'E']

        if Standby > 0:
            Texto= Texto + lib.loc[7,'E']

    print(Texto)
    return Texto