import pandas as pd
import numpy  as np
import unicodedata
import csv
import codecs
import urllib.request
import urllib.error
import sys
import requests
from io import StringIO
from datetime import date
import os
def ligarTextolink(texto, link):
    """
    Ligar link a texto, no hace nada si el link esta vacio
    :param texto: Texto al cual se quiere ligar el link
    :param link:  Link de la pagina
    :return: cadena de texto original o cadena con el texto ligado al hipervinculo
    """
    if pd.isna(link) or (link == ''):# or np.isnan(link):
        return texto
    else:
        texto = '<link href="' + link + '"color="blue">' + texto + ' </link>'
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
            if c < (n-1):
                txt= txt + ' '+ lista[c]+','
            elif c == (c-1):
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
def formStrig(txt):
    txt = txt.lower()
    nfkd = unicodedata.normalize("NFKD", txt)
    lugar = nfkd.encode("ASCII", 'ignore')
    lugar = lugar.decode("utf-8")
    return txt

def formDFstring(df):
    df= df.str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    return df

def dataClima(CP,Country="mexico",DefaultPeriod=True,StartDate="",EndDate="",Period="last7days", ApiKey = '68YK8W8YZCXYZMPNPJMJFTLHX'):
    """
    DATE INFO
    Optional start and end dates
    If nothing is specified, the forecast is retrieved.
    If start date only is specified, a single historical or forecast day will be retrieved
    If both start and and end date are specified, a date range will be retrieved
    Parameters
    ----------
    CP             Postal Code - string of 5 digits
    Country        Actual Country - string
    DefaultPeriod  Pivot variable to retrive last 7 days data or use StartDate and EndDate
    StartDate      string format YYYY-MM-DD
    EndDate        string format YYYY-MM-DD
    Period         string by default
    ApiKey         by default use my personal account key

    Returns
    -------
    df : data frame with weather data (feelslike) data have linear interpol to fill NaN
    """
    today = date.today()
    ad = today.strftime("%b-%d-%Y")
    # set-up
    # Base string for query
    BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
    # UnitGroup sets the units of the output - us or metric
    UnitGroup = 'metric'
    # Location for the weather data
    Location = CP+","+Country
    # JSON or CSV
    # JSON format supports daily, hourly, current conditions, weather alerts and events in a single JSON package
    # CSV format requires an 'include' parameter below to indicate which table section is required
    ContentType = "csv"
    # include sections
    # values include days,hours,current,alerts
    Include = "hours"
    #ApiQuery = BaseURL + Location +"?key="+ApiKey
    ApiQuery = BaseURL + Location

    if DefaultPeriod:
        ApiQuery += "/"+Period
    else:
        if (len(StartDate)):
            ApiQuery += "/" + StartDate
            if (len(EndDate)):
                ApiQuery += "/" + EndDate

    ApiQuery += "?"
    ApiQuery += "&unitGroup="   + UnitGroup
    ApiQuery += "&contentType=" + ContentType
    ApiQuery += "&include="     + Include
    ApiQuery += "&key="         + ApiKey

    fileName =CP+"_"+Country+"_"+ad+".csv"
    path=None
    path1=f"D:/Findero Dropbox/Datos de Consultas/Datos Meteorologicos"
    path2=f"../../../Datos de Consultas/Datos Meteorologicos"
    if os.path.exists(path1):
        path=path1
    elif os.path.exists(path2):
        path=path2
    #print("Rutas para datos climaticos: ",path)
    #print(os.listdir(path))
    #print(fileName in os.listdir(path))
    if (fileName) in os.listdir(path):
        print("LEYENDO INFORMACIÓN CLIMATICA DESDE LA RUTA-> ",path)
        df = pd.read_csv(path+"/"+fileName)

    else:
        print(' - CORRIENDO QUERY AL URL: ', ApiQuery,"\n")
        r = requests.get(ApiQuery)
        df = pd.read_csv(StringIO(r.text))
        df["feelslike"] = df["feelslike"].interpolate(method="linear", limit_direction="both")
        df.to_csv((path+"/"+fileName),index=False)


    return df