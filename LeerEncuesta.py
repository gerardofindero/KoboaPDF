import pandas as pd
import re
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from tkinter import *
from tkinter import messagebox as MessageBox
from pandas import ExcelWriter
from pathlib import Path

from pathlib         import Path
from Refrigeradores  import refrigerador
from Cluster         import clustertv
from Especiales      import especiales
from Iluminacion     import iluminacion
from Bombas          import bombas
from Lavanderia      import lavanderia
from Cocina          import cocina
from Calentadores    import calentadores
from pdf             import CrearPDF
from Deciframiento   import Archivo


from Condiciones import condicionesRefrigeracion
####################  FUNCIONES ###################################

### SE LLAMA A LAS FUNCIONES CORRESPONDIENTES
def SEGURIDAD():
    print("Seguridad ")
def AIRESA():
    print("Aire Acondicionado ")
def CALENTADORES():
    print("Calentadores ")
def ENTRETENIMIENTO():
    print("Entretenimiento ")
def COCINA():
    print("Cocina ")
def CALEFACCION():
    print("Calefaccion ")
def REGULADORES():
    print("Reguladores ")
def COMPUTO():
    print("Computo ")
def OTRO():
    print("Otro ")

def abrirexcel():
    #print("Como se llama el archivo de fugas")
    #nombrearchivo=str(input())
    #nombre = nombrearchivo+".xlsx"







    Cliente='Manuel Uribe'





    ClientEx=Cliente.replace(' ','_')
    ClientEx=ClientEx +'.xlsx'
    try:
        Excel = pd.read_excel(Path.home() / 'Desktop' /ClientEx )
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    return Excel,Cliente

def definirequipos(Excel, Nocircuito,NomCircuito,tablero,primafila,FilaLib):
    indx = 0
    Consum=0
    Columnas = Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("equipos_c_i", case=False)]
    Equipos = Excel[InfoEquipos]
    Circuito1 = Equipos.loc[Nocircuito]
    #Circuito1.dropna(inplace = True)
    DatosFun=pd.DataFrame()
    DatosCL = pd.DataFrame()
    Fugas = pd.DataFrame(columns=['Tablero','Circuito','Marca','Consumo'])
    nombre='C.'+ str(NomCircuito[0])
    pdcir=pd.DataFrame(columns= [str(tablero[0]), nombre ])
    pdcir.to_excel(writer ,index=False,startrow=primafila-1)
    #print(Circuito1)

    for j in Circuito1:
        if j == 1:
            if indx == 1:
                print("Cluster ")
                Datos_CL, Consum ,Codigo , Notas = clustertv(Excel,Nocircuito,NomCircuito)
                DatosFun = DatosFun.append(Notas, ignore_index=True)
                DatosFun = DatosFun.append(Datos_CL, ignore_index=True)
                DatosCL = DatosCL.append(Notas, ignore_index=True)
                DatosCL = DatosCL.append(Datos_CL, ignore_index=True)
                Datos_CL.to_excel(writer,  index=True,startrow=primafila)
                primafila = primafila+ len(Datos_CL) + 4
                Codigo.to_excel(writer, sheet_name='Libreria', index=True, startrow=FilaLib)

                Fugas = Fugas.append(Datos_CL, ignore_index=True)

                FilaLib += 2

            if indx == 2:
                print("Refrigeracion")
                Datos_RF, Consum = refrigerador(Excel,Nocircuito,NomCircuito)
                DatosFun = DatosFun.append(Datos_RF, ignore_index=True)

                Datos_RF.to_excel(writer, index=True,startrow=primafila)
                primafila = primafila+len(Datos_RF) + 4
                Codigo = condicionesRefrigeracion(Datos_RF)
                Codigo.to_excel(writer, sheet_name='Libreria', index=True,startrow=FilaLib)
                FilaLib += 2

            if indx == 3:
                print("Iluminacion ")
                Datos_IL= iluminacion(Excel,Nocircuito)
                DatosFun = DatosFun.append(Datos_IL, ignore_index=True)

                Datos_IL.to_excel(writer,  index=True,startrow=primafila)
                primafila = primafila+len(Datos_IL) + 4

            if indx == 4:
                print("Bombas ")
                Datos_Bb = bombas(Excel, Nocircuito)
                DatosFun = DatosFun.append(Datos_Bb, ignore_index=True)
                Datos_Bb.to_excel(writer, index=True, startrow=primafila)
                primafila = primafila + len(Datos_Bb) + 4

            if indx == 5:
                print("Cocina")
                Datos_CN = cocina(Excel, Nocircuito,NomCircuito)
                DatosFun = DatosFun.append(Datos_CN, ignore_index=True)
                Datos_CN.to_excel(writer, index=True ,startrow=primafila)
                primafila = primafila+len(Datos_CN) + 4

            if indx == 6:
                print("Lavanderia")
                Datos_LV = lavanderia(Excel, Nocircuito,NomCircuito)
                DatosFun = DatosFun.append(Datos_LV, ignore_index=True)
                Datos_LV.to_excel(writer, index=True ,startrow=primafila)
                primafila = primafila+len(Datos_LV) + 4

            if indx == 7:
                print("Calentadores")
                Datos_Cal = calentadores(Excel, Nocircuito,NomCircuito)
                DatosFun  = DatosFun.append(Datos_Cal, ignore_index=True)
                Datos_Cal.to_excel(writer, index=True, startrow=primafila)
                primafila = primafila + len(Datos_Cal) + 4

            if indx == 8:
                print("Solar")

            if indx == 9:
                print("Especiales")
                Datos_ES, Consum = especiales(Excel, Nocircuito,NomCircuito)
                DatosFun = DatosFun.append(Datos_ES, ignore_index=True)
                Datos_ES.to_excel(writer, index=True,startrow=primafila)
                primafila = primafila+len(Datos_ES) + 4

            if indx == 10:
                COMPUTO()

            if indx == 11:
                SEGURIDAD()
            if indx == 12:
                AIRESA()

            if indx == 13:
                ENTRETENIMIENTO()

            if indx == 14:
                REGULADORES()

        indx = indx+ 1

        #Datos.to_excel(writer, sheet_name=NomCircuito, index=True)
    #print("_____________________________")
    Fugas = Fugas[Fugas['Consumo'] != 0]
    Fugas.dropna(subset=['Consumo'], inplace = True)
    NOM=str(NomCircuito[0])
    Fugas['Circuito'].fillna(NOM, inplace = True)
    Fugas['Tablero'].fillna(tablero[0], inplace=True)
    Datoss=DatosFun.copy()
    return Datoss, primafila, FilaLib,Fugas
    #MessageBox.showinfo(Datos)  # título, mensaje


