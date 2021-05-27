import pandas as pd
import math
from scipy import stats
import numpy as np

# 1.b. Lee otra librería (ver cuál es la Protolibreria)
def libreria2():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/TV y refris/ProtoLibreriaTVs_EDM.xlsx",sheet_name='Libreria')
        Precios = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/TV y refris/ProtoLibreriaTVs_EDM.xlsx",sheet_name='Precio')
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    Dicc = ['A', 'B', 'C', 'D', 'E','F'] # Define los nombres de las columnas en Excel.
    Libreria.columns = Dicc



    return Libreria, Precios



def ClavesClusterTV(EquiposClusterTV):
    EquiposCTV = EquiposClusterTV
    EquiposR = EquiposCTV.fillna(0)
    Lib=libreria2()
    for i in EquiposCTV.index:
        Standby = EquiposClusterTV.loc['TV', 'Standby']
        Pulgadas  = EquiposClusterTV.loc['TV', 'Pulgadas']
        ConsumoTV   = EquiposClusterTV.loc['TV', 'Nominal']

        Codigo = 'C,'+ str(ConsumoTV) +'/'+str(Standby)+'/'+str(Pulgadas)




    return  Codigo


def Clasifica(Claves):
    ClavesSep='N'
    if pd.notna(Claves):
        ClavesSep=Claves.split(", ")
    return ClavesSep[0]


def LeeClavesTV(Claves,Uso,Consumo,DAC):
    Texto=''
    lib, precios=libreria2()
    if pd.notna(Claves):
        ClavesSep=Claves.split(", ")
        Datos= ClavesSep[1].split("/")
        Potencia=Datos[0]
        Standby = Datos[1]
        Pulgadas=Datos[2]
        percentil=70


        Pulgadas=20
        Watts=80
        kWh=50
        #CC = kWh - (2.989644 + 0.034468 * 40) / 0.2606
        XX = np.log(Watts)
        Percentil = stats.norm.sf((XX-(3.189644 + 0.034468 * Pulgadas))/0.2606)
        print(Percentil)

        y = 25.567 *(math.exp(0.035* Pulgadas))
        MaxP=(y+(y*.25))
        MinP=(y - (y * .25))

        Ahorro = y*Consumo/Potencia
        Ahorro = 1-(Ahorro/Consumo)



        if Consumo>80:
            Texto = Texto + ' ' + lib.loc[3, 'E']

        if Uso>=30:
            Texto = Texto + ' ' + lib.loc[10, 'E']

        ## Uso
        if Uso<20:
            Texto = Texto + ' ' + lib.loc[0, 'E']

        if Uso>=20:
            Texto = Texto + ' ' + lib.loc[15, 'E']


        if Potencia > MaxP:
            Texto= Texto+' '+lib.loc[1,'E']
        if Potencia <= MaxP:
            Texto= Texto+' Tu TV tiene un consumo promedio'

        if Standby > 0:
            Texto= Texto + lib.loc[9,'E']


    return Texto