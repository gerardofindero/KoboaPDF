import pandas as pd
import funcionesComunes as fc
def leerLibreria():
    # try:
    #     lib = pd.read_excel(
    #         f"../../../Recomendaciones de eficiencia energetica/Librerias/Maquinas de hielo/libreriaHielo.xlsx",
    #         sheet_name='libreriaHielo')
    #     links = pd.read_excel(
    #         f"../../../Recomendaciones de eficiencia energetica/Librerias/Maquinas de hielo/libreriaHielo.xlsx",
    #         sheet_name='links')
    #except:

    lib = pd.read_excel(
        f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Dispensadores de agua/libreriaDispensadores.xlsx",
        sheet_name='libreriaDispensadores')

    links = pd.read_excel(
        f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Dispensadores de agua/libreriaDispensadores.xlsx",
        sheet_name='links')

    return lib, links
def recoDispensadores(kwh):
    PotAhorro = pd.DataFrame(index=[0],columns=["%Ahorro","kwhAhorrado","Accion"])
    lib, links = leerLibreria()
    if kwh<=20:
        txt = fc.selecTxt(lib, "DIS01")
    else:
        txt = fc.selecTxt(lib,"DIS02").replace("[TIMER INTELIGENTE]",fc.ligarTextolink("Link de compra",links.at[0,"Link"]))
        PotAhorro["%Ahorro"]     = 0.30
        PotAhorro["kwhAhorrado"] = kwh*0.30
        PotAhorro["Accion"]      = fc.selecTxt(lib,"DISpa01").replace("[TIMER INTELIGENTE]",fc.ligarTextolink("Link de compra",links.at[0,"Link"]))
    txt = txt.replace('[/n]','<br />')
    return [txt, PotAhorro]
