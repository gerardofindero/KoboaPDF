import pandas as pd
import random
from libreriaLucesSolares import recoSolares
from libreriaSenMov import recoSensores
from libreriaTubosFluorescente import recoTuboFluorescente
from libreriaTirasLED import recoTirasLed
### Preguntas generales

# Tareas:
# Meter textos diferenciados (para repeticiones) de ROI

############################# Libreria Luminarias ###################################
## Este programa elige el texto correcto de luminarias para insertar en los reportes a clientes.
## El texto se anota sobre un archivo de Excel (Resultados_cliente.xlsx), pestaña 'Desciframiento', que después es procesado para generar el reporte automático.


## 1.
## Lee librería de textos de luminarias.
def libreriaL():
    try:
        # Libreria = pd.read_excel(Path.home() / 'Desktop' /'ProtoLibreria Luminaria.xlsx')
        Libreria = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Iluminación/Libreria_Luminarias.xlsx",sheet_name='Textos')
    except:
        Libreria = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Iluminación/Libreria_Luminarias.xlsx",sheet_name='Textos')
    # Libreria = pd.read_excel(r'C:\Users\Cesar\Desktop\libreria.xlsx')
    #Dicc = ['A', 'B', 'C', 'D', 'E'] # Define los nombres de las columnas en Excel.
    #Libreria.columns = Dicc # Asigna los nombres de las columnas de Excel al data frame de Python
    Libreria=Libreria.set_index('Codigo')
    return Libreria






## Esta función elige la primera sección de cada texto, en base al la información reportada en KOBO

def CondicionesLuces(Luminaria):
# Luminaria aquí es la base de datos condensada de Kobo.
## Se hace una copia de respaldo para no alterar los datos originales.
    Lumi = Luminaria.copy()
    print('Luminaria')

## Se lee la libreria textos de luminarias con la función libreriaL() y se asigna a 'Lib'
    Lib = libreriaL()

##Se rellenan los datos faltantes con NA en luminaria adicional (Luminaria KOBO).
    Luminaria['Adicional'].fillna('NA', inplace=True)

## Se resetea el indice para tener la referencia bien establecida (Luminaria KOBO).
    Luminaria.reset_index(drop=True, inplace=True)

## En este ciclo FOR se analiza cada una de las luces/conjunto de luces reportadas en el KOBO y se le asiga el texto correspondiente de la librería.
    for i in Luminaria.index:
        Numero = Luminaria.loc[i, 'Numero']         # Obtiene el número de luminarias que hay de ese tipo en ese espacio específico.

    ## Se asignan las variables de tipo y lugar de las luminarias encontradas en KOBO
        Tipo = Luminaria.loc[i, 'Tecnologia']       # Obtiene la tecnologia de luminarias

    ## Establece los textos a reportar cuando la luminaria no es LED.
        if Tipo != 'led':
            Adicional = Luminaria.loc[i, 'Adicional']      # Agrega todas las características adicionales de un tipo de foco (p. ej. dimeable, luz cálida, foco inteligente, etc...).
            if Adicional == 'NA':
                TextoCompleto = 'NA'
            else:
                TextoCompleto = Adicional

        else:
            TextoCompleto = 'LED'


    ##Se escribe el texto resultante en el condensado de Kobo.
        Luminaria.loc[i, 'Texto'] = TextoCompleto

    ## Se regresan los textos correspondientes como un data frame.
    return Luminaria['Texto']





############################# Base de Datos de Luminarias ###############################################
## En esta parte se lee la base de datos de luminarias y se filtran las opciones hasta tener el mejor sustituto LED

## Se lee la base de datos de luminarias (contiene modelos, precios, características, etc...)
def libreriaLED():
    try:
        ## Se va a la ruta donde se encuentra el archivo de Excel
        Libreria = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Iluminación/Base de datos luminarias/"
            f"Librería Luminarias vBENE final.xlsx",sheet_name='Librería')
    except:
        Libreria = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Iluminación/Base de datos luminarias/"
            f"Librería Luminarias vBENE final.xlsx",sheet_name='Librería')

    #Se renombran las columnas como se tienen en excel para facilitar referencia
    Dicc = ['A', 'B', 'C', 'D', 'E','F','G','H','I','J','K','L','M','N','O','P','Q','R',
            'S','T','U','V','W','X','Y','Z','AA','BB']
    Libreria.columns = Dicc
    return Libreria

