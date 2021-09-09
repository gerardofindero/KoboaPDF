import pandas as pd
import numpy as np
from scipy import stats
import math
from pandas import ExcelWriter
from pathlib         import Path
from PDF             import CrearPDF
from Deciframiento   import Archivo
from Hipervinculos   import hipervinculos
from Ahorro          import potencial_ahorro2
from Leer_Deciframiento import leer_deciframiento, leer_solar,leer_potencial
from DesgloseEquipos import definirequipos
from Condiciones import condicionesLuces
from LibreriaLED import BuscarLED
####################  FUNCIONES ###################################
def abrirexcel(Cliente):
    ClientEx=Cliente.replace(' ','_')
    ClientEx=ClientEx +'.xlsx'
    try:
        Excel = pd.read_excel(Path.home() / 'Desktop' /ClientEx )
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    return Excel,Cliente

def Crear_Kobo(NCliente):
    Excel, Cliente=abrirexcel(NCliente)
    Ilum  = pd.DataFrame()
    Clust = pd.DataFrame()
    Coci  = pd.DataFrame()
    Comu  = pd.DataFrame()
    Esp   = pd.DataFrame()
    Lava  = pd.DataFrame()
    Refri = pd.DataFrame()
    Bomba = pd.DataFrame()
    PCs    = pd.DataFrame()
    Cal    = pd.DataFrame()
    Aire   = pd.DataFrame()
    Segu = pd.DataFrame()
    Nota = pd.DataFrame()

    pd.set_option('display.max_columns', 15)
    Datosa= pd.DataFrame(columns=['Circuito','Tablero'])
    FugasT = pd.DataFrame()
    TotRenglones=len(Excel)
    Nombre='Kobo_'+ Cliente +'.xlsx'
    print(Nombre)
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
        Datos, fila, filaLib, Fugas, ilum, clust, coci, comu,esp,lava,refri,\
        bomba,pcs,cal,segu,aires,notass= definirequipos(Excel, int(Nocircuito),Circuito,Tablero,fila,filaLib,writer)

        Ilum  =  Ilum.append(ilum)
        Clust =  Clust.append(clust)
        Coci  =  Coci.append(coci)
        Comu  =  Comu.append(comu)
        Esp   =  Esp.append(esp)
        Lava  =  Lava.append(lava)
        Refri =  Refri.append(refri)
        Bomba =  Bomba.append(bomba)
        PCs   =  PCs.append(pcs)
        Cal = Cal.append(cal)
        Segu = Segu.append(segu)
        Aire = Aire.append(aires)
        Nota=Nota.append(notass)
        Datosa =Datosa.append(Datos, ignore_index=True)
        print(Esp)
        Circuito = Excel.loc[i, ['circuito_c_i']]
        Datosa.loc[i+largoD, ['Circuito']] = Circuito.values
        FugasT = FugasT.append(Fugas, ignore_index=True)
    writer.save()
    Tluz=condicionesLuces(Ilum)
    Archivo(Cliente,Ilum,Clust,Coci,Esp,Lava,Refri,Bomba,PCs,Comu,Cal,Segu,Aire,Tluz)





##################################################################
def Nombre_Cliente():


    NCliente = 'Cliente Prueba'

    return NCliente

###################### MAIN  #####################################
if __name__ == '__main__':

    NCliente=Nombre_Cliente()

    print("Que quieres hacer? ")
    print("1.- Crear lista ")
    print("2.- Leer Kobo y Crear Deciframiento ")
    print("3.- Crear Reporte")
    #Opcion= input("Elija una opción: \n")


    Opcion='2'


    if Opcion == '1':
        print("Creando Lista")

    if Opcion == '2':
        print("Deciframiento y Kobo")
        Crear_Kobo(NCliente)
        #leer_lista(NCliente)
        hipervinculos(NCliente)
        #ConLED, Precio, Link  =BuscarLED()



    if Opcion == '3':
        Pulgadas = 55
        Watts = 300
        kWh = 99
        PrecioProm= 9975
        DAC=6.08

        # CC = kWh - (2.989644 + 0.034468 * 40) / 0.2606
        XX = np.log(Watts)
        YY= (XX - (3.189644 + 0.034468 * Pulgadas))/0.2606
        Percentil =(1- stats.norm.sf(YY))*100
        print(Percentil)

        Ahorro=100*((Watts - np.exp(3.189644 + 0.034468 * Pulgadas)) / Watts)
        print(Ahorro)

        ROI=PrecioProm/((Ahorro/100)*DAC*kWh)
        print(ROI)


        if kWh<10:
            carita='verde'
        else:
            carita='amarilla'

        if kWh>100 or (Percentil>90 and ROI<18):
            carita='roja'
        print(carita)

    if Opcion == '4':
        print("Generando Reporte")
        datosSolar=pd.DataFrame()
        #Excel, Cliente = abrirexcel()
        aparatos, luces, fugas, consumo,costo, tarifa, Cfugas, solar = leer_deciframiento(NCliente)
        print(solar[0])
        if solar[0] =='Si':
            datosSolar = leer_solar(NCliente)

        CrearPDF(aparatos, luces, fugas, consumo, costo, tarifa, Cfugas, NCliente,datosSolar)















