from SepararFugas import *
from pandas import ExcelWriter
from pathlib         import Path
import pandas as pd
import xlwings
from Tarifa          import leer_tarifa_Dac
from Leer_Lista      import leer_lista
import numpy as np
from Carpeta_Clientes import carpeta_clientes

def tipoluces(tipo):
    tipoGen='focos'
    tipoGen='tubos'
    tipoGen='tiras'


#### Excel
def ExcelDes(Equipos, Luminarias, Fugas,archivo_resultados,Cliente)    :

    FugasC=Fugas.copy()
    LuminariasC=Luminarias.copy()

    Atacable = Fugas['Atacable'].values
    Fugas.drop(['Atacable'], axis=1, inplace=True)
    Fugas.reset_index(inplace=True, drop=True)
    Tipo = Luminarias['Tipo'].values
    Numero = Luminarias['Numero'].values.astype(int)
    Luminarias.drop(['Numero'], axis=1, inplace=True)
    Luminarias.drop(['Tipo'], axis=1, inplace=True)
    Luminarias.reset_index(inplace=True, drop=True)



    workbook = xlwings.Book(archivo_resultados)
    gris = (200, 200, 200)
    Consumo_bimestral = '=Resumen!A9'
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
    Sheet1.range(len(Equipos) + 9, 17).value = 'Entrada y Tipo'

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



############## Rellena con Atacables y tipo de luminaria ##############3
    i = 0
    inicioL = len(Equipos) + 10
    Sheet1.range(inicioL - 1, 1).value = 'Numero y Tipo'
    Tipo= ' '+Tipo
    Tipo= Numero.astype(str) + Tipo

    for tipo in Tipo:
        Sheet1.range(inicioL + i, 1).value = tipo
        i = i + 1

    i=0
    inicioL = len(Equipos) + len(Luminarias) + 13
    Sheet1.range(inicioL -1, 1).value = 'Atacable'
    for atac in Atacable:
        Sheet1.range(inicioL + i, 1).value = atac
        i=i+1





####### Color y Bordes ##################
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

    Sheet1.range('N11').api.WrapText = True



###################### Parte de matchear códigos PP y QQ ###############################
    infoL= leer_lista(Cliente)
    infoL['B']=infoL['B'].str.upper()
    cony=0
    infoL['J'].fillna('X')
    print(infoL['J'])
    for i in Equipos['Codigo']:
        i = i.upper()
        identificados= infoL[infoL['B'].str.contains(i)].index
        if not identificados.empty:
            Sheet1.range(7 + cony, 6).value =infoL.loc[identificados[0],'D']
            Sheet1.range(7 + cony, 7).value = infoL.loc[identificados[0], 'F']
            Sheet1.range(7 + cony, 16).value = infoL.loc[identificados[0], 'H']
            Sheet1.range(7 + cony, 8).value = infoL.loc[identificados[0], 'J']

        else:
            Sheet1.range(7 + cony, 8).value ='=K8 * 1000 / J8'


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
    Fugas['Codigo'].fillna('FF',inplace=True)
    for i in Fugas['Codigo']:
        i = i.upper()
        identificados = infoL[infoL['B'].str.contains(i)].index
        if not identificados.empty:
            Sheet1.range(inicioF + cony, 6).value = infoL.loc[identificados[0], 'D']
        cony=cony+1

    workbook.save()
    workbook.close()


