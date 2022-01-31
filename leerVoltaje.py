import datetime
import os
from datetime import datetime
import pandas as pd
from Carpeta_Clientes import carpeta_clientes

def leer_volts(Cliente):
    archivo_resultados =carpeta_clientes(Cliente)
    Exx = pd.read_excel(archivo_resultados, sheet_name='Resumen')
    Dic = ['A', 'B', 'C', 'D','E', 'F', 'G', 'H','I','J','K','L','M','N','O','P','Q']
    Exx.columns = Dic
    Exx.fillna('0',inplace=True)

    DsEst = Exx.loc[11,'F']
    Media =Exx.loc[12,'F']
    MaxMin =Exx.loc[13,'F']
    MAxMin = MaxMin.split('/')
    Max=    float(MAxMin[0])
    Min=    float(MAxMin[1])
    NSub = Exx.loc[15,'E']
    NSob = Exx.loc[15,'F']
    TSub = Exx.loc[15,'G']
    TSob = Exx.loc[15,'H']


    if Max<135:
        if (Media+(2*(DsEst)))<135:
            VFE=True
            if Min>105:
                if 105 < (Media+(2*(DsEst))):
                    if (Media-(2*(DsEst)))>105:
                        VFM=True


    return VFE,VFM,NSub,NSob,TSub,TSob