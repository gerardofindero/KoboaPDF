from SepararFugas import *
import datetime
import os
from pandas import ExcelWriter
from pathlib         import Path
from datetime import datetime
import pandas as pd
import xlwings
from Tarifa          import leer_tarifa_Dac
from Leer_Lista      import leer_lista
import numpy as np


def tipoluces(tipo):
    tipoGen='focos'
    tipoGen='tubos'
    tipoGen='tiras'


#### Excel
def ExcelDes(Equipos, Luminarias, Fugas,archivo_resultados,Cliente)    :



    Atacable = Fugas['Atacable'].values
    Fugas.drop(['Atacable'], axis=1, inplace=True)
    Fugas.reset_index(inplace=True, drop=True)

    Tipo = Luminarias['Tipo'].values
    Luminarias.drop(['Tipo'], axis=1, inplace=True)
    Luminarias.reset_index(inplace=True, drop=True)

    workbook = xlwings.Book(archivo_resultados)
    gris = (200, 200, 200)
    Consumo_bimestral = '=Resumen!E4'
    Tarifa = leer_tarifa_Dac()
    try:
        workbook.sheets.add('Desciframiento')
    except:
        print('Hoja ya creada')

    celdaFinal = len(Equipos) + len(Luminarias) + len(Fugas) + 12
    Sheet1 = workbook.sheets['Desciframiento']
    #Deciframiento = pd.concat([Equipos, Luminarias, Fugas])
    Sheet1.range('A6').value = Equipos
    Sheet1.range(len(Equipos)+9,1).value = Luminarias
    Sheet1.range(len(Equipos)+len(Luminarias)+12,1).value= Fugas
    Sheet1.range('C2').value = Consumo_bimestral
    Sheet1.range('C3').value = '=SUM(K7:K'+str(celdaFinal)+')'
    Sheet1.range('C1').value = 'Consumo'
    Sheet1.range('C1').color = gris
    Sheet1.range('D1').value = 'Costo'
    Sheet1.range('D1').color = gris
    Sheet1.range('D2').value = '=C2*G1'
    Sheet1.range('D3').value = '=(C3*G1)+263.32'
    Sheet1.range('B2').value = 'Bimestral'
    Sheet1.range('B2').color = gris
    Sheet1.range('B3').value = 'Ajustado con costo fijo'
    Sheet1.range('B3').color = gris
    Sheet1.range('G1').value =  Tarifa
    Sheet1.range('F1').value = 'Tarifa'
    Sheet1.range('F1').color = gris
    Sheet1.range('F2').value = 'Medidor'
    Sheet1.range('F2').color = gris
    Sheet1.range('F3').value = 'Voltaje'
    Sheet1.range('F3').color = gris
    Sheet1.range('G2').value = '1'
    Sheet1.range('G3').value = '1'


    Sheet1.range(6, 16).value = 'Descripcion de Señal'
    Sheet1.range(6, 14).value = 'Texto a PDF'
    Sheet1.range(6, 17).value = 'Claves'
    for i in range(len(Equipos)):
        Sheet1.range(7+i, 9).value = '=F'+str(7+i)+'*C$2'
        Sheet1.range(7+i, 11).value = '=IF(J'+str(7+i)+'="NM",I'+str(7+i)+',(J'+str(7+i)+' / G'+str(7+i)+') * I'+str(7+i)+')'
        Sheet1.range(7+i, 12).value = '=K'+str(7+i)+' / C$3'
        Sheet1.range(7+i, 13).value = '=K'+str(7+i)+'*G$1'

    Sheet1.range(len(Equipos)+9, 4).value= 'Luminaria'
    Sheet1.range(len(Equipos) + 9, 14).value = 'Texto a PDF'
    Sheet1.range(len(Equipos) + 9, 16).value = 'Descripcion de Señal'
    Sheet1.range(len(Equipos) + 9, 17).value = 'Número'
    for i in range(len(Luminarias)):
        inicioL=len(Equipos)+10
        Sheet1.range(inicioL+i, 9).value = '=F'+str(i+inicioL)+'*C$2'
        Sheet1.range(inicioL+i, 11).value = '=IF(J'+str(i+inicioL)+'="NM",G'+str(i+inicioL)+',(J'+str(i+inicioL)+' / G'+str(i+inicioL)+') * I'+str(i+inicioL)+')'
        Sheet1.range(inicioL+i, 12).value = '=K'+str(i+inicioL)+' / C$3'
        Sheet1.range(inicioL+i, 13).value = '=K'+str(i+inicioL)+'*G$1'

    Sheet1.range(len(Equipos) + len(Luminarias)+12, 4).value = 'Perdidas'
    Sheet1.range(len(Equipos) + len(Luminarias) + 12, 16).value = 'Descripcion'

    for i in range(len(Fugas)):
        inicioF=len(Equipos)+len(Luminarias)+13
        #Sheet1.range(inicioL+i, 8).value = '=E'+str(inicioL+i)+'*C$2'
        Sheet1.range(inicioF+i, 11).value = '=J'+str(inicioF+i)+'*24*60/1000'
        Sheet1.range(inicioF+i, 12).value = '=K'+str(inicioF+i)+' / C$3'
        Sheet1.range(inicioF+i, 13).value = '=K'+str(inicioF+i)+'*G$1'

