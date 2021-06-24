import pandas as pd


# 1.b. Lee otra librería (ver cuál es la Protolibreria)
def libreria2():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/TV y refris/Proto_Libreria_Refrigeradores.xlsx")
    except:
        Libreria = pd.read_excel(f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/TV y refris/Proto_Libreria_Refrigeradores.xlsx")
    Dicc = ['A', 'B', 'C', 'D', 'E'] # Define los nombres de las columnas en Excel.
    Libreria.columns = Dicc
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
        Codigo = 'R,'+str(TempR)+'/'+str(TempC)+'/'+ str(NominalComp) + '/'+str(TempComp)

        ## Compresor
        if NominalComp > 50:
            Codigo += ", CN"

        #Calor
            if TempComp > 50:
                Codigo +=', TM'

        #Ruido
            if 'ruido' in str(EquiposR['Prob Comp']):
                Codigo +=', RU'

        #Ventilador
            if 'ventilador' in str(EquiposR['Prob Comp']):
                Codigo +=", VE"

            if 'encerrado' in str(EquiposR['Ventilacion']):
                Codigo +=", VN"

        # Suciedad
            if 'suciedad' in str(EquiposR['Prob Comp']):
                Codigo += ", SU"
        # Viejo
            if 'viejo' in str(EquiposR['Prob Comp']):
                Codigo += ", VI"
        #Cierre
        if EquiposR['Cierre'][0]!= 0:

            Codigo += ", CI"

        if EquiposR['Empaques'][0] != 'si':
            Codigo += ", EB"
        else:
            Codigo += ", EM"

        #Temperatura interior
        if -10 > EquiposR['Temp Conge'][0] >-14:
            Codigo += ', TCB'
        if EquiposR['Temp Conge'][0] <-14:
            Codigo += ', TCM'
        # Temperatura interior

        if 3 >= TempR >= -7:
            Codigo += ', TRB'
        if EquiposR['Temp Refri'][0] < -8:
            Codigo += ', TRM'

    return  Codigo


def Clasifica(Claves):
    ClavesSep='N'
    if pd.notna(Claves):
        ClavesSep=Claves.split(", ")
    return ClavesSep[0]


def LeeClavesR(Claves):
    Texto=''
    lib=libreria2()

    if pd.notna(Claves):
        ClavesSep=Claves.split(",")
        Datos= ClavesSep[1].split("/")
        TRef=Datos[0]
        TCong = Datos[1]
        NomCom=Datos[2]
        TempCom=Datos[3]


        if 'EB' in Claves:
            Texto= Texto+' '+lib.loc[10,'E']+' '+lib.loc[12,'E']
        if 'EM' in Claves:
            Texto= Texto+' '+lib.loc[10,'E']+' '+lib.loc[11,'E']
        if 'TCM' in Claves:
            Texto= Texto+' '+lib.loc[13,'E']+' '+lib.loc[14,'E']
            Texto = Texto.replace('[EQQ]', 'congelador')
        if 'TCB' in Claves:
            Texto = Texto + ' ' + lib.loc[17, 'E']
        if 'TRM' in Claves:
            Texto= Texto+' '+lib.loc[13,'E']+' '+lib.loc[15,'E']
            Texto = Texto.replace('[EQQ]', 'refrigerador')
        if 'TRB' in Claves:
            Texto = Texto + ' ' + lib.loc[18, 'E']
        if 'CN' in Claves:
            Texto= Texto+' '+lib.loc[6,'E']
            Texto= Texto.replace(' [Y]',str(NomCom))
        if 'TM' in Claves:
            Texto = Texto + ' ' + lib.loc[1, 'E']
            Texto = Texto.replace('[TC]', str(TempCom))
        if 'RU' in Claves:
            Texto = Texto + ' ' + lib.loc[2, 'E']
        if 'VE' in Claves:
            Texto = Texto + ' ' + lib.loc[3, 'E']
        if 'SU' in Claves:
            Texto = Texto + ' ' + lib.loc[4, 'E']
        if 'VI' in Claves:
            Texto = Texto + ' ' + lib.loc[5, 'E']
        if 'VN' in Claves:
            Texto = Texto + ' ' + lib.loc[9, 'E']

        # Texto=Texto.replace('[/n]','<br />')
        # Address = 'Link de compra'
        # linkA = 'http://www.amazon.com.mx/'
        # LinkS = '<link href="' + linkA + '"color="blue">' + Address + ' </link>'
        # Texto = Texto + '<br /> ' + '<br /> '+ LinkS

    return Texto