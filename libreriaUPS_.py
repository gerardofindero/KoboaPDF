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
        txt = txt.replace("[recoREG]",fc.ligarTextolink("Regulador recomendado",rec2.at[0,"link"]))
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
        if standby <= 15:
            Atac = "No"
        elif standby > 15:
            [roi,rec] = reemplazo(dbUPS,standby,wC)
            if roi:
                Atac = "Si"
            else:
                Atac = "No"

    return Atac




def sepNobAta(dfDes,DAC):
    # A atacable D Nombre N texto Q claves
    print(dfDes)
    indexNB = dfDes.index[dfDes.D.str.contains('NoBreak',case=False)]
    Claves = dfDes.loc[indexNB,'Q'].str.split(',',expand=True)
    dfDes.loc[indexNB,'VA'] = Claves[1].astype(int)
    dfDes.loc[indexNB, 'wC'] = Claves[2].astype(int)

    dfDes[['nombre','dispPrincipal','trash']] = dfDes.loc[indexNB,'D'].str.split(' ',n=2,expand=True)
    dfDes.loc[indexNB,'nombre'] = dfDes.loc[indexNB,'nombre']+' '+ dfDes.loc[indexNB,'dispPrincipal']

    for i in indexNB:
        libUPSObj = libreriaUPS()
        libUPSObj.setData(nomNB        = dfDes.at[i,'nombre'],
                          VA            = dfDes.at[i,'VA'],
                          wC            = dfDes.at[i,'wC'],
                          w             = dfDes.at[i, 'J'],
                          dispPrincipal = dfDes.at[i,'dispPrincipal'],
                          DAC=DAC)
        libUPSObj.armarTxt()
        dfDes.loc[i, 'N'] = libUPSObj.txt
        dfDes.loc[i, 'A'] = libUPSObj.atacable


    return dfDes.loc[:,'A':'Q'].copy()

