import pandas as pd
import math
from scipy import stats
import numpy as np

# 1.b. Lee otra librería (ver cuál es la Protolibreria)
def libreria2():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/TV/Librería_TVs.xlsx",sheet_name='Libreria')
        Precios = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/TV/Librería_TVs.xlsx",sheet_name='Precio')
        Reemplazos = pd.read_excel(
            f"../../../Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/TV/Librería_TVs.xlsx",
            sheet_name='Reemplazos')
    except:
        Libreria = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/TV/Librería_TVs.xlsx",
            sheet_name='Libreria')
        Precios = pd.read_excel( f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/TV/Librería_TVs.xlsx",sheet_name='Precio')
        Reemplazos = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/TV/Librería_TVs.xlsx",
            sheet_name='Reemplazos')
    #
    # Dicc = ['A', 'B', 'C', 'D', 'E','F','G'] # Define los nombres de las columnas en Excel.
    # Libreria.columns = Dicc
    # # Dicc = ['A', 'B', 'C', 'D', 'E', 'F', 'G','H','I','J','K','L','M','N','O','P','Q','R']  # Define los nombres de las columnas en Excel.
    # # Reemplazos.columns = Dicc

    #Libreria2=Libreria2.set_index('Codigo')
    Libreria=Libreria.set_index('Codigo')


    return Libreria, Precios, Reemplazos



def ClavesClusterTV(EquiposClusterTV):
    EquiposCTV = EquiposClusterTV
    EquiposCTV = EquiposCTV.fillna(0)
    Standby     = EquiposClusterTV.loc['TV', 'Standby']
    Pulgadas    = EquiposClusterTV.loc['TV', 'Pulgadas']
    PotenciaTV   = EquiposClusterTV.loc['TV', 'Nominal']
    Tolerancia = EquiposClusterTV.loc['TV', 'Tolerancia']
    if Tolerancia == 'no_haydatos':
        Tolerancia= 'F'
    else:
        Tolerancia ='T'

    Codigo = 'TV,'+Tolerancia +','+ str(PotenciaTV) +'/'+str(Standby)+'/'+str(Pulgadas)

    return Codigo


def Clasifica(Claves):
    ClavesSep='N'
    if pd.notna(Claves):
        ClavesSep=Claves.split(",")
    return ClavesSep[0]


def EncontrarRemplazo(reemplazo,Pulgadas):
    mx=Pulgadas+Pulgadas*.1
    mn = Pulgadas - Pulgadas * .1
    Filtro1 = reemplazo.loc[(reemplazo['C'].astype(int)) < mx]
    Filtro2 = Filtro1.loc[Filtro1['C'].astype(int) > mn]
    Filtro2.reset_index(drop=True, inplace=True)
    return Filtro2['P'][0]


def LeeClavesTV(Claves,Uso,Consumo,DAC):
    Texto=''
    lib, precios, reemplazos =libreria2()
    if pd.notna(Claves):
        ClavesSep=Claves.split(",")
        Tolerancia = ClavesSep[1]
        Datos= ClavesSep[2].split("/")
        Potencia=float(Datos[0])
        Standby = float(Datos[1])
        Pulgadas=float(Datos[2])

        # Estimaciones de base
        Precio     = (1.873320 + 0.030815*(Pulgadas))**(1/0.13) # Precio de una nueva TV

        PotTeorica = math.exp(3.189644 + 0.034468 * Pulgadas) # Potencia teórica de una TV LED

        Ahorro     = 1 - PotTeorica / Potencia # Ahorro (fracción) con una TV LED

        XX         = np.log(Potencia) # Logaritmo de la potencia (será útil para calcular percentiles)

        Percentil = stats.norm.sf((XX-(3.189644 + 0.034468 * Pulgadas))/0.2606) # Percentil de potencia de la TV en cuestión

        Horas = Consumo*1000/(Potencia*60) # Calcula las horas diarias de consumo promedio para los 60 días del bimestre

        Wattakwh = 24*60/1000 # Convierte un watt de standby a KWh por bimestre

        ROI=0
        if Consumo==0: #Si el consumo es cero, lo convierte en 0.1 para evitar errores en la fórmula de ROI.
            Consumo=0.1

        # Cálculo de retorno de inversión

        if Standby>1:
            ROI=Precio/(DAC*((Standby-1)*Wattakwh + Ahorro*Consumo)) # Considera gastos en standby

        else:
            ROI=Precio/(DAC*((Standby-1)*24*60/1000 + Ahorro*Consumo))

        if Percentil > 0.8: # Asigna texto indicando que la TV NO es eficiente y si vale la pena un reemplazo
            if ROI<=18:
                Texto = Texto + ' ' + lib.loc['TV01A', 'Texto']
            elif ROI >18:
                Texto = Texto + ' ' + lib.loc['TV01B', 'Texto']

        if Percentil<= 0.8:
            if Horas>4:
                Texto = Texto + ' ' + lib.loc['TV02A', 'Texto']

        elif Horas<=4:
            if Horas>1:
                Texto = Texto + ' ' + lib.loc['TV02B', 'Texto']
            elif Horas<=1:
                Texto = Texto + ' ' + lib.loc['TV02C', 'Texto']

        Texto = Texto.replace('[Ahorro]', str(round(abs(Ahorro)*100)))
        Texto = Texto.replace('[ROI]', str(round(abs(ROI))))

    return Texto
