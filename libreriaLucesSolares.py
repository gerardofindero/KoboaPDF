import pandas as pd
import funcionesComunes as fc

def recoSolares(focoFuncion = None, som = None, kwh =None,w =None,dac =None):
    """

    :param seg: Funcióndel foco si es nocturna buscara una recomendación de luz solar
    :param som: Sombreados, valore "Si" y "No". Viene de kobo y hace referencia a si hay occlusiones de luz
    :param kwh:
    :param w:
    :param dac:
    :return: texto con recomendacion
    """

    ls=libreriaLucesSolares()
    ls.setData(kwh,w,focoFuncion,som,dac)
    txt = ls.armarTxt()
    return txt


class libreriaLucesSolares():
    def __init__(self):
        try:
            self.lib = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Luces Solares/libreriaLucesSoalres.xlsx",
                sheet_name='libreriaLucesSolares')
            self.db = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Luces Solares/libreriaLucesSoalres.xlsx",
                sheet_name='dbSolares')
        except:
            self.lib = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Luces Solares/libreriaLucesSoalres.xlsx",
                sheet_name='libreriaLucesSolares')
            self.db = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Luces Solares/libreriaLucesSoalres.xlsx",
                sheet_name='dbSolares')
        self.v=False
        self.txt=""

    def val(self,kwh, w ,seg, som, dac):

        val_kwh =False
        val_w   =False
        val_seg =False
        val_som =False

        if pd.isnull(seg):
            print('seg es nulo')
        elif not isinstance(seg,str):
            print('seg no es un str')
        else:
            val_seg = True

        if pd.isnull(som):
            print('som es nulo')
        elif not isinstance(som,str):
            print('som no es un str')
        else:
            val_som = True

        if pd.isnull(kwh):
            print('kwh es nulo')
        elif not isinstance(kwh, (int, float)):
            print('kwh no es numerico')
        elif kwh<0:
            print('kwh es igual a negativo')
        else:
            val_kwh = True

        if pd.isnull(w):
            print('w es nulo')
        elif not isinstance(w, (int, float)):
            print('w no es numerico')
        elif w<0:
            print('w es igual a negativo')
        else:
            val_w=True

        if pd.isnull(dac):
            print('DAC es nulo')
        elif not isinstance(dac,(int,float)):
            print('DAC no es numerico')
        elif dac<=0:
            print('DAC menor o igual a 0')
        else:
            val_dac=True

        if val_w and val_dac and val_kwh and val_som and val_seg:
            self.v = True
        else:
            self.v = False
    def setData(self,kwh =None,w =None,seg =None,som =None,dac =None):
        self.val(kwh,w,seg,som,dac)
        if self.v:
            self.kwh=kwh
            self.w=w
            self.seg=seg
            self.som=som
            self.dac=dac
    def armarTxt(self):
        txt=""
        if (self.seg == "nocturna"):
            if self.som=="Si":
                idx = self.db.index[
                    (self.db.nombre == "Jackyled - 1000 lúmenes")|(self.db.nombre == "Richarm - 1000 lúmenes" )]
            else:
                idx = self.db.index[
                    (self.db.nombre == "Sebami -1200 lúmenes") | (self.db.nombre == "Ameritop - 800 lúmenes")]
            roi = self.db.loc[idx, "costo"] / (self.kwh * self.dac)

            if (roi<3).any():
                txt = txt+fc.selecTxt(self.lib,'LUS02')
            else:
                txt = txt+fc.selecTxt(self.lib,'LUS03')
            op0 = fc.ligarTextolink(self.db.at[idx[0],"nombre"],self.db.at[idx[0],"links"])
            op1 = fc.ligarTextolink(self.db.at[idx[1], "nombre"], self.db.at[idx[1], "links"])

            txt = txt.replace("[recomendacion]", op0+" y "+op1).replace("\n","<br />").replace("<br />","")
        self.txt=txt
        return txt