## 4.
## Segunda parte para introducir textos de la librería de luminarias
## En esta funión se llevan a cabo los calculos para tener el % de ahorro y el ROI
## se eligen los textos correpondientes.

def variablesLuces(NumyTip, Watts,VV,tex,DAC,EntyTip,Lugar,conteoNOled,conteoled, conteoROI,uso,texto): # Variables se jalan de archivo de Excel en pestaña Desciframiento.
    aleatorio=random.randint(1, 3)
    #Se lee libreria de textos
    Lib =  libreriaL()
    Clav=''
    TextoCompleto = '' # Se declara la variable TextoCompleto para introducir textos de 'Lib' (libreria de textos)
    #ENTY = ['nada', 'nada'] # Se declara ENTY que albergará el tipo de entrada y tipo de foco.
    ENTY = EntyTip.split()
    tipo=''
    entrada=''
    Solar=False
    Sensor=False

    # Entrada y tipo de entrada vienen dentro de una variable, aquí se separan
    # Numero y tipo (LED, Fluorecente...etc ) vienen dentro de una variable, aquí se separan
    Numero = float(NumyTip.split()[0]) # Se saca el número de focos de cierto tipo
    Tecno = str(NumyTip.split()[1]) # Se saca la tecnología del tipo de foco (e.g. incandescente, halógena, etc...)
    if Numero==0:
        Numero=0.001
    Watts = float(Watts)/float(Numero) # Se sacan los watts por foco.

    TextoSolar=''
    if 'NOC' in texto:
        TextoSolar = recoSolares('nocturna','Si',VV,Watts,DAC)
        Solar=True
    #TextoSensor = recoSensores (kwh =VV , w = Watts, lugar = Lugar ,dac = DAC,hrsUso=uso)
    #if TextoSensor!='X':
    #    Sensor=True

    # Textos al reporte cuando el foco ya es LED.
    if Tecno =='led' or Tecno=='tira':
        if Tecno =='led':
            if aleatorio==1:
                TextoCompleto = TextoCompleto + Lib.loc['LUM14a', 'Texto']
            if aleatorio==2:
                TextoCompleto = TextoCompleto + Lib.loc['LUM14b', 'Texto']
            if aleatorio==3:
                TextoCompleto = TextoCompleto + Lib.loc['LUM14c', 'Texto']
        if Tecno =='tira':
            TextoCompleto = TextoCompleto + Lib.loc['LUM18', 'Texto']

        if conteoled == 5:
            TextoCompleto = TextoCompleto + Lib.loc['LUM07a', 'Texto']
            conteoled = 2
        if conteoled == 4:
            TextoCompleto = TextoCompleto + Lib.loc['LUM07b', 'Texto']
            conteoled = conteoled + 1
        if conteoled == 3:
            TextoCompleto = TextoCompleto + Lib.loc['LUM07c', 'Texto']
            conteoled = conteoled + 1
        if conteoled == 2:
            TextoCompleto = TextoCompleto + Lib.loc['LUM07d', 'Texto']
            conteoled = conteoled + 1
        if conteoled == 1:
            TextoCompleto = TextoCompleto + Lib.loc['LUM07f', 'Texto']
            conteoled = conteoled + 1

        # elif conteoled <= 5:
        #     TextoCompleto = TextoCompleto + Lib.loc[14+(conteoled-1), 'Texto']
        #     conteoled = conteoled + 1
        #     if conteoled==5:

        if uso>5 and Numero<10:
            TextoCompleto = TextoCompleto + Lib.loc['LUM11', 'Texto']
        if Numero>10 and uso<5:
            TextoCompleto = TextoCompleto + Lib.loc['LUM12', 'Texto']
        if Numero>10 and uso>5:
            TextoCompleto = TextoCompleto + Lib.loc['LUM13', 'Texto']

        if Sensor==False and Solar==False:
            if aleatorio==1:
                TextoCompleto = TextoCompleto + Lib.loc['LUM16a', 'Texto']
        if Sensor==False and Solar==False:
            if aleatorio==2:
                TextoCompleto = TextoCompleto + Lib.loc['LUM16b', 'Texto']
        if Sensor==False and Solar==False:
            if aleatorio==3:
                TextoCompleto = TextoCompleto + Lib.loc['LUM16c', 'Texto']

    ##### Tira LEDS
        if 'tira' in tex:
            largoLED= tex.split(',')[1]
            largoLED=largoLED.replace('cm','')
            TextoCompleto=recoTirasLed(float(largoLED), tex, DAC, Watts, VV, texto,TextoCompleto)

        if Numero == 1:
            TextoCompleto = TextoCompleto.replace('[s]', '')
        else:
            TextoCompleto = TextoCompleto.replace('[s]', 's')

        TextoCompleto = TextoCompleto.replace('[NUML]', str(round(int(Numero))))
        TextoCompleto = TextoCompleto.replace('[horasUso]', str(round(int(uso))))
    #separadodiag=


    elif  Tecno!= 'led':
        if not 'NO HAY CARS' in tex:
            Car1,Car2,Car3,Car4 = Caracteristicas(tex) # Se buscan las caracteristicas de las luminarias según el Kobo y se adecúan para que puedan ser comparadas en
        else:
            Car1=''
        # la base de datos de luminarias
        # Imprimir en pantalla características de focos

        if conteoNOled == 1:
            TextoCompleto = Lib.loc['LUM00a', 'Texto']
            conteoNOled  = conteoNOled + 1
        else:
            TextoCompleto = Lib.loc['LUM00b', 'Texto']

        genero=Lugar[len(Lugar)-3]
        if genero=='a':
            Lugar='la '+Lugar
        if genero=='o':
            Lugar='el '+Lugar
        # Reemplaza los 'placeholders' del texto por su valor reportado en campo (la hoja de 'Desciframiento' ya tiene estos valores.
        TextoCompleto = TextoCompleto.replace('[Tecnologia]', Tecno)
        TextoCompleto = TextoCompleto.replace('[Lugar_iluminación]', Lugar)
        TextoCompleto = TextoCompleto.replace('[CAR]', tex)
        TextoCompleto = TextoCompleto.replace('[NUML]', str(Numero))
        TextoCompleto = TextoCompleto.replace('[horasUso]', str(uso))
        TextoCompleto = TextoCompleto.replace('.0', "")
        TextoCompleto = TextoCompleto.replace('[...]', "")
        TextoCompleto = TextoCompleto.replace('Cocina', "la cocina")
        TextoCompleto = TextoCompleto.replace('cocina', "la cocina")
        TextoCompleto = TextoCompleto.replace('Recámara', "la recámara")
        TextoCompleto = TextoCompleto.replace('Recamara', "la recámara")
        TextoCompleto = TextoCompleto.replace('estudio_oficina', "la oficina")
        TextoCompleto = TextoCompleto.replace('Sala', "la sala")
        TextoCompleto = TextoCompleto.replace('Baño', "el baño")

        if Numero == 1:
            TextoCompleto = TextoCompleto.replace('1', 'única')
            TextoCompleto = TextoCompleto.replace('(s)', '')
            TextoCompleto = TextoCompleto.replace('(un)', 'un')
            TextoCompleto = TextoCompleto.replace('(n)', '')
            TextoCompleto = TextoCompleto.replace('(es)','')
            TextoCompleto = TextoCompleto.replace('halogenos','halogeno')

        else:
            TextoCompleto = TextoCompleto.replace('(s)','s')
            TextoCompleto = TextoCompleto.replace('(un)', '')
            TextoCompleto = TextoCompleto.replace('(n)', 'n')
            TextoCompleto = TextoCompleto.replace('(es)', 'es')
            TextoCompleto = TextoCompleto.replace('halogenoss', 'halogenos')

        # TEXTOS DE RETORNO DE INVERSION (Seguimos con focos que no son LED).
        ## Para las luminarias que cuentan con entrada y tipo de entrada se busca en la base de datos de las luminarias
        ## se obtienen consumo del LED, su precio y su LINK

        #Se cambian las variables para adecuarlas a la base de datos
        if len(ENTY)>=2:
            tipo=ENTY[0]
            tipo = DiccionarioLuz(tipo) # Función definida abajo. Cambia la sintaxis de la entrada del foco para ser igual a la de la base de datos.
            #print('Tipo: ' + str(tipo))
            entrada=ENTY[1]
            entrada = DiccionarioLuz(entrada)
            #print('Entrada tipo: ' + str(entrada))
            #Se usa la función de BuscarLED para encontrar el consumo, precio y link de los equivalentes en LED



        ConLED, Precio, Link = BuscarLED(tipo, entrada, Watts,Car1,Car2,Car3,Car4,Tecno,Numero)
        TT=0
        if ConLED != 0:

            #print('Potencia c LED: '+ str(ConLED))
            #print('Precio; '+ str(Precio))
            #print('Link: '+ Link)
            #Formulas
            TT = int(((1 - (float(ConLED) / Watts))*100)-10)
            ROI = abs((Numero * Precio) / ((TT/100) * VV * DAC)) # Calcula retorno de inversion en bimestres.

            ## Se elige el texto correspondiente de la libreria de textos para el ROI correspondiente
            if ROI <= 18: # Cuando el ROI es en un periodo corto.
                TextoROI = Lib.loc['LUM02', 'Texto']
            else: # Cuando el ROI no se alcanza en menos de 3 años.
                if conteoROI == 1:
                    TextoROI = Lib.loc['LUM03a', 'Texto']
                    conteoROI = conteoROI + 1
                elif conteoROI == 2:
                    TextoROI = Lib.loc['LUM03b', 'Texto']
                    conteoROI = conteoROI + 1
                elif conteoROI > 2:
                    TextoROI = Lib.loc['LUM03c', 'Texto']

            ## Se sustituye la variable ROI por el texto correspondiente
            TextoCompleto = TextoCompleto  + TextoROI
            TextoCompleto = TextoCompleto.replace('[ROI]', str(int(ROI)))
            TextoCompleto = TextoCompleto.replace('[NUML]', str(round(Numero, 0)))
            TextoCompleto = TextoCompleto.replace('[T]', str(round(TT, 1)))
            TextoCompleto = TextoCompleto.replace('[...]', '')
            if Numero == 1:
                TextoCompleto = TextoCompleto.replace('1', 'única')
                TextoCompleto = TextoCompleto.replace('(s)', '')
                TextoCompleto = TextoCompleto.replace('(un)', 'un')
                TextoCompleto = TextoCompleto.replace('(n)', '')
                TextoCompleto = TextoCompleto.replace('(es)','')

            else:
                TextoCompleto = TextoCompleto.replace('(s)','s')
                TextoCompleto = TextoCompleto.replace('(un)', '')
                TextoCompleto = TextoCompleto.replace('(n)', 'n')
                TextoCompleto = TextoCompleto.replace('(es)', 'es')

            Address = 'Link de compra'
            LinkS = '<link href="' + str(Link) + '"color="blue">' + Address + ' </link>'
            TextoCompleto = TextoCompleto + ' '+LinkS



        else:
            #print ('No se encontró el tipo de foco buscado')
            #Por la falta de información se usa un estandar en consumo LED y no se pone link
            TextoCompleto = TextoCompleto #+ '. Foco tipo '+ENTY[0]+' con entrada '+ENTY[0]
            if Tecno == 'fluorescente':
                TT = 40
            if Tecno == 'incandescente':
                TT = 70
            if Tecno == 'halogena':
                TT = 60
            if Tecno == 'halogenos':
                TT = 60
            TextoCompleto = TextoCompleto.replace('del [T]%', 'alrededor del [T]%')
            TextoCompleto = TextoCompleto.replace('[T]', str(round(TT, 1)))
    #
    #
    # # Lo que pasa si el foco no está especificado en términos de tecnología.
    # else:
    #     TextoCompleto = TextoCompleto+'. No existe información suficiente para una recomendación'

    TextoCompleto=recoTuboFluorescente(tex,Numero,DAC,Watts,VV,texto,TextoCompleto)
    #TextoSensor=TextoSensor.replace('X','')
    TextoCompleto = TextoCompleto + '' +TextoSolar
    #TextoCompleto = TextoCompleto + '' +TextoSensor


    if 'DACCS' in tex:
        TextoCompleto = TextoCompleto+ Lib.loc['LUM06b', 'Texto']

    TextoCompleto = TextoCompleto.replace('[...]','')
    TextoCompleto = TextoCompleto.replace('[/n]','<br />')






    return TextoCompleto, conteoled, conteoNOled, conteoROI


