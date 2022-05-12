import datetime
import os
from datetime import datetime

def carpeta_clientes(Cliente):

    fecha = datetime.now()
    mes = fecha.strftime("%B").capitalize()
    anho = fecha.strftime("%Y")
    carpeta_resultados=' '
    Cl=''
    try:
        #carpeta_resultados = f"../../../Datos de clientes/Clientes {anho}/11-noviembre/"
        #carpeta_resultados = f"../../../Datos de clientes/Clientes 2021/12-diciembre/"
        carpeta_resultados = f"../../../Datos de clientes/Clientes 2022/04-abril/"
        #carpeta_resultados = f"../../../Datos de clientes/Clientes {anho}/03-marzo/"
        clientes = os.listdir(carpeta_resultados)
        if 'Bot_' in Cliente:
            Cl=Cliente
            Cliente='Cliente Prueba'

        booleanos = [Cliente.lower() in c.lower() for c in clientes]


    except:
        #carpeta_resultados = f"D:/Findero Dropbox/Datos de clientes/Clientes {anho}/11-noviembre/"
        #carpeta_resultados = f"D:/Findero Dropbox/Datos de clientes/Clientes {anho}/03-marzo/"
        carpeta_resultados = f"D:/Findero Dropbox/Datos de clientes/Clientes 2022/04-abril/"

        clientes = os.listdir(carpeta_resultados)
        Cl=''
        if 'Bot_' in Cliente:
            Cl=Cliente
            Cliente='Cliente Prueba'

        booleanos = [Cliente.lower() in c.lower() for c in clientes]

    carpeta_cliente = Cliente
    for idx, valor in enumerate(booleanos):
        if valor:
            carpeta_cliente = clientes[idx]
    carpeta_resultados = carpeta_resultados + f"{carpeta_cliente}/Resultados"

    cliente_ = Cliente.replace(' ', '_')
    if 'Bot_' in Cl:
        cliente_=Cl
    archivo_resultados = f"{carpeta_resultados}/Resumen_{cliente_}.xlsx"

    return archivo_resultados

def carpeta_clientes_Imagenes(Cliente):
    Cl=''
    try:
        #carpeta_resultados = f"../../../Datos de clientes/Clientes 2021/12-diciembre/"
        #carpeta_resultados = f"../../../Datos de clientes/Clientes 2022/03-marzo/"
        carpeta_resultados = f"../../../Datos de clientes/Clientes 2022/04-abril/"
        clientes = os.listdir(carpeta_resultados)
        if 'Bot_' in Cliente:
            Cl=Cliente
            Cliente='Cliente Prueba'

        booleanos = [Cliente.lower() in c.lower() for c in clientes]


    except:
        #carpeta_resultados = f"D:/Findero Dropbox/Datos de clientes/Clientes 2022/03-marzo/"
        carpeta_resultados = f"D:/Findero Dropbox/Datos de clientes/Clientes 2022/04-abril/"


        clientes = os.listdir(carpeta_resultados)
        Cl=''
        if 'Bot_' in Cliente:
            Cl=Cliente
            Cliente='Cliente Prueba'
        booleanos = [Cliente.lower() in c.lower() for c in clientes]
    carpeta_cliente = Cliente
    for idx, valor in enumerate(booleanos):
        if valor:
            carpeta_cliente = clientes[idx]
    carpeta_resultados = carpeta_resultados + f"{carpeta_cliente}/Imagenes/V1.png"

    return carpeta_resultados