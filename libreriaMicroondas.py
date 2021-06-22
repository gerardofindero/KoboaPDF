import pandas as pd
from scipy.stats import norm
def leerLibreriaMicroondas():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/Microondas/libreria_microondas.xlsx",sheet_name='libreriaMicroondas')
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    Dicc = ['A','B', 'C'] # Define los nombres de las columnas en Excel.
    Libreria.columns = Dicc
    return Libreria

def leerConsumoMicroondas(consumo):
    try:
        statistics = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Microondas/libreria_microondas.xlsx",
            sheet_name='statistics')
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    Dicc = ['A', 'B', 'C','D','F']  # Define los nombres de las columnas en Excel.
    statistics.columns = Dicc
    # media y desviacion estandar almacenados en el excel de libreria_microondas.xlsx
    # en esta sección se esta trabajdno con la transformación consumo**0.4 (kWh)
    media=statistics.loc[0,'B']
    desStd=statistics.loc[3,'B']
    consumoTrans= consumo**0.4
    percentil= norm.cdf(consumoTrans,loc=float(media),scale=float(desStd))
    percentil=round(percentil,2)
    print(percentil)
    lib=leerLibreriaMicroondas()
    if percentil <0.33:
        texto=lib.loc[3,'C'].replace('[1-perc_cons]',str(int((1-percentil)*100)))
        return texto
    elif 0.33<percentil<0.66:
        texto = lib.loc[4, 'C'].replace('[perc_cons]',str(int(percentil*100)))
        return texto
    elif percentil>0.66:
        texto = lib.loc[5, 'C'].replace('[perc_cons]',str(int(percentil*100)))
        return texto