import pandas as pd
from pandas import ExcelWriter
from pathlib         import Path
from PDF             import CrearPDF
from Deciframiento   import Archivo
from Leer_Deciframiento import leer_deciframiento, leer_solar,leer_potencial,leer_resumen
from DesgloseEquipos import definirequipos
from Condiciones import condicionesLuces
from Potencial_de_ahorro import potecial_ahorro



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
    Solar= pd.DataFrame()
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
        Tablero = Excel.loc[i, ['tablero_codigo_c_i']]
        if Tablero[0]=='otro':
            Tablero = Excel.loc[i, ['tablero_otro_c_i']]
        Datosa.loc[i + largoD, ['Tablero']] = Tablero.values
        Datos, fila, filaLib, Fugas, ilum, clust, coci,esp,lava,refri,bomba,pcs,cal,aires,solar,notass\
            = definirequipos(Excel, int(Nocircuito),Circuito,Tablero,fila,filaLib,writer)

        Ilum  =  Ilum.append(ilum)
        Clust =  Clust.append(clust)
        Coci  =  Coci.append(coci)
        #Comu  =  Comu.append(comu)
        Esp   =  Esp.append(esp)
        Lava  =  Lava.append(lava)
        Refri =  Refri.append(refri)
        Bomba =  Bomba.append(bomba)
        PCs   =  PCs.append(pcs)
        Cal = Cal.append(cal)
        #Segu = Segu.append(segu)
        Aire = Aire.append(aires)
        Solar =Solar.append(solar)
        Nota=Nota.append(notass)
        Datosa =Datosa.append(Datos, ignore_index=True)
        Circuito = Excel.loc[i, ['circuito_c_i']]
        Datosa.loc[i+largoD, ['Circuito']] = Circuito.values
        FugasT = FugasT.append(Fugas, ignore_index=True)
    writer.save()
    Tluz=condicionesLuces(Ilum)
    Archivo(Cliente,Ilum,Clust,Coci,Esp,Lava,Refri,Bomba,PCs,Comu,Cal,Segu,Aire,Tluz,Solar)






##################          PRUEBAS        ########################################
##############    Elige el cliente prueba que desees correr  #####################
def Cliente_Prueba():
    # equipo='Microcomponentes_Cocina'
    # equipo='TVs'
    # equipo='Refris'
    # equipo='Regulador'
    # equipo='Maquinas_de_Hielo_y_Dispensadores'
    # equipo='Lavadoras_y_Secadoras'
    # equipo='Bombas_Presurizadoras'
    #equipo='Reguladores_y_No-Breaks'
    #equipo='Luces'

    #equipo='Tecno'
    equipo='Refris2'


    Cliente = 'Bot_'+ equipo


    return Cliente



################# SE ELIGE EL CLIENTE ##############################################
def Nombre_Cliente():


    #NCliente = Cliente_Prueba()
    NCliente = "Marianela Hernandez"
    #NCliente = "Rodolfo Hill"
    #NCliente = "Jorge Mercado"
    #NCliente = "Guillermo Casas"
    #NCliente = "Carmela Oteyza"

    return NCliente
####################################################################################

###################### PROGRAMA PRINCIPAL  #####################################
if __name__ == '__main__':
    NCliente=Nombre_Cliente()

        #
        #
        #
        #
    #   #   #
     #     #
      #   #
       # #
        #
########################
## Se elige la opción del programa que se quiere correr

    Opcion='4'
#######################


### Se crea la lista (Esta opción no sirve, el programa es independiente)
    if Opcion == '1':
        print("Creando Lista")
### Se lee el Excel de KOBO y se crea la pestaña de deciframiento
    if Opcion == '2':
        print("Deciframiento y Kobo")
        Crear_Kobo(NCliente)
        #hipervinculos(NCliente)

### Se crea la pestaña de potencial de ahorro
    if Opcion == '3':
        potecial_ahorro(NCliente)

### Apartir del Excel de resultados se crea el reporte automático en PDF
    if Opcion == '4':
        print("________________________________")
        print(f"Generando Reporte de {NCliente}")
        datosSolar=pd.DataFrame()
        Ndatos=leer_resumen(NCliente)
        ahorro=leer_potencial(NCliente)
        aparatos, luces, fugas, consumo,costo, tarifa, Cfugas, solar,voltaje = leer_deciframiento(NCliente)
        if solar:
            datosSolar = leer_solar(NCliente)

        CrearPDF(aparatos, luces, fugas, consumo, costo, tarifa, Cfugas, NCliente,datosSolar,voltaje,ahorro,Ndatos)


###########Para hacer pruebas################
    if Opcion == '5':
        leer_resumen(NCliente)

###########################################
    if Opcion == '6':
        #from libBomGrav import armarTxt
        #Claves = "600,si,si,si,ninguno,si,alto,abiertas,no,no,figasTXT, flotador,no,si,no,problemas,0.75,5,10,5,21,1.20,plastica"
        #txt, PotAhorro = armarTxt(100,20,Claves)
        #print(txt)


        #print(PotAhorro.at[0,"Accion"])

        # from funcionesComunes import dataClima as dc
        # wd = dc(CP="10340",Period="today")

        import libreriaAiresAcondicionados as libAA
        print(libAA.armarTxt())

