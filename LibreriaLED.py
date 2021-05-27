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
        print("No se encuentra el archivo ")
        breakpoint()

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

    ## Se asignan datos provenientes de Kobo a "Tipo" (tipo de luminaria: LED, halógena, incandescente, etc...) y a "Lugar" (lugar de la casa).
    Tipo = Luminaria['Tecnologia']
    Lugar = Luminaria['Lugar']
    count1 = 0 # Conteo de cuantas veces se ha usado el texto
    FraseLED=0
    ## En este ciclo FOR se analiza cada una de las luces/conjunto de luces reportadas en el KOBO y se le asiga el texto correspondiente de la librería.
    for i in Luminaria.index:
        Numero = Luminaria.loc[i, 'Numero'] # Obtiene el número de luminarias que hay de ese tipo en ese espacio específico.

        ## Se asignan las variables de tipo y lugar de las luminarias encontradas en KOBO
        Tipo = Luminaria.loc[i, 'Tecnologia'] # Obtiene la tecnologia de luminarias
        Lugar = Luminaria.loc[i, 'Lugar'] # Obtiene el lugar dónde se encuentra la luminaria.
        TextoCompleto = '' # Define la variable TextoCompleto, pero no asigna texto todavía.
        Car = '' # Va a ser el conjunto de caracterísiticas adicionales de los focos. Por ejemplo, temperatura de color, si es dimeable, si es foco inteligente.
        cuantos = 0 # Conteo de caracteristicas de focos
        
        ## Establece los textos a reportar cuando la luminaria no es LED.
        if Tipo != 'led':
            if count1 == 0:
                TextoCompleto = Lib.loc[32, 'E'] # El texto en el renglón 32 y columna 'E' de la librería corresponde a todos los focos que no son LED.
            else:
                TextoCompleto = Lib.loc[33, 'E'] # La alternativa de texto para no repetir 
            
            Adicional = Luminaria.loc[i, 'Adicional'] # Agrega todas las características adicionales de un tipo de foco (p. ej. dimeable, luz cálida, foco inteligente, etc...).
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

                TextoCompleto = TextoCompleto + Lib.loc[38, 'E'] + ' [ROI]'
                count1 = count1 + 1
        else:
            ### Se ponen diferentes frases para hacerlo ver menos robotizado
            if FraseLED == 0:
                TextoCompleto = TextoCompleto + Lib.loc[45, 'E'] # Texto que inserta si el tipo de foco ya es LED.
            else:
                TextoCompleto = TextoCompleto + Lib.loc[45+FraseLED, 'E']
                if FraseLED >= 5:
                    FraseLED=0

            FraseLED=FraseLED+1

        ## Reemplaza los 'placeholders' del texto por su valor reportado en Kobo.
        TextoCompleto = TextoCompleto.replace('[Tecnologia]', Tipo)
        TextoCompleto = TextoCompleto.replace('[Lugar_iluminación]', Lugar)
        TextoCompleto = TextoCompleto.replace('[CAR]', Car)
        TextoCompleto = TextoCompleto.replace('[NUML]', str(Numero))
        TextoCompleto = TextoCompleto.replace('.0', "")
        TextoCompleto = TextoCompleto.replace('[...]', "")
        TextoCompleto = TextoCompleto.replace('Cocina', "la cocina")
        TextoCompleto = TextoCompleto.replace('Recámara', "la recámara")

        TT = TextoCompleto
        
        # Aquí se eliminan parte de los textos. 
        nuevo = TT.replace('[VV]', "10")
        nuevo = nuevo.replace('(s)', "")
        nuevo = nuevo.replace('(un)', "un")
        nuevo = nuevo.replace('(n)', "")
        nuevo = nuevo.replace('/n', "")
        nuevo = nuevo.replace('(es)', "")

        ##Se escribe el texto resultante en el condensado de Kobo.
        Luminaria.loc[i, 'Texto'] = nuevo
        
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

def variablesLuces(NumyTip, Watts,VV,tex,DAC,EntyTip): # Variables se jalan de archivo de Excel en pestaña Desciframiento. DE DONDE SALE 'tex'
    #Se lee libreria de textos
    Lib =  libreriaL()

    # Entrada y tipo de entrada vienen dentro de una variable, aquí se separan
    try:
        ENTY = EntyTip.split()
    except:
        ENTY= ['nada','nada']
    # Numero y tipo (LED, Fluorecente...etc ) vienen dentro de una variable, aquí se separan
    Numero = float(NumyTip.split()[0]) 

    # Se buscan las caracteristicas de las luminarias según el Kobo y se adecúan para que puedan ser comparadas en
    # la base de datos de luminarias
    Car1,Car2,Car3,Car4 = Caracteristicas(tex) # Nota: esta función está definida abajo.

    ## Para las luminarias que cuentan con entrada y tipo de entrada se busca en la base de datos de las luminarias
    ## se obtienen consumo del LED, su precio y su LINK
    try:
        #Se cambian las variables para adecuarlas a la base de datos
        tipo=ENTY[0]
        tipo = DiccionarioLuz(tipo) # Función definida abajo. Cambia la sintaxis de la entrada del foco oara ser igual a la de la base de datos.
        entrada=ENTY[1]
        entrada = DiccionarioLuz(entrada)

        #Se usa la función de BuscarLED para encontrar el consumo, precio y link de los equivalentes en LED
        ConLED, Precio, Link = BuscarLED(tipo, entrada, Watts,Car1,Car2,Car3,Car4) 

        #Formulas
        TT = (1 - (ConLED / Watts / Numero))*100
        ROI = abs((Numero * Precio) / (TT * VV * DAC)) # Calcula retorno de inversion en bimestres.

        ## Se elige el texto correspondiente de la libreria de textos para el ROI correspondiente
        if ROI <= 18: 
            TextoROI = Lib.loc[34, 'E']
        else:
            TextoROI = Lib.loc[35, 'E']
        ## Se sustituye la variable ROI por el texto correspondiente
        TextoCompleto = tex.replace('[ROI]', TextoROI) # Nota: aquí '[ROI]' es el texto referente a Roi de la librería de textos, NO el valor numérico del ROI
        TextoCompleto = TextoCompleto.replace('[ROI]', str(round(ROI, 1)))
        TextoCompleto = TextoCompleto.replace('[NUML]', str(round(Numero, 0)))
    ## Si no se cuenta con entrada y tipo o no se encuentra nada en la base de datos no escribe ningún texto de ROI. SERIA BUENO PONER UN WARNING VISIBLE PARA NOSOTROS Y   ##REPORTAR COMO BUG
    except:

        #Por la falta de información se usa un estandar en consumo LED y no se pone link
        ConLED = 10 ## REALMENTE SE NECESITA REDEFINIR AQUI. YA ES EL RESULTADO DE LA FUNCION 'BuscarLED'
        Link=' '
        TT = (1 - (ConLED / Watts / Numero))*100
        TextoCompleto = tex.replace('[ROI]','')

    # Se sustituye El % de ahorro en los textos y se agrega el link
    TextoCompleto = TextoCompleto.replace('[T]', str(round(TT, 1)))
    TextoCompleto = TextoCompleto.replace('[...]', '')
    TextoCompleto = TextoCompleto+'. ' + Link


    return TextoCompleto





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
    
    Filtro = Filtro8.loc[Filtro8['AB'] =='Top choice']

    print(Filtro['C'])

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
    if entrada=='gu_5_3':
        salida='GU5.3'
    if entrada == 'mr16':
        salida = 'MR16'
    if entrada == 'e26_27':
        salida = 'E26'
    if entrada == 'e11_12':
        salida = 'E12'

    return salida
