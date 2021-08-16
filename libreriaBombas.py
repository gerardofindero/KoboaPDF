# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 13:29:50 2021

@author: Azure
"""

#------------------------------------------------------
# *1 AGUA UTILIZADA AL DÍA POR PERSONA
# Una persona usa de 80-100 galones en EU
# (302-378 Litros) de agua por dia 
# Consideración de 90 galones por dia, 340 litros por día
# la OMS recomienda que una persona use 100L por día 
# Conagua reporto 314L per capita en 2010
#-------------------------------------------------------
# *2 Los tinacos tienen una capacidad/persona proemdio de 220 L
#-------------------------------------------------------
# *3 De cuanto tiempo se dispone para llenar los reservorios?
# ya que aumentar el gasto de agua incrmentara el cabezal necesitado
# Segun Tzatchkov et al 2005 el gasto más alto de 3 hogares fue
# de u=5.57 y sigma=3.56 L/min (Usar solo una desviación estandar?)
# Ventanas de uso de mas grande u=21.22 y sigma= 74.16  
#-------------------------------------------------------
# v = Q/A (Q:gasto A:área de la tuberia = pi*Diametro^2 / 4)
# como determinar una Q adecuada? *3
# v_max = (u+sigma) * (1min/60seg) / A = 0.15 L/s / A
# v_pro = (u)       * (1min/60seg) / A = 0.09 L/s / A
# v_min = (u-sigma) * (1min/60seg) / A = 0.03 L/s / A
# diamtros valvulas de llenado rotoplas
# 1/2 pulgadas
# 3/4 pulgadas
# 2   pulgadas
 
# Hbomba = Hs+Hd (Hd = K*v^2 / 2*g) 
# Hcisterna : profundidad de la cisterna 
# Hdescarga : distancia de la cisterna a al nivel de desarga
# Hs min = Hdescarga
# Hs max = Hdescaga + Hcisterna

# K = Kaccesorios + Ktuberia
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
class libreriaBombasGravitacionales:
    def __init__(self):
        self.kc90 = 1   # factor de resisencia de codo de 90°
        self.g    = 9.8 # mestro por segundo
        try:
            self.cur = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/curBom.xlsx")
            self.dbB = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/Base de datos de bombas gravitacionales.xlsx",
                sheet_name='Base de datos')
        except:
            self.cur = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/curBom.xlsx")
            self.dbB  = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/Base de datos de bombas gravitacionales.xlsx",
                sheet_name='Base de datos')

    def valData(self,hrsUso=None,w=None,Q=None,
                nC90=None,Hdescarga=None,
                material=None,longT=None,diametroInt=None):
        self.val = True
    
    def setData(self,hrsUso=None,w=None,Z=None,Q=None,L=None,D=None,nC90=None,material=None,T=None):
        """

        :param hrsUso:
        :param w:
        :param Z: Cabezal estatico en metros
        :param Q: Caudal  en litros por min
        :param L: longitud Tuberia en m
        :param D: Diamestro interno de la tuberia en m
        :param nC90: numero de codos
        :param T:  temperatura en °C
        :param material:   material de tuberia
        """
        Qc = Q/100/60 # Qc (Q de la casa)=>litros/min (1m3/1000L)(1min/60s)  -> m3/s
        D  = D/100 #convertir Diametro interno de centimetros a metros
        Qp = np.linspace(1, 200, 200)/1000/60 # Qp (Q de prueba)=>litros/min (1m3/1000L)(1min/60s)  -> m3/s
        df = pd.DataFrame({'Qp(m3/s)':Qp})
        df['Hp']=0
        for i in range(200):
            df.loc[i,'Hp']=estH(Z=Z,Q=df.at[i,'Qp(m3/s)'],L=L,D=D,nC90=nC90,material=material,T=T)
        self.cur['Hp']=df.loc[:,'Hp']
        self.dbB['Qp']=0
        self.dbB['Hp']=0
        # descomentar para revizar graficas y ver el punto de operacion con cada bomba
       # print(self.cur.loc[10:40,:])
        #demo=self.cur.set_index(['Q(L/min)'],drop=True,inplace=False)
        #demo.plot()
        #plt.show()
        ms = self.cur.columns[1:-2]
        print(ms)

        for m in ms:
            idx=(self.cur.loc[:,m]-self.cur.loc[:,'Hp']).abs().idxmin()
            self.dbB.loc[self.dbB.index[self.dbB.Modelo == m][0], 'Qp'] = self.cur.at[idx, 'Q(L/min)']
            self.dbB.loc[self.dbB.index[self.dbB.Modelo == m][0], 'Hp'] = self.cur.at[idx, 'Hp']

        tc   = 1000/Q
        kwhc = w*tc/60/1000
        self.dbB['t']=1000/self.dbB.Qp
        self.dbB['kwh']=self.dbB.loc[:,'Potencia (HP)']*self.dbB.loc[:,'t']*0.7457/60
        self.dbB['%ahorro']=1-(self.dbB.kwh/kwhc)
        print(self.dbB.loc[:, ['Modelo','Hmin', 'Hmax', 'Qp', 'Hp','t','kwh','%ahorro']])
        print(tc, kwhc)


    def reemplazo(self):
        filtro=(self.H>self.dbB.Hmin)&(self.H<self.dbB.Hmax)
        indx=self.dbB.index[filtro]
        for i in indx:
            self.optimizar(i)
    def optimizar(self,i):
        Hc   = self.H
        V = 1000  # litros
        for i2 in range(3):
            coef = self.dbB.loc[i,['a','b','c']].values
            #Qb   = np.max(np.roots(coef-np.array([0,0,Hc]))) # litros por minuto
            Qb = np.max(np.roots(coef ))  # litros por minuto
            t    = V/Qb # tiempo en minutos
            kw   = self.dbB.at[i,'Potencia (HP)']*0.7457 # conversion HP a kw
            kwh  = t*kw/60 # kw*min*(1hr/60min)
            v    = Qb/self.A/60/1000
            f    = est_f(v,self.D,self.vis,self.Km)
            Kt   = f*self.L/self.D
            Hc   = self.H+(self.Ka+Kt)*(v**2)/2/self.g
        print(self.Kt, Kt)
        print(self.v, v)
        print(self.f, f)
        print(self.H, Hc)
        print(self.Q, Qb)

def est_v(Q,A):
    # Q en m3/sec
    # A en m2
    # v en m/sec
    v=Q/A
    return v
def est_A(D):
    # D en me
    # A en m2
    A = np.pi*(D**2)/4
    return A
def est_Ka(nC90,D):
    D = D*100
    try:
        dbka = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='Kaccesorio')
    except:
        dbka = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='Kaccesorio')
    Ka_indx = (dbka.loc[:, 'diametro interno cm min'] - D).abs().idxmin()
    kC90 = dbka.at[Ka_indx, 'K']
    return nC90*kC90
def est_vis(T):
    try:
        dbpa = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='porpAgua')
    except:
        dbpa = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='propAgua')
    dif = dbpa.loc[:, 'Temp. [°C]'] - T
    vis = dbpa.at[dif.abs().idxmin(), 'Kin. Viscosity [mm²/s]'] / 1.0E+6  # viscocidad del agua en funcion de la temperatura
    return vis

def estH(Z,Q,L,D,nC90,material,T):
    """
    Estimación de cabezal en funcion de ...
    :param Z: Cabezal estatico en metros
    :param Q: Caudal  en m3/s
    :param L: longitud Tuberia en m
    :param D: Diamestro interno de la tuberia en m
    :param nC90: numero de codos
    :param T:  temperatura en °C
    :param material:   material de tuberia
    :return:
    """
    g      = 9.8        # gravedad         - m/s
    A      = est_A(D)   # Área interna     - m2
    v      = est_v(Q,A) # velocidad        - m/s
    Ka     = est_Ka(nC90,D) # adimencional número de codos por resistencia de codos
    vis    = est_vis(T)
    km     = est_km(material)
    f      = est_f(v,D,vis,km)
    Kt     =est_Kt(f,L,D)
    K      = Ka + Kt    # adimencionales
    Hd     = K * (v**2)/2/g
    H      = Z + Hd
    return H
def est_km(material):
    try:
        dbkm = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='Kmaterial')
    except:
        dbkm = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='Kmaterial')
    Km_indx = dbkm.index[dbkm.Superficie.str.contains(material)][0]
    km = dbkm.at[Km_indx, 'max K (10^-3)m'] * 1E-3
    return km

def est_f(v,D,vis,km):
    Re = v*D/vis      # velocidad por diametro entre viscocidad (en funcion de la temperatura)
    num=0.25          # numerado de la funcion para calcular el coeficiente de friccion
    den=(km/3.7/D)+(5.74/(Re**0.9)) # denominado km: factor k del material D: diametro de la tuberia
    den=np.log10(den)**2
    f = num/den
    return f

def est_Kt(f,L,D):
    return f*L/D

def graficas():
    try:
        dbB = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/Base de datos de bombas gravitacionales.xlsx",
            sheet_name='Base de datos')
    except:
        dbB = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/Base de datos de bombas gravitacionales.xlsx",
            sheet_name='Base de datos')
    ms=dbB.loc[:,'Modelo'].unique()
    Q = np.linspace(1,200,200)
    curBom=pd.DataFrame({'Q(L/min)':Q})
    for m in ms:
        p=dbB.loc[dbB.Modelo==m,['a','b','c']].to_numpy().T
        curBom[m]=np.polyval(p,Q)
    curBom.to_excel('curBom.xlsx')