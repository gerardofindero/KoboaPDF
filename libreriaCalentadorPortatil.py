import pandas as pd
import funcionesComunes as fc
def leerLibreriaCP():
    try:
        lib = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/calentadorPortatil/libreriaCalentadorPortatil.xlsx",
            sheet_name='libreria')
        links = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/calentadorPortatil/libreriaCalentadorPortatil.xlsx",
            sheet_name='links')

    except:
        lib = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/calentadorPortatil/libreriaCalentadorPortatil.xlsx",
            sheet_name='libreria')
        links = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/calentadorPortatil/libreriaCalentadorPortatil.xlsx",
            sheet_name='links')

    lib = lib.set_index("Codigo")
    links = links.set_index("Variable")
    return [lib, links]
def recoCP(kWh):
    lib, links= leerLibreriaCP()
    txt = ""
    if kWh<=27:
        txt = lib.at["CP01","Texto"]
    elif 27<kWh<=68:
        txt = lib.at["CP02","Texto"]
    elif 68<kWh:
        txt = lib.at["CP03","Texto"]
    txt = txt.replace("\n","<br />")
    linkTermostato = links.at["[linkTermostato]","Links"]
    txt = txt.replace("[linkTermostato]",fc.ligarTextolink("Termostato",linkTermostato))
    return txt
