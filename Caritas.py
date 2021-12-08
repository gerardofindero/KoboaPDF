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

def caritaMicroondas(consumo,clave):
    kWh=float(consumo)
    media  =2.38
    desStd =0.79
    consumoTrans= consumo**0.4
    percentil= norm.cdf(consumoTrans,loc=float(media),scale=float(desStd))
    Percentil=round(percentil,2)
    if Percentil>0.90:
        Ca=3
    elif 0.90 >= Percentil>=0.50:
        Ca=2
    else:
        Ca=1


    return Ca

def caritaCafetera(consumo,clave):
    kWh=float(consumo)
    media = 2.38
    dstd  = 2.39
    kwh = kWh**0.42
    Percentil= norm.cdf(kwh,loc=media,scale=dstd)

    if Percentil>0.55:
        Ca=2
    if 0.55 >= Percentil:
        Ca=1
    if kWh >35:
        Ca=3

    return Ca



def caritaEquipos(consumo,clave):
    kWh=float(consumo)
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
    potencia = float(DAtosTV[0])
    PotTeorica = math.exp(2.958131 + 0.039028 * pulgadas)
    XX = np.log(potencia) # Logaritmo de la potencia (será útil para calcular percentiles)
    Percentil = stats.norm.cdf((XX-(2.958131 + 0.039028 * pulgadas))/0.2040771) # Percentil de potencia de la TV en cuestión
    uso=(kWh*1000)/(potencia*60)

    if uso >= 3.5:
        Ca=3
    else:
        Ca=1
    if Percentil >= 0.9:
        Ca=2
    if kWh>45:
        Ca = 3

    # elif (1 <= uso < 3.5) or (Percentil >= 0.9):
    #         Ca = 2
    # elif (uso < 1 or kWh<15) and (Percentil < 0.9):
    #     Ca = 1

    return Ca

def caritaRefri(consumo,Claves):
    kWh = float(consumo)

    ClavesSep=Claves.split(",")
    tipo=ClavesSep[0]
    Datos= ClavesSep[1].split("/")
    TRef=Datos[0]
    TCong = Datos[1]
    NomCom=Datos[2]
    TempCom=Datos[3]
    Volumen=13
    #Volumen=float(Datos[4])

    #NORMDIST(((kWh*6)^0.1 - (1.738365 + 0.0057272 * Volumen))/0.01962684,0,1,TRUE)
    percentil= norm.cdf(((float(kWh)*6.0)**0.1 - (1.738365 + 0.0057272 * Volumen))/0.01962684,loc=0,scale=1)
    # if percentil>=0.99:
    #     Ca = 3
    # if 0.5<=percentil<0.99:
    #     Ca = 2
    # if 0.5 > percentil:
    #     Ca = 1


    if kWh>150:
        Ca = 3
    if 95<kWh<=150:
        Ca = 2
    if 95 >= kWh:
        Ca = 1

    return Ca



def caritaMiniB(consumo,Claves):
    kWh = float(consumo)

    ClavesSep=Claves.split(",")
    tipo=ClavesSep[0]
    Datos= ClavesSep[1].split("/")
    TRef=Datos[0]
    TCong = Datos[1]
    NomCom=Datos[2]
    TempCom=Datos[3]
    Volumen=13
    #Volumen=float(Datos[4])
    if kWh>150:
        Ca = 3
    if 100<kWh<=150:
        Ca = 2
    if 100 >= kWh:
        Ca = 1

    return Ca


def caritaCava(consumo,Claves):
    kWh = float(consumo)
    ClavesSep=Claves.split(",")
    Datos= ClavesSep[1].split("/")
    TRef=Datos[0]
    TCong = Datos[1]
    NomCom=Datos[2]
    TempCom=Datos[3]
    Volumen=13
    #Volumen=float(Datos[4])

    if kWh>150:
        Ca = 3
    if 100<kWh<=150:
        Ca = 2
    if 100 >= kWh:
        Ca = 1

    return Ca


def caritaPlancha(consumo,clave):
    if consumo>33:
        Ca = 3
    if 19<=consumo<33:
        Ca = 2
    if 19 > consumo:
        Ca = 1

    return Ca


def caritaAires(consumo,clave):
    if consumo>=500:
        Ca = 3
    if 200<consumo<300:
        Ca = 2
    if  200 >= consumo:
        Ca = 1
    return Ca

def caritaBombaP(consumo,clave):
    if consumo>=90:
        Ca = 3
    if 35<consumo<90:
        Ca = 2
    if  35 >= consumo:
        Ca = 1
    return Ca

def caritaBombaG(consumo,clave):
    if consumo>=90:
        Ca = 3
    if 35<consumo<90:
        Ca = 2
    if  35 >= consumo:
        Ca = 1
    return Ca

def caritaBombaR(consumo,clave):
    if consumo>=90:
        Ca = 3
    if 35<consumo<90:
        Ca = 2
    if  35 >= consumo:
        Ca = 1
    return Ca


def caritaDispensador(consumo,clave):
    if consumo>=40:
        Ca = 3
    if 20<consumo<40:
        Ca = 2
    if  20 >= consumo:
        Ca = 1
    return Ca

def caritaHielos(consumo,clave):
    if consumo>=40:
        Ca = 3
    if 20<consumo<40:
        Ca = 2
    if  20 >= consumo:
        Ca = 1
    return Ca

def definircarita(Equipo):
    for index,aparato in Equipo.iterrows():
        if pd.notna(aparato[16]):
            clave = aparato[16]
            consumo = aparato[10]
            equipoid = aparato[16].split(',')[0]
            if equipoid == 'RF':
                Carita = caritaRefri(consumo,clave)
            elif equipoid == 'CN':
                Carita = caritaRefri(consumo,clave)
            elif equipoid == 'MB':
                Carita = caritaMiniB(consumo,clave)
            elif equipoid == 'CV':
                Carita = caritaCava(consumo,clave)
            elif equipoid == 'HL':
                Carita = caritaHielos(consumo,clave)
            elif equipoid == 'TV':
                Carita = caritaTV(consumo,clave)
            elif equipoid == 'LV':
                Carita =caritaLava(consumo,clave)
            elif equipoid == 'SC':
                Carita =caritaSeca(consumo,clave)
            elif equipoid == 'BP':
                Carita =caritaBombaP(consumo,clave)
            elif equipoid == 'BR':
                Carita =caritaBombaG(consumo,clave)
            elif equipoid == 'BG':
                Carita =caritaBombaG(consumo,clave)
            elif equipoid == 'PL':
                Carita =caritaPlancha(consumo,clave)
            elif equipoid == 'MC':
                Carita =caritaMicroondas(consumo,clave)
            elif equipoid == 'CF':
                Carita =caritaCafetera(consumo,clave)
            elif equipoid == 'AA':
                Carita =caritaAires(consumo,clave)
            elif equipoid == 'DA':
                Carita =caritaDispensador(consumo,clave)
            else:
                Carita =caritaEquipos(consumo, clave)

        aparato[0]=Carita

