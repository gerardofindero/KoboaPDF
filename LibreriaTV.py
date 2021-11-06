import pandas as pd
import math
from scipy import stats
import numpy as np

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
        #Precio = (0.0151*((Pulgadas)**4))-(2.6271*((Pulgadas)**3)) + (164.63*((Pulgadas)**2)) - (4134*(Pulgadas)) + 37921.0
        #Ahorro= (Potencia - math.exp(3.189644 + (0.034468 * Pulgadas))) / Potencia
        Precio     = (1.873320 + 0.030815*(Pulgadas))**(1/0.13) # Precio de una nueva TV
        PotTeorica = math.exp(3.189644 + 0.034468 * Pulgadas) # Potencia teórica de una TV LED
        Ahorro     = 1 - PotTeorica / Potencia # Ahorro (fracción) con una TV LED
        uso = Consumo*1000/(Potencia*60) # Calcula las horas diarias de consumo promedio para los 60 días del bimestre

        if Consumo==0: #Si el consumo es cero, lo convierte en 0.1 para evitar errores en la fórmula de ROI.
            Consumo=0.1

        # Cálculo de retorno de inversión
        Wattakwh = 24*60/1000 # Convierte un watt de standby a KWh por bimestre

        if Standby>1:
            ROI=Precio/(DAC*((Standby-1)*Wattakwh + Ahorro*Consumo)) # Considera gastos en standby

        else:
            ROI=abs(Precio/(DAC*((Standby-1)*24*60/1000 + Ahorro*Consumo)))


        if Consumo==0:
            Consumo=0.1

        WTV=25.57* math.exp(0.035*Pulgadas)
        WTV2=31.17* math.exp(0.035*Pulgadas)
        XX         = np.log(Potencia) # Logaritmo de la potencia (será útil para calcular percentiles)
        Percentil = stats.norm.sf((XX-(3.189644 + 0.034468 * Pulgadas))/0.2606) # Percentil de potencia de la TV en cuestión


        if uso>=4.0:
            Texto = Texto +' '+ lib.loc['TV03B','Texto']
            bien=False
        if 2<=uso<4.0:
            Texto = Texto +' '+ lib.loc['TV03A','Texto']
            bien=True
        if uso < 2 or Consumo<15:
            bien=True
            Texto = Texto +' '+ lib.loc['TV01A','Texto']
        else:
            #if Potencia>=WTV2:
            if Percentil>0.9:
                print(ROI)
                if ROI<18:
                    Texto = Texto +' '+ lib.loc['TV02A','Texto']
                    Texto = Texto +' '+ lib.loc['TV02C','Texto']
                    linkA=EncontrarRemplazo(reemplazos, Pulgadas)
                    Texto = Texto + ' ' + lib.loc['TV04B', 'Texto']
                    Address = 'Link de compra'
                    LinkS = '<link href="' + str(linkA) + '"color="blue">' + Address + ' </link>'
                    Texto = Texto + '<br /> '+  '<br /> '+LinkS
                else:
                    Texto = Texto +' '+ lib.loc['TV02A','Texto']
                    Texto = Texto + ' ' + lib.loc['TV04A', 'Texto']
            else:
                Texto = Texto +' '+ lib.loc['TV02B','Texto']


        # if WTV<=Potencia<WTV2:
        #     Texto = Texto +' '+ lib.loc['TV02B','Texto']
        # if WTV > Potencia:




        if Standby>1:
            Texto = Texto + ' ' + lib.loc['TV05A', 'Texto']

    if bien==True:
        Texto = Texto.replace('[PRON]','El problema es que tu')
    if bien==False:
        Texto = Texto.replace('[PRON]','[/n]Otro problema es que tu')
    Texto = Texto.replace('[/n]','<br />')
    Texto = Texto.replace('[...]', ' ')
    Texto = Texto.replace('[Ahorro]', str(round(abs(Ahorro))))
    Texto = Texto.replace('[ROI]', str(round(abs(ROI))))
    Texto = Texto.replace('[ConsumoStandBy]', str(round(Standby)))
    Texto = Texto.replace('[USO]', str(round(uso)))



    return Texto








