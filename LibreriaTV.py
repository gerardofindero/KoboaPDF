import pandas as pd


# 1.b. Lee otra librería (ver cuál es la Protolibreria)
def libreria2():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/TV y refris/ProtoLibreriaTVs_EDM.xlsx")
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    #Libreria = pd.read_excel(r'C:\Users\Cesar\Desktop\libreria.xlsx')

    return Libreria



def condicionesCluster(EquiposCluster,Nominal,ConsumoTotal,NumdeAparatos, Tolerancia, Multis,Voltaje):
    Lib = pd.DataFrame(index=['Television'],
                       columns=['Marca', 'Codigo', 'Texto'])

    ConsumoTV = EquiposCluster.loc['TV', 'Standby']
    Pulgadas  = EquiposCluster.loc['TV', 'Pulgadas']
    Nominal = EquiposCluster.loc['TV', 'Nominal']


    Y = round(ConsumoTotal * 60 * 24/1000 * DAC)
    Z = round(Y*6)
    #ConsumoTV = EquiposCluster.loc['TV','Consumo']
    ##### Condiciones #########
    Texto=" "
    Codigo=str(Nominal) +'/'+str(ConsumoTV)+'/'+str(Pulgadas)
    Libreria=libreria2()

#     # Para saber si tiene un cluster de TV
#     if ConsumoTotal > 3:
#         Texto1 = Libreria.loc[0, 'Texto']
#         Texto2 = Texto1.replace("Y","$"+str(Y))
#         Texto += "\n"+Texto2.replace("Z","$"+ str(Z))
#         Codigo += ", " + Libreria.loc[0, 'Codigo']
#
#     # Si no tiene multicontactos
#     if Multis < 1:
#         if NumdeAparatos >= 2:
#             Texto = "\n"+ Libreria.loc[1, 'Texto']
#             Codigo += ", " + Libreria.loc[1, 'Codigo']
#
#     # Si necesita un regulador
#     if EquiposCluster.loc['Regulador1', 'Existencia'] == 1:
#         if Tolerancia:
#             if Voltaje:
#                 ConsumoR = EquiposCluster.loc['Regulador1', 'Standby']
#                 #ConsumoR = consumoEq(ConsumoR)
#                 Consumo= round(ConsumoR * 60 * 24/1000 * DAC)
#                 Texto1 = Libreria.loc[2, 'Texto']
#                 Texto = "\n"+Texto1.replace("X", "$" + str(Consumo*6))
#                 Codigo += ", " + Libreria.loc[2, 'Codigo']
#
#
#     # Si necesita un No Break
#     if EquiposCluster.loc['NoBreak', 'Existencia'] == 1:
#         if Voltaje:
#             ConsumoR = EquiposCluster.loc['NoBreak', 'Standby']
#             #ConsumoR = consumoEq(ConsumoR)
#             Consumo = round(ConsumoR * 60 * 24 / 1000 * DAC)
#             Texto1 = Libreria.loc[3, 'Texto']
#             Texto = "\n"+Texto1.replace("X", "$" + str(Consumo * 6))
#             Codigo += ", " + Libreria.loc[3, 'Codigo']
#
#     # Aparatos de Sonido
#     if EquiposCluster.loc['Sonido', 'Existencia'] == 1:
#         if EquiposCluster.loc['Regulador1', 'Existencia'] == 1 or EquiposCluster.loc['Regulador1', 'Existencia'] == 1:
#             Texto ="\n"+ Libreria.loc[4, 'Texto']
#             Codigo += ", " + Libreria.loc[4, 'Codigo']
#
#
#     #Decodificador
#     if EquiposCluster.loc['Regulador1', 'Existencia'] == 1 or EquiposCluster.loc['Regulador1', 'Existencia'] == 1:
#         Texto = "\n"+Libreria.loc[5, 'Texto']
#         Codigo += ", " + Libreria.loc[5, 'Codigo']
#     #TV
#     if EquiposCluster.loc['TV', 'Existencia'] == 1:
#
#         ConsumoTV = EquiposCluster.loc['TV', 'Standby']
#         #ConsumoTV = consumoEq(ConsumoTV)
#         if ConsumoTV!=0:
#             TamanoConsumo= int(EquiposCluster.loc['TV', 'Pulgadas']) / ConsumoTV
#         else:
#             TamanoConsumo=1
#
#         if EquiposCluster.loc['Regulador1', 'Existencia'] == 1 or EquiposCluster.loc['Regulador1', 'Existencia'] == 1:
#             if Tolerancia:
#                 ConsumoR = EquiposCluster.loc['Regulador1', 'Standby']
#                 #ConsumoR = consumoEq(ConsumoR)
#                 Consumo = round(ConsumoR * 60 * 24 / 1000 * DAC)
#                 Texto1 = Libreria.loc[6, 'Texto']
#                 Texto = "\n"+Texto1.replace("X", "$" + str(Consumo * 6))
#                 Codigo += ", " + Libreria.loc[6, 'Codigo']
#         #ConsumoTV
#         if 5 >= ConsumoTV > 2:
#             Texto = "\n"+Libreria.loc[7, 'Texto']
#             Codigo += ", " + Libreria.loc[7, 'Codigo']
#         if 8 > ConsumoTV > 5:
#             Texto ="\n"+ Libreria.loc[8, 'Texto']
#             Codigo += ", " + Libreria.loc[8, 'Codigo']
#         if ConsumoTV >= 8:
#             Texto ="\n"+ Libreria.loc[9, 'Texto']
#             Codigo += ", " + Libreria.loc[9, 'Codigo']
# ######
#         #TamañoTV
#         if TamanoConsumo > 5:
#             Texto ="\n"+ Libreria.loc[10, 'Texto']
#             Codigo += ", " + Libreria.loc[10, 'Codigo']
#
#         if TamanoConsumo <=5 :
#             Texto = "\n"+Libreria.loc[11, 'Texto']
#             Codigo += ", " + Libreria.loc[11, 'Codigo']
#         if TamanoConsumo <=5 :
#             Texto ="\n"+ Libreria.loc[12, 'Texto']
#             Codigo += ", " + Libreria.loc[12, 'Codigo']
#
#
#         #Modem
#     if EquiposCluster.loc['Modem', 'Existencia'] == 1:
#         Texto = "\n"+Libreria.loc[13, 'Texto']
#         Codigo += ", " + Libreria.loc[13, 'Codigo']
#
#     marca = EquiposCluster['Marca'][0]
#     lugar = EquiposCluster['Lugar'][0]
#     Lib.loc['Television', 'Marca'] = marca
#     Lib.loc['Television', 'Lugar'] = lugar
#     Lib.loc['Television', 'Codigo'] = Codigo
#     Lib.loc['Television', 'Texto'] = Texto
    return Lib