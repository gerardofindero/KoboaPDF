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
    """
    Recomendación para dispensadores de agua
    :param kwh: consumo de kwh al bimestre del dispensador de agua
    :return:    Recomendación y potencial de ahorro con el timer inteligente
    """
    PotAhorro = pd.DataFrame(index=[0],columns=["%Ahorro","kwhAhorrado","Accion"])
    lib, links = leerLibreria()
    if kwh<=20:
        txt = fc.selecTxt(lib, "DIS01")
    else:
        txt = fc.selecTxt(lib,"DIS02").replace("[TIMER INTELIGENTE]",fc.ligarTextolink("Link de compra",links.at[0,"Link"]))
        # potencial de ahorro del 30% al implementar un timer
        PotAhorro["%Ahorro"]     = 0.30
        PotAhorro["kwhAhorrado"] = kwh*0.30
        PotAhorro["Accion"]      = fc.selecTxt(lib,"DISpa01").replace("[TIMER INTELIGENTE]",fc.ligarTextolink("Link de compra",links.at[0,"Link"]))
    txt = txt.replace('[/n]','<br />')
    txt = txt.replace("[TIMER INTELIGENTE]",fc.ligarTextolink("Link de compra",links.at[0,"Link"]))
    return [txt, PotAhorro]
