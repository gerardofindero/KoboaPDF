import pandas as pd
from scipy.stats import norm
def leerLibreriaPlanchas():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/Planchas/libreria_planchas.xlsx",sheet_name='libreriaPlanchas')
    except:
        Libreria = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Planchas/libreria_planchas.xlsx",
            sheet_name='libreriaPlanchas')

    Dicc = ['A','B', 'C'] # Define los nombres de las columnas en Excel.
    Libreria.columns = Dicc
    return Libreria

def leerConsumoPlanchas(consumo):
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
    # media y desviacion estandar almacenados en el excel de planchas
    # en esta sección se esta trabajdno con la transformación consumo**0.3 (kWh)
    media=statistics.loc[0,'B']
    desStd=statistics.loc[3,'B']
    consumoTrans= consumo**0.3
    percentil= norm.cdf(consumoTrans,loc=float(media),scale=float(desStd))
    percentil=round(percentil,2)
    #print(percentil)
    lib=leerLibreriaPlanchas()
    if percentil <0.33:
        texto=lib.loc[3,'C'].replace('[1-perc_cons]',str(int((1-percentil)*100)))
        return texto
    elif 0.33<=percentil<0.45:
        linkA = links.loc[0, 'C']
        Address = 'Estrategia para planchas'
        LinkS = '<br />' + '<link href="' + str(linkA) + '"color="blue">' + Address + ' </link>'
        texto = lib.loc[4, 'C'].replace('[perc_cons]', str(int(percentil * 100))).replace('{link_blog_planchas}', LinkS)
        return texto
    elif 0.45<=percentil<0.55:
        linkA = links.loc[0, 'C']
        Address = 'Estrategia para planchas'
        LinkS = '<br />' + '<link href="' + str(linkA) + '"color="blue">' + Address + ' </link>'
        texto = lib.loc[5, 'C'].replace('[perc_cons]', str(int(percentil * 100))).replace('{link_blog_planchas}', LinkS)
        return texto
    elif 0.55<=percentil<0.66:
        linkA = links.loc[0, 'C']
        Address = 'Estrategia para planchas'
        LinkS = '<br />' + '<link href="' + str(linkA) + '"color="blue">' + Address + ' </link>'
        texto = lib.loc[6, 'C'].replace('[perc_cons]', str(int(percentil * 100))).replace('{link_blog_planchas}', LinkS)
        return texto
    elif percentil>=0.66:
        linkA = links.loc[0,'C']
        Address = 'Estrategia para planchas'
        LinkS = '<br />'+'<link href="' + str(linkA) + '"color="blue">' + Address + ' </link>'
        texto = lib.loc[7, 'C'].replace('[perc_cons]',str(int(percentil*100))).replace( '{link_blog_planchas}',LinkS )
        return texto



