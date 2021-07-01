import pandas as pd
import numpy as np
import scipy as sp
def leerLibreriaCTV():
    try:
        libCTV = pd.read_excel(
        f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
        sheet_name='libreriaCTV')
        libUPS = pd.read_excel(
        f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
        sheet_name='libreriaCTV')
    except:
        libCTV = pd.read_excel(
        f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
        sheet_name='libreriaCTV')
        libUPS = pd.read_excel(
        f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
        sheet_name='libreriaCTV')


    libCTV.columns = ['A','B', 'C','D','E'] # Define los nombres de las columnas en Excel.
    libUPS.columns = ['A','B','C','D','E']
    return [libCTV, libUPS]



def caractCTV(dfCTV):
    # Sonido
    sLogic= (dfCTV.disp == 'Sonido'     ) | \
            (dfCTV.disp == 'Bocinas'    ) | \
            (dfCTV.disp == 'Surround'   ) | \
            (dfCTV.disp == 'HomeTheater')

    sonido=sLogic.any()
    if sonido:
        tolSonido = all(dfCTV.loc[sLogic,'tol'])
    else:
        tolSonido = False
    if any(dfCTV.disp.str.contains('NoBreak')):
        UPS=True
    else:
        UPS=False
    # TV
    if any(dfCTV.disp.str.contains('TV')):
        tolTV = all(dfCTV.tol[dfCTV.disp.str.contains('TV')])
    else:
        tolTV = False
    # Reguladores
    regLogic=dfCTV.disp.str.contains('Regulador')
    nReg=(regLogic*1).sum()
    if nReg>1:
        regulador = True
        consumoRegulador = 0
    elif nReg==1:
        regulador = True
        consumoRegulador = dfCTV.loc[regLogic, 'cons']
    else:
        regulador = False
        consumoRegulador = 0
    # Consumo excluyendo *
    excLogic=(dfCTV.disp=='Decodificador')|\
    (dfCTV.disp=='Decodificador2')|\
    (dfCTV.disp=='Modem')|\
    (dfCTV.disp=='NoBreak')|\
    (dfCTV.disp=='Repetidor')|\
    (dfCTV.disp=='Antena')
    consumoStanby = dfCTV.loc[~excLogic,'cons'].sum()
    decodificador= ((dfCTV.disp== 'Decodificador')|(dfCTV.disp== 'Decodificador2')).any()
    print('VEces')
    print(consumoRegulador)
    if consumoRegulador is None:
        consumoRegulador=0
    else:
        consumoRegulador=consumoRegulador[1]
    print(consumoRegulador)

    return [consumoStanby, regulador, nReg,consumoRegulador, UPS, tolTV, sonido, tolSonido, decodificador]

def roiUPS(dfCTV):
    ROIUPS=3
    return  ROIUPS
def roiReg (dfCTV):
    ROI=3
    return ROI
def regDes(consumoRegulador, libCTV):
    # * = A5 A6 B5 B6
    ROI = roiReg()
    if consumoRegulador < 5:
        # *.1 - CTV15
        textoAdd = libCTV.loc[19,'E']
    else:
        if ROI > 3:
            # *.2 CTV16 CTV17
            textoAdd = libCTV.loc[20,'E'] + libCTV.loc[20,'E']
        else:
            # *.3 CTV16 CTV18
            textoAdd = libCTV.loc[20,'E'] + libCTV.loc[22,'E']
    return textoAdd
def regNodo(texto,volEst,consumoStanby,consumoRegulador,tolTV,sonido,tolSonido,nReg,libCTV):

    if volEst:
        print('volEst')
        print(consumoRegulador)
        if (consumoStanby-consumoRegulador)<=2:
            # A1 B1 - CTV04S03 CTV04S05 CTV04S06
            texto = libCTV.loc[5,'E']+libCTV.loc[7,'E']+libCTV.loc[8,'E']
        if (consumoStanby-consumoRegulador)>2:
            # A2 B2 - CTV01 CTV02 CTV04S03 CTV04S06 CTV22
            print('# A2 B2 - CTV01 CTV02 CTV04S03 CTV04S06 CTV22')
            texto = libCTV.loc[0,'E']+libCTV.loc[1,'E']+'\n'+libCTV.loc[5,'E']+libCTV.loc[8,'E']+'\n'+libCTV.loc[26,'E']
    else:
        if tolTV:
            if not sonido:
                if (consumoStanby - consumoRegulador)<=2:
                    # A3.1 B3.1 - CTV04S02 CTV04S04 CTV04S06
                    texto = libCTV.loc[4, 'E'] + ' ' + libCTV.loc[6, 'E'] + libCTV.loc[8, 'E']
                if (consumoStanby - consumoRegulador)> 2:
                    # A3.2 B3.2 - CTV01 CTV02 CTV04S02 CTV04S04 CTV04S06
                    texto = libCTV.loc[0, 'E'] + ' ' + libCTV.loc[1, 'E'] + '\n' + libCTV.loc[4, 'E'] + ' ' + libCTV.loc[6, 'E'] + libCTV.loc[8, 'E']
            if sonido:
                if tolSonido and ((consumoStanby - consumoRegulador)<=2):
                    # A3.1 B3.1 - CTV04S02 CTV04S04 CTV04S06
                    texto = libCTV.loc[4, 'E'] + ' ' + libCTV.loc[6, 'E'] + libCTV.loc[8, 'E']
                if tolSonido and ((consumoStanby - consumoRegulador)> 2):
                    # A3.2 B3.2 - CTV01 CTV02 CTV04S02 CTV04S04 CTV04S06
                    texto = libCTV.loc[0, 'E'] + ' ' + libCTV.loc[1, 'E'] + '\n' + libCTV.loc[4, 'E'] + ' ' + libCTV.loc[6, 'E'] + libCTV.loc[8, 'E']
                if not tolSonido:
                    # A6 B6 - priemra parte CTV01 CTV02 CTV10
                    texto = libCTV.loc[0, 'E'] + ' ' + libCTV.loc[1, 'E'] + libCTV.loc[14, 'E']
                    if nReg>1:
                        texto = texto + '\n'+ 'HAY MAS DE UN REGULADOR\nREQUIERO RECOMENDACIÓN MANUAL'
                    elif nReg==1:
                        texto = texto+ '\n' + regDes( consumoRegulador)
        if not tolTV:
            # A5 B5 - priemra parte CTV01 CTV02 CTV10
            texto = libCTV.loc[0, 'E'] + ' ' + libCTV.loc[1, 'E'] + libCTV.loc[14, 'E']
            if nReg > 1:
                texto = texto + '\n' + 'HAY MAS DE UN REGULADOR\nREQUIERO RECOMENDACIÓN MANUAL'
            elif nReg==1:
                texto = texto + '\n' + regDes( consumoRegulador)
    return texto

