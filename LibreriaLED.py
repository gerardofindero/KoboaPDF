import pandas as pd


############################# Libreria Luminarias ###################################
## Parte del programa dedicado a sacar la info de la libreria de luminarias compararla y elegir el texto correspondiente
## al excel de desciframiento


# Lee librería de luminarias.
def libreriaL():
    try:
        # Libreria = pd.read_excel(Path.home() / 'Desktop' /'ProtoLibreria Luminaria.xlsx')
        Libreria = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Iluminación/Libreria_Luminarias.xlsx")
    except:
        print("No se encuentra el archivo ")
        breakpoint()

    # Libreria = pd.read_excel(r'C:\Users\Cesar\Desktop\libreria.xlsx')
    Dicc = ['A', 'B', 'C', 'D', 'E']
    Libreria.columns = Dicc

    return Libreria





## Aquí se  eligen los primeros textos en base al la información del KOBO
def CondicionesLuces(Luminaria):
    ## Se hace una copia de los datos de luminarias sacados de kobo en la cual se va a trabajar
    ## Se hace una copia para no alterar los datos originales
    Lumi = Luminaria.copy()

    ## Se lee la libreria de luminarias
    Lib = libreriaL()

    ##Se rellenan los datos faltantes con NA en luminaria adicional (Luminaria KOBO)
    Luminaria['Adicional'].fillna('NA', inplace=True)

    ## Se resetea el indice para tener la referencia bien establecida (Luminaria KOBO)
    Luminaria.reset_index(drop=True, inplace=True)

    ## Se asignan las variables de tipo y lugar de las luminarias encontradas en KOBO
    Tipo = Luminaria['Tecnologia']
    Lugar = Luminaria['Lugar']

    ## En este FOR se analiza cada una de las luces en el KOBO y se le asiga su correspondiente texto
    for i in Luminaria.index:
        Numero = Luminaria.loc[i, 'Numero']

        ## Se asignan las variables de tipo y lugar de las luminarias encontradas en KOBO
        Tipo = Luminaria.loc[i, 'Tecnologia']
        Lugar = Luminaria.loc[i, 'Lugar']
        TextoCompleto = ''
        Car = ''
        cuantos = 0

        ## Se comparan las condiciones de las luminarias del KOBO para asignarles
        ## un texto de la libreria
        if Tipo != 'led':
            TextoCompleto = Lib.loc[32, 'E']
            Adicional = Luminaria.loc[i, 'Adicional']
            if Adicional != 'NA':
                Car = ''
                if 'calida' in Adicional:
                    Car = Car + 'luz cálida '
                    if cuantos > 0:
                        Car = Car + ','
                    cuantos = cuantos + 1
                if 'fria' in Adicional:
                    Car = Car + 'luz fría '
                    if cuantos > 0:
                        Car = Car + ','
                    cuantos = cuantos + 1
                if 'dimeable' in Adicional:
                    Car = Car + 'foco dimeable '
                    if cuantos > 0:
                        Car = Car + ','
                    cuantos = cuantos + 1
                if 'inteligente' in Adicional:
                    Car = Car + 'foco inteligente '
                    if cuantos > 0:
                        Car = Car + ','
                    cuantos = cuantos + 1

                TextoCompleto = TextoCompleto + Lib.loc[38, 'E'] + ' [ROI]'
        else:
            TextoCompleto = TextoCompleto + Lib.loc[45, 'E']

        ## Del texto se remplazan las variables dentro del texto de la libreria
        ## por las variables que se obtienen del KOBO
        TextoCompleto = TextoCompleto.replace('[Tecnologia]', Tipo)
        TextoCompleto = TextoCompleto.replace('[Lugar_iluminación]', Lugar)
        TextoCompleto = TextoCompleto.replace('[CAR]', Car)
        TextoCompleto = TextoCompleto.replace('[NUML]', str(Numero))
        TextoCompleto = TextoCompleto.replace('.0', "")
        TextoCompleto = TextoCompleto.replace('[...]', "")
        TextoCompleto = TextoCompleto.replace('Cocina', "la cocina")
        TextoCompleto = TextoCompleto.replace('Recámara', "la recámara")

        TT = TextoCompleto
        nuevo = TT.replace('[VV]', "10")
        nuevo = nuevo.replace('(s)', "")
        nuevo = nuevo.replace('(un)', "un")
        nuevo = nuevo.replace('(n)', "")
        nuevo = nuevo.replace('/n', "")
        nuevo = nuevo.replace('(es)', "")

        ##Se coloca el texto dentro de las variables del KOBO para que se escriban en Excel
        Luminaria.loc[i, 'Texto'] = nuevo

        ## Se regresa el Texto seleccionado al excel
    return Luminaria['Texto']






############################# Base de Datos de Luminarias ###############################################
## En esta parte se lee la base de datos de luminarias y se filtran las opciones hasta tener el mejor sustituto LED

## Se lee la base de datos de luminarias
def libreriaLED():
    try:
        ## Se va a la ruta donde se encuentra el archivo de excel
        Libreria = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Iluminación/Base de datos luminarias/"
            f"Base de datos_Luminarias_automatizacion.xlsx",sheet_name='Base de Datos ')
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    #Se renombran las columnas como se tienen en excel para facilitar referencia
    Dicc = ['A', 'B', 'C', 'D', 'E','F','G','H','I','J','K','L','M','N','O','P','Q','R',
            'S','T','U','V','W','X','Y','Z','AA','AB','AC']
    Libreria.columns = Dicc

    return Libreria







