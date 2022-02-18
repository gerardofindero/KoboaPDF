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
    print("recoBA")
    lib, f =leerLibreriaBA()
    f.loc[:,"Potencia"]   = f.loc[:,"Potencia"].astype(float)

    txt = ""
    ClavesS=Claves.split(",")

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

    if "CO" in Claves:
        n = 9
        print("CO -> n = 8")
    else:
        n = 2
        print("RE -> n = 2")

    if Vc != 0:
        tq = Vc * n / flujo  # horas al día para recircular el agua n veces, acorde al tipo de uso
    else:
        tq = -1

    if kwhc != 0 and wc != 0:
        tw = kwhc * 1000 / wc / 60 # número de horas al día que funciona la bomba (ver Kobo->Caritas)
    else:
        if hrsUso>0:
            tw = hrsUso/7
        else:
            tw = -1
    tq = int(round(tq))
    tw = int(round(tw))

    print("tw: ",tw, "tq: ",tq)
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

