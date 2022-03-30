import pandas as pd
import numpy as np
from scipy.stats import norm
import funcionesComunes as fc
from leerVoltaje import leer_volts

def leerLibReg():
    """
    libReg -> libreria con textos
    dbReg  -> Base de datos de reguladores
    dbPro  -> base de datos de protectores de voltaje
    :return: librerias con formato
    """
    try:
        libReg = pd.read_excel(
            f"../../../Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Reguladores/libreria_reguladores.xlsx",
            sheet_name='libreriaReguladoresN')
        dbReg = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Reguladores/libreria_reguladores.xlsx",
            sheet_name='data')
        dbPro = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Reguladores/libreria_reguladores.xlsx",
            sheet_name='protectorVoltaje')
    except:
        dbReg = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Reguladores/libreria_reguladores.xlsx",
            sheet_name='data')
        libReg = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Reguladores/libreria_reguladores.xlsx",
            sheet_name='libreriaReguladoresN')
        dbPro = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Reguladores/libreria_reguladores.xlsx",
            sheet_name='protectorVoltaje')

    libReg = libReg.set_index("Codigo")
    dbPro  = dbPro.set_index("variable")

    return [dbReg,libReg,dbPro]


def armarTxt_NAtac(Claves):
    """
    Crear texto para reguladores no atacables
    :param Claves:
    EL      El regulador se ocupa para dispositivos puramente electronicos (TV, consolas, pc etc)
    MC      El regulador se ocupa para aparatos mecanicos (Refris, lavadoras, etc)
    EE      El volatje del domicilio es estable para uso electronico
    EM      El voltaje del domicilio es estable para uso mecanico
    TO      Todos los equipos conectados al regulador tienen una amplia toleracia a variaciones de voltaje
    :return:
    """

    dbReg, lib, dbPro = leerLibReg()
    txt=""
    clavesS = Claves.split(",")
    nombre =  clavesS[1]

    if "EL" in Claves:
        txt += lib.at["REG03F","Texto"]

    if "MC" in Claves:
        txt += lib.at["REG06F","Texto"]

    linkSP = dbPro.at["[linkSP]","link"]
    linkPV = dbPro.at["[linkPV]","link"]
    txt = txt.replace("[linkSP]",fc.ligarTextolink("Supresor de picos",linkSP))
    txt = txt.replace("[linkSP]",fc.ligarTextolink("Protector de voltaje",linkPV))
    txt = txt.replace("[nombre]",nombre)
    return txt


def armarTxt_Atac(Claves,standby,voltaje):
    """
    Funcio para crear texto de reguladores atacables
    :param Claves:
    EL      El regulador se ocupa para dispositivos puramente electronicos (TV, consolas, pc etc)
    MC      El regulador se ocupa para aparatos mecanicos (Refris, lavadoras, etc)
    EE      El volatje del domicilio es estable para uso electronico
    EM      El voltaje del domicilio es estable para uso mecanico
    TO      Todos los equipos conectados al regulador tienen una amplia toleracia a variaciones de voltaje
    :param standby: consumo pasivo del regulador del cliente
    :param voltaje: Variable con el comportamiento de la señal de voltaje en la casa del cliente
            voltaje[0] -> Estabilidad del voltaje para uso electronico
            voltaje[1] -> Estabilidad del voltaje para uso mecanico
            voltaje[2] -> Número de picos de subvoltaje
            voltaje[3] -> Número de picos de sobrevoltaje
            voltaje[4] -> Tiempo que el voltaje estuvo por debajo del umbral inferior
            voltaje[5] -> Tiempo que el volatje estuvo por encima del umbral superior
    :return: Recomendación automatica
    """
    EE = False
    EM = False
    rangoE = voltaje[0]
    rangoM = voltaje[1]
    nSub = voltaje[2]
    nSob = voltaje[3]
    tSub = voltaje[4]
    tSob = voltaje[5]
    if rangoE:
        EE = True
    elif (nSob < 7) and (tSob < 0.17):
        EE = True

    if rangoM:
        EM = True
    elif ((nSob + nSub) < 7) and ((tSub + tSob) < 0.17):
        EM = True

    dbReg, lib, dbPro = leerLibReg()
    txt = ""
    clavesS = Claves.split(",")
    nombre = clavesS[1]
    wC=clavesS[-1]
    # sección de reguladores de uso electronico
    if "EL" in Claves:
        # si el regulador es atacble se busca un regulador más eficiente
        [roi, rec] = reemplazo("EL", standby, wC, dbReg)
        if EE:
            txt += lib.loc["REG01F", "Texto"]
        elif "TO" in Claves:
            txt += lib.loc["REG02F", "Texto"]
        else:
            if roi:
                txt += lib.loc["REG03Fb","Texto"]

    # sección de reguladores mecanicos
    if "MC" in Claves:
        # si el regulador es atacble se busca un regulador más eficiente
        [roi, rec] = reemplazo("MC", standby, wC, dbReg)
        if EM:
            txt += lib.at["REG04F","Texto"]
        else:
            if roi:
                txt += lib.loc["REG06Fb","Texto"]

    if roi:
        txt = txt.replace("[linkReco]",fc.ligarTextolink("Regulador recomendado",rec.at[0,"link"]))
    linkSP = dbPro.loc["[linkSP]","link"]
    linkPV = dbPro.loc["[linkPV]","link"]
    txt = txt.replace("[linkSP]",fc.ligarTextolink("Supresor de picos",linkSP)) # protector de voltaje para equipos electronicos
    txt = txt.replace("[linkPV]",fc.ligarTextolink("Protector de voltaje",linkPV)) # protector de voltaje para equipos mecanicos
    txt = txt.replace("[nombre]",nombre)
    txt+= "<br /><br />"
    return txt