#
# # 1.b. Lee otra librería (ver cuál es la Protolibreria)
# def libreria2():
#     try:
#         Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/TV/Librería_TVs.xlsx",sheet_name='Libreria')
#         Precios = pd.read_excel(
#             f"../../../Recomendaciones de eficiencia energetica/Librerias/TV/Librería_TVs.xlsx",sheet_name='Precio')
#         Reemplazos = pd.read_excel(
#             f"../../../Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/TV/Librería_TVs.xlsx",
#             sheet_name='Reemplazos')
#     except:
#         Libreria = pd.read_excel(
#             f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/TV/Librería_TVs.xlsx",
#             sheet_name='Libreria')
#         Precios = pd.read_excel( f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/TV/Librería_TVs.xlsx",sheet_name='Precio')
#         Reemplazos = pd.read_excel(
#             f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/TV/Librería_TVs.xlsx",
#             sheet_name='Reemplazos')
#
#     Libreria=Libreria.set_index('Codigo')
#
#
#     return Libreria, Precios, Reemplazos
#
#
#
# def ClavesClusterTV(EquiposClusterTV):
#     EquiposCTV = EquiposClusterTV
#     EquiposCTV = EquiposCTV.fillna(0)
#     Standby     = EquiposClusterTV.loc['TV', 'Standby']
#     Pulgadas    = EquiposClusterTV.loc['TV', 'Pulgadas']
#     PotenciaTV   = EquiposClusterTV.loc['TV', 'Nominal']
#     Tolerancia = EquiposClusterTV.loc['TV', 'Tolerancia']
#     if Tolerancia == 'no_haydatos':
#         Tolerancia= 'F'
#     else:
#         Tolerancia ='T'
#
#     Codigo = 'TV,'+Tolerancia +','+ str(PotenciaTV) +'/'+str(Standby)+'/'+str(Pulgadas)
#
#     return Codigo
#
#
# def Clasifica(Claves):
#     ClavesSep='N'
#     if pd.notna(Claves):
#         ClavesSep=Claves.split(",")
#     return ClavesSep[0]
#
#
# def EncontrarRemplazo(reemplazo,Pulgadas):
#     mx=Pulgadas+Pulgadas*.1
#     mn = Pulgadas - Pulgadas * .1
#     Filtro1 = reemplazo.loc[(reemplazo['C'].astype(int)) < mx]
#     Filtro2 = Filtro1.loc[Filtro1['C'].astype(int) > mn]
#     Filtro2.reset_index(drop=True, inplace=True)
#     return Filtro2['P'][0]
#
#
# def LeeClavesTV(Claves,Uso,Consumo,DAC):
#     Texto=''
#     lib, precios, reemplazos =libreria2()
#     if pd.notna(Claves):
#         ClavesSep=Claves.split(",")
#         Tolerancia = ClavesSep[1]
#         Datos= ClavesSep[2].split("/")
#         Potencia=float(Datos[0])
#         Standby = float(Datos[1])
#         Pulgadas=float(Datos[2])
#
#         # Estimaciones de base
#         Precio     = (1.873320 + 0.030815*(Pulgadas))**(1/0.13) # Precio de una nueva TV
#
#         PotTeorica = math.exp(3.189644 + 0.034468 * Pulgadas) # Potencia teórica de una TV LED
#
#         Ahorro     = 1 - PotTeorica / Potencia # Ahorro (fracción) con una TV LED
#
#         XX         = np.log(Potencia) # Logaritmo de la potencia (será útil para calcular percentiles)
#
#         Percentil = stats.norm.sf((XX-(3.189644 + 0.034468 * Pulgadas))/0.2606) # Percentil de potencia de la TV en cuestión
#
#         Horas = Consumo*1000/(Potencia*60) # Calcula las horas diarias de consumo promedio para los 60 días del bimestre
#
#         Wattakwh = 24*60/1000 # Convierte un watt de standby a KWh por bimestre
#
#         ROI=0
#         if Consumo==0: #Si el consumo es cero, lo convierte en 0.1 para evitar errores en la fórmula de ROI.
#             Consumo=0.1
#
#         # Cálculo de retorno de inversión
#
#         if Standby>1:
#             ROI=Precio/(DAC*((Standby-1)*Wattakwh + Ahorro*Consumo)) # Considera gastos en standby
#
#         else:
#             ROI=Precio/(DAC*((Standby-1)*24*60/1000 + Ahorro*Consumo))
#
#         if Percentil > 0.9: # Asigna texto indicando que la TV NO es eficiente y si vale la pena un reemplazo
#             if ROI<=18:
#                 Texto = Texto + ' ' + lib.loc['TV01A', 'Texto']
#             elif ROI >18:
#                 Texto = Texto + ' ' + lib.loc['TV01B', 'Texto']
#
#         if Percentil<= 0.8:
#             if Horas>4:
#                 Texto = Texto + ' ' + lib.loc['TV02A', 'Texto']
#
#         elif Horas<=4:
#             if Horas>1:
#                 Texto = Texto + ' ' + lib.loc['TV02B', 'Texto']
#             elif Horas<=1:
#                 Texto = Texto + ' ' + lib.loc['TV02C', 'Texto']
#
#         Texto = Texto.replace('[Ahorro]', str(round(abs(Ahorro)*100)))
#         Texto = Texto.replace('[ROI]', str(round(abs(ROI))))
#
#     return Texto