###################### MAIN  #####################################
if __name__ == '__main__':
    Excel, Cliente=abrirexcel()

    #cirr = Excel['circuito_c_i']
    #sorted(cirr, key=lambda x: int("".join([i for i in x if i.isdigit()])))
    #Excel.sort_values(by=['circuito_c_i'])


    pd.set_option('display.max_columns', 15)
    Datosa= pd.DataFrame(columns=['Circuito','Tablero'])
    FugasT = pd.DataFrame()
    TotRenglones=len(Excel)
    Nombre='Kobo_'+ Cliente +'.xlsx'
    writer = ExcelWriter(Path.home() / 'Desktop' / Nombre , engine='xlsxwriter')
    fila=3
    filaLib=0
    for i in range(TotRenglones):
    #i=0
        Nocircuito=i
        largoD = len(Datosa)
        Circuito = Excel.loc[i, ['circuito_c_i']]
        Datosa.loc[i + largoD, ['Circuito']] = Circuito.values
        Tablero = Excel.loc[i, ['tablero_c_i']]
        if Tablero[0]=='otro':
            Tablero = Excel.loc[i, ['tablero_otro_c_i']]

        Datosa.loc[i + largoD, ['Tablero']] = Tablero.values

        Datos, fila, filaLib, Fugas= definirequipos(Excel, int(Nocircuito),Circuito,Tablero,fila,filaLib)

        Datosa =Datosa.append(Datos, ignore_index=True)

        Circuito = Excel.loc[i, ['circuito_c_i']]
        Datosa.loc[i+largoD, ['Circuito']] = Circuito.values

        FugasT = FugasT.append(Fugas, ignore_index=True)

        #nombre='C.'+ str(Circuito[0])
    ##print(FugasT)
    #Archivo(Cliente)
    CrearPDF()
    writer.save()
    #print(Datosa)














