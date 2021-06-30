import pandas as pd

def leerLibreriaCTV():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",sheet_name='libreriaCTV')
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    Dicc = ['A','B', 'C','D','E'] # Define los nombres de las columnas en Excel.
    Libreria.columns = Dicc
    return Libreria
def plural(listDisp):
    if len(listDisp)>1:
        return True
    else:
        return False
def armarTexto():
    lib=leerLibreriaCTV()
    texto=''
    consumoStanby=1
    UPS=True
    if   ((consumoStanby >= 2)==False) and (UPS==False):
        texto=lib.loc[24,'E']
    elif ((consumoStanby >= 2) == False) and (UPS == True ):
        texto='pendiente'
    elif ((consumoStanby >= 2) == True ) and (UPS == False):
        if regulador==False:
            texto=lib.loc[,'E']
    elif ((consumoStanby >= 2) == True ) and (UPS == True ):
        texto='pendiente'
    return texto


