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
    estadisticas.columns = ['A','B'] # en esta pestaña de la libería se encuentran los parametros estadisticos de consumo de fateras
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
    if numDias == 0:
        txt = ''
    elif numDias == 1:
        txt = 'el día ' + dias[0]
    elif numDias == 2:
        txt = 'los días ' + dias[0] + ' y ' + dias[1]
    elif numDias > 2:
        txt = 'los días'
        for c, dia in enumerate(dias):
            if c < (numDias - 2):
                txt = txt + ' ' + dias[c] + ','
            elif c == (numDias - 2):
                txt = txt + ' ' + dias[c]
            else:
                txt = txt + ' y ' + dias[c]
    return txt




def armarTxtCaf(nombre,kwh, hrsUso,dscr=''):
    """
    Recomendación de cafeteras se hace a partit
    :param nombre: Nombre de la cafetera
    :param kwh:    Consumo de la cafetera al bimestre
    :param hrsUso: Horas de uso a la semana. Proporcionado por analisis
    :param dscr:   Descripción de analisis con los dias de la semana que se utilizó la cafetera
    :return:       Recomendaciones acorde al tipo de carita
    """
    diasUso = dias(dscr)
    KWH=kwh
    [lib, st] = leerLibreriaCafeteras()
    media = st.at[0,'B']
    dstd  = st.at[3,'B']
    kwh = kwh**0.42
    percentil= norm.cdf(kwh,loc=media,scale=dstd)
    txt=''
    print(percentil)
    if percentil <=0.33:
        txt= lib.at[0,'D']
    elif 0.33<percentil<= 0.45:
        txt = lib.at[1, 'D']
    elif 0.45<percentil<=0.55:
        txt = lib.at[2, 'D']
    elif 0.55<percentil<=0.66:
        txt = lib.at[3, 'D']
    elif 0.66<percentil:
        if KWH>35:
            txt = lib.at[5, 'D']
        else:
            txt = lib.at[4, 'D']

    if hrsUso>3:
        texhoras=' Encontramos que la usaste un total de ' +str(hrsUso) +' horas en la semana.'
        txt = txt.replace('[Horas]',texhoras)
    else:
        txt = txt.replace('[Horas]','')

    if 0.55<percentil:
        if nombre == 'tetera':
            txt = txt + lib.at[6, 'D']
        else:
            txt = txt + lib.at[7, 'D']
    if nombre == 'tetera':
        txt = txt.replace('[equipo]','tetera')
    else:
        txt = txt.replace('[equipo]','cafetera')

    txt = txt.replace('[%]',str(int(percentil*100)))
    return txt.replace('[/n]','<br />')#.replace('<br /><br />','<br />')