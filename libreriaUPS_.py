import pandas as pd
import numpy as np
import funcionesComunes as fc
import libreriaReguladores_ as lr

def leerLibreriasNB():
    """
    :return: lib   -> Libreria con textos, pestaña "Libreria UPS_"
             links -> Links de protectores de voltaje
             dbUPS -> Base de datos con nobreaks para reemplazo
    """
    try:
        lib = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/libreriaUPS.xlsx",
            sheet_name="Libreria UPS_")
        links = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/libreriaUPS.xlsx",
            sheet_name="links")
        dbUPS = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/dbUPSreducida.xlsx",
            sheet_name="data")
    except:
        lib = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/libreriaUPS.xlsx",
            sheet_name="Libreria UPS_")
        links = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/libreriaUPS.xlsx",
            sheet_name="links")
        dbUPS = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/dbUPSreducida.xlsx",
            sheet_name="data")
    sb = 'Total Input Power in W at 0% Load Min Config Lowest Dependency (ac)'  # standby
    w  = 'Active Output Power Rating Minimum Configuration (W)'                 # potencia que puede proporcionar
    va = 'Apparent Output Power Rating Minimum Configuration (VA)'              # Volts-Amperes que puede proporcionar
    numCR = 'Number of Battery Backup and Surge Protected Outlets'              # numero de conectores con respaldo de bateria
    numSR = 'Number of Surge Protected Only Outlets'                            # numero de conectores sin respaldo de bateria
    entrada = 'Rated Input Voltage (V rms)'                                     # voltaje de entrada del nobreak (escoger los que trabajan a 120 Vrms)
    costo = 'Cost (MXN)'                                                        # costo en pesos mexicanos
    link = 'Buy Link'                                                           # link de compra
    marca = 'Brand Name'
    modelo = 'Model Name'
    dbUPS = dbUPS.loc[:, [sb,w, va, numCR, numSR, entrada, costo, link, marca, modelo]]
    # Simplicación de los nombres de las columns de dbUPS
    dbUPS.columns = ['sb','w','va', 'numCR', 'numSR', 'entrada', 'costo', 'link', 'marca', 'modelo']
    # Eliminar renglones con datos faltantes
    filtro = pd.notnull(dbUPS.costo) & pd.notnull(dbUPS.link) & pd.notnull(dbUPS.va) & pd.notnull(
        dbUPS.sb)
    dbUPS = dbUPS.loc[filtro, :].reset_index(drop=True).copy()

    lib = lib.set_index("Codigo")
    links = links.set_index("variable")
    return [lib,dbUPS,links]

def crearClavesNB():
    # Las Claves se crean directo en el programa que lee la información de kobo correspondiente
    Claves = ""
    return Claves

def armarTxt_NAtac():
    # Texto para los nobreak no atacables
    lib, dbUPS,links = leerLibreriasNB()
    txt = lib.at["NB06F","Texto"]
    return txt