## 5.
## Función para buscar el sustituto LED
def BuscarLED(tipo,entrada,potencia,color,dim,intel,fila,tec,numero): # Esta función se jala desde PDF.py
    ## Se lee la base de datos
    LIB = libreriaLED() # ESTA CREO QUE ESTA DECLARADA SOLO COM 'Libreria' EN LA FUNCION QUE LA IMPORTA
    ## Para buscar por potencia equivalente se  usa un rango de +-20% en el foco orginal
    mx=(potencia+(potencia*0.4))
    mn=(potencia-(potencia*0.2))/numero
    LIB=LIB.fillna(0)
    ## Se va filtrando la base de datos con la información del excel y se elige la opción TOP choice
    Filtro1 = LIB.loc[LIB['F'] == tipo]
    Filtro2 = Filtro1.loc[Filtro1['G'] == entrada]
    if tec=='fluorescente':
        Filtro3 = Filtro2[Filtro2['J'] < mx]
        Filtro4 = Filtro3[Filtro3['J'] > mn]
    else:
        Filtro3 = Filtro2[Filtro2['I'] < mx]# Parece estar aquí el error de que no encontraba focos porque H se refiere a la potencia en LED, no en equivalente halógeno/incandescente.
        Filtro4 = Filtro3[Filtro3['I'] > mn] # Parece estar aquí el error de que no encontraba focos

    # Filtro5 = Filtro4.loc[Filtro4['M'] == color]
    # Filtro6 = Filtro5.loc[Filtro5['O'] == dim]
    # Filtro7 = Filtro6.loc[Filtro6['Q'] == intel]
    # Filtro8 = Filtro7.loc[Filtro7['P'] == fila]
    Filtro = Filtro4.loc[Filtro4['AA'] =='Top choice']

    if not Filtro.empty:
        return Filtro['H'].values[0],Filtro['W'].values[0],Filtro['V'].values[0] # Regresa 1) Potencia en LED ('conLED'), 2) Precio, y 3) Link de compra

    else:
        return 0, 0, ''




