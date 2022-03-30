import pandas as pd
import numpy as np

def leerLibreriaBA():
    try:
        lib = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Albercas/libreriaAlbercas.xlsx",
            sheet_name='libreriaAlberca')
        flujo = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Albercas/libreriaAlbercas.xlsx",
            sheet_name='flujo')

    except:
        lib = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Albercas/libreriaAlbercas.xlsx",
            sheet_name='libreriaAlberca')
        flujo = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Albercas/libreriaAlbercas.xlsx",
            sheet_name='flujo')

    lib = lib.set_index("Codigo")
    return [lib, flujo]

def crearClavesBA(infoEq):
    """
    Función para crear las claves de bombas de alberca
    :param infoEq: Data frame con la información de kobo
    :return: Claves = "/kwh al bimestre/Potencia de la bomba/volumen de la alberca/,....
             Tipo de uso              -> comercial (CO) y residencial (RE)
             Calentador de agua solar -> Con solar (CS) y Sin solar (SS)
    """
    Codigo = ""
    if np.isnan(infoEq["Gasto"])  : Codigo += "/0"
    else                          : Codigo += "/" + str(infoEq["Gasto"  ])
    if np.isnan(infoEq["Nominal"]): Codigo += "/0"
    else                          : Codigo += "/" + str(infoEq["Nominal"])
    if np.isnan(infoEq["Volumen"]): Codigo += "/0"
    else                          : Codigo += "/" + str(infoEq["Volumen"])
    if "si" in infoEq["TipoUso"]  : Codigo += ",CO" # Uso Comercial
    else                          : Codigo += ",RE" # Uso residencial, Default si no se especifica
    if "si" in infoEq["Solar"]    : Codigo += ",CS"
    else                          : Codigo += ",SS"
    return Codigo

def recoBA(Claves,kWh,hrsUso,W):
    """
    Función para crear recomendaciones para bombas de alberca.
    Se realiza con los datos capturados en kobo para que la descición tomada en kobo y en la recomendación sea la misma.
    La recomendación  esta en función del número de veces que se recircula el agua (acorde al tipo de uso Residencial o comercial)
    :param Claves: Estructura de las claves Claves de equipo (BA),kwh consumido al bimestre/potencia de la bomba/Volumen de la alberca/,otras claves
                    Tipo de uso              -> comercial (CO) y residencial (RE)
                    Calentador de agua solar -> Con solar (CS) y Sin solar (SS)
    :param kWh   : consumo bimestral de la bomba
    :param hrsUso: número de horas que estuvo prendida la bomba durante la semana
    :param W     : Potencia de la bomba
    :return      : Recomendación
    """
    print("recoBA")
    lib, f =leerLibreriaBA()
    f.loc[:,"Potencia"]   = f.loc[:,"Potencia"].astype(float)

    txt = ""
    # Claves generadas a partir de kobo
    ClavesS=Claves.split(",")
    print("Clave completa:",ClavesS)
    print("Clave[1]",ClavesS[1])
    kwhc, wc, Vc = ClavesS[1].split("/")
    kwhc = float(kwhc)
    wc   = float(wc)
    Vc   = float(Vc)

    if wc!=0:
        f.loc[:, "Diferencia"] = ((f.loc[:, "Potencia"] * 735.5) - wc).abs() # Comparación de potencia
        flujo = f.at[f.loc[:,"Diferencia"].idxmin(),"Flujo(m3/h)"]           # flujo aproximado de la bomba
    else:
        f.loc[:, "Diferencia"] = ((f.loc[:, "Potencia"] * 735.5) - W).abs()  # Comparación de potencia
        flujo = f.at[f.loc[:, "Diferencia"].idxmin(), "Flujo(m3/h)"]  # flujo aproximado de la bomba
    print("flujo",flujo)
    # La n es el número de veces que debe recircular el algua de la alberca acorde al tipo de uso que se le da
    # Para uso comercial debe recircular 9 veces y 2 para us residencial
    if "CO" in Claves:
        n = 9
        #print("CO -> n = 9")
    else:
        n = 2
        #print("RE -> n = 2")
    # Vc es el volumen de la alberca
    if Vc != 0:
        # Tiempo en horas para recircular el agua n veces
        tq = Vc * n / flujo  # horas al día para recircular el agua n veces, acorde al tipo de uso
    else:
    # Si el volumen de la alberca es de -1 queire decir que no se midio
        tq = -1

    if kwhc != 0 and wc != 0:
        # Tiempo en horas que funciona la bomba al día
        tw = kwhc * 1000 / wc / 60 # número de horas al día que funciona la bomba (ver Kobo->Caritas)
    else:
        if hrsUso>0:
            tw = hrsUso/7
        else:
            tw = -1
    tq = int(round(tq))
    tw = int(round(tw))

    # print("tw: ",tw, "tq: ",tq)
    # Si que funciona la bomba es menor al tiempoe stimado recirculación del agua quiere decir que se da un buen uso
    # En caso contrario (dependiendo de si tiene calentador solar) se
    if (tw > 0) and (tq > 0):
        if tw <= tq:
            txt += lib.at["PIS01","Texto"]
        elif (tw > tq) and ("CS" in Claves):
            txt += lib.at["PIS03","Texto"]
        elif (tw > tq) and ("SS" in Claves):
            txt += lib.at["PIS02","Texto"]

    else:
        print("En bombas de alberca")
        print("Claves BA,kWh/W/V,(SS-CS o CO-RE): ",Claves)
        print("hrsUso: ",hrsUso)
        print("kwh: ", kWh)
        print("W: " , W)
    txt = txt.replace("\n","<br />")
    txt = txt.replace("X",str(tw)).replace("Y",str(tq))

    return txt

