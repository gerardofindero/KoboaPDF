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


def armarTxt_Atac(Claves,standby,wC):
    dbReg, lib, dbPro = leerLibReg()
    txt = ""
    clavesS = Claves.split(",")
    nombre = clavesS[1]

    if "EL" in Claves:
        txt += lib.loc["REG01", "Texto"]
        [roi,rec] = reemplazo("EL",standby,wC,dbReg)
        if "TO" in Claves:
            txt += lib.loc["REG02F", "Texto"]
        elif roi:
            txt += lib.loc["REG03Fb","Texto"]


    if "MC" in Claves:
        [roi,rec] = reemplazo()
        if roi:
            txt += lib.loc["REG06Fb","Texto"]
        else:
            txt += lib.loc["REG04F","Texto"]

    if roi:
        txt = txt.replace("[linkReco]",fc.ligarTextolink("Regulador recomendado",rec.at[0,"link"]))
    linkSP = dbPro.loc["[linkSP]","link"]
    linkPV = dbPro.loc["[linkPV]","link"]
    txt = txt.replace("[linkSP]",fc.ligarTextolink("Supresor de picos",linkSP))
    txt = txt.replace("[linkSP]",fc.ligarTextolink("Protector de voltaje",linkPV))
    txt = txt.replace("[nombre]",nombre)

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
    wC = wC *1.20
    if "EL" == uso:
        filt = (dbReg.uso == "elec") & ( dbReg.w >= wC ) & ( dbReg.standby<standby )
    elif "MC" == uso:
        filt = (dbReg.uso == "meca") & (dbReg.w >= wC) & (dbReg.standby < standby)
    if filt.sum()>0:
        rec = dbReg.loc[dbReg.index[filt][0],:].reset_index(drop=True).copy()
        roi = True
    else:
        roi = False
        rec = None
    return [roi,rec]

def Atac_Mec(voltaje,standby,wC):
    # stand by del regulador
    # watts de lo que tenia conectado
    [dbReg, libReg, dbPro] = leerLibReg()
    rango = voltaje[0]
    nSub = voltaje[1]
    nSob = voltaje[2]
    tSub = voltaje[3]
    tSob = voltaje[4]
    if rango:
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
    rango = voltaje[0]
    nSub = voltaje[1]
    nSob = voltaje[2]
    tSub = voltaje[3]
    tSob = voltaje[4]
    if rango:
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