## 6.
## Función para adecuar las caracteristicas para ser filtradas por BuscarLED().
def Caracteristicas(tex):
    Car1 = ''
    Car2 = ''
    Car3 = ''
    Car4 = ''

    if 'cálida' in tex:
        Car1 = 'Cálida'
    elif 'fria' in tex:
        Car1 = 'Fria'
    else:
        Car1 = 'No'

    if 'dimeable' in tex:
        Car2 = 'Dimeable'
    else:
        Car2 = 'No'

    if 'inteligente' in tex:
        Car3 = 'Inteligente'
    else:
        Car3 = 'No'

    if 'filamento' in tex:
        Car4 = 'Filamento'
    else:
        Car4 = 'No'

    return  Car1, Car2, Car3, Car4


## 7.
## Función para adecuar las variables de entrada y tipo de entrada para ser filtradas por BuscarLED()
def DiccionarioLuz(entrada):
    salida = entrada
    if entrada=='gu_5_3':
        salida='GU5.3'
    if entrada == 'mr16':
        salida = 'MR16'
    if entrada == 'e26_27':
        salida = 'E26'
    if entrada == 'e11_12':
        salida = 'E12'
    if entrada == 'e27':
        salida = 'E26'
    if entrada == 'a19':
        salida = 'A19'
    if entrada == 'par20':
        salida = 'PAR20'
    if entrada == 'vela':
        salida = 'Vela'
    if entrada == 'e10':
        salida = 'E10'
    return salida

