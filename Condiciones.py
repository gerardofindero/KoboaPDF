import pandas as pd
from Consumo import consumoEq
from pathlib         import Path

def libreria():
    try:
        Libreria = pd.read_excel(Path.home() / 'Desktop' /'libreria.xlsx')
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    #Libreria = pd.read_excel(r'C:\Users\Cesar\Desktop\libreria.xlsx')

    return Libreria



def condicionesCluster(EquiposCluster,Nominal,ConsumoTotal,NumdeAparatos, Tolerancia, Multis,Voltaje):
    Lib = pd.DataFrame(index=['Television'],
                       columns=['Marca', 'Codigo', 'Texto'])
    DAC = 5.2
    Y = round(ConsumoTotal * 60 * 24/1000 * DAC)
    Z = round(Y*6)
    #ConsumoTV = EquiposCluster.loc['TV','Consumo']
    ##### Condiciones #########
    Texto=" "
    Codigo=" "

    Libreria=libreria()

    # Para saber si tiene un cluster de TV
    if ConsumoTotal > 3:
        Texto1 = Libreria.loc[0, 'Texto']
        Texto2 = Texto1.replace("Y","$"+str(Y))
        Texto += "\n"+Texto2.replace("Z","$"+ str(Z))
        Codigo += "\n " + Libreria.loc[0, 'Codigo']

    # Si no tiene multicontactos
    if Multis < 1:
        if NumdeAparatos >= 2:
            Texto = "\n"+ Libreria.loc[1, 'Texto']
            Codigo += "\n " + Libreria.loc[1, 'Codigo']

    # Si necesita un regulador
    if EquiposCluster.loc['Regulador1', 'Existencia'] == 1:
        if Tolerancia:
            if Voltaje:
                ConsumoR = EquiposCluster.loc['Regulador1', 'Consumo']
                #ConsumoR = consumoEq(ConsumoR)
                Consumo= round(ConsumoR * 60 * 24/1000 * DAC)
                Texto1 = Libreria.loc[2, 'Texto']
                Texto = "\n"+Texto1.replace("X", "$" + str(Consumo*6))
                Codigo += "\n " + Libreria.loc[2, 'Codigo']


    # Si necesita un No Break
    if EquiposCluster.loc['NoBreak', 'Existencia'] == 1:
        if Voltaje:
            ConsumoR = EquiposCluster.loc['NoBreak', 'Consumo']
            #ConsumoR = consumoEq(ConsumoR)
            Consumo = round(ConsumoR * 60 * 24 / 1000 * DAC)
            Texto1 = Libreria.loc[3, 'Texto']
            Texto = "\n"+Texto1.replace("X", "$" + str(Consumo * 6))
            Codigo += "\n " + Libreria.loc[3, 'Codigo']

    # Aparatos de Sonido
    if EquiposCluster.loc['Sonido', 'Existencia'] == 1:
        if EquiposCluster.loc['Regulador1', 'Existencia'] == 1 or EquiposCluster.loc['Regulador1', 'Existencia'] == 1:
            Texto ="\n"+ Libreria.loc[4, 'Texto']
            Codigo += "\n " + Libreria.loc[4, 'Codigo']


    #Decodificador
    if EquiposCluster.loc['Regulador1', 'Existencia'] == 1 or EquiposCluster.loc['Regulador1', 'Existencia'] == 1:
        Texto = "\n"+Libreria.loc[5, 'Texto']
        Codigo += "\n " + Libreria.loc[5, 'Codigo']
    #TV
    if EquiposCluster.loc['TV', 'Existencia'] == 1:

        ConsumoTV = EquiposCluster.loc['TV', 'Consumo']
        #ConsumoTV = consumoEq(ConsumoTV)
        if ConsumoTV!=0:
            TamanoConsumo= int(EquiposCluster.loc['TV', 'Pulgadas']) / ConsumoTV
        else:
            TamanoConsumo=1

        if EquiposCluster.loc['Regulador1', 'Existencia'] == 1 or EquiposCluster.loc['Regulador1', 'Existencia'] == 1:
            if Tolerancia:
                ConsumoR = EquiposCluster.loc['Regulador1', 'Consumo']
                #ConsumoR = consumoEq(ConsumoR)
                Consumo = round(ConsumoR * 60 * 24 / 1000 * DAC)
                Texto1 = Libreria.loc[6, 'Texto']
                Texto = "\n"+Texto1.replace("X", "$" + str(Consumo * 6))
                Codigo += "\n " + Libreria.loc[6, 'Codigo']
        #ConsumoTV
        if 5 >= ConsumoTV > 2:
            Texto = "\n"+Libreria.loc[7, 'Texto']
            Codigo += "\n " + Libreria.loc[7, 'Codigo']
        if 8 > ConsumoTV > 5:
            Texto ="\n"+ Libreria.loc[8, 'Texto']
            Codigo += "\n " + Libreria.loc[8, 'Codigo']
        if ConsumoTV >= 8:
            Texto ="\n"+ Libreria.loc[9, 'Texto']
            Codigo += "\n " + Libreria.loc[9, 'Codigo']
