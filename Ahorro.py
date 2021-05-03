import pandas as pd
import numpy as np
import xlsxwriter
from xlsxwriter import workbook
from xlsxwriter.utility import xl_rowcol_to_cell, xl_range
from xlsxwriter.utility import xl_cell_to_rowcol
from pandas import ExcelWriter
import xlwings
from pathlib         import Path
import os

def ahorro_luces(Luces):
     Luces_=Luces.copy()
     periodo=8.6
     tarifa=5.52
     Luces_.replace(np.nan, '_', inplace=True)
     luces_A = pd.DataFrame(columns=['Tipo','Iluminacion', 'Ubicacion',
                                     'kWh en recibo' ,'Pesos en Recibo', 'Uso actual', 'Acción considerada',
                                     'reduccion', 'kWh de ahorro', 'Pesos de ahorro' ,'Costo de equipos a implementar','Retorno de la inversión','Rentable'])
     luces_A['Tipo']=Luces_['Tecnologia']
     luces_A['kWh en recibo'] = Luces_['Consumo']*periodo
     luces_A['Pesos en Recibo'] = luces_A['kWh en recibo']*tarifa
     luces_A['Iluminacion']= Luces_['Tecnologia']+' '+ Luces_['Tamano'] +' '+ Luces_['Entrada']
     luces_A['Ubicacion']   = Luces_['Lugar'] + ' / ' +  Luces_['Lugar Especifico']
     luces_A['Acción considerada'] = 'Sustituir por Luminaria LED'

     luces_A.loc[luces_A['Tipo'] == 'halogeno', 'reduccion'] = 0.7
     luces_A.loc[luces_A['Tipo'] == 'incandescente', 'reduccion'] = 0.6
     luces_A.loc[luces_A['Tipo'] == 'fluorescente', 'reduccion'] = 0.4
     luces_A.loc[luces_A['Tipo'] == 'led', 'reduccion'] = 0.0
     luces_A.loc[luces_A['Tipo'] == 'tira_led', 'reduccion'] = 0.0

     luces_A['kWh de ahorro']=(luces_A['reduccion'])*luces_A['kWh en recibo']
     luces_A['Pesos de ahorro'] = luces_A['kWh de ahorro'] * tarifa


     luces_A = luces_A[luces_A.reduccion != 0]

     return luces_A

def ahorro_cluster(cluster):
     clusterTV=cluster.copy()
     # print(clusterTV)
     # clusterTV.drop(index='Lugar',inplace=True)
     periodo=8.6
     tarifa=5.52
     tiempoUso=95
     tiempoPeriodo=166
     reduccionT=tiempoUso/tiempoPeriodo
     clusterTV_A = pd.DataFrame(columns=['Equipo','Consumo', 'Ubicacion',
                                     'kWh en recibo', 'Pesos en Recibo', 'Uso actual', 'Acción considerada',
                                     'reduccion', 'kWh de ahorro', 'Pesos de ahorro','Costo de equipos a implementar','Retorno de la inversión','Rentable'])

     clusterTV.dropna(subset=['Standby'],inplace=True)
     clusterTV = clusterTV[clusterTV.Standby != 0]
     clusterTV.reset_index(inplace=True)
     clusterTV_A['Equipo'] = clusterTV['index'] + ' '+ clusterTV['Marca'].apply(str)
     clusterTV_A['Consumo'] = clusterTV['Standby']
     clusterTV_A['kWh en recibo'] = clusterTV['Standby'] * periodo
     clusterTV_A['Pesos en Recibo'] = clusterTV_A['kWh en recibo'] * tarifa
     clusterTV_A['Ubicacion'] = clusterTV['Zona']
     clusterTV_A['Acción considerada'] = 'Implementar Timer inteligente'
     clusterTV_A['reduccion'] = reduccionT
     clusterTV_A['kWh de ahorro'] = (clusterTV_A['reduccion']) * clusterTV_A['kWh en recibo']
     clusterTV_A['Pesos de ahorro'] = clusterTV_A['kWh de ahorro'] * tarifa

     return (clusterTV_A)

