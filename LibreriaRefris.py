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
    """
    Función para crear claves de equipos de refrigeración a partir de kobo
    :param EquiposRefri: DataFrame con información de kobo Refrigerador.py
    :return: Claves con el formato  Equipo,Temperatura Refrigeración/Temperatura Congelación/Potencia del compresor/Temperatura del compresor/ Volumen externo/Porcentaje de encendido, otras claves
                    Horientación de congelador: Vertical (CVE) y Horizontal (CHO)
                    Alarma de puertas         : Alarma inexistente (AI) y Alarma dañada (AD)
                    Ventilas                  : Sin ventilas (SV)
                    Tiempo de prendido        : Lapsos de encendio prolongados (PR)
                    Ciclos de deshielo        : Con ciclos de deshielo (DH)
                    Vebtilación               : Sin ventilación (SV)
                    Liempieza del evaporador  : Evaporador sucio (SU)
                    Potencia del compresor    : Potencia mayor a 120 watts (NC)
                    Estado del empaque        : Empaque dañado (EM)
                    Estado del difusor        : Difusor dañado (DM)
                    Estado de las puertas     : Puertas dañadas (PM)
                    Fugas de refrigerante     : Se encontraron fugas de refrigerante (FG)
    """
    EquiposR = EquiposRefri
    for i in EquiposR.index:
        if np.isnan(EquiposR['Temp Refri'])    : TempR = 100
        else                                      : TempR = (EquiposR['Temp Refri'])
        if np.isnan(EquiposR['Temp Conge'])    : TempC = 100
        else                                      : TempC =(EquiposR['Temp Conge'])
        if np.isnan(EquiposR['Pot Compresor']) : NominalComp = 10
        else                                      : NominalComp = int(EquiposR['Pot Compresor'])
        if np.isnan(EquiposR['Temp Compresor']): TempComp = 10
        else                                      : TempComp = float(EquiposR['Temp Compresor'])
        Volumen =int(EquiposR['Volumen'])
        if  np.isnan(EquiposR["Encendido"])    : Encendido = 60
        else                                      : Encendido = float(EquiposR["Encendido"])
        #Codigo=EquiposR['Clave']
        Codigo=""
        Codigo = str(Codigo)+','+str(TempR)+'/'+str(TempC)+'/'+ str(NominalComp) + '/'+str(TempComp) + '/'+str(Volumen)+"/"+str(Encendido)
