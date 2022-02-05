import pandas as pd
import numpy as np
from scipy.stats import norm
import funcionesComunes as fc
from leerVoltaje import leer_volts

def sepRegAta(dfDes,DAC,vEstEle,vEstMec,nSob,nSub,tSob,tSub):
    # A atacable D Nombre N texto Q claves

    indexReg = dfDes.index[dfDes.D.str.contains('regulador|Regulador',case=False)]
    nReg     = len(indexReg)
    dfDes.loc[indexReg, 'N']=''
    if nReg>0:
        libRegObj=libreriaReguladores()
        if vEstEle and vEstMec:
            if   nReg == 1:
                Texto  = libRegObj.libReg.at[1,'Texto']
            elif nReg > 1:
                Texto = libRegObj.libReg.at[1, 'Texto']
            dfDes.loc[indexReg,'A'] = 'Si'
            """
            for i in indexReg:
                dfDes.loc[i,'N'] = dfDes.loc[i,'N']+",1,"+str(dfDes.at[i,"K"])+","+fc.selecTxt(libRegObj.libReg,"REGpa01")
            """
            linkA='https://www.amazon.com.mx/Volteck-AD-270-Adaptador-Supresor-Picos/dp/B0124HMZR2/' \
                  'ref=sr_1_2?__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=R30CP3WL83BB&keywords=supresor+de+picos&qid=1644019250&s=electronics&sprefix=supresor+de+picos%2Celectronics%2C169&sr=1-2'
            Address = 'Link de compra'
            LinkS = '<link href="' + str(linkA) + '"color="blue">' + Address + ' </link>'

            Texto = Texto.replace('[LinkPdP]', LinkS)

            dfDes.loc[indexReg, 'N'] = Texto

            return dfDes

        else:
            Claves = dfDes.loc[indexReg,'Q'].str.split(',',expand=True)
            dfDes.loc[indexReg, 'VA']  = Claves[1].astype(int)
            dfDes.loc[indexReg, 'wC']  = Claves[2].astype(int)
            dfDes.loc[indexReg, 'uso'] = Claves[3]
            dfDes.loc[indexReg, 'tol'] = Claves[4]
            dfDes.loc[indexReg, 'tol'] = dfDes.loc[indexReg, 'tol'] == 'T'

            if (dfDes.uso=='elec').all():
                if vEstEle:
                    if nReg == 1:
                        dfDes.loc[indexReg, 'N'] = libRegObj.libReg.at[1, 'Texto'].replace('{s}', '').replace('{es}','')
                    elif nReg > 1:
                        dfDes.loc[indexReg, 'N'] = libRegObj.libReg.at[1, 'Texto'].replace('{', '').replace('}', '')
                    dfDes.loc[indexReg, 'A'] = 'Si'
                    """
                    for i in indexReg:
                        dfDes.loc[i, 'N'] = dfDes.loc[i, 'N'] + ",1," + str(dfDes.at[i, "K"]) + "," + fc.selecTxt(libRegObj.libReg, "REGpa01")
                    """
                    return dfDes.loc[:,'A':'Q'].copy()


            elif (dfDes.uso=='meca').all():
                if vEstMec:
                    if nReg == 1:
                        dfDes.loc[indexReg, 'N'] = libRegObj.libReg.at[1, 'Texto'].replace('{s}', '').replace('{es}','')
                    elif nReg > 1:
                        dfDes.loc[indexReg, 'N'] = libRegObj.libReg.at[1, 'Texto'].replace('{', '').replace('}', '')
                    dfDes.loc[indexReg, 'A'] = 'Si'
                    """
                    for i in indexReg:
                        dfDes.loc[i, 'N'] = dfDes.loc[i, 'N'] + ",1," + str(dfDes.at[i, "K"]) + "," + fc.selecTxt(libRegObj.libReg, "REGpa01")
                    """
                    return dfDes.loc[:,'A':'Q'].copy()
            else:
                indexElec  = dfDes.loc[indexReg,:].index[dfDes.loc[indexReg,'uso']=='elec']
                nElec = len(indexElec)

                indexMeca  = dfDes.loc[indexReg,:].index[dfDes.loc[indexReg,'uso']=='meca']
                nMeca = len(indexMeca)

                #dfDes[['fuga','nombre','dispPrincipal','trash']] = dfDes.loc[indexReg,'D'].str.split(' ',n=3,expand=True)
                dfDes[['nombre','dispPrincipal','trash']] = dfDes.loc[indexReg,'D'].str.split(' ',n=2,expand=True)
                dfDes.loc[indexReg,'nombre'] = dfDes.loc[indexReg,'nombre']+' '+ dfDes.loc[indexReg,'dispPrincipal']

                if vEstEle:
                    nomsRegs = fc.listarComas(dfDes.loc[indexElec,'nombre'].tolist())
                    if nElec == 1:
                        dfDes.loc[indexElec, 'N'] = libRegObj.libReg.at[1, 'Texto'].replace('{s} regulador{es}', nomsRegs)
                    elif nElec > 1:
                        dfDes.loc[indexElec, 'N'] = libRegObj.libReg.at[1, 'Texto'].replace('{s} regulador{es}', nomsRegs)
                    dfDes.loc[indexElec, 'A'] = 'Si'
                    """
                    for i in indexElec:
                        dfDes.loc[i, 'N'] = dfDes.loc[i, 'N'] + ",1," + str(dfDes.at[i, "K"]) + "," + fc.selecTxt(libRegObj.libReg, "REGpa01")
                    """
                else:
                    for i in  indexElec:
                        nombre = dfDes.at[i,'nombre']
                        dispPrincipal = dfDes.at[i,'dispPrincipal']
                        w   = dfDes.at[i, 'J']
                        VA  = dfDes.at[i,'VA']
                        uso = dfDes.at[i,'uso']
                        tol = dfDes.at[i,'tol']
                        wC  =  dfDes.at[i,'wC']
                        libRegObj.setData(
                            nomReg=nombre, VA=VA, wC=wC , w=w, uso=uso,
                            dispPrincipal=dispPrincipal,
                            tol=tol, vEstEle=vEstEle, vEstMec=vEstMec,
                            DAC=DAC,nSob=nSob,nSub=nSub,tSob=tSob,tSub=tSub)
                        libRegObj.armarTxt()
                        dfDes.loc[i, 'N'] = libRegObj.txt

                        # dfDes.loc[i, 'N'] = libRegObj.txt
                        # if not libRegObj.sustitutos.empty:
                        #     porAhorro = libRegObj.sustitutos.at[0, 'kwhAhorroBimestral'] / wC
                        #     if libRegObj.sustitutos.accion == "retirar":
                        #         dfDes.loc[i, 'N'] = libRegObj.txt + "," + str(porAhorro) + "," + str(libRegObj.sustitutos.at[0, 'kwhAhorroBimestral']) + "," + fc.selecTxt(libRegObj.libReg,"REGpa01")
                        #     elif libRegObj.sustitutos.accion == "compra":
                        #         if libRegObj.sustitutos.tipo == "Protector":
                        #             potAtxt = fc.selecTxt(libRegObj.libReg, "REGpa02").replace("[recomendacion]", fc.ligarTextolink("Protector de voltaje",libRegObj.sustitutos.at[0, "link"]))
                        #             dfDes.loc[i, 'N'] = libRegObj.txt + "," + str(porAhorro) + "," + str(libRegObj.sustitutos.at[0, 'kwhAhorroBimestral']) + "," + potAtxt
                        #         elif libRegObj.sustitutos.tipo == "Regulador":
                        #             potAtxt = fc.selecTxt(libRegObj.libReg, "REGpa03").replace("[recomendacion]",fc.ligarTextolink("Regulador", libRegObj.sustitutos.at[ 0, "link"]))
                        #             dfDes.loc[i, 'N'] = libRegObj.txt + "," + str(porAhorro) + "," + str(libRegObj.sustitutos.at[0, 'kwhAhorroBimestral']) + "," + potAtxt

                        dfDes.loc[i,'A'] = 'Si'


                if vEstMec:
                    nomsRegs = fc.listarComas(dfDes.loc[indexMeca, 'nombre'].tolist())
                    if nMeca == 1:
                        dfDes.loc[indexMeca, 'N'] = libRegObj.libReg.at[1, 'Texto'].replace('{s} regulador{es}', nomsRegs)
                    elif nMeca > 1:
                        dfDes.loc[indexMeca, 'N'] = libRegObj.libReg.at[1, 'Texto'].replace('{s} regulador{es}', nomsRegs)
                    dfDes.loc[indexElec, 'A'] = 'Si'
                    """
                    for i in indexMeca:
                        dfDes.loc[i, 'N'] = dfDes.loc[i, 'N'] + ",1," + str(dfDes.at[i, "K"]) + "," + fc.selecTxt(libRegObj.libReg, "REGpa01")
                    """
                else:
                    for i in indexMeca:
                        nombre = dfDes.at[i, 'nombre']
                        dispPrincipal = dfDes.at[i, 'dispPrincipal']
                        w = dfDes.at[i, 'J']
                        VA = dfDes.at[i, 'VA']
                        uso = dfDes.at[i, 'uso']
                        tol = dfDes.at[i, 'tol']
                        wC = dfDes.at[i, 'wC']
                        libRegObj.setData(
                        nomReg=nombre, VA=VA,wC=wC, w=w, uso=uso,
                        dispPrincipal=dispPrincipal,
                        tol=tol, vEstEle=vEstEle, vEstMec=vEstMec,
                        DAC=DAC,nSob=nSob,nSub=nSub,tSob=tSob,tSub=tSub)
                        libRegObj.armarTxt()
                        dfDes.loc[i, 'N'] = libRegObj.txt
                        # porAhorro = libRegObj.sustitutos.at[0, 'kwhAhorroBimestral'] / wC
                        # if libRegObj.sustitutos.accion == "retirar":
                        #     dfDes.loc[i, 'N'] = libRegObj.txt+","+str(porAhorro)+","+str(libRegObj.sustitutos.at[0,'kwhAhorroBimestral'])+","+fc.selecTxt(libRegObj.libReg, "REGpa01")
                        # elif libRegObj.sustitutos.accion == "compra":
                        #     if libRegObj.sustitutos.tipo == "Protector":
                        #         potAtxt = fc.selecTxt(libRegObj.libReg, "REGpa02").replace("[recomendacion]",fc.ligarTextolink("Protector de voltaje",libRegObj.sustitutos.at[0,"link"]))
                        #         dfDes.loc[i, 'N'] = libRegObj.txt + "," + str(porAhorro) + "," + str(libRegObj.sustitutos.at[0, 'kwhAhorroBimestral']) + "," + potAtxt
                        #     elif libRegObj.sustitutos.tipo == "Regulador":
                        #         potAtxt = fc.selecTxt(libRegObj.libReg, "REGpa03").replace("[recomendacion]",fc.ligarTextolink("Regulador",libRegObj.sustitutos.at[0, "link"]))
                        #         dfDes.loc[i, 'N'] = libRegObj.txt + "," + str(porAhorro) + "," + str(libRegObj.sustitutos.at[0, 'kwhAhorroBimestral']) + "," + potAtxt
                        dfDes.loc[i, 'A'] = 'Si'

                return dfDes.loc[:, 'A':'Q'].copy()


    else:

        return dfDes

