import pandas as pd
import math
from scipy import stats
import numpy as np

# 1.b. Lee otra librería (ver cuál es la Protolibreria)
def libreria2():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/Lavadora/Libreria_LavadorasySecadoras.xlsx",sheet_name='Reporte')
    except:
        Libreria = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Lavadora Y Secadora/Libreria_LavadorasySecadoras.xlsx",sheet_name='Reporte')
    Dicc = ['A', 'B', 'C', 'D', 'E'] # Define los nombres de las columnas en Excel.
    Libreria.columns = Dicc



    return Libreria



def ClavesLavaSeca(Standby):
    Codigo = 'L,'+str(Standby)

    return  Codigo


def LeeClavesLavaSeca(Claves,consumo):
    Texto=''
    lib=libreria2()
    kWh=consumo
    if pd.notna(Claves):
        ClavesS = Claves.split(",")

    #Standby=float(ClavesS[1])

    if pd.notna(Claves):
        if ClavesS[0]=='LV':
            kWh = float(consumo)
            Percentil = (1 - stats.norm.sf(x=(np.log(kWh)), loc=3.3034, scale=0.4575424))

            if Percentil >= 0.8:
                Texto = Texto + ' ' + lib.loc[4, 'E']
            if 0.6 <= Percentil < 0.8:
                Texto = Texto + ' ' + lib.loc[3, 'E']
            if 0.4 <= Percentil < 0.6:
                Texto = Texto + ' ' + lib.loc[2, 'E']
            if 0.3 <= Percentil < 0.4:
                Texto = Texto + ' ' + lib.loc[1, 'E']
            if 0.3 > Percentil:
                Texto = Texto + ' ' + lib.loc[0, 'E']


            Texto = Texto.replace('["PCML"]', str(int(100-Percentil*100)))
            Texto = Texto.replace('["PCMLF"]', str(int(Percentil * 100)))
            Texto = Texto.replace('[/n]', '<br />')

        if ClavesS[0] == 'SC':
            Percentil = (1 - stats.norm.sf(x=(np.log(kWh)), loc=3.7147, scale=1.2349))

            if Percentil >= 0.8:
                Texto = Texto + ' ' + lib.loc[9, 'E']
            if 0.6 <= Percentil < 0.8:
                Texto = Texto + ' ' + lib.loc[8, 'E']
            if 0.4 <= Percentil < 0.6:
                Texto = Texto + ' ' + lib.loc[7, 'E']
            if 0.3 <= Percentil < 0.4:
                Texto = Texto + ' ' + lib.loc[6, 'E']
            if 0.3 > Percentil:
                Texto = Texto + ' ' + lib.loc[5, 'E']

            Texto = Texto.replace('["PCMS"]', str(int(100-Percentil*100)))
            Texto = Texto.replace('["PCMSF"]', str(int( Percentil * 100)))


            Texto = Texto.replace('[/n]', '<br />')

        # if Standby > 0:
        #     Texto= Texto + lib.loc[7,'E']


    return Texto