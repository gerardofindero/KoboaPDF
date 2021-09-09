from scipy import stats
import numpy as np
import pandas as pd
import math
from scipy.stats import norm
def caritaLava(consumo,clave):

    kWh = float(consumo)
    Percentil = (1 - stats.norm.sf(x=(np.log(kWh)), loc=3.3034, scale=0.4575424))
    if Percentil>=0.8:
        Ca = 3
    if 0.6<=Percentil<0.8:
        Ca = 2
    if 0.4<=Percentil<0.6:
        Ca = 2
    if 0.3 <= Percentil<0.4:
        Ca = 2
    if 0.3 > Percentil:
        Ca = 1
    print (Ca)
    return Ca


def caritaSeca(consumo,clave):
    kWh=float(consumo)
    Percentil=(1-stats.norm.sf(x=(np.log(kWh)), loc=3.7, scale=1.23))
    if Percentil>0.7:
        Ca=3
    if 0.33<Percentil<0.7:
        Ca=2
    if 0.33 > Percentil:
        Ca=1

    return Ca


def caritaEquipos(consumo,clave):
    kWh=float(consumo)
    print(kWh)
    if kWh>=70:
        Ca = 3
    elif 25<kWh<70:
        Ca = 2
    elif 25 >= kWh:
        Ca = 1

    return Ca


def caritaTV(consumo,clave):
    kWh = float(consumo)

    DatosTV=clave.split(',')
    DAtosTV=DatosTV[2].split('/')
    pulgadas=float(DAtosTV[2])

    CC= kWh - (2.989644 + 0.034468 * 40)/0.2606
    XX=np.log(abs(CC))
    Percentil=(1-stats.norm.sf(x=(XX), loc=3.7, scale=1.23))
    Ahorro=(kWh - math.exp(2.989644 + 0.034468 * pulgadas)) / kWh
    nueva=(1.849608 + 0.034 * pulgadas) ** (1 / 0.13)
    retorno=nueva/(Ahorro*kWh*5.5)
    if Percentil>0.7:
        Ca = 3
    if 0.33<Percentil<0.7:
        Ca = 2
    if 0.33 > Percentil:
        Ca = 1

    return Ca

def caritaBomba(consumo,clave):
    kWh=70
    pulgadas=40
    if kWh>100:
        Ca = 3
    if 50<kWh<100:
        Ca = 2
    if 50 > kWh:
        Ca = 1
    return Ca

def caritaRefri(consumo,clave):
    kWh = float(consumo)

    DatosTV=clave.split(',')
    DAtosTV=DatosTV[1].split('/')

    if kWh>170:
        Ca = 3
    if 100<kWh<170:
        Ca = 2
    if 100 > kWh:
        Ca = 1
    return Ca


def caritaPlancha(consumo,clave):
    media = 1.94
    desStd = 0.6
    consumoTrans = consumo ** 0.3
    percentil = norm.cdf(consumoTrans, loc=float(media), scale=float(desStd))
    Percentil = round(percentil, 2)
    if Percentil>0.66:
        Ca = 3
    if 0.33<Percentil<0.66:
        Ca = 2
    if 0.33 > Percentil:
        Ca = 1
    return Ca

def definircarita(Equipo):
    # Caritas=pd.DataFrame(columns=['Indice','Carita'])
    # Equipos=Equipo.copy()
    #
    #
    # secadora=Equipos[Equipos.D.str.contains('Secadora')]
    # secadorak=secadora[~secadora.D.str.contains('pelo')]
    # Caritas.loc[1, 'Indice']=int(secadorak.index.values[0])
    # Caritas.loc[1,'Carita']=caritaSeca(secadorak.K.values)
    #
    # lavadora=Equipos[Equipos.D.str.contains('Lavadora')]
    # Carita=caritaLava(lavadora.K.values)
    # Caritas.loc[2, 'Indice'] = int(lavadora.index.values[0])
    # Caritas.loc[2, 'Carita'] = Carita
    #
    # tele=Equipos[Equipos.D.str.contains('TV')]
    # cont=3
    # for i in tele.index:
    #     cont=cont+1
    #     Carita=caritaTV(tele.loc[i,('K')])
    #     Caritas.loc[cont, 'Indice'] = i
    #     Caritas.loc[cont, 'Carita'] = Carita
    #
    # Otros=Equipos.drop(Caritas['Indice'].apply(int))
    # #caritaEquipos(kwh)
    # Otros.dropna(subset=['K'],inplace=True)
    #
    # cont=len(Caritas)
    # for i in Otros.index:
    #     cont=cont+1
    #     Carita = caritaEquipos(Otros.loc[i, ('K')])
    #     Caritas.loc[cont, 'Indice'] = i
    #     Caritas.loc[cont, 'Carita'] = Carita


    print('Poniendo caritas...')
    for index,aparato in Equipo.iterrows():
        if pd.notna(aparato[16]):
            clave = aparato[16]
            consumo = aparato[10]
            equipoid = aparato[16].split(',')[0]
            if equipoid == 'RF':
                Carita = caritaRefri(consumo,clave)
            elif equipoid == 'TV':
                Carita = caritaTV(consumo,clave)
            elif equipoid == 'LV':
                Carita =caritaLava(consumo,clave)
            elif equipoid == 'SC':
                Carita =caritaSeca(consumo,clave)
            elif equipoid == 'BG' or equipoid == 'BP':
                Carita =caritaBomba(consumo,clave)
            elif equipoid == 'PL':
                Carita =caritaPlancha(consumo,clave)
            else:
                Carita =caritaEquipos(consumo, clave)

        aparato[0]=Carita