def Horaszona(nombre,horas):
    mucho=False
    if 'rec' in nombre:
        if horas> 5.5:
            mucho='true'
    if 'sala' in nombre:
        if horas> 4:
            mucho='true'

    if 'cocina' in nombre:
        if horas> 6:
            mucho='true'

    if 'cocina' in nombre:
        if horas> 6:
            mucho='true'

    if 'rec' in nombre:
        if horas> 5.5:
            mucho='true'

    if 'sala' in nombre:
        if horas> 4:
            mucho='true'

    if 'cocina' in nombre:
        if horas> 6:
            mucho='true'

    if 'cocina' in nombre:
        if horas> 6:
            mucho='true'
    return mucho


######################################################################################################
def UnirLuces(df):
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    ## Juntar luces con mismo PP
    Pepes = pd.unique(df['B'])

    for i in Pepes:
        dfxpepes=df[df["B"] == i]
        if len(dfxpepes)>1:
            ## Checar si tienen el mismo porcentaje
            PorC = pd.unique(dfxpepes['L'])
            if len(PorC)==1:
                dfx=dfxpepes.copy()
                ## Juntar focos de tecnologías iguales
                dfx=sumariguales1(dfx,'halogena')
                dfx=sumariguales1(dfx,'incandescente')
                dfx=sumariguales1(dfx,'fluorescente')
                dfx=sumariguales1(dfx,'led')


                ## Asignar los porcentajes por tecnología
                dfx = distporc(dfx)

                ## Separar y asignar los porcentajes por tecnología
                df=separatecno(df,dfxpepes,dfx,'halogena')
                df=separatecno(df,dfxpepes,dfx,'incandescente')
                df=separatecno(df,dfxpepes,dfx,'fluorescente')
                df=separatecno(df,dfxpepes,dfx,'led')


    zonas=pd.unique(df['E'])
    for i in zonas:
        dfxzona=df[df["E"] == i]
        df,dfxzona=sumariguales(dfxzona,df,'halogena')
        df,dfxzona=sumariguales(dfxzona,df,'incandescente')
        df,dfxzona=sumariguales(dfxzona,df,'fluorescente')
        df,dfxzona=sumariguales(dfxzona,df,'led')
        dfxzona=df[df["E"] == i]
        sumazona=dfxzona['L'].sum()
        sumaDzona=dfxzona['M'].sum()

        for j in dfxzona['A'].index:
            df.loc[j,"Y"] =sumaDzona
            df.loc[j,"Z"] =sumazona

    return df


