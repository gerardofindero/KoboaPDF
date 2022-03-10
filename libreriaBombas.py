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
#import matplotlib.pyplot as plt
import funcionesComunes as fc

def crearClavesBG(infEq):
    """
    w (potencia)
    kwh (consumo)

    :param infEq: Q/Z/L/nC90/D/T
    :return:
    """
    print("Creando claves de BG")
    # Claves para reemplazo de bomba
    claves = ""
    if float(infEq["FlujoSegundos"]) == 0: claves += ",0"
    else                                 : claves += ","+str(60/float(infEq["FlujoSegundos"]))
    if infEq["FlujoSegundos"]== 0: print("Q: 0")
    claves += "/"+str(infEq["Delta"])
    if infEq["Delta"]        == 0: print("Delta: 0m")
    claves += "/"+str(infEq["Longitud"])
    if infEq["Longitud"]     == 0: print("Longitud: 0m")
    claves += "/"+str(infEq["Codos"])
    if infEq["Codos"]        == 0: print("Número de codos: 0")
    claves += "/"+str(float(infEq["Diametro"])*0.0254)
    if infEq["Diametro"]     == 0: print("Diamtero: 0in")
    claves += "/"+str(infEq["Temperatura"])
    if infEq["Temperatura"]  == 0: print("Temperatura del agua: 0")
    if infEq["Material"] == "plastica":
        claves += "/PA"
    elif infEq["Material"] == "aluminio":
        claves += "/AL"
    elif infEq["Material"] == "hierro":
        claves += "/HI"
    elif infEq["Material"] == "NA":
        print("Material no estaba en kobo")
        claves += "/NA"
    else:
        print("Material: ",infEq["Material"],"?")
        claves += "/NA"
    ##### Claves de condiciones
    ## Sobrecalentamiento
    if "bobina"     in infEq["Termografia"]: claves += ",BO"
    if "rodamiento" in infEq["Termografia"]: claves += ",RO"
    if "general"    in infEq["Termografia"]: claves += ",GE"
    # Obstrucciones
    if "alto"       in infEq["Dureza"]     : claves += ",DU"
    if "si"         in infEq["Sarro"]      : claves += ",SA"
    # valvulas
    if "cerradas"   in infEq["Valvulas"]   : claves += ",VC"
    # Fugas
    if "si" in infEq["FugasSup"]: claves += ",FS"
    if "si" in infEq["FugasTer"]: claves += ",FT"
    # control
    if   "flotador"     in infEq["ControlTipo"]   : claves += ",CF"
    elif "electronivel" in infEq["ControlTipo"]   : claves += ",CE"
    elif "anillo"       in infEq["ControlTipo"]   : claves += ",CA"
    elif "ninguno"      in infEq["ControlTipo"]   : claves += ",CN"
    if   "no"           in infEq["ControlCierra"] : claves += ",NC"
    if   "si"           in infEq["ControlPeg"]    : claves += ",PE"
    if   "no"           in infEq["ControlContra"] : claves += ",NP"
    ########## Acceso y Permisos ###################
    if "no" in infEq["Encender"]    : claves += ",NB"
    if "no" in infEq["Acceso"]      : claves += ",ST"
    if "no" in infEq["AccesoBomba"] : claves += ",SB"
    ## Textos
    # Texto fugas
    claves+=","
    if len(infEq["FugaTxt"])!=0: claves += "-"+ infEq["FugaTxt"]
    else                       : claves += "-*"
    if len(infEq["ControlProblemas"])!=0 : claves += "-" + infEq["ControlProblemas"]
    else              : claves += "-*"
    # def setData(self, hrsUso=None,w=None, kwh=None,
    #            Q1   = None, Q2 = None, Q3 = None,
    #            wQ_r1=None, wQ_r2=None, wQ_r3=None,
    #            ac=None, control=None, elecB=None, con=None, termo=None, durCis=None, durTin=None,
    #            Z=None, Q=None, L=None, D=None, nC90=None, material=None, T=None):
    return claves

def leerLibreriaBG():
    try:
        cur = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/curBom.xlsx")
        dbB = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/Base de datos de bombas gravitacionales.xlsx",
            sheet_name='Base de datos')
        lib = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='libreriaBombas')
    except:
        cur = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/curBom.xlsx")
        dbB = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/Base de datos de bombas gravitacionales.xlsx",
            sheet_name='Base de datos')
        lib = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='libreriaBombas')
    lib = lib.set_index("lib")

    return [lib, dbB, cur]