################### Hoja de Potencial de ahorro ####################################


    Luminarias = pd.DataFrame(columns=['Claves','Tipo', 'Luces', 'Ubicacion Exacta',
                                       'kWh en Recibo', 'Pesos en Recibo', 'Uso actual', 'Acción considerada',
                                       'Reduccion', 'kWh de ahorro', 'Pesos de ahorro',
                                       'Costo de equipos a implementar', 'Retorno de la inversión', 'Rentable'])
    Fugas = pd.DataFrame(columns=['Claves','Atacable', 'Fuga', 'Ubicacion Exacta',
                                  'kWh en Recibo', 'Pesos en Recibo', 'Uso actual', 'Acción considerada',
                                  'Reduccion', 'kWh de ahorro', 'Pesos de ahorro', 'Costo de equipos a implementar',
                                  'Retorno de la inversión', 'Rentable'])

    Equipos = pd.DataFrame(columns=[' ',' ', 'Equipo', 'Ubicacion Exacta',
                                    'kWh en Recibo', 'Pesos en Recibo', 'Uso actual', 'Acción considerada',
                                    'Reduccion', 'kWh de ahorro', 'Pesos de ahorro', 'Costo de equipos a implementar',
                                    'Retorno de la inversión', 'Rentable'])


############################### POTENCIAL DE AHORRO ##########################################3
    workbook = xlwings.Book(archivo_resultados)
    try:
        workbook.sheets.add('Potencial de ahorro')
    except:
        print('Hoja ya creada')

    Sheet1 = workbook.sheets['Potencial de ahorro']
    Sheet1.range('B1').value = 'Reporte Potencial de ahorro de '
    Sheet1.range('C3').value = 'Ahorro en kWh'
    Sheet1.range('D3').value = 'Ahorro en Pesos'

    Sheet1.range('D3').api.Font.Bold = True
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
    Sheet1.range('G5').value = 5.8

    Fuga = FugasC[FugasC['Atacable'].str.contains('Si', regex=False, na=False)]
    Fugas['Claves'] = Fuga['Claves']
    Fugas['Atacable'] = Fuga['Atacable']
    Fugas['Fuga'] = Fuga['Equipo']
    Fugas['Ubicacion Exacta'] = Fuga['Lugar']
    Fugas['kWh en Recibo'] = 0
    Fugas['Pesos en Recibo'] = 0
    Fugas['Uso actual'] = '24 Horas'
    Fugas['Acción considerada'] = 'Apagar cuando no se use, puede usarse un Timer inteligente'
    Fugas['Reduccion'] = 0.8

    Luminaria = LuminariasC[~LuminariasC['Tipo'].str.contains('led', regex=False, na=False)]
    Luminarias['Claves'] = Luminaria['Claves']
    Luminarias['Tipo'] = Luminaria['Tipo']
    Luminarias['Luces'] = 'Luminaria tipo ' + Luminaria['Tipo']
    Luminarias['Ubicacion Exacta'] = Luminaria['Lugar']
    Luminarias['kWh en Recibo'] = 0
    Luminarias['Pesos en Recibo'] = 0
    Luminarias['Uso actual'] = ' '
    Luminarias['Acción considerada'] = 'Cambiar a iluminación tipo LED, Apagar cuando no se use'
    Luminarias['Reduccion'] = np.select([Luminarias['Tipo'] == 'incandecente', Luminarias['Tipo'] == 'fluorecente',
                                         Luminarias['Tipo'] == 'halogeno'], ["0.7", "0.4", "0.6"])


    Sheet1.range('A10').options(pd.DataFrame, index=False).value= Fugas
    Sheet1.range(len(Fugas) + 12, 1 ).options(pd.DataFrame, index=False).value = Luminarias


    inicioF = 11
    for i in range(len(Fugas)):
        Sheet1.range(inicioF + i, 10).value = '=E' + str(inicioF + i) + '*( I' + str(inicioF + i) + ')'
        Sheet1.range(inicioF + i, 11).value = '=J' + str(inicioF + i) + ' * G$5'


    inicioF = len(Fugas) + 13
    for i in range(len(Luminarias)):
        Sheet1.range(inicioF + i, 10).value = '=E' + str(inicioF + i) + '*( I' + str(inicioF + i) + ')'
        Sheet1.range(inicioF + i, 11).value = '=J' + str(inicioF + i) + ' * G$5'

    Sheet1.range('C4').value = '= SUM(J11:J' + str(len(Fugas) + 11) + ')'
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


    return Equipos, Luminarias, Fugas

