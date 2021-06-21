import pandas as pd
from scipy.stats import norm
def leerLibreriaPlanchas():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/Planchas/libreria_planchas.xlsx",sheet_name='libreriaPlanchas')
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    Dicc = ['A','B', 'C'] # Define los nombres de las columnas en Excel.
    Libreria.columns = Dicc
    return Libreria

def leerConsumoPlanchas(consumo):
    try:
        statistics = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Planchas/libreria_planchas.xlsx",
            sheet_name='statistics')
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    Dicc = ['A', 'B', 'C','D','F']  # Define los nombres de las columnas en Excel.
    statistics.columns = Dicc
    # media y desviacion estandar almacenados en el excel de planchas
    # en esta sección se esta trabajdno con la transformación consumo**0.3 (kWh)
    media=statistics.loc[0,'A']
    desStd=statistics.loc[3,'A']
    consumoTrans= consumo**0.3
    percentil= norm.cdf(consumoTrans,loc=media,scale=desStd)
    lib=leerLibreriaPlanchas()
    if percentil <0.33:
        texto=lib.loc[3,'C']
    if 0.33>=percentil<0.66:
        texto = lib.loc[4, 'C']
    if percentil>=0.66:
        texto = lib.loc[5, 'C']

    return texto

