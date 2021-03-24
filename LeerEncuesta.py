import pandas as pd

from pandas import ExcelWriter
from pathlib         import Path
from pdf             import CrearPDF
from Deciframiento   import Archivo
from Hipervinculos   import hipervinculos
from Ahorro          import potencial_ahorro
from Leer_Deciframiento import leer_deciframiento, leer_solar
from DesgloseEquipos import definirequipos
from Condiciones import condicionesLuces

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

        Circuito = Excel.loc[i, ['circuito_c_i']]
        Datosa.loc[i+largoD, ['Circuito']] = Circuito.values
        FugasT = FugasT.append(Fugas, ignore_index=True)
    writer.save()
    #condicionesLuces(Ilum)
    Equipos, Luminarias, Fugas = Archivo(Cliente,Ilum,Clust,Coci,Esp,Lava,Refri,Bomba,PCs,Comu,Cal,Segu,Aire)

    #potencial_ahorro(Cliente,Equipos, Luminarias, Fugas)

###################### MAIN  #####################################
if __name__ == '__main__':

    #NCliente = 'Gerardo Fernandez'
    #NCliente = 'Jose Martin Carballo'
    #NCliente = 'Sergio Maya'
    NCliente = 'Pruebas'

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

    if Opcion == '3':
        print("Poner Condiciones")
        print("Poner caritas")
        print("Pasar a formato para PDF")
        print("Generar Potencial de ahorro")
        #hipervinculos(NCliente)
        #Excel, Cliente = abrirexcel(NCliente)
        aparatos, luces, fugas, consumo,costo, tarifa, Cfugas, solar= leer_deciframiento(NCliente)
        #caritas=definircarita(aparatos)
        potencial_ahorro(NCliente, aparatos, luces, fugas, tarifa)


    if Opcion == '4':
        print("Generando Reporte")
        datosSolar=pd.DataFrame()
        #Excel, Cliente = abrirexcel()
        aparatos, luces, fugas, consumo,costo, tarifa, Cfugas, solar = leer_deciframiento(NCliente)
        print(solar[0])
        if solar[0] =='Si':
            datosSolar = leer_solar(NCliente)

        CrearPDF(aparatos, luces, fugas, consumo, costo, tarifa, Cfugas, NCliente,datosSolar)