def ahorro_cocina(coci):
     cocinaF = coci.copy()
     #CocinaF.drop(index='Lugar', inplace=True)
     periodo = 8.6
     tarifa = 5.52
     tiempoUso = 95
     tiempoPeriodo = 166
     reduccionT = tiempoUso / tiempoPeriodo

     cocinaF_A = pd.DataFrame(columns=['Equipo', 'Consumo', 'Ubicacion',
                                         'kWh en recibo', 'Pesos en Recibo', 'Uso actual', 'Acción considerada',
                                         'reduccion', 'kWh de ahorro', 'Pesos de ahorro','Costo de equipos a implementar','Retorno de la inversión','Rentable'])

     cocinaF.dropna(subset=['Standby'], inplace=True)
     cocinaF =  cocinaF[ cocinaF.Standby != 0]
     cocinaF.reset_index(inplace=True)

     cocinaF_A['Equipo'] =  cocinaF['index'] + ' ' +  cocinaF['Marca']

     cocinaF_A['Consumo'] =  cocinaF['Standby']
     cocinaF_A['kWh en recibo'] =  cocinaF['Standby'] * periodo
     cocinaF_A['Pesos en Recibo'] = cocinaF_A['kWh en recibo'] * tarifa
     cocinaF_A['Ubicacion'] =  'Cocina'
     cocinaF_A['Acción considerada'] = 'Implementar Timer inteligente'
     cocinaF_A['reduccion'] = reduccionT
     cocinaF_A['kWh de ahorro'] = (cocinaF_A['reduccion']) * cocinaF_A['kWh en recibo']
     cocinaF_A['Pesos de ahorro'] = cocinaF_A['kWh de ahorro'] * tarifa

     return(cocinaF_A)


def ahorro_comunicaciones(comu):
     comuF = comu.copy()
     periodo = 8.6
     tarifa = 5.52
     tiempoUso = 95
     tiempoPeriodo = 166
     reduccionT = tiempoUso / tiempoPeriodo

     comuF_A = pd.DataFrame(columns=['Equipo', 'Consumo', 'Ubicacion',
                                         'kWh en recibo', 'Pesos en Recibo', 'Uso actual', 'Acción considerada',
                                         'reduccion', 'kWh de ahorro', 'Pesos de ahorro','Costo de equipos a implementar','Retorno de la inversión','Rentable'])
     comuF.dropna(subset=['Standby'], inplace=True)
     comuF =  comuF[ comuF.Standby != 0]
     comuF.reset_index(inplace=True)

     comuF_A['Equipo'] =  comuF['index'] + ' ' +  comuF['Marca']
     comuF_A['Consumo'] =  comuF['Standby']
     comuF_A['kWh en recibo'] =  comuF['Standby'] * periodo
     comuF_A['Pesos en Recibo'] = comuF_A['kWh en recibo'] * tarifa
     comuF_A['Ubicacion'] =  comuF['Zona']
     comuF_A['Acción considerada'] = 'Implementar Timer inteligente'
     comuF_A['reduccion'] = reduccionT
     comuF_A['kWh de ahorro'] = (comuF_A['reduccion']) * comuF_A['kWh en recibo']
     comuF_A['Pesos de ahorro'] = comuF_A['kWh de ahorro'] * tarifa

     return(comuF_A)


