import pandas as pd
from libreriaHielo import recoMaqHie
from scipy.stats import norm
# 1.b. Lee otra librería (ver cuál es la Protolibreria)
def libreria2():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/Refrigeradores/libreriaRefrisV3s.xlsx",sheet_name='Libreria')
    except:
        Libreria = pd.read_excel(f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Refrigeradores/libreriaRefrisV3s.xlsx",sheet_name='Libreria')
    Libreria=Libreria.set_index('Codigo')
    return Libreria


def ClavesRefri(EquiposRefri):
    EquiposR = EquiposRefri
    EquiposR=EquiposR.dropna(subset=['Pot Compresor'])
    EquiposR = EquiposR.fillna(0)
    Libreria=libreria2()

    Lib = pd.DataFrame(index=['Refrigerador'],
                            columns=['Marca', 'Codigo', 'Texto'])
    for i in EquiposR.index:
        TempR = (EquiposR['Temp Refri'][0])
        TempC = (EquiposR['Temp Conge'][0])
        NominalComp = int(EquiposR['Pot Compresor'][0])
        TempComp = float(EquiposR['Temp Compresor'][0])
        Volumen =int(EquiposR['Volumen'][0])
        Encendido = float(EquiposR["Encendido"][0])
        Codigo=EquiposR['Clave'][0]
        Codigo = str(Codigo)+','+str(TempR)+'/'+str(TempC)+'/'+ str(NominalComp) + '/'+str(TempComp) + '/'+str(Volumen)+"/"+str(Encendido)
####### Detalles      #######################################
        # Alarma
        if "inexistente"  in str(EquiposR["Alarma"])    : Codigo += ",AI"
        if "descompuesto" in str(EquiposR["Alarma"])    : Codigo += ",AD"
        # Ventilas
        if "no"           in str(EquiposR["Ventilas"])  : Codigo += ",SV"
        # Porcentaje de prendido
        if ("prolongado"  in str(EquiposR["Prob Refr"])) \
        or ("ontiempo"    in str(EquiposR["Prob Refr"])): Codigo += ",PR"
        # Ciclos de deshielo continuos
        if "deshielo"     in str(EquiposR["Prob Refr"]) : Codigo += ",DH"
####### Causas suaves #######################################
        # Ventilacion
        if '1'          in str(EquiposR['Encerrado']) : Codigo += ",VN"
        # Evaporador sucio
        if 'suciedad'   in str(EquiposR['Prob Comp']) : Codigo += ",SU"
####### Causas tecnica ######################################
        # compresor a alta potencia
        if (NominalComp > 120) \
        or ("altapotencia" in str(EquiposR["Prob Refr"])) :Codigo += ",CN"
        # empaque
        if "si" in str(EquiposR["Empaques"]): Codigo += "EM"
        # difusor mal
        if ("potenciaventilador" in str(EquiposR["Prob Comp"] ))\
        or ("tocandolo"          in str(EquiposR["Difusor"]   ))\
        or ("detenido"           in str(EquiposR["Difusor"]   ))\
        or ("rotas"              in str(EquiposR["Difusor"]   ))\
        or ("otro"               in str(EquiposR["Difusor"]   )): Codigo += "DM"
        # tuberias picadas | fugas de refrigerante
        if "si" in str(EquiposR["Tuberias"]): Codigo += "FG"
        # puertas dañadas
        if "puertasdanadas"     in str(EquiposR["Cierre"]): Codigo += "PD"
    return  Codigo


def Clasifica(Claves):
    ClavesSep='N'
    if pd.notna(Claves):
        ClavesSep=Claves.split(", ")
    return ClavesSep[0]


def LeeClavesR(Claves,notas,nombre,consumo):
    print("Claves refrigeracion",Claves)
    kWh = float(consumo)
    Texto=''

    TextoF = notas
    PotencialAhorro=0
    PotAhorro = pd.DataFrame(index=[0], columns=["%Ahorro", "kwhAhorrado", "Accion"])
    lib = libreria2()

    if pd.notna(Claves):
        ClavesSep=Claves.split(",")
        equipoR=ClavesSep[0]
        Datos= ClavesSep[1].split("/")

        TRef      = float(Datos[0])
        TCong     = float(Datos[1])
        NomCom    = float(Datos[2])
        TempCom   = float(Datos[3])
        Volumen   = float(Datos[4])
        Encendido = float(Datos[5])/100

        #print("NomCom",NomCom)
        #print("TempCom",TempCom)
        #print("Volumen",Volumen)
        #print("TRef",TRef)
        #print("TCong",TCong)
        #print("Encendido",Encendido)

        if equipoR=='RF':
            EQR='refrigerador'
            Volumen=float(Datos[4])*0.000022

            percentil = norm.cdf(((float(kWh)*6.0)**0.1 - (1.738365 + 0.0057272 * Volumen))/0.01962684,loc=0,scale=1)

            Ns = 0
            if (TRef < 4) or (TCong <-14): Ns+=1
            if "VN" in Claves            : Ns+=1
            if "SU" in Claves            : Ns+=1
            EncendidoNs=Encendido-(0.07*Ns)
            percentilNs =  norm.cdf((((1-0.07*Ns)*float(kWh)*6.0)**0.1 - (1.738365 + 0.0057272 * Volumen))/0.01962684,loc=0,scale=1)
            #print("EncendidoNs", EncendidoNs)
            #print("Ns", Ns)
            #print("Percentil ori",percentil)
            #print("Percentil Ns",percentilNs)
            #print("kwh kwhNs",kWh,kWh*(1-(0.07*Ns)))
            Nt = 0
            #if "CN" in Claves: Nt +=1
            if "EM" in Claves: Nt +=1
            if "DM" in Claves: Nt +=1
            if "FG" in Claves: Nt +=1
            if "PD" in Claves: Nt +=1
            #print("Nt",Nt)
            if percentil<0.3:
                #### Zona verde ####
                Texto += lib.loc['REF001','Texto'] + lib.loc["REF015","Texto"]
            elif percentil>=0.90:
                #### NS a amarillo ####
                if percentilNs<0.90:
                    Texto += lib.loc['REF002', 'Texto']
                    # Temperaturas muy bajas
                    if Ns>0:
                        Texto += lib.loc["REF003", "Texto"]
                        if TRef >= 4 and TCong < -14:
                            Texto += lib.loc["REF004", "Texto"]
                        elif TRef < 4 and TCong >= -14:
                            Texto += lib.loc["REF005", "Texto"]
                        elif TRef < 4 and TCong < -14:
                            Texto += lib.loc["REF006", "Texto"]
                        # Mala ventilacion
                        if "VN" in Claves:
                            if "SV" in Claves:
                                Texto += lib.loc["REF007", "Texto"]
                            else:
                                Texto += lib.loc["REF009", "Texto"]
                        if "SU" in Claves:
                            Texto += lib.loc["REF010", "Texto"]

                    if "PR" in Claves:
                        Texto += "<br />" + lib.loc["REF011", "Texto"]
                        if "AI" in Claves:
                            Texto += lib.loc["REF011S02", "Texto"]
                        if "AD" in Claves:
                            Texto += lib.loc["REF011S03", "Texto"]
                    Texto += lib.loc["REF015", "Texto"]
                else:
                    #### NS rojo ####
                    Texto += lib.loc['REF016', 'Texto']
                    if (NomCom > 120) and not("CN" in Claves):
                        Texto+= lib.loc["REF017","Texto"]
                    elif (NomCom <= 120) and ("CN" in Claves):
                        Texto+= lib.loc["REF018","Texto"]
                    elif (NomCom > 120) and ("CN" in Claves):
                        Texto += lib.loc["REF019","Texto"]
                    else:
                        Texto = Texto.replace(" La principal causa es que su compresor (motor)","")
                    if Nt>0:
                        Texto += lib.loc["REF020","Texto"]
                        if "FG" in Claves:
                            Texto += lib.loc["REF021","Texto"]
                        if "DM" in Claves:
                            Texto += lib.loc["REF022","Texto"]
                        if "EM" in Claves:
                            Texto += lib.loc["REF023","Texto"]
                        if "PD" in Claves:
                            Texto += lib.loc["REF024","Texto"]

                    if Nt>1:
                        Texto += lib.loc["REF025","Texto"] + lib.loc["REF026","Texto"]
                        # Mala ventilacion
                        if "VN" in Claves:
                            if "SV" in Claves:
                                Texto += lib.loc["REF007", "Texto"]
                            else:
                                Texto += lib.loc["REF009", "Texto"]
                    elif (Nt == 0) and ("CN" in Claves):
                        Texto += lib.loc["REF028","Texto"] + lib.loc["REF029","Texto"]
                    elif (Nt == 0) and ((Encendido*(1-0.07*Ns))<0.53):
                        Texto += lib.loc["REF030","Texto"]
                    if TempCom > 50:
                        Texto += lib.loc["REF031","Texto"] + lib.loc["REF032","Texto"]

           


            else:

            ########## Escenario amarillo ##########
                Texto += lib.loc['REF002','Texto']
                # Temperaturas muy bajas
                if Ns>0:
                    Texto += lib.loc["REF003","Texto"]
                    if   TRef >= 4 and TCong <  -14:
                        Texto+= lib.loc["REF004","Texto"]
                    elif TRef <  4 and TCong >= -14:
                        Texto+= lib.loc["REF005","Texto"]
                    elif TRef <  4 and TCong <  -14:
                        Texto+= lib.loc["REF006","Texto"]
                    # Mala ventilacion
                    if "VN" in Claves:
                        if "SV" in Claves:
                            Texto += lib.loc["REF007", "Texto"]
                        else:
                            Texto += lib.loc["REF009", "Texto"]
                    if "SU" in Claves:
                        Texto += lib.loc["REF010", "Texto"]

                if "PR" in Claves:
                    Texto += "<br />" + lib.loc["REF011","Texto"]
                    if "AI" in Claves:
                        Texto += lib.loc["REF011S02","Texto"]
                    if "AD" in Claves:
                        Texto += lib.loc["REF011S03","Texto"]
                Texto += lib.loc["REF015","Texto"]


            Texto = Texto.replace("/n*", "<br />- ")
            print("percentil original Refris: ",percentil)
            print("percentil Ns Refris: ",percentilNs)
            #print(Texto)


    PotAhorro['%Ahorro']=PotencialAhorro
    PotAhorro['kWhAhorrado']=kWh*PotencialAhorro
    PotAhorro['Accion']='Reemplazar el equipo por uno nuevo'



    return Texto,TextoF,PotAhorro