import pandas as pd
from scipy.stats import norm
def leerLibreriaMicroondas():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/Microondas/libreria_microondas.xlsx",sheet_name='libreriaMicroondas')
    except:
        Libreria = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Microondas/libreria_microondas.xlsx",
            sheet_name='libreriaMicroondas')

    Dicc = ['A','B', 'C','D'] # Define los nombres de las columnas en Excel.
    Libreria.columns = Dicc
    return Libreria

def leerConsumoMicroondas(consumo, hrsUso=None):
    try:
        statistics = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Microondas/libreria_microondas.xlsx",
            sheet_name='statistics')
    except:
        statistics = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Microondas/libreria_microondas.xlsx",
            sheet_name='statistics')
    Dicc = ['A', 'B', 'C','D','F']  # Define los nombres de las columnas en Excel.
    statistics.columns = Dicc
    # media y desviacion estandar almacenados en el excel de libreria_microondas.xlsx
    # en esta sección se esta trabajdno con la transformación consumo**0.4 (kWh)
    media=statistics.loc[0,'B']
    desStd=statistics.loc[3,'B']
    consumoTrans= consumo**0.4
    percentil= norm.cdf(consumoTrans,loc=float(media),scale=float(desStd))
    percentil=round(percentil,2)
    lib=leerLibreriaMicroondas()
    col='D'
    texto = ''

    if (not (hrsUso is None)) and(hrsUso!=0)and(percentil>=0.45):
        print('entre')
        texto= texto + lib.loc[3,col].replace('[horasUso]',str(hrsUso)) +' '

    if percentil <0.33:
        texto= texto+lib.loc[4,col]

    elif 0.33<=percentil<0.45:
        texto =texto +lib.loc[5, col]

    elif 0.45<=percentil<0.55:
        texto = texto +lib.loc[6, col]

    elif 0.55<=percentil<0.66:
        texto = texto +lib.loc[7, col]

    elif 0.66<=percentil<0.97:
        texto = texto +lib.loc[8, col]
    elif percentil>=0.97:
        texto = texto +lib.loc[9, col]
    texto = texto.replace('[1-perc_cons]',str(int((1-percentil)*100))).replace('[perc_cons]',str(int(percentil*100)))
    return texto