def armarTexto(volEst,dfCTV):
    [lib, libUPS]=leerLibreriaCTV()
    texto=''
    [consumoStanby, regulador, nReg,consumoRegulador, UPS, tolTV, sonido, tolSonido,decodificador] = caractCTV(dfCTV)
    print([consumoStanby, regulador, nReg,consumoRegulador, UPS, tolTV, sonido, tolSonido,decodificador])
    if UPS:
        ROIUPS = roiUPS(lib)

    if   ((consumoStanby >= 2)==False) and (UPS==False):
        # 1 CTV20
        print('1 CTV20')
        texto=lib.loc[24,'E']

    elif ((consumoStanby >= 2) == False) and (UPS == True ):
        # ROIUPS=ROI_UPS()
        if (regulador == False) and (ROIUPS <= 3):
            # 3 UPS01 UPS03
            print('# 3 UPS01 UPS03')
            texto = libUPS.loc[0, 'E'] + '\n' + libUPS.loc[2, 'E']

        if (regulador == False) and (ROIUPS > 3):
            # 4 UPS02 UPS03
            print('# 4 UPS02 UPS03')
            texto = libUPS.loc[1, 'E'] + '\n' + libUPS.loc[2, 'E']

        if (regulador == True) and (UPS == True):
            # Linea A
            print('# Linea A')
            texto = texto + 'REQUIERO UNA RECOMENDACIÓN MANUAL HYA UN UPS Y REGULADOR EN EL CTV\n'
            texto = regNodo(texto,volEst,consumoStanby,consumoRegulador,tolTV,sonido,tolSonido,nReg,lib) # acomodar argumentos

    elif ((consumoStanby >= 2) == True ) and (UPS == False):
        if not regulador :
            # 2 CTV01 CTV02 CTV04S06
            print('# 2 CTV01 CTV02 CTV04S06')
            texto=lib.loc[0,'E']+'\n'+lib.loc[1,'E']+lib.loc[8,'E']
        if regulador:
            # Linea B
            print('# Linea B')
            texto= regNodo(texto,volEst,consumoStanby,consumoRegulador,tolTV,sonido,tolSonido,nReg,lib) # acomodar argumentos

    elif ((consumoStanby >= 2) == True ) and (UPS == True ):
        if (regulador == False) and (ROIUPS <= 3):
            # 5 UPS01 CTV23 UPS03
            print('# 5 UPS01 CTV23 UPS03')
            texto = libUPS.loc[0, 'E'] + '\n'+lib.loc[27,'E'] +'\n'+ libUPS.loc[2, 'E']

        if (regulador == False) and (ROIUPS > 3):
            # 6 UPS02 CTV23 UPS03
            print('# 6 UPS02 CTV23 UPS03')
            texto = libUPS.loc[1, 'E'] + '\n' +lib.loc[27,'E'] +'\n'+ libUPS.loc[2, 'E']
    if decodificador:
        texto=texto+'\n'+lib.loc[2,'E']

    if len(dfCTV)>1:
        texto=texto.replace('{s}','s')
        texto = texto.replace('{n}', 'n')
    else:
        texto=texto.replace('{s}','')
        texto = texto.replace('{n}', '')
        texto = texto.replace('dispositivo', 'equipo')
        texto = texto.replace('tiene un alto consumo','se mantiene consumiendo energía')


    linkA = 'www.google.com'
    Address = 'link'
    LinkS = '<br />'+'<link href="' + str(linkA) + '"color="blue">' + Address + ' </link>'
    texto = texto.replace('[link protector de sobrevoltaje]',LinkS)


    return texto




