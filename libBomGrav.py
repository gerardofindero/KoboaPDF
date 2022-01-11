# K = Kaccesorios + Ktuberia
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import funcionesComunes as fc

def leerLibreria():
    kc90 = 1  # factor de resisencia de codo de 90°
    g    = 9.8  # metros por segundo
    try:
        cur = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/curBom.xlsx")
        dbB = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/Base de datos de bombas gravitacionales.xlsx",
            sheet_name='Base de datos')
        lib = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='libreriaBombas')
    except:
        cur = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/curBom.xlsx")
        dbB = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/Base de datos de bombas gravitacionales.xlsx",
            sheet_name='Base de datos')
        lib = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='libreriaBombas')

    dbB = dbB.loc[:11,:].reset_index(drop=True).copy()
    cur = cur.iloc[:,:13].reset_index(drop=True).copy()
    #print(dbB.Modelo)
    #print(cur.columns)
    return [kc90,g,cur,dbB,lib]

def armarTxt(kwh,hrsUso,Claves):
    """

    Parameters
    ----------
    kwh:    kwh al bimestre
    hrsUso: horas de uso a la semana
    Claves:
    w           watts(numerico)
    encender    plomeria_gravitacional_encender_c_i          (string              ) valores: si, no
    acceso      plomeria_gravitacional_acceso_c_i            (string              ) valores: si, no
    accesoB     plomeria_gravitacional_accesobomba_c_i       (string              ) valores: si, no

    termografia plomeria_gravitacional_termografia_c_i       (string              ) valores: ninguno, bobina, rodamiento, general
    sarro       plomeria_gravitacional_sarro_c_i             (string              ) valores: si, no
    dureza      plomeria_gravitacional_dureza_c_i            (string              ) valores: bajo, alto
    valvulas    plomeria_gravitacional_valvulas_abiertas_c_i (string              ) valores: abiertas, cerradas

    fugasTer    plomeria_gravitacional_fugasTer_c_i          (string              ) valores: si, no
    fugasSup    plomeria_gravitacional_fugasSup_c_i          (string              ) valores: si, no
    fugasTXT    plomeria_gravitacional_fugasTXT_c_i          (string-texto libre  )

    control     plomeria_gravitacional_control_c_i           (string              ) valores: flotador, electronivel, anillo, ninguno
    cierra      plomeria_gravitacional_control_cierra_c_i    (string              ) valores: si, no
    pegados     plomeria_gravitacional_control_pegados_c_i   (string              ) valores: si, no
    contrapeso  plomeria_gravitacional_control_contrapeso_c_i(string              ) valores: si, no
    problemas   plomeria_gravitacional_control_problemas_c_i (string-texto libre  )

    diametro    plomeria_gravitacional_diametro_c_i          (numerico            )
    longitud    plomeria_gravitacional_longitud_c_i          (numerico            )
    altura      plomeria_gravitacional_delta_c_i             (numerico            )
    nCodos      plomeria_gravitacional_codos_c_i             (nuemrico            )
    temperatura plomeria_gravitacional_temperatura_c_i       (numerico            )
    flujo       plomeria_gravitacional_flujo_segundos_c_i    (nuemrico            )
    material    plomeria_gravitacional_material_c_i          (string              ) valores: plastica, aluminio, hierro

    Returns [Consejos,PotAhorro]
    -------
    """
    txt=''
    PotAhorro = pd.DataFrame(index=[0], columns=["%Ahorro", "kwhAhorrado", "Accion"])
    # abirir archivos base y constantes
    kc90, g, cur, dbB, lib = leerLibreria()
    # split claves, estan en el mismo orden de la documentacion
    Claves=Claves.replace(" ","")
    [w, encender,acceso,accesoB,termografia,sarro,dureza,valvulas,fugasTer,fugasSup,fugasTXT,control,cierra,pegados,contrapeso,problemas,diametro,longitud,altura,nCodos,temperatura,flujo,material]= Claves.split(",")