def separatecno(df,dfxpepes,dfx,tipo):
    tipoxpepes=dfxpepes[dfxpepes['A'].str.contains(tipo)]
    tipox=dfx[dfx['A'].str.contains(tipo)]


    if len(tipoxpepes)>1:
        separado1=tipox.A.str.split(expand=True)
        numT=separado1[0]
        porcentajeT=float(tipox['L'])

        for k in tipoxpepes.index:
            separado2=tipoxpepes.A.str.split(expand=True)
            numsep=int(separado2.loc[k,0])/int(numT)
            df.loc[k,'L']=numsep*porcentajeT
    else:

        for k in tipox.index:
            df.loc[k,'L']=dfx.loc[k,'L']


    return df


def sumariguales1(dflocal,tipo):
    tipoxzona=dflocal[dflocal['A'].str.contains(tipo)]
    if len(tipoxzona) >1:
        dff=tipoxzona.A.str.split(expand=True)
        dff[0] = dff[0].astype(int)
        sumaFocos=dff[0].sum()
        nuevototal= str(sumaFocos) +' '+  str(tipo)
        primero=True
        for j in tipoxzona['A'].index:
            if primero==False:
                dflocal.drop(index=j,inplace=True)
            else:
                dflocal.loc[j,'A']=nuevototal
            primero=False

    return dflocal

#### Sumar los focos de la misma tecnología por zona
def sumariguales(dfxzona,df,tipo):
    tipoxzona=dfxzona[dfxzona['A'].str.contains(tipo)]
    if len(tipoxzona) >1:
        dff=tipoxzona.A.str.split(expand=True)
        dff[0] = dff[0].astype(int)
        sumaFocos=dff[0].sum()
        sumaPor=tipoxzona['L'].sum()
        sumakWh=tipoxzona['K'].sum()
        sumaDin=tipoxzona['M'].sum()
        nuevototal= str(sumaFocos) +' '+  str(tipo)
        primero=True
        for j in tipoxzona['A'].index:
            if primero==False:
                df.drop(index=j,inplace=True)
                dfxzona.drop(index=j,inplace=True)
            else:
                df.loc[j,'A']=nuevototal
                df.loc[j,'L']=sumaPor
                df.loc[j,'K']=sumakWh
                df.loc[j,'M']=sumaDin
            primero=False
    return df, dfxzona