def armarTxt_Atac(voltaje, Claves, standby, wC):
    """
    Crea texto para nobreaks en la sección de fugas
    :param voltaje: Variables sobre el voltaje de la casa
    :param Claves:  EE: Volatje estable para apartos electronicos
                    NR: Los equipos conectados al no break requeiren respaldo de enrgía
    :param standby: estandby del nobreak (numca se desconecta)
    :param wC:      Watts de todas las cosas conectadas al nobreak (Se utiliza para estimar la capacidad del reemplazo)
    :return:
    """
    # Recomendaciónes para reguladores atacables

    lib,dbUPS,links = leerLibreriasNB()
    rango = voltaje[0]  # EL voltaje se encuentra en rango
    nSub = voltaje[1]   # Número de veces que el voltaje fue menor al umbral inferior de voltaje
    nSob = voltaje[2]   # Número de veces que el voltaje fue mayor al umbral superior e voltaje
    tSub = voltaje[3]   # Tiempo que el voltaje fue menor al limite inferior de voltaje
    tSob = voltaje[4]   # Tiempo que el voltaje fue mayor al limite superior de voltaje

    if rango:
        Claves += ",EE"
    elif (nSob < 7) and (tSob < 0.17):
        Claves += ",EE"

    txt = ""
    if not "NR" in Claves:
        if "EE" in Claves:
            txt += lib.at["NB04F","Texto"]
        else:
            # si el voltaje no es estable pero los aparatos no requieren respaldo de energía se sugire un regulador
            [dbReg, libReg, dbPro] = lr.leerLibReg()
            # ROI2 corresponde a la recomendación de un regulador
            roi2, rec2 = lr.reemplazo("elec", standby, wC, dbReg)
            txt += lib.at["NB05F","Texto"]
    elif "NR" in Claves:
        if standby <= 15:
            txt += lib.at["NB06F","Texto"]
        else:
            roi, rec = reemplazo(dbUPS,standby,wC)
            # roi corresponde a un reemplazo de nobreak ya que los equipos conectados al nobreak si requieren respaldo de energía
            if roi:
                txt += lib.at["NB07F","Texto"]
            else:
                txt += lib.at["NB08F","Texto"]

    txt = txt.replace("[linkSP]",fc.ligarTextolink("Supresor de picos",links.at["[linkSP]","link"]))
    # Estos if solo son para sustituir el reemplazo sugerido
    if roi:
        txt = txt.replace("[recoNB]",fc.ligarTextolink("No Break recomendado",dbUPS.at[0,"link"]))
    if (not "NR" in Claves) and (not "EE" in Claves):
        if roi2:
            txt = txt.replace("[recoREG]",fc.ligarTextolink("Regulador recomendado",rec2.at[0,"link"]))
        else:
            txt = txt.replace("un regulador eficiente ([recoReg])","alguno de la marca APC, Cybey Power ó Tripp Lite")
    return txt

def armarTxtE(Claves,standby):
    """
    :param Claves:  EE: Volatje estable para apartos electronicos
                    NR: Los equipos conectados al no break requeiren respaldo de enrgía
    :param standby: standby del nobreak (sección de equipos)
    :return:
    """
    # armar texto para librerias de nobreaks en sección de equipos
    lib, dbUPS,links = leerLibreriasNB()
    txt = ""
    if not "NR" in Claves:
        txt += lib.at["NB01E","Texto"]
    elif "NR" in Claves:
        if standby <= 15:
            txt += lib.at["NB02E","Texto"]
        else:
            standby += lib.at["NB03E","Texto"]
    return txt

def reemplazo(dbUPS,standby,wC):
    """
    Selección de nobreak mas eficiente
    :param dbUPS: Base de datos de UPS Librerias\No Breaks UPS\dbUPSreducida.xlsx
    :param standby: estandby de nobreak del cliente
    :param wC:     Suma de los watts que consumen los equipos conectados al nobreak del cliente
    :return: roi -> True si hay almenos una opción de nobreak mas eficiente
             rec -> data frame con información de nobreaks mas eficientes, si hay mas de uno el priemero en la lista es el de menor standby
    """
    wC = wC * 1.20
    standby = standby < 0.80
    filt = (dbUPS.sb < standby) & (dbUPS.w>wC)
    if filt.sum()>0:
        roi = True
        rec = dbUPS.at[dbUPS.loc[filt,:].sort_values("w",ascending=True).idex[0],:].reset_index(drop=True).copy()
    else:
        roi = False
        rec = None
    return [roi,rec]

def Atac_NB(Claves,standby,wC):
    """
    Función para determinar si un nobreak es atacble o no y separarlo en la lista del desciframiento
    :param Claves:   EE: Volatje estable para apartos electronicos
                    NR: Los equipos conectados al no break requeiren respaldo de enrgía
    :param standby: estandby del nobreak
    :param wC:      suma de la potencia de los equipos conectados al nobreak
    :return:
    """
    [lib, dbUPS, links] = leerLibreriasNB()
    if not "NR" in Claves:
        Atac = "Si"
    elif ("NR" in Claves):

        if standby=='Nm':
            Atac = "No"
        elif standby <= 15:
            Atac = "No"
        elif standby > 15:
            [roi,rec] = reemplazo(dbUPS,standby,wC)
            if roi:
                Atac = "Si"
            else:
                Atac = "No"

    return Atac


