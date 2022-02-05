import pandas as pd
import re
import numpy as np
import funcionesComunes as fc

def analizarCTV(df,DAC):
    libCTV= libreriaCTV()
    txt='.'
    clave=df['Q']

    if 'decodificador' in df['D'].lower():
        txt='El decodificador puede mantenerse apagado y prenderse el domingo en la madrugada para actualizarse. <br />'
    if 'consola' or 'nintendo' in df['D'].lower():
        txt='Lo mejor es mantener completamente apagada la consola, muchas veces se queda en modo espera. <br />'
    # A atacable D Nombre N texto Q claves

    return txt

def leerExcel():
    try:
        lib = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
            sheet_name='libreriaCTV')
        links = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
            sheet_name='links')
        variables = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
            sheet_name='variables')
    except:
        lib = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
            sheet_name='libreriaCTV')
        links = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
            sheet_name='links')
        variables = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
            sheet_name='variables')
    return [lib,links,variables]


def analizarCTV(standby,DAC,listaDispositivos):
    """

    Parameters
    ----------
    standby: standby de dispositivos en el cluster de TV
    DAC
    listaDispositivos: lista con el nombre de dispositivos en el cluster de TV

    Returns
    [consejo,df con potencial de ahorro]
    -------

    """
    lib,links,variables = libreriaCTV()
    txt=''
    if standby < 2:
        txt = txt +fc.selecTxt(lib,"CTV01")
    else:
        kwhAhorrado=(standby*24*60/1000)*0.33
        ahorroBimestral = kwhAhorrado*DAC
        ROI             = 250/ahorroBimestral/6
        if ROI <= 3:
            txt = txt+fc.selecTxt(lib,"CTV02")
        else:
            txt = txt+fc.selecTxt(lib,"CTV03")
    """
    if 'decodificador' in listaDispositivos:
        txt = txt+' El decodificador puede mantenerse apagado y prenderse el domingo en la madrugada para actualizarse. <br />'
    if 'consola' or 'nintendo' in listaDispositivos:
        txt = txt+' Lo mejor es mantener completamente apagada la consola, muchas veces se queda en modo espera. <br />'

    txt=txt.replace("[recomendacion]",fc.ligarTextolink("Timer inteligente",links.iat[0,2]))
    if len(listaDispositivos)>1:
        txt = txt.replace('{el/los}','los').replace("{s}",'s').replace("{n}","n")
    else:
        txt = txt.replace('{el/los}', 'el').replace("{s}", '').replace("{n}", "")
    """
    PotAhorro = pd.DataFrame(index=[0], columns=["%Ahorro", "kwhAhorrado", "Accion"])
    if "timer" in txt:
        PotAhorro.loc[0,'%Ahorro']   = 0.33
        PotAhorro.loc[0,"kwhAhorro"] = ahorroBimestral
        PotAhorro.loc[0,'Acción']    = fc.selecTxt(lib,"CTVpa01").replace("[timer]",fc.ligarTextolink("Timer inteligente",links.iat[0,2]))
    return [txt, PotAhorro]