####### Detalles      #######################################
        # Disposicion congelador
        #if "CN" in Codigo:
        try:
            if   "vertical"   in EquiposR["Disposicion"]: Codigo+=",CVE"
            elif "horizontal" in EquiposR["Disposicion"]: Codigo+=",CHO"
        except:
            Codigo+=""


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
        or ("altapotencia" in str(EquiposR["Prob Refr"])) :Codigo += ",NC"
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
    """
    Función que da la recomendaciones para equipos de refrigeración.
    El color y mensaje se dan acorde al percentil en el que se encuentra el kwh al bimestre
    :param Claves: formato  Equipo,Temperatura Refrigeración/Temperatura Congelación/Potencia del compresor/Temperatura del compresor/ Volumen externo/Porcentaje de encendido, otras claves
                    Horientación de congelador: Vertical (CVE) y Horizontal (CHO)
                    Alarma de puertas         : Alarma inexistente (AI) y Alarma dañada (AD)
                    Ventilas                  : Sin ventilas (SV)
                    Tiempo de prendido        : Lapsos de encendio prolongados (PR)
                    Ciclos de deshielo        : Con ciclos de deshielo (DH)
                    Vebtilación               : Sin ventilación (SV)
                    Liempieza del evaporador  : Evaporador sucio (SU)
                    Potencia del compresor    : Potencia mayor a 120 watts (NC)
                    Estado del empaque        : Empaque dañado (EM)
                    Estado del difusor        : Difusor dañado (DM)
                    Estado de las puertas     : Puertas dañadas (PM)
                    Fugas de refrigerante     : Se encontraron fugas de refrigerante (FG)
    :param notas:   Notas de campo
    :param nombre:  Nombre del refrigerador
    :param consumo: kwh al bimestre del refrigerador
    :return:        Recomendación ->            percentil < 0.30    - carita verde
                                        0.30 <= percentil < 0.90    - carita amrilla Si un equiipo puede reducir su consumo por debajo del percentil 0.90 de vulve amarillo
                                        0.90 <= percentil           - carita roja
    """
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
        # equipoR -> Temperatura Refrigeración/Temperatura Congelación/Potencia del compresor/Temperatura del compresor/ Volumen externo/Porcentaje de encendido
        equipoR=ClavesSep[0]
        Datos= ClavesSep[1].split("/")
        TRef      = float(Datos[0]) # temperatura de refrigeración
        TCong     = float(Datos[1]) # temperatura de congelación
        NomCom    = float(Datos[2]) # Potencia del compresor
        TempCom   = float(Datos[3]) # Temperatura del compresor
        Volumen   = float(Datos[4]) # Volumen externo del congelador
        Encendido = float(Datos[5])/100 # Proporción de encendido del refrigerador con respecto a su ciclo de trabajo
        Ns = 0      # Número de causas suaves
        if equipoR == "CV":
            if (TRef < 12): Ns+=1
        else:
            if (TRef < 4) or (TCong < -14): Ns += 1
        if "VN" in Claves: Ns += 1
        if "SU" in Claves: Ns += 1
        EncendidoNs = Encendido - (0.07 * Ns)

        Nt = 0     # número de causas tecnicas
        if "EM" in Claves: Nt += 1
        if "DM" in Claves: Nt += 1
        if "FG" in Claves: Nt += 1
        if "PD" in Claves: Nt += 1


        # El modelo de percentil relaciona el kwh por el volumen
        # Se escoge el modelo matematico acorde al tipo de equipo
        if (equipoR=='RF') or (equipoR=="MB"):
            # Refrigeradores y minibares
            Volumen = float(Datos[4]) * 0.000022
            percentil = norm.cdf(((float(kWh)*6.0)**0.1 - (1.738365 + 0.0057272 * Volumen))/0.01962684,loc=0,scale=1)
            percentilNs = norm.cdf((((1 - 0.07 * Ns) * float(kWh) * 6.0) ** 0.1 - (1.738365 + 0.0057272 * Volumen)) / 0.01962684, loc=0,scale=1)
        if equipoR=="CV":
            # Cavas
            formulaV = (Volumen / 1300.8) + 21.4
            formulaR = (Volumen / 1300.8) + 51.6
        if equipoR=="CN":
            # Cogelador
            if "CHO" in Claves:
                # Congelador horizontal
                formulaV = (Volumen / 8000.35) - 7.58
                formulaR = (Volumen / 3955.11) - 15.33
            if "CVE" in Claves:
                # Congelador vertical
                formulaV = (Volumen / 6863.63) - 8.83
                formulaR = (Volumen / 3432.19) - 17.67
        if equipoR == "CV" or equipoR == "CN":
            if kWh < formulaV              : percentil = 0.20
            elif formulaV <= kWh < formulaR: percentil = 0.50
            else                           : percentil = 0.95
            if kWh*(1-(Ns*0.07)) < formulaV             : percentilNs = 0.20
            elif formulaV<= kWh*(1-(Ns*0.07)) < formulaR: percentilNs = 0.50
            else                                        : percentilNs = 0.95

        if percentil<0.3:
            #### Zona verde ####
            Texto += lib.loc['REF001','Texto'] + lib.loc["REF015","Texto"]
        elif percentil>=0.90:
            #### Carita amarilla  al quitar el consumo de las causas suaves y tecnicas ####
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
                #### Carita roja  ####
                Texto += lib.loc['REF016', 'Texto']
                if (NomCom > 120) and not("NC" in ClavesSep):
                    Texto+= lib.loc["REF017","Texto"]
                elif (NomCom <= 120) and ("NC" in ClavesSep):
                    Texto+= lib.loc["REF018","Texto"]
                elif (NomCom > 120) and ("NC" in ClavesSep):
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

                elif (Nt == 0) and ("NC" in ClavesSep):
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
        ########## Escenario amarillo sin considerar causas suaves o tecnicas ##########
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
    # Reemplazo de variables depndiendo el tipo de equipo de refrigeración
    if equipoR == "RF":
        # Refrigerador
        Texto = Texto.replace("[TEMPR]",str(int(TRef)))
        Texto = Texto.replace("[TEMPC]",str(int(TCong)))

    if equipoR == "MB":
        # Minibar
        Texto = Texto.replace("[TEMPR]", str(int(TRef)))
        Texto = Texto.replace("[TEMPC]", str(int(TCong)))
        Texto = Texto.replace("[equipo]","minibar")
        Texto = Texto.replace("Refrigerador","Minibar").replace("refrigerador","minibar")
        PotAhorro.loc[0,"Accion"] = PotAhorro.at[0,"Accion"].replace("Refrigerador","Minibar").replace("refrigerador","minibar")
    if equipoR == "CN":
        # Congelador
        Texto = Texto.replace("[TEMPC]",str(int(TCong)))
        Texto = Texto.replace("Refrigerador", "Congelador").replace("refrigerador", "congelador")
        PotAhorro.loc[0,"Accion"] = PotAhorro.at[0,"Accion"].replace("Refrigerador", "Congelador").replace("refrigerador", "congelador")
    if equipoR == "CV":
        # Cavas
        Texto = Texto.replace("[TEMPR]", str(int(TRef)))
        Texto = Texto.replace("Refrigerador", "Equipo").replace("refrigerador", "equipo")
        PotAhorro.loc[0, "Accion"] = PotAhorro.at[0, "Accion"].replace("Refrigerador", "Equipo").replace("refrigerador", "equipo")

    Texto = Texto.replace("/n*", "<br />- ")
    Texto = Texto.replace("\\n*", "<br />- ")
    linkBlog = links.loc["[link]","link"]
    linkGuia = links.loc["[link guia de refrigeradores]","link"]
    Texto = Texto.replace("[link]",fc.ligarTextolink("link",linkBlog))
    Texto = Texto.replace("[link guia de refrigeradores]",fc.ligarTextolink("(Guia de compra)",linkGuia))

    return Texto,TextoF,PotAhorro