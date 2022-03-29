import pandas as pd
import numpy as np
import funcionesComunes as fc
import libreriaReguladores_ as lr

def leerLibreriasNB():
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
    w  = 'Active Output Power Rating Minimum Configuration (W)'
    va = 'Apparent Output Power Rating Minimum Configuration (VA)'  # VA
    numCR = 'Number of Battery Backup and Surge Protected Outlets'  # numero de conectores con respaldo de bateria
    numSR = 'Number of Surge Protected Only Outlets'  # numero de conectores sin respaldo de bateria
    entrada = 'Rated Input Voltage (V rms)'  # voltaje de entrada del nobreak (escoger los que trabajan a 120 Vrms)
    costo = 'Cost (MXN)'  # costo en pesos mexicanos
    link = 'Buy Link'  # link de compra
    marca = 'Brand Name'
    modelo = 'Model Name'
    dbUPS = dbUPS.loc[:, [sb,w, va, numCR, numSR, entrada, costo, link, marca, modelo]]
    dbUPS.columns = ['sb','w','va', 'numCR', 'numSR', 'entrada', 'costo', 'link', 'marca', 'modelo']
    filtro = pd.notnull(dbUPS.costo) & pd.notnull(dbUPS.link) & pd.notnull(dbUPS.va) & pd.notnull(
        dbUPS.sb)
    dbUPS = dbUPS.loc[filtro, :].reset_index(drop=True).copy()

    lib = lib.set_index("Codigo")
    links = links.set_index("variable")
    return [lib,dbUPS,links]

def crearClavesNB():
    # NR -> necesita respaldo (tiene conectado algo de comunicaciones, equipo de seguridad o computadorea de escritorio)
    Claves = ""
    return Claves

def armarTxt_NAtac():
    lib, dbUPS,links = leerLibreriasNB()
    txt = lib.at["NB06F","Texto"]
    return txt

def armarTxt_Atac(voltaje, Claves, standby, wC):
    lib,dbUPS,links = leerLibreriasNB()
    rango = voltaje[0]
    nSub = voltaje[1]
    nSob = voltaje[2]
    tSub = voltaje[3]
    tSob = voltaje[4]

    if rango:
        Claves += ",EE"
    elif (nSob < 7) and (tSob < 0.17):
        Claves += ",EE"

    txt = ""
    if not "NR" in Claves:
        if "EE" in Claves:
            txt += lib.at["NB04F","Texto"]
        else:
            [dbReg, libReg, dbPro] = lr.leerLibReg()
            roi2, rec2 = lr.reemplazo("elec", standby, wC, dbReg)
            txt += lib.at["NB05F","Texto"]
    elif "NR" in Claves:
        if standby <= 15:
            txt += lib.at["NB06F","Texto"]
        else:
            roi, rec = reemplazo(dbUPS,standby,wC)
            if roi:
                txt += lib.at["NB07F","Texto"]
            else:
                txt += lib.at["NB08F","Texto"]

    txt = txt.replace("[linkSP]",fc.ligarTextolink("Supresor de picos",links.at["[linkSP]","link"]))
    if roi:
        txt = txt.replace("[recoNB]",fc.ligarTextolink("No Break recomendado",dbUPS.at[0,"link"]))
    if (not "NR" in Claves) and (not "EE" in Claves):
        if roi2:
            txt = txt.replace("[recoREG]",fc.ligarTextolink("Regulador recomendado",rec2.at[0,"link"]))
        else:
            txt = txt.replace("un regulador eficiente ([recoReg])","alguno de la marca APC, Cybey Power ó Tripp Lite")
    return txt

def armarTxtE(Claves,standby):
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


