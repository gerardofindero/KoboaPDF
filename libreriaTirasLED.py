import pandas as pd
import numpy as np

class libreriaTirasLED:
    def __init__(self):
        self.txt = ''  # inicia variable del texto para el reporte al cliente
        self.sustitutos = pd.DataFrame(columns=['tipo', 'cantidad', 'costo', 'link', 'ahorroBimestral', 'roi'])
        try:
            self.libTxt = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Iluminación/Libreria_Luminarias.xlsx",
                sheet_name='Sheet1')
            self.dbTiras = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Iluminación/Base Tubos Fluorescentes Plus.xlsx",
                sheet_name='Tira LED')

        except:
            self.libTxt = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Iluminación/Libreria_Luminarias.xlsx",
                sheet_name='Sheet1')
            self.dbTiras = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Iluminación/Base Tubos Fluorescentes Plus.xlsx",
                sheet_name='Tira LED')

        self.libTxt.columns=['A','B','C','D','E']

        columns = self.dbTiras.loc[1, :]
        self.dbTiras = self.dbTiras.iloc[2:, :].reset_index(drop=True).copy()
        self.dbTiras.columns = columns

    def dias(self, dscr):
        dias = []
        if ('lunes' in dscr) or ('Lunes' in dscr):
            dias.append('lunes')
        if ('Martes' in dscr) or ('martes' in dscr):
            dias.append('martes')
        if ('Miercoles' in dscr) or ('miercoles' in dscr):
            dias.append('miercoles')
        if ('Jueves' in dscr) or ('jueves' in dscr):
            dias.append('jueves')
        if ('Viernes' in dscr) or ('viernes' in dscr):
            dias.append('viernes')
        if ('Sábado' in dscr) or ('sabado' in dscr) or ('Sabado' in dscr) or ('sabado' in dscr):
            dias.append('sábado')
        if ('Domingo' in dscr) or ('domingo' in dscr):
            dias.append('domingo')
        numDias = len(dias)
        txt = ''
        if numDias == 0:
            txt = ''
        elif numDias == 1:
            txt = 'el día ' + dias[0]
        elif numDias == 2:
            txt = 'los días ' + dias[0] + ' y ' + dias[1]
        elif numDias > 2:
            txt = 'los días'
            for c, dia in enumerate(dias):
                if c < (numDias - 2):
                    txt = txt + ' ' + dias[c] + ','
                elif c == (numDias - 2):
                    txt = txt + ' ' + dias[c]
                else:
                    txt = txt + ' y ' + dias[c]
        self.diasUso = txt

    def ligarTextolink(self, texto, link):
        if (link == 'nan') or (link=='') :
            return texto
        else:
            texto = '<br />' + '<link href="' + link + '"color="blue">' + texto + ' </link>'
            return texto

    def setData(self, longitud ,caracteristicas, DAC, wt, kwh, dscr):
        carac      = caracteristicas.split(',')
        if 'fria' in carac:
            filtro = self.dbTiras['Color Tira LED']=='Frio'
        elif 'calida' in carac:
            filtro = self.dbTiras['Color Tira LED']=='Calido'
        elif 'color' in carac:
            filtro = (self.dbTiras['Color Tira LED']=='RGB') | (self.dbTiras['Color Tira LED']=='Multicolor')
        #if 'atenuable' in carac:
        #    filtro = filtro & (self.dbTiras['']=='')
        #if 'sensor_movimiento' in carac:
        #    filtro = filtro & (self.dbTiras['']=='')
        #if 'inteligente' in carac:
        #    filtro = filtro & (self.dbTiras[''] == '')
        self.filtro = filtro
        self.lon    = longitud
        self.DAC    = DAC
        self.wt     = wt
        self.kwh    = kwh
        self.dias(dscr)
        self.hrsUso = kwh * 1000 / wt

    def roi(self):
        opcTir = self.dbTiras.loc[self.filtro,:].reset_index().copy()
        cortes = ~pd.isnull(opcTir.loc[:, 'Intervalos de Corte [cm]'])
        opcTir.loc[cortes, 'residuo'] = \
            self.lon % opcTir.loc[cortes, 'Intervalos de Corte [cm]']
        opcTir.loc[~cortes, 'residuo'] = \
            self.lon % opcTir.loc[~cortes, 'Longitud Tira LED [cm]']

        opcTir.loc[cortes, 'lonTiras'] = \
            self.lon / opcTir.loc[cortes, 'Longitud Tira LED [cm]']
        opcTir.loc[~cortes, 'lonTiras'] = \
            self.lon / opcTir.loc[~cortes, 'Longitud Tira LED [cm]']

        opcTir.loc[cortes, 'lonTiras'] = \
            self.lon / opcTir['Longitud Tira LED [cm]']

        opcTir['nTiras'] = opcTir.lonTiras.apply(np.ceil)

        opcTir.loc[:, 'ahorroBimestral'] =\
            (self.wt - (opcTir.loc[:, 'lonTiras'] * opcTir.loc[:, 'Potencia Tira LED [W]'])) * 24 * 60 * self.DAC * (self.hrsUso / 24 / 7) / 1000

        opcTir.loc[:, 'roi'] = \
            (opcTir.nTiras * opcTir.loc[:, 'Costo Tira LED']) / opcTir.loc[:, 'ahorroBimestral'] / 6

        if (opcTir.roi<=3).any():
            opcTir=opcTir.loc[opcTir.roi<=3,:].sort_values(by=['roi','residuo'])
        else:
            opcTir=opcTir.sort_values(by=['roi','residuo'])
        opcTir = opcTir.loc[opcTir.residuo < 10, :].reset_index(drop=True).copy()
        opcTir = opcTir.loc[opcTir.roi>0, :].reset_index(drop=True).copy()

        if len(opcTir) < 5:
            nSugerencias = len(opcTir)
            df = pd.DataFrame({'tipo': (['Tira LED'] * nSugerencias),
                               'cantidad': opcTir['nTiras'][:nSugerencias],
                               'costo': opcTir['Costo Tira LED'][:nSugerencias],
                               'link': opcTir['Link Tira LED'][:nSugerencias],
                               'ahorroBimestral': opcTir['ahorroBimestral'][:nSugerencias],
                               'roi': opcTir['roi'][:nSugerencias]})

            self.sustitutos = self.sustitutos.append(df, ignore_index=True)
        else:
            df = pd.DataFrame({'tipo': (['Tira LED'] * 5),
                               'cantidad': opcTir['nTiras'][:5],
                               'costo': opcTir['Costo Tira LED'][:5],
                               'link': opcTir['Link Tira LED'][:5],
                               'ahorroBimestral': opcTir['ahorroBimestral'][:5],
                               'roi': opcTir['roi'][:5]})

            self.sustitutos = self.sustitutos.append(df, ignore_index=True)

    def buildText(self):
        self.roi()
        txt=''
        if len(self.diasUso)!=0:
            # LUMN15
            txt = txt + self.libTxt.loc[51,'E'].replace('[diasUso]',self.diasUso ).replace('[horasUso]',str(int(self.hrsUso)))
        else:
            # LUM16
            txt = txt + self.libTxt.loc[52,'E'].replace('[horasUso]',str(int(self.hrsUso)))

        if len(self.sustitutos)>0:
            if (self.sustitutos['roi']<3).any():
                #print(txt,'\n',self.libTxt.loc[57,'E'])
                txt = txt+ ' ' + self.libTxt.loc[57,'E']
            else:
                txt = txt+ ' ' + self.libTxt.loc[58,'E']

            if len(self.sustitutos)==1:
                recomendacion = 'Te dejamos esta opción de reemplazo:\n'
                recomendacion = recomendacion + self.ligarTextolink(
                    self.sustitutos.at[0, 'tipo'], self.sustitutos.at[0, 'link']) + ' c/u $' + str(self.sustitutos.at[0, 'costo'])
                txt = txt.replace('[recomendacion]', recomendacion)
            else:
                recomendacion = 'Te dejamos estas opciones de reemplazo:\n'
                recomendacion = recomendacion + self.ligarTextolink(
                    self.sustitutos.at[0, 'tipo'] + ' opción 1' ,self.sustitutos.at[0, 'link']) + ' c/u $' + str(self.sustitutos.at[0, 'costo'])+'\n'
                recomendacion = recomendacion + self.ligarTextolink(
                    self.sustitutos.at[1, 'tipo'] + ' opción 2' ,self.sustitutos.at[1, 'link']) + ' c/u $' + str(self.sustitutos.at[1, 'costo'])
                txt = txt.replace('[recomendacion]',recomendacion)

        else:
            txt = txt + '\n[NO SE ENCONTRO NINGUN SUSTITUTO VIABLE]'

        #txt= txt.replace('\n','<br />')
        self.txt = txt