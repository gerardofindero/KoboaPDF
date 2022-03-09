from scipy import stats
import numpy as np
import pandas as pd
import math
from scipy.stats import norm
from libreriaBombasAlberca import leerLibreriaBA
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


def caritaTV(consumo,clave,potenciaE):
    kWh = float(consumo)
    DatosTV=clave.split(',')
    DAtosTV=DatosTV[2].split('/')
    pulgadas=float(DAtosTV[2])
    potencia = float(DAtosTV[0])
    PotTeorica = math.exp(2.958131 + 0.039028 * pulgadas)
    XX = np.log(potencia) # Logaritmo de la potencia (será útil para calcular percentiles)
    Percentil = stats.norm.cdf((XX-(2.958131 + 0.039028 * pulgadas))/0.2040771) # Percentil de potencia de la TV en cuestión

    if potenciaE>=0:
        potenciaE=1
    uso=(kWh*1000)/(potenciaE*60)

    if kWh>45:
        Ca=3
    else:
        Ca=1
        if Percentil >= 0.9:
            Ca=2





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
    TRef=float(Datos[0])
    TCong = float(Datos[1])
    NomCom=Datos[2]
    TempCom=Datos[3]
    Volumen=float(Datos[4])*0.000022
    #NORMDIST(((kWh*6)^0.1 - (1.738365 + 0.0057272 * Volumen))/0.01962684,0,1,TRUE)

    Ns = 0
    if (TRef < 4) or (TCong < -14): Ns += 1
    if "VN" in Claves: Ns += 1
    if "SU" in Claves: Ns += 1
    percentil   = norm.cdf(((float(kWh)*6.0)**0.1 - (1.738365 + 0.0057272 * Volumen))/0.01962684,loc=0,scale=1)
    percentilNs = norm.cdf((((1-0.07*Ns)*float(kWh)*6.0)**0.1 - (1.738365 + 0.0057272 * Volumen))/0.01962684,loc=0,scale=1)
    if percentil>=0.9:
        if percentilNs>=0.9:
            Ca = 3
        elif percentilNs<0.9:
            Ca = 2
    elif 0.3<=percentil<0.9:
        Ca = 2
    elif percentil<0.3:
        Ca = 1

    return Ca



def caritaMiniB(consumo,Claves):
    kWh = float(consumo)
    ClavesSep=Claves.split(",")
    tipo=ClavesSep[0]
    Datos= ClavesSep[1].split("/")
    TRef= float(Datos[0])
    TCong = float(Datos[1])
    NomCom=float(Datos[2])
    TempCom=float(Datos[3])
    Volumen=float(Datos[4])*0.000022
    Ns = 0
    if (TRef < 4) or (TCong < -14): Ns += 1
    if "VN" in Claves: Ns += 1
    if "SU" in Claves: Ns += 1
    percentil = norm.cdf(((float(kWh) * 6.0) ** 0.1 - (1.738365 + 0.0057272 * Volumen)) / 0.01962684, loc=0, scale=1)
    percentilNs = norm.cdf(
        (((1 - 0.07 * Ns) * float(kWh) * 6.0) ** 0.1 - (1.738365 + 0.0057272 * Volumen)) / 0.01962684, loc=0, scale=1)
    if percentil >= 0.9:
        if percentilNs >= 0.9:
            Ca = 3
        elif percentilNs < 0.9:
            Ca = 2
    elif 0.4 <= percentil < 0.9:
        Ca = 2
    elif percentil < 0.4:
        Ca = 1

    return Ca


def caritaCava(consumo,Claves):
    kWh = float(consumo)
    ClavesSep=Claves.split(",")
    Datos= ClavesSep[1].split("/")
    TRef = float(Datos[0])
    TCong = float(Datos[1])
    NomCom = float(Datos[2])
    TempCom = float(Datos[3])
    Volumen = float(Datos[4])
    formulaV=(Volumen/1300.8)+21.4
    formulaR=(Volumen/1300.8)+51.6
    Ns = 0
    if (TRef < 4) or (TCong < -14): Ns += 1
    if "VN" in Claves: Ns += 1
    if "SU" in Claves: Ns += 1
    if kWh < formulaV              : percentil = 0.20
    elif formulaV <= kWh < formulaR: percentil = 0.50
    else                           : percentil = 0.95
    if kWh * (1 - (Ns * 0.07)) < formulaV      : percentilNs = 0.20
    elif formulaV<= kWh*(1-(Ns*0.07)) <formulaR: percentilNs = 0.50
    else                                       : percentilNs = 0.95

    if percentil >= 0.9:
        if percentilNs >= 0.9:
            Ca = 3
        elif percentilNs < 0.9:
            Ca = 2
    elif 0.3 <= percentil < 0.9:
        Ca = 2
    elif percentil < 0.3:
        Ca = 1
    return Ca


def caritaCongeV(consumo,Claves):

    kWh = float(consumo)
    ClavesSep=Claves.split(",")
    Datos= ClavesSep[1].split("/")
    TRef = float(Datos[0])
    TCong = float(Datos[1])
    Volumen=float(Datos[4])
    formulaV=(Volumen/6863.63)-8.83
    formulaR=(Volumen/3432.19)-17.67
    Ns = 0
    if (TRef < 4) or (TCong < -14): Ns += 1
    if "VN" in Claves: Ns += 1
    if "SU" in Claves: Ns += 1
    if kWh < formulaV              : percentil = 0.20
    elif formulaV <= kWh < formulaR: percentil = 0.50
    else                           : percentil = 0.95
    if kWh * (1 - (Ns * 0.07)) < formulaV              : percentilNs = 0.20
    elif formulaV <= kWh * (1 - (Ns * 0.07)) < formulaR: percentilNs = 0.50
    else                                               : percentilNs = 0.95

    if percentil >= 0.9:
        if percentilNs >= 0.9:
            Ca = 3
        elif percentilNs < 0.9:
            Ca = 2
    elif 0.3 <= percentil < 0.9:
        Ca = 2
    elif percentil < 0.3:
        Ca = 1
    return Ca