def ahorro_especiales(esp):
     espF = esp.copy()


     periodo = 8.6
     tarifa = 5.52
     tiempoUso = 95
     tiempoPeriodo = 166
     reduccionT = tiempoUso / tiempoPeriodo

     espF_A = pd.DataFrame(columns=['Equipo', 'Consumo', 'Ubicacion',
                                         'kWh en recibo', 'Pesos en Recibo', 'Uso actual', 'Acción considerada',
                                         'reduccion', 'kWh de ahorro', 'Pesos de ahorro','Costo de equipos a implementar','Retorno de la inversión','Rentable'])

     espF.dropna(subset=['Standby'], inplace=True)
     espF =  espF[ espF.Standby != 0]
     espF.reset_index(inplace=True)
     espF_A['Equipo'] =  espF['Equipo'] + ' ' +  espF['Marca']
     espF_A['Consumo'] =  espF['Standby']
     espF_A['kWh en recibo'] =  espF['Standby'] * periodo
     espF_A['Pesos en Recibo'] = espF_A['kWh en recibo'] * tarifa
     espF_A['Ubicacion'] =  espF['Zona']
     espF_A['Acción considerada'] = 'Implementar Timer inteligente'
     espF_A['reduccion'] = reduccionT
     espF_A['kWh de ahorro'] = (espF_A['reduccion']) * espF_A['kWh en recibo']
     espF_A['Pesos de ahorro'] = espF_A['kWh de ahorro'] * tarifa

     return(espF_A)



def ahorro_(coci):
     equipo = coci.copy()
     #CocinaF.drop(index='Lugar', inplace=True)
     periodo = 8.6
     tarifa = 5.52
     tiempoUso = 95
     tiempoPeriodo = 166
     reduccionT = tiempoUso / tiempoPeriodo

     Equipo_A = pd.DataFrame(columns=['Equipo', 'Consumo', 'Ubicacion',
                                         'kWh en recibo', 'Pesos en Recibo', 'Uso actual', 'Acción considerada',
                                         'reduccion', 'kWh de ahorro', 'Pesos de ahorro','Costo de equipos a implementar','Retorno de la inversión','Rentable'])

     equipo.dropna(subset=['Standby'], inplace=True)
     equipo =  equipo[ equipo.Standby != 0]
     equipo.reset_index(inplace=True)

     Equipo_A['Equipo'] =  equipo['index'] + ' ' +  equipo['Marca']

     Equipo_A['Consumo'] =  equipo['Standby']
     #cocinaF_A['kWh en recibo'] =  cocinaF['Standby'] * periodo
     #cocinaF_A['Pesos en Recibo'] = cocinaF_A['kWh en recibo'] * tarifa
     Equipo_A['Ubicacion'] =  'Cocina'
     #cocinaF_A['Acción considerada'] = 'Implementar Timer inteligente'
     #cocinaF_A['reduccion'] = reduccionT
     #cocinaF_A['kWh de ahorro'] = (cocinaF_A['reduccion']) * cocinaF_A['kWh en recibo']
     #cocinaF_A['Pesos de ahorro'] = cocinaF_A['kWh de ahorro'] * tarifa




