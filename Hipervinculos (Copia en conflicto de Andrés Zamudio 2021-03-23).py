# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 10:51:38 2021

@author: Findero ANZV GZM

Este programa es parte de la lectura de los datos guardados en Kobo y permite 
generar hipervínculos a la tabla de Desciframiento para optimizar la localización
de los equipos en las gráficas que fueron identificados en la detección de fugas.
"""
#Librerías
import datetime
import os
from datetime import datetime
import pandas as pd
import xlwings
#Definición de la función llamada en la lectura del Kobo
def hipervinculos(Cliente):
    print('Creando hipervinculos')
    fecha = datetime.now()
    meses={'January':'01-Enero','February':'02-Febrero','March':'03-Marzo','April':'04-Abril','May':'05-Mayo','June':'06-Junio','July':'07-Julio',
       'August':'08-Agosto','September':'09-Septiembre','October':'10-Octubre','November':'11-Noviembre','December':'12-Diciembre'}
    mes = fecha.strftime("%B").capitalize()
    print(mes)
    print(meses)
    mes=meses[mes]
    anho = fecha.strftime("%Y")
    ## Se busca el cliente, la carpeta que lo contiene y el archivo de resumen
    carpeta_resultados = f"../../Datos de clientes/Clientes {anho}/{mes}/"
    clientes = os.listdir(carpeta_resultados)
    booleanos = [Cliente.lower() in c.lower() for c in clientes]
    carpeta_cliente = Cliente
    for idx, valor in enumerate(booleanos):
        if valor:
            carpeta_cliente = clientes[idx]
    carpeta_resultados = carpeta_resultados + f"{carpeta_cliente}/Resultados"
    cliente_ = Cliente.replace(' ', '_')
    archivo_resultados = f"{carpeta_resultados}/Resumen_{cliente_}.xlsx"
    Res = pd.read_excel(archivo_resultados, sheet_name='Resumen')
    #Se crean las columnas para el archivo de desciframiento y se asignan 
    Dic = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I','J','K','L','M','N','O','P','Q']
    Dicc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
    Res.columns = Dic
    #Formato y eliminación de renglones que no se utilizan
    Res[['A', 'B']] = Res[['A', 'B']].fillna(method = 'pad')
    Des = pd.read_excel(archivo_resultados, sheet_name='Desciframiento')
    Des.columns = Dicc
    Des.drop([0,1,2,3,4],inplace=True)
    Des.dropna(subset=['C'],inplace=True)
    Res.drop(Res.index[:9], inplace=True)
    Res = Res[Res.A != 'Periodo:']
    Res = Res[Res.B != 'Tablero']
    Des['C'] = Des['C'].str.capitalize()
    circuitoD = Des['C'][Des.C != 'Ubicacion']
    circuitoD = circuitoD.str.split(' ', 1)
    Res.dropna(subset=['D'], inplace=True)
    Res['D'] = Res['D'].astype(str)
    circuitoR = Res[['B', 'D']]
    valorT = len(set(Res['B']))
    V1= Res.loc[8,'H']
    V2= Res.loc[8,'H']
    V3 = Res.loc[8, 'H']
    print(V1)
    circuitoR['B'] = circuitoR['B'].str.lower()
    circuitoR['D'] = circuitoR['D'].str.split().str.get(0)
    workbook = xlwings.Book(archivo_resultados)
    Sheet1 = workbook.sheets['Desciframiento']
    for i in circuitoD.index:
        try:
            circ=int(circuitoD[i][0][1:])
            tab = circuitoD[i][1][0:]
            donde = circuitoR[int(circuitoR) == circ].index 
            
        except:
            circ = circuitoD[i][0][1:]
            tab = circuitoD[i][1][0:]
            donde = circuitoR[circuitoR== circ].index
        if valorT > 3:
            if not donde.empty:
                for j in donde.values:
                    if circuitoR['B'][j]==tab and circuitoR['D'][j]==circ:
                        Puerto =Res['C'][j]
                        Findero=Res['A'][j]
                        Hvin= '../Graficas/Consumo/'+ str(Findero) +'/'  + str(Findero) +'Puerto ' + str(Puerto) +'.html'
                        Sheet1.range(i+2,3).add_hyperlink(Hvin,str(Des.loc[i,'C']))
        else:
           if not donde.empty:
               for j in donde.values:
                   if circuitoR['D'][j]==circ:
                       Puerto =Res['C'][j]
                       Findero=Res['A'][j]
                       Hvin= '../Graficas/Consumo/'+ str(Findero) +'/'  + str(Findero) +'Puerto ' + str(Puerto) +'.html'
                       Sheet1.range(i+2,3).add_hyperlink(Hvin,str(Des.loc[i,'C']))




    workbook.save()
    workbook.close()