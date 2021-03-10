import pandas as pd
from datetime import datetime

def leer_tarifa_Dac():
    meses_lista = {'Enero':1, ' Febrero':2, 3: '03 Marzo',
                   4: '04 Abril', 5: '05 Mayo', 6: '06 Junio',
                   7: '07 Julio', 8: '08 Agosto', 9: '09 Septiembre',
                   10: '10 Octubre', 11: '11 Noviembre', 12: '12 Diciembre'}
    print('Leyendo tarifas')
    #Tarifas = pd.read_excel(r'D:/01 Findero/Findero Dropbox/Tarifas/Lista_Tarifas.xlsx', sheet_name='DAC')
    Tarifas = pd.read_excel(r'D:/Findero Dropbox/Tarifas/Lista_Tarifas.xlsx', sheet_name='DAC')
    fecha = datetime.now()
    mes = fecha.strftime("%B").capitalize()
    anho = fecha.strftime("%Y")
    anhoActual= int(anho)-1913
    TarifaDAC=round(float(Tarifas.loc[anhoActual+datetime.now().month, ['Central']].values*1.16),3)
    #print(datetime.now().month)
    print('La tarifa actual es de:' + str(TarifaDAC))

    return TarifaDAC
#D:\01 Findero\Findero Dropbox\Tarifas