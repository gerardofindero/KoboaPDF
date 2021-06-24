import pandas as pd

def leerLibreriaCTV():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/Clusters de TV/libreriaCTV.xlsx",sheet_name='libreriaCTV')
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    Dicc = ['A','B', 'C','D','E'] # Define los nombres de las columnas en Excel.
    Libreria.columns = Dicc
    return Libreria
def formatoPluralSingular(texto, plural):
    if not plural:
        texto = texto.replace('{s}','').replace('{n}','')
    else:
        texto = texto.replace('{', '').replace('}', '')
    return texto
def armarTexto(gastobimestral=18, horasBimestre=732, listDisp=[], estbVol=False, toleDisp=False, timerKobo=False, maniobras=None):
    plural=len(listDisp)>1
    texto=''
    libreria = leerLibreriaCTV()
    costoTimer=150
    bimestresAlAño=6
    porcentajeAhorro=1.0-(horasBimestre/1464)  # 1 - porcentaje de tiempo que estan en uso los dispositivos
    ahorro = gastobimestral*porcentajeAhorro   # ahorro de $ al bimestre
    ROI    = costoTimer/ahorro/bimestresAlAño  # años para el ROI

    texto=formatoPluralSingular(libreria.loc[0,'E'],plural)

    if ROI <= 3 and timerKobo==True:
        texto = texto + libreria.loc[1,'E']

    if ('decodificador1' in listDisp) or ('decodificador2' in listDisp):
        texto= texto +'\n\n'+ libreria.loc[2,'E']

    if ('regulador1' in listDisp) or ('regulador2' in listDisp):
        if estbVol or toleDisp:
            if toleDisp and estbVol:
                texto=texto+'\n\n'+formatoPluralSingular(libreria.loc[3,'E'],plural)
            elif toleDisp and (not estbVol):
                texto = texto + '\n\n' + formatoPluralSingular(libreria.loc[4, 'E'], plural)
            elif (not toleDisp) and estbVol:
                texto = texto + '\n\n' + formatoPluralSingular(libreria.loc[5, 'E'], plural)
            texto=texto+' '+libreria.loc[6,'E']
    if 'nobreak' in listDisp:
        texto= texto+'\n\n'+ libreria.loc[7,'E']

    texto = texto+'\n\n'+ libreria.loc[8,'E']

    if (not(maniobras is None)) and len(maniobras)>0:
        texto=texto+'\n\n'+libreria.loc[9,'E'].replace('[maniobras]', ('\n'+maniobras))
    if ROI <= 3 and timerKobo == True:
        texto='\n'+texto+'\n\n'+libreria.loc[10,'E']

    texto = texto.replace('\n','<br />')
    return texto