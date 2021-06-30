import pandas as pd

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
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Iluminación/Libreria_Luminarias.xlsx")
    except:
        Libreria = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Iluminación/Libreria_Luminarias.xlsx")
    # Libreria = pd.read_excel(r'C:\Users\Cesar\Desktop\libreria.xlsx')
    Dicc = ['A', 'B', 'C', 'D', 'E'] # Define los nombres de las columnas en Excel.
    Libreria.columns = Dicc # Asigna los nombres de las columnas de Excel al data frame de Python

    return Libreria





## 2
## Esta función elige la primera sección de cada texto, en base al la información reportada en KOBO
def CondicionesLuces(Luminaria): # Luminaria aquí es la base de datos condensada de Kobo.
    ## Se hace una copia de respaldo para no alterar los datos originales. 
    Lumi = Luminaria.copy() 

    ## Se lee la libreria textos de luminarias con la función libreriaL() y se asigna a 'Lib'
    Lib = libreriaL()

    ##Se rellenan los datos faltantes con NA en luminaria adicional (Luminaria KOBO). 
    Luminaria['Adicional'].fillna('NA', inplace=True)

    ## Se resetea el indice para tener la referencia bien establecida (Luminaria KOBO).
    Luminaria.reset_index(drop=True, inplace=True)

    FraseLED=0
    ## En este ciclo FOR se analiza cada una de las luces/conjunto de luces reportadas en el KOBO y se le asiga el texto correspondiente de la librería.
    for i in Luminaria.index:
        Numero = Luminaria.loc[i, 'Numero'] # Obtiene el número de luminarias que hay de ese tipo en ese espacio específico.

        ## Se asignan las variables de tipo y lugar de las luminarias encontradas en KOBO
        Tipo = Luminaria.loc[i, 'Tecnologia'] # Obtiene la tecnologia de luminarias
        Lugar = Luminaria.loc[i, 'Lugar'] # Obtiene el lugar dónde se encuentra la luminaria.
        TextoCompleto = '' # Define la variable 'TextoCompleto' para llenar el texto que debe ir en el archivo, pero no asigna texto todavía.
        Car = '' # Va a ser el conjunto de caracterísiticas adicionales de los focos. Por ejemplo, temperatura de color, si es dimeable, si es foco inteligente.
        cuantos = 0 # Conteo de caracteristicas de focos
        
        ## Establece los textos a reportar cuando la luminaria no es LED.
        if Tipo != 'led':
            Adicional = Luminaria.loc[i, 'Adicional'] # Agrega todas las características adicionales de un tipo de foco (p. ej. dimeable, luz cálida, foco inteligente, etc...).
            if Adicional == 'NA':
                print('No se tienen datos para el reemplazo del foco de tecnología diferente a LED')
                TextoCompleto = 'NO HAY CARS'
            if Adicional != 'NA':
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
                if 'atenuable' in Adicional:
                    Car = Car + 'foco dimeable '
                    if cuantos > 0:
                        Car = Car + ','
                    cuantos = cuantos + 1
                if 'inteligente' in Adicional:
                    Car = Car + 'foco inteligente '
                    if cuantos > 0:
                        Car = Car + ','
                    cuantos = cuantos + 1 
                if 'filamento' in Adicional:
                    Car = Car + 'de filamento '
                    if cuantos > 0:
                        Car = Car + ','
                    cuantos = cuantos + 1
            TextoCompleto = Car
            
        else:
            TextoCompleto = 'Ya es LED'


        ##Se escribe el texto resultante en el condensado de Kobo.
        Luminaria.loc[i, 'Texto'] = TextoCompleto
        
        ## Se regresan los textos correspondientes como un data frame.
    return Luminaria['Texto']






## 3.
############################# Base de Datos de Luminarias ###############################################
## En esta parte se lee la base de datos de luminarias y se filtran las opciones hasta tener el mejor sustituto LED

## Se lee la base de datos de luminarias (contiene modelos, precios, características, etc...)
def libreriaLED():
    try:
        ## Se va a la ruta donde se encuentra el archivo de Excel
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