def armarTxtE(kwh):
    """
    Recomendación para reguladores en la sección de equipos del reprote
    :param kwh: consumo de kwh al bimestre del regulador
    :return:
    """
    dbReg, lib, dbPro = leerLibReg()
    txt = ""
    if kwh <= 7:
        txt+=lib.at["REG01E","Texto"]
    else:
        txt+= lib.at["REG02E","Texto"]
    linkSP = dbPro.at["[linkSP]","link"]
    txt = txt.replace("[linkSP]",fc.ligarTextolink("Supresor de picos",linkSP))
    return txt

def reemplazo(uso,standby,wC,dbReg):
    """
    Función para buscar un regulador mas eficiente
    :param uso:     elec es uso electrico (Tvs, compuso, modems, etc) y meca es uso mecanico (refris, lavadoras,etc)
    :param standby: potencia que consumo el regulador del cliente
    :param wC:      suma de la potencia de los equipos conectados al regulador
    :param dbReg:   base de datos con las opciones de reemplazo de regulador
    :return: roi -> bandera booleana si se encontro al menos un regulador para recomendar
             rec -> dataframe con la informaición del regulador recomendado
    """
    # se da un colchon de %20 para asegurar que el regulador seleccioando pueda soprotar los equipos del cliente
    wC = float(wC) *1.20

    # Si wC es igual a 10000 es un valor arbitrario que se usa cuando no se pudo medir el estandby del regulador
    if wC==10000*1.20:
        roi=False
        rec=None
    # Seccion de reguladores de uso electronico

    elif "EL" == uso:
        #filta la base de datos por tipo de uso, potencia maxima y estandby
        filt = (dbReg.uso == "elec") & ( dbReg.w<=wC ) & ( dbReg.standby<standby )
        if filt.sum() > 0:
            # se ordenan los reguladores por el standby que manejan
            rec = dbReg.loc[dbReg.index[filt][0], :].reset_index(drop=True).copy()
            roi = True
        else:
            roi = False
            rec = None

    elif "MC" == uso:
        # Sección de reguladores de uso mecánico
        filt = (dbReg.uso == "meca") & (dbReg.w <= wC) & (dbReg.standby < standby)
        if filt.sum()>0:
            rec = dbReg.loc[dbReg.index[filt][0],:].reset_index(drop=True).copy()
            roi = True
        else:
            roi = False
            rec = None
    else:
        roi = False
        rec = None

    return [roi,rec]

def Atac_Mec(voltaje,standby,wC):
    """
    Función para determianr si un regulador de uso mecánico es atacable en el excel de desciframiento
    :param voltaje: lista con información de la estabilidad del voltaje
            voltaje[0] -> Estabilidad del voltaje para uso electronico
            voltaje[1] -> Estabilidad del voltaje para uso mecanico
            voltaje[2] -> Número de picos de subvoltaje
            voltaje[3] -> Número de picos de sobrevoltaje
            voltaje[4] -> Tiempo que el voltaje estuvo por debajo del umbral inferior
            voltaje[5] -> Tiempo que el volatje estuvo por encima del umbral superior
    :param standby: consumo pasivo del regulador
    :param wC:      suma de las potencias de los equipos conectados al regulador
    :return:        Si o No
    """
    # stand by del regulador
    # watts de lo que tenia conectado
    [dbReg, libReg, dbPro] = leerLibReg()
    rangoE = voltaje[0]
    rangoM = voltaje[1]
    nSub = voltaje[2]
    nSob = voltaje[3]
    tSub = voltaje[4]
    tSob = voltaje[5]
    if rangoM:
        Atac = 'Si'
    elif (nSob < 7) and (tSob < 0.17):
        Atac = 'Si'
    else:
        [roi,rec] = reemplazo("MC",standby,wC,dbReg)
        if roi:
            Atac = "Si"
        else:
            Atac = "No"



    return Atac



def Atac_Elec(voltaje,standby,wC):
    """
        Función para determianr si un regulador de uso mecánico es atacable en el excel de desciframiento
        :param voltaje: lista con información de la estabilidad del voltaje
            voltaje[0] -> Estabilidad del voltaje para uso electronico
            voltaje[1] -> Estabilidad del voltaje para uso mecanico
            voltaje[2] -> Número de picos de subvoltaje
            voltaje[3] -> Número de picos de sobrevoltaje
            voltaje[4] -> Tiempo que el voltaje estuvo por debajo del umbral inferior
            voltaje[5] -> Tiempo que el volatje estuvo por encima del umbral superior
        :param standby: consumo pasivo del regulador
        :param wC:      suma de las potencias de los equipos conectados al regulador
        :return:        Si o No
    """
    [dbReg, libReg, dbPro] = leerLibReg()
    rangoE = voltaje[0]
    rangoM = voltaje[1]
    nSub = voltaje[2]
    nSob = voltaje[3]
    tSub = voltaje[4]
    tSob = voltaje[5]
    if rangoE:
        Atac = 'Si'
    elif ((nSob + nSub) < 7) and ((tSub + tSob) < 0.17):
        Atac = "Si"
    else:
        [roi,rec] = reemplazo("EL",standby,wC,dbReg)
        if roi:
            Atac = "Si"
        else:
            Atac = 'No'

    return Atac