def caritaCongeH(consumo,Claves):
    kWh = float(consumo)
    ClavesSep=Claves.split(",")
    Datos= ClavesSep[1].split("/")
    TRef = float(Datos[0])
    TCong = float(Datos[1])
    Volumen=float(Datos[4])
    formulaV=(Volumen/8000.35)-7.58
    formulaR=(Volumen/3955.11)-15.33

    Ns = 0
    if (TRef < 4) or (TCong < -14): Ns += 1
    if "VN" in Claves: Ns += 1
    if "SU" in Claves: Ns += 1
    if kWh < formulaV              : percentil = 0.20
    elif formulaV <= kWh < formulaR: percentil = 0.50
    else                           : percentil = 0.95
    if kWh * (1 - (Ns * 0.07)) < formulaV              : percentilNs = 0.20
    elif formulaV <= kWh * (1 - (Ns * 0.07)) < formulaR: percentilNs = 0.50
    else                                               : percentilNs = 0.95

    if percentil >= 0.9:
        if percentilNs >= 0.9:
            Ca = 3
        elif percentilNs < 0.9:
            Ca = 2
    elif 0.3 <= percentil < 0.9:
        Ca = 2
    elif percentil < 0.3:
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

    if consumo < 70:
        Ca = 1
    elif 70<=consumo<120:
        Ca = 2
    elif consumo >= 120:
        Ca = 3

    return Ca

def caritaBombaP(consumo,clave):
    if consumo < 40:
        Ca = 1
    elif 40 <= consumo <80:
        Ca = 2
    elif consumo >= 80:
        Ca = 3
    return Ca

def caritaBombaG(consumo,clave):
    if consumo <=22:
        Ca=1
    elif 22<consumo<= 60:
        Ca=2
    elif 60<consumo:
        Ca=3
    return Ca

def caritaBombaR(consumo,clave):
    if consumo>=90:
        Ca = 3
    if 35<consumo<90:
        Ca = 2
    if  35 >= consumo:
        Ca = 1
    return Ca

def caritaRegulador(consumo):
    if consumo <= 7:
        Ca = 1
    else:
        Ca = 2
    return Ca


def caritaBombaA(consumo,clave):
    lib, f = leerLibreriaBA()
    f.loc[:, "Potencia"] = f.loc[:, "Potencia"].astype(float)
    ClavesS = clave.split(",")

    kwhc, wc, Vc = ClavesS[1].split("/")
    kwhc = float(kwhc)
    wc = float(wc)
    Vc = float(Vc)
    f.loc[:, "Diferencia"] = ((f.loc[:, "Potencia"] * 735.5) - wc).abs()  # Comparación de potencia
    flujo = f.at[f.loc[:, "Diferencia"].idxmin(), "Flujo(m3/h)"]  # flujo aproximado de la bomba
    if "CO" in clave:
        n = 9

    else:
        n = 2

    tq = Vc * n / flujo  # horas al día para recircular el agua n veces, acorde al tipo de uso
    tw = kwhc * 1000 / wc / 60  # número de horas al día que funciona la bomba (ver Kobo->Caritas)
    if tw <= tq:
        Ca = 1
    elif tw > tq and tw <= tq*1.2:
        Ca = 2
    elif tw > tq and tw > tq*1.2:
        Ca = 3

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

def caritaCP(consumo,clave):
    if consumo <= 27:
        Ca = 1
    elif 27 < consumo <= 68:
        Ca = 2
    elif 68 < consumo:
        Ca = 3
    return Ca

def definircarita(Equipo):
    for index,aparato in Equipo.iterrows():
        print(aparato)
        if pd.notna(aparato[16]):
            clave = aparato[16]
            consumo = aparato[10]
            potencia = aparato[6]
            equipoid = aparato[16].split(',')[0]
            equipoi = aparato[16].split('/')[0]

            if equipoid == 'RF':
                Carita = caritaRefri(consumo,clave)
            elif equipoid == 'CN':
                Carita = caritaCongeV(consumo,clave)
            elif equipoid == 'MB':
                Carita = caritaMiniB(consumo,clave)
            elif equipoid == 'CV':
                Carita = caritaCava(consumo,clave)
            elif equipoid == 'HL':
                Carita = caritaHielos(consumo,clave)
            elif equipoid == 'TV':
                Carita = caritaTV(consumo,clave,potencia)
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
            elif equipoid == "BA":
                Carita = caritaBombaA(consumo,clave)
            elif equipoid == 'PL':
                Carita =caritaPlancha(consumo,clave)
            elif equipoid == 'MC':
                Carita =caritaMicroondas(consumo,clave)
            elif equipoid == 'CF':
                Carita =caritaCafetera(consumo,clave)
            elif equipoi == 'AA':
                Carita =caritaAires(consumo,clave)
            elif equipoid == 'DA':
                Carita =caritaDispensador(consumo,clave)
            elif equipoid == "CP":
                Carita = caritaCP(consumo,clave)
            else:
                Carita =caritaEquipos(consumo, clave)


        aparato[0]=Carita

