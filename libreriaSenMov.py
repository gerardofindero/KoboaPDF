import numpy as np
import pandas as pd
from scipy.stats import norm


class libreriaSensores:

    def __init__(self):
        self.txt = ''
        try:
            self.lib = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Sensores Movimiento/libreriaSensoresMovimiento.xlsx",
                sheet_name='libreriaSensoresMovimiento')
            self.stats = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Sensores Movimiento/libreriaSensoresMovimiento.xlsx",
                sheet_name='Calculadora')
        except:
            self.lib = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Sensores Movimiento/libreriaSensoresMovimiento.xlsx",
                sheet_name='libreriaSensoresMovimiento')
            self.stats = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Sensores Movimiento/libreriaSensoresMovimiento.xlsx",
                sheet_name='Calculadore')
    def setData(self, kwh, w, zona, sector):
        # self.valData(kwh, w, zona, sector)
        rec_mara_principal
        rec_mara_ni_o_s
        rec_mara_ni_a_s
        cocina
        sala
        comedor
        sala_de_tv
        estudio_oficina
        lavanderia
        recamara_servicio
        estancia
        gimnasio
        jard_n
        calle
        ba_o_de_visitas
        estacionamiento
        otro


