import pandas as pd
from pandas import ExcelWriter
from pathlib         import Path
from PDF             import CrearPDF
from Deciframiento   import Archivo
from Leer_Deciframiento import leer_deciframiento, leer_solar,leer_potencial,leer_resumen
from DesgloseEquipos import definirequipos
from Condiciones import condicionesLuces
from Potencial_de_ahorro import potecial_ahorro
from Carpeta_Clientes import carpeta_clientes_Imagenes
from leerVoltaje import leer_volts

####################  FUNCIONES ###################################
def abrirexcel(Cliente):
    ClientEx=Cliente.replace(' ','_')
    ClientEx=ClientEx +'.xlsx'
    Excel = pd.read_excel(Path.home() / 'Desktop' /ClientEx )
    return Excel,Cliente

def Crear_Kobo(NCliente):
    voltaje = leer_volts(NCliente)

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
            = definirequipos(Excel, int(Nocircuito),Circuito,Tablero,fila,filaLib,writer,voltaje)

        Ilum  =  pd.concat([Ilum,ilum])
        Clust =  pd.concat([Clust,clust])
        Coci  =  pd.concat([Coci,coci])
        #Comu  =  Comu.append(comu)
        Esp   =  pd.concat([Esp,esp])
        Lava  =  pd.concat([Lava,lava])
        Refri =  pd.concat([Refri,refri])
        Bomba =  pd.concat([Bomba,bomba])
        PCs   =  pd.concat([PCs,pcs])
        Cal   =  pd.concat([Cal,cal])
        #Segu = Segu.append(segu)
        Aire  =  pd.concat([Aire,aires])
        Solar =  pd.concat([Solar,solar])
        Nota  =  pd.concat([Nota,notass])
        Datosa = pd.concat([Datosa,Datos], ignore_index=True)
        Circuito = Excel.loc[i, ['circuito_c_i']]
        Datosa.loc[i+largoD, ['Circuito']] = Circuito.values
        FugasT = pd.concat([FugasT,Fugas], ignore_index=True)
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
    #NCliente = "Guillermo Casas"
    #NCliente = "Federico Rios"
    #NCliente = "San Simon"
    #NCliente = "Guillermo Casas"
    #NCliente = "Rebeca Tabachnik"
    #NCliente = 'Leon Cukiert'
    #NCliente = 'Julieta Porres'
    #NCliente = 'Magali Duran'
    NCliente = 'Antonio Lopez Irragori'

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
        KoboS=pd.DataFrame()
        Ndatos=leer_resumen(NCliente)
        ahorro=leer_potencial(NCliente)
        aparatos, luces, fugas, consumo,costo, tarifa, Cfugas, solar,voltaje = leer_deciframiento(NCliente)
        info_volts=leer_volts(NCliente)
        if solar:
            datosSolar,KoboS = leer_solar(NCliente)
        CrearPDF(aparatos, luces, fugas, consumo, costo, tarifa, Cfugas, NCliente,datosSolar,KoboS,voltaje,ahorro,Ndatos,info_volts)


###########Para hacer pruebas################
    if Opcion == '5':
        archivo_resultados = carpeta_clientes_Imagenes(NCliente)
        print(archivo_resultados)

###########################################
    if Opcion == '6':

        import libreriaBombasAlberca as lba
        Claves   = "BA,720/800/60,RE,SS"
        potencia = 800
        hrsUso   = 15*7
        kwh      = 50
        trash = lba.recoBA(Claves,kwh,hrsUso,potencia)
        print(trash)

