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

    # Dicc = ['A', 'B', 'C', 'D', 'E','F','G'] # Define los nombres de las columnas en Excel.
    # Libreria.columns = Dicc
    Libreria=Libreria.set_index('Codigo')
    Dicc = ['A', 'B', 'C', 'D', 'E', 'F', 'G','H','I','J','K','L','M','N','O','P','Q','R']  # Define los nombres de las columnas en Excel.
    Reemplazos.columns = Dicc


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
        Precio = (0.0151*((Pulgadas)**4))-(2.6271*((Pulgadas)**3)) + (164.63*((Pulgadas)**2)) - (4134*(Pulgadas)) + 37921.0
        Ahorro= (Potencia - math.exp(3.189644 + (0.034468 * Pulgadas))) / Potencia

        if Consumo==0:
            Consumo=0.1

        WTV=25.57* math.exp(0.035*Pulgadas)
        WTV2=31.17* math.exp(0.035*Pulgadas)

        if Potencia>=WTV2:
            Texto = Texto +' '+ lib.loc['TV03B','Texto']
            linkA=EncontrarRemplazo(reemplazos, Pulgadas)
            Texto = Texto + ' ' + lib.loc['TV04', 'Texto']
            Address = 'Link de compra'
            LinkS = '<link href="' + str(linkA) + '"color="blue">' + Address + ' </link>'
            Texto = Texto + '<br /> '+  '<br /> '+LinkS
        if WTV<=Potencia<WTV2:
            Texto = Texto +' '+ lib.loc['TV02B','Texto']
        if WTV > Potencia:
            Texto = Texto +' '+ lib.loc['TV01B','Texto']

        uso=(Consumo*1000)/(Potencia*60)
        if uso>=5.0:
            Texto = Texto +' '+ lib.loc['TV03A','Texto']
        if 2.5<=uso<5.0:
            Texto = Texto +' '+ lib.loc['TV02A','Texto']
        if uso < 2.5:
            Texto = Texto +' '+ lib.loc['TV01A','Texto']




        if Standby>1:
            Texto = Texto + ' ' + lib.loc['TV05', 'Texto']

    Texto = Texto.replace('[/n]','<br />')
    Texto = Texto.replace('[...]', ' ')
    Texto = Texto.replace('[Ahorro]', str(round(abs(Ahorro))))
    #Texto = Texto.replace('[ROI]', str(round(abs(ROI))))
    Texto = Texto.replace('[ConsumoStandBy]', str(round(Standby)))
    Texto = Texto.replace('[Uso]', str(round(uso)))

    return Texto