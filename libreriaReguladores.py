import pandas as pd
import numpy as np
from scipy.stats import norm
def leerLibreriaReguladores():
    try:
        Libreria = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Reguladores/libreria_reguladores.xlsx",
            sheet_name='libreriaReguladores')
        ReguladoresLB = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Reguladores/libreria_reguladores.xlsx",
            sheet_name='dataLB')
        ReguladoresEle = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Reguladores/libreria_reguladores.xlsx",
            sheet_name='dataEle')
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    Libreria.columns = ['A','B', 'C','D','E','F','G']
    ReguladoresLB.columns=['A','B', 'C','D','E','F','G','H']
    ReguladoresEle.columns=['A','B', 'C','D','E','F','G','H']
    return [Libreria, ReguladoresEle, ReguladoresLB]
def determinarReferencia(listDispo):
    dispLB=['refrigerador','lavadora','secadora']
    for disp in listDispo:
        if disp in dispLB:
            return 11
    return 3
def esDispEspecial(listDisp):
    dispEsp=['refrigerador','lavadora','secadora','television']
    for disp in listDisp:
        if disp in dispEsp:
            return True
    return False
def reemplazarPor(ref, VA_max):
    return['regulador x', 600, 2]
def recoProtec(horasUso, mediaVoltaje,desvVoltaje):
    areaDebajo = norm.cdf(115, loc=float(mediaVoltaje), scale=float(desvVoltaje))
    areaEncima = 1-norm.cdf(135, loc=float(mediaVoltaje), scale=float(desvVoltaje))
    ppFuera=areaEncima+areaDebajo
    ppUso=horasUso/24/7
    indicador=ppUso*ppFuera
    print(indicador)
    return indicador<0.01

def evaluarRegulador(toleDisp=False, volEst=False, consumo=0, horasUso=0,listDisp=None, fuga=False,VA_max=10, mediaVoltaje=125, desvVoltaje=5):
    [lib,rgLB,rgEl]= leerLibreriaReguladores()
    DAC=6.1
    refElec=3
    refLB=11
    texto=''
    ref = determinarReferencia(listDisp)
    dispInDisEsp= esDispEspecial(listDisp)
    if toleDisp or volEst:
        porcUso=horasUso/24/60
        ahorroRetirar=(consumo*24*60/1000)*porcUso*DAC
        texto=lib.loc[0,'G'].replace('[ahorroRetirar]',str(np.round(ahorroRetirar)))
        return texto
    else :
        if (consumo <= ref) and (not fuga):
            texto=lib.loc[1,'G']
            return texto

        elif (consumo <= ref) and fuga:
            porcUso = horasUso / 24 / 60
            ahorroReducir = (consumo * 24 * 60 / 1000) * (1 - porcUso) * DAC
            texto=lib.loc[2,'G'].replace('[ahorroReducir]',str(np.round(ahorroReducir,2)))
            return texto

        elif(consumo > ref) and (not fuga):
            if not dispInDisEsp:
                porcUso = horasUso / 24 / 60
                [nombreRegulador, costo, nuevoConsumo] = reemplazarPor(ref, VA_max)
                dineroAhorrado=(consumo-nuevoConsumo)*24*60*DAC*porcUso/1000
                ROI=costo/dineroAhorrado/6
                texto = lib.loc[3,'G'].replace('{nombreRegulador}',nombreRegulador).replace('[añosROI]',str(int(np.ceil(ROI))))
                return texto
            elif dispInDisEsp and (not recProtector):
                porcUso = horasUso / 24 / 60
                [nombreRegulador, costo, nuevoConsumo] = reemplazarPor(ref, VA_max)
                dineroAhorrado = (consumo - nuevoConsumo) * 24 * 60 * DAC * porcUso / 1000
                ROI = costo / dineroAhorrado / 6
                texto = lib.loc[3, 'G'].replace('{nombreRegulador}', nombreRegulador).replace('[añosROI]', str(int(np.ceil(ROI))))
                return texto
            elif dispInDisEsp and recProtector:
                texto=lib.loc[5,'G']
                return texto
        elif(consumo > ref) and fuga:
            if not dispInDisEsp:
                [nombreRegulador, costo, nuevoConsumo] = reemplazarPor(ref, VA_max)
                dineroAhorrado = (consumo - nuevoConsumo) * 24 * 60 * DAC  / 1000
                ROI = costo / dineroAhorrado / 6
                texto = lib.loc[3,'G'].replace('{nombreRegulador}',nombreRegulador).replace('[añosROI]',str(int(np.ceil(ROI))))
                return texto
            elif dispInDisEsp and (not recProtector):
                [nombreRegulador, costo, nuevoConsumo] = reemplazarPor(ref, VA_max)
                dineroAhorrado = (consumo - nuevoConsumo) * 24 * 60 * DAC / 1000
                ROI = costo / dineroAhorrado / 6
                texto = lib.loc[3, 'G'].replace('{nombreRegulador}', nombreRegulador).replace('[añosROI]',
                                                                                              str(int(np.ceil(ROI))))
                return texto
            elif dispInDisEsp and recProtector:
                texto=lib.loc[5,'G']
                return texto