# Claves = "745,si,si,si,ninguno,si,alto,abiertas,no,no,figasTXT, flotador,no,si,no,problemas,0.75,5,3,5,21,10,plastica"
    # conversion a nuemrico
    w           = float(w)
    diametro    = float(diametro)
    longitud    = float(longitud)
    altura      = float(altura)
    nCodos      = float(nCodos)
    temperatura = float(temperatura)
    flujo       = float(flujo)

    # Se agrega texto y se hacen operaciones acorde al kwh obtenido
    # Linea de apertura
    if kwh<=22.0:
        txt = txt + fc.selecTxt(lib,"BOM01")
    elif 22<kwh<=60:
        txt = txt + fc.selecTxt(lib,"BOM02")
    else:
        txt = txt + fc.selecTxt(lib,"BOM03")
    # Información de la potencia
    txt = txt + " " + fc.selecTxt(lib,"BOM04").replace("[w]",str(w))

    if termografia!="":
        if termografia   == "bobina":
            txt = txt + " " + fc.selecTxt(lib,"BOM05")
        elif termografia == "rodamiento":
            txt = txt + " " + fc.selecTxt(lib, "BOM06")
        elif termografia == "general":
            txt = txt + " " + fc.selecTxt(lib, "BOM07")

    if sarro == "si":
        txt = txt + " " + fc.selecTxt(lib, "BOM08")
    if dureza == "alto":
        txt = txt + " " + fc.selecTxt(lib, "BOM09")
    if (sarro == "si") or (dureza == "alto"):
        txt = txt + " " + fc.selecTxt(lib, "BOM10")

    if valvulas == "cerradas":
        txt = txt + " " + fc.selecTxt(lib,"BOM11")

    if fugasSup == "si":
        txt = txt + " " + fc.selecTxt(lib, "BOM12")
    if fugasTer == "si":
        txt = txt + " " + fc.selecTxt(lib, "BOM13")
    if ((fugasSup == "si") or (fugasTer == "si")) and (len(fugasTXT.replace(" ",""))!=0):
            fugasTXT = fugasTXT.lower()
            txt = txt + "<br />" + fc.selecTxt(lib, "BOM14").replace("[fugas_txt]", fugasTXT) + "<br />"

    if control != "":
        if control == "ninguno":
            txt = txt + " " + fc.selecTxt(lib, "BOM15")
        if (control == "flotador"    ) and (cierra=="no"      ):
            txt = txt + " " + fc.selecTxt(lib, "BOM16")
        if (control == "electronivel") and (pegados=="si"     ):
            txt = txt + " " + fc.selecTxt(lib, "BOM17")
        if (control == "anillo"      ) and (contrapeso == "no"):
            txt = txt + " " + fc.selecTxt(lib, "BOM18")
        if len(problemas.replace(" ",""))!=0:
            problemas = problemas.lower()
            txt = txt + " " + fc.selecTxt(lib,"BOM19").replace("[problemas]",problemas)
    if kwh > 60:
        # w
        # longitud debe estar en metros
        # altura   debe estar en metros
        # nCodos   debe ser un entero
        # temperatura debe estar en °C
        flujo    = 1/flujo                          # incialmente flujo tiene cuantos segundo toma llenar un litro: Flujo (L/s) = 1L/ #segundos
        Q        = flujo * 60                       # caudal en litros por minuto
        diametro = diametro / 39.3701               # conversión de pulgadas a metros
        Qc       = flujo    * 0.001                 # conversión de L/s a m3/s
        Qp       = np.linspace(1, 200, 200)/1000/60 # Qp (Q de prueba)=>litros/min (1m3/1000L)(1min/60s)  -> m3/s
        df       = pd.DataFrame({'Qp(m3/s)': Qp})   # data frame con eje de flujo en m3/s         } esto es para tener la curva de flujo cabezal
        df['Hp'] = 0                                # inicialización de cabezal a distintos flujo } esto es para tener la curva de flujo cabezal

        for i in range(200):
            df.loc[i,'Hp']=estH(Z=altura,Q=df.at[i,'Qp(m3/s)'],L=longitud,D=diametro,nC90=nCodos,material=material,T=temperatura)
        cur['Hp'] = df.loc[:, 'Hp']
        dbB['Qp'] = 0
        dbB['Hp'] = 0
