import pandas as pd
import math

# 1.b. Lee otra librería (ver cuál es la Protolibreria)
def libreria2():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/TV y refris/ProtoLibreriaTVs_EDM.xlsx")
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


def Clasifica(Claves):
    ClavesSep='N'
    if pd.notna(Claves):
        ClavesSep=Claves.split(", ")
    return ClavesSep[0]


def LeeClavesLavaSeca(Claves,Uso,Consumo,DAC):
    Texto=''
    lib, precios=libreria2()
    if pd.notna(Claves):
        ClavesSep=Claves.split(", ")
        Datos= ClavesSep[1].split("/")
        Potencia=Datos[0]
        Standby = Datos[1]
        Pulgadas=Datos[2]
        percentil=70

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