class libreriaReguladores:
    def __init__(self):
        self.txt=''
        self.val     = False
        self.sustitutos = pd.DataFrame(columns=['tipo', 'cantidad', 'costo', 'link','kwhAhorroBimestral','ahorroBimestral', 'roi','accion'])
        try:
            self.libReg = pd.read_excel(
                f"../../../Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Reguladores/libreria_reguladores.xlsx",
                sheet_name='libreriaReguladore')
            self.dbReg = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Reguladores/libreria_reguladores.xlsx",
                sheet_name='data')
            self.dbPro = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Reguladores/libreria_reguladores.xlsx",
                sheet_name='protectorVoltaje')
        except:
            self.dbReg = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Reguladores/libreria_reguladores.xlsx",
                sheet_name='data')
            self.libReg = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Reguladores/libreria_reguladores.xlsx",
                sheet_name='libreriaReguladores')
            self.dbPro = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Reguladores/libreria_reguladores.xlsx",
                sheet_name='protectorVoltaje')

    def setData(self,nomReg = None,VA = None,wC = None,w = None,
                uso=None,dispPrincipal=None,tol=None,vEstEle=None,
                vEstMec=None,DAC=None,nSob=None,nSub=None,tSob=None,tSub=None):
        print('Libreria de raguladores setData\nRevizando variables:')
        if self.validacionVariables(nomReg,VA,wC,w,uso,dispPrincipal,tol,vEstEle,vEstMec,DAC,nSob,nSub,tSob,tSub):
            self.sustitutos = pd.DataFrame(columns=['tipo', 'cantidad', 'costo', 'link', 'kwhAhorroBimestral', 'ahorroBimestral', 'roi','accion' ])
            self.DAC    = DAC
            self.nomReg = nomReg # nombre del regulador
            self.w      = w      # potencia de estand by del regulador
            self.uso    = uso    # uso del regulador
            self.tol    = tol
            if uso == 'elec':
                VAc = (wC/0.8) * 1.20
                if VA > VAc:
                    self.VA = VA
                else:
                    self.VA = VAc
            elif uso == 'meca':
                VAc = (wC/0.6) * 1.20
                if VA > VAc:
                    self.VA = VA
                else:
                    self.VA = VAc

            self.atacable = 'Si'
            self.nSub   = nSub
            self.nSob   = nSob
            self.tSub   = tSub
            self.tSob   = tSob
            self.requiereRegulador = True
            if uso == 'elec':
                self.vEst = vEstEle
                self.ref  = 3
            elif uso == 'meca':
                self.vEst = vEstMec
                self.ref  = 12
            self.val=True
        else:
            self.val=False

    def validacionVariables(self,nomReg,VA,wC,w,uso,dispPrincipal,tol,vEstEle,vEstMec,DAC,nSob,nSub,tSob,tSub):
        val_nomReg        = False
        val_VA            = False
        val_w             = False
        val_uso           = False
        val_vEstElec      = False
        val_vEstMec       = False
        val_tol           = False
        val_dispPrincipal = False
        val_DAC           = False
        val_nSub          = False
        val_nSob          = False
        val_tSub          = False
        val_tSob          = False
        val_wC            = False
        if wC is None:
            print('Watts de los conectado al regulador es None')
        elif not isinstance(wC,(int,float)):
            print('Watts de los conectado al regulador no es numerico')
        elif wC == 0:
            print('Watts de los conectado al regulador es 0')
        else:
            val_wC = True

        if nomReg=='':
            print('Nombre de regulador vacio')
        elif nomReg is None:
            print('Nombre de regulador nulo')
        elif not isinstance(nomReg,str):
            print('Nombre de regulador no es de una cadea')
        else:
            val_nomReg=True

        if VA==0:
            print('VA valor de 0')
        elif VA is None:
            print('VA es nula')
        elif not isinstance(VA,(int,float)):
            print('VA no es nuemrica')
        else:
            val_VA=True

        if w==0:
            print('w de standby valor de 0')
        elif w is None:
            print('w de standby es nula')
        elif not isinstance(w,(int,float)):
            print('w de standby no es nuemrica')
        else:
            val_w=True

        if uso == '':
            print('uso es una cadena vacia')
        elif uso is None:
            print('uso es nula')
        elif not isinstance(uso, str):
            print('uso no es una cadena')
        elif uso not in  ['elec','meca']:
            print('uso no tiene una funciona reconocida: opciones elec->Electronico o meca->Mecanico')
        else:
            val_uso = True

        if vEstEle is None:
            print('vEstEle es nula')
        elif not isinstance(vEstEle,bool):
            print('vEstEle no es logica')
        else:
            val_vEstElec=True

        if vEstMec is None:
            print('vEstMec es nula')
        elif not isinstance(vEstMec, bool):
            print('vEstMec no es logica')
        else:
            val_vEstMec = True
        if tol is None:
            print('toleracia de dispositivos conectados es nula')
        elif not isinstance(tol, bool):
            print('toleracia de dispositivos conectados no es logica')
        else:
            val_tol = True
        if dispPrincipal=='':
            print('dispositivo principal vacio')
        elif not isinstance(dispPrincipal,str):
            print('dispositivo principal no es una cadena')
        # elif dispPrincipal not in ['Refrigerador','TV','Congelador','Lavadora','Vala']:
        #     print('dispositivo principal no esta en la lista reconocida')
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

        if nSob is None:
            print('nSob es nulo')
        elif not isinstance(nSob,(int,float)):
            print('nSob no es numerico')
        else:
            val_nSob = True
        if nSub is None:
            print('nSub es nulo')
        elif not isinstance(nSub,(int,float)):
            print('nSub no es numerico')
        else:
            val_nSub = True

        if tSob is None:
            print('tSob es nulo')
        elif not isinstance(tSob,(int,float)):
            print('tSob no es numerico')
        else:
            val_tSob = True

        if tSub is None:
            print('tSub es nulo')
        elif not isinstance(tSub,(int,float)):
            print('tSub no es numerico')
        else:
            val_tSub = True

        if val_nomReg and val_VA and val_w and val_uso and val_vEstElec and\
                val_vEstMec and val_tol and val_dispPrincipal and val_DAC and\
                val_nSub and val_nSob and val_tSub and val_tSob and val_wC:
            print('Variables aceptadas, procediendo con asignacion del setData')
            return True
        else:
            print('VARIABLES NO ACEPTADAS, setData fallido')
            return False
    def recRem(self):
        reco = self.dbReg.loc[self.dbReg.uso==self.uso,:].reset_index(drop=True).copy()
        filtro = reco.va>=self.VA
        filtro = filtro & (reco.standby<self.w)
        reco = reco.loc[filtro,:].copy()
        reco.loc[:,'kwhAhorroBimestral'] = (self.w-reco.loc[:,'standby'])*24*60/1000
        reco.loc[:,   'ahorroBimestral'] = reco.kwhAhorroBimestral*self.DAC
        reco.loc[:,               'roi'] = reco.precio/reco.ahorroBimestral/6
        [self.roiM3, reco]=fc.checarROI(reco)

        if len(reco)!=0:
            df= pd.DataFrame({
                'tipo': (['Regulador'] * len(reco)),
                'cantidad': [1]*len(reco),
                'costo': reco.precio,
                'link': reco.link,
                'kwhAhorroBimestral': reco.kwhAhorroBimestral,
                'ahorroBimestral': reco.ahorroBimestral,
                'roi': reco.roi,
                'accion':(['compra']*len(reco))})
        else:
            df= pd.DataFrame()

        self.sustitutos = self.sustitutos.append(df,ignore_index=True)


    def checkProtector(self):
        if self.uso == 'elec':
            if (self.nSob<7) and (self.tSob<0.17):
                self.requiereRegulador = False
            else:
                self.requiereRegulador = True
        if self.uso == 'meca':
            if ((self.nSob+self.nSub)<7) and ((self.tSub+self.tSob)<0.17):
                self.requiereRegulador = False
            else:
                self.requiereRegulador = True


        if not self.requiereRegulador:
            wkhAhorroBimestral = (self.w-self.dbPro.at[0,'standby'])*24*60/1000
            ahorroBimestral    = wkhAhorroBimestral*self.DAC
            roi                = self.dbPro.at[0,'costo']/ahorroBimestral/6
            df = pd.DataFrame({
                'tipo': ['Protector'],
                'cantidad': [1],
                'costo': [self.dbPro.at[0,'costo']],
                'link': [self.dbPro.at[0,'link']],
                'kwhAhorroBimestral': [wkhAhorroBimestral],
                'ahorroBimestral': [ahorroBimestral],
                'roi': roi,
                'accion': ['compra']})
            self.sustitutos = self.sustitutos.append(df.loc[df.roi<3,:], ignore_index=True)

    def armarTxt(self):
        txt = ''
        print('\nIniciando armarTxt')
        if not self.val:
            print('Variables no validadas - No se puede proceder con el módulo')
        else:
            print('INICIANDO MÓDULO DE REGULADORES DE FORMA INDIVIDUAL\n')
            if self.vEst:
                txt = txt + fc.selecTxt(self.libReg,'REG01').replace('[nomReg]',self.nomReg)
                df = pd.DataFrame({
                    'kwhAhorroBimestral': self.w*24*60/1000,
                    'ahorroBimestral': self.w*24*60*self.DAC/1000,
                    'accion': ['retirar']})
                self.sustitutos = self.sustitutos.append(df, ignore_index=True)
            else:
                if self.tol:
                    txt = txt + fc.selecTxt(self.libReg,'REG02').replace('[nomReg]',self.nomReg)
                    df = pd.DataFrame({
                        'kwhAhorroBimestral': self.w * 24 * 60 / 1000,
                        'ahorroBimestral': self.w * 24 * 60 * self.DAC / 1000,
                        'accion': ['retirar']})
                    self.sustitutos = self.sustitutos.append(df, ignore_index=True)
                else:
                    self.checkProtector()
                    if not self.requiereRegulador:
                        if len(self.sustitutos)<1:
                            txt = txt + '[CON ESTOS DATOS EL PROTECTOR DE VOLTAJE NO ES VIABLE]'
                        elif self.uso == 'elec':
                            reemplazo = fc.ligarTextolink('Protector de voltaje', self.sustitutos.at[0, 'link']) + \
                                        ' con ahorro anual de $' + str(
                                round(self.sustitutos.at[0, 'ahorroBimestral']*6, 2))
                            txt = txt + fc.selecTxt(self.libReg, 'REG03S01').replace('[recomendación]',reemplazo)
                        elif self.uso == 'meca':
                            reemplazo = fc.ligarTextolink('Protector de voltaje', self.sustitutos.at[0, 'link']) + \
                                        ' con ahorro anual de $' + str(
                                round(self.sustitutos.at[0, 'ahorroBimestral']*6, 2))
                            txt = txt + fc.selecTxt(self.libReg, 'REG03S02').replace('[recomendación]',reemplazo)
                    else:
                        if self.w < self.ref:
                            txt = txt + fc.selecTxt(self.libReg,'REG04').replace('[nomReg]',self.nomReg)
                            self.atacable = 'No'
                        else:
                            self.recRem()
                            if len(self.sustitutos)<1:
                                txt = txt + 'Te recomendamos cambiar tu regulador por uno más eficiente, lamentablemente no encontramos uno adecuado en nuestra base de datos.'
                            elif self.roiM3:
                                reemplazo = 'Con este regulador que te recomendamos podrías lograr un ahorro anual de $' + str(int(self.sustitutos.at[0,'ahorroBimestral']*6))+ '. Aquí te dejamos el '+fc.ligarTextolink('Link de compra',self.sustitutos.at[0,'link'])
                                txt = txt + fc.selecTxt(self.libReg,'REG05').replace('[recomendación]',reemplazo).replace('[nomReg]',self.nomReg)
                            else:
                                reemplazo = 'Con este regulador que te recomendamos podrías lograr un ahorro anual de $' + str(int(self.sustitutos.at[0, 'ahorroBimestral']*6))+'. Aquí te dejamos el '+fc.ligarTextolink('Link de compra',self.sustitutos.at[0, 'link'])
                                txt = txt + fc.selecTxt(self.libReg, 'REG06').replace('[recomendación]', reemplazo).replace('[nomReg]',self.nomReg)
        txt = txt.replace('\n','<br />')
        self.txt = txt

