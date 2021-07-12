import pandas as pd
import math
import numpy as np
from scipy import stats
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
import libreriaClusterTV as CTV
import libreriaReguladores as lg
import libreriaUPS as lups
import libreriaCafeteras as lc
####################  FUNCIONES ###################################
def abrirexcel(Cliente):
    ClientEx=Cliente.replace(' ','_')
    ClientEx=ClientEx +'.xlsx'

    Excel = pd.read_excel(Path.home() / 'Desktop' /ClientEx )

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

    fila=3 #
    filaLib=0 #
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
        Circuito = Excel.loc[i, ['circuito_c_i']]
        Datosa.loc[i+largoD, ['Circuito']] = Circuito.values
        FugasT = FugasT.append(Fugas, ignore_index=True)
    writer.save()
    Tluz=condicionesLuces(Ilum)
    Archivo(Cliente,Ilum,Clust,Coci,Esp,Lava,Refri,Bomba,PCs,Comu,Cal,Segu,Aire,Tluz)





##################################################################
def Nombre_Cliente():


    #NCliente = 'Enrique Tawil'
    NCliente = 'Cliente Prueba'
    #NCliente = 'Carlos Estefan'

    return NCliente

###################### MAIN  #####################################
if __name__ == '__main__':

    NCliente=Nombre_Cliente()

    print("Que quieres hacer? ")
    print("1.- Crear Excel")
    print("2.- Leer Kobo y Crear Deciframiento ")
    print("4.- Crear Reporte")
    #Opcion= input("Elija una opción: \n")


    Opcion='4'


    if Opcion == '1': # NO CONVENDRIA LIMPIAR ESTO PARA TENER ESTE ARCHIVO MAS LEGIBLE?
        print("Creando Lista")

    if Opcion == '2':
        print("Deciframiento y Kobo")
        Crear_Kobo(NCliente)
        #hipervinculos(NCliente)

    if Opcion == '3': # IGUAL AL COMENTARIO ANTERIOR, NO CONVENDRIA LIMPIAR ESTO?
        """
        dfCTV=pd.DataFrame.from_dict({'disp':['TV','Decodificador','NoBreak','Bocinas'],
                                      'nominal' :[30,30, 10, 10]                   ,
                                      'standby' :[.3,  .3, 10,  .5]                   ,
                                      'tol'     :[True , True , True , True ]     ,
                                      'cReg'    :[False , False, False, False ]     ,
                                      'cUPS'    :[True, False, False, True]     ,
                                      'ampere'  :[1 , 1, 1, 1]                   ,})
        volEst=True
        VAmax=1000
        Vpro=120
        FPfuga=0.8
        # print(lg.roiReg(dfCTV, VAmax, Vpro, FPfuga, 'E'))
        # print(lups.recomendaciónUPS(dfCTV, VAmax, Vpro, FPfuga))
        print(CTV.armarTexto(volEst,dfCTV,VAmax,Vpro,FPfuga))
        """
        #lc.leerLibreriaCafeteras()
        print(lc.dias('lunes martes andlasnda domingo'))
    if Opcion == '4':
        print("Generando Reporte")
        datosSolar=pd.DataFrame()
        #Excel, Cliente = abrirexcel()
        aparatos, luces, fugas, consumo,costo, tarifa, Cfugas, solar,voltaje = leer_deciframiento(NCliente)
        print(solar[0])
        if solar[0] =='Si':
            datosSolar = leer_solar(NCliente)

        CrearPDF(aparatos, luces, fugas, consumo, costo, tarifa, Cfugas, NCliente,datosSolar,voltaje)















