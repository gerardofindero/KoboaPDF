import pandas as pd
from pandas import ExcelWriter

from pathlib         import Path
from Refrigeradores  import refrigerador
from Cluster         import clustertv
from Especiales      import especiales
from Iluminacion     import iluminacion
from Bombas          import bombas
from Lavanderia      import lavanderia
from Cocina          import cocina
from Calentadores    import calentadores
from Comunicaciones  import comunicaciones
from Computo         import computo
from Seguridad       import seguridad
from Solar           import solar
from AiresA          import airesA
from pdf             import CrearPDF
from Deciframiento   import Archivo
from Hipervinculos   import hipervinculos
from Ahorro          import potencial_ahorro
from Leer_Deciframiento import leer_deciframiento, leer_solar


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

def abrirexcel(Cliente):
    ClientEx=Cliente.replace(' ','_')
    ClientEx=ClientEx +'.xlsx'
    try:
        Excel = pd.read_excel(Path.home() / 'Desktop' /ClientEx )
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    return Excel,Cliente

def definirequipos(Excel, Nocircuito,NomCircuito,tablero,primafila,FilaLib,writer):
    indx = 0
    Columnas = Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("equipos_c_i", case=False)]
    Equipos = Excel[InfoEquipos]
    Circuito1 = Equipos.loc[Nocircuito]
    Notas_Equipos=pd.DataFrame(columns=['Tablero','Circuito', 'Equipo','Lugar','Notas'])
    Notas_ = pd.DataFrame(columns=['Tablero', 'Circuito', 'Equipo', 'Lugar','Notas'])
    DatosFun=pd.DataFrame()
    DatosCL = pd.DataFrame(columns=['Tablero','Circuito','Zona','Marca','Standby','Nominal','Tolerancia', 'Pulgadas','Atacable','Existencia'])
    DatosIlu = pd.DataFrame(columns=['Tablero','Circuito'])
    DatosRF = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosCoc = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosCom = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosPC = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosSegu = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosAire = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosES = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosLava = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosBb = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosCal = pd.DataFrame(columns=['Tablero', 'Circuito'])
    Fugas = pd.DataFrame(columns=['Tablero','Circuito','Marca','Consumo'])
    nombre='C.'+ str(NomCircuito[0])
    pdcir=pd.DataFrame(columns= [str(tablero[0]), nombre ])
    pdcir.to_excel(writer ,index=False,startrow=primafila-1)

    for j in Circuito1:
        if j == 1:
            if indx == 1:
                print("Cluster")
                Datos_CL, Consum ,Codigo , Zona = clustertv(Excel,Nocircuito,NomCircuito)
                DatosCL = DatosCL.append(Datos_CL)
                Datos_CL.to_excel(writer,  index=True,startrow=primafila)
                primafila = primafila+ len(Datos_CL) + 4
                Codigo.to_excel(writer, sheet_name='Libreria', index=True, startrow=FilaLib)
                DatosCL['Tablero'].fillna(tablero[0], inplace=True)
                DatosCL['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosCL['Zona'].fillna(Zona, inplace=True)
                notass=Datos_CL.loc['Notas','Marca']
                DatosCL['Nota']=notass
                Notas_Equipos.loc[primafila]=[tablero[0],NomCircuito[0],'ClusterTV',Zona,notass]
                Notas_ = Notas_.append(Notas_Equipos)
                FilaLib += 2

            if indx == 2:
                print("Refrigeracion")
                Datos_RF, Consum, Codigo = refrigerador(Excel,Nocircuito,NomCircuito)
                DatosFun = DatosFun.append(Datos_RF, ignore_index=True)
                DatosRF = DatosRF.append(Datos_RF)
                DatosRF['Tablero'].fillna(tablero[0], inplace=True)
                DatosRF['Circuito'].fillna(NomCircuito[0], inplace=True)
                Datos_RF.to_excel(writer, index=True,startrow=primafila)
                primafila = primafila+len(Datos_RF) + 4
                Codigo.to_excel(writer, sheet_name='Libreria', index=True,startrow=FilaLib)
                FilaLib += 2

            if indx == 3:
                print("Iluminacion ")
                Datos_IL= iluminacion(Excel,Nocircuito)
                DatosIlu= DatosIlu.append(Datos_IL)
                DatosIlu['Tablero'].fillna(tablero[0], inplace=True)
                DatosIlu['Circuito'].fillna(NomCircuito[0], inplace=True)
                Datos_IL.to_excel(writer,  index=True,startrow=primafila)
                primafila = primafila+len(Datos_IL) + 4
                notass = DatosIlu[["Tablero",'Circuito','Tecnologia','Lugar','Notas']]
                notass.columns=['Tablero','Circuito', 'Equipo','Lugar','Notas']
                notass.dropna(subset=['Notas'], inplace=True)
                Notas_Equipos= notass
                Notas_ = Notas_.append(Notas_Equipos)

            if indx == 4:
                print("Bombas")
                Datos_Bb = bombas(Excel, Nocircuito)
                DatosBb = DatosBb.append(Datos_Bb)
                DatosFun = DatosFun.append(Datos_Bb, ignore_index=True)
                Datos_Bb.to_excel(writer, index=True, startrow=primafila)
                DatosBb['Tablero'].fillna(tablero[0], inplace=True)
                DatosBb['Circuito'].fillna(NomCircuito[0], inplace=True)
                primafila = primafila + len(Datos_Bb) + 4

            if indx == 5:
                print("Cocina")
                Datos_CN = cocina(Excel, Nocircuito,NomCircuito)
                DatosCoc = DatosCoc.append(Datos_CN)
                DatosCoc['Tablero'].fillna(tablero[0], inplace=True)
                DatosCoc['Circuito'].fillna(NomCircuito[0], inplace=True)
                notass = Datos_CN.loc['Notas', 'Marca']
                DatosCoc['Notas'] = notass
                DatosFun = DatosFun.append(Datos_CN, ignore_index=True)
                Datos_CN.to_excel(writer, index=True ,startrow=primafila)
                primafila = primafila+len(Datos_CN) + 4

            if indx == 6:
                print("Lavanderia")
                Datos_LV = lavanderia(Excel, Nocircuito,NomCircuito)
                DatosLava = DatosLava.append(Datos_LV)
                DatosLava['Tablero'].fillna(tablero[0], inplace=True)
                DatosLava['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosFun = DatosFun.append(Datos_LV, ignore_index=True)
                Datos_LV.to_excel(writer, index=True ,startrow=primafila)
                primafila = primafila+len(Datos_LV) + 4

            if indx == 7:
                print("Calentadores")
                Datos_Cal = calentadores(Excel, Nocircuito,NomCircuito)
                DatosCal = DatosCal.append(Datos_Cal)
                DatosCal['Tablero'].fillna(tablero[0], inplace=True)
                DatosCal['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosFun  = DatosFun.append(Datos_Cal, ignore_index=True)
                Datos_Cal.to_excel(writer, index=True, startrow=primafila)
                primafila = primafila + len(Datos_Cal) + 4

            if indx == 8:
                print("Solar")
                Datos_Solar=solar(Excel, Nocircuito, NomCircuito)
                Datos_Solar.to_excel(writer, index=True, startrow=primafila)
                primafila = primafila + len(Datos_Solar) + 4

            if indx == 9:
                print('Computo')
                Datos_PC = computo(Excel, Nocircuito, NomCircuito)
                DatosPC = DatosPC.append(Datos_PC)
                DatosPC['Tablero'].fillna(tablero[0], inplace=True)
                DatosPC['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosFun = DatosFun.append(Datos_PC, ignore_index=True)
                Datos_PC.to_excel(writer, index=True, startrow=primafila)
                primafila = primafila + len(Datos_PC) + 4

            if indx == 10:
                print('Comunicaciones')
                Datos_Com = comunicaciones(Excel, Nocircuito, NomCircuito)
                DatosCom = DatosCom.append(Datos_Com)
                DatosCom['Tablero'].fillna(tablero[0], inplace=True)
                DatosCom['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosFun = DatosFun.append(Datos_Com, ignore_index=True)
                Datos_Com.to_excel(writer, index=True, startrow=primafila)
                primafila = primafila + len(Datos_Com) + 4

            if indx == 11:
                print('Seguridad')
                Datos_Segu = seguridad(Excel, Nocircuito, NomCircuito)
                DatosSegu = DatosSegu.append(Datos_Segu)
                DatosSegu['Tablero'].fillna(tablero[0], inplace=True)
                DatosSegu['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosFun = DatosFun.append(Datos_Segu, ignore_index=True)
                Datos_Segu.to_excel(writer, index=True, startrow=primafila)
                primafila = primafila + len(Datos_Segu) + 4

            if indx == 12:
                print('Aires Acondicionados')
                Datos_Aires = airesA(Excel, Nocircuito, NomCircuito)
                DatosAire = DatosSegu.append(Datos_Aires)
                DatosAire['Tablero'].fillna(tablero[0], inplace=True)
                DatosAire['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosFun = DatosFun.append(Datos_Aires, ignore_index=True)
                Datos_Aires.to_excel(writer, index=True, startrow=primafila)
                primafila = primafila + len(Datos_Aires) + 4

            if indx == 13:
                print("Especiales")
                Datos_ES, Consum = especiales(Excel, Nocircuito,NomCircuito)
                DatosES=DatosES.append(Datos_ES)
                DatosES['Tablero'].fillna(tablero[0], inplace=True)
                DatosES['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosFun = DatosFun.append(Datos_ES, ignore_index=True)
                Datos_ES.to_excel(writer, index=True,startrow=primafila)
                primafila = primafila+len(Datos_ES) + 4

        indx = indx+ 1

    Fugas = Fugas[Fugas['Consumo'] != 0]
    Fugas.dropna(subset=['Consumo'], inplace = True)
    NOM=str(NomCircuito[0])
    Fugas['Circuito'].fillna(NOM, inplace = True)
    Fugas['Tablero'].fillna(tablero[0], inplace=True)
    Datoss=DatosFun.copy()
    return Datoss, primafila, FilaLib,Fugas,DatosIlu,DatosCL,DatosCoc,\
           DatosCom,DatosES,DatosLava,DatosRF,DatosBb,DatosPC,DatosCal,DatosSegu,DatosAire,Notas_



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

    Equipos, Luminarias, Fugas = Archivo(Cliente,Ilum,Clust,Coci,Esp,Lava,Refri,Bomba,PCs,Comu,Cal,Segu,Aire)
    #potencial_ahorro(Cliente,Equipos, Luminarias, Fugas)

###################### MAIN  #####################################
if __name__ == '__main__':

    NCliente = 'Gerardo Fernandez'
    #NCliente = 'Jose Escalante Cuernavaca'
    #NCliente = 'Patty Lopez de la Cerda'
    #NCliente = 'Monica Larrosa'



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















