import numpy as np
import pandas as pd
import funcionesComunes as fc

def leerLibreria():
    try:
        lib   = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Aires Acondicionados/libreriaAiresAcondicionados.xlsx",
            sheet_name='libreriaAires')
        links = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Aires Acondicionados/libreriaAiresAcondicionados.xlsx",
            sheet_name='links')
        ct    = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Aires Acondicionados/libreriaAiresAcondicionados.xlsx",
            sheet_name='CargaTermica')
        aadb = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Aires Acondicionados/reemplazos.xlsx",
            sheet_name='Reemplazos')
    except:
       lib   = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Aires Acondicionados/libreriaAiresAcondicionados.xlsx",
            sheet_name='libreriaAires')
       links = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Aires Acondicionados/libreriaAiresAcondicionados.xlsx",
            sheet_name='links')
       ct    = pd.read_excel(
           f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Aires Acondicionados/libreriaAiresAcondicionados.xlsx",
           sheet_name='CargaTermica')
       aadb = pd.read_excel(
           f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Aires Acondicionados/reemplazos.xlsx",
           sheet_name='Reemplazos')
    return [lib, links,ct,aadb]


def armarTxt(Claves,kwh,DAC, hrsUso):
    """

    Parameters
    ----------
    consumo
    DAC
    Uso
    Claves
    AA        clave de aire acondicionado
    w         potencia                                  (num) SEER = (BTU/h)/w 12=12000/w -> 12000/18=w=1000 / 1Ton = 12000BTU/h
    zona      aire_zonaTermica_c_i                      (str) VALORES: zona1, zona2, zona3, zona4
    cp        aires_cp_c_i                              (str) codigo postal de prueba 01180 la api d eclima solo permite 5 descargas de last7days por día
    tempp     aires_temperatura_programada_c_i          (num) temperatura ideal es a 24°C
    peli      aires_cuarto_pelicula_c_i                 (str) VALORES: si, no
    pare      aires_cuarto_paredes_c_i                  (str) VALORES: si, no
    radi      aires_condensador_radiacion_c_i           (str) VALORES: si, no
    filt      aires_cuarto_filtraciones_c_i             (str) VALORES: si, no
    filtTxt   aires_cuarto_filtracionesTxt_c_i          (str) Texto libre
    velocidad aires_evaporador_valocidad_c_i            (num)
    alto      aires_evaporador_alto_c_i                 (num)
    largo     aires_evaporador_largo_c_i                (num)
    evaTemp   aires_evaporador_temperatura_c_i          (num)
    habTemp   aires_habitacion_temperatura_c_i          (num)
    largoC    aires_cuarto_largo_c_i                    (num)
    anchoC    aires_cuarto_ancho_c_i                    (num)
    nPerso    aires_personas_c_i                        (num)
    activi    aires_cuarto_actividad_c_i                (str) VALORES: dormir, estudiar, ejercicio, entretenimiento, cocinar
    ilumin    aires_cuarto_iluminacion_c_i              (str) VALORES: incandecente, fluorescente, halogena,led
    fuentes   aires_cuarto_fuentes_calor_c_i            (str) VALORES: television, cocina, luces, ninguno, computo
    evaLim    aires_evaporador_limpieza_c_i             (str) VALORES: si, no
    conLim    aires_condensador_limpieza_c_i            (str) VALORES: si, no
    evaVen    aires_evaporador_ventilador_c_i           (str) VALORES: si, no
    conVen    aires_condensador_ventilador_c_i          (str) VALORES: si, no
    evaVenT   aires_evaporador_ventiladorTxt_c_i        (str) Texto libre
    conVenT   aires_condensador_ventiladorTxt_c_i       (str) Texto libre
    tuberias  aires_condensador_tuberias_c_i            (str) VALORES:combinaciones de -> tuberia_golpes, tuberias_hielo, aislamiento_mal, buen_estado
    fugas     aires_refrigerante_fugas_c_i              (str) VALORES: si, no
    fugasT    aires_refrigerante_fugasTxt_c_i           (str) Texto libre
    tempSuc   aires_condensador_temperatura_succion_c_i (num)
    tempDes   aires_condensador_temperatura_descarga_c_i(num)

    Returns
    -------

    """
    # INICIALIZADO
    PotAhorro = pd.DataFrame(index=[0], columns=["%Ahorro", "kwhAhorrado", "Accion"])
    txt = ""
    lib, links, ct, aadb = leerLibreria()
    #print(Claves)
    AA,w,zona,cp,tempp,peli,pare,radi,filt,filtTxt,velocidad,alto,largo,evaTemp,habTemp,largoC,anchoC,nPerso,activi,ilumin,fuentes,evaLim,conLim,evaVen,conVen,evaVenT,conVenT,tuberias,fugas,fugasT,tempSuc,tempDes = Claves.split("/")
    # adecuación de claves númericas
    try   : w         = float(w)
    except: w = 0
    try   : tempp     = float(tempp)
    except: tempp = 0


    # información clímatica
    wd    = fc.dataClima(cp)
    hrsNe = (wd.feelslike > 24).sum()

    # armado de texto
    if kwh < 70:
        txt+= fc.selecTxt(lib,"AA01")
    elif 70 <= kwh < 120:
        txt+= fc.selecTxt(lib,"AA02")
    elif kwh >= 120:
        txt+= fc.selecTxt(lib,"AA03")

    # if filt=="si" and filtTxt!="":
    #     txt+= " "+fc.selecTxt(lib,"AA04").replace("[filtTxt]",filtTxt)
    #
    # if tempp < 24:
    #     txt+= ' '+fc.selecTxt(lib,"AA05").replace("[tempp]",str(tempp))
    # if hrsUso>hrsNe:
    #     txt+=" "+fc.selecTxt(lib,"AA06")
    # elif (hrsUso<=hrsNe) and (kwh>=70):
    #     txt+=" "+fc.selecTxt(lib,"AA06S1").replace("[hrsUso]",str(round(hrsUso)))
    #
    # if radi=="si":
    #     txt += " "+fc.selecTxt(lib,"AA07")
    #
    # if peli == "no":
    #     link=fc.selecTxt(links,"[nano]")
    #     link=fc.ligarTextolink("Filtro de calor",link)
    #     txt += " "+fc.selecTxt(lib,"AA08").replace("[nano]",link)
    # if pare == "si":
    #     link1=fc.selecTxt(links,"[pintura1]")
    #     link2=fc.selecTxt(links,"[pintura2]")
    #     link1=fc.ligarTextolink("Pintura 1",link1)
    #     link2=fc.ligarTextolink("Pintura 2",link2)
    #     txt+= " "+fc.selecTxt(lib,"AA09").replace("[pintura1]",link1).replace("[pintura2]",link2)

    if kwh>=70:
        # orinalmente era verde esto :V
        if filt=="si" and filtTxt!="":
            txt+= " "+fc.selecTxt(lib,"AA04").replace("[filtTxt]",filtTxt)

        if tempp < 24:
            txt+= ' '+fc.selecTxt(lib,"AA05").replace("[tempp]",str(tempp))
        if hrsUso>hrsNe:
            txt+=" "+fc.selecTxt(lib,"AA06")
        elif (hrsUso<=hrsNe) and (kwh>=70):
            txt+=" "+fc.selecTxt(lib,"AA06S1").replace("[hrsUso]",str(round(hrsUso)))

        if radi=="si":
            txt += " "+fc.selecTxt(lib,"AA07")

        if peli == "no":
            link=fc.selecTxt(links,"[nano]")
            link=fc.ligarTextolink("Filtro de calor",link)
            txt += " "+fc.selecTxt(lib,"AA08").replace("[nano]",link)
        if pare == "si":
            link1=fc.selecTxt(links,"[pintura1]")
            link2=fc.selecTxt(links,"[pintura2]")
            link1=fc.ligarTextolink("Pintura 1",link1)
            link2=fc.ligarTextolink("Pintura 2",link2)
            txt+= " "+fc.selecTxt(lib,"AA09").replace("[pintura1]",link1).replace("[pintura2]",link2)
        # variables sección amarilla
        try   : velocidad = float(velocidad)
        except: velocidad =0
        try   : alto      = float(alto)
        except: alto      = 0
        try   : largo     = float(largo)
        except: largo     = 0
        try   : evaTemp   = float(evaTemp)
        except: evaTemp   = 0
        try   : habTemp   = float(habTemp)
        except: habTemp   = 0
        try   : largoC    = float(largoC)
        except: largoC    = 0
        try   : anchoC    = float(anchoC)
        except: anchoC    = 0
        try   : nPerso    = float(nPerso)
        except: nPerso    = 0
        # cambio de sección
        txt+="<br />"

        # BTU
        """
        calEspAire = 1.012                                          # J/gk
        denAire    = 1.20                                           # kg/m**3
        flujo      = velocidad*alto*largo*(1/10000)*3600*1.20*(1000) # g/h
        deltaT     = abs(habTemp-evaTemp)                  # Delta en °C / °K
        jules_g    = calEspAire*deltaT                              # jules/gramo
        julesT     = flujo*jules_g                                  # jules/hora
        btu        = julesT/1055.06                                 # btu/h
        """
        btu       = velocidad*alto*largo*abs(habTemp-evaTemp)*0.41 # btu/h
        seerS     = btu/w                                          # SEER in situ
        toneladas = btu/12000
        p         = toneladas//0.5
        r         = toneladas%0.5

        if round(r/0.5)>0:
            p+=1
        toneladas=p*0.5
        #print("BTU/Hr: ",btu)
        #print("Toneladas",toneladas)
        #print("SEER in Situ: ",seerS)
        # estimacion de carga termica
        area = anchoC*largoC
        filZ = (ct.loc[:,"zona"]==zona)&(ct.loc[:,"min"]<=area)&(ct.loc[:,"max"]>area)
        idx  = filZ.index[filZ][0]
        toneladasRequeridas = ct.at[idx,"toneladas"]
        btuRequeridos = toneladasRequeridas*12000
        btuRequeridos+= nPerso*500
        if ("cocinar"in activi) or ("cocina" in fuentes):
            btuRequeridos+= 4000
        toneladasRequeridas = btuRequeridos/12000
        p = toneladasRequeridas//0.5
        r = toneladasRequeridas%0.5
        if r>0:
            p+=1
        toneladasRequeridas=p*0.5

        #print("bturRequeridos: ", btuRequeridos)
        #print("toneladasRequeridas: ",toneladasRequeridas)
        # iluminación
        if (ilumin!="") and (ilumin!="led"):
            txt+=fc.selecTxt(lib,"AA10")+" "
        # Carga termica
        if (toneladasRequeridas>toneladas) and (toneladas!=0) :
            txt+=fc.selecTxt(lib,"AA11").replace("[tE]",str(round(toneladas,2))).replace("[tR]",str(round(toneladasRequeridas,2)))+" "
        seerS=round(seerS)
        # SEER
        if toneladas != 0:
            if seerS<16:
                txt+=fc.selecTxt(lib, "AA12")+" "
            elif 16<=seerS<19:
                txt+=fc.selecTxt(lib,"AA13")+" "
            elif 19<=seerS:
                txt+=fc.selecTxt(lib,"AA14")+" "
            txt=txt.replace("[seer]",str(seerS))
        # resumen de revisión
        if (seerS>=16) and (hrsUso<=hrsNe):
            txt+=fc.selecTxt(lib,"AA06S2")
        if seerS<19 and ((evaLim=="si")or (conLim=="si")or(evaVen=="no")or(conVen=="no")or((tuberias!="")and(tuberias!="buen_estado"))):
            #print(tuberias)
            txt+="<br />"+fc.selecTxt(lib,"AA15")+" "
            if (evaLim=="si") or (conLim=="si"):
                txt+=fc.selecTxt(lib,"AA16")+" "
            if evaVen=="no":
                txt+=fc.selecTxt(lib,"AA17").replace("[evaVenTxt]",evaVenT)+" "
            if conVen=="no":
                txt+=fc.selecTxt(lib,"AA18").replace("[conVenTxt]",conVenT)+" "
            if "tuberia_golpes" in tuberias:
                txt+=fc.selecTxt(lib,"AA19")+" "
            if "tuberias_hielos" in tuberias:
                txt+=fc.selecTxt(lib,"AA20")+" "
            if "aislamiento_mal" in tuberias:
                txt+=fc.selecTxt(lib,"AA21")+" "
            if fugas=="si":
                txt+=fc.selecTxt(lib,"AA22").replace("[fugasTxt]",fugasT)+" "
        if ((seerS<16) or (toneladasRequeridas>toneladas)) and (toneladas!=0):
            aadb["ton"]=aadb[["BTU/h"]]/12000
            if (aadb.ton==toneladasRequeridas).any():
                idx    = aadb.index[aadb.ton==toneladasRequeridas][0]
                PotAhorro.loc[0,"%Ahorro"    ] = 1-(seerS/aadb.at[idx,"SEER"])
                PotAhorro.loc[0,"kwhAhorrado"] = PotAhorro.loc[0,"%Ahorro"]*kwh
                PotAhorro.loc[0,"Accion"     ] = fc.selecTxt(lib,"AApa01").replace("[minisplit]",fc.ligarTextolink("Minisplit",aadb.at[idx,"link"]))
                txt += "<br />" + fc.selecTxt(lib, "AA23").replace("[minisplit]",fc.ligarTextolink("Minisplit",aadb.at[idx,"link"]))
            else:
                print("¡¡SIN OPCIONES DE REEMPLAZO PARA EL AIRE ACONDICIOANDO!!")


    return txt