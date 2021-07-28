import pandas as pd
import numpy  as np


def ligarTextolink(texto, link):
    """
    Ligar link a texto, no hace nada si el link esta vacio
    :param texto: Texto al cual se quiere ligar el link
    :param link:  Link de la pagina
    :return: cadena de texto original o cadena con el texto ligado al hipervinculo
    """
    #print(link)
    if (link == 'nan') or (link == '') or np.isnan(link):
        return texto
    else:
        texto = '<br />' + '<link href="' + link + '"color="blue">' + texto + ' </link>'
        return texto
def dias(dscr):
    """
    Forma el texto con los días que se utilizó el dispositivo a partir de la descripción del deciframiento.
    :param dscr: texto recuperado de la descripción del deciframiento
    :return: texto correspondiente a los días que se utilizo el dispositivo
    """
    dias = []
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
    numDias = len(dias)
    txt = ''
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

def listarComas(lista):
    n = len(lista)
    if n == 0:
        return ''
    elif n == 1:
        return lista[0]
    elif n == 2:
        return  lista[0]+' y '+ lista[1]
    elif n>2:
        txt=''
        for c, cosa in enumerate(lista):
            if c < (n-2):
                txt= txt + ' '+ lista[c]+','
            elif c == (c-2):
                txt = txt +  ' ' + lista[c]
            else:
                txt = txt + ' y ' + lista[c]
        return txt

def selecTxt(df,codigo):
    index = df.index[df.Codigo == codigo][0]
    txt   = df.at[index,'Texto']
    return txt

def checarROI(df):
    df.sort_values(by=['ahorroBimestral', 'roi'], ascending=[False, True])
    if (df.roi<3).any():
        return [True,
                df.loc[df.roi<3,:].reset_index(drop=True).loc[:5,:].copy()]
    else:
        return [False,
                df.reset_index(drop=True).loc[:5, :].copy()]
