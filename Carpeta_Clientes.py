import datetime
import os
from datetime import datetime

def carpeta_clientes(Cliente):

    fecha = datetime.now()
    mes = fecha.strftime("%B").capitalize()
    anho = fecha.strftime("%Y")
    carpeta_resultados=' '
    try:
        carpeta_resultados = f"../../../Datos de clientes/Clientes {anho}/11-noviembre/"
        #carpeta_resultados = f"../../../Datos de clientes/Clientes {anho}/10-octubre/"
        clientes = os.listdir(carpeta_resultados)
        if 'Bot_' in Cliente:
            Cl=Cliente
            Cliente='Cliente Prueba'

        booleanos = [Cliente.lower() in c.lower() for c in clientes]


    except:
        try:
            carpeta_resultados = f"D:/Findero Dropbox/Datos de clientes/Clientes {anho}/11-noviembre/"
         # la linea de abajo se habilito para que funcione en la computadora de Andres, PONER TRY EXCEPT, DUDESSSS!!!! Atte Hercules.
        except:
            carpeta_resultados = f"C:/Users/finde/Findero Dropbox/Datos de clientes/Clientes {anho}/11-noviembre/"
        # carpeta_resultados = f"D:/Findero Dropbox/Datos de clientes/Clientes {anho}/11-noviembre/"
        #carpeta_resultados = f"D:/Findero Dropbox/Datos de clientes/Clientes {anho}/10-octubre/"
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
    print(archivo_resultados)

    return archivo_resultados