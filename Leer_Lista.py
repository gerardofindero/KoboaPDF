import datetime
import os
from datetime import datetime
import pandas as pd
from Carpeta_Clientes import carpeta_clientes

def leer_lista(Cliente):
    archivo_resultados =carpeta_clientes(Cliente)
    Exx = pd.read_excel(archivo_resultados, sheet_name='Lista')
    # Dic = ['A', 'B', 'C', 'D', 'I','E', 'F', 'G', 'H']
    # Dic = ['A', 'B', 'C', 'D','K', 'I','E', 'F', 'G', 'H','J']
    Dic = ['A', 'B', 'C', 'D', 'I','K','E', 'F', 'G', 'H','J']
    Exx.columns = Dic
    Exx.fillna('0',inplace=True)
    infoL=Exx.drop(['A','C','E','G'],axis=1)
    infoL=infoL.drop(0)

    return infoL