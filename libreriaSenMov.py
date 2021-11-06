import numpy as np
import pandas as pd
from scipy.stats import norm
import funcionesComunes as fc
import unicodedata
def recoSensores (kwh = None,w = None, lugar = None ,dac = None,hrsUso=None):
    ls=libreriaSensores()
    ls.setData(kwh,w,lugar, dac,hrsUso)
    txt=ls.armarTxt()
    return txt.replace("<br />","")

class libreriaSensores:

    def __init__(self):
        self.txt = ''
        try:
            self.lib = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Sensores Movimiento/libreriaSensoresMovimiento.xlsx",
                sheet_name='libreriaSensoresMovimiento')
            self.links = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Sensores Movimiento/libreriaSensoresMovimiento.xlsx",
                sheet_name='links')
            self.stats = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Sensores Movimiento/libreriaSensoresMovimiento.xlsx",
                sheet_name='Calculadora')

        except:
            self.lib = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Sensores Movimiento/libreriaSensoresMovimiento.xlsx",
                sheet_name='libreriaSensoresMovimiento')
            self.links = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Sensores Movimiento/libreriaSensoresMovimiento.xlsx",
                sheet_name='links')
            self.stats = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Sensores Movimiento/libreriaSensoresMovimiento.xlsx",
                sheet_name='Calculadora')
        self.stats = self.stats.loc[self.stats.loc[:, "f"] == "s", :].reset_index(drop=True).copy()
        self.v=False
    def val(self, kwh, w, lugar,dac):
        val_kwh   = False
        val_w     = False
        val_lugar = False
        val_dac   = False

        if pd.isnull(lugar):
            print('lugar es nulo')
        elif not isinstance(lugar,str):
            print('lugar no es un str')
        else:
            val_lugar = True

        if pd.isnull(kwh):
            print('kwh es nulo')
        elif not isinstance(kwh, (int, float)):
            print('kwh no es numerico')
        elif kwh<0:
            print('kwh es igual a negativo')
        else:
            val_kwh = True

        if pd.isnull(w):
            print('w es nulo')
        elif not isinstance(w, (int, float)):
            print('w no es numerico')
        elif w<0:
            print('w es igual a negativo')
        else:
            val_w=True

        if pd.isnull(dac):
            print('DAC es nulo')
        elif not isinstance(dac,(int,float)):
            print('DAC no es numerico')
        elif dac<=0:
            print('DAC menor o igual a 0')
        else:
            val_dac=True

        if val_w and val_dac and val_kwh and val_lugar:
            self.v = True
        else:
            self.v = False

    def setData(self, kwh = None, w=None, lugar=None,dac=None,hrsUso=None):
        self.val(kwh,w,lugar,dac)
        if self.v:
            self.kwh   = kwh
            self.w     = w
            lugar = lugar.lower()
            nfkd  = unicodedata.normalize("NFKD",lugar)
            lugar = nfkd.encode("ASCII",'ignore')
            lugar = lugar.decode("utf-8")
            self.lugar = lugar
            self.dac   = dac
            self.hrsUso = hrsUso
            
    def armarTxt(self):
        txt='X'
        if self.stats.tags.str.contains(self.lugar).any():
            idx=self.stats.index[self.stats.tags.str.contains(self.lugar)][0]
            mean = self.stats.at[idx, "mean"]
            std  = self.stats.at[idx, "std" ]
            lam  = self.stats.at[idx, "lambdas"]
            perU = self.stats.at[idx,"percentil umbral"]
            #hrsUso = self.kwh*1000/self.w/60
            hrsUso = self.hrsUso/7
            hrsUsoT = ((hrsUso**lam)-1)/lam
            percentil= norm.cdf(hrsUsoT,mean,std)
            if percentil >= perU:
                roi = 200/(self.kwh*0.35*self.dac)/6
                if roi <= 3:
                    txt = txt+ fc.selecTxt(self.lib, "SEN01")
                else:
                    txt = txt+ fc.selecTxt(self.lib, "SEN02")
                vtl="[aqui-link]"
                vtb="[blog-link]"
                link = self.links.at[self.links.index[self.links.Variable==vtl][0], "Link"]
                linkC = fc.ligarTextolink("aqui",link)
                linkb = self.links.at[self.links.index[self.links.Variable==vtb][0], "Link"]
                linkB = fc.ligarTextolink("blog",linkb)
                txt = txt.replace(vtl,linkC).replace(vtb,linkB)

        return txt




