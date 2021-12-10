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
#def recoPresu(w, kwh, tinaco, pastilla, pb, pa, ver, val, jar, fug1, fug1l, fug2, fug2l, pru):
def recoPresu(Claves,kwh):
    PotAhorro = pd.DataFrame(index=[0], columns=["%Ahorro", "kwhAhorrado", "Accion"])
    trsh, w, tinaco, pastilla, pb, pa, ver, val, jar, fug1, fug1l, fug2, fug2l, pru = Claves.split(sep=",")
    w= float(w)
    """
    Parameters
    ----------
    w        potencia numerico
    kwh      consumo numerico
    tinaco   kobo-> plomeria_tinaco_existencia_c_i          valores(str) si, no
    pastilla kobo-> plomeria_tuberia_pastilla_c_i           valores(str) si, no
    pb       kobo-> plomeria_tuberia_presion_off_pa_c_i     valores(str) bien, insuficiente, nada
    pa       kobo-> plomeria_tuberia_presion_off_pa_c_i     valores(str) bien, insuficiente, nada, no_hay_pa
    ver      kobo-> plomeria_tuberia_valvulas_verificar_c_i valores(str) bien, insuficiente, nada
    val      kobo-> plomeria_tuberia_valvulas_abiertas_c_i  valore(str) abiertas, algo_cerradas
    jar      kobo-> plomeria_tinaco_jarrosdeaire_c_i,       valores(str) bien, valvula, no_hay
    fug1     kobo-> plomeria_tuberia_fuga_c_i               valores(str) si, no
    fug1l    kobo-> plomeria_tuberia_fuga_lugar_c_i         valores(str) TEXTO LIBRE
    fug2     kobo-> plomeria_tuberia_inspeccion_c_i         valores(str) si, no
    fug2l    kobo-> plomeria_tuberia_inspeccion_lugar_c_i   valores(str) TEXTO LIBRE
    pru      kobo-> plomeria_tuberia_pruebafugas            valores(str) apaga, prendido, no_se_pudo_ver

    Returns
    -------
    texto con recomendacion
    """
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
    # Potencual de ahorro
    PotAhorro["Accion"] = ""
    if ("el caudal de agua es adecuado" in txt):
        PotAhorro["%Ahorro"] = 1
        PotAhorro["kwhAhorrado"] = kwh
        PotAhorro["Accion"] = fc.selecTxt(lib, "PREpa03")
    elif (fug1 == "si") or (fug2=="si"):
        PotAhorro["%Ahorro"]     =  1-(0.5/tpro)
        PotAhorro["kwhAhorrado"] = PotAhorro.at[0,"%Ahorro"]*kwh
        PotAhorro["Accion"]      = fc.selecTxt(lib,"PREpa01")
    elif (tinaco=="no", ):
        PotAhorro["%Ahorro"] = 1
        PotAhorro["kwhAhorrado"] = kwh
        PotAhorro["Accion"] = fc.selecTxt(lib, "PREpa02")
    elif ("[timer]" in txt):
        PotAhorro["%Ahorro"] = 1 - (0.5 / tpro)
        PotAhorro["kwhAhorrado"] = PotAhorro.at[0, "%Ahorro"] * kwh
        PotAhorro["Accion"] = fc.selecTxt(lib, "PREpa04")

    if kwh>35:
        return [txt.replace("\n","<br/>"), PotAhorro]
    else:
        return [fc.selecTxt(lib,"PRE00"),  PotAhorro]


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
    if hrsUso==1:
        txt = txt + fc.selecTxt(lib, "PRE08").replace("[horasUso]", str(hrsUso)).replace("horas","hora")
    elif hrsUso>1:
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
