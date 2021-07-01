import pandas as pd

def leerLibreriaCTV():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",sheet_name='libreriaCTV')
    except:
        Libreria = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",
            sheet_name='libreriaCTV')

    Dicc = ['A','B', 'C','D','E'] # Define los nombres de las columnas en Excel.
    Libreria.columns = Dicc
    return Libreria
def formatoPluralSingular(texto, plural):
    if not plural:
        texto = texto.replace('{s}','').replace('{n}','')
    else:
        texto = texto.replace('{', '').replace('}', '')
    return texto
def armarTextoCTV(gastobimestral, horasBimestre, listDisp, estbVol, toleDisp, timerKobo, maniobras):
    plural=len(listDisp)>1
    Dec = False
    Reg=False
    NBK=False
    texto=''
    libreria = leerLibreriaCTV()
    costoTimer=150
    bimestresAlAño=6
    porcentajeAhorro=1.0-(horasBimestre/1464)  # 1 - porcentaje de tiempo que estan en uso los dispositivos
    ahorro = gastobimestral*porcentajeAhorro   # ahorro de $ al bimestre
    ROI    = costoTimer/ahorro/bimestresAlAño  # años para el ROI
    if estbVol==1:
        estbVol=True
    else:
        estbVol=False
    texto=formatoPluralSingular(libreria.loc[0,'E'],plural)

    if ROI <= 3 and timerKobo==True:
        texto = texto + libreria.loc[1,'E']

    for i in listDisp:
        if ('Decodificador' in i) or ('Decodificador2' in i):
            if not Dec:
                texto= texto +'\n\n'+ libreria.loc[2,'E']
                Dec=True

        if ('Regulador' in i) or ('Regulador2' in i):
            if not Reg:
                if estbVol or toleDisp:
                    if toleDisp and estbVol:
                        texto=texto+'\n\n'+formatoPluralSingular(libreria.loc[3,'E'],plural)
                    elif toleDisp and (not estbVol):
                        texto = texto + '\n\n' + formatoPluralSingular(libreria.loc[4, 'E'], plural)
                    elif (not toleDisp) and estbVol:
                        texto = texto + '\n\n' + formatoPluralSingular(libreria.loc[5, 'E'], plural)
                    texto=texto+' '+libreria.loc[6,'E']
                    Reg=True
        if 'nobreak' in i:
            if not NBK:
                texto= texto+'\n\n'+ libreria.loc[7,'E']
                NBK=True

    texto = texto+'\n\n'+ libreria.loc[8,'E']

    if (not(maniobras is None)) and len(maniobras)>0:
        texto=texto+'\n\n'+libreria.loc[9,'E'].replace('[maniobras]', ('\n'+maniobras))

    if ROI <= 3 and timerKobo == True:
        linkA = 'https://www.amazon.com.mx/inteligente-compatible-temporizador-concentrador-certificado/'\
                'dp/B087D1ZXM4/ref=sr_1_5?__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&'\
                'dchild=1&keywords=timer+inteligente+smart+life&qid=1624486703&sr=8-5'
        Address =libreria.loc[10,'E']
        LinkS = '<br />' + '<link href="' + str(linkA) + '"color="blue">' + Address + ' </link>'
        texto=texto+'<br />'+LinkS

    texto = texto.replace('\n','<br />')

    print(len(texto))
    return texto