######### descomentar para revizar graficas y ver el punto de operacion con cada bomba######################################
        # demo=cur.set_index(['Q(L/min)'],drop=True,inplace=False)
        # demo.plot()                                                                   # curvas de operación de las bombas
        # plt.stem([Q],[estH(altura,Qc,longitud,diametro,nCodos,material,temperatura)]) # punto de operación de la casa
        # plt.show()
############################################################################################################################
        ms = cur.columns[1:-2]
        for m in ms:
            idx = (cur.loc[:, m] - cur.loc[:, 'Hp']).abs().idxmin()
            dbB.loc[dbB.index[dbB.Modelo == m][0], 'Qp'] = cur.at[idx, 'Q(L/min)']
            dbB.loc[dbB.index[dbB.Modelo == m][0], 'Hp'] = cur.at[idx, 'Hp']

        tc = 1000 / Q
        kwhc = w * tc / 60 / 1000
        dbB['t'] = 1000 / dbB.Qp
        dbB['kwh'] = dbB.loc[:, 'Potencia (HP)'] * dbB.loc[:, 't'] * 0.7457 / 60
        dbB['%ahorro'] = 1 - (dbB.kwh / kwhc)
        selector        = (dbB.loc[:, "Hp"] > dbB.loc[:, "Hmin"]) & (dbB.loc[:, "Hp"] < dbB.loc[:, "Hmax"])
        dbB["HinRange"] = (dbB.loc[:, "Hp"] > dbB.loc[:, "Hmin"]) & (dbB.loc[:, "Hp"] < dbB.loc[:, "Hmax"])
        print(dbB.loc[:, ['Modelo', 'Hmin', 'Hmax', 'Qp', 'Hp', 't', 'kwh', '%ahorro',"HinRange"]])
        print("tiempo que tarda en llenar 1000 la bomba de la casa: ",tc,"\nkwh para llenar impulsar 1000L: ",kwhc)
        idxMaxAhorro = dbB.loc[selector,"%ahorro"].idxmax()
        print(idxMaxAhorro)
        if dbB.at[idxMaxAhorro,"%ahorro"]>0:
            ahorro        = round(dbB.at[idxMaxAhorro,"%ahorro"]*100,2)
            recomendacion = "Bomba de la marca "+ dbB.at[idxMaxAhorro,"Marca"]+" modelo "+ dbB.at[idxMaxAhorro,"Modelo"]
            txt = txt + "\n"+fc.selecTxt(lib,"BOM20")
            txt = txt.replace("[ahorro]",str(ahorro))
            txt = txt.replace("[recomendacion]",recomendacion)

