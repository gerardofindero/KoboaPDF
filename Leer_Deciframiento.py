
import pandas as pd
from Carpeta_Clientes import carpeta_clientes

def leer_deciframiento(Cliente):
    archivo_resultados =  carpeta_clientes(Cliente)
    Exx = pd.read_excel(archivo_resultados, sheet_name='Desciframiento')
    #ExL = pd.read_excel(archivo_resultados, sheet_name='Lista')

    Tarifa =Exx.columns[6]

    Dic = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L','M','N','O','P','Q']
    Exx.columns = Dic
    Consumo=Exx.loc[1,['C']]
    Costo=Exx.loc[1,['D']]
    Solar =Exx.loc[2, ['G']]
    Voltaje = Exx.loc[1, ['G']]
    Exx.dropna(subset=['C'],inplace=True)
    #Exx.fillna(0,inplace=True)
    Luces = Exx[Exx['D'].str.contains('Luces', regex=False,na=False)]
    Fugas = Exx[Exx['D'].str.contains('Fuga', regex=False, na=False)]
    EXX   = Exx[~Exx['D'].str.contains('Luces', regex=False,na=False)]
    Aparatos = EXX[~EXX['D'].str.contains('Fuga', regex=False,na=False)]
    Aparatos = Aparatos[~Aparatos['B'].str.contains('Codigo', regex=False, na=False)]
    Aparatos.drop([0,1],inplace=True)
    ConsumoFugas=Fugas['K'].sum()

    return Aparatos,Luces,Fugas,Consumo,Costo,Tarifa, ConsumoFugas, Solar,Voltaje

def leer_potencial(Cliente):
    archivo_resultados = carpeta_clientes(Cliente)
    Exx = pd.read_excel(archivo_resultados, sheet_name='PotPrueba')
    Dic = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L','M','N']
    Exx.columns = Dic
    Ahorro=Exx.loc[5,'C']
    return Ahorro

def leer_resumen(Cliente):
    archivo_resultados = carpeta_clientes(Cliente)
    Exx = pd.read_excel(archivo_resultados, sheet_name='Resumen')
    Dic = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
    Exx.columns = Dic
    Datos = Exx.loc[0, ['G']][0]
    return Datos


def leer_solar(Cliente):
    archivo_resultados = carpeta_clientes(Cliente)
    Exx = pd.read_excel(archivo_resultados, sheet_name='Resumen')
    Dic = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
    Exx.columns = Dic

    DSolar = pd.DataFrame(index=['Produccion','MaxW','MaxkWh','Min','Medidor','ProduccionSem','ProduccionBim'],
                        columns=['F1','F2','F3','Total'])

    DSolar.loc['Produccion','F1']= Exx.loc[1, ['J']][0]
    DSolar.loc['MaxW', 'F1']      = Exx.loc[9, ['J']][0]
    DSolar.loc['MaxkWh', 'F1']    = Exx.loc[5, ['J']][0]
    DSolar.loc['Min', 'F1']       = Exx.loc[7, ['J']][0]

    DSolar.loc['Produccion', 'F2']= Exx.loc[1, ['K']][0]
    DSolar.loc['MaxW', 'F2'] =      Exx.loc[9, ['K']][0]
    DSolar.loc['MaxkWh', 'F2'] =    Exx.loc[5, ['K']][0]
    DSolar.loc['Min', 'F2'] =       Exx.loc[7, ['K']][0]

    DSolar.loc['Produccion', 'F3']  = Exx.loc[1, ['L']][0]
    DSolar.loc['MaxW', 'F3']        = Exx.loc[9, ['L']][0]
    DSolar.loc['MaxkWh', 'F3']      = Exx.loc[5, ['L']][0]
    DSolar.loc['Min', 'F3']         = Exx.loc[7, ['L']][0]

    DSolar.loc['Medidor', 'Total'] = Exx.loc[11, ['L']][0]
    DSolar.loc['ProduccionSem', 'Total'] = Exx.loc[13, ['L']][0]

    DSolar.loc['Produccion','F1']= Exx.loc[3, ['J']][0]
    DSolar.loc['MaxW', 'F1']      = Exx.loc[5, ['J']][0]
    DSolar.loc['MaxkWh', 'F1']    = Exx.loc[7, ['J']][0]
    DSolar.loc['Min', 'F1']       = Exx.loc[9, ['J']][0]

    DSolar.loc['Produccion', 'F2']=Exx.loc[3, ['K']][0]
    DSolar.loc['MaxW', 'F2'] = Exx.loc[5, ['K']][0]
    DSolar.loc['MaxkWh', 'F2'] = Exx.loc[7, ['K']][0]
    DSolar.loc['Min', 'F2'] = Exx.loc[9, ['K']][0]

    DSolar.loc['Produccion', 'F3']=Exx.loc[3, ['L']][0]
    DSolar.loc['MaxW', 'F3'] = Exx.loc[5, ['L']][0]
    DSolar.loc['MaxkWh', 'F3'] = Exx.loc[7, ['L']][0]
    DSolar.loc['Min', 'F3'] = Exx.loc[9, ['L']][0]

    DSolar.loc['Medidor', 'Total'] = Exx.loc[16, ['L']][0]
    DSolar.loc['ProduccionSem', 'Total'] = Exx.loc[12, ['L']][0]
    DSolar.loc['ProduccionBim', 'Total'] = int( DSolar.loc['ProduccionSem', 'Total'])*int(Exx.loc[0, ['E']][0])



    return (DSolar)