####### Color y Bordes
    CelF="$A$6:$Q$"+str(celdaFinal)
    for i in range(17):
        Sheet1.range(6,i+1).color = gris
        Sheet1.range(len(Equipos) + 9, 1+i).color = gris
        Sheet1.range(len(Equipos) + len(Luminarias) + 12, 1+i).color = gris

    Sheet1.range(CelF).api.Borders.Weight = 2
    Sheet1.range("$B$1:$D$3").api.Borders.Weight = 2
    Sheet1.range("$F$1:$G$3").api.Borders.Weight = 2
    Sheet1.range(CelF).columns.autofit()
    Sheet1['1:1'].api.ColumnWidth = 10
    Sheet1.range('N1').column_width = 100
    Sheet1.range('O1').column_width = 100
    Sheet1.range('P1').column_width = 100
    Sheet1.range('D1').column_width = 30
    Sheet1.range('E1').column_width = 20

    i = 0
    inicioL = len(Equipos) + 10
    Sheet1.range(inicioL - 1, 1).value = 'Tipo'
    for tipo in Tipo:
        Sheet1.range(inicioL + i, 1).value = tipo
        i = i + 1

    i=0
    inicioL = len(Equipos) + len(Luminarias) + 13
    Sheet1.range(inicioL -1, 1).value = 'Atacable'
    for atac in Atacable:
        Sheet1.range(inicioL + i, 1).value = atac
        i=i+1



    infoL= leer_lista(Cliente)
    infoL['B']=infoL['B'].str.upper()
    print(infoL['B'])
    cony=0
    #print(Equipos)
    for i in Equipos['Codigo']:
        print(i)
        i = i.upper()
        identificados= infoL[infoL['B'].str.contains(i)].index
        if not identificados.empty:
            Sheet1.range(7 + cony, 6).value =infoL.loc[identificados[0],'D']
            Sheet1.range(7 + cony, 7).value = infoL.loc[identificados[0], 'F']
            Sheet1.range(7+ cony, 16).value = infoL.loc[identificados[0], 'H']
        cony=cony+1
    cony = 0
    inicioL = len(Equipos) + 10

    for i in Luminarias['Codigo']:
        i=i.upper()
        identificados= infoL[infoL['B'].str.contains(i)].index
        if not identificados.empty:
            Sheet1.range(inicioL + cony, 6).value = infoL.loc[identificados[0], 'D']
            Sheet1.range(inicioL + cony, 7).value = infoL.loc[identificados[0], 'F']
            Sheet1.range(inicioL + cony, 16).value = infoL.loc[identificados[0], 'H']
        cony = cony + 1


    cony = 0
    inicioF = len(Equipos) + len(Luminarias) + 13
    print(Fugas)

    for i in Fugas['Codigo']:

        i = i.upper()
        identificados = infoL[infoL['B'].str.contains(i)].index
        if not identificados.empty:
            Sheet1.range(inicioF + cony, 6).value = infoL.loc[identificados[0], 'D']
        cony=cony+1
    workbook.save()
    workbook.close()

    return Equipos, Luminarias, Fugas

