import pandas as pd
from libreriaHielo import recoMaqHie
from scipy.stats import norm
# 1.b. Lee otra librería (ver cuál es la Protolibreria)
def libreria2():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/Refrigeradores/"
                                  f"Libreria_de_Refrigeradores.xlsx",sheet_name='Libreria')
        # Libreria2 = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/Refrigeradores/"
        #                           f"Libreria_de_Refrigeradores.xlsx",sheet_name='LibreriaF')
    except:
        Libreria = pd.read_excel(f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Refrigeradores/"
                                 f"Libreria_de_Refrigeradores.xlsx",sheet_name='Libreria')
        # Libreria2 = pd.read_excel(f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Refrigeradores/"
        #                          f"Libreria_de_Refrigeradores.xlsx",sheet_name='LibreriaF')
    #Dicc = ['A', 'B', 'C', 'D', 'E'] # Define los nombres de las columnas en Excel.
    #Dicc2 = ['A', 'B', 'C', 'D', 'F','E'] # Define los nombres de las columnas en Excel.
    #Libreria.columns = Dicc
    #Libreria2.columns = Dicc2
    #Libreria2=Libreria2.set_index('Codigo')
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
        Codigo=EquiposR['Clave'][0]
        Codigo = str(Codigo)+','+str(TempR)+'/'+str(TempC)+'/'+ str(NominalComp) + '/'+str(TempComp) + '/'+str(Volumen)

        ## Compresor Nominal
        if NominalComp > 120:
            Codigo += ",CN"

        #Calor
        if TempComp > 50:
            Codigo +=',TM'

        if 'prendido' in str(EquiposR['Prob Refr']):
            Codigo +=',PR'
        if 'puertas' in str(EquiposR['Prob Refr']):
            Codigo +=',PT'
        if 'dehielo' in str(EquiposR['Prob Refr']):
            Codigo +=',DH'
        if  'si' in EquiposR['Tuberias']:
            Codigo += ",TB"
        if  'si' in EquiposR['Jabon']:
            Codigo += ",JB"
        if 'inexistente' in str(EquiposR['Prob Refr']) or 'descompuesto' in str(EquiposR['Prob Refr']):
            Codigo +=',AM'

    #Ruido
        if 'ruido' in str(EquiposR['Prob Comp']):
            Codigo +=',RU'

        #Ventilador
        if 'ventilador' in str(EquiposR['Prob Comp']):
            Codigo +=",VE"

        if 'encerrado' in str(EquiposR['Ventilacion']):
            Codigo +=",VN"

         # Suciedad
        if 'suciedad' in str(EquiposR['Prob Comp']):
            Codigo += ",SU"
        # Viejo
        if 'viejo' in str(EquiposR['Prob Comp']):
            Codigo += ",VI"
            # Suciedad
        if 'encerrado' in str(EquiposR['Prob Comp']):
            Codigo += ",EN"
        # Viejo
        if 'enclaustrado' in str(EquiposR['Prob Comp']):
            Codigo += ",EN"
        #Cierre
        if EquiposR['Cierre'][0]!= 0:

            Codigo += ",CI"
        #Empaques
        if EquiposR['Empaques'][0] != 'si':
            Codigo += ",EB"
        else:
            Codigo += ",EM"

        #Temperatura interior
        if -10 > EquiposR['Temp Conge'][0] >-14:
            Codigo += ',TCB'
        if EquiposR['Temp Conge'][0] <-14:
            Codigo += ',TCM'
        # Temperatura interior

        if 3 >= TempR >= -7:
            Codigo += ',TRB'
        if EquiposR['Temp Refri'][0] < -8:
            Codigo += ',TRM'

    return  Codigo


def Clasifica(Claves):
    ClavesSep='N'
    if pd.notna(Claves):
        ClavesSep=Claves.split(", ")
    return ClavesSep[0]


