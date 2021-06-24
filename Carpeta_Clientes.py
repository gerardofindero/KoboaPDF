import datetime
import os
from datetime import datetime

def carpeta_clientes(Cliente):

    fecha = datetime.now()
    mes = fecha.strftime("%B").capitalize()
    anho = fecha.strftime("%Y")
    try:
        carpeta_resultados = f"../../../Datos de clientes/Clientes {anho}/06-junio/"
        clientes = os.listdir(carpeta_resultados)
        booleanos = [Cliente.lower() in c.lower() for c in clientes]
    except:
        carpeta_resultados = f"D:/Findero Dropbox/Datos de clientes/Clientes {anho}/06-junio/"

        clientes = os.listdir(carpeta_resultados)
        booleanos = [Cliente.lower() in c.lower() for c in clientes]
    carpeta_cliente = Cliente
    for idx, valor in enumerate(booleanos):
        if valor:
            carpeta_cliente = clientes[idx]
    carpeta_resultados = carpeta_resultados + f"{carpeta_cliente}/Resultados"

    cliente_ = Cliente.replace(' ', '_')
    archivo_resultados = f"{carpeta_resultados}/Resumen_{cliente_}.xlsx"

    return archivo_resultados