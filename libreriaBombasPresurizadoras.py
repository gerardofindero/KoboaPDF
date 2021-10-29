import pandas as pd
import funcionesComunes as fc
def leerLibreria():
    try:
        lib= pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas Presurizadoras/libreriaBombPre.xlsx",
            sheet_name='libreria')
        link= pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas Presurizadoras/libreriaBombPre.xlsx",
            sheet_name='link')
    except:
        lib = pd.read_excel(
             f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas Presurizadoras/libreriaBombPre.xlsx",
            sheet_name='libreria')
        link = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas Presurizadoras/libreriaBombPre.xlsx",
            sheet_name='link')
    return lib, link
def recoPresu(w, kwh, tinaco, pastilla, pb, pa, ver, val, jar, fug1, fug1l, fug2, fug2l, pru):
    lib, link = leerLibreria()
    tpro = kwh*1000/w/(24*60)

    txt = ""
    if (tinaco == "si") and (pastilla == "si"):
        txt = txt + prezuNece(txt, lib, pb, pa, ver, val, jar, fug1, fug2, pru, tpro)
    elif (tinaco == "si") and (pastilla == "no"):
        txt = txt + fc.selecTxt(lib, "PRE01")
    elif (tinaco == "no") and (kwh>35):
        txt = txt + fugas(txt, lib, fug1, fug2, pru,tpro)
        txt = txt + fc.selecTxt(lib,"PRE15")

    txt = txt.replace("[fug1l]", fug1l).replace("[fug2l]", fug2l).replace("[timer]",fc.ligarTextolink("timer",link.at[0,"link"])).replace("<br />","")
    if fug1=="no":
        txt = txt + fc.selecTxt(lib, "PRE16")
    if fug2=="no":
        txt = txt + fc.selecTxt(lib, "PRE17")
    return txt


def prezuNece(txt, lib, pb, pa, ver, val, jar, fug1, fug2, pru, tpro):
    if val == "algo_cerradas":
        txt = txt + fc.selecTxt(lib, "PRE02")
    if jar == "valvula":
        txt = txt + fc.selecTxt(lib, "PRE03")
    elif jar == "no_hay":
        txt = txt + fc.selecTxt(lib, "PRE04")
    if ver == "":
        if (pb == "nada") and (pa == "nada"):
            txt = txt + fc.selecTxt(lib, "PRE05") + fugas(txt, lib, fug1, fug2, pru, tpro)  # necesario
        elif (pb == "bien") and (pa == "bien"):
            txt = txt + fc.selecTxt(lib, "PRE07")  # no necesario
        elif (pb == "bien") and (pa == "no_hay_pa"):
            txt = txt + fc.selecTxt(lib, "PRE07")  # no necesario
        else:
            txt = txt + fc.selecTxt(lib, "PRE06")  # timer
    else:
        if ver == "bien":
            txt = txt + fc.selecTxt(lib, "PRE07")  # no necesario
        elif ver == "insuficiente":
            txt = txt + fc.selecTxt(lib, "PRE06")  # timer
        elif ver == "nada":
            txt = txt + fc.selecTxt(lib, "PRE05") + fugas(txt, lib, fug1, fug2, pru, tpro)  # necesario

    return txt


def fugas(txt, lib, fug1, fug2, pru, tpro):
    print(tpro)
    hrsUso = int(tpro*24)
    minUso = int(tpro*24*60)
    if hrsUso>=1:
        txt = txt +fc.selecTxt(lib,"PRE08").replace("[horasUso]",str(hrsUso))
    else:
        txt = txt +fc.selecTxt(lib,"PRE08").replace("[horasUso]",str(minUso)).replace("horas","minutos")
    if tpro > 0.15:
        if fug2 == 'si':
            txt = txt + fc.selecTxt(lib, "PRE11")
        if fug1 == "si":
            txt = txt + fc.selecTxt(lib, "PRE09")
        elif fug1 == "no_info":
            txt = txt + fc.selecTxt(lib, "PRE10")
        if pru == 'apaga':
            txt = txt + fc.selecTxt(lib, "PRE12")
        elif pru == "encendido":
            txt = txt + fc.selecTxt(lib, "PRE13")
        elif pru == "no_se_pudo_ver":
            txt = txt + fc.selecTxt(lib, "PRE14")
    return txt
