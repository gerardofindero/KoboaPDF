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

    #Dicc = ['A','B', 'C','D'] # Define los nombres de las columnas en Excel.
    #Libreria.columns = Dicc
    return Libreria

def leerConsumoPlanchas(consumo, hrsUso=None):
    """
    Librería de planchas normales
    :param consumo: Consumo de kwh  al bimestre
    :param hrsUso:  Número de horas usao a la semana
    :return:
    """
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
    # en esta sección se esta trabajando con la transformación consumo**0.3 (kWh)
    media=statistics.loc[0,'B']   # media de la distribución normalizada
    desStd=statistics.loc[3,'B']  # desviación estandar de la distribucón
    consumoTrans= consumo**0.3
    percentil= norm.cdf(consumoTrans,loc=float(media),scale=float(desStd))
    percentil=round(percentil,2)
    lib=leerLibreriaPlanchas()
    Addres = 'Estrategia para planchas'
    Link   = links.loc[0, 'C']

    texto=''

    if (not (hrsUso is None)) and (not hrsUso==0 )and consumo> 33:
        texto = fc.selecTxt(lib,"test04")
    # Persentil de consumo
    if consumo <= 19:
        texto = fc.selecTxt(lib,"test01")
    elif (consumo > 19) and (consumo<=33):
        texto = fc.selecTxt(lib,"test02")
    elif consumo>33:
        texto = fc.selecTxt(lib,"test03")
        
    texto =  texto.replace('[perc_cons]',str(int(percentil*100))).replace('[link_blog_planchas]', fc.ligarTextolink(Addres,Link))
    texto =  texto.replace('[1-perc_cons]',str(int(percentil*100))).replace('[perc_cons]',str(int(percentil*100))).replace('{link_blog_planchas}', fc.ligarTextolink(Addres,Link))
    texto =  texto.replace('[1-perc_cons]',str(int(percentil*100))).replace('[perc_cons]',str(int(percentil*100))).replace('{link_blog_planchas}', fc.ligarTextolink(Addres,Link))
    texto =  texto.replace('\n','<br />')
    return texto



