import datetime
import os
from datetime import datetime
import pandas as pd

def leer_lista(Cliente):
    fecha = datetime.now()
    mes = fecha.strftime("%B").capitalize()
    anho = fecha.strftime("%Y")
    #carpeta_resultados = f"../../Datos de clientes/Clientes {anho}/01-enero/"
    #carpeta_resultados = f"../../Datos de clientes/Clientes {anho}/03-Marzo/"
    carpeta_resultados = f"D:/Findero Dropbox/Datos de clientes/Clientes 2021/03-Marzo/"
    clientes = os.listdir(carpeta_resultados)
    booleanos = [Cliente.lower() in c.lower() for c in clientes]
    carpeta_cliente = Cliente
    for idx, valor in enumerate(booleanos):
        if valor:
            carpeta_cliente = clientes[idx]
    carpeta_resultados = carpeta_resultados + f"{carpeta_cliente}/Resultados"

    cliente_ = Cliente.replace(' ', '_')
    archivo_resultados = f"{carpeta_resultados}/Resumen_{cliente_}.xlsx"
    Exx = pd.read_excel(archivo_resultados, sheet_name='Lista')
    print(Exx)
    Dic = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    Exx.columns = Dic
    Exx.fillna('0',inplace=True)
    #print(Exx[Exx['A'].str.contains('Circuito')])


    infoL=Exx.drop(['A','C','E','G'],axis=1)
    infoL=infoL.drop(0)

    #print(infoL)
    return infoL