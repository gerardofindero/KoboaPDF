import pandas as pd
import Consumo
from LibreriaLED import CondicionesLuces
from LibreriaRefris import ClavesRefri
from LibreriaTV import ClavesClusterTV
from pathlib         import Path

DAC = 5.2

# 1. Leer librerías
# 1.a. Lee libreía general (primer esbozo con refrigeradores, lavadoras, secadoras, y clusters de TV)
def libreria():
    try:
        Libreria = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/TV y refris/Protolibreria.xlsx")
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    #Libreria = pd.read_excel(r'C:\Users\Cesar\Desktop\libreria.xlsx')

    return Libreria

# 1.b. Lee otra librería (ver cuál es la Protolibreria)
def libreria2():
    try:
        Libreria = pd.read_excel( f"../../../Recomendaciones de eficiencia energetica/Librerias/TV y refris/Protolibreria.xlsx")
    except:
        print("No se encuentra el archivo ")
        breakpoint()
    #Libreria = pd.read_excel(r'C:\Users\Cesar\Desktop\libreria.xlsx')

    return Libreria







def condicionesCluster(EquiposCluster,Nominal,ConsumoTotal,NumdeAparatos, Tolerancia, Multis,Voltaje):

    Lib=ClavesClusterTV(EquiposCluster)

#     Lib = pd.DataFrame(index=['Television'],
#                        columns=['Marca', 'Codigo', 'Texto'])
#
#     ConsumoTV = EquiposCluster.loc['TV', 'Standby']
#     Pulgadas  = EquiposCluster.loc['TV', 'Pulgadas']
#     Nominal = EquiposCluster.loc['TV', 'Nominal']
#
#
#     # Y = round(ConsumoTotal * 60 * 24/1000 * DAC)
#     # Z = round(Y*6)
#     #ConsumoTV = EquiposCluster.loc['TV','Consumo']
#     ##### Condiciones #########
#     Texto=" "
#     Codigo=str(Nominal) +'/'+str(ConsumoTV)+'/'+str(Pulgadas)
#
#     Libreria=libreria2()
#
#
#
#
#
#
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


