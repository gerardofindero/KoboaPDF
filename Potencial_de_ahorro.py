import pandas as pd
import numpy as np
from Leer_Deciframiento import leer_deciframiento
import xlwings
from Carpeta_Clientes import carpeta_clientes
def potecial_ahorro(Cliente):


    Aparatos, LuminariasC, FugasC, Consumo, Costo, Tarifa, ConsumoFugas, Solar, Voltaje=leer_deciframiento(Cliente)

    print(LuminariasC.columns)

    archivo_resultados = carpeta_clientes(Cliente)
    workbook = xlwings.Book(archivo_resultados)
    gris = (200, 200, 200)
    #Consumo_bimestral = '=Resumen!A9'
    #Tarifa = leer_tarifa_Dac()

    ################### Hoja de Potencial de ahorro ####################################

    Luminarias = pd.DataFrame(columns=['Claves', 'Tipo', 'Luces', 'Ubicacion Exacta',
                                       'kWh en Recibo', 'Pesos en Recibo', 'Uso actual', 'Acción considerada',
                                       'Reduccion', 'kWh de ahorro', 'Pesos de ahorro',
                                       'Costo de equipos a implementar', 'Retorno de la inversión', 'Rentable'])
    Fugas = pd.DataFrame(columns=['Claves', 'Atacable', 'Fuga', 'Ubicacion Exacta',
                                  'kWh en Recibo', 'Pesos en Recibo', 'Uso actual', 'Acción considerada',
                                  'Reduccion', 'kWh de ahorro', 'Pesos de ahorro', 'Costo de equipos a implementar',
                                  'Retorno de la inversión', 'Rentable'])

    Equipos = pd.DataFrame(columns=[' ', ' ', 'Equipo', 'Ubicacion Exacta',
                                    'kWh en Recibo', 'Pesos en Recibo', 'Uso actual', 'Acción considerada',
                                    'Reduccion', 'kWh de ahorro', 'Pesos de ahorro', 'Costo de equipos a implementar',
                                    'Retorno de la inversión', 'Rentable'])

    ############################### POTENCIAL DE AHORRO ##########################################3
    workbook = xlwings.Book(archivo_resultados)
    try:
        workbook.sheets.add('PotPrueba')
    except:
        print('Hoja ya creada')

    Sheet1 = workbook.sheets['PotPrueba']
    Sheet1.range('B1').value = 'Reporte Potencial de ahorro de '
    Sheet1.range('C3').value = 'Ahorro en kWh'
    Sheet1.range('D3').value = 'Ahorro en Pesos'

    #Sheet1.range('D3').api.Font.Bold = True
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
    Sheet1.range('G5').value = '=Desciframiento!G1'

    Fuga = FugasC[FugasC['A'].str.contains('Si', regex=False, na=False)]

    Fugas['Claves'] = Fuga['Q']
    Fugas['Atacable'] = Fuga['A']
    Fugas['Fuga'] = Fuga['D']
    Fugas['Ubicacion Exacta'] = Fuga['E']
    Fugas['kWh en Recibo'] = Fuga['K']
    Fugas['Pesos en Recibo'] = Fuga['M']
    Fugas['Uso actual'] = '24 Horas'
    Fugas['Acción considerada'] = 'Apagar cuando no se use, puede usarse un Timer inteligente'
    Fugas['Reduccion'] = 0.8
    Fugas['Costo de equipos a implementar'] = 250


    Luminaria = LuminariasC[~LuminariasC['A'].str.contains('led', regex=False, na=False)]

    Luminarias['Claves'] = Luminaria['Q']
    Luminarias['Tipo'] = Luminaria['A']
    Luminarias['Luces'] = 'Luminaria tipo ' + Luminaria['A']
    Luminarias['Ubicacion Exacta'] = Luminaria['E']
    Luminarias['kWh en Recibo'] = Luminaria['K']
    Luminarias['Pesos en Recibo'] =Luminaria['M']
    Luminarias['Uso actual'] = Luminaria['H']
    Luminarias['Acción considerada'] = 'Cambiar a iluminación tipo LED, Apagar cuando no se use'
    Luminarias['Costo de equipos a implementar'] = 50

    Sheet1.range('A10').options(pd.DataFrame, index=False).value = Fugas
    Sheet1.range(len(Fugas) + 12, 1).options(pd.DataFrame, index=False).value = Luminarias

    inicioF = 11
    Fugas.reset_index(drop=True,inplace=True)
    for i in Fugas.index:
        Sheet1.range(inicioF + i, 10).value = '=E' + str(inicioF + i) + '*( I' + str(inicioF + i) + ')'
        Sheet1.range(inicioF + i, 11).value = '=J' + str(inicioF + i) + ' * G$5'
        Sheet1.range(inicioF + i, 13).value = '=L' + str(inicioF + i) + '/( K' + str(inicioF + i) + ')'
        Sheet1.range(inicioF + i, 14).value = '=IF(M' + str(inicioF + i) + '<18,"Si","No")'

    inicioF = len(Fugas) + 13
    Luminarias.reset_index(drop=True,inplace=True)
    for i in Luminarias.index:
        print(Luminarias.loc[i,'Tipo'])
        if 'halogena' in Luminarias.loc[i,'Tipo']:
            Sheet1.range(inicioF + i, 9).value = 0.6
        if 'fluorescente' in Luminarias.loc[i,'Tipo']:
            Sheet1.range(inicioF + i, 9).value = 0.4
        if 'incandescente' in Luminarias.loc[i,'Tipo']:
            Sheet1.range(inicioF + i, 9).value = 0.8

        numero=Luminarias.loc[i,'Tipo'].split(' ')[0]
        Sheet1.range(inicioF + i, 12).value = int(numero)*50
        Sheet1.range(inicioF + i, 10).value = '=E' + str(inicioF + i) + '*( I' + str(inicioF + i) + ')'
        Sheet1.range(inicioF + i, 11).value = '=J' + str(inicioF + i) + ' * G$5'
        Sheet1.range(inicioF + i, 13).value = '=L' + str(inicioF + i) + '/( K' + str(inicioF + i) + ')'
        Sheet1.range(inicioF + i, 14).value = '=IF(M' + str(inicioF + i)+'<18,"Si","No")'


    Sheet1.range('C4').value = '=SUMIF((N11:N'+str(len(Fugas) + 10)+'),"Si",(J11:J'+str(len(Fugas) + 10)+'))'
    Sheet1.range('C5').value = '=SUMIF((N'+ str(len(Fugas) + 19)+':N' + str(len(Luminarias) + 19) + '),"Si",(J'+ str(len(Fugas) + 19)+':J' + str(len(Luminarias) + 19)+'))'
    Sheet1.range("$B$3:$D$7").api.Borders.Weight = 2
    Sheet1.range("$F$3:$H$5").api.Borders.Weight = 2

    LargoFugas = len(Fugas) + 10
    cuadroceldas = "$A$10:$N$" + str(LargoFugas)
    Sheet1.range(cuadroceldas).api.Borders.Weight = 2

    LargoFugas = len(Fugas) + len(Luminarias) + 12
    cuadroceldas = "$A$" + str(len(Fugas) + 12) + ":$N$" + str(LargoFugas)
    Sheet1.range(cuadroceldas).api.Borders.Weight = 2

    LargoFugas = len(Fugas) + len(Luminarias) + 15
    cuadroceldas = "$A$" + str(len(Fugas) + len(Luminarias) + 14) + ":$N$" + str(LargoFugas)
    Sheet1.range(cuadroceldas).api.Borders.Weight = 2

    Sheet1['1:1'].api.ColumnWidth = 15
    Sheet1.range('B1').column_width = 25
    Sheet1.range('C1').column_width = 35
    Sheet1.range('H1').column_width = 55
    Sheet1.range('D1').column_width = 25

    gris = (200, 200, 200)
    for i in range(14):
        Sheet1.range(10, i + 1).color = gris
        Sheet1.range(len(Fugas) + 12, i + 1).color = gris
        Sheet1.range(len(Fugas) + len(Luminarias) + 14, i + 1).color = gris

    workbook.save()
    #workbook.close()