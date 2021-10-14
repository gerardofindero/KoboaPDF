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
from Leer_Deciframiento import leer_deciframiento, leer_solar,leer_potencial,leer_resumen
from DesgloseEquipos import definirequipos
from Condiciones import condicionesLuces
from Potencial_de_ahorro import potecial_ahorro
from LibreriaLED import BuscarLED
import libreriaClusterTV as CTV
import libreriaReguladores as lg
import libreriaUPS as lups
import libreriaCafeteras as lc
from libreriaTubosFluorescente import libreriaTubosFluorescentes
from libreriaTirasLED import libreriaTirasLED
import libreriaPlanchas as lp
from leerVoltaje import leer_volts
import libreriaBombas as lb



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

    NCliente = 'Cliente Prueba'
    #NCliente = 'Ricardo Martins'
    #NCliente = 'Valeria Arriaga'
    #NCliente = 'Alex Soto'
    #NCliente = 'Josefa Rivero'
    NCliente  = 'Manuel Gutierrez'
    #NCliente = 'Miguel Lascurain'
    #NCliente = 'David Mekler'
    #NCliente = 'Jaime Massieu'
    return NCliente

###################### MAIN  #####################################
if __name__ == '__main__':

    NCliente=Nombre_Cliente()

    # print("Que quieres hacer? ")
    # print("1.- Crear Excel")
    # print("2.- Leer Kobo y Crear Deciframiento ")
    # print("4.- Crear Reporte")
    #Opcion= input("Elija una opción: \n")


    Opcion='3'


    if Opcion == '1':
        print("Creando Lista")

    if Opcion == '2':
        print("Deciframiento y Kobo")
        #VE = leer_volts(NCliente)
        Crear_Kobo(NCliente)
        #hipervinculos(NCliente)

    if Opcion == '3':
        import libreriaBombasPresurizadoras as lbp
        txt = lbp.recoPresu(w=370,kwh=456,tinaco="si",pastilla="si",pb="bien",pa="bien", ver="",
                            val="",jar="",fug1="no",fug1l="concina",fug2="no",fug2l="baño",
                            pru="")
        print(txt)

    if Opcion == '4':
        print("________________________________")
        print(f"Generando Reporte de {NCliente}")
        datosSolar=pd.DataFrame()
        Ndatos=leer_resumen(NCliente)
        #Excel, Cliente = abrirexcel()
        ahorro=leer_potencial(NCliente)
        #ahorro=140
        aparatos, luces, fugas, consumo,costo, tarifa, Cfugas, solar,voltaje = leer_deciframiento(NCliente)
        solar='No'
        if solar =='Si':
            datosSolar = leer_solar(NCliente)
        CrearPDF(aparatos, luces, fugas, consumo, costo, tarifa, Cfugas, NCliente,datosSolar,voltaje,ahorro,Ndatos)


###########Para hacer pruebas################
    if Opcion == '5':
        leer_resumen(NCliente)
        # import libreriaSenMov as lsm
        # lib=lsm.libreriaSensores()
        # lib.setData(300,50,"Baño",6.1)
        # print(lib.armarTxt())











