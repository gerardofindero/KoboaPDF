import pandas as pd
from Correciones import Lugar

def palabras(DT):
    DT=pd.DataFrame()
    DT=DT.replace('hal_geno','halógena')
    return DT


def iluminacion (Excel,Nocircuito):
    Aparatos_C = pd.DataFrame(index=['Incandecentes E1','Halogeno E1','Fluorecentes E1','Tira E1','LED E1',
                                     'Incandecentes E2','Halogeno E2','Fluorecentes E2','Tira E2','LED E2',
                                     'Incandecentes E3','Halogeno E3','Fluorecentes E3','Tira E3','LED E3',
                                     'Incandecentes E4','Halogeno E4','Fluorecentes E4','Tira E4','LED E4'],
                              columns=['Lugar', 'LugarEs','Fuga','Tecnologia','FugaDET','Standby'
                                       'Consumo', 'Numero','Fundidos','Total','Combinacion', 'Sobreilum',
                                       'CodigoN','CodigoS','DobCodigo','Codigo2N','Gasto','Donde','DondeDetalle',
                                       'Cajillo','Varios','TipoyTam','Entrada','Adicional','Funcion','Acceso','Cantidad',
                                       'Adecuaciones','Apagador','Notas','LargoTubo','Info','Datos','Disposicion'])
    Circuito = Excel.loc[Nocircuito]
    Columnas=Excel.columns
    InfoEquipos = Circuito[Columnas.str.contains("iluminacion", case=False)]
    lista=['incandescente','hal_geno','fluorescente','tira_led','led']
    AccesoN=['necesita_remoci_n_de_estructuras__p__ej_','con_andamios','luces_indirectas_de_dif_cil_acceso__p__e',
             'dentro_de_alberca','otro']
    AccesoS=['a_la_mano','con_escalera_mediana__1_5_m','con_escalera_larga__1_5_m']
    CodStandby  = Circuito.filter(regex='circuito_standby_codigofindero_c_i')[0]
    listaTubos=['t2','t5','t8','t12']

