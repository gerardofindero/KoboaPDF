import pandas as pd
from Consumo    import calc_consumo
from Ahorro import  ahorro_luces
from Consumo    import calc_consumo , consumoEq
from Correciones import Lugar
import numpy as np


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
    lista=['incandescente','hal_geno','fluorescente','tira','led']
    listaTubos=['t2','t5','t8','t12']
    # Aparatos_C.loc[NombreVar, 'Datos' ]=''
####Lum1

    esc=True
    j=0
    while esc==True:
        lugar, lugar_especifico, tec, fuga, fugadetalles, standby, sobreilum, notas,InfoEsc=escenario(InfoEquipos,j)
        tec=tec.split()

        for i in tec:
            for k in lista:
                if i==k:
                    if k=='hal_geno':
                        k='halogenos'

                    tipo=k.capitalize()
                    Esc = 'E'+ str(j+1)

                    InfoLum = InfoEsc.filter(regex=k)
                    NombreVar=tipo+' '+Esc
                    InfoLum=InfoLum.fillna('X')
                    Aparatos_C.loc[NombreVar, 'Info']          = ''
                    Aparatos_C.loc[NombreVar, 'Datos']         = ''
                    Aparatos_C.loc[NombreVar, 'Tecnologia']   = k
                    Aparatos_C.loc[NombreVar, 'Lugar']        = Lugar(lugar)
                    Aparatos_C.loc[NombreVar, 'LugarES']      =lugar_especifico
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
                    Aparatos_C.loc[NombreVar, 'Combinacion']  = InfoLum.filter(regex='cobinacion')[0]
                    Aparatos_C.loc[NombreVar, 'Consumo']      = consumoEq(InfoLum.filter(regex='consumo')[0])
                    Aparatos_C.loc[NombreVar, 'DobCodigo']    = InfoLum.filter(regex='doblecodigo')[0]
                    Aparatos_C.loc[NombreVar, 'Forma' ] = 'F'
                    #Aparatos_C.loc['Incandecentes E1', 'Pendientes']    = InfoLum.filter(regex='otrospendientes_c_i')[0]

                    if InfoLum.filter(regex='doblecodigo')[0]=='no':
                        Aparatos_C.loc[NombreVar, 'CodigoN']      = InfoLum.filter(regex='codigofindero_')[0]
                    else:
                        Aparatos_C.loc[NombreVar, 'CodigoN']      = InfoLum.filter(regex='codigofindero2_')[0]

                    if InfoLum.filter(regex='otrospendientes')[0]=='si':
                        Aparatos_C.loc[NombreVar, 'CodigoN']      = Aparatos_C.loc[NombreVar, 'CodigoN']+\
                                                                            ', '+InfoLum.filter(regex='otroscodigos')[0]
                        Aparatos_C.loc[NombreVar, 'Notas']        = str(Aparatos_C.loc[NombreVar, 'Notas'])+\
                                                                     '. Otros codigos: '+InfoLum.filter(regex='otroscodigos')[0]


                    if not k=='led':
                        Aparatos_C.loc[NombreVar, 'Gasto']        = InfoLum.filter(regex='gasto')[0]
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
                            Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info'] +','+InfoLum.filter(regex='funcion')[0]+'/'
                        if 'cajillo' in InfoLum.filter(regex='donde_c_i')[0]:
                            Aparatos_C.loc[NombreVar, 'Info']         = '/CAJ_si_'+str(InfoLum.filter(regex='cajillo')[0])+'/'

                        if k== 'fluorescente':
                            if not InfoLum.filter(regex='disposicion')[0] == 'X':
                                Aparatos_C.loc[NombreVar, 'Disposicion']  = Aparatos_C.loc[NombreVar, 'Funcion']  +','+InfoLum.filter(regex='disposicion')[0]
                                Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info']+','+InfoLum.filter(regex='disposicion')[0]
                            if not InfoLum.filter(regex='deterioro')[0] == 'X':
                                Aparatos_C.loc[NombreVar, 'Info']         = Aparatos_C.loc[NombreVar, 'Info']+',/DET_'+InfoLum.filter(regex='deterioro')[0]+'/'

                        Aparatos_C.loc[NombreVar, 'Acceso']       = InfoLum.filter(regex='acceso')[0]
                        Aparatos_C.loc[NombreVar, 'Adecuaciones'] = InfoLum.filter(regex='adecuaciones')[0]
                        Aparatos_C.loc[NombreVar, 'Apagador']     = InfoLum.filter(regex='apagador')[0]
                        Aparatos_C.loc[NombreVar, 'Cantidad' ]    = str(Aparatos_C.loc[NombreVar, 'Numero'])


                        for l in range(4):
                            CantidadPL= 'portalamp'+str(l+1)+'_cantidad'
                            LargoPL   = 'portalamp'+str(l+1)+'_largo'
                            AnchoPL   = 'portalamp'+str(l+1)+'_ancho'
                            Portalamp = 'portalamp'+str(l+1)+'_c_i'
                            #CantidadPL= 'portalamp'+str(l+1)+'_cantidad'

                            cantidad = 'cantidad' +str(l+1)
                            funcion  = 'funcion' +str(l+1)
                            adicional= 'adicional' +str(l+1)
                            tipoytam = 'tipoytam' +str(l+1)
                            entrada  = 'entrada' +str(l+1)
                            disposicion  = 'disposicion' +str(l+1)
                            numero  = 'numero' +str(l+1)

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

                            if k== 'fluorescente':
                                if not InfoLum.filter(regex=disposicion)[0] == 'X':
                                    Aparatos_C.loc[NombreVar, 'Disposicion']        = Aparatos_C.loc[NombreVar, 'Funcion']  +','+InfoLum.filter(regex=funcion)[0]
                                    Aparatos_C.loc[NombreVar, 'Info']               = Aparatos_C.loc[NombreVar, 'Info']+','+InfoLum.filter(regex=disposicion)[0]
                                print(InfoLum.filter(regex=Portalamp)[0])
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
    if InfoEsc.filter(regex='lugar')[0] == 'otro':
        lugar = InfoEsc.filter(regex='lugar_extra')[0]
    else:
        lugar = InfoEsc.filter(regex='lugar')[0]
    lugar_especifico   = InfoEsc.filter(regex='lugar_especifico')[0]
    if lugar_especifico=='otro':
        lugar_especifico  = Lugar(InfoEsc.filter(regex='lugar_otro_c_i')[0])
    else:
        lugar_especifico  = Lugar(lugar_especifico)

    tec             = InfoEsc.filter(regex='tecnologia')[0]
    fuga            = InfoEsc.filter(regex='fugaluces')[0]
    fugadetalles    = InfoEsc.filter(regex='fugaluces_detalles')[0]
    standby         = InfoEsc.filter(regex='standby')[0]
    sobreilum       = InfoEsc.filter(regex='sobreilum')[0]
    notas           = InfoEsc.filter(regex='notas')[0]

    return lugar, lugar_especifico, tec, fuga, fugadetalles, standby, sobreilum, notas, InfoEsc




