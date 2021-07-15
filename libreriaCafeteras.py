import pandas as pd
from scipy.stats import norm

def leerLibreriaCafeteras():
    try:
        libreria = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/cafeteras/libreriaCafeteras.xlsx",
            sheet_name='libreriaCafeteras')
        estadisticas= pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/cafeteras/libreriaCafeteras.xlsx",
            sheet_name='statistics')
    except:
        libreria = pd.read_excel(
             f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/cafeteras/libreriaCafeteras.xlsx",
            sheet_name='libreriaCafeteras')
        estadisticas = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/cafeteras/libreriaCafeteras.xlsx",
            sheet_name='statistics')
    libreria.columns = ['A','B','C','D']
    estadisticas.columns = ['A','B']
    print(libreria)
    print(estadisticas)
    return [libreria, estadisticas]


def dias(dscr):
    txt=''
    dias=[]
    numDias=0
    if ('lunes' in dscr) or ('Lunes' in dscr):
        dias.append('lunes')
    if ('Martes' in dscr) or ('martes' in dscr):
        dias.append('martes')
    if ('Miercoles' in dscr) or ('miercoles' in dscr):
        dias.append('miercoles')
    if ('Jueves' in dscr) or ('jueves' in dscr):
        dias.append('jueves')
    if ('Viernes' in dscr) or ('viernes' in dscr):
        dias.append('viernes')
    if ('Sábado' in dscr) or ('sabado' in dscr) or ('Sabado' in dscr) or ('sabado' in dscr):
        dias.append('sábado')
    if ('Domingo' in dscr) or ('domingo' in dscr):
        dias.append('domingo')
    numDias=len(dias)
    txt=''
    if numDias==0:
        txt=''
    elif numDias==1:
        txt=''+txt.replace(dias[0],1)




def armarTxtCaf(kwh, hrsUso,dscr):
    [lib, st] = leerLibreriaCafeteras()
    media = st.at[0,'B']
    dstd  = st.at[1,'B']
    kwh = kwh**0.42
    percentil= norm.cdf(kwh,loc=media,scale=dstd)
    txt=''
    if percentil <=0.33:
        txt=txt+lib.at[0,'C']
    elif 0.33<percentil<= 0.45:
        txt = txt + lib.at[1, 'C']
    elif 0.45<percentil<=0.55:
        txt = txt + lib.at[2, 'C']
    elif 0.55<percentil<=0.66:
        txt = txt + lib.at[3, 'C']
    elif 0.66<percentil:
        txt = txt + lib.at[4, 'C']
    txt=txt.replace('[diasUso]',dias(dscr)).replace('[totalHoras]',int(hrsUso)) # se utilizó .... los días **** o todos los días
    return txt