## 4.
## Segunda parte para introducir textos de la librería de luminarias
## En esta funión se llevan a cabo los calculos para tener el % de ahorro y el ROI
## se eligen los textos correpondientes.

def variablesLuces(NumyTip, Watts,VV,tex,DAC,EntyTip,Lugar,conteoNOled,conteoled, conteoROI): # Variables se jalan de archivo de Excel en pestaña Desciframiento. DE DONDE SALE 'tex'
    #Se lee libreria de textos
    Lib =  libreriaL()
    TextoCompleto = ''

    # Entrada y tipo de entrada vienen dentro de una variable, aquí se separan
    try:
        ENTY = EntyTip.split()
    except:
        ENTY= ['nada','nada']
    # Numero y tipo (LED, Fluorecente...etc ) vienen dentro de una variable, aquí se separan
    Numero = float(NumyTip.split()[0]) # Se saca el número de focos de cierto tipo
    #print('Numero de focos ' + str(Numero))
    Tecno = str(NumyTip.split()[1]) # Se saca la tecnología del tipo de foco (e.g. incandescente, halógena, etc...)
    Watts = Watts/Numero # Se sacan los watts por foco.
    #print('Potencia ' + str(Watts))
    
    # Textos al reporte cuando el foco ya es LED.

    if tex =='Ya es LED':
        if conteoled == 1:
            TextoCompleto = TextoCompleto + Lib.loc[45, 'E']
            conteoled = conteoled + 1
        elif conteoled <= 5:
            TextoCompleto = TextoCompleto + Lib.loc[45+max((conteoled-1),5), 'E']
            conteoled = conteoled + 1
            if conteoled==5:
                conteoled = 2
    
    # Texto al reporte cuando los focos NO son LED.
    elif tex !='NO HAY CARS':
        Car1,Car2,Car3,Car4 = Caracteristicas(tex) # Se buscan las caracteristicas de las luminarias según el Kobo y se adecúan para que puedan ser comparadas en
        # la base de datos de luminarias
        # Imprimir en pantalla características de focos
        #print('Temperatura de color: ' + str(Car1))
        #print('Dimeable: ' + str(Car2))
        #print('Inteligente: ' + str(Car3))
        #print('Filamento: ' + str(Car4))
        if conteoNOled == 1:
            TextoCompleto = Lib.loc[32, 'E']
            conteoNOled  = conteoNOled + 1
        else:
            TextoCompleto = Lib.loc[33, 'E']
        
        # Reemplaza los 'placeholders' del texto por su valor reportado en campo (la hoja de 'Desciframiento' ya tiene estos valores.
        TextoCompleto = TextoCompleto.replace('[Tecnologia]', Tecno)
        TextoCompleto = TextoCompleto.replace('[Lugar_iluminación]', Lugar)
        TextoCompleto = TextoCompleto.replace('[CAR]', tex)
        TextoCompleto = TextoCompleto.replace('[NUML]', str(Numero))
        TextoCompleto = TextoCompleto.replace('.0', "")
        TextoCompleto = TextoCompleto.replace('[...]', "")
        TextoCompleto = TextoCompleto.replace('Cocina', "la cocina")
        TextoCompleto = TextoCompleto.replace('Recámara', "la recámara")
        
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
        
        # TEXTOS DE RETORNO DE INVERSION (Seguimos con focos que no son LED).
        ## Para las luminarias que cuentan con entrada y tipo de entrada se busca en la base de datos de las luminarias
        ## se obtienen consumo del LED, su precio y su LINK
        try:
            #Se cambian las variables para adecuarlas a la base de datos
            tipo=ENTY[0]
            tipo = DiccionarioLuz(tipo) # Función definida abajo. Cambia la sintaxis de la entrada del foco oara ser igual a la de la base de datos.
            #print('Tipo: ' + str(tipo))
            entrada=ENTY[1]
            entrada = DiccionarioLuz(entrada)
            #print('Entrada tipo: ' + str(entrada))
            #Se usa la función de BuscarLED para encontrar el consumo, precio y link de los equivalentes en LED
            ConLED, Precio, Link = BuscarLED(tipo, entrada, Watts,Car1,Car2,Car3,Car4)
            
            #print('Potencia c LED: '+ str(ConLED))
            #print('Precio; '+ str(Precio))
            #print('Link: '+ Link)
            #Formulas
            TT = (1 - (ConLED / Watts))*100
            ROI = abs((Numero * Precio) / ((TT/100) * VV * DAC)) # Calcula retorno de inversion en bimestres.

            ## Se elige el texto correspondiente de la libreria de textos para el ROI correspondiente
            if ROI <= 18: # Cuando el ROI es en un periodo corto.
                TextoROI = Lib.loc[34, 'E']
            else: # Cuando el ROI no se alcanza en menos de 3 años.
                if conteoROI == 1:
                    TextoROI = Lib.loc[35, 'E']
                    conteoROI = conteoROI + 1
                elif conteoROI == 2:
                    TextoROI = Lib.loc[36, 'E']
                    conteoROI = conteoROI + 1
                elif conteoROI > 2:
                    TextoROI = Lib.loc[37, 'E']
                    
            ## Se sustituye la variable ROI por el texto correspondiente
            TextoCompleto = TextoCompleto  + TextoROI
            TextoCompleto = TextoCompleto.replace('[ROI]', str(round(ROI, 1)))
            TextoCompleto = TextoCompleto.replace('[NUML]', str(round(Numero, 0)))
            TextoCompleto = TextoCompleto.replace('[T]', str(round(TT, 1)))
            TextoCompleto = TextoCompleto.replace('[...]', '')
            TextoCompleto = TextoCompleto+'. ' + Link
                
        except:
            print ('No se encontró el tipo de foco buscado')
            #Por la falta de información se usa un estandar en consumo LED y no se pone link
            TextoCompleto = TextoCompleto + 'NO SE ENCONTRO EL TIPO DE FOCO BUSCADO'
    
    # Lo que pasa si el foco no está especificado en términos de tecnología.
    else:
        TextoCompleto = 'No existe información suficiente para una recomendación'
    

    return TextoCompleto, conteoled, conteoNOled, conteoROI





