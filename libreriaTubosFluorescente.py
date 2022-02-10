import pandas as pd
import numpy as np

#def recoTuboFluorescente(tipo, entr, disp, port, func, ntub, detr, difu, temp, lntb, caji, caln, plta, plnu, DAC,wt,kwh,dscr):
def recoTuboFluorescente(texto,ntub,DAC,wt,kwh,texto2,Completo):
    # :param tipo: tipo de tubo (t2, t5, t12, etc) - str
    tipo=''
    # :param entr: entrada del tubo (g5, etc) - str
    entr=''
    # :param disp: disposición de los tubo (aislado, serie, parealelo) - str
    disp=''
    # :param port: tipo de portalampara (sobresale, introduce, sin, etc) - str
    port=''
    # :param func: funcion de la iluminación (principal, nocturna, espejos etc) - str
    func=''
    # :param ntub: número de tuobos fluorescente - int o float
    ntub=0.0001
    # :param detr: Señales de deterioro en los tubos (True, False) - bool
    detr=False
    # :param difu: Si los tubos fluorescentes tienen difusor (True, False) - bool
    difu=False
    # :param temp: Tipo de iluminación (calida o fria) - str
    temp=''
    # :param lntb: longitud del tubo (largo_30, largo_61, etc) -  str
    lntb=''
    # :param caji: True si es cajillo (True, False) - bool
    caji=False
    # :param caln: longitud del cajillo - int o float
    caln=0.01
    # :param plta: lista con largo y ancho de placa ([largo, ancho]) - list de int o float
    plta=[0,0]
    # :param plnu: numero de placas - int o float
    plnu=0
    # :param DAC:
    # :param wt:
    # :param kwh:
    # :param dscr: descripcion del deciframiento. Se utiliza para extraer dias de la semana que se ocupo la luminaria
    # :return:
    # """

    dscr=texto2
    dispo=['aislado', 'serie', 'paralelo']
    funcion=['principal','indirecta','nocturna','espejos','estudio','arte','mesas','bodegas']
    temperatura=['calida','fria']
    tubo=False

    separadodiag=texto.split('/')
    for i in separadodiag:
        separarcoma=i.split(',')
        if separarcoma[0]=="T":
            tubo=True
            tipo=separarcoma[1]
            entr=separarcoma[2]

            for j in separarcoma:
                if 'largo_' in j:
                    largoT=j.replace('largo_','')
                    lntb=j
                    print(j)
                if j in dispo:
                    disp=j


                if 'PL_' in j:
                    largoT=j.replace('PL_','')
                    port=j

                if j in funcion:
                    func=j

                if j in temperatura:
                    temp=j
                    print(temp)



        if 'DET_' in i:
            soloD=i.replace('DET_','')
            if soloD=='si':
                detr=True
            else:
                detr=False

        if 'DIF_' in i:
            soloD=i.replace('DIF_','')
            if soloD=='si':
                difu=True
            else:
                difu=False

        if 'CAJ_' in i:
            soloD=i.replace('CAJ_','')
            cajillo= soloD.split('_')
            cajill = cajillo[0]
            if cajill=='si':
                caji=True
            else:
                caji=False
            caln = cajillo[1]


    if tubo==True:
        lf=libreriaTubosFluorescentes()
        print('Entra a Libreria de tubos fluorescentes')
        print("disp:" ,disp)
        lf.setData(tipo, entr, disp, port, func, ntub, detr, difu, temp, lntb, caji, caln, plta, plnu, DAC,wt,kwh,dscr)
        print("lf.detr: ",lf.detr)
        reco = lf.buildText()
        print(reco)

    else:
        reco=Completo
    return reco



