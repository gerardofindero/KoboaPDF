import pandas as pd

def leerLibreriaCafeteras():
    try:
        libreria = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/cafeteras/libreriaCafeteras.xlsx",
            sheet_name='libreriaCafeteras')
    except:
        libreria = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/cafeteras/libreriaCafeteras.xlsx",
            sheet_name='libreriaCafeteras')



    return [libreria]


def dias(dscr):
    txt=''
    dias=[]
    numDias=0
    if ('lunes' in dscr) or ('Lunes' in dscr):
        dias.append('lunes')
    if ('Martes' in dscr) or ('martes' in dscr):