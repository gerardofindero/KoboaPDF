# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 10:51:38 2021

@author: Findero ANZV GZM

Este programa es parte de la lectura de los datos guardados en Kobo y permite 
generar hipervínculos a la tabla de Desciframiento para optimizar la localización
de los equipos en las gráficas que fueron identificados en la detección de fugas.
"""
#Librerías
import os
from datetime import datetime
import pandas as pd
import xlwings
from Carpeta_Clientes import carpeta_clientes


#Definición de la función llamada en la lectura del Kobo
def hipervinculos(Cliente):
    print('Creando hipervinculos')
    meses={'1':'01-Enero','2':'02-Febrero','3':'03-Marzo','4':'04-Abril','5':'05-Mayo','6':'06-Junio','7':'07-Julio',
       '8':'08-Agosto','9':'09-Septiembre','10':'10-Octubre','11':'11-Noviembre','12':'12-Diciembre'}
    #Se crea el diccionario de meses y se obtiene la fecha actual del sistema desde donde se corre el script.

    archivo_resultados = carpeta_clientes(Cliente)
    Res = pd.read_excel(archivo_resultados, sheet_name='Resumen')
    #Se crean las columnas para el archivo de desciframiento y se asignan 
    Dic = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I','J','K','L','M','N','O','P','Q']
    Dicc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
    Res.columns = Dic
    #Formato general y eliminación de renglones que no se utilizan
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
    circuitoR['B'] = circuitoR['B'].str.lower()
    circuitoR['D'] = circuitoR['D'].str.split().str.get(0)
    workbook = xlwings.Book(archivo_resultados)
    Sheet1 = workbook.sheets['Desciframiento']
    #Asignación de los hipervínculos por tablero y circuitos a la hoja de desciframiento
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
                   if circuitoR['B'][j]==tab and circuitoR['D'][j]==circ:
                       Puerto =Res['C'][j]
                       Findero=Res['A'][j]
                       Hvin= '../Graficas/Consumo/'+ str(Findero) +'/'  + str(Findero) +'Puerto ' + str(Puerto) +'.html'
                       Sheet1.range(i+2,3).add_hyperlink(Hvin,str(Des.loc[i,'C']))
    workbook.save()
    workbook.close()