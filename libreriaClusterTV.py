import pandas as pd
import libreriaReguladores as lr
import libreriaUPS as lups
def leerLibreriaCTV():
    try:
        libCTV = pd.read_excel(
        f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
        sheet_name='libreriaCTV')
        links = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
            sheet_name='links')
        libUPS = pd.read_excel(
        f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
        sheet_name='libreriaCTV')
    except:
        libCTV = pd.read_excel(
        f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
        sheet_name='libreriaCTV')
        links = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
            sheet_name='links')
        libUPS = pd.read_excel(
        f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
        sheet_name='libreriaCTV')


    libCTV.columns = ['A','B', 'C','D','E'] # Define los nombres de las columnas en Excel.
    libUPS.columns = ['A','B','C','D','E']
    links.columns  = ['A','B','C','D']
    return [libCTV, libUPS, links]

def ligarTextolink(texto, link):
    if link == 'nan':
        link=''
    if len(link)>0:
        texto = '<br />' + '<link href="' + link + '"color="blue">' + texto + ' </link>'
        return texto
    else:
        return texto

def caractCTV(dfCTV):
    # Sonido
    sLogic= (dfCTV.disp.str.contains('Sonido'     )) | \
            (dfCTV.disp.str.contains('Bocinas'    )) | \
            (dfCTV.disp.str.contains('Surround'   )) | \
            (dfCTV.disp.str.contains('HomeTheater'))

    sonido=sLogic.any()
    if sonido:
        tolSonido = all(dfCTV.loc[sLogic,'tol'])
    else:
        tolSonido = False
    if any(dfCTV.disp.str.contains('NoBreak')):
        standbyUPS = float(dfCTV.loc[dfCTV.disp.str.contains('NoBreak'),'standby'])
        UPS=True
    else:
        standbyUPS = 0
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
        consumoRegulador = int(dfCTV.loc[regLogic, 'standby'])
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
    consumoStanby = dfCTV.loc[~excLogic,'standby'].sum()
    decodificador= ((dfCTV.disp== 'Decodificador')|(dfCTV.disp== 'Decodificador2')).any()

    return [consumoStanby, regulador, nReg,consumoRegulador,standbyUPS ,UPS, tolTV, sonido, tolSonido, decodificador]

def gastoUPS(standby):
    gasto= standby*24*60*6.1/1000
    return gasto
def upsNodo(consumoStanby,volEst,texto, standbyUPS,lib,links,dfCTV,VAmax,Vpro,FPfuga):
    refUPS = 3 # consumo en watts promedio de nobreaks por debajo de 16000 VA y 15 watts en la base de datos de energiStar
    if volEst:
        texto = lib.loc[28, 'E']
        if standbyUPS < refUPS:
            texto = texto + ' ' + lib.loc[30, 'E'].replace('[costoAlBimestreUPS]', str(gastoUPS(standbyUPS)))
        else:
            [ROIUPS, marca, modelo, linkUPS] = lups.recomendacionUPS(dfCTV, VAmax, Vpro, FPfuga)
            if ROIUPS <= 3:
                marcaYModelo = 'UPS de la marca ' + marca + ' modelo ' + modelo
                texto = texto + ' ' + lib.loc[31, 'E'].replace('[reemplazoUPS]',
                                                               ligarTextolink(marcaYModelo, str(linkUPS)))
            else:
                texto = texto + ' ' + lib.loc[32, 'E']
    else:
        texto = lib.loc[29, 'E']
        tolDispUPS = dfCTV.loc[dfCTV.cUPS == True, 'tol'].all()
        if tolDispUPS:
            texto = texto + ' ' + lib.loc[30, 'E'].replace('[costoAlBimestreUPS]', str(gastoUPS(standbyUPS)))
        else:
            texto = texto + ' ' + lib.loc[33, 'E']
    texto=texto.replace('[Consulta nuestro blog sobre UPS]',ligarTextolink('Consulta nuestro blog sobre UPS',str(links.at[10,'C'])))
    #print(str(links.at[10,'C'])=='nan')
    if consumoStanby > 2:
        texto = texto +'\n'+ lib.loc[27,'E']
    return texto