def condicionesRefrigeracion(EquiposRefri):
    lib= ClavesRefri(EquiposRefri)

    # EquiposR = EquiposRefri
    # EquiposR=EquiposR.dropna(subset=['Pot Compresor'])
    # EquiposR = EquiposR.fillna(0)
    # Libreria=libreria()
    #
    # Lib = pd.DataFrame(index=['Refrigerador'],
    #                         columns=['Marca', 'Codigo', 'Texto'])
    #
    #
    #
    # for i in EquiposR.index:
    #     NominalComp = int(EquiposR['Pot Compresor'][0])
    #     TempComp = float(EquiposR['Temp Compresor'][0])
    #     TempR = (EquiposR['Temp Refri'][0])
    #     TempC = (EquiposR['Temp Conge'][0])
    #     Texto  = " "
    #     Codigo = str(TempR)+'/'+str(TempC)+'/'+ str(NominalComp) + '/'+str(TempComp)
    #     ## Compresor
    #     if NominalComp > 30:
    #         Texto1 = Libreria.loc[19, 'Texto']
    #         Texto2 = Texto1.replace("Z", str(round((NominalComp/ 130 - 1) * 100)))
    #         Texto += '\n' + Texto2.replace("Y", str(NominalComp))
    #         Codigo += ", " + Libreria.loc[19, 'Codigo']
    #
    #     #Calor
    #         if TempComp > 50:
    #             Texto1 =  Libreria.loc[14, 'Texto']
    #             Texto = Texto1.replace("X", str(EquiposRefri.loc[i,'Temp Compresor']))
    #             Texto += '\n'+Texto
    #             Codigo +=',  '+ Libreria.loc[14, 'Codigo']
    #
    #     #Ruido
    #         if 'ruido' in str(EquiposR['Prob Comp']):
    #             Texto += '\n'+Libreria.loc[15, 'Texto']
    #             Codigo +=',  '+ Libreria.loc[15, 'Codigo']
    #
    #     #Ventilador
    #         if 'ventilador' in str(EquiposR['Prob Comp']):
    #             Texto += '\n'+Libreria.loc[16, 'Texto']
    #             Codigo +=",  "+ Libreria.loc[16, 'Codigo']
    #
    #     # Ventilador
    #         if 'suciedad' in str(EquiposR['Prob Comp']):
    #             Texto += '\n'+Libreria.loc[17, 'Texto']
    #             Codigo += ",  "+Libreria.loc[17, 'Codigo']
    #     # Viejo
    #         if 'viejo' in str(EquiposR['Prob Comp']):
    #             Texto = '\n'+Texto + Libreria.loc[18, 'Texto']
    #             Codigo += ",  "+Libreria.loc[18, 'Codigo']
    #
    #
    #     #**Encendido constante
    #     # if 'abierta' in str(EquiposR['Prob Comp']):
    #     #     Texto = Libreria.loc[21, 'Texto']
    #     if EquiposR['Cierre'][0]!= 0:
    #         Texto += '\n'+Libreria.loc[20, 'Texto']
    #         Codigo += ",  "+Libreria.loc[20, 'Codigo']
    #     if EquiposR['Empaques'][0] != 0:
    #         Texto += '\n'+Libreria.loc[24, 'Texto']
    #         Codigo += ",  "+Libreria.loc[24, 'Codigo']
    #     else:
    #         Texto += '\n'+Libreria.loc[23, 'Texto']
    #         Codigo += ",  "+Libreria.loc[23, 'Codigo']
    #
    #     # #Ventilado Refri
    #     # if 'encerrado' in EquiposR['Ventilacion'][0]:
    #     #     Texto += '\n'+Libreria.loc[25, 'Texto']
    #     #     Codigo += ",  "+ Libreria.loc[25, 'Codigo']
    #     #     Texto += '\n'+ Libreria.loc[26, 'Texto']
    #     #     Codigo += ", "+ Libreria.loc[26, 'Codigo']
    #
    #
    #     #Temperatura interior
    #     if -10 > EquiposR['Temp Conge'][0] >-14:
    #         Texto +=  '\n'+Libreria.loc[26, 'Texto']
    #         Codigo += ', ' + Libreria.loc[26, 'Codigo']
    #     if EquiposR['Temp Conge'][0] <-14:
    #         Texto += '\n'+ Libreria.loc[23, 'Texto']
    #         Codigo += ', ' + Libreria.loc[23, 'Codigo']
    #     # Temperatura interior
    #
    #
    #     if 3 >= TempR >= -7:
    #         Texto += '\n' + Libreria.loc[27, 'Texto']
    #         Codigo += ',  ' + Libreria.loc[27, 'Codigo']
    #     if EquiposR['Temp Refri'][0] < -8:
    #         Texto += '\n' + Libreria.loc[24, 'Texto']
    #         Codigo += ', ' + Libreria.loc[24, 'Codigo']
    #
    #     #codigo= Codigo+'/'+str(TempR)+'/'+str(TempC)+'/'+ NominalComp + '/'+TempComp
    #     marca=EquiposR['Marca'][0]
    #     Lib.loc[i,'Marca']=marca
    #     Lib.loc[i, 'Lugar'] = 'Cocina'
    #     Lib.loc[i, 'Codigo'] = Codigo
    #     Lib.loc[i, 'Texto'] = Texto
    #
    return  lib



