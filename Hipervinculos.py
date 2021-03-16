import datetime
import os
from datetime import datetime
import pandas as pd
import xlwings


def hipervinculos(Cliente):
    print('Creando hipervinculos')
    fecha = datetime.now()
    mes = fecha.strftime("%B").capitalize()
    anho = fecha.strftime("%Y")
    #carpeta_resultados = f"../../Datos de clientes/Clientes {anho}/01-enero/"
    carpeta_resultados = f"../../Datos de clientes/Clientes {anho}/03-Marzo/"
    clientes = os.listdir(carpeta_resultados)
    booleanos = [Cliente.lower() in c.lower() for c in clientes]
    carpeta_cliente = Cliente
    for idx, valor in enumerate(booleanos):
        if valor:
            carpeta_cliente = clientes[idx]
    carpeta_resultados = carpeta_resultados + f"{carpeta_cliente}/Resultados"
    cliente_ = Cliente.replace(' ', '_')
    archivo_resultados = f"{carpeta_resultados}/Resumen_{cliente_}.xlsx"
    Res = pd.read_excel(archivo_resultados, sheet_name='Resumen')
    Dic = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I','J','K','L','M','N','O','P','Q']
    Dicc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q','R']
    Res.columns = Dic
    Res[['A', 'B']] = Res[['A', 'B']].fillna(method = 'pad')
    Des = pd.read_excel(archivo_resultados, sheet_name='Desciframiento')
    Des.columns = Dicc
    Des.drop([0,1,2,3,4],inplace=True)
    Des.dropna(subset=['C'],inplace=True)
    Res.drop(Res.index[:9], inplace=True)
    # Des = Des.replace('C', '')
    Res = Res[Res.A != 'Periodo:']
    Res = Res[Res.B != 'Tablero']
    #print(Res)
    Des['C'] = Des['C'].str.capitalize()
    circuitoD = Des['C'][Des.C != 'Ubicacion']
    circuitoD = circuitoD.str.split(' ', 1)
    Res.dropna(subset=['D'], inplace=True)
    Res['D'] = Res['D'].astype(str)
    circuitoR = Res[['B', 'D']]
    #print(circuitoR)
    valorT = len(set(Res['B']))
    print(valorT)
    #print(len(valorT))
    circuitoR['B'] = circuitoR['B'].str.lower()
    circuitoR['D'] = circuitoR['D'].str.split().str.get(0)
    workbook = xlwings.Book(archivo_resultados)
    Sheet1 = workbook.sheets['Desciframiento']
    for i in circuitoD.index:
        try:
            circ=int(circuitoD[i][0][1:])
            tab = circuitoD[i][1][0:]
            donde = circuitoR[int(circuitoR) == circ].index 
            
        except:
            circ = circuitoD[i][0][1:]
            tab = circuitoD[i][1][0:]
            donde = circuitoR[circuitoR== circ].index
        if valorT > 3:
            if not donde.empty:
                for j in donde.values:
                    if circuitoR['B'][j]==tab and circuitoR['D'][j]==circ:
                        Puerto =Res['C'][j]
                        Findero=Res['A'][j]
                        Hvin= '../Graficas/Consumo/'+ str(Findero) +'/'  + str(Findero) +'Puerto ' + str(Puerto) +'.html'
                        Sheet1.range(i+2,3).add_hyperlink(Hvin,str(Des.loc[i,'C']))
        else:
           if not donde.empty:
               for j in donde.values:
                   if circuitoR['D'][j]==circ:
                       Puerto =Res['C'][j]
                       Findero=Res['A'][j]
                       Hvin= '../Graficas/Consumo/'+ str(Findero) +'/'  + str(Findero) +'Puerto ' + str(Puerto) +'.html'
                       Sheet1.range(i+2,3).add_hyperlink(Hvin,str(Des.loc[i,'C']))
    workbook.save()
    workbook.close()