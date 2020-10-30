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


from pathlib         import Path
from Refrigeradores  import refrigerador
from Cluster         import clustertv
from Especiales      import especiales
from Iluminacion     import iluminacion
from Bombas          import bombas
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
    try:
        Excel = pd.read_excel(Path.home() / 'Desktop' / 'Carrera.xlsx' )
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    return Excel

def definirequipos(Excel, Nocircuito):
    indx = 0
    Consum=0
    Columnas = Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("equipos_c_i", case=False)]
    Equipos = Excel[InfoEquipos]
    Circuito1 = Equipos.loc[Nocircuito]
    DatosFun=pd.DataFrame()

    for i in Circuito1:
        if i == 1:
            if indx == 1:
                Datos_CL, Consum = clustertv(Excel,Nocircuito)
                DatosFun = DatosFun.append(Datos_CL, ignore_index=True)

            if indx == 2:
                Datos_RF, Consum = refrigerador(Excel,Nocircuito,)
                DatosFun = DatosFun.append(Datos_RF, ignore_index=True)

            if indx == 3:
                Datos_RF= iluminacion(Excel,Nocircuito)
                DatosFun = DatosFun.append(Datos_RF, ignore_index=True)

            if indx == 4:
                Datos_RF = bombas(Excel, Nocircuito)
                DatosFun = DatosFun.append(Datos_RF, ignore_index=True)

            if indx == 5:
                Datos_ES, Consum = especiales(Excel, Nocircuito)
                DatosFun = DatosFun.append(Datos_ES, ignore_index=True)

            if indx == 6:
                SEGURIDAD()
            if indx == 7:
                AIRESA()
            if indx == 8:
                CALENTADORES()
            if indx == 9:
                ENTRETENIMIENTO()
            if indx == 10:
                COCINA()
            if indx == 11:
                CALEFACCION()
            if indx == 12:
                REGULADORES()
            if indx == 13:
                COMPUTO()
            if indx == 14:
                OTRO()
        indx = indx+ 1

    #print("_____________________________")
    #print(DatosFun)
    Datoss=DatosFun.copy()
    return Datoss
    #MessageBox.showinfo(Datos)  # título, mensaje


###################### MAIN  #####################################
if __name__ == '__main__':
    Excel=abrirexcel()
    pd.set_option('display.max_columns', 10)
    Datosa= pd.DataFrame(columns=['Circuito','Tablero'])
    TotRenglones=len(Excel)
    for i in range(TotRenglones):

    #for i in TableroCircuitos.index.values:
        Nocircuito=i
        largoD = len(Datosa)
        Circuito = Excel.loc[i, ['circuito_c_i']]
        Datosa.loc[i + largoD, ['Circuito']] = Circuito.values
        Tablero = Excel.loc[i, ['tablero_c_i']]
        Datosa.loc[i + largoD, ['Tablero']] = Tablero.values
        Datos = definirequipos(Excel, int(Nocircuito))
        Datosa=Datosa.append(Datos, ignore_index=True)

        Circuito = Excel.loc[i, ['circuito_c_i']]
        Datosa.loc[i+largoD, ['Circuito']] = Circuito.values
    #print(Datosa)
    Datosa.to_excel("output.xlsx")