def armarTxtBG(Claves,kwh,DAC,hrsUso,w):
    lib, dbB, cur = leerLibreriaBG()
    ClavesS = Claves.split(",")
    ClavesD = ClavesS[1].split("/") #Q/Z/L/nC90/D/T
    Q        = float(ClavesD[0])
    Z        = float(ClavesD[1])
    L        = float(ClavesD[2])
    nC90     = float(ClavesD[3])
    D        = float(ClavesD[4])
    T        = float(ClavesD[5])
    material = ClavesD[6]

    txt=""
    if kwh <= 23:
        txt += lib.at['BOM01',"Texto"]
    elif (kwh > 23) and (kwh <= 60):
        txt += lib.at['BOM02',"Texto"]
    elif kwh > 60:
        txt += lib.at['BOM03',"Texto"]

    if  ac == 'Si':
        txt += lib.at['BOM04',"Texto"]
    if "flotador" in control:
        txt += lib.at["BOM06","Texto"]
    if ("placas" in control) and (elecB == "No"):
        txt += lib.at["BOM07","Texto"]
    if "contrapeso" in control:
        if (elecB == "") and (con == ""):
            txt += lib.at["BOM08","Texto"]
        elif (elecB == "") and (con == ""):
            txt += lib.at["BOM09","Texto"]
        elif (elecB == "") and (con == ""):
            txt += lib.at["BOM10","Texto"]
    if "bobina" in termo:
        txt += lib.at["BOM12","Texto"]
    if "rodamiento" in termo:
        txt += lib.at["BOM13","Texto"]
    if "general" in termo:
        txt += lib.at["BOM14","Texto"]
    if durCis == "dura":
        txt += lib.at["BOM15","Texto"]
    if durTin == "dura":
        txt += lib.at["BOM16","Texto"]
    if (wQ_r1 >= 8.53):
        if (wQ_r3 is not None) and wQ_r3 >= 8.53:
            txt += lib.at["BOM20","Texto"]
        if (wQ_r3 is not None) and wQ_r3 < 8.53:
            txt += lib.at["BOM19","Texto"]
        if (wQ_r2 is not None) and wQ_r2 < 8.53:
            txt +=lib.at["BOM18","Texto"]
    if (wQ_r1 is not None) and wQ_r1 < 8.53:
        txt += lib.at["BOM17","Texto"]

    return txt


