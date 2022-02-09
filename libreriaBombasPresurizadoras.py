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
    lib = lib.set_index("Codigo")
    link = link.set_index("variable")
    return lib, link
#def recoPresu(w, kwh, tinaco, pastilla, pb, pa, ver, val, jar, fug1, fug1l, fug2, fug2l, pru):

def crearClavesBP(infoEq):
    """
    Parameters
    ----------
    tinaco   kobo-> plomeria_tinaco_existencia_c_i          valores(str) si, no
    pastilla kobo-> plomeria_tuberia_pastilla_c_i           valores(str) si, no
    pb       kobo-> plomeria_tuberia_presion_off_pb_c_i     valores(str) bien, insuficiente, nada
    pa       kobo-> plomeria_tuberia_presion_off_pa_c_i     valores(str) bien, insuficiente, nada, no_hay_pa
    ver      kobo-> plomeria_tuberia_valvulas_verificar_c_i valores(str) bien, insuficiente, nada
    val      kobo-> plomeria_tuberia_valvulas_abiertas_c_i  valore(str) abiertas, algo_cerradas
    jar      kobo-> plomeria_tinaco_jarrosdeaire_c_i,       valores(str) bien, valvula, no_hay
    fug1     kobo-> plomeria_tuberia_fuga_c_i               valores(str) si, no
    fug2     kobo-> plomeria_tuberia_inspeccion_c_i         valores(str) si, no
    fug2l    kobo-> plomeria_tuberia_inspeccion_lugar_c_i   valores(str) TEXTO LIBRE
    pru      kobo-> plomeria_tuberia_pruebafugas            valores(str) apaga, prendido, no_se_pudo_ver

    Returns
    -------
    claves
    """
    ClavesBP=""
    #print("infoEq en clavesBP en libreria: \n",infoEq)
    if "si"               in infoEq.loc["TinacoEx"]            : ClavesBP += ",ST"
    else                                                       : ClavesBP += ",NT"
    if "si"               in infoEq.loc["Pastilla"]            : ClavesBP += ",PA"

    if  "insuficiente"    in infoEq.loc["PresionOFF PB"]       : ClavesBP += ",IB"
    elif "nada"           in infoEq.loc["PresionOFF PB"]       : ClavesBP += ",NB"

    if  "insuficiente"    in infoEq.loc["PresionOFF PA"]       : ClavesBP += ",IA"
    elif "nada"           in infoEq.loc["PresionOFF PA"]       : ClavesBP += ",NA"
    elif "no_hay_pa"      in infoEq.loc["PresionOFF PA"]       : ClavesBP += ",SA"

    if  "insuficiente"    in infoEq.loc["Valvulas Verificada"] : ClavesBP += ",IV"
    elif "nada"           in infoEq.loc["Valvulas Verificada"] : ClavesBP += ",NV"

    if   "algo_cerradas"  in infoEq.loc["Valvulas Abiertas"]   : ClavesBP += ",AC"

    if  "valvula"         in infoEq.loc["Jarros"]              : ClavesBP += ",VJ"
    elif "no_hay"         in infoEq.loc["Jarros"]              : ClavesBP += ",NJ"

    if   "si"             in infoEq.loc["Fuga"]                : ClavesBP += ",FG"
    elif "si"             in infoEq.loc["Inspección"]          : ClavesBP += ",FG"

    if  "apaga"           in infoEq.loc["PruebasF"]            : ClavesBP += ",AF"
    elif "prendido"       in infoEq.loc["PruebasF"]            : ClavesBP += ",PF"
    elif "no_se_pudo_ver" in infoEq.loc["PruebasF"]            : ClavesBP += ",NF"

    if "FG" in ClavesBP: ClavesBP+= "-" + infoEq.loc["Inspección Lugar"]
    else: ClavesBP += "-*"

    return ClavesBP