def Archivo(Cliente,Luz,Clust,Coci,Esp,Lava,Refri,Bomba,PCs,Comu,Cal,Segu,Aire):

    Luminaria=Luz.copy()
    Luminarias = pd.DataFrame(
        columns=['Codigo','Ubicacion', 'Equipo', 'Lugar', '% Equipo', 'Potencia', 'Horas de la semana', 'kWh', 'Potencia Kobo',
                 'kWh Ajustado','% Ajustado','$ Bimestre', 'Texto','Notas',' ', 'Claves'])
    Equipos = pd.DataFrame(
        columns=['Codigo','Ubicacion', 'Equipo', 'Lugar', '% Equipo', 'Potencia', 'Horas de la semana', 'kWh', 'Potencia Kobo',
                 'kWh Ajustado','% Ajustado','$ Bimestre', 'Texto','Notas',' ', 'Claves'])
    Fugas = pd.DataFrame(
        columns=['Atacable','Codigo','Ubicacion', 'Equipo', 'Lugar', '% Equipo', 'Potencia', 'Horas de la semana', 'kWh', 'Potencia Kobo',
                 'kWh Ajustado','% Ajustado','$ Bimestre', 'Texto','Notas',' ', 'Claves'])

    Dic=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q']

    print(f"Comenzó el reporte de {Cliente}")
    fecha = datetime.now()
    mes = fecha.strftime("%B").capitalize()
    anho = fecha.strftime("%Y")

    #carpeta_resultados = f"../../Datos de clientes/Clientes 2021/01-Enero/"
    #carpeta_resultados = f"../../Datos de clientes/Clientes 2021/03-Marzo/"
    carpeta_resultados = f"D:\Findero Dropbox/Datos de clientes/Clientes 2021/03-Marzo/"


    clientes = os.listdir(carpeta_resultados)

    booleanos = [Cliente.lower() in c.lower() for c in clientes]
    carpeta_cliente = Cliente

    for idx, valor in enumerate(booleanos):
        if valor:
            carpeta_cliente = clientes[idx]

    carpeta_resultados = carpeta_resultados + f"{carpeta_cliente}/Resultados"

    cliente_ = Cliente.replace(' ', '_')
    archivo_resultados = f"{carpeta_resultados}/Resumen_{cliente_}.xlsx"
    Exx = pd.read_excel(archivo_resultados,sheet_name='Resumen')
    Exx.columns=Dic

    Exx.drop(Exx.index[:12],inplace=True)
    donde=Exx.loc[Exx['A'] == 'Periodo:']
    Exx = Exx.drop(Exx[Exx['C'] == 'Total'].index)
    if not Refri.empty:
        print("Refri")
        Equipo,Fuga = separar_fugasR(Refri)
        Equipos = Equipos.append(Equipo,sort=False)[Equipos.columns.tolist()]
        Fugas   = Fugas.append(Fuga,sort=False)[Fugas.columns.tolist()]

    if not Clust.empty:
        print("Cluster")
        Equipo, Fuga = separar_fugasTV(Clust)
        Equipos = Equipos.append(Equipo, sort=False)[Equipos.columns.tolist()]
        Fugas = Fugas.append(Fuga, sort=False)[Fugas.columns.tolist()]

    if not Lava.empty:
        print("Lava")
        Equipo,Fuga = separar_fugas(Lava)
        Equipos = Equipos.append(Equipo,sort=False)[Equipos.columns.tolist()]
        Fugas   = Fugas.append(Fuga,sort=False)[Fugas.columns.tolist()]

    if not Coci.empty:
        print("Cocina")
        Equipo,Fuga = separar_fugasC(Coci)
        Equipos = Equipos.append(Equipo,sort=False)[Equipos.columns.tolist()]
        Fugas   = Fugas.append(Fuga,sort=False)[Fugas.columns.tolist()]


    if not PCs.empty:
        print("Computo")
        Equipo, Fuga = separar_fugas(PCs)
        Equipos = Equipos.append(Equipo, sort=False)[Equipos.columns.tolist()]
        Fugas = Fugas.append(Fuga, sort=False)[Fugas.columns.tolist()]

    if not Comu.empty:
        print("Comunicaciones")
        Equipo, Fuga = separar_fugas(Comu)
        Equipos = Equipos.append(Equipo, sort=False)[Equipos.columns.tolist()]
        Fugas = Fugas.append(Fuga, sort=False)[Fugas.columns.tolist()]

    if not Cal.empty:
        print("Calefaccion")
        print(Cal)
        Equipo, Fuga = separar_fugasCal(Cal)
        Equipos = Equipos.append(Equipo, sort=False)[Equipos.columns.tolist()]
        Fugas = Fugas.append(Fuga, sort=False)[Fugas.columns.tolist()]

    if not Bomba.empty:
        print("Bomba")
        Equipo, Fuga = separar_fugasBB(Bomba)
        Equipos = Equipos.append(Equipo, sort=False)[Equipos.columns.tolist()]
        Fugas = Fugas.append(Fuga, sort=False)[Fugas.columns.tolist()]

    if not Segu.empty:
        print("Seguridad")
        Equipo, Fuga = separar_fugas(Segu)
        Equipos = Equipos.append(Equipo, sort=False)[Equipos.columns.tolist()]
        Fugas = Fugas.append(Fuga, sort=False)[Fugas.columns.tolist()]

    if not Aire.empty:
        print("Aires Acondicionados")
        Equipo, Fuga = separar_fugasA(Aire)
        Equipos = Equipos.append(Equipo, sort=False)[Equipos.columns.tolist()]
        Fugas = Fugas.append(Fuga, sort=False)[Fugas.columns.tolist()]

    if not Esp.empty:
        print("Especial")
        Equipo,Fuga = separar_fugasE(Esp)
        Equipos = Equipos.append(Equipo,sort=False)[Equipos.columns.tolist()]
        Fugas   = Fugas.append(Fuga,sort=False)[Fugas.columns.tolist()]

    Luminaria.fillna(' ', inplace=True)

    Ldicc=['mr16','mr11','espiral','bombilla','vela','globo','cacahuate','flama','par']
    Luminaria.loc[Luminaria['Tamano'].str.contains('tubo'), 'Tipytam'] = 'tubos'
    Luminaria.loc[Luminaria['Tamano'].isin(Ldicc), 'Tipytam'] = 'focos'
    Luminaria['Tipytam'].fillna('focos', inplace=True)
    print(Luminaria)


    Luminarias['Codigo'] = Luminaria['CodigoN']
    Luminarias['Equipo'] = 'Luces '+ Luminaria['Lugar']
    Luminarias['Lugar']=Luminaria['Lugar'] +' '+ Luminaria['Lugar Especifico']
    Luminarias['Ubicacion'] = 'C'+ Luminaria['Circuito'].apply(str)+' '+Luminaria['Tablero'].apply(str)
    Luminarias['Potencia Kobo'] = Luminaria['Consumo']
    Luminarias['Claves']=Luminaria['Numero'].apply(int)
    Luminarias['Texto']=Luminaria['Notas']
    Luminarias['Notas'] = Luminaria['Notas']
    Luminarias['Tipo'] = Luminaria['Tecnologia']

    Tdos=pd.DataFrame()
    eq=Equipos[['Ubicacion','Equipo','Lugar','Texto']]
    Tdos= Tdos.append(eq)
    eq = Luminarias[['Ubicacion', 'Equipo', 'Lugar', 'Texto']]
    Tdos = Tdos.append(eq)
    eq = Fugas[['Ubicacion', 'Equipo', 'Lugar', 'Texto']]
    Tdos = Tdos.append(eq)
    Tdos =Tdos[['Ubicacion', 'Equipo', 'Lugar', 'Texto']]
    Tdos.columns=['Ubicacion', 'Equipo', 'Lugar', 'Notas']

    Nombre = 'Notas_' + Cliente + '.xlsx'
    writer2 = ExcelWriter(Path.home() / 'Desktop' / Nombre, engine='xlsxwriter')
    Tdos.to_excel(writer2, index=True,startrow=2)
    writer2.save()

    Luminaria['Lugar Especifico'].fillna('_',inplace=True)
    Luminarias['Texto'] = 'Luminaria tipo ' + Luminaria['Tecnologia'] + ' en ' + Luminaria['Lugar'].str.lower() + ' (' + Luminaria[
        'Lugar Especifico'] + ') que consta de ' + Luminaria['Numero'].apply(str) + ' '+Luminaria['Tipytam']+'. Notas: ' + Luminaria['Notas']

    cont=0
    Luminarias=Luminarias.reset_index(drop=True)

    for i in Luminaria['Numero']:
        if i==1:
            #print(Luminarias.loc[cont,'Texto'])
            Luminarias.loc[cont,'Texto'] = Luminarias.loc[cont,'Texto'].replace("focos", 'foco')

        cont = cont + 1

    Luminarias['Texto']=  Luminarias['Texto'].str.replace(r"\( \)",'')
    Luminarias['Texto'] = Luminarias['Texto'].str.replace(".0", '')
    Luminarias['Texto'] = Luminarias['Texto'].str.replace("led", 'LED')

    Equipos.reset_index(inplace=True, drop=True)
    Fugas.reset_index(inplace=True, drop=True)
    Luminarias.reset_index(inplace=True, drop=True)
    Equipos.drop(Equipos[Equipos.Codigo == 'X'].index, inplace=True)
    Equipos.reset_index(inplace=True, drop=True)

    Luminarias.sort_values(by='Lugar', ascending=True, inplace=True)
    Fugas.sort_values(by='Atacable', ascending=True, inplace=True)
    Fugas.sort_values(by='Lugar', ascending=True,inplace=True)

    Equipos.replace(0.01,'NM',inplace=True)

    ExcelDes(Equipos, Luminarias, Fugas, archivo_resultados, Cliente)

    return Equipos, Luminarias, Fugas
