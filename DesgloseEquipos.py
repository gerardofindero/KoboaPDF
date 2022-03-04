import pandas as pd

from Refrigeradores  import refrigerador
from Cluster         import clustertv
from Especiales      import especiales
from Tecnologia      import tecnologia
from Luminaria       import iluminacion
from Bombas          import bombas
from Lavanderia      import lavanderia
from Cocina          import cocina
from Calentadores    import calentadores
from Solar           import solar
from AiresA          import airesA

def definirequipos(Excel, Nocircuito,NomCircuito,tablero,primafila,FilaLib,writer,voltaje):
    indx = 0
    Columnas = Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("equipos_c_i", case=False)]
    Equipos = Excel[InfoEquipos]
    Circuito1 = Equipos.loc[Nocircuito]
    Notas_Equipos=pd.DataFrame(columns=['Tablero','Circuito', 'Equipo','Lugar','Notas'])
    Notas_ = pd.DataFrame(columns=['Tablero', 'Circuito', 'Equipo', 'Lugar','Notas'])
    DatosFun=pd.DataFrame()
    DatosCL     = pd.DataFrame(columns=['Tablero','Circuito','Zona','Marca','Standby','Nominal','Tolerancia', 'Pulgadas','Atacable','Existencia'])
    DatosIlu    = pd.DataFrame(columns=['Tablero','Circuito'])
    DatosRF     = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosCoc    = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosCom    = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosPC     = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosSegu   = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosAire   = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosES     = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosLava   = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosBb     = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosCal    = pd.DataFrame(columns=['Tablero', 'Circuito'])
    DatosSol    = pd.DataFrame(columns=['Tablero', 'Circuito'])
    Fugas       = pd.DataFrame(columns=['Tablero','Circuito','Marca','Consumo'])
    nombre='C.'+ str(NomCircuito[0])
    pdcir=pd.DataFrame(columns= [str(tablero[0]), nombre ])
    pdcir.to_excel(writer ,index=False,startrow=primafila-1)

    for j in Circuito1:
        if j == 1:
            if indx == 1:
                print("Cluster")
                Datos_CL , Zona = clustertv(Excel,Nocircuito,NomCircuito,voltaje)
                DatosCL = pd.concat([DatosCL,Datos_CL])
                Datos_CL.to_excel(writer,  index=True,startrow=primafila)
                primafila = primafila+ len(Datos_CL) + 4
                DatosCL['Tablero'].fillna(tablero[0], inplace=True)
                DatosCL['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosCL['Zona'].fillna(Zona, inplace=True)
                FilaLib += 2

            if indx == 2:
                print("Refrigeracion")
                Datos_RF, Consum, Codigo = refrigerador(Excel,Nocircuito,NomCircuito,voltaje)
                DatosFun = pd.concat([DatosFun, Datos_RF], ignore_index=True)
                DatosRF = pd.concat([DatosRF,Datos_RF])
                DatosRF['Tablero'].fillna(tablero[0], inplace=True)
                DatosRF['Circuito'].fillna(NomCircuito[0], inplace=True)
                Datos_RF.to_excel(writer, index=True,startrow=primafila)
                primafila = primafila+len(Datos_RF) + 4
                #Codigo.to_excel(writer, sheet_name='Libreria', index=True,startrow=FilaLib)
                FilaLib += 2

            if indx == 3:
                print("Iluminacion ")
                Datos_IL= iluminacion(Excel,Nocircuito)
                DatosIlu = pd.concat([DatosIlu,Datos_IL])
                DatosIlu['Tablero'].fillna(tablero[0], inplace=True)
                DatosIlu['Circuito'].fillna(NomCircuito[0], inplace=True)
                Datos_IL.to_excel(writer,  index=True,startrow=primafila)
                primafila = primafila+len(Datos_IL) + 4
                notass = DatosIlu[["Tablero",'Circuito','Tecnologia','Lugar','Notas']]
                notass.columns=['Tablero','Circuito', 'Equipo','Lugar','Notas']
                notass=notass.dropna(subset=['Notas'])
                Notas_Equipos= notass
                Notas_ = pd.concat([Notas_,Notas_Equipos])

            if indx == 4:
                print("Bombas")
                Datos_Bb = bombas(Excel, Nocircuito)
                DatosBb = pd.concat([DatosBb,Datos_Bb])
                DatosFun = pd.concat([DatosFun,Datos_Bb], ignore_index=True)
                Datos_Bb.to_excel(writer, index=True, startrow=primafila)
                DatosBb['Tablero'].fillna(tablero[0], inplace=True)
                DatosBb['Circuito'].fillna(NomCircuito[0], inplace=True)
                primafila = primafila + len(Datos_Bb) + 4

            if indx == 5:
                print("Cocina")
                Datos_CN = cocina(Excel, Nocircuito,NomCircuito)
                DatosCoc = pd.concat([DatosCoc,Datos_CN])
                DatosCoc['Tablero'].fillna(tablero[0], inplace=True)
                DatosCoc['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosFun = pd.concat([DatosFun,Datos_CN], ignore_index=True)
                Datos_CN.to_excel(writer, index=True ,startrow=primafila)
                primafila = primafila+len(Datos_CN) + 4

            if indx == 6:
                print("Lavanderia")
                Datos_LV = lavanderia(Excel, Nocircuito,NomCircuito,voltaje)
                DatosLava = pd.concat([DatosLava,Datos_LV])
                DatosLava['Tablero'].fillna(tablero[0], inplace=True)
                DatosLava['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosFun = pd.concat([DatosFun,Datos_LV], ignore_index=True)
                Datos_LV.to_excel(writer, index=True ,startrow=primafila)
                primafila = primafila+len(Datos_LV) + 4

            if indx == 7:
                print("Calentadores")
                Datos_Cal = calentadores(Excel, Nocircuito,NomCircuito)
                DatosCal = pd.concat([DatosCal,Datos_Cal])
                DatosCal['Tablero'].fillna(tablero[0], inplace=True)
                DatosCal['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosFun  = pd.concat([DatosFun,Datos_Cal], ignore_index=True)
                Datos_Cal.to_excel(writer, index=True, startrow=primafila)
                primafila = primafila + len(Datos_Cal) + 4

            if indx == 8:
                print("Solar")
                Datos_Solar=solar(Excel, Nocircuito, NomCircuito)
                DatosSol = pd.concat([DatosSol,Datos_Solar])
                DatosSol['Tablero'].fillna(tablero[0], inplace=True)
                DatosSol['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosFun  = pd.concat([DatosFun,Datos_Solar], ignore_index=True)
                Datos_Solar.to_excel(writer, index=True, startrow=primafila)
                primafila = primafila + len(Datos_Solar) + 4


            if indx == 9:
                print('Tecnologia')
                Datos_PC = tecnologia(Excel, Nocircuito, NomCircuito,voltaje)
                DatosPC = pd.concat([DatosPC,Datos_PC])
                DatosPC['Tablero'].fillna(tablero[0], inplace=True)
                DatosPC['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosFun = pd.concat([DatosFun,Datos_PC], ignore_index=True)
                Datos_PC.to_excel(writer, index=True, startrow=primafila)
                primafila = primafila + len(Datos_PC) + 4


            if indx == 10:
                print('Aires Acondicionados')
                Datos_Aires = airesA(Excel, Nocircuito, NomCircuito)
                DatosAire = pd.concat([DatosSegu,Datos_Aires])
                DatosAire['Tablero'].fillna(tablero[0], inplace=True)
                DatosAire['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosFun = pd.concat([DatosFun,Datos_Aires], ignore_index=True)
                Datos_Aires.to_excel(writer, index=True, startrow=primafila)
                primafila = primafila + len(Datos_Aires) + 4

            if indx == 11:
                print("Especiales")
                Datos_ES, Consum = especiales(Excel, Nocircuito,NomCircuito)
                DatosES=pd.concat([DatosES,Datos_ES])
                DatosES['Tablero'].fillna(tablero[0], inplace=True)
                DatosES['Circuito'].fillna(NomCircuito[0], inplace=True)
                DatosFun = pd.concat([DatosFun,Datos_ES], ignore_index=True)
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
           DatosES,DatosLava,DatosRF,DatosBb,DatosPC,DatosCal,DatosAire,DatosSol,Notas_