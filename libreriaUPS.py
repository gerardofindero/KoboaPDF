import pandas as pd
import numpy as np
def reducirdatos():
    try:
        data = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/libreriaUPS.xlsx",
            sheet_name= "UPS y NoBreaks")
    except:
        data = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/libreriaUPS.xlsx",
            sheet_name="UPS y NoBreaks")
    sb = 'Total Input Power in W at 0% Load Min Config Lowest Dependency (ac)'  # standby
    va = 'Apparent Output Power Rating Minimum Configuration (VA)'  # VA
    numCR = 'Number of Battery Backup and Surge Protected Outlets'  # numero de conectores con respaldo de bateria
    numSR = 'Number of Surge Protected Only Outlets'  # numero de conectores sin respaldo de bateria
    entrada = 'Rated Input Voltage (V rms)'  # voltaje de entrada del nobreak (escoger los que trabajan a 120 Vrms)
    costo = 'Cost (MXN)'  # costo en pesos mexicanos
    link = 'Buy Link'  # link de compra
    marca = 'Brand Name'
    modelo = 'Model Name'
    selec = (data.loc[:, va] < 1600) & (data.loc[:, sb] < 15)
    data=data.loc[selec,:].copy()
    vrms120 = data.loc[:,entrada].str.split(pat='-').apply(vrms)
    data=data.loc[vrms120,:].copy()
    writer = pd.ExcelWriter('dbUPSreducida.xlsx')
    data.to_excel(writer, 'data')
    writer.save()
    print(data)

def leerLibreriaUPSLimpieza():
    try:
        data = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/libreriaUPS.xlsx",
            sheet_name= "UPS y NoBreaks")
    except:
        data = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/libreriaUPS.xlsx",
            sheet_name="UPS y NoBreaks"
        )
    sb      = 'Total Input Power in W at 0% Load Min Config Lowest Dependency (ac)' # standby
    va      = 'Apparent Output Power Rating Minimum Configuration (VA)'             # VA
    numCR   = 'Number of Battery Backup and Surge Protected Outlets'                # numero de conectores con respaldo de bateria
    numSR   = 'Number of Surge Protected Only Outlets'                              # numero de conectores sin respaldo de bateria
    entrada = 'Rated Input Voltage (V rms)'                                         # voltaje de entrada del nobreak (escoger los que trabajan a 120 Vrms)
    costo   = 'Cost (MXN)'                                                          # costo en pesos mexicanos
    link    = 'Buy Link'                                                            # link de compra
    marca   = 'Brand Name'
    modelo  = 'Model Name'
    selec = (data.loc[:,va]<1600) & (data.loc[:,sb]<15)
    data=data.loc[selec,[sb,va,numCR,numSR,entrada,costo,link,marca,modelo]].copy()
    data.columns=['sb','va','numCR','numSR','entrada','costo','link','marca','modelo']
    vrms120=data.entrada.str.split(pat='-').apply(vrms)
    data=data.loc[vrms120,['sb','va','numCR','numSR','costo','link','marca','modelo']].copy().reset_index()
    print(data)
    return data
def leerLibreriaUPS():
    try:
        data = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/dbUPSreducida.xlsx",
            sheet_name= "data")
    except:
        data = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/No Breaks UPS/dbUPSreducida.xlsx",
            sheet_name="data"
        )
    sb      = 'Total Input Power in W at 0% Load Min Config Lowest Dependency (ac)' # standby
    va      = 'Apparent Output Power Rating Minimum Configuration (VA)'             # VA
    numCR   = 'Number of Battery Backup and Surge Protected Outlets'                # numero de conectores con respaldo de bateria
    numSR   = 'Number of Surge Protected Only Outlets'                              # numero de conectores sin respaldo de bateria
    entrada = 'Rated Input Voltage (V rms)'                                         # voltaje de entrada del nobreak (escoger los que trabajan a 120 Vrms)
    costo   = 'Cost (MXN)'                                                          # costo en pesos mexicanos
    link    = 'Buy Link'                                                            # link de compra
    marca   = 'Brand Name'
    modelo  = 'Model Name'
    data=data.loc[:,[sb,va,numCR,numSR,entrada,costo,link,marca,modelo]].copy()
    data.columns=['sb','va','numCR','numSR','entrada','costo','link','marca','modelo']
    return data

def vrms(vrmsRstr):
    vrmsRnumeric = [float(i) for i in vrmsRstr]
    vrmsRnumeric = ((120<=max(vrmsRnumeric)) & (120>=min(vrmsRnumeric)))
    return vrmsRnumeric
def roiUPS(sugUPS, sbUPS):
    ahorro = (sbUPS-sugUPS.at[0,'sb'])*24*60*6.1/1000 # ahorro al bimestre
    roi    = sugUPS.at[0,'costo']/ahorro/6
    return roi
def recomendacionUPS(dfDisp,VAmax,Vpro,FPfuga):
    dbUPS=leerLibreriaUPS()
    if dfDisp.disp.str.contains('NoBreak').any():
        nUPS=sum(dfDisp.disp.str.contains('NoBreak'))
        if nUPS==1:
            sbUPS     = float(dfDisp.loc[dfDisp.disp.str.contains('NoBreak'),'standby'])
            nDispCone = float(sum(dfDisp.cUPS))
            VAUPS     = sbUPS/FPfuga
            VAnoConecUPS = Vpro * dfDisp.loc[dfDisp.cUPS==False,'ampere'].sum()
            VAreco = VAmax-VAUPS-VAnoConecUPS
            VAreco = VAreco/0.8
            if (dbUPS.va>VAreco).any():
                posibilidades = dbUPS.loc[dbUPS.va>VAreco,:]
                posibilidades = posibilidades.loc[dbUPS.costo.notnull(),:]
                minIndx       = posibilidades.costo.idxmin()
                sugUPS        = posibilidades.loc[[minIndx]].copy().reset_index()
                if sugUPS.at[0,'sb']<sbUPS:
                    roi = roiUPS(sugUPS, sbUPS)
                    if any(sugUPS.link.isna()):
                        sugUPS.loc[0,'link']=''
                    result=[roi                  ,
                            sugUPS.at[0,'marca'] ,
                            sugUPS.at[0,'modelo'],
                            sugUPS.at[0,'link']]
                    return result

                else:
                    print('EL STANDBY DEL NOBREAK SUGERIDO ES MAYOR AL DEL ENCONTRADO EN CASA')
            else:
                print("VA de los sispositivos conectados al ups es superior a 1600")
        elif nUPS>1:
            print("RECOMENSACIÓN MANUAL, HAY MAS DE UN NOBREAK")
    else:
        print ("NO SE DETECTO UPS EN EL DF PROPORCIONADO")



