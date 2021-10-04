import pandas as pd
import funcionesComunes as fc
def leerLibreria():
    try:
        lib = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Dispensadores de Agua/libreriaDispensadore.xlsx",
            sheet_name='libreriaDispensadores')
        links = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Dispensadores de Agua/libreriaDispensadore.xlsx",
            sheet_name='links')
    except:
        lib = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Dispensadores de Agua/libreriaDispensadore.xlsx",
            sheet_name='libreriaDispensadores')
        links = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Dispensadores de Agua/libreriaDispensadore.xlsx",
            sheet_name='limks')
    return lib, links
def recoDispensadore(kwh):
    lib, links = leerLibreria()
    if kwh<=20:
        txt = fc.selecTxt(lib, "DIS01")
    else:
        txt = fc.selecTxt(lib,"DIS02")
