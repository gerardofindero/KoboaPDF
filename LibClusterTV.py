import pandas as pd
import funcionesComunes as fc
def leerExcel():
    try:
        lib = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
            sheet_name='libreriaCTV')
        links = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
            sheet_name='links')
        variables = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
            sheet_name='variables')
    except:
        lib = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
            sheet_name='libreriaCTV')
        links = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
            sheet_name='links')
        variables = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
            sheet_name='variables')
    return [lib,links,variables]
def recoCTV(standby,DAC):
    """
    Parameters
    ----------
    standby: standby de dispositivos en el cluster de TV
    DAC

    Returns
    [consejo,df con potencial de ahorro]
    -------

    """
    lib,links,variables = leerExcel()
    txt=''
    if standby < 2:
        txt = txt +fc.selecTxt(lib,"CTV01")
    else:
        kwhAhorrado=(standby*24*60/1000)*0.33
        ahorroBimestral = kwhAhorrado*DAC
        ROI             = 250/ahorroBimestral/6
        if ROI <= 3:
            txt = txt+fc.selecTxt(lib,"CTV02")
        else:
            txt = txt+fc.selecTxt(lib,"CTV03")
    """
    if 'decodificador' in listaDispositivos:
        txt = txt+' El decodificador puede mantenerse apagado y prenderse el domingo en la madrugada para actualizarse. <br />'
    if 'consola' or 'nintendo' in listaDispositivos:
        txt = txt+' Lo mejor es mantener completamente apagada la consola, muchas veces se queda en modo espera. <br />'
    
    txt=txt.replace("[recomendacion]",fc.ligarTextolink("Timer inteligente",links.iat[0,2]))
    if len(listaDispositivos)>1:
        txt = txt.replace('{el/los}','los').replace("{s}",'s').replace("{n}","n")
    else:
        txt = txt.replace('{el/los}', 'el').replace("{s}", '').replace("{n}", "")
    """
    PotAhorro = pd.DataFrame(index=[0], columns=["%Ahorro", "kwhAhorrado", "Accion"])

    if "timer" in txt:
        PotAhorro.loc[0,'%Ahorro']   = 0.33
        PotAhorro.loc[0,"kwhAhorro"] = ahorroBimestral
        PotAhorro.loc[0,'Acción']    = fc.selecTxt(lib,"CTVpa01").replace("[timer]",fc.ligarTextolink("Timer inteligente",links.iat[0,2]))
    return [txt, PotAhorro]