######
        #TamañoTV
        if TamanoConsumo > 5:
            Texto ="\n"+ Libreria.loc[10, 'Texto']
            Codigo += "\n " + Libreria.loc[10, 'Codigo']

        if TamanoConsumo <=5 :
            Texto = "\n"+Libreria.loc[11, 'Texto']
            Codigo += "\n " + Libreria.loc[11, 'Codigo']
        if TamanoConsumo <=5 :
            Texto ="\n"+ Libreria.loc[12, 'Texto']
            Codigo += "\n " + Libreria.loc[12, 'Codigo']


        #Modem
    if EquiposCluster.loc['Modem', 'Existencia'] == 1:
        Texto = "\n"+Libreria.loc[13, 'Texto']
        Codigo += "\n " + Libreria.loc[13, 'Codigo']

    marca = EquiposCluster['Marca'][0]
    Lib.loc['Television', 'Marca'] = marca
    Lib.loc['Television', 'Codigo'] = Codigo
    Lib.loc['Television', 'Texto'] = Texto
    return Lib


def condicionesRefrigeracion(EquiposRefri):
    EquiposR=EquiposRefri.fillna(0)


    Lib = pd.DataFrame(index=['Refrigerador'],
                            columns=['Marca', 'Codigo', 'Texto'])


    Libreria=libreria()
    Consumo=int(EquiposR['Pot Compresor'][0])
    Texto  = " "
    Codigo = " "
    ## Compresor
    if Consumo > 130:
        Texto1 = Libreria.loc[19, 'Texto']
        Texto2 = Texto1.replace("Z", str(round((Consumo / 130 - 1) * 100)))
        Texto += '\n' + Texto2.replace("Y", str(Consumo))
        Codigo += "\n " + Libreria.loc[19, 'Codigo']

    #Calor
        if int(EquiposRefri['Temp Compresor'][0])>50:
            Texto1 =  Libreria.loc[14, 'Texto']
            Texto = Texto1.replace("X", str(EquiposRefri['Temp Compresor'][0]))

            Texto += '\n'+Texto

            Codigo +='\n '+ Libreria.loc[14, 'Codigo']
    #Ruido
        if 'ruido' in str(EquiposR['Prob Comp']):
            Texto += '\n'+Libreria.loc[15, 'Texto']
            Codigo +='\n '+ Libreria.loc[15, 'Codigo']

    #Ventilador
        if 'ventilador' in str(EquiposR['Prob Comp']):
            Texto += '\n'+Libreria.loc[16, 'Texto']
            Codigo +="\n "+ Libreria.loc[16, 'Codigo']

    # Ventilador
        if 'suciedad' in str(EquiposR['Prob Comp']):
            Texto += '\n'+Libreria.loc[17, 'Texto']
            Codigo += "\n "+Libreria.loc[17, 'Codigo']
    # Viejo
        if 'viejo' in str(EquiposR['Prob Comp']):
            Texto = '\n'+Texto + Libreria.loc[18, 'Texto']
            Codigo += "\n "+Libreria.loc[18, 'Codigo']


    #**Encendido constante
    # if 'abierta' in str(EquiposR['Prob Comp']):
    #     Texto = Libreria.loc[21, 'Texto']
    if EquiposR['Cierre'][0]!= 0:
        Texto += '\n'+Libreria.loc[20, 'Texto']
        Codigo += "\n "+Libreria.loc[20, 'Codigo']
    if EquiposR['Empaques'][0] != 0:
        Texto += '\n'+Libreria.loc[24, 'Texto']
        Codigo += "\n "+Libreria.loc[24, 'Codigo']
    else:
        Texto += '\n'+Libreria.loc[23, 'Texto']
        Codigo += "\n "+Libreria.loc[23, 'Codigo']

    #Ventilado Refri
    if EquiposR['Ventilacion'][0] != 0:
        Texto += '\n'+Libreria.loc[25, 'Texto']
        Codigo += "\n "+ Libreria.loc[25, 'Codigo']
        Texto += '\n'+ Libreria.loc[26, 'Texto']
        Codigo += " \n"+ Libreria.loc[26, 'Codigo']


    #Temperatura interior
    if -10 > EquiposR['Temp Conge'][0] >-14:
        Texto +=  '\n'+Libreria.loc[27, 'Texto']
        Codigo += '\n ' + Libreria.loc[27, 'Codigo']
    if EquiposR['Temp Conge'][0] <-14:
        Texto += '\n'+ Libreria.loc[28, 'Texto']
        Codigo += '\n' + Libreria.loc[28, 'Codigo']
    # Temperatura interior

    if 3 >= EquiposR['Temp Refri'][0] >= -7:
        Texto += '\n' + Libreria.loc[29, 'Texto']
        Codigo += '\n ' + Libreria.loc[29, 'Codigo']
    if EquiposR['Temp Refri'][0] < -8:
        Texto += '\n' + Libreria.loc[30, 'Texto']
        Codigo += '\n' + Libreria.loc[30, 'Codigo']


    marca=EquiposR['Marca'][0]
    Lib.loc['Refrigerador','Marca']=marca
    Lib.loc['Refrigerador', 'Codigo'] = Codigo
    Lib.loc['Refrigerador', 'Texto'] = Texto
    return  Lib

def condicionesSecadora(Secadora):
    print("")