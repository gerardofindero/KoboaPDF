import pandas as pd
import numpy as np
class libreriaTubosFluorescentes:
    def __init__(self):
        # Kobo Info de kobo en diccionario, tarifa DAC, potencia total de los tubos led, energía consumida
        self.txt        = ''    # inicia variable del texto para el reporte al cliente
        self.sustitutos = pd.DataFrame(columns=['tipo','cantidad','costo','link','ahorroBimestral','roi'])
        try:
            self.libTxt = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Iluminación/Libreria_Luminarias.xlsx",
                sheet_name='Sheet1')
            self.dbTubos=pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Iluminación/Base Tubos Fluorescentes Plus.xlsx",
                sheet_name='Tubo LED')
            self.dbTiras = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Iluminación/Base Tubos Fluorescentes Plus.xlsx",
                sheet_name='Tira LED')
            self.dbPanel = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Iluminación/Base Tubos Fluorescentes Plus.xlsx",
                sheet_name='Panel LED')
        except:
            self.libTxt = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Iluminación/Libreria_Luminarias.xlsx",
                sheet_name='Sheet1')
            self.dbTubos=pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Iluminación/Base Tubos Fluorescentes Plus.xlsx",
                sheet_name='Tubo LED')
            self.dbTiras = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Iluminación/Base Tubos Fluorescentes Plus.xlsx",
                sheet_name='Tira LED')
            self.dbPanel = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Iluminación/Base Tubos Fluorescentes Plus.xlsx",
                sheet_name='Panel LED')
        self.libTxt.columns=['A','B','C','D','E']

        columns              = self.dbTubos.loc[1,:]
        self.dbTubos         = self.dbTubos.iloc[2:,:].reset_index(drop=True).copy()
        self.dbTubos.columns = columns

        columns              = self.dbTiras.loc[1,:]
        self.dbTiras         = self.dbTiras.iloc[2:,:].reset_index(drop=True).copy()
        self.dbTiras.columns = columns

        columns              = self.dbPanel.loc[1, :]
        self.dbPanel         = self.dbPanel.iloc[2:, :].reset_index(drop=True).copy()
        self.dbPanel.columns = columns

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

    def setData(self,kobo,DAC,wt,kwh,dscr):
            self.tipo       = kobo['tipo'] # tipo de tubo               - str
            self.entr       = kobo['entr'] # conector del tubo          - str
            self.dist       = kobo['dist'] # disposición de los tubos   - str
            self.port       = kobo['port'] # tipo de portalampara       - str
            self.func       = kobo['func'] # funcion de la ilumincación - str
            self.ntub       = kobo['ntub'] # númerod de tubos           - num
            self.detr       = kobo['detr'] # deterioro                  - log
            self.difu       = kobo['difu'] # tiene difusor              - log
            self.temp       = kobo['temp'] # luz calida o fría          - str
            self.lntb       = kobo['lntb'] # longitud de los tubos      - str
            self.caji       = kobo['caji'] # cajillo                    - log
            self.caln       = kobo['caln'] # longitud del cajillo       - num (0 por default)
            self.plta       = kobo['plta'] # medidas de placa           - list num  [largo, ancho] ([0,0] por default)
            self.plnu       = kobo['plnu'] # número de placas

            self.w_t        = wt                           # Potencia de la luminaria
            self.DAC        = DAC                          # Tarifa Dac vigente
            self.kwh_t      = kwh                          # kWh de la luminaria
            self.hrsUso     = kwh * 1000 / wt              # horas que estuvo en uso la luminaría asumiento que unicamente son tubos fluorescentes
            self.w_ff       = wt/kobo['ntub']              # watts por tubo
            #self.lm_ff      = self.w_ff * self.ganLumiPro # lumenes por tubo
            #self.lm_t       = wt*self.ganLumiDes          # lumenes totales
            self.dias(dscr)                                # Detecta que dias seutilizarón degun la descripcción del deciframiento


    def RTL(self):
        # LUMENES POR METRO CON BASE EN LONGITUD DEL CAJILLO O LONGITUD DE LOS TUBOS
        if self.caji:
            lmXm = self.lumT/self.caln
        else:
            lmXm = self.lumT/ (self.ntub*self.tubL)
        # FILTRO DE LUMENES POR METRO
        #selc=((self.dbTiras['Lm/m']/100)>(lmXm*0.9))&((self.dbTiras['Lm/m']/100)<(lmXm*1.35))
        selc = ((self.dbTiras['Lm/m'] / 100) > (lmXm * 0.5)) & ((self.dbTiras['Lm/m'] / 100) < (lmXm * 2.0))
        opcTir = self.dbTiras.loc[selc,:].reset_index(drop=True).copy()
        # ESTIMACIÓN DE ESPACIO FALTANTE PARA CUBRIR LA LONGITUD
        cortes=~pd.isnull(opcTir.loc[:, 'Intervalos de Corte [cm]'])
        opcTir.loc[cortes,'residuo']=\
                self.caln % opcTir.loc[cortes,'Intervalos de Corte [cm]']
        opcTir.loc[~cortes,'residuo']=\
                self.caln % opcTir.loc[~cortes,'Longitud Tira LED [cm]']
        # ESTIMACIÓN DE LA LONGITUD DE TIRA NECESARIA PARA OBTENER LOS W QUE USARA LA TIRA LED
        opcTir.loc[cortes, 'lonTiras'] = \
                self.caln / opcTir.loc[cortes, 'Longitud Tira LED [cm]']
        opcTir.loc[~cortes, 'lonTiras'] = \
                self.caln / opcTir.loc[~cortes, 'Longitud Tira LED [cm]']
        # ESTIMACION DEL NÚMERO DE TIRAS QUE DEBEN COMPRARSE
        opcTir['nTiras']=opcTir.lonTiras.apply(np.ceil)
        # AHORRO BIMESTRAL
        opcTir.loc[:,'ahorroBimestral']= (self.w_t-(opcTir.loc[:,'lonTiras']*opcTir.loc[:,'Potencia Tira LED [W]']))*24*60*self.DAC*(self.hrsUso/24/7)/1000
        # ROI
        opcTir.loc[:,'roi']=(opcTir.nTiras*opcTir.loc[:,'Costo Tira LED'])/opcTir.loc[:,'ahorroBimestral']/6

        # SE PRIORIZA LA SELECCION DE AQUELLAS TIRAS CON ROI MENOR A 3 AÑOS
        if (opcTir.roi<=3).any():
            opcTir=opcTir.loc[opcTir.roi<=3,:].sort_values(by=['roi','residuo'])
        else:
            opcTir=opcTir.sort_values(by=['roi','residuo'])
        # FILTRO DE TIRAS QUE LES FALTARA MAS DE 10 CENTIMETROS PARA CUBRIR LA LONGITUD TOTAL
        opcTir = opcTir.loc[opcTir.residuo < 10, :].reset_index(drop=True).copy()
        # SELECCIÓN DE LAS 5 MEJORES OPCIONES CONSIDERANDO PRIMERO ROI Y LUEGO LA EXACTITUD CON LA QUE CUBRIRAN LA ZONA
        if len(opcTir)<5:
            nSugerencias=len(opcTir)
            df = pd.DataFrame({'tipo'           : (['Tira LED'] *nSugerencias ),
                               'cantidad'       : opcTir['nTiras'][:nSugerencias],
                               'costo'          : opcTir['Costo Tira LED'][:nSugerencias],
                               'link'           : opcTir['Link Tira LED'][:nSugerencias],
                               'ahorroBimestral': opcTir['ahorroBimestral'][:nSugerencias],
                               'roi'            : opcTir['roi'][:nSugerencias]})
            # CONCATENADO DE LOS SUSTITUTOS MAS VIABLES AL DF SE SALIDA
            self.sustitutos = self.sustitutos.append(df, ignore_index=True)
        else:
            df=pd.DataFrame({'tipo'           : (['Tira LED']*5),
                             'cantidad'       : opcTir['nTiras'][:5],
                             'costo'          : opcTir['Costo Tira LED'][:5],
                             'link'           : opcTir['Link Tira LED'][:5],
                             'ahorroBimestral': opcTir['ahorroBimestral'][:5],
                             'roi'            : opcTir['roi'][:5]})
            # CONCATENADO DE LOS SUSTITUTOS MAS VIABLES AL DF SE SALIDA
            self.sustitutos = self.sustitutos.append(df, ignore_index=True)

    def RTbL(self):
        self.rec=self.dbTubos.loc[self.filtro,:].reset_index(drop=True).copy()
        ahorro=(self.w_t - (self.rec.at[0, 'Potencia Tubo LED [W]'] * self.ntub))*24*60*self.DAC*(self.hrsUso/168)/1000
        roiRTbL=self.ntub*self.rec.at[0,'Costo Tubo LED']/ahorro/6
        self.sustitutos=self.sustitutos.append({'tipo'           :'Tubo LED',
                                                'cantidad'       : self.ntub,
                                                'costo'          : self.rec.at[0,'Costo Tubo LED'],
                                                'link'           : self.rec.at[0,'Link Tubo LED'],
                                                'ahorroBimestral': ahorro,
                                                'roi':roiRTbL},
                                                ignore_index=True)
    def RPL(self):
        lmXp = self.lumT / self.plnu
        wXp  = self.w_t  / self.plnu
        plar = self.plta.max()
        panc = self.plta.min()
        print(lmXp)
        print(wXp)
        if self.port == 'sobresale':
            filPla =  self.dbPanel.loc[:,'Sobresale']=='si'
        elif self.port == 'colgante':
            filPla = self.dbPanel.loc[:,'Colgar']=='si'
        elif self.port == 'introduce':
            filPla = self.dbPanel.loc[:,'Empotrar']=='si'
        filPla = filPla & (self.dbPanel['Largo Panel [cm]']==plar) & (self.dbPanel['Ancho Panel [cm]']==panc)
        #filPla = filPla & (self.dbPanel['Lumenes Panel [Lm]']>(lmXp*0.9)) & (self.dbPanel['Lumenes Panel [Lm]']<(lmXp*1.35))
        filPla = filPla & (self.dbPanel['Lumenes Panel [Lm]'] > (lmXp * 0.5)) & (self.dbPanel['Lumenes Panel [Lm]'] < (lmXp * 2))
        opcPla = self.dbPanel.loc[filPla,:].reset_index().copy()
        print(opcPla['Lumenes Panel [Lm]'],'\n',opcPla['Potencia Panel [W]'])
        opcPla['ahorro'] = (wXp-opcPla['Potencia Panel [W]'])*24*60*(self.hrsUso/7/24)*self.DAC*self.plnu/1000
        opcPla['roi']    = opcPla['Costo Panel LED']*self.plnu/opcPla['ahorro']/6
        opcPla=opcPla.loc[opcPla['ahorro']>=0,:].reset_index(drop=True).copy()
        if len(opcPla) < 5:
            nSugerencias = len(opcPla)
            df = pd.DataFrame({'tipo': (['Placa LED'] * nSugerencias),
                               'cantidad': ([self.plnu] * nSugerencias),
                               'costo': opcPla['Costo Panel LED'][:nSugerencias],
                               'link': opcPla['Link Panel LED'][:nSugerencias],
                               'ahorroBimestral': opcPla['ahorro'][:nSugerencias],
                               'roi': opcPla['roi'][:nSugerencias]})
            # CONCATENADO DE LOS SUSTITUTOS MAS VIABLES AL DF SE SALIDA
            self.sustitutos = self.sustitutos.append(df, ignore_index=True)
        else:
            df = pd.DataFrame({'tipo': (['Placa LED'] * 5),
                               'cantidad': ([self.plnu] * 5),
                               'costo': opcPla['Costo Panel LED'][:5],
                               'link': opcPla['Link Panel LED'][:5],
                               'ahorroBimestral': opcPla['ahorro'][:5],
                               'roi': opcPla['roi'][:5]})
            # CONCATENADO DE LOS SUSTITUTOS MAS VIABLES AL DF SE SALIDA
            self.sustitutos = self.sustitutos.append(df, ignore_index=True)

    def recRem(self,tipRem):
        self.filtro = (self.dbTubos.Tamaño == self.tipo) & \
                      (self.dbTubos.Entrada == self.entr) & \
                      (self.dbTubos.Longitud == self.lntb) & \
                      (self.dbTubos.Color == self.temp)
        self.lumT = (self.dbTubos.loc[self.filtro, 'Lum/W típicos']*self.w_t).iat[0]
        self.tubL = float(self.dbTubos.loc[self.filtro, 'Longitud'].iat[0].replace('largo_',''))

        # if 'RTbL' in tipRem:
        self.RTbL()
        if 'RTL'  in tipRem:
           self.RTL()
        if 'RPL'  in tipRem:
           self.RPL()
        reco=self.sustitutos.sort_values(by=['roi']).reset_index(drop=True).copy().iloc[:2]
        if len(reco)>0 :
            if (reco['roi']<=3).any():
                reco=reco.loc[reco['roi']<=3,:].reset_index(drop=True).copy()
                txt = '\n'+self.libTxt.loc[54,'E']
            elif (self.sustitutos['roi']<3).any() and self.detr:
                txt = '\n'+self.libTxt.loc[55, 'E']
            elif (self.sustitutos['roi']<3).any() and (not self.detr):
                txt = '\n'+self.libTxt.loc[56, 'E']
            if len(reco)==1:
                recomendacion='Te dejamos esta opción de reemplazo:\n'
                recomendacion = recomendacion + self.ligarTextolink(
                    reco.at[0,'tipo'],reco.at[0,'link']) + ' c/u $' + str(reco.at[0,'costo'])
                txt = txt.replace('[recomendacion]',recomendacion)
            else:
                recomendacion = 'Te dejamos estas opciones de reemplazo:\n'
                recomendacion = recomendacion + self.ligarTextolink(
                    reco.at[0, 'tipo'] + ' opción 1' ,reco.at[0, 'link']) + ' c/u $' + str(reco.at[0, 'costo'])+'\n'
                recomendacion = recomendacion + self.ligarTextolink(
                    reco.at[1, 'tipo'] + ' opción 2' ,reco.at[1, 'link']) + ' c/u $' + str(reco.at[1, 'costo'])
                txt = txt.replace('[recomendacion]',recomendacion)

            return txt
        else:
            return '\n[NO SE ENCONTRO NINGUN SUSTITUTO VIABLE]'

    def buildText(self):
        txt=''
        if len(self.diasUso)!=0:
            # LUMN15
            txt = txt + self.libTxt.loc[51,'E'].replace('[diasUso]',self.diasUso ).replace('[horasUso]',str(int(self.hrsUso)))
        else:
            # LUM16
            txt = txt + self.libTxt.loc[52,'E'].replace('[horasUso]',str(int(self.hrsUso)))
        if self.detr:
            # LUM17
            txt = txt +'\n' +self.libTxt.loc[53,'E']
        if self.caji:
            # cajillo  True
            txt = txt + self.recRem(['RTL'])
        else:
            # Funcion
            if self.func == 'arte':
                txt = txt + 'FUNCIÓN PRINCIMAL ES ARTE\n SOLICITO APOYO DE UN HUMANO'
            elif self.func in ['indirecta', 'espejos', 'bodegas', 'peceras']:
                txt = txt + self.recRem(['RTL','RTbL'])
            else:
                # Dispoisicion
                if   self.dist =='serie':
                    txt = txt + self.recRem(['RTL', 'RTbL'])
                elif self.dist =='paralelo':
                    txt = txt + self.recRem(['RTbL', 'RPL'])
                elif self.dist =='aislado':
                    # Porta lampara
                    if (self.port == 'sobresale') | (self.port == 'introduce'):
                        txt = txt + self.recRem(['RTL','RTbL'])
                    elif self.port == 'colgante':
                        txt = txt + self.recRem(['RTbL'])
                    elif self.port == 'sin':
                        txt = txt + self.recRem(['RTbL'])
        #txt= txt.replace('\n','<br />')
        self.txt = txt

