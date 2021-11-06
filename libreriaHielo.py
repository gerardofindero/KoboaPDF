import pandas as pd
import funcionesComunes as fc

def leerLibreria():
    try:
        lib = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Maquinas de hielo/libreriaMaquinasHielo.xlsx",
            sheet_name='libreriaHielo')
        links = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Maquinas de hielo/libreriaMaquinasHielo.xlsx",
            sheet_name='links')
    except:
        lib = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Maquinas de hielo/libreriaMaquinasHielo.xlsx",
            sheet_name='libreriaHielo')
        links = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Maquinas de hielo/libreriaMaquinasHielo.xlsx",
            sheet_name='links')
    return lib, links
def recoMaqHie(kwh):
    lib, links = leerLibreria()

    if kwh<=20:
        txt = fc.selecTxt(lib, "HIEL01")
    else:
        txt = fc.selecTxt(lib, "HIEL02").replace("[TIMER INTELIGENTE]",fc.ligarTextolink("Timer inteligente",links.at[0,"Link"]))
    return txt