## 5.
## Función para buscar el sustituto LED
def BuscarLED(tipo,entrada,potencia,color,dim,intel,fila): # Esta función se jala desde PDF.py

    ## Se lee la base de datos
    LIB = libreriaLED() # ESTA CREO QUE ESTA DECLARADA SOLO COM 'Libreria' EN LA FUNCION QUE LA IMPORTA

    ## Para buscar por potencia equivalente se  usa un rango de +-20% en el foco orginal
    mx=potencia+(potencia*0.2)
    mn=potencia-(potencia*0.2)

    ## Se va filtrando la base de datos con la información del excel y se elige la opción TOP choice
    Filtro1 = LIB.loc[LIB['D'] == tipo]
    Filtro2 = Filtro1.loc[Filtro1['E'] == entrada]
    Filtro3 = Filtro2.loc[(Filtro2['G'].astype(int)) < mx]
    Filtro4 = Filtro3.loc[Filtro3['G'] > mn]
    Filtro5 = Filtro4.loc[Filtro4['J'] == color]
    Filtro6 = Filtro5.loc[Filtro5['L'] == dim]
    Filtro7 = Filtro6.loc[Filtro6['O'] == intel]
    Filtro8 = Filtro7.loc[Filtro7['M'] == fila]
    
    Filtro = Filtro2.loc[Filtro2['AB'] =='Top choice']



    return Filtro['F'].values[0],Filtro['R'].values[0],Filtro['Q'].values[0] # Regresa 1) Potencia en LED ('conLED'), 2) Precio, y 3) Link de compra






## 6.
## Función para adecuar las caracteristicas para ser filtradas por BuscarLED().
def Caracteristicas(tex):
    Car1 = ''
    Car2 = ''
    Car3 = ''
    Car4 = ''

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
   
    if 'filamento' in tex:
        Car4 = 'Si'
    else:
        Car4 = 'No'    

    return  Car1, Car2, Car3, Car4 


## 7.
## Función para adecuar las variables de entrada y tipo de entrada para ser filtradas por BuscarLED()
def DiccionarioLuz(entrada):
    salida = ''
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
        

    return salida