class libreriaTubosFluorescentes:
    def __init__(self):
        # Kobo Info de kobo en diccionario, tarifa DAC, potencia total de los tubos led, energía consumida
        self.txt        = ''    # inicia variable del texto para el reporte al cliente
        self.sustitutos = pd.DataFrame(
            columns=['tipo', 'cantidad', 'costo', 'link', 'kwhAhorroBimestral', 'ahorroBimestral', 'roi', 'accion'])
        self.lmXwt5    = 92 * 0.93
        self.lmXwt8    = 89 * 0.90
        self.lmXwt12   = 80 * 0.78
        try:
            self.libTxt = pd.read_excel(
                f"../../../Recomendaciones de eficiencia energetica/Librerias/Iluminación/Libreria_Luminarias_.xlsx",
                sheet_name='Textos')
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
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Iluminación/Libreria_Luminarias_.xlsx",
                sheet_name='Textos')
            self.dbTubos=pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Iluminación/Base Tubos Fluorescentes Plus.xlsx",
                sheet_name='Tubo LED')
            self.dbTiras = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Iluminación/Base Tubos Fluorescentes Plus.xlsx",
                sheet_name='Tira LED')
            self.dbPanel = pd.read_excel(
                f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Iluminación/Base Tubos Fluorescentes Plus.xlsx",
                sheet_name='Panel LED')
        self.libTxt=self.libTxt.set_index('Codigo')


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
            texto = '<br />' + '<link href="' + str(link) + '"color="blue">' + str(texto) + ' </link>'
            return texto

    def setData(self,tipo, entr, disp, port, func, ntub, detr, difu, temp, lntb, caji, caln, plta, plnu,DAC,wt,kwh,dscr):
            #print("setdat detr: ", detr)
            self.tipo       = tipo
            self.entr       = entr
            self.dist       = disp
            self.port       = port
            self.func       = func
            self.ntub       = ntub
            self.detr       = detr
            self.difu       = difu
            self.temp       = temp
            self.lntb       = lntb
            self.Lntb       = float(lntb.replace("largo_",""))
            self.caji       = caji
            self.caln       = caln
            self.plta       = plta
            self.plnu       = plnu

            self.w_t        = wt                           # Potencia de la luminaria
            self.DAC        = DAC                          # Tarifa Dac vigente
            self.kwh_t      = kwh                          # kWh de la luminaria
            self.hrsUso     = kwh * 1000 / wt*60            # horas que estuvo en uso la luminaría asumiento que unicamente son tubos fluorescentes
            self.w_ff       = wt/ntub              # watts por tubo
            #self.lm_ff      = self.w_ff * self.ganLumiPro # lumenes por tubo
            #self.lm_t       = wt*self.ganLumiDes          # lumenes totales
            self.dias(dscr)                                # Detecta que dias seutilizarón degun la descripcción del deciframiento


    def RTL(self):
        print("ENTRE A REEMPALZO DE TIRA LED")
        # LUMENES POR METRO CON BASE EN LONGITUD DEL CAJILLO O LONGITUD DE LOS TUBOS
        if self.caji:
            lmXm = self.lumT/float(self.caln)
            lng  = self.caln
        else:
            #print(self.lntb, self.tubL)
            lmXm = float(self.lumT)/ (float(self.ntub)*float(self.Lntb))
            lng  = self.Lntb*self.ntub
        # FILTRO DE LUMENES POR METRO
        #selc=((self.dbTiras['Lm/m']/100)>(lmXm*0.9))&((self.dbTiras['Lm/m']/100)<(lmXm*1.35))
        selc = ((self.dbTiras['Lm/m'] / 100) > (lmXm * 0.5)) & ((self.dbTiras['Lm/m'] / 100) < (lmXm * 2.0))
        opcTir = self.dbTiras.loc[selc,:].reset_index(drop=True).copy()
        # ESTIMACIÓN DE ESPACIO FALTANTE PARA CUBRIR LA LONGITUD
        cortes=~pd.isnull(opcTir.loc[:, 'Intervalos de Corte [cm]'])
        try:
            opcTir.loc[cortes,'residuo']=\
                    lng % opcTir.loc[cortes,'Intervalos de Corte [cm]']
            opcTir.loc[~cortes,'residuo']=\
                    lng % opcTir.loc[~cortes,'Longitud Tira LED [cm]']
            # ESTIMACIÓN DE LA LONGITUD DE TIRA NECESARIA PARA OBTENER LOS W QUE USARA LA TIRA LED
            opcTir.loc[cortes, 'lonTiras'] = \
                    lng / opcTir.loc[cortes, 'Longitud Tira LED [cm]']
            opcTir.loc[~cortes, 'lonTiras'] = \
                    lng / opcTir.loc[~cortes, 'Longitud Tira LED [cm]']
            # ESTIMACION DEL NÚMERO DE TIRAS QUE DEBEN COMPRARSE
            opcTir['nTiras']=opcTir.lonTiras.apply(np.ceil)
            # AHORRO BIMESTRAL
            opcTir.loc[:,'kwhAhorroBimestral'] = (self.w_t-(opcTir.loc[:,'lonTiras']*opcTir.loc[:,'Potencia Tira LED [W]']))*24*60*self.DAC*(self.hrsUso/24/7)/1000
            opcTir.loc[:,'ahorroBimestral'   ] = opcTir.loc[:,'kwhAhorroBimestral']*self.DAC
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
                                   'kwhAhorroBimestral': opcTir['kwhAhorroBimestral'][:nSugerencias],
                                   'ahorroBimestral': opcTir['ahorroBimestral'][:nSugerencias],
                                   'roi'            : opcTir['roi'][:nSugerencias],
                                   'accion'         : (['compra']*nSugerencias)})
                # CONCATENADO DE LOS SUSTITUTOS MAS VIABLES AL DF SE SALIDA
                self.sustitutos = self.sustitutos.append(df, ignore_index=True)
            else:
                df=pd.DataFrame({'tipo'           : (['Tira LED']*5),
                                 'cantidad'       : opcTir['nTiras'][:5],
                                 'costo'          : opcTir['Costo Tira LED'][:5],
                                 'link'           : opcTir['Link Tira LED'][:5],
                                 'kwhAhorroBimestral':opcTir['kwhAhorroBimestral'][:5],
                                 'ahorroBimestral': opcTir['ahorroBimestral'][:5],
                                 'roi'            : opcTir['roi'][:5],
                                 'accion'         : (['compra']*5)})
                # CONCATENADO DE LOS SUSTITUTOS MAS VIABLES AL DF SE SALIDA
                self.sustitutos = self.sustitutos.append(df, ignore_index=True)
        except:
            print('No hay recomendacion')

    def RTbL(self):
        print("ETRE A REEMPLAZO DE TIRA TUBO LED")
        self.rec=self.dbTubos.loc[self.filtro,:].reset_index(drop=True).copy()
        kwhAhorroBimestral=(self.w_t - (self.rec.at[0, 'Potencia Tubo LED [W]'] * self.ntub))*24*60*(self.hrsUso/168)/1000
        ahorroBimestral = kwhAhorroBimestral*self.DAC
        roiRTbL=self.ntub*self.rec.at[0,'Costo Tubo LED']/ahorroBimestral/6
        self.sustitutos=self.sustitutos.append({'tipo'           :'Tubo LED',
                                                'cantidad'       : self.ntub,
                                                'costo'          : self.rec.at[0,'Costo Tubo LED'],
                                                'link'           : self.rec.at[0,'Link Tubo LED'],
                                                'kwhAhorroBimestral': kwhAhorroBimestral,
                                                'ahorroBimestral': ahorroBimestral,
                                                'roi':roiRTbL,
                                                'accion':'compra'},
                                                ignore_index=True)
        print(self.sustitutos)
    def RPL(self):
        print("ENTRE A REEMPLAZO DE PLACA LED")
        lmXp = self.lumT / self.plnu
        wXp  = self.w_t  / self.plnu
        plar = self.plta.max()
        panc = self.plta.min()
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
        #print(opcPla['Lumenes Panel [Lm]'],'\n',opcPla['Potencia Panel [W]'])
        opcPla['kwhAhorroBimestral'] = (wXp-opcPla['Potencia Panel [W]'])*24*60*(self.hrsUso/7/24)*self.plnu/1000
        opcPla['ahorro'] = opcPla *self.DAC
        opcPla['roi']    = opcPla['Costo Panel LED']*self.plnu/opcPla['ahorro']/6
        opcPla=opcPla.loc[opcPla['ahorro']>=0,:].reset_index(drop=True).copy()
        if len(opcPla) < 5:
            nSugerencias = len(opcPla)
            df = pd.DataFrame({'tipo': (['Placa LED'] * nSugerencias),
                               'cantidad': ([self.plnu] * nSugerencias),
                               'costo': opcPla['Costo Panel LED'][:nSugerencias],
                               'link': opcPla['Link Panel LED'][:nSugerencias],
                               'kwhAhorroBimestral':opcPla['kwhAhorroBimestral'][:nSugerencias],
                               'ahorroBimestral': opcPla['ahorro'][:nSugerencias],
                               'roi': opcPla['roi'][:nSugerencias],
                               'accion' : (['compra']*nSugerencias)})
            # CONCATENADO DE LOS SUSTITUTOS MAS VIABLES AL DF SE SALIDA
            self.sustitutos = self.sustitutos.append(df, ignore_index=True)
        else:
            df = pd.DataFrame({'tipo': (['Placa LED'] * 5),
                               'cantidad': ([self.plnu] * 5),
                               'costo': opcPla['Costo Panel LED'][:5],
                               'link': opcPla['Link Panel LED'][:5],
                               'kwhAhorroBimestral': opcPla['kwhAhorroBimestral'][:5],
                               'ahorroBimestral': opcPla['ahorro'][:5],
                               'roi': opcPla['roi'][:5],
                               'accion' : (['compra']*5)})
            # CONCATENADO DE LOS SUSTITUTOS MAS VIABLES AL DF SE SALIDA
            self.sustitutos = self.sustitutos.append(df, ignore_index=True)

    def recRem(self,tipRem):
        self.filtro = (self.dbTubos.Tamaño == self.tipo) & \
                      (self.dbTubos.Entrada == self.entr) & \
                      (self.dbTubos.Longitud == self.lntb) & \
                      (self.dbTubos.Color == self.temp)

        #self.lumT = (self.dbTubos.loc[self.filtro, 'Lum/W típicos']*self.w_t).iat[0]
        if   self.tipo == 't12':
            self.lumT = self.w_t * self.lmXwt12
        elif self.tipo == 't8':
            self.lumT = self.w_t * self.lmXwt8
        elif (self.tipo == 't5') or (self.tipo=='t2'):
            self.lumT = self.w_t * self.lmXwt5
        #try:
        if len(self.dbTubos.loc[self.filtro, 'Longitud'])<1:
            print("No hay un tubo led en la base de datos equivalente")
        else:
            self.tubL = float(self.dbTubos.loc[self.filtro, 'Longitud'].iat[0].replace('largo_',''))
            self.RTbL()
        # if 'RTbL' in tipRem:

        if 'RTL'  in tipRem:
           self.RTL()
        if 'RPL'  in tipRem:
           self.RPL()
        reco=self.sustitutos.sort_values(by=['roi']).reset_index(drop=True).copy().iloc[:2]
        print(reco.roi<3)
        txt=''
        if len(reco)>0 :
            print("reco")
            if (reco['roi']<=3).any():
                reco=reco.loc[reco['roi']<=3,:].reset_index(drop=True).copy()
                txt = self.libTxt.loc['LUM18','Texto']
                print("txt: reco roi<3: ", txt)
            elif (self.sustitutos['roi']<3).any() and self.detr:
                txt = self.libTxt.loc['LUM19', 'Texto']
            elif (self.sustitutos['roi']<3).any() and (not self.detr):
                txt = self.libTxt.loc['LUM20', 'Texto']

            if len(reco)==1:
                recomendacion='Te dejamos esta opción de reemplazo:'
                recomendacion = recomendacion + self.ligarTextolink(
                    reco.at[0,'tipo'],reco.at[0,'link']) + ' c/u $' + str(reco.at[0,'costo'])
                txt = txt.replace('[recomendacion]',recomendacion)
            else:
                recomendacion = 'Te dejamos estas opciones de reemplazo:'
                recomendacion = recomendacion + self.ligarTextolink(
                    reco.at[0, 'tipo'] + ' opción 1' ,reco.at[0, 'link']) + ' c/u $' + str(reco.at[0, 'costo'])
                recomendacion = recomendacion + self.ligarTextolink(
                    reco.at[1, 'tipo'] + ' opción 2' ,reco.at[1, 'link']) + ' c/u $' + str(reco.at[1, 'costo'])
                txt = txt.replace('[recomendacion]',recomendacion)

            return txt
        else:
            return '\n[NO SE ENCONTRO NINGUN SUSTITUTO VIABLE]'
        #except:
        #    print("Trone y entre al except")
        #    return '\n[NO SE ENCONTRO NINGUN SUSTITUTO VIABLE]'
    def buildText(self):
        #print("Entre a build text")
        txt=''
        if len(self.diasUso)!=0:
            # LUMN15
            txt = txt + self.libTxt.loc['LUM36','Texto']
        #print("self.diasUso: ",self.diasUso ,"txt: ", txt)
        # else:
        #     # LUM16
        #     txt = txt + self.libTxt.loc['LUM16','Texto'].replace('[horasUso]',str(int(self.hrsUso)))
        if self.detr:
            # LUM17
            txt = txt +self.libTxt.loc['LUM17','Texto']
        #print("detr: ",self.detr,"txt: ", txt)
        #print("caji: ",self.caji)
        if self.caji:
            # cajillo  True
            txt = txt + self.recRem(['RTL'])

        else:
            #print("func: ", self.func)
            # Funcion
            if self.func == 'arte':
                txt = txt + 'FUNCIÓN PRINCIMAL ES ARTE\n SOLICITO APOYO DE UN HUMANO'
            elif self.func in ['indirecta', 'espejos', 'bodegas', 'peceras']:

                txt = txt + self.recRem(['RTL','RTbL'])
            else:
                #print("funcion else")
                # Dispoisicion
                print("distribución: ", self.dist)
                if   self.dist =='serie':
                    print("dist: ", self.dist)
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
        txt= txt.replace('\n','')

        return txt