def potencial_ahorro(Cliente,Equipos, Luminaria, Fuga):
     tarifa=5.8
     Dic = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J','K','L','M']
     Luminarias = pd.DataFrame(columns=['Tipo','Luces', 'Ubicacion Exacta',
                                         'kWh en Recibo', 'Pesos en Recibo', 'Uso actual', 'Acción considerada',
                                         'Reduccion', 'kWh de ahorro', 'Pesos de ahorro','Costo de equipos a implementar','Retorno de la inversión','Rentable'])
     Fugas = pd.DataFrame(columns=['Atacable','Fuga', 'Ubicacion Exacta',
                                     'kWh en Recibo', 'Pesos en Recibo', 'Uso actual', 'Acción considerada',
                                     'Reduccion', 'kWh de ahorro', 'Pesos de ahorro','Costo de equipos a implementar','Retorno de la inversión','Rentable'])

     Equipos = pd.DataFrame(columns=[' ', 'Equipo', 'Ubicacion Exacta',
                                   'kWh en Recibo', 'Pesos en Recibo', 'Uso actual', 'Acción considerada',
                                   'Reduccion', 'kWh de ahorro', 'Pesos de ahorro', 'Costo de equipos a implementar',
                                   'Retorno de la inversión', 'Rentable'])

     # Nombre = 'Potencial_ahorro_' + Cliente + '.xlsx'
     #
     #
     # # carpeta_resultados = f"../../Datos de clientes/Clientes 2021/01-Enero/"
     # carpeta_resultados = f"../../Datos de clientes/Clientes 2021/02-Febrero/"
     #
     # clientes = os.listdir(carpeta_resultados)
     # booleanos = [Cliente.lower() in c.lower() for c in clientes]
     # capeta_cliente = Cliente
     # for idx, valor in enumerate(booleanos):
     #      if valor:
     #           carpeta_cliente = clientes[idx]
     # carpeta_resultados = carpeta_resultados + f"{carpeta_cliente}/Resultados"
     #
     # cliente_ = Cliente.replace(' ', '_')
     # archivo_resultados = f"{carpeta_resultados}/Resumen_{cliente_}.xlsx"
     # workbook = xlwings.Book(archivo_resultados)
     try:
          workbook.sheets.add('Potencial de Ahorro')
     except:
          print('Hoja ya creada')

     Sheet1 = workbook.sheets['Potencial de Ahorro']

     Sheet1.range('B1').value = 'Reporte Potencial de ahorro de '
     Sheet1.range('C3').value = 'Ahorro en kWh'
     Sheet1.range('D3').value = 'Ahorro en Pesos'

     Sheet1.range('D4').value = "=C4*G$5"
     Sheet1.range('D5').value = "=C5*G$5"
     Sheet1.range('D6').value = "=C6*G$5"
     Sheet1.range('C7').value = "=SUM(C4:C6)"
     Sheet1.range('D7').value = "=SUM(D4:D6)"


     Sheet1.range('B4').value = 'Subtotal ahorro de fugas'
     Sheet1.range('B5').value = 'Subtotal ahorro de luces'
     Sheet1.range('B6').value = 'Subtotal ahorro de por equipos'
     Sheet1.range('B7').value = 'Potencial ahorro Total'
     Sheet1.range('F4').value = 'Mes'
     Sheet1.range('F5').value = 'Precio/kWh'
     Sheet1.range('G3').value = 'Tarifa '
     Sheet1.range('G5').value = tarifa

     Fuga = Fuga[Fuga['A'].str.contains('Si', regex=False, na=False)]
     Fugas['Atacable'] = Fuga['A']
     Fugas['Fuga'] = Fuga['D']
     Fugas['Ubicacion Exacta'] = Fuga['E']
     Fugas['kWh en Recibo'] = Fuga['K']
     Fugas['Pesos en Recibo'] = Fuga['M']
     Fugas['Uso actual'] = '24 Horas'
     Fugas['Acción considerada']= 'Apagar cuando no se use, puede usarse un Timer inteligente'
     Fugas['Reduccion'] = 0.8

     Luminaria = Luminaria[~Luminaria['A'].str.contains('led', regex=False, na=False)]
     Luminarias['Tipo'] = Luminaria['A']
     Luminarias['Luces'] = Luminaria['D'] + ' tipo ' +Luminaria['A']
     Luminarias['Ubicacion Exacta'] = Luminaria['E']
     Luminarias['kWh en Recibo'] = Luminaria['K']
     Luminarias['Pesos en Recibo'] = Luminaria['M']
     Luminarias['Uso actual'] = ' '
     Luminarias['Acción considerada'] = 'Cambiar a iluminación tipo LED, Apagar cuando no se use'

     # Luminarias['Reduccion'] = np.where(Luminarias['Tipo'] == 'incandecente', '0.7', '')
     # Luminarias['Reduccion'] = np.where(Luminarias['Tipo'] == 'fluorecente', '0.4', '')
     Luminarias['Reduccion']= np.select([Luminarias['Tipo'] =='incandecente', Luminarias['Tipo'] =='fluorecente',
                                         Luminarias['Tipo'] =='halogeno'],["0.7", "0.4","0.6"])
     #Luminarias['Reduccion'] = 0.8
     #Fugas['kWh de ahorro'] = '80%'

     Sheet1.range('A10').value = Fugas
     Sheet1.range(len (Fugas)+12 ,1).value = Luminarias
     Sheet1.range(len(Fugas)+ len(Luminarias) + 14, 1).value = Equipos


     inicioF = 11
     for i in range(len(Fugas)):
          # Sheet1.range(inicioL+i, 8).value = '=E'+str(inicioL+i)+'*C$2'
          Sheet1.range(inicioF + i, 10).value = '=E' + str(inicioF + i) + '*( I'+ str(inicioF + i)+')'
          Sheet1.range(inicioF + i, 11).value = '=J' + str(inicioF + i) + ' * G$5'
          # Sheet1.range(inicioF + i, 13).value = '=K' + str(inicioF + i) + '*G$1'

     inicioF = len(Fugas)+13
     for i in range(len(Luminarias)):
          # Sheet1.range(inicioL+i, 8).value = '=E'+str(inicioL+i)+'*C$2'
          Sheet1.range(inicioF + i, 10).value = '=E' + str(inicioF + i) + '*( I' + str(inicioF + i) + ')'
          Sheet1.range(inicioF + i, 11).value = '=J' + str(inicioF + i) + ' * G$5'
          # Sheet1.range(inicioF + i, 13).value = '=K' + str(inicioF + i) + '*G$1'



     Sheet1.range('C4').value = '= SUM(J11:J'+str(len(Fugas)+11) +')'
     #Sheet1.range('C5').value = 'SUM(' + +')'


     Sheet1.range("$B$3:$D$7").api.Borders.Weight = 2
     Sheet1.range("$F$3:$H$5").api.Borders.Weight = 2

     LargoFugas=len(Fugas)+10
     cuadroceldas="$B$10:$N$"+ str(LargoFugas)
     Sheet1.range(cuadroceldas).api.Borders.Weight = 2

     LargoFugas = len(Fugas)+len(Luminarias) + 12
     cuadroceldas = "$B$"+str(len(Fugas)+12) +":$N$" + str(LargoFugas)
     Sheet1.range(cuadroceldas).api.Borders.Weight = 2

     LargoFugas = len(Fugas) + len(Luminarias) + 15
     cuadroceldas = "$B$" + str(len(Fugas) + len(Luminarias) + 14) + ":$N$" + str(LargoFugas)
     Sheet1.range(cuadroceldas).api.Borders.Weight = 2

     #Sheet1.range(CelF).columns.autofit()
     Sheet1['1:1'].api.ColumnWidth = 15
     Sheet1.range('B1').column_width = 25
     Sheet1.range('C1').column_width = 35
     Sheet1.range('H1').column_width = 55
     Sheet1.range('D1').column_width = 25
     #Sheet1.range('O1').column_width = 100
     gris = (200, 200, 200)
     for i in range(13):
          Sheet1.range(10, i + 2).color = gris
          Sheet1.range(len(Fugas) + 12, i + 2).color = gris
          Sheet1.range(len(Fugas)+len(Luminarias) + 14, i + 2).color = gris


def potencial_ahorro2(Cliente,fugas, luces,fugasK,lucesK):
     carpeta_resultados = f"../../../Datos de clientes/Clientes 2021/03-Marzo/"

     clientes = os.listdir(carpeta_resultados)
     booleanos = [Cliente.lower() in c.lower() for c in clientes]
     capeta_cliente = Cliente
     for idx, valor in enumerate(booleanos):
          if valor:
               carpeta_cliente = clientes[idx]
     carpeta_resultados = carpeta_resultados + f"{carpeta_cliente}/Resultados"

     cliente_ = Cliente.replace(' ', '_')
     archivo_resultados = f"{carpeta_resultados}/Resumen_{cliente_}.xlsx"
     workbook = xlwings.Book(archivo_resultados)
     print(lucesK)

     #iguales=np.where(luces['Q'] ==