### Distribuir los porcentajes
def distporc(dfx):
    NI=0
    NF=0
    NH=0
    NL=0
    Por=0
    for i in dfx.index:
        dff=dfx.loc[i,'A'].split()
        if 'inc' in dff[1]:
            NI=int(dff[0])
        if 'led' in dff[1]:
            NL=int(dff[0])
        if 'hal' in dff[1]:
            NH=int(dff[0])
        if 'fluo' in dff[1]:
            NF=int(dff[0])
        Por=float(dfx.loc[i,'L'])
        kWh=float(dfx.loc[i,'K'])
        Din=float(dfx.loc[i,'M'])
    SumL=0
    if NL>0:
        SumL= SumL+(NL)
    if NH>0:
        SumL= SumL+((NH)*7)
    if NI>0:
        SumL= SumL+((NI)*8)
    if NF>0:
        SumL= SumL+((NF)*4)

    if NL>0:
        L=NL/SumL
        KL=(kWh*L)
        ML=(Din*L)
        L=(L*Por)
    if NH>0:
        H=7*NH/SumL
        KH=(kWh*H)
        MH=(Din*H)
        H=(H*Por)
    if NI>0:
        I=8*NI/SumL
        KI=(kWh*I)
        MI=(Din*I)
        I=(I*Por)
    if NF>0:
        F=4*NF/SumL
        KF=(kWh*F)
        MF=(Din*F)
        F=(F*Por)

    for i in dfx.index:
        dff=dfx.loc[i,'A'].split()
        if 'inc' in dff[1]:
            dfx.loc[i,'L']=I
            dfx.loc[i,'K']=KI
            dfx.loc[i,'M']=MI
        if 'led' in dff[1]:
            dfx.loc[i,'L']=L
            dfx.loc[i,'K']=KL
            dfx.loc[i,'M']=ML
        if 'hal' in dff[1]:
            dfx.loc[i,'L']=H
            dfx.loc[i,'K']=KH
            dfx.loc[i,'M']=MH
        if 'fl' in dff[1]:
            dfx.loc[i,'L']=F
            dfx.loc[i,'K']=KF
            dfx.loc[i,'M']=MF
    return(dfx)

def distporc1(dfx,df):
    if len(dfx) >1:
        NI=0
        NF=0
        NH=0
        NL=0
        Por=0
        for i in dfx.index:
            dff=dfx.loc[i,'A'].split()
            if 'inc' in dff[1]:
                NI=int(dff[0])
            if 'led' in dff[1]:
                NL=int(dff[0])
            if 'hal' in dff[1]:
                NH=int(dff[0])
            if 'fluo' in dff[1]:
                NF=int(dff[0])
            Por=float(dfx.loc[i,'L'])
            kWh=float(dfx.loc[i,'K'])
            Din=float(dfx.loc[i,'M'])
        SumL=0
        if NL>0:
            SumL= SumL+(NL)
        if NH>0:
            SumL= SumL+((NH)*7)
        if NI>0:
            SumL= SumL+((NI)*8)
        if NF>0:
            SumL= SumL+((NF)*4)

        if NL>0:
            L=NL/SumL
            KL=(kWh*L)
            ML=(Din*L)
            L=(L*Por)
        if NH>0:
            H=7*NH/SumL
            KH=(kWh*H)
            MH=(Din*H)
            H=(H*Por)
        if NI>0:
            I=8*NI/SumL
            KI=(kWh*I)
            MI=(Din*I)
            I=(I*Por)
        if NF>0:
            F=4*NF/SumL
            KF=(kWh*F)
            MF=(Din*F)
            F=(F*Por)


        for i in dfx.index:
            dff=dfx.loc[i,'A'].split()
            if 'inc' in dff[1]:
                df.loc[i,'L']=I
                df.loc[i,'K']=KI
                df.loc[i,'M']=MI
            if 'led' in dff[1]:
                df.loc[i,'L']=L
                df.loc[i,'K']=KL
                df.loc[i,'M']=ML
            if 'hal' in dff[1]:
                df.loc[i,'L']=H
                df.loc[i,'K']=KH
                df.loc[i,'M']=MH
            if 'fl' in dff[1]:
                df.loc[i,'L']=F
                df.loc[i,'K']=KF
                df.loc[i,'M']=MF
    return(df)