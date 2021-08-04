import pandas as pd
import re
import numpy as np
import funcionesComunes as fc

def analizarCTV(df,DAC):
    # A atacable D Nombre N texto Q claves
    txt=''
    df = df.copy()
    indexCTV = df.index[df.Q.str.contains('ctv',na=False)]
    df = df.loc[indexCTV, :]
    df[['ctv', 'tag', 'claves']] = df.loc[indexCTV,'Q'].str.split(pat=',', n=2, expand=True)
    df[['fuga','nombre1','nombre2','trash']] = df.loc[indexCTV,'D'].str.split(pat=' ', n = 3, expand=True)
    df = df.loc[~df.nombre1.str.contains('nobreak|no break|NoBreak|No Break|regulador|Regulador'),:]
    df.loc[:,'nombre1'] = (df.loc[:,'nombre1'] + ' '+df.loc[:,'nombre2']).str.replace('_',' ')
    tags = df.tag.unique()
    for tag in tags:
        claves=df.at[(df.index[df.tag==tag])[0],'claves']
        w = df.loc[df.tag==tag,'J'].sum()
        apa = df.loc[df.tag==tag,'nombre1'].tolist()
        apa = fc.listarComas(apa)
        libCTV= libreriaCTV()
        libCTV.setData(w=w,la=apa,clv=claves, DAC=DAC)
        libCTV.armarTxt()
        txt= libreriaCTV.txt+'\n'
    return txt




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
            print('lista de aparatos es nulla')
        elif not isinstance(la,str):
            print('lista de aparatos no es de tipo cadena')
        elif len(la)<=0:
            print('lista de dispositivos vacia')
        else:
            val_la = True

        if pd.isnull(clv):
            print('lista de claves es nulla')
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
        self.txt = txt.replace('\n','<br />')