# Segunda parte para introducir textos de la librería de luminarias
## En esta funión se llevan a cabo los calculos para tener el % de ahorro y el ROI
## se eligen los textos correpondientes y se agregan al PDF

def variablesLuces(NumyTip, Watts,VV,tex,DAC,EntyTip):
    #Se lee libreria de textos
    Lib =  libreriaL()

    # Entrada y tipo de entrada vienen dentro de una variable, aquí se separan
    ENTY = EntyTip.split()
    # Numero y tipo (LED, Fluorecente...etc ) vienen dentro de una variable, aquí se separan
    Numero = float(NumyTip.split()[0])

    # Se buscan las caracteristicas de las luminarias según el Kobo y se adecúan para que puedan ser comparadas en
    # la base de datos de luminarias
    Car1,Car2, Car3 =Caracteristicas(tex)

    ## Para las luminarias que cuentan con entrada y tipo de entrada se busca en la base de datos de las luminarias
    ## se obtienen consumo del LED, su precio y su LINK
    try:
        #Se cambian las variables para adecuarlas a la base de datos
        tipo=ENTY[0]
        tipo = DiccionarioLuz(tipo)
        entrada=ENTY[1]
        entrada = DiccionarioLuz(entrada)

        #Se usa la función de BuscarLED para encontrar el consumo, precio y link de los equivalentes en LED
        ConLED, Precio, Link = BuscarLED(tipo, entrada, Watts,Car1,Car2,Car3)

        #Formulas
        ZZ = VV / Watts / Numero
        RR = ZZ * ConLED
        TT = RR / VV * 100
        ROI = abs((Numero * Precio) / ((VV - RR) * DAC))

        ## Se elige el texto correspondiente de la libreria de textos para el ROI correspondiente
        if ROI < 18:
            TextoROI = Lib.loc[34, 'E']
        else:
            TextoROI = Lib.loc[35, 'E']
        ## Se sustituye la variable ROI por el texto correspondiente
        TextoCompleto = tex.replace('[ROI]', TextoROI)
        TextoCompleto = TextoCompleto.replace('[ROI]', str(round(ROI, 1)))
    ## Si no se cuenta con entrada y tipo o no se encuentra nada en la base de datos no escribe ningún texto de ROI
    except:

        #Por la falta de información se usa un estandar en consumo LED y no se pone link
        ConLED = 10
        Link=' '
        ZZ = VV / Watts / Numero
        RR = ZZ * ConLED
        TT = RR / VV * 100
        TextoCompleto = tex.replace('[ROI]','')

    # Se sustituye El % de ahorro en los textos y se agrega el link
    TextoCompleto = TextoCompleto.replace('[T]', str(round(TT, 1)))
    TextoCompleto = TextoCompleto.replace('[...]', '')
    TextoCompleto = TextoCompleto+'. ' + Link


    return TextoCompleto






## Función para buscar el sustituto LED
def BuscarLED(tipo,entrada,potencia,color,dim,intel):

    ## Se lee la base de datos
    LIB = libreriaLED()

    ## para buscar por potencia se  usa un rango de +-20%
    mx=potencia+(potencia*0.2)
    mn=potencia-(potencia*0.2)

    ## Se va filtrando la base de datos con la información del excel y se elige la opción TOP choice
    Filtro1 = LIB.loc[LIB['D'] == tipo]
    Filtro2 = Filtro1.loc[Filtro1['E'] == entrada]
    Filtro3 = Filtro2.loc[(Filtro2['G'].astype(int)) < mx]
    Filtro4 = Filtro3.loc[Filtro3['G'] > mn]
    Filtro5 = Filtro4.loc[Filtro3['J'] == color]
    Filtro6 = Filtro5.loc[Filtro3['L'] == dim]
    Filtro7 = Filtro6.loc[Filtro3['O'] == intel]
    Filtro = Filtro7.loc[Filtro4['AB'] =='Top choice']

    print(Filtro['C'])

    return Filtro['F'].values[0],Filtro['R'].values[0],Filtro['Q'].values[0]







## Función para adecuar las caracteristicas para ser filtradas por BuscarLED()
def Caracteristicas(tex):
    Car1 = ''
    Car2 = ''
    Car3 = ''

    if 'cálida' in tex:
        Car1 = 'Cálida'
    if 'fria' in tex:
        Car1 = 'Blanca'

    if 'dimeable' in tex:
        Car2 = 'Si'
    else:
        Car2 = 'No'

    if 'inteligente' in tex:
        Car3 = 'Si'
    else:
        Car3 = 'No'

    return  Car1, Car2, Car3



## Función para adecuar las variables de entrada y tipo de entrada para ser filtradas por BuscarLED()
def DiccionarioLuz(entrada):
    if entrada=='gu_5_3':
        salida='GU5.3'
    if entrada == 'mr16':
        salida = 'MR16'
    if entrada == 'e26_27':
        salida = 'E26'
    if entrada == 'e11_12':
        salida = 'E12'

    return salida