import pandas as pd
import numpy as np
from scipy.stats import norm
import funcionesComunes as fc
from leerVoltaje import leer_volts

def leerLibReg():

    #self.txt=''
    #self.val     = False
    #self.sustitutos = pd.DataFrame(columns=['tipo', 'cantidad', 'costo', 'link','kwhAhorroBimestral','ahorroBimestral', 'roi','accion'])
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
# nSob   numero de muestras se sobre voltaje, num
# tSob   tiempo que estuvo de sobre voltaje, num
# nSub   numero de muestras se sub voltaje, num
# tSub   tiempo que estuvo de sobre voltaje, num
# w      potencia regulador, potencia de fuga, watts
# uso    Tipo de uso, Clave -> UE, UM
# VA     volt/aampere de lo que tiene conectado, num
# WC     watts de lo que esta conectado, num
# dispositivo princial
# vEstElec Voltaje estable para uso electrico, Clave -> VEE
# vEstMec  Voltaje estable para uso mecanico,  Clave -> VEM
# tiempo de uso s epedue sacar con kWh y w
# tol    Toleracia de los equipos conectados
# desconectar DS, DN
# el cliente lo apaga AS, AN

def armarTxt_NAtac(Claves):

    dbReg, lib, dbPro = leerLibReg()
    txt=""
    clavesS = Claves.split(",")
    nombre =  clavesS[1]

    if "EL" in Claves:
        txt += lib.at["REG03F","PropuestaFF"]
    if "MC" in Claves:
        txt += lib.at["REG06F","PropuestaFF"]

    linkSP = dbPro.at["[linkSP]","link"]
    linkPV = dbPro.at["[linkPV]","link"]
    txt = txt.replace("[linkSP]",fc.ligarTextolink("Supresor de picos",linkSP))
    txt = txt.replace("[linkSP]",fc.ligarTextolink("Protector de voltaje",linkPV))
    txt = txt.replace("[nombre]",nombre)
    return txt


def armarTxt_Atac(Claves,standby,voltaje):
    EE = False
    EM = False
    print(voltaje)
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

    if "EL" in Claves:
        [roi, rec] = reemplazo("EL", standby, wC, dbReg)
        if EE:
            txt += lib.loc["REG01F", "Texto"]
        elif "TO" in Claves:
            txt += lib.loc["REG02F", "Texto"]
        else:
            if roi:
                txt += lib.loc["REG03Fb","Texto"]


    if "MC" in Claves:
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
    txt = txt.replace("[linkSP]",fc.ligarTextolink("Supresor de picos",linkSP))
    txt = txt.replace("[linkPV]",fc.ligarTextolink("Protector de voltaje",linkPV))
    txt = txt.replace("[nombre]",nombre)
    txt+= "<br />"
    return txt



def armarTxtE(kwh):
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

    wC = float(wC) *1.20
    if wC==10000*1.20:
        roi=False
        rec=None
    elif "EL" == uso:
        filt = (dbReg.uso == "elec") & ( dbReg.w<=wC ) & ( dbReg.standby<standby )
        if filt.sum() > 0:
            rec = dbReg.loc[dbReg.index[filt][0], :].reset_index(drop=True).copy()
            roi = True
        else:
            roi = False
            rec = None

    elif "MC" == uso:
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

