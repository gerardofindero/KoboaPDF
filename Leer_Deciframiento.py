import datetime
import os
from datetime import datetime
import pandas as pd
from Carpeta_Clientes import carpeta_clientes

def leer_deciframiento(Cliente):
    archivo_resultados =  carpeta_clientes(Cliente)
    Exx = pd.read_excel(archivo_resultados, sheet_name='Desciframiento')
    ExL = pd.read_excel(archivo_resultados, sheet_name='Lista')

    Tarifa =Exx.columns[6]

    Dic = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L','M','N','O','P','Q']
    Exx.columns = Dic
    Consumo=Exx.loc[1,['C']]
    Costo=Exx.loc[1,['D']]
    Solar =Exx.loc[2, ['G']]

    Exx.dropna(subset=['C'],inplace=True)
    #Exx.fillna(0,inplace=True)
    Luces = Exx[Exx['D'].str.contains('Luces', regex=False,na=False)]
    Fugas = Exx[Exx['D'].str.contains('Fuga', regex=False, na=False)]
    EXX   = Exx[~Exx['D'].str.contains('Luces', regex=False,na=False)]
    Aparatos = EXX[~EXX['D'].str.contains('Fuga', regex=False,na=False)]
    Aparatos = Aparatos[~Aparatos['B'].str.contains('Codigo', regex=False, na=False)]


    Aparatos.drop([0,1],inplace=True)

    ConsumoFugas=Fugas['K'].sum()

    return Aparatos,Luces,Fugas,Consumo,Costo,Tarifa, ConsumoFugas, Solar

def leer_potencial(Cliente):
    archivo_resultados = carpeta_clientes(Cliente)
    Exx = pd.read_excel(archivo_resultados, sheet_name='Potencial de ahorro')
    Dic = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L','M','N']
    Exx.columns = Dic
    Exx.dropna(subset=['C'],inplace=True)
    #Exx.fillna(0,inplace=True)
    Luces = Exx[Exx['C'].str.contains('Luminaria', regex=False,na=False)]
    Fugas = Exx[Exx['C'].str.contains('Fuga', regex=False, na=False)]
    EXX   = Exx[~Exx['C'].str.contains('Luces', regex=False,na=False)]
    Aparatos = EXX[~EXX['C'].str.contains('Fuga', regex=False,na=False)]
    return Aparatos,Luces,Fugas



def leer_solar(Cliente):
    archivo_resultados = carpeta_clientes(Cliente)
    Exx = pd.read_excel(archivo_resultados, sheet_name='Resumen')
    Dic = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
    Exx.columns = Dic

    DSolar = pd.DataFrame(index=['Produccion','MaxW','MaxkWh','Min','Medidor','ProduccionSem','ProduccionBim'],
                        columns=['F1','F2','F3','Total'])

    DSolar.loc['Produccion','F1']= Exx.loc[1, ['O']][0]
    DSolar.loc['MaxW', 'F1']      = Exx.loc[3, ['O']][0]
    DSolar.loc['MaxkWh', 'F1']    = Exx.loc[4, ['O']][0]
    DSolar.loc['Min', 'F1']       = Exx.loc[5, ['O']][0]

    DSolar.loc['Produccion', 'F2']=Exx.loc[1, ['P']][0]
    DSolar.loc['MaxW', 'F2'] = Exx.loc[3, ['P']][0]
    DSolar.loc['MaxkWh', 'F2'] = Exx.loc[4, ['P']][0]
    DSolar.loc['Min', 'F2'] = Exx.loc[5, ['P']][0]

    DSolar.loc['Produccion', 'F3']=Exx.loc[1, ['Q']][0]
    DSolar.loc['MaxW', 'F3'] = Exx.loc[3, ['Q']][0]
    DSolar.loc['MaxkWh', 'F3'] = Exx.loc[4, ['Q']][0]
    DSolar.loc['Min', 'F3'] = Exx.loc[5, ['Q']][0]

    DSolar.loc['Medidor', 'Total'] = Exx.loc[7, ['Q']][0]
    DSolar.loc['ProduccionSem', 'Total'] = Exx.loc[7, ['O']][0]
    DSolar.loc['ProduccionBim', 'Total'] = Exx.loc[7, ['P']][0]



    return (DSolar)