def regDes(consumoRegulador,dfCTV, libCTV,VAmax,Vpro,FPfuga,Uso):
    # * = A5 A6 B5 B6
    if consumoRegulador < 5:
        # *.1 - CTV15
        textoAdd = libCTV.loc[19,'E']
    else:
        [ROI, marcaYmodelo]= lr.roiReg(dfCTV,VAmax,Vpro,FPfuga,Uso)
        if ROI > 3:
            # *.2 CTV16 CTV17'
            print('# *.2 CTV16 CTV17')
            textoAdd = libCTV.loc[20,'E'] + libCTV.loc[20,'E']
        else:
            # *.3 CTV16 CTV18
            print('# *.3 CTV16 CTV18')
            textoAdd = libCTV.loc[20,'E'] + libCTV.loc[22,'E']
            textoAdd = textoAdd.replace('[reemplazoRegulador]', marcaYmodelo)
    return textoAdd
def regNodo(texto,volEst,consumoStanby,consumoRegulador,tolTV,sonido,tolSonido,nReg,libCTV,VAmax,Vpro,FPfuga,Uso,dfCTV):

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
                        texto = texto+ '\n' + regDes( consumoRegulador, dfCTV,libCTV,VAmax,Vpro,FPfuga,Uso)
        if not tolTV:
            # A5 B5 - priemra parte CTV01 CTV02 CTV10
            texto = libCTV.loc[0, 'E'] + ' ' + libCTV.loc[1, 'E'] + libCTV.loc[14, 'E']
            if nReg > 1:
                texto = texto + '\n' + 'HAY MAS DE UN REGULADOR\nREQUIERO RECOMENDACIÓN MANUAL'
            elif nReg==1:
                texto = texto + '\n' + regDes( consumoRegulador,dfCTV ,libCTV,VAmax,Vpro,FPfuga,Uso)
    return texto

def armarTexto(volEst,dfCTV,VAmax,Vpro,FPfuga):
    [lib, libUPS, links]=leerLibreriaCTV()
    texto=''
    [consumoStanby, regulador, nReg,consumoRegulador,standbyUPS, UPS, tolTV, sonido, tolSonido,decodificador] = caractCTV(dfCTV)
    print([consumoStanby, regulador, nReg,consumoRegulador, UPS, tolTV, sonido, tolSonido,decodificador])

    if   ((consumoStanby >= 2)==False) and (UPS==False):
        # 1 CTV20
        print('1 CTV20')
        texto=lib.loc[24,'E']

    elif ((consumoStanby >= 2) == False) and (UPS == True ):
        if not regulador:
            # Linea 3 y 4
            texto = upsNodo(consumoStanby,volEst,texto, standbyUPS,lib,links,dfCTV,VAmax,Vpro,FPfuga)

        if (regulador == True) and (UPS == True):
            # Linea A
            print('# Linea A')
            texto = texto + 'REQUIERO UNA RECOMENDACIÓN MANUAL HYA UN UPS Y REGULADOR EN EL CTV\n'
            texto = regNodo(texto,volEst,consumoStanby,consumoRegulador,tolTV,sonido,tolSonido,nReg,lib,VAmax,Vpro,FPfuga,'E',dfCTV) # acomodar argumentos

    elif ((consumoStanby >= 2) == True ) and (UPS == False):
        if not regulador :
            # 2 CTV01 CTV02 CTV04S06
            print('# 2 CTV01 CTV02 CTV04S06')
            texto=lib.loc[0,'E']+'\n'+lib.loc[1,'E']+lib.loc[8,'E']
        if regulador:
            # Linea B
            print('# Linea B')
            texto= regNodo(texto,volEst,consumoStanby,consumoRegulador,tolTV,sonido,tolSonido,nReg,lib,VAmax,Vpro,FPfuga,'E',dfCTV) # acomodar argumentos

    elif ((consumoStanby >= 2) == True ) and (UPS == True ):
        if not regulador:
            # Linea 5 y 6
            texto = upsNodo(consumoStanby,volEst, texto, standbyUPS, lib,links, dfCTV, VAmax, Vpro, FPfuga)
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


    linkA = links.loc[7,'C']
    Address = 'Protector de voltaje 40A'
    LinkS = '<br />'+'<link href="' + str(linkA) + '"color="blue">' + Address + ' </link>'
    texto = texto.replace('{link protector de sobrevoltaje}',LinkS)

    return texto