class libreriaUPS:
    def __init__(self):
        self.txt = ''
        self.val = False
        self.sustitutos = pd.DataFrame(columns=['tipo', 'cantidad', 'costo', 'link', 'kwhAhorroBimestral', 'ahorroBimestral', 'roi', 'accion'])
        try:
            self.lib = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/libreriaUPS.xlsx",
                sheet_name="Libreria UPS")
            self.dbUPS = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/dbUPSreducida.xlsx",
                sheet_name="data")
        except:
            self.lib = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/libreriaUPS.xlsx",
                sheet_name="Libreria UPS")
            self.dbUPS = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/dbUPSreducida.xlsx",
                sheet_name="data")
        sb = 'Total Input Power in W at 0% Load Min Config Lowest Dependency (ac)'  # standby
        va = 'Apparent Output Power Rating Minimum Configuration (VA)'  # VA
        numCR = 'Number of Battery Backup and Surge Protected Outlets'  # numero de conectores con respaldo de bateria
        numSR = 'Number of Surge Protected Only Outlets'  # numero de conectores sin respaldo de bateria
        entrada = 'Rated Input Voltage (V rms)'  # voltaje de entrada del nobreak (escoger los que trabajan a 120 Vrms)
        costo = 'Cost (MXN)'  # costo en pesos mexicanos
        link = 'Buy Link'  # link de compra
        marca = 'Brand Name'
        modelo = 'Model Name'
        self.dbUPS = self.dbUPS.loc[:, [sb, va, numCR, numSR, entrada, costo, link, marca, modelo]]
        self.dbUPS.columns =['sb', 'va', 'numCR', 'numSR', 'entrada', 'costo', 'link', 'marca', 'modelo']
        filtro = pd.notnull(self.dbUPS.costo) & pd.notnull(self.dbUPS.link) & pd.notnull(self.dbUPS.va) & pd.notnull(self.dbUPS.sb)
        self.dbUPS = self.dbUPS.loc[filtro,:].reset_index(drop=True).copy()


    def validacionVariables(self, nomNB, VA, wC, w, dispPrincipal, DAC):
        val_wC            = False
        val_w             = False
        val_DAC           = False
        val_dispPrincipal = False
        val_VA            = False
        val_nomReg        = False

        if wC is None:
            print('Watts de los conectado al regulador es None')
        elif not isinstance(wC, (int, float)):
            print('Watts de los conectado al regulador no es numerico')
        elif wC == 0:
            print('Watts de los conectado al regulador es 0')
        else:
            val_wC = True

        if nomNB == '':
            print('Nombre de regulador vacio')
        elif nomNB is None:
            print('Nombre de regulador nulo')
        elif not isinstance(nomNB, str):
            print('Nombre de regulador no es de una cadea')
        else:
            val_nomReg = True

        if VA == 0:
            print('VA valor de 0')
        elif VA is None:
            print('VA es nula')
        elif not isinstance(VA, (int, float)):
            print('VA no es nuemrica')
        else:
            val_VA = True

        if w == 0:
            print('w de standby valor de 0')
        elif w is None:
            print('w de standby es nula')
        elif not isinstance(w, (int, float)):
            print('w de standby no es nuemrica')
        else:
            val_w = True
        print(dispPrincipal)
        if dispPrincipal=='':
            print('dispositivo principal vacio')
        elif not isinstance(dispPrincipal,str):
            print('dispositivo principal no es una cadena')
        elif dispPrincipal not in ['Refrigerador','TV','Congelador','Lavadora','PC','TV','NoBreak']:
            print('dispositivo principal no esta en la lista reconocida')
        else:
            val_dispPrincipal=True

        if DAC is None:
            print('DAC es nulo')
        elif not isinstance(DAC, (int, float)):
            print('DAC es no es numerico')
        elif DAC==0:
            print('DAC es 0')
        else:
            val_DAC=True
        if val_wC and val_w and val_DAC and val_dispPrincipal and val_VA and val_nomReg:
            print('Variables aceptadas, procediendo con asignacion del setData')
            return True
        else:
            print('VARIABLES NO ACEPTADAS, setData fallido')
            return False

    def setData(self, nomNB, VA, wC, w, dispPrincipal, DAC):
        self.txt = ''
        print('Libreria UPS setData\nRevizando variables:')
        if self.validacionVariables(nomNB, VA, wC, w, dispPrincipal, DAC):
            self.nomNB = nomNB
            self.DAC   = DAC
            self.w     = w
            self.dispPrincipal = dispPrincipal
            self.atacable = 'Si'
            VAc = (wC / 0.8) * 1.20
            if VA > VAc:
                self.VA = VA
            else:
                self.VA = VAc
            self.val=True
        else:
            self.val=False

    def recRem(self):
        filtro = (self.VA < self.dbUPS.va) & (self.dbUPS.sb < self.w)
        reco =self.dbUPS.loc[filtro,:].copy()
        reco.loc[:,'kwhAhorroBimestral'] = (self.w-reco.sb)*24*60/1000
        reco.loc[:,'ahorroBimestral'   ] = reco.kwhAhorroBimestral*self.DAC
        reco.loc[:,'roi'               ] = reco.costo/reco.ahorroBimestral/6
        [self.roiM3, reco]=fc.checarROI(reco)

        if len(reco)!=0:
            df= pd.DataFrame({
                'tipo': (['Regulador'] * len(reco)),
                'cantidad': [1]*len(reco),
                'costo': reco.costo,
                'link': reco.link,
                'kwhAhorroBimestral': reco.kwhAhorroBimestral,
                'ahorroBimestral': reco.ahorroBimestral,
                'roi': reco.roi,
                'accion':(['compra']*len(reco))})
            self.sustitutos = self.sustitutos.append(df,ignore_index=True)

    def armarTxt(self):
        txt = ''
        print('\nIniciando armarTxt')
        dispQueRequierenNoBreak = []
        #indispensable = self.dispPrincipal in dispQueRequierenNoBreak
        indispensable = False
        if not indispensable:
            if self.w > 3:
                self.recRem()
                if len(self.sustitutos)<1:
                    txt = txt + '[NO SE ENCONTRO UN REEMPLAZO DE NOBREAK VIABLE]'
                elif self.roiM3:
                    reemplazo = fc.ligarTextolink('Nobreak', self.sustitutos.at[0, 'link']) + \
                                ' con ahorro anual de $' + str(round(self.sustitutos.at[0, 'ahorroBimestral'] * 6, 2))
                    txt = txt + fc.selecTxt(self.lib,'UPS01').replace('[recomendacion]',reemplazo)
                    df = pd.DataFrame({
                        'kwhAhorroBimestral': self.w * 24 * 60 / 1000,
                        'ahorroBimestral': self.w * 24 * 60 * self.DAC / 1000,
                        'accion': ['retirar']})
                    self.sustitutos = self.sustitutos.append(df, ignore_index=True)
                elif not self.roiM3:
                    reemplazo = fc.ligarTextolink('Nobreak', self.sustitutos.at[0, 'link']) + \
                                ' con ahorro anual de $' + str(round(self.sustitutos.at[0, 'ahorroBimestral'] * 6, 2))
                    txt = txt + fc.selecTxt(self.lib,'UPS02').replace('[recomendacion]',reemplazo)
                    df = pd.DataFrame({
                        'kwhAhorroBimestral': self.w * 24 * 60 / 1000,
                        'ahorroBimestral': self.w * 24 * 60 * self.DAC / 1000,
                        'accion': ['retirar']})
                    self.sustitutos = self.sustitutos.append(df, ignore_index=True)
            else:
                txt = txt + fc.selecTxt(self.lib,'UPS03')
                df = pd.DataFrame({
                    'kwhAhorroBimestral': self.w * 24 * 60 / 1000,
                    'ahorroBimestral': self.w * 24 * 60 * self.DAC / 1000,
                    'accion': ['retirar']})
                self.sustitutos = self.sustitutos.append(df, ignore_index=True)
        else:
            if self.w > 3:
                self.recRem()
                if len(self.sustitutos)<1:
                    txt = txt + '[NO SE ENCONTRO UN REEMPLAZO DE NOBREAK VIABLE]'
                elif self.roiM3:
                    reemplazo = fc.ligarTextolink('Nobreak', self.sustitutos.at[0, 'link']) + \
                                ' con ahorro anual de $' + str(round(self.sustitutos.at[0, 'ahorroBimestral'] * 6, 2))
                    txt = txt + fc.selecTxt(self.lib, 'UPS04').replace('[recomendacion]',reemplazo)
                    df = pd.DataFrame({
                        'kwhAhorroBimestral': self.w * 24 * 60 / 1000,
                        'ahorroBimestral': self.w * 24 * 60 * self.DAC / 1000,
                        'accion': ['retirar']})
                    self.sustitutos = self.sustitutos.append(df, ignore_index=True)
                elif not self.roiM3:
                    reemplazo = fc.ligarTextolink('Nobreak', self.sustitutos.at[0, 'link']) + \
                                ' con ahorro anual de $' + str(round(self.sustitutos.at[0, 'ahorroBimestral'] * 6, 2))
                    txt = txt + fc.selecTxt(self.lib, 'UPS05').replace('[recomendacion]',reemplazo)
                    df = pd.DataFrame({
                        'kwhAhorroBimestral': self.w * 24 * 60 / 1000,
                        'ahorroBimestral': self.w * 24 * 60 * self.DAC / 1000,
                        'accion': ['retirar']})
                    self.sustitutos = self.sustitutos.append(df, ignore_index=True)
            else:
                txt = txt + fc.selecTxt(self.lib, 'UPS06')
                self.atacable = 'No'
        self.txt = txt.replace('[nomNB]', self.nomNB).replace('\n','<br />')
        ### potencial de ahorro
        if not indispensable:
            self.txt = self.txt+",1,"+str(self.w)+","+fc.selecTxt(self.lib,"UPSpa01")
        if indispensable:
            if self.w<3:
                self.txt = self.txt+",0,0,"+fc.selecTxt(self.lib,"UPSpa03")
            else:
                porAhorro= self.sustitutos.at[0,"ahorroBimestral"]/self.w
                nbsus=fc.ligarTextolink("No break",self.sustitutos.at[0,"link"])
                self.txt = self.txt + ","+str(porAhorro)+","+str(self.sustitutos.at[0,"ahorroBimestral"]) +","+ fc.selecTxt(self.lib, "UPSpa03").replace("[recomendacion]",nbsus)









