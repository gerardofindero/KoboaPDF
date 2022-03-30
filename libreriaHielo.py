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
        lib   = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Maquinas de hielo/libreriaMaquinasHielo.xlsx",
            sheet_name='libreriaHielo')
        links = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Maquinas de hielo/libreriaMaquinasHielo.xlsx",
            sheet_name='links')
    return lib, links


def recoMaqHie(kwh):
    """
    Recomendaciones para maquinas de hielo
    :param kwh: Consumo de kwh al bimestre de la maáquina de hielo
    :return:    Recomendación automatica y potencial de ahorro con el timer inteligente
    """
    PotAhorro = pd.DataFrame(index=[0], columns=["%Ahorro", "kwhAhorrado", "Accion"])
    lib, links = leerLibreria()

    if kwh<=20:
        txt = fc.selecTxt(lib, "HIEL01")
    else:
        txt = fc.selecTxt(lib, "HIEL02").replace("[TIMER INTELIGENTE]",fc.ligarTextolink("Link",links.at[0,"Link"]))
        PotAhorro["%Ahorro"] = 0.30
        PotAhorro["kwhAhorrado"] = kwh * 0.30
        PotAhorro["Accion"] = fc.selecTxt(lib, "HIELpa01").replace("[TIMER INTELIGENTE]",fc.ligarTextolink("Link",links.at[0,"Link"]))
    txt = txt.replace('[/n]','<br />')
    return [txt, PotAhorro]