def LeeClavesR(Claves,notas,nombre,consumo):
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
        TCong=Datos[0]
        TRef = Datos[1]
        NomCom=Datos[2]
        TempCom=Datos[3]
        Volumen=Datos[4]

        if equipoR=='RF':
            EQR='refrigerador'
            Volumen=float(Datos[4])*0.000022
            percentil= norm.cdf(((float(kWh)*6.0)**0.1 - (1.738365 + 0.0057272 * Volumen))/0.01962684,loc=0,scale=1)
            if 0.3 > percentil:
                Texto = lib.loc['REF001','Texto']
            elif percentil>0.90:
                Texto = lib.loc['REF016','Texto']
                if NomCom>120:
                    Texto = lib.loc['REF017','Texto']




            else:
                Texto = lib.loc['REF002','Texto']



# #### Dentro del cuadro
#         # Empaques bien
#         if 'EB' in Claves:
#             #Texto= Texto+' '+lib.loc[10,'E']+' '+lib.loc[12,'E']
#             TextoF= TextoF+' '+lib2.loc['REFF06','Texto']
#
#         # Empaques mal
#         if 'EM' in Claves:
#             Texto= Texto+' '+lib.loc['REF13','Texto']
#             TextoF= TextoF+' '+lib2.loc['REFF07','Texto']
#
#         # Temperatura congelador mal
#         if 'TCM' in Claves:
#             Texto= Texto+' '+lib.loc['REF14','Texto']+' '+lib.loc['REF15','Texto']+' '+lib.loc['REF17','Texto']
#             Texto = Texto.replace('[EQQ]', 'congelador')
#             #TextoF= TextoF+' '+lib2.loc['REFF07','Texto']
#
#         #Temperatura congelador bien
#         # if 'TCB' in Claves:
#         #     #Texto = Texto + ' ' + lib.loc[17, 'E']
#         #     TextoF= TextoF+' '+lib2.loc['REFF07','Texto']
#
#         #Temperatura refrigerador mal
#         if 'TRM' in Claves:
#             Texto= Texto+' '+lib.loc['REF14','Texto']+' '+lib.loc['REF16','Texto']+' '+lib.loc['REF18','Texto']
#             #Texto = Texto.replace('[EQQ]', 'refrigerador')
#             TextoF= TextoF+' '+lib2.loc['REFF22','Texto']
#
#         #Temperatura refrigerador bien
#         # if 'TRB' in Claves:
#         #     #Texto = Texto + ' ' + lib.loc[18, 'E']
#         #     TextoF= TextoF+' '+lib2.loc['REFF07','Texto']
# ###
#         ## Compresor Nominal
#         if 'CN' in Claves:
#             Texto= Texto+' '+lib.loc['REF00','Texto']+' '+lib.loc['REF02','Texto']
#             Texto= Texto.replace(' [Y]',str(NomCom))
#             TextoF= TextoF+' '+lib2.loc['REFF04','Texto']
#             if 'TM' in Claves:
#                 Texto= Texto+' y una'
#
#         ## Temp Compresor
#         if float(TempCom) > 10.0:
#             if 'TM' in Claves:
#                 Texto= Texto+' '+lib.loc['REF00','Texto']+' '+lib.loc['REF01','Texto']
#                 #Texto = Texto.replace('[TC]', str(TempCom))
#                 TextoF= TextoF+' '+lib2.loc['REFF10','Texto']
#
#                 TextoF = TextoF.replace('[TC]', str(TempCom))
#
#             else:
#                 TextoF= TextoF+' '+lib2.loc['REFF11','Texto']
#                 TextoF = TextoF.replace('[TC]', str(TempCom))
#
#         if 'TM' in Claves or 'CN' in Claves:
#             Texto= Texto+' '+ lib.loc['REF03','Texto']
#
# ###
#         if 'RU' in Claves or 'VI' in Claves:
#             Texto= Texto+' '+ lib.loc['REF04','Texto']
#         ## Ruido
#         if 'RU' in Claves:
#             Texto = Texto + ' ' + lib.loc['REF05', 'Texto']
#             TextoF= TextoF+' '+lib2.loc['REFF12','Texto']
#         ## Viejo
#         if 'VI' in Claves:
#             Texto = Texto + ' ' + lib.loc['REF06', 'Texto']
#             TextoF= TextoF+' '+lib2.loc['REFF13','Texto']
#         if 'RU' in Claves or 'VI' in Claves:
#             Texto= Texto+' '+ lib.loc['REF07','Texto']
#
#         ## VEntilador
#         if 'VE' in Claves:
#             Texto = Texto + ' ' + lib.loc['REF09', 'Texto']
#             TextoF= TextoF+' '+lib2.loc['REFF19','Texto']
#
#         ## Sucio
#         if 'SU' in Claves:
#             Texto = Texto + ' ' + lib.loc['REF08', 'Texto']
#             TextoF= TextoF +' ' + lib2.loc['REFF14','Texto']
#
#
#         ## Ventilador Encerrado
#         if 'VN' in Claves:
#             Texto = Texto + ' ' + lib.loc['REF12', 'Texto']
#             TextoF= TextoF+' '+lib2.loc['REFF15','Texto']
#         if 'PR' in Claves:
#             Texto= Texto+' '+ lib.loc['REF10', 'Texto']
#             #TextoF= TextoF+' '+lib2.loc['REFF02','Texto']
#         if 'PT' in Claves:
#             Texto= Texto+' '+ lib.loc['REF11', 'Texto']
#             TextoF= TextoF+' '+lib2.loc['REFF21','Texto']
#         if 'DH' in Claves:
#             #Texto= Texto+' '+lib.loc[6,'E']
#             TextoF= TextoF+' '+lib2.loc['REFF03','Texto']
#         if 'TB' in Claves:
#             #Texto= Texto+' '+lib.loc[6,'E']
#             TextoF= TextoF+' '+lib2.loc['REFF016','Texto']
#         if 'JB' in Claves:
#             #Texto= Texto+' '+lib.loc[6,'E']
#             TextoF= TextoF+' '+lib2.loc['REFF017','Texto']
#         if 'AM' in Claves:
#             #Texto= Texto+' '+lib.loc[6,'E']
#             TextoF= TextoF+' '+lib2.loc['REFF018','Texto']

        # if 'hielo' in nombre:
        #     TextoF = recoMaqHie(consumo)
        # if equipoR=='CN':
        #     EQR='congelador'
        #     formulaV=(float(Volumen)/6863.63)-8.83
        #     if formulaV>kWh:
        #         Texto = notas+lib2.loc['REF20','Texto']
        #     Texto = Texto.replace('Refrigerador', 'Congelador')
        #     TextoF = TextoF.replace('Refrigerador', 'Congelador')
        #     if kWh>250:
        #         PotencialAhorro=1-(120/kWh)
        #     else:
        #         PotencialAhorro=0
        #
        #
        #
        #
        # if equipoR=='MB':
        #     EQR='minibar'
        #     Volumen=float(Datos[4])*0.000022
        #     percentil= norm.cdf(((float(kWh)*6.0)**0.1 - (1.738365 + 0.0057272 * Volumen))/0.01962684,loc=0,scale=1)
        #     if 0.5 > percentil:
        #         Texto = notas+lib2.loc['REFF20','Texto']
        #     Texto = Texto.replace('Refrigerador', 'Minibar')
        #     TextoF = TextoF.replace('Refrigerador', 'Minibar')
        #
        #
        # if equipoR=='CV':
        #     EQR='cava'
        #     formulaV=(float(Volumen)/1300.8)+21.4
        #     if formulaV>kWh:
        #         Texto = notas+lib2.loc['REFF20','Texto']
        #     Texto = Texto.replace('Refrigerador', 'Cava')
        #     TextoF = TextoF.replace('Refrigerador', 'Cava')


        Texto = Texto.replace('[P]', NomCom)
        TextoF = TextoF.replace('[P]', NomCom)
        #TextoF = TextoF.replace('[R]', EQR)
        TextoF = TextoF.replace('[TR]', TRef)

        Texto = Texto.replace('[/n]', '<br /><br />')
        Texto = Texto.replace('[...]', ' ')
        TextoF = TextoF.replace('[/n]', '<br /><br />')
        TextoF = TextoF.replace('[...]', ' ')

    PotAhorro['%Ahorro']=PotencialAhorro
    PotAhorro['kWhAhorrado']=kWh*PotencialAhorro
    PotAhorro['Accion']='Reemplazar el equipo por uno nuevo'



    return Texto,TextoF,PotAhorro