class libreriaCTV:
    def __init__(self):
        self.txt=''
        self.sustitutos = pd.DataFrame(
            columns=['tipo', 'cantidad', 'costo', 'link', 'kwhAhorroBimestral', 'ahorroBimestral', 'roi', 'accion'])
        try:
            self.libCTV = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
                sheet_name='libreriaCTV')
            self.links = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
                sheet_name='links')
            variables = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
                sheet_name='variables')
        except:
            self.lib = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
                sheet_name='libreriaCTV')
            self.links = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
                sheet_name='links')
            variables = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
                sheet_name='variables')
        self.val = False
        self.ct  = variables.at[variables.index[variables.variables=='nt' ][0],'costo']
        self.cs  = variables.at[variables.index[variables.variables=='ns' ][0],'costo']
        self.cm6 = variables.at[variables.index[variables.variables=='nm6'][0],'costo']
        self.cm8 = variables.at[variables.index[variables.variables=='nm8'][0],'costo']
        self.ce1 = variables.at[variables.index[variables.variables=='ne1'][0],'costo']
        self.ce2 = variables.at[variables.index[variables.variables=='ne2'][0],'costo']
        self.ca  = variables.at[variables.index[variables.variables=='na' ][0],'costo']
        self.cce = variables.at[variables.index[variables.variables=='nce'][0],'costo']
        self.ccs = variables.at[variables.index[variables.variables=='ncs'][0],'costo']

    def validarDatos(self,w=None,la=None,clv=None,DAC=None):
        print('\n Validando variables (CTV)')
        val_w    = False
        val_la   = False
        val_clv  = False
        val_DAC  = False
        self.val = False

        if pd.isnull(w):
            print('w es nulo')
        elif not isinstance(w,(int,float)):
            print('w no es numerico')
        elif w<0:
            print('w es igual a negativo')
        else:
            val_w=True
        if pd.isnull(la):
            print('lista de aparatos es nula')
        elif not isinstance(la,str):
            print('lista de aparatos no es de tipo cadena')
        elif len(la)<=0:
            print('lista de dispositivos vacia')
        else:
            val_la = True

        if pd.isnull(clv):
            print('lista de claves es nula')
        elif not isinstance(clv,str):
            print('lista de claves no es de tipo cadena')
        else:
            val_clv = True

        if pd.isnull(DAC):
            print('DAC es nulo')
        elif not isinstance(DAC,(int,float)):
            print('DAC no es numerico')
        elif DAC<=0:
            print('DAC menor o igual a 0')
        else:
            val_w=True

        if val_w and val_la and val_clv and val_DAC:
            self.val=True
        else:
            self.val=False

    def checkROI(self):
        costo = 0
        c     = 0

        if re.search('1t'):
            costo+= self.ct
            c+=1

        if re.search('2t'):
            costo+= self.ct*2
            c += 1

        if re.search('1s'):
            costo+= self.cs
            c += 1
        if re.search('2s'):
            costo+= self.cs*2
            c += 1

        if re.search('1m6'):
            costo+= self.cm6
            c += 1
        if re.search('2m6'):
            costo+= self.cm6*2
            c += 1

        if re.search('1m8'):
            costo+=self.cm8
            c += 1
        if re.search('2m8'):
            costo+=self.cm8*2
            c += 1

        if re.search('1e1'):
            costo+=self.ce1
            c += 1
        if re.search('2e1'):
            costo+=self.ce1*2
            c += 1

        if re.search('1e2'):
            costo += self.ce2
            c += 1
        if re.search('2e2'):
            costo += self.ce2 * 2
            c += 1

        if re.search('1a'):
            costo += self.ca
            c += 1
        if re.search('2a'):
            costo += self.ca*2
            c += 1

        if re.search('1ce'):
            costo += self.cce
            c += 1
        if re.search('2ce'):
            costo += self.cce*2
            c += 1

        if re.search('1cs'):
            costo += self.ccs
            c += 1
        if re.search('2cs'):
            costo += self.ccs * 2
            c += 1

        if costo == 0: costo += self.ct


        kwhAhorroBimestral = (self.w - 2)*24*60/1000
        ahorroBimestral    = kwhAhorroBimestral*self.DAC
        roi = costo/ahorroBimestral/6
        if roi <=3:
            self.roiM3 = True
        else:
            self.roiM3 = False

        df = pd.DataFrame({
            'tipo': ['timer['+self.clv+']'],
            'cantidad': [1],
            'costo': [costo],
            'link': [self.links.at[0, 'link']],
            'kwhAhorroBimestral': [kwhAhorroBimestral],
            'ahorroBimestral': [ahorroBimestral],
            'roi': roi,
            'accion': ['compra']})
        self.sustitutos = self.sustitutos.append(df.loc[df.roi < 3, :], ignore_index=True)

    def setData(self,w = None, la = None,clv=None, DAC=None):
        self.roiM3=False
        print('Iniciando setData de libreria CTV')
        self.validarDatos(w=w,la=la,clv=clv,DAC=DAC)
        if self.val:
            self.w   = w
            self.la  = la
            self.clv = clv
            self.DAC = DAC
            print('\nVariables aceptadas')
        else:
            print('\nVariables no aceptadas\nSet Data fallido')
    def armarTxt(self):
        print('Iniciando armadado de texto para CTV')
        txt=''
        if self.w<2:
            if len(self.la.split('y'))>1:
                txt = txt + fc.selecTxt(self.lib,'CTV01').replace('{s}','').replace('{n}','').replace('{el/los}','el')
            else:
                txt = txt + fc.selecTxt(self.lib, 'CTV01').replace('{','').replace('}','').replace('{el/los}','los')
        else:
            self.checkROI()
            reemplazo = fc.ligarTextolink('Timer inteligente', self.sustitutos.at[0, 'link']) + \
                        ' con ahorro anual de $' + str(round(self.sustitutos.at[0, 'ahorroBimestral'] * 6, 2))
            if self.roiM3:
                if len(self.la.split('y')) > 1:

                    txt = txt + fc.selecTxt(self.lib, 'CTV03').replace('{s}', '').replace('{n}', '').replace('{el/los}',
                                                                                                             'el')
                else:
                    txt = txt + fc.selecTxt(self.lib, 'CTV03').replace('{', '').replace('}', '').replace('{el/los}',
                                                                                                         'los')
            else:
                if len(self.la.split('y')) > 1:

                    txt = txt + fc.selecTxt(self.lib, 'CTV02').replace('{s}', '').replace('{n}', '').replace('{el/los}',
                                                                                                             'el')
                else:
                    txt = txt + fc.selecTxt(self.lib, 'CTV02').replace('{', '').replace('}', '').replace('{el/los}',
                                                                                                         'los')
                txt = txt.replace('[recomendacion]',reemplazo)
        self.txt = txt.repla