####Lum1

    esc=True
    j=0
    while esc==True:
        lugar, lugar_especifico, tec, fuga, fugadetalles, standby, sobreilum, notas,InfoEsc,pendiente,CodN,Consumo=escenario(InfoEquipos,j)
        tec=tec.split()
        for i in tec:
            for k in lista:
                if i==k:
                    if k=='hal_geno':
                        k='halogenos'
                    if k=='tira_led':
                        k='tira'

                    tipo=k.capitalize()
                    Esc = 'E'+ str(j+1)

                    InfoLum = InfoEsc.filter(regex=k)
                    NombreVar=tipo+' '+Esc
                    InfoLum=InfoLum.fillna('X')
                    Aparatos_C.loc[NombreVar, 'Info']          = ''
                    Aparatos_C.loc[NombreVar, 'Datos']         = ''
                    Aparatos_C.loc[NombreVar, 'Tecnologia']   = k
                    Aparatos_C.loc[NombreVar, 'Lugar']        = Lugar(lugar)
                    Aparatos_C.loc[NombreVar, 'Fuga']         = fuga
                    Aparatos_C.loc[NombreVar, 'FugaDET']      = fugadetalles
                    Aparatos_C.loc[NombreVar, 'Standby']      = standby
                    Aparatos_C.loc[NombreVar, 'Sobreilum']    = sobreilum
                    Aparatos_C.loc[NombreVar, 'Notas'] = notas

                    Aparatos_C.loc[NombreVar, 'Numero']       = InfoLum.filter(regex='numero_c_i')[0]
                    if Aparatos_C.loc[NombreVar, 'Numero']=='X':
                        Aparatos_C.loc[NombreVar, 'Numero']   =0
                    Aparatos_C.loc[NombreVar, 'Cantidad']     =str(Aparatos_C.loc[NombreVar, 'Numero'])
                    Aparatos_C.loc[NombreVar, 'Fundidos']     = InfoLum.filter(regex='fundidos')[0]
                    Aparatos_C.loc[NombreVar, 'Total']        = InfoLum.filter(regex='total')[0]
                    Aparatos_C.loc[NombreVar, 'Forma' ] = 'F'
                    Aparatos_C.loc[NombreVar, 'CodigoN'] = CodN
                    Aparatos_C.loc[NombreVar, 'CodigoS'] =CodStandby
                    Aparatos_C.loc[NombreVar, 'Consumo'] = Consumo

                    if k=='tira':
                        Aparatos_C.loc[NombreVar, 'Acceso']       = InfoLum.filter(regex='acceso')[0]

                    if k!='led' and k!='tira' :
                        Aparatos_C.loc[NombreVar, 'Donde']        = InfoLum.filter(regex='donde_c_i')[0]
                        Aparatos_C.loc[NombreVar, 'DondeDetalle'] = InfoLum.filter(regex='donde_detalle')[0]
                        Aparatos_C.loc[NombreVar, 'Cajillo']      = InfoLum.filter(regex='cajillo')[0]
                        Aparatos_C.loc[NombreVar, 'Varios']       = InfoLum.filter(regex='varios')[0]
                        Aparatos_C.loc[NombreVar, 'TipoyTam']     = InfoLum.filter(regex='tipoytam')[0]
                        if Aparatos_C.loc[NombreVar, 'TipoyTam'] == 'otro':
                            Aparatos_C.loc[NombreVar, 'TipoyTam']     = InfoLum.filter(regex='tipoytam_otro_c_i')[0]

                        if not InfoLum.filter(regex='tipoytam')[0] == 'X':
                            if InfoLum.filter(regex='tipoytam')[0] in listaTubos:
                                Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info']+',T,'
                            else:
                                Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info']+',F,'
                        Aparatos_C.loc[NombreVar, 'TipoyTam']     = InfoLum.filter(regex='tipoytam')[0]
                        if not InfoLum.filter(regex='tipoytam')[0] == 'X':
                            Aparatos_C.loc[NombreVar, 'Info']         =Aparatos_C.loc[NombreVar, 'Info']+ InfoLum.filter(regex='tipoytam')[0]


                        Aparatos_C.loc[NombreVar, 'Entrada']      = InfoLum.filter(regex='entrada')[0]
                        if Aparatos_C.loc[NombreVar, 'Entrada']      == 'otro':
                            Aparatos_C.loc[NombreVar, 'Entrada']      = InfoLum.filter(regex='entrada_otro_c_i')[0]
                        if not InfoLum.filter(regex='entrada')[0] == 'X':
                            Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info'] +','+InfoLum.filter(regex='entrada')[0]
                        Aparatos_C.loc[NombreVar, 'Adicional']    = InfoLum.filter(regex='adicional')[0]
                        if not InfoLum.filter(regex='adicional')[0] == 'X':
                            Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info'] +','+InfoLum.filter(regex='adicional')[0]
                        Aparatos_C.loc[NombreVar, 'Funcion']      = InfoLum.filter(regex='funcion')[0]
                        if not InfoLum.filter(regex='funcion')[0] == 'X':
                            Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info'] +','+InfoLum.filter(regex='funcion')[0]
                        if not InfoLum.filter(regex='color')[0] == 'X':
                            Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info'] +','+InfoLum.filter(regex='color')[0]

                        if 'cajillo' in InfoLum.filter(regex='donde_c_i')[0]:
                            Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info']+',CAJ_si_'+str(InfoLum.filter(regex='cajillo_c_i')[0])

                        if k== 'fluorescente':

                            if not InfoLum.filter(regex='disposicion')[0] == 'X':
                                Aparatos_C.loc[NombreVar, 'Disposicion']  = Aparatos_C.loc[NombreVar, 'Funcion']  +','+InfoLum.filter(regex='disposicion')[0]
                                Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info']+','+InfoLum.filter(regex='disposicion')[0]
                            if not InfoLum.filter(regex='deterioro')[0] == 'X':
                                Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info']+',DET_'+InfoLum.filter(regex='deterioro')[0]
                            if not InfoLum.filter(regex='tubos')[0]  == 'X':
                                Aparatos_C.loc[NombreVar, 'Info' ]       = Aparatos_C.loc[NombreVar, 'Info']+','+InfoLum.filter(regex='tubos')[0]
                            if not InfoLum.filter(regex='portalamp')[0]  == 'X':
                                Aparatos_C.loc[NombreVar, 'Info' ]       = Aparatos_C.loc[NombreVar, 'Info']+',PL_'+InfoLum.filter(regex='portalamp')[0]+'/'
                            if not InfoLum.filter(regex='fluorescentes_tubos_c_i')[0]  == 'X':
                                Aparatos_C.loc[NombreVar, 'Info' ]       = Aparatos_C.loc[NombreVar, 'Info']+','+InfoLum.filter(regex='fluorescentes_tubos_c_i')[0]+'/'


                        Aparatos_C.loc[NombreVar, 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
                        Aparatos_C.loc[NombreVar, 'Apagador']     = InfoLum.filter(regex='apagador')[0]
                        Aparatos_C.loc[NombreVar, 'Cantidad' ]    = str(Aparatos_C.loc[NombreVar, 'Numero'])


                        for l in range(4):
                            CantidadPL= 'portalamp'+str(l+1)+'_cantidad'
                            LargoPL   = 'portalamp'+str(l+1)+'_largo'
                            AnchoPL   = 'portalamp'+str(l+1)+'_ancho'
                            Portalamp = 'portalamp'+str(l+1)+'_c_i'
                            cantidad = 'cantidad' +str(l+1)
                            funcion  = 'funcion' +str(l+1)
                            adicional= 'adicional' +str(l+1)
                            tipoytam = 'tipoytam' +str(l+1)
                            entrada  = 'entrada' +str(l+1)
                            disposicion  = 'disposicion' +str(l+1)
                            color  = 'color' +str(l+1)
                            Ntubos = 'tubos'+str(l+1)
                            largo = 'fluorescentes_tubos'+str(l+1)

                            if not InfoLum.filter(regex=tipoytam)[0] == 'X':
                                if InfoLum.filter(regex=tipoytam)[0] in listaTubos:
                                    Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info']+',T,'
                                else:
                                    Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info']+',F,'

                            if not InfoLum.filter(regex=tipoytam)[0] == 'X':
                                Aparatos_C.loc[NombreVar, 'TipoyTam']     = Aparatos_C.loc[NombreVar, 'TipoyTam'] +','+InfoLum.filter(regex=tipoytam)[0]
                                Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info']+','+InfoLum.filter(regex=tipoytam)[0]
                            if not InfoLum.filter(regex=entrada)[0] == 'X':
                                Aparatos_C.loc[NombreVar, 'Entrada']      = Aparatos_C.loc[NombreVar, 'Entrada']  +','+InfoLum.filter(regex=entrada)[0]
                                Aparatos_C.loc[NombreVar, 'Info']=Aparatos_C.loc[NombreVar, 'Info']+','+InfoLum.filter(regex=entrada)[0]
                            if not InfoLum.filter(regex=adicional)[0] == 'X':
                                Aparatos_C.loc[NombreVar, 'Adicional']    = Aparatos_C.loc[NombreVar, 'Adicional']+','+InfoLum.filter(regex=adicional)[0]
                                Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info']+','+InfoLum.filter(regex=adicional)[0]
                            if not InfoLum.filter(regex=funcion)[0] == 'X':
                                Aparatos_C.loc[NombreVar, 'Funcion']      = Aparatos_C.loc[NombreVar, 'Funcion']  +','+InfoLum.filter(regex=funcion)[0]
                                Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info']+','+InfoLum.filter(regex=funcion)[0]
                            if not InfoLum.filter(regex=color)[0] == 'X':
                                Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info']+','+InfoLum.filter(regex=color)[0]



                            if k== 'fluorescente':
                                if not InfoLum.filter(regex=disposicion)[0] == 'X':
                                    Aparatos_C.loc[NombreVar, 'Disposicion']        = Aparatos_C.loc[NombreVar, 'Funcion']  +','+InfoLum.filter(regex=funcion)[0]
                                    Aparatos_C.loc[NombreVar, 'Info']               = Aparatos_C.loc[NombreVar, 'Info']+','+InfoLum.filter(regex=disposicion)[0]

                                if InfoLum.filter(regex=Portalamp)[0] != 'sin' :
                                    if InfoLum.filter(regex=Portalamp)[0] != 'X':
                                        Aparatos_C.loc[NombreVar, 'Portalamp']          = InfoLum.filter(regex=Portalamp)[0]
                                        Aparatos_C.loc[NombreVar, 'PortalampC']         = InfoLum.filter(regex=CantidadPL)[0]
                                        Aparatos_C.loc[NombreVar, 'PortalampL']         = InfoLum.filter(regex=LargoPL)[0]
                                        Aparatos_C.loc[NombreVar, 'PortalampA']         = InfoLum.filter(regex=AnchoPL)[0]
                                        datosPortalamp= 'PL_'+InfoLum.filter(regex=Portalamp)[0]+'_'+str(InfoLum.filter(regex=CantidadPL)[0])\
                                                        +'_'+str(InfoLum.filter(regex=LargoPL)[0])+'_'+str(InfoLum.filter(regex=AnchoPL)[0])

                                        Aparatos_C.loc[NombreVar, 'Info']               = Aparatos_C.loc[NombreVar, 'Info']+','+datosPortalamp
                                #Aparatos_C.loc[NombreVar, 'PortalampCJ']        = InfoLum.filter(regex='cajillo_c_i')[0]
                                if not InfoLum.filter(regex=largo)[0] == 'X':
                                    Aparatos_C.loc[NombreVar, 'Info']  = Aparatos_C.loc[NombreVar, 'Info']+','+InfoLum.filter(regex=largo)[0]


                            if not InfoLum.filter(regex=cantidad)[0] == 'X':
                                Aparatos_C.loc[NombreVar, 'Cantidad' ]    = str(Aparatos_C.loc[NombreVar, 'Cantidad' ])+','+str(InfoLum.filter(regex=cantidad)[0])
                            if not InfoLum.filter(regex=cantidad)[0] == 'X':
                                Aparatos_C.loc[NombreVar, 'Numero' ]    = Aparatos_C.loc[NombreVar, 'Numero' ]+InfoLum.filter(regex=cantidad)[0]

                            if Aparatos_C.loc[NombreVar, 'Info' ] != '':
                                Aparatos_C.loc[NombreVar, 'Datos' ]    = Aparatos_C.loc[NombreVar, 'Datos' ]+'/'+Aparatos_C.loc[NombreVar, 'Info' ]
                            Aparatos_C.loc[NombreVar, 'Info' ]     =''
                            Aparatos_C.loc[NombreVar, 'Datos']=Aparatos_C.loc[NombreVar, 'Datos'].replace(' ',',')
                    else:
                        Aparatos_C.loc[NombreVar, 'Datos']='YA ES LED'
                    if Aparatos_C.loc[NombreVar, 'Acceso'] in  AccesoN :
                        Aparatos_C.loc[NombreVar, 'Datos']=Aparatos_C.loc[NombreVar, 'Datos']+','+'DACCS'
        j=j+1
        if j<4:
            existencia='esce'+str(j+1)+'_existencia_c_i'
            Esce = InfoEquipos.filter(regex=existencia)


            if Esce[0] == 'si':
                esc=True
            else:
                esc=False
        else:
            esc=False

    Aparatos_C.replace('hal_geno', 'halogena',inplace=True)
    Aparatos_C['Datos'].replace('nan/,', '',inplace=True)
    Aparatos_C['Datos'].replace('////', '',inplace=True)
    Aparatos_C['Datos'].replace(",,", ',',inplace=True,regex=True)
    Aparatos_C['Datos'].replace("/,", '/',inplace=True,regex=True)
    Aparatos = Aparatos_C[Aparatos_C['Tecnologia'].notna()]

    Aparatos.reset_index()

    return Aparatos


def escenario(InfoEquipos, num):
    escena='esce'+str(num+1)
    InfoEsc = InfoEquipos.filter(regex=escena)
    InfoEsc = InfoEsc.fillna('X')
    if InfoEsc.filter(regex='lugar')[0] == 'otro':
        lugar = InfoEsc.filter(regex='lugar_extra')[0]
    else:
        lugar = InfoEsc.filter(regex='lugar')[0]

    lugar_especifico  = InfoEsc.filter(regex='donde_c_i')[0]
    tec             = InfoEsc.filter(regex='tecnologia')[0]
    fuga            = InfoEsc.filter(regex='fugaluces')[0]
    fugadetalles    = InfoEsc.filter(regex='fugaluces_detalles')[0]
    standby         = InfoEsc.filter(regex='standby')[0]
    sobreilum       = InfoEsc.filter(regex='sobreilum')[0]
    notas           = InfoEsc.filter(regex='notas')[0]
    pendiente       = InfoEsc.filter(regex='espendiente_c_i')[0]
    Consumo         = InfoEsc.filter(regex='noreportada_consumo')[0]


    if pendiente== 'si':
        if not InfoEsc.filter(regex='codigofindero2_c_i')[0]=='X':
            CodN      = InfoEsc.filter(regex='codigofindero_c_i')[0] + ', ' +str(InfoEsc.filter(regex='codigofindero2_c_i')[0])
        else:
            CodN      = InfoEsc.filter(regex='codigofindero_c_i')[0]
    else:
        CodN= InfoEsc.filter(regex='codigofinderoQQ_c_i')[0]


    return lugar, lugar_especifico, tec, fuga, fugadetalles, standby, sobreilum, notas, InfoEsc, pendiente,CodN,Consumo