# FUNCION QUE CREA PESTANA DE EXCEL 'DESCIFRAMIENTO'

def Archivo(Cliente,Luz,Clust,Coci,Esp,Lava,Refri,Bomba,PCs,Comu,Cal,Segu,Aire,Tluz):

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

    archivo_resultados = carpeta_clientes(Cliente)
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
        print(Equipos)

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



    regusDF= Fugas.loc[Fugas['Equipo'].str.contains('Regulador')]
    print(regusDF)

    Luminaria.fillna(' ', inplace=True)
    Ldicc=['mr16','mr11','espiral','bombilla','vela','globo','cacahuate','flama','par']
    Luminaria.loc[Luminaria['TipoyTam'].str.contains('tubo'), 'Tipytam'] = 'tubos'
    Luminaria.loc[Luminaria['TipoyTam'].isin(Ldicc), 'Tipytam'] = 'focos'
    Luminaria['Tipytam'].fillna('focos', inplace=True)
    Luminarias['Numero'] = Luminaria['Numero']
    Luminarias['Codigo'] = Luminaria['CodigoN']
    Luminarias['Equipo'] = 'Luces '+ Luminaria['Lugar']
    Luminarias['Lugar']=Luminaria['Lugar'] +' '+ Luminaria['LugarEs']
    Luminarias['Ubicacion'] = 'C'+ Luminaria['Circuito'].apply(str)+' '+Luminaria['Tablero'].apply(str)
    Luminarias['Potencia Kobo'] = Luminaria['Consumo']

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

    Luminaria['LugarEs'].fillna('_',inplace=True)
    #Luminarias['Texto'] = 'Luminaria tipo ' + Luminaria['Tecnologia'] + ' en ' + Luminaria['Lugar'].str.lower() + ' (' + Luminaria[
    #    'Lugar Especifico'] + ') que consta de ' + Luminaria['Numero'].apply(str) + ' '+Luminaria['Tipytam']+'. Notas: ' + Luminaria['Notas']

    Luminarias['Texto']=Tluz #+' '+ Luminaria['TipoyTam']+'  '+ Luminaria['Entrada']
    Luminarias['Claves'] = Luminaria['TipoyTam'] + ' ' + Luminaria['Entrada']

    cont=0
    Luminarias=Luminarias.reset_index(drop=True)

    # for i in Luminaria['Numero']:
    #     if i==1:
    #         #print(Luminarias.loc[cont,'Texto'])
    #         Luminarias.loc[cont,'Texto'] = Luminarias.loc[cont,'Texto'].replace("focos", 'foco')
    #
    #     cont = cont + 1

    # Luminarias['Texto']=  Luminarias['Texto'].str.replace(r"\( \)",'')
    # Luminarias['Texto'] = Luminarias['Texto'].str.replace(".0", '')
    # Luminarias['Texto'] = Luminarias['Texto'].str.replace("led", 'LED')

    Equipos.reset_index(inplace=True, drop=True)
    Fugas.reset_index(inplace=True, drop=True)
    Luminarias.reset_index(inplace=True, drop=True)
    Equipos.drop(Equipos[Equipos.Codigo == 'X'].index, inplace=True)
    Equipos.reset_index(inplace=True, drop=True)

    Luminarias.sort_values(by='Lugar', ascending=True, inplace=True)
    Fugas.sort_values(by='Atacable', ascending=True, inplace=True)
    Fugas.sort_values(by='Lugar', ascending=True,inplace=True)

    Equipos.replace(0.01,'NM',inplace=True)

    # j = 0
    # for i in Luminarias.index:
    #     j = j + 1
    #     num = 'L' + str(j)
    #     Luminarias.loc[i, 'Claves'] = num
    j=0
    for i in Fugas.index:
        j = j + 1
        num = 'FG' + str(j)
        Fugas.loc[i, 'Claves'] = num


    ExcelDes(Equipos, Luminarias, Fugas, archivo_resultados, Cliente)


