import pandas as pd
from Consumo import consumoEq

def condicionesCluster(EquiposCluster,ConsumoTotal,NumdeAparatos, Tolerancia, Multis,Voltaje):
    DAC = 5.2
    Y = round(ConsumoTotal * 60 * 24/1000 * DAC)
    Z = round(Y*6)
    ConsumoTV = EquiposCluster.loc['TV','Consumo']

    ##### Condiciones ################
    Libreria = pd.read_excel(r'C:\Users\Cesar\Desktop\libreria.xlsx')
    # Para saber si tiene un cluster de TV
    if ConsumoTotal > 3:
        Texto = Libreria.loc[0, 'Texto']
        Texto1 = Texto.replace("Y","$"+str(Y))
        Texto1 = Texto1.replace("Z","$"+ str(Z))


    # Si no tiene multicontactos
    if Multis < 1:
        if NumdeAparatos >= 2:
            Texto = Libreria.loc[1, 'Texto']

    # Si necesita un regulador
    if EquiposCluster.loc['Regulador1', 'Numero'] == 1:
        if Tolerancia:
            if Voltaje:
                ConsumoR = EquiposCluster.loc['Regulador1', 'Consumo']
                ConsumoR = consumoEq(ConsumoR)
                Consumo= round(ConsumoR * 60 * 24/1000 * DAC)
                Texto = Libreria.loc[2, 'Texto']
                Texto = Texto.replace("X", "$" + str(Consumo*6))


    # Si necesita un No Break
    if EquiposCluster.loc['NoBreak', 'Numero'] == 1:
        if Voltaje:
            ConsumoR = EquiposCluster.loc['NoBreak', 'Consumo']
            ConsumoR = consumoEq(ConsumoR)
            Consumo = round(ConsumoR * 60 * 24 / 1000 * DAC)
            Texto = Libreria.loc[3, 'Texto']
            Texto = Texto.replace("X", "$" + str(Consumo * 6))

    # Aparatos de Sonido
    if EquiposCluster.loc['Sonido', 'Numero'] == 1:
        if EquiposCluster.loc['Regulador1', 'Numero'] == 1 or EquiposCluster.loc['Regulador1', 'Numero'] == 1:
            Texto = Libreria.loc[4, 'Texto']
            print(Texto)

    #Decodificador
    if EquiposCluster.loc['Regulador1', 'Numero'] == 1 or EquiposCluster.loc['Regulador1', 'Numero'] == 1:
        Texto = Libreria.loc[5, 'Texto']
    #TV
    if EquiposCluster.loc['TV', 'Numero'] == 1:

        ConsumoTV = EquiposCluster.loc['TV', 'Consumo']
        ConsumoTV = consumoEq(ConsumoTV)
        TamanoCunsumo= int(EquiposCluster.loc['TV', 'Pulgadas']) / ConsumoTV

        if EquiposCluster.loc['Regulador1', 'Numero'] == 1 or EquiposCluster.loc['Regulador1', 'Numero'] == 1:
            if Tolerancia:
                ConsumoR = EquiposCluster.loc['Regulador1', 'Consumo']
                ConsumoR = consumoEq(ConsumoR)
                Consumo = round(ConsumoR * 60 * 24 / 1000 * DAC)
                Texto = Libreria.loc[6, 'Texto']
                Texto = Texto.replace("X", "$" + str(Consumo * 6))
        #ConsumoTV
        if 5 >= ConsumoTV > 2:
            Texto = Libreria.loc[7, 'Texto']
        if 8 > ConsumoTV > 5:
            Texto = Libreria.loc[8, 'Texto']
        if ConsumoTV >= 8:
            Texto = Libreria.loc[9, 'Texto']

        #TamañoTV
        if TamanoCunsumo > 5:
            Texto = Libreria.loc[10, 'Texto']

        if TamanoCunsumo <=5 :
            Texto = Libreria.loc[11, 'Texto']
        if TamanoCunsumo <=5 :
            Texto = Libreria.loc[12, 'Texto']


        #Modem
    if EquiposCluster.loc['Modem', 'Numero'] == 1:
        Texto = Libreria.loc[13, 'Texto']


def condicionesRefrigeracion(EquiposCluster,ConsumoTotal,NumdeAparatos, Tolerancia, Multis,Voltaje):
    print("")