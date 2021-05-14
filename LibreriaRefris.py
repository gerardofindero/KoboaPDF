import pandas as pd


# 1.b. Lee otra librería (ver cuál es la Protolibreria)
def libreria2():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/TV y refris/ProtoLibreria.xlsx")
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    #Libreria = pd.read_excel(r'C:\Users\Cesar\Desktop\libreria.xlsx')

    return Libreria


def condicionesRefrigeracion(EquiposRefri):
    EquiposR = EquiposRefri
    EquiposR=EquiposR.dropna(subset=['Pot Compresor'])
    EquiposR = EquiposR.fillna(0)
    Libreria=libreria2()

    Lib = pd.DataFrame(index=['Refrigerador'],
                            columns=['Marca', 'Codigo', 'Texto'])



    for i in EquiposR.index:
        NominalComp = int(EquiposR['Pot Compresor'][0])
        TempComp = float(EquiposR['Temp Compresor'][0])
        TempR = (EquiposR['Temp Refri'][0])
        TempC = (EquiposR['Temp Conge'][0])
        Texto  = " "
        Codigo = str(TempR)+'/'+str(TempC)+'/'+ str(NominalComp) + '/'+str(TempComp)
        ## Compresor
        if NominalComp > 30:
            Texto1 = Libreria.loc[19, 'Texto']
            Texto2 = Texto1.replace("Z", str(round((NominalComp/ 130 - 1) * 100)))
            Texto += '\n' + Texto2.replace("Y", str(NominalComp))
            Codigo += ", " + Libreria.loc[19, 'Codigo']

        #Calor
            if TempComp > 50:
                Texto1 =  Libreria.loc[14, 'Texto']
                Texto = Texto1.replace("X", str(EquiposRefri.loc[i,'Temp Compresor']))
                Texto += '\n'+Texto
                Codigo +=',  '+ Libreria.loc[14, 'Codigo']

        #Ruido
            if 'ruido' in str(EquiposR['Prob Comp']):
                Texto += '\n'+Libreria.loc[15, 'Texto']
                Codigo +=',  '+ Libreria.loc[15, 'Codigo']

        #Ventilador
            if 'ventilador' in str(EquiposR['Prob Comp']):
                Texto += '\n'+Libreria.loc[16, 'Texto']
                Codigo +=",  "+ Libreria.loc[16, 'Codigo']

        # Ventilador
            if 'suciedad' in str(EquiposR['Prob Comp']):
                Texto += '\n'+Libreria.loc[17, 'Texto']
                Codigo += ",  "+Libreria.loc[17, 'Codigo']
        # Viejo
            if 'viejo' in str(EquiposR['Prob Comp']):
                Texto = '\n'+Texto + Libreria.loc[18, 'Texto']
                Codigo += ",  "+Libreria.loc[18, 'Codigo']


        #**Encendido constante
        # if 'abierta' in str(EquiposR['Prob Comp']):
        #     Texto = Libreria.loc[21, 'Texto']
        if EquiposR['Cierre'][0]!= 0:
            Texto += '\n'+Libreria.loc[20, 'Texto']
            Codigo += ",  "+Libreria.loc[20, 'Codigo']
        if EquiposR['Empaques'][0] != 0:
            Texto += '\n'+Libreria.loc[24, 'Texto']
            Codigo += ",  "+Libreria.loc[24, 'Codigo']
        else:
            Texto += '\n'+Libreria.loc[23, 'Texto']
            Codigo += ",  "+Libreria.loc[23, 'Codigo']

        # #Ventilado Refri
        # if 'encerrado' in EquiposR['Ventilacion'][0]:
        #     Texto += '\n'+Libreria.loc[25, 'Texto']
        #     Codigo += ",  "+ Libreria.loc[25, 'Codigo']
        #     Texto += '\n'+ Libreria.loc[26, 'Texto']
        #     Codigo += ", "+ Libreria.loc[26, 'Codigo']


        #Temperatura interior
        if -10 > EquiposR['Temp Conge'][0] >-14:
            Texto +=  '\n'+Libreria.loc[27, 'Texto']
            Codigo += ', ' + Libreria.loc[27, 'Codigo']
        if EquiposR['Temp Conge'][0] <-14:
            Texto += '\n'+ Libreria.loc[28, 'Texto']
            Codigo += ', ' + Libreria.loc[28, 'Codigo']
        # Temperatura interior


        if 3 >= TempR >= -7:
            Texto += '\n' + Libreria.loc[29, 'Texto']
            Codigo += ',  ' + Libreria.loc[29, 'Codigo']
        if EquiposR['Temp Refri'][0] < -8:
            Texto += '\n' + Libreria.loc[30, 'Texto']
            Codigo += ', ' + Libreria.loc[30, 'Codigo']

        #codigo= Codigo+'/'+str(TempR)+'/'+str(TempC)+'/'+ NominalComp + '/'+TempComp
        marca=EquiposR['Marca'][0]
        Lib.loc[i,'Marca']=marca
        Lib.loc[i, 'Lugar'] = 'Cocina'
        Lib.loc[i, 'Codigo'] = Codigo
        Lib.loc[i, 'Texto'] = Texto

    return  Lib

