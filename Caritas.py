from scipy import stats
import numpy as np
import pandas as pd
import math

def caritaLava(kwh):
    kWh = float(kwh)
    Percentil=(1-stats.norm.sf(x=(np.log(kWh)), loc=3.3034, scale=0.4575424))


    if Percentil>0.7:

        Ca = 3
    if 0.33<Percentil<0.7:

        Ca = 2
    if 0.33 > Percentil:

        Ca = 1
    return Ca


def caritaSeca(kwh):
    kWh=float(kwh)
    Percentil=(1-stats.norm.sf(x=(np.log(kWh)), loc=3.7, scale=1.23))
    if Percentil>0.7:

        Ca=3
    if 0.33<Percentil<0.7:

        Ca=2
    if 0.33 > Percentil:

        Ca=1

    return Ca


def caritaEquipos(kwh):
    kWh=float(kwh)
    Percentil=(1-stats.norm.sf(x=(np.log(kWh)), loc=3.7, scale=1.23))
    print(kWh)
    if kWh>=30:
        Ca = 3
    elif 15<kWh<30:
        Ca = 2
    elif 15 >= kWh:
        Ca = 1

    return Ca


def caritaTV(kwh):
    kWh = float(kwh)
    pulgadas=40
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

def caritaBomba():
    kWh=70
    pulgadas=40
    if kWh>60:

        Ca = 3
    if 30<kWh<60:

        Ca = 2
    if 0.30 > kWh:

        Ca = 1


def definircarita(Equipo):
    Caritas=pd.DataFrame(columns=['Indice','Carita'])
    Equipos=Equipo.copy()
    secadora=Equipos[Equipos.D.str.contains('Secadora')]
    secadorak=secadora[~secadora.D.str.contains('pelo')]
    Caritas.loc[1, 'Indice']=int(secadorak.index.values[0])
    Caritas.loc[1,'Carita']=caritaSeca(secadorak.K.values)

    lavadora=Equipos[Equipos.D.str.contains('Lavadora')]
    Carita=caritaLava(lavadora.K.values)
    Caritas.loc[2, 'Indice'] = int(lavadora.index.values[0])
    Caritas.loc[2, 'Carita'] = Carita

    tele=Equipos[Equipos.D.str.contains('TV')]
    cont=3
    for i in tele.index:
        cont=cont+1
        Carita=caritaTV(tele.loc[i,('K')])
        Caritas.loc[cont, 'Indice'] = i
        Caritas.loc[cont, 'Carita'] = Carita

    Otros=Equipos.drop(Caritas['Indice'].apply(int))
    #caritaEquipos(kwh)
    Otros.dropna(subset=['K'],inplace=True)

    cont=len(Caritas)
    for i in Otros.index:
        cont=cont+1
        Carita = caritaEquipos(Otros.loc[i, ('K')])
        Caritas.loc[cont, 'Indice'] = i
        Caritas.loc[cont, 'Carita'] = Carita

    return (Caritas)

