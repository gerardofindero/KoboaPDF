import numpy as np
import pandas as pd
import funcionesComunes as fc
from libreriaHielo import recoMaqHie
from scipy.stats import norm
# 1.b. Lee otra librería (ver cuál es la Protolibreria)
def libreria2():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/Refrigeradores/libreriaRefrisV3s.xlsx",sheet_name='Libreria')
    except:
        Libreria = pd.read_excel(f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Refrigeradores/libreriaRefrisV3s.xlsx",sheet_name='Libreria')
    Libreria=Libreria.set_index('Codigo')
    return Libreria
def linkss():
    try:
        links = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/Refrigeradores/libreriaRefrisV3s.xlsx",sheet_name='links')
    except:
        links = pd.read_excel(f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Refrigeradores/libreriaRefrisV3s.xlsx",sheet_name='links')
    links=links.set_index('variable')
    return links

def ClavesRefri(EquiposRefri):

    EquiposR = EquiposRefri
    #EquiposR = EquiposR.dropna(subset=['Pot Compresor'])
    #EquiposR = EquiposR.fillna(0)
    for i in EquiposR.index:

        if np.isnan(EquiposR['Temp Refri'][0])    : TempR = 100
        else                                      : TempR = (EquiposR['Temp Refri'][0])
        if np.isnan(EquiposR['Temp Conge'][0])    : TempC = 100
        else                                      : TempC =(EquiposR['Temp Conge'][0])
        if np.isnan(EquiposR['Pot Compresor'][0]) : NominalComp = 100
        else                                      : NominalComp = int(EquiposR['Pot Compresor'][0])
        if np.isnan(EquiposR['Temp Compresor'][0]): TempComp = 100
        else                                      : TempComp = float(EquiposR['Temp Compresor'][0])
        Volumen =int(EquiposR['Volumen'][0])
        if  np.isnan(EquiposR["Encendido"][0])    : Encendido = 60
        else                                      : Encendido = float(EquiposR["Encendido"][0])
        Codigo=EquiposR['Clave'][0]
        Codigo = str(Codigo)+','+str(TempR)+'/'+str(TempC)+'/'+ str(NominalComp) + '/'+str(TempComp) + '/'+str(Volumen)+"/"+str(Encendido)
        #print("codigo",Codigo)
####### Detalles      #######################################
        # Disposicion congelador
        if "CN" in Codigo:
            if   "vertical"   in EquiposR["Disposicion"][0]: Codigo+=",CVE"
            elif "horizontal" in EquiposR["Disposicion"][0]: Codigo+=",CHO"
        # Alarma
        if "inexistente"  in str(EquiposR["Alarma"])    : Codigo += ",AI"
        if "descompuesto" in str(EquiposR["Alarma"])    : Codigo += ",AD"
        # Ventilas
        if "no"           in str(EquiposR["Ventilas"])  : Codigo += ",SV"
        # Porcentaje de prendido
        if ("prolongado"  in str(EquiposR["Prob Refr"]))\
        or ("ontiempo"    in str(EquiposR["Prob Refr"])): Codigo += ",PR"
        # Ciclos de deshielo continuos
        if "deshielo"     in str(EquiposR["Prob Refr"]) : Codigo += ",DH"
####### Causas suaves #######################################
        # Ventilacion
        if '1'          in str(EquiposR['Encerrado']) : Codigo += ",VN"
        # Evaporador sucio
        if 'suciedad'   in str(EquiposR['Prob Comp']) : Codigo += ",SU"
####### Causas tecnica ######################################
        # compresor a alta potencia
        if (NominalComp > 120) \
        or ("altapotencia" in str(EquiposR["Prob Refr"])) :Codigo += ",CN"
        # empaque
        if "si" in str(EquiposR["Empaques"]): Codigo += ",EM"
        # difusor mal
        if ("potenciaventilador" in str(EquiposR["Prob Comp"] ))\
        or ("tocandolo"          in str(EquiposR["Difusor"]   ))\
        or ("detenido"           in str(EquiposR["Difusor"]   ))\
        or ("rotas"              in str(EquiposR["Difusor"]   ))\
        or ("otro"               in str(EquiposR["Difusor"]   )): Codigo += ",DM"
        # tuberias picadas | fugas de refrigerante
        if "si" in str(EquiposR["Tuberias"]): Codigo += ",FG"
        # puertas dañadas
        if "puertasdanadas"     in str(EquiposR["Cierre"]): Codigo += ",PD"
####### orientación congelador ############
    return  Codigo


def Clasifica(Claves):
    ClavesSep='N'
    if pd.notna(Claves):
        ClavesSep=Claves.split(", ")
    return ClavesSep[0]


def LeeClavesR(Claves,notas,nombre,consumo):
    #print("LibreriaRefris.py Claves",Claves)
    #print("Claves refrigeracion",Claves)
    kWh   = float(consumo)
    Texto = ''

    TextoF = notas
    PotencialAhorro=0
    PotAhorro = pd.DataFrame(index=[0], columns=["%Ahorro", "kwhAhorrado", "Accion"])
    lib = libreria2()
    links = linkss()
    PotAhorro['Accion'] = ""

    if pd.notna(Claves):

        ClavesSep=Claves.split(",")

        equipoR=ClavesSep[0]
        print(equipoR)
        Datos= ClavesSep[1].split("/")
        TRef      = float(Datos[0])
        TCong     = float(Datos[1])
        NomCom    = float(Datos[2])
        TempCom   = float(Datos[3])
        Volumen   = float(Datos[4])
        Encendido = float(Datos[5])/100
        #print(Claves, ClavesSep[0])
        #print("NomCom",NomCom)
        #print("TempCom",TempCom)
        #print("Volumen",Volumen)
        #print("TRef",TRef)
        #print("TCong",TCong)
        #print("Encendido",Encendido)




        Ns = 0
        if equipoR == "CV":
            if (TRef < 12): Ns+=1
        else:
            if (TRef < 4) or (TCong < -14): Ns += 1
        if "VN" in Claves: Ns += 1
        if "SU" in Claves: Ns += 1
        EncendidoNs = Encendido - (0.07 * Ns)

        Nt = 0
        if "EM" in Claves: Nt += 1
        if "DM" in Claves: Nt += 1
        if "FG" in Claves: Nt += 1
        if "PD" in Claves: Nt += 1

        if (equipoR=='RF') or (equipoR=="MB"):
            Volumen = float(Datos[4]) * 0.000022
            percentil = norm.cdf(((float(kWh)*6.0)**0.1 - (1.738365 + 0.0057272 * Volumen))/0.01962684,loc=0,scale=1)
            percentilNs = norm.cdf((((1 - 0.07 * Ns) * float(kWh) * 6.0) ** 0.1 - (1.738365 + 0.0057272 * Volumen)) / 0.01962684, loc=0,scale=1)
        if equipoR=="CV":
            formulaV = (Volumen / 1300.8) + 21.4
            formulaR = (Volumen / 1300.8) + 51.6
        if equipoR=="CN":
            if "CHO" in Claves:
                formulaV = (Volumen / 8000.35) - 7.58
                formulaR = (Volumen / 3955.11) - 15.33
            if "CVE" in Claves:
                formulaV = (Volumen / 6863.63) - 8.83
                formulaR = (Volumen / 3432.19) - 17.67
        if equipoR == "CV" or equipoR == "CN":
            if kWh < formulaV              : percentil = 0.20
            elif formulaV <= kWh < formulaR: percentil = 0.50
            else                           : percentil = 0.95
            if kWh*(1-(Ns*0.07)) < formulaV             : percentilNs = 0.20
            elif formulaV<= kWh*(1-(Ns*0.07)) < formulaR: percentilNs = 0.50
            else                                        : percentilNs = 0.95
            #print("percentil libreria", percentil)
            #print("percentil Ns libreria", percentilNs)
        #print("EncendidoNs", EncendidoNs)
        #print("Ns", Ns)
        #print("Percentil ori",percentil)
        #print("Percentil Ns",percentilNs)
        #print("kwh kwhNs",kWh,kWh*(1-(0.07*Ns)))

        #print("Nt",Nt)
        if percentil<0.3:
            #### Zona verde ####
            Texto += lib.loc['REF001','Texto'] + lib.loc["REF015","Texto"]
        elif percentil>=0.90:
            #### NS a amarillo ####
            if percentilNs<0.90:
                Texto += lib.loc['REF002', 'Texto']
                # Temperaturas muy bajas
                if Ns > 0:
                    Texto += lib.loc["REF003", "Texto"]
                    if equipoR!="CV":
                        if TRef >= 4 and TCong < -14:
                            Texto += lib.loc["REF004", "Texto"]
                            PotAhorro['Accion'] += lib.loc["REFpa04", "Texto"]
                        elif TRef < 4 and TCong >= -14:
                            Texto += lib.loc["REF005", "Texto"]
                            PotAhorro['Accion'] += lib.loc["REFpa05", "Texto"]
                        elif TRef < 4 and TCong < -14:
                            Texto += lib.loc["REF006", "Texto"]
                            PotAhorro['Accion'] += lib.loc["REFpa06", "Texto"]
                    else:
                        if TRef < 12:
                            Texto += lib.loc["CV005", "Texto"]
                            PotAhorro['Accion'] += lib.loc["CVpa05", "Texto"]
                    # Mala ventilacion
                    if "VN" in Claves:
                        if "SV" in Claves:
                            Texto += lib.loc["REF007", "Texto"]
                            PotAhorro['Accion'] += lib.loc["REFpa07", "Texto"]
                        else:
                            Texto += lib.loc["REF009", "Texto"]
                            PotAhorro['Accion'] += lib.loc["REFpa07", "Texto"]
                    if "SU" in Claves:
                        Texto += lib.loc["REF010", "Texto"]
                        PotAhorro['Accion'] += lib.loc["REFpa10", "Texto"]

                if "PR" in Claves:
                    Texto += "<br />" + lib.loc["REF011", "Texto"]
                    if "AI" in Claves:
                        Texto += lib.loc["REF011S02", "Texto"]
                    elif "AD" in Claves:
                        Texto += lib.loc["REF011S03", "Texto"]
                    else:
                        Texto += lib.loc["REF011S01", "Texto"]
                        PotAhorro['Accion'] += lib.loc["REFpa11", "Texto"]
                Texto += lib.loc["REF015", "Texto"]
                PotAhorro['%Ahorro'] = Ns * 0.07
                PotAhorro['kWhAhorrado'] = kWh * PotencialAhorro
            else:
                #### NS rojo ####
                Texto += lib.loc['REF016', 'Texto']
                if (NomCom > 120) and not("CN" in ClavesSep):
                    Texto+= lib.loc["REF017","Texto"]
                elif (NomCom <= 120) and ("CN" in ClavesSep):
                    Texto+= lib.loc["REF018","Texto"]
                elif (NomCom > 120) and ("CN" in ClavesSep):
                    Texto += lib.loc["REF019","Texto"]
                else:
                    Texto = Texto.replace(" La principal causa es que su compresor (motor)","")
                if Nt>0:
                    Texto += lib.loc["REF020","Texto"]
                    if "FG" in Claves:
                        Texto += lib.loc["REF021","Texto"]
                        PotAhorro['%Ahorro'] = 0.50
                        PotAhorro['kWhAhorrado'] = kWh * PotencialAhorro
                        PotAhorro['Accion'] += lib.loc["REFpa21", "Texto"]
                    if "DM" in Claves:
                        Texto += lib.loc["REF022","Texto"]
                        PotAhorro['%Ahorro'] = 0.50
                        PotAhorro['kWhAhorrado'] = kWh * PotencialAhorro
                        PotAhorro['Accion'] += lib.loc["REFpa22", "Texto"]
                    if "EM" in Claves:
                        Texto += lib.loc["REF023","Texto"]
                        PotAhorro['%Ahorro'] = 0.50
                        PotAhorro['kWhAhorrado'] = kWh * PotencialAhorro
                        PotAhorro['Accion'] += lib.loc["REFpa23", "Texto"]
                    if "PD" in Claves:
                        Texto += lib.loc["REF024","Texto"]
                        PotAhorro['%Ahorro'] = 0.50
                        PotAhorro['kWhAhorrado'] = kWh * PotencialAhorro
                        PotAhorro['Accion'] += lib.loc["REFpa24", "Texto"]

                if Nt>1:
                    if equipoR=="RF":
                        Texto += lib.loc["REF025","Texto"] + lib.loc["REF026","Texto"]
                    else:
                        Texto += lib.loc["MB025","Texto"] + lib.loc["REF026","Texto"]
                    PotAhorro['%Ahorro'] = 0.50
                    PotAhorro['kWhAhorrado'] = kWh * PotencialAhorro
                    if equipoR=="RF":
                        PotAhorro['Accion'] += lib.loc["REFpa25", "Texto"]
                    else:
                        PotAhorro['Accion'] += lib.loc["MBpa25", "Texto"]
                    # Mala ventilacion
                    if "VN" in Claves:
                        Texto += lib.loc["REF027", "Texto"]

                elif (Nt == 0) and ("CN" in ClavesSep):
                    Texto += lib.loc["REF028","Texto"] + lib.loc["REF029","Texto"]
                    PotAhorro['%Ahorro'] = 0.50
                    PotAhorro['kWhAhorrado'] = kWh * PotencialAhorro
                    PotAhorro['Accion'] += lib.loc["REFpa29", "Texto"]
                elif (Nt == 0) and (EncendidoNs<0.53) and ((equipoR=="RF")or(equipoR=="MB")):
                    Texto += lib.loc["REF030","Texto"]
                elif (Nt == 0) and (EncendidoNs<0.40) and (equipoR=="CN"):
                    Texto += lib.loc["REF030","Texto"]
                elif (Nt == 0) and (EncendidoNs<0.60) and (equipoR=="CV"):
                    Texto += lib.loc["REF030","Texto"]
                if TempCom > 50:
                    Texto += lib.loc["REF031","Texto"] + lib.loc["REF032","Texto"]

        else:
        ########## Escenario amarillo ##########
            Texto += lib.loc['REF002','Texto']
            # Temperaturas muy bajas
            if Ns>0:
                Texto += lib.loc["REF003","Texto"]
                if equipoR != "CV":
                    if TRef >= 4 and TCong < -14:
                        Texto += lib.loc["REF004", "Texto"]
                        PotAhorro['Accion'] += lib.loc["REFpa04", "Texto"]
                    elif TRef < 4 and TCong >= -14:
                        Texto += lib.loc["REF005", "Texto"]
                        PotAhorro['Accion'] += lib.loc["REFpa05", "Texto"]
                    elif TRef < 4 and TCong < -14:
                        Texto += lib.loc["REF006", "Texto"]
                        PotAhorro['Accion'] += lib.loc["REFpa06", "Texto"]
                else:
                    if TRef < 12:
                        Texto += lib.loc["CV005", "Texto"]
                        PotAhorro['Accion'] += lib.loc["CVpa05", "Texto"]
                # Mala ventilacion
                if "VN" in Claves:
                    if "SV" in Claves:
                        Texto += lib.loc["REF007", "Texto"]
                        PotAhorro['Accion'] += lib.loc["REFpa07", "Texto"]
                    else:
                        Texto += lib.loc["REF009", "Texto"]
                        PotAhorro['Accion'] += lib.loc["REFpa07", "Texto"]
                if "SU" in Claves:
                    Texto += lib.loc["REF010", "Texto"]
                    PotAhorro['Accion'] += lib.loc["REFpa10", "Texto"]

            if "PR" in Claves:
                Texto += "<br />" + lib.loc["REF011","Texto"]
                if   "AI" in Claves:
                    Texto += lib.loc["REF011S02","Texto"]
                elif "AD" in Claves:
                    Texto += lib.loc["REF011S03","Texto"]
                else:
                    Texto += lib.loc["REF011S01","Texto"]
                    PotAhorro['Accion'] += lib.loc["REFpa11", "Texto"]
            Texto += lib.loc["REF015","Texto"]
            PotAhorro['%Ahorro'] = Ns*0.07
            PotAhorro['kWhAhorrado'] = kWh * PotencialAhorro

    if equipoR == "MB":
        Texto = Texto.replace("Refrigerador","Minibar").replace("refrigerador","minibar")
        PotAhorro.loc[0,"Accion"] = PotAhorro.at[0,"Accion"].replace("Refrigerador","Minibar").replace("refrigerador","minibar")
    if equipoR == "CN":
        Texto = Texto.replace("Refrigerador", "Congelador").replace("refrigerador", "congelador")
        PotAhorro.loc[0,"Accion"] = PotAhorro.at[0,"Accion"].replace("Refrigerador", "Congelador").replace("refrigerador", "congelador")
    if equipoR == "CV":
        Texto = Texto.replace("Refrigerador", "Equipo").replace("refrigerador", "equipo")
        PotAhorro.loc[0, "Accion"] = PotAhorro.at[0, "Accion"].replace("Refrigerador", "Equipo").replace("refrigerador", "equipo")
        #print(PotAhorro.at[0,"Accion"])
    Texto = Texto.replace("/n*", "<br />- ")
    Texto = Texto.replace("\\n*", "<br />- ")
    linkBlog = links.loc["[link]","link"]
    linkGuia = links.loc["[link guia de refrigeradores]","link"]
    Texto = Texto.replace("[link]",fc.ligarTextolink("link",linkBlog))
    Texto = Texto.replace("[link guia de refrigeradores]",fc.ligarTextolink("(Guia de compra)",linkGuia))
    #print("percentil original Refris: ",percentil)
    #print("percentil Ns Refris: ",percentilNs)
    #print(Texto)

    #print("Porcencial de ahorro############# ",PotAhorro.at[0,"Accion"])
    return Texto,TextoF,PotAhorro