class libreriaBombasGravitacionales:
    def __init__(self):
        self.txt=''
        self.kc90 = 1   # factor de resisencia de codo de 90°
        self.g    = 9.8 # metros por segundo
        try:
            self.cur = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/curBom.xlsx")
            self.dbB = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/Base de datos de bombas gravitacionales.xlsx",
                sheet_name='Base de datos')
            self.lib = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
                sheet_name='libreriaBombas')
        except:
            self.cur = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/curBom.xlsx")
            self.dbB  = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/Base de datos de bombas gravitacionales.xlsx",
                sheet_name='Base de datos')
            self.lib = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
                sheet_name='libreriaBombas')

    
    #def setData(self, hrsUso=None,w=None, kwh=None,
    #            Q1   = None, Q2 = None, Q3 = None,
    #            wQ_r1=None, wQ_r2=None, wQ_r3=None,
    #            ac=None, control=None, elecB=None, con=None, termo=None, durCis=None, durTin=None,
    #            Z=None, Q=None, L=None, D=None, nC90=None, material=None, T=None):

    def setData(self, Claves,consumo,hrsUso,potencia):
        """
        :param hrsUso   : horas de uso a la semana
        :param w        : potencia de la bomba
        :param kwh      : kWh/bimestre
        :param wQ_r1    : relación potencia flujo inicial
        :param wQ_r2    : relación potencia flujo tras abrir vavulas
        :param wQ_r3    : relación potencia flujo tras cebar bomba
        :param ac       : acumulación de sarro
        :param control  : tipos de control
        :param elecB    : estado del electronivel
        :param con      : contrapeso
        :param termo    : termografía
        :param durCis   : dureza cisterna
        :param durTin   : dureza tinaco
        :param Z        : Cabezal estatico en metros
        :param Q        : Caudal en litros por min
        :param L        : longitud Tuberia en m
        :param D        : Diamestro interno de la tuberia en m
        :param nC90     : numero de codos
        :param T        : temperatura en °C
        :param material : material de tuberia
        """

        ClavesS=Claves.split(",")
        # Q/Z/L/nC90/D/T
        Q, Z, L, nc90, D, T = ClavesS[1].split("/")
        self.Z    = float(Z)
        self.Q    = float(Q)
        self.L    = float(L)
        self.D    = float(D)
        self.nc90 = float(nc90)
        self.T    = float(T)

        self.hrsUso  = hrsUso
        self.w       = potencia
        self.kwh     = consumo
        self.wQ_r1   = wQ_r1
        self.wQ_r2   = wQ_r2
        self.wQ_r3   = wQ_r3

        self.Q1=Q1
        self.Q2=Q2
        self.Q3=Q3

        self.ac      = ac
        self.control = control
        self.elecB   = elecB
        self.con     = con
        self.termo   = termo
        self.durCis  = durCis
        self.durTin  = durTin


        self.material = material

        self.txt = ''

        #self.Qm3s    = Q/100/60 # Qm3s (Q de la casa)=>litros/min (1m3/1000L)(1min/60s) -> m3/s


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
        # demo=self.cur.set_index(['Q(L/min)'],drop=True,inplace=False)
        # demo.plot()
        # plt.show()
        ms = self.cur.columns[1:-2]
        print(ms)

        for m in ms:
            idx = (self.cur.loc[:, m]-self.cur.loc[:, 'Hp']).abs().idxmin()
            self.dbB.loc[self.dbB.index[self.dbB.Modelo == m][0], 'Qp'] = self.cur.at[idx, 'Q(L/min)']
            self.dbB.loc[self.dbB.index[self.dbB.Modelo == m][0], 'Hp'] = self.cur.at[idx, 'Hp']

        tc   = 1000/Q
        kwhc = w*tc/60/1000
        self.dbB['t']=1000/self.dbB.Qp
        self.dbB['kwh']=self.dbB.loc[:, 'Potencia (HP)']*self.dbB.loc[:, 't']*0.7457/60
        self.dbB['%ahorro']=1-(self.dbB.kwh/kwhc)
        print(self.dbB.loc[:, ['Modelo','Hmin', 'Hmax', 'Qp', 'Hp','t','kwh','%ahorro']])
        print(tc, kwhc)

    def armarTxt(self):
        txt = ''
        if self.kwh <= 22:
            txt =txt + fc.selecTxt(self.lib,'BOM01')
        elif (self.kwh>22) and (self.kwh<=60):
            txt = txt + fc.selecTxt(self.lib, 'BOM02')
        elif self.kwh > 60:
            txt = txt + fc.selecTxt(self.lib, 'BOM03')
        if self.ac=='Si':
            txt = txt + fc.selecTxt(self.lib, 'BOM04')
        if "flotador" in self.control:
            txt = txt + fc.selecTxt(self.lib, "BOM06")
        if ("placas" in self.control) and (self.elecB == "No"):
            txt = txt + fc.selecTxt(self.lib, "BOM07")
        if "contrapeso" in self.control:
            if   (self.elecB == "") and (self.con == ""):
                txt = txt + fc.selecTxt(self.lib, "BOM08")
            elif (self.elecB == "") and (self.con == ""):
                txt = txt + fc.selecTxt(self.lib, "BOM09")
            elif (self.elecB == "") and (self.con == ""):
                txt = txt + fc.selecTxt(self.lib, "BOM10")
        if "bobina" in self.termo:
            txt = txt + fc.selecTxt(self.lib, "BOM12")
        if "rodamiento" in self.termo:
            txt = txt + fc.selecTxt(self.lib, "BOM13")
        if "general" in self.termo:
            txt = txt + fc.selecTxt(self.lib, "BOM14")
        if self.durCis == "dura":
            txt = txt + fc.selecTxt(self.lib, "BOM15")
        if self.durTin == "dura":
            txt = txt + fc.selecTxt(self.lib, "BOM16")
        if (self.wQ_r1>= 8.53):
            if (self.wQ_r3 is not None) and self.wQ_r3 >= 8.53:
                txt = txt + fc.selecTxt(self.lib, "BOM20")
            if (self.wQ_r3 is not None) and self.wQ_r3 < 8.53:
                txt = txt + fc.selecTxt(self.lib, "BOM19")
            if (self.wQ_r2 is not None) and self.wQ_r2 < 8.53:
                txt = txt + fc.selecTxt(self.lib, "BOM18")
        if (self.wQ_r1 is not None) and self.wQ_r1 < 8.53:
            txt = txt + fc.selecTxt(self.lib, "BOM17")
        return txt

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
    Estimación de cabezal
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