##def condicionesRefrigeracionsolo(EquiposRefri):




    # EquiposR = EquiposRefri
    # EquiposR=EquiposR.dropna(subset=['Pot Compresor'])
    # EquiposR = EquiposR.fillna(0)
    #
    #
    # Lib = pd.DataFrame(index=['Refrigerador'],
    #                         columns=['Marca', 'Codigo', 'Texto'])
    #
    #
    # Libreria=libreria()
    #
    # Consumo=int(EquiposR.loc['Pot Compresor'][0])
    # Texto  = " "
    # Codigo = " "
    # ## Compresor
    # if Consumo > 130:
    #     Texto1 = Libreria.loc[19, 'Texto']
    #     Texto2 = Texto1.replace("Z", str(round((Consumo / 130 - 1) * 100)))
    #     Texto += '\n' + Texto2.replace("Y", str(Consumo))
    #     Codigo += ", " + Libreria.loc[19, 'Codigo']
    #
    # #Calor
    #     if float(EquiposRefri['Temp Compresor'][0])>50:
    #         Texto1 =  Libreria.loc[14, 'Texto']
    #         Texto = Texto1.replace("X", str(EquiposRefri['Temp Compresor'][0]))
    #
    #         Texto += '\n'+Texto
    #
    #         Codigo +=',  '+ Libreria.loc[14, 'Codigo']
    # #Ruido
    #     if 'ruido' in str(EquiposR['Prob Comp']):
    #         Texto += '\n'+Libreria.loc[15, 'Texto']
    #         Codigo +=',  '+ Libreria.loc[15, 'Codigo']
    #
    # #Ventilador
    #     if 'ventilador' in str(EquiposR['Prob Comp']):
    #         Texto += '\n'+Libreria.loc[16, 'Texto']
    #         Codigo +=",  "+ Libreria.loc[16, 'Codigo']
    #
    # # Ventilador
    #     if 'suciedad' in str(EquiposR['Prob Comp']):
    #         Texto += '\n'+Libreria.loc[17, 'Texto']
    #         Codigo += ",  "+Libreria.loc[17, 'Codigo']
    # # Viejo
    #     if 'viejo' in str(EquiposR['Prob Comp']):
    #         Texto = '\n'+Texto + Libreria.loc[18, 'Texto']
    #         Codigo += ",  "+Libreria.loc[18, 'Codigo']
    #
    #
    # #**Encendido constante
    # # if 'abierta' in str(EquiposR['Prob Comp']):
    # #     Texto = Libreria.loc[21, 'Texto']
    # if EquiposR['Cierre'][0]!= 0:
    #     Texto += '\n'+Libreria.loc[20, 'Texto']
    #     Codigo += ",  "+Libreria.loc[20, 'Codigo']
    # if EquiposR['Empaques'][0] != 0:
    #     Texto += '\n'+Libreria.loc[24, 'Texto']
    #     Codigo += ",  "+Libreria.loc[24, 'Codigo']
    # else:
    #     Texto += '\n'+Libreria.loc[23, 'Texto']
    #     Codigo += ",  "+Libreria.loc[23, 'Codigo']
    #
    # #Ventilado Refri
    # if EquiposR['Ventilacion'][0] != 0:
    #     Texto += '\n'+Libreria.loc[25, 'Texto']
    #     Codigo += ",  "+ Libreria.loc[25, 'Codigo']
    #     Texto += '\n'+ Libreria.loc[26, 'Texto']
    #     Codigo += ", "+ Libreria.loc[26, 'Codigo']
    #
    #
    # #Temperatura interior
    # if -10 > EquiposR['Temp Conge'][0] >-14:
    #     Texto +=  '\n'+Libreria.loc[27, 'Texto']
    #     Codigo += ', ' + Libreria.loc[27, 'Codigo']
    # if EquiposR['Temp Conge'][0] <-14:
    #     Texto += '\n'+ Libreria.loc[28, 'Texto']
    #     Codigo += ', ' + Libreria.loc[28, 'Codigo']
    # # Temperatura interior
    #
    #
    # if 3 >= (EquiposR['Temp Refri'][0]) >= -7:
    #     Texto += '\n' + Libreria.loc[29, 'Texto']
    #     Codigo += ',  ' + Libreria.loc[29, 'Codigo']
    # if EquiposR['Temp Refri'][0] < -8:
    #     Texto += '\n' + Libreria.loc[30, 'Texto']
    #     Codigo += ', ' + Libreria.loc[30, 'Codigo']
    #
    #
    # marca=EquiposR['Marca'][0]
    # Lib.loc['Equipo','Marca']=marca
    # Lib.loc['Equipo', 'Lugar'] = 'Cocina'
    # Lib.loc['Equipo', 'Codigo'] = Codigo
    # Lib.loc['Equipo', 'Texto'] = Texto
    #
    # return  Lib




def condicionesSecadora(Secadora):
    print("")


def condicionesLuces(Luminaria):
    return CondicionesLuces(Luminaria)