def recoPresu(kwh,potencia,Claves,hrsUso):
    PotAhorro = pd.DataFrame(index=[0], columns=["%Ahorro", "kwhAhorrado", "Accion"])
    PotAhorro.loc[0,"Accion"] =""
    fgTXT = Claves.split("-")[-1]

    lib, link = leerLibreria()
    #print("recoPresu Claves: ",Claves)
    #print("recoPresu kwh: ",kwh)
    txt = ""

    if "NT" in Claves:
        nec = True
    elif "ST" in Claves and (("IA" in Claves) or ("NA" in Claves) or ("IA" in Claves) or ("NA" in Claves) ):
        nec = True
    else:
        nec = False

    if kwh < 40:
        txt += lib.at["PRE001","Texto"]
    elif 40 <= kwh < 80:
        txt += lib.at["PRE002","Texto"]
    elif kwh >= 80:
        txt += lib.at["PRE003","Texto"]

    if 40 <= kwh:
        if "PA" in Claves:
            if not nec:
                txt+= lib.at["PRE004","Texto"]
            else:
                if ("VJ" in Claves) or ("FG" in Claves) or("AC" in Claves) or ("NJ" in Claves):
                    txt += lib.at["PRE005","Testo"]
                    if "AC" in Claves:
                        txt += lib.at["PRE005S01","Texto"]
                        PotAhorro.loc[0, "%Ahorro"] = 0.2
                        PotAhorro.loc[0, "kwhAhorrado"] = PotAhorro.at[0, "%Ahorro"]
                        PotAhorro.loc[0, "Accion"] = lib.at["PRE005S01pa05", "Texto"]
                    if "NC" in Claves:
                        txt += lib.at["PRE005S02","Texto"]
                        PotAhorro.loc[0, "%Ahorro"] = 0.2
                        PotAhorro.loc[0, "kwhAhorrado"] = PotAhorro.at[0, "%Ahorro"]
                        PotAhorro.loc[0, "Accion"] = lib.at["PRE005S02pa05", "Texto"]
                    if "VV" in Claves:
                        txt += lib.at["PRE005S03","Texto"]
                        PotAhorro.loc[0, "%Ahorro"] = 0.2
                        PotAhorro.loc[0, "kwhAhorrado"] = PotAhorro.at[0, "%Ahorro"]
                        PotAhorro.loc[0, "Accion"] = lib.at["PRE005S03pa05", "Texto"]
                    if "FG" in Claves:
                        txt += lib.at ["PRE005s04","Texto"]
                        PotAhorro.loc[0, "%Ahorro"] = 1 - ((30*7)/(hrsUso*60))
                        PotAhorro.loc[0, "kwhAhorrado"] = PotAhorro.at[0, "%Ahorro"]
                        PotAhorro.loc[0, "Accion"] = lib.at["PRE005S04pa05", "Texto"]
                else:
                    if hrsUso <= 7*0.5:
                        txt += lib.at["PRE007","Texto"]
                    else:
                        txt += lib.at["PRE006","Texto"]
                    #["%Ahorro", "kwhAhorrado", "Accion"]
                    PotAhorro.loc[0,"%Ahorro"    ] = 0.5
                    PotAhorro.loc[0,"kwhAhorrado"] = 0.5*kwh
                    PotAhorro.loc[0,"Accion"     ] = lib.at["PRE006pa06","Texto"]
        else:
            txt += lib.at["PRE008","Texto"]
        if "NT" in Claves:
            txt += lib.at["PRE009","Texto"]

    txt = txt.replace("*","<br />- ")
    timer  = fc.ligarTextolink("link a timer",link.at["[timer]","link"])
    bomVar = fc.ligarTextolink("link a bomba",link.at["[bomVar]","link"])
    txt = txt.replace("[timer]",timer)
    txt = txt.replace("[bomVar]",bomVar)
    txt = txt.replace("[hrsUso]",str(round(hrsUso)))
    txt = txt.replace("[w]",str(round(potencia)))
    txt = txt.replace("[fgTXT]",fgTXT)
    print(PotAhorro.loc[0,"Accion"])
    PotAhorro.loc[0,"Accion"] = PotAhorro.at[0,"Accion"].replace("[bomVar]", bomVar)
    return [txt, PotAhorro]