########################### potencial de ahorro #######################################################################
    medidas=""
    if termografia!="":
        medidas = medidas + "\n- Mantenimeinto de la bomba (cebado, capacitor, bobinas y rodamiento)"
    if (sarro == "si") or (dureza=="alto"):
        medidas = medidas + "\n- Liempeiza de y destapado de tuberías"
    if valvulas == "":
        medidas = medidas + "\n- Mantener las valvulas de paso abiertas"
    if (fugasTer == "si") or (fugasSup== "si"):
        medidas = medidas + "\n- Reparar las fugas existentes"
    if control != "":
        if cierra == "no":
            medidas = medidas +"\n- Cambiar el empaque de la valvula"
        if pegados == "si":
            medidas == medidas +"\n- Adecuar electroniveles para evitar que hagan corto"
        if contrapeso == "no":
            medidas = medidas + "\n- Conseguir el contrapeso para el electronivel"
        if control == "ninguno":
            medidas = medidas + "\n- Instalar un electronivel para regular los siclos de encendido"
    try:
        ahorro
    except:
        print("no hubo bomba viable")
    else:
        medidas = medidas +"\n- Cambiando por la bomba de la amrca"+ dbB.at[idxMaxAhorro,"Marca"]+" modelo "+ dbB.at[idxMaxAhorro,"Modelo"]
    if medidas != "":
        PotAhorro.loc[0,"%Ahorro"]     = 1-((w*60/1000)/kwh)
        PotAhorro.loc[0,"kwhAhorrado"] = PotAhorro.at[0,"%Ahorro"] * kwh
        PotAhorro.loc[0,"Accion"]      = fc.selecTxt(lib,"BOMpa01").replace("[%ahorro]",str(PotAhorro.at[0,"%Ahorro"])).replace("[medidas]",medidas)
    #print(PotAhorro)
    return [txt,PotAhorro]

"""
txt = txt + " " + fc.selecTxt(lib, "BOM")
flotador, electronivel, anillo, ninguno
"""
def estH(Z,Q,L,D,nC90,material,T):
    """
    Estimación de cabezal en funcion de ...
    :param Z: Cabezal estatico en metros
    :param Q: Caudal  en m3/s
    :param L: longitud Tuberia en m
    :param D: Diamestro interno de la tuberia en m
    :param nC90: numero de codos
    :param T:  temperatura en °C
    :param material:   material de tuberia
    :return: H :cabezal en metros
    """
    g      = 9.8        # gravedad         - m/s
    A      = est_A(D)   # Área interna     - m2
    v      = est_v(Q,A) # velocidad        - m/s
    Ka     = est_Ka(nC90,D) # adimencional número de codos por resistencia de codos
    vis    = est_vis(T)
    km     = est_km(material)
    f      = est_f(v,D,vis,km)
    Kt     =est_Kt(f,L,D)
    K      = Ka + Kt    # adimencionales
    Hd     = K * (v**2)/2/g
    H      = Z + Hd
    return H

def est_v(Q,A):
    # Q en m3/sec
    # A en m2
    # v en m/sec
    v=Q/A
    return v
def est_A(D):
    # D en me
    # A en m2
    A = np.pi*(D**2)/4
    return A
def est_Ka(nC90,D):
    D = D*100
    try:
        dbka = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='Kaccesorio')
    except:
        dbka = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='Kaccesorio')
    Ka_indx = (dbka.loc[:, 'diametro interno cm min'] - D).abs().idxmin()
    kC90 = dbka.at[Ka_indx, 'K']
    #print(kC90)
    return nC90*kC90
def est_vis(T):
    try:
        dbpa = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='porpAgua')
    except:
        dbpa = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='propAgua')
    dif = dbpa.loc[:, 'Temp. [°C]'] - T
    vis = dbpa.at[dif.abs().idxmin(), 'Kin. Viscosity [mm²/s]'] / 1.0E+6  # viscocidad del agua en funcion de la temperatura
    return vis

def est_km(material):
    try:
        dbkm = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='Kmaterial')
    except:
        dbkm = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Bombas agua/libreriaBombas.xlsx",
            sheet_name='Kmaterial')
    Km_indx = dbkm.index[dbkm.Superficie.str.contains(material)][0]
    km = dbkm.at[Km_indx, 'max K (10^-3)m'] * 1E-3
    return km

def est_f(v,D,vis,km):
    Re = v*D/vis      # velocidad por diametro entre viscocidad (en funcion de la temperatura)
    num=0.25          # numerado de la funcion para calcular el coeficiente de friccion
    den=(km/3.7/D)+(5.74/(Re**0.9)) # denominado km: factor k del material D: diametro de la tuberia
    den=np.log10(den)**2
    f = num/den
    return f

def est_Kt(f,L,D):
    return f*L/D
