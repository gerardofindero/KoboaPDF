import pandas as pd
from scipy.stats import norm
import funcionesComunes as fc
def leerLibreriaPlanchas():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/Planchas/libreria_planchas.xlsx",sheet_name='libreriaPlanchas')
    except:
        Libreria = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Planchas/libreria_planchas.xlsx",
            sheet_name='libreriaPlanchas')

    Dicc = ['A','B', 'C','D'] # Define los nombres de las columnas en Excel.
    Libreria.columns = Dicc
    return Libreria

def leerConsumoPlanchas(consumo, hrsUso=None):
    try:
        statistics = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Planchas/libreria_planchas.xlsx",
            sheet_name='statistics')
        links   = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Planchas/libreria_planchas.xlsx",
            sheet_name='links')
    except:
        statistics = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Planchas/libreria_planchas.xlsx",
            sheet_name='statistics')
        links   = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Planchas/libreria_planchas.xlsx",
            sheet_name='links')
    statistics.columns = ['A', 'B', 'C','D']  # Define los nombres de las columnas en Excel.
    links.columns =  ['A','B','C']
    col = 'D'
    # media y desviacion estandar almacenados en el excel de planchas
    # en esta sección se esta trabajdno con la transformación consumo**0.3 (kWh)
    media=statistics.loc[0,'B']
    desStd=statistics.loc[3,'B']
    consumoTrans= consumo**0.3
    percentil= norm.cdf(consumoTrans,loc=float(media),scale=float(desStd))
    percentil=round(percentil,2)
    print(percentil)
    #print(percentil)
    lib=leerLibreriaPlanchas()
    Addres = 'Estrategia para planchas'
    Link   = links.loc[0, 'C']

    texto=''
    if (not (hrsUso is None)) and (not hrsUso==0 )and percentil>= 0.45:
        texto = texto + lib.loc[3,col].replace('[horasUso]',str(hrsUso))

    if percentil <0.33:
        texto=lib.loc[4,col]
    elif 0.33<=percentil<0.45:
        texto = texto + ' '+lib.loc[5, col]
    elif 0.45<=percentil<0.55:
        texto = texto + ' '+lib.loc[6, col]
    elif 0.55<=percentil<0.66:
        texto = texto + ' '+lib.loc[7, col]
    elif percentil>=0.66:
        texto = texto + ' '+lib.loc[8, col]

    texto =  texto.replace('[perc_cons]',str(int(percentil*100))).replace('{link_blog_planchas}', fc.ligarTextolink(Addres,Link))

    texto =  texto.replace('\n','<br />')
    return texto



