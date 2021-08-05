import datetime
import os
from datetime import datetime
import pandas as pd
from Carpeta_Clientes import carpeta_clientes

def leer_volts(Cliente):
    archivo_resultados =carpeta_clientes(Cliente)
    Exx = pd.read_excel(archivo_resultados, sheet_name='Resumen')
    #Dic = ['A', 'B', 'C', 'D', 'I','E', 'F', 'G', 'H']
    Dic = ['A', 'B', 'C', 'D','E', 'F', 'G', 'H','I','J','K','L','M','N','O','P','Q']
    Exx.columns = Dic
    Exx.fillna('0',inplace=True)
    #print(Exx[Exx['A'].str.contains('Circuito')])
    subset=Exx[["O", "P","Q"]]

    print(subset)
    VFE = False
    VFM = False
    VoltajeF1 = (subset.loc[0,'O']+subset.loc[0,'P']+subset.loc[0,'Q'])/3
    VoltajeMxF1 = subset.loc[3, 'O']
    VoltajeMnF1 = subset.loc[6, 'O']
    DsEst = subset.loc[1, 'O']
    print(VoltajeF1)

    if VoltajeMxF1<135:
        if (VoltajeF1+(2*(DsEst)))<135:
            VFE=True
            if VoltajeMnF1>105:
                if 105 < (VoltajeF1+(2*(DsEst))):
                    if (VoltajeF1-(2*(DsEst)))>105:
                        VFM=True

    print(VFE)
    print(VFM)
    Voltajes = [VFE,VFM]


    